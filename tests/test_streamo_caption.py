import json
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'streamo_caption'))
import streamo_caption as sc  # noqa: E402


def make_video(path, seconds, fps=25, size=(64, 48)):
    """Synthetic video whose frame brightness encodes the second it belongs to."""
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    for i in range(int(seconds * fps)):
        level = (int(i / fps) * 20) % 256
        writer.write(np.full((size[1], size[0], 3), level, np.uint8))
    writer.release()
    return str(path)


class ScriptedModel:
    """Mock model returning scripted answers and recording every request."""

    def __init__(self, answers):
        self.answers = list(answers)
        self.calls = []

    def __call__(self, messages, images):
        self.calls.append((messages, images))
        return self.answers[len(self.calls) - 1] if len(self.calls) <= len(self.answers) else '</Silence>'


@pytest.mark.parametrize('raw,expected', [
    ('</Silence>', ('silence', '')),
    ('</Standby>', ('standby', '')),
    ('</Response> A man jumps into the pool.', ('response', 'A man jumps into the pool.')),
    ('<Response>\n Two  lines\n here', ('response', 'Two lines here')),
    ('</Response>', ('response', '')),
    ('I think a man jumps.', ('unknown', 'I think a man jumps.')),
    ('', ('unknown', '')),
])
def test_parse_answer(raw, expected):
    assert sc.parse_answer(raw) == expected


def test_time_tag_keeps_streamo_integer_format():
    assert sc.time_tag(3, 4) == '<3s-4s>'
    assert sc.time_tag(1.5, 2.0) == '<1.5s-2s>'


def test_events_from_state_sequence():
    agg = sc.EventAggregator()
    seq = ['silence', 'standby', 'standby', 'response', 'silence', 'response', 'standby']
    for i, state in enumerate(seq):
        agg.update(i, i, i + 1, state, f'cap{i}' if state == 'response' else '')
    assert [(e.start, e.end, e.caption, e.standby_rounds) for e in agg.events] == [
        (1, 4, 'cap3', 2), (5, 6, 'cap5', 0)]
    assert agg.open_event() == {'start': 6, 'standby_rounds': 1}


def test_empty_response_does_not_create_event_but_closes_pending():
    agg = sc.EventAggregator()
    agg.update(0, 0, 1, 'standby', '')
    agg.update(1, 1, 2, 'response', '')
    assert agg.events == [] and agg.open_event() is None


def test_window_matches_official_protocol():
    rounds = [{'index': i, 'start': i, 'end': i + 1, 'image': f'img{i}', 'raw': f'a{i}'} for i in range(5)]
    rounds[-1]['raw'] = None
    msgs, imgs = sc.build_window('SYS', 'Q', rounds, max_rounds=3)
    assert imgs == ['img2', 'img3', 'img4']
    assert [m['role'] for m in msgs] == ['system', 'user', 'assistant', 'user', 'assistant', 'user']
    assert msgs[1]['content'] == 'Q\n<2s-3s>\n<image>'
    assert msgs[3]['content'] == '<3s-4s>\n<image>'
    assert msgs[-1]['content'] == '<4s-5s>\n<image>'
    # Without global_question the question only stays while round 0 is in the window.
    msgs, _ = sc.build_window('SYS', 'Q', rounds, max_rounds=3, global_question=False)
    assert not msgs[1]['content'].startswith('Q')
    msgs, _ = sc.build_window('SYS', 'Q', rounds, max_rounds=10, global_question=False)
    assert msgs[1]['content'] == 'Q\n<0s-1s>\n<image>'


def test_caption_video_end_to_end(tmp_path):
    video = make_video(tmp_path / 'v.mp4', seconds=6)
    model = ScriptedModel(['</Silence>', '</Standby>', '</Response> A light turns on.',
                           'not a state', '</Standby>', '</Standby>'])
    sampler = sc.VideoFrameSampler(video, fps=1.0)
    result = sc.caption_video(sampler, model, 'Q', max_rounds=2)
    sampler.close()
    assert result.num_rounds == 6 and len(model.calls) == 6
    # Window is bounded and frames come from the right second.
    for i, (msgs, imgs) in enumerate(model.calls):
        assert len(imgs) == min(i + 1, 2)
        assert np.asarray(imgs[-1]).mean() == pytest.approx(i * 20, abs=3)
    assert [(e.start, e.end, e.caption) for e in result.events] == [(1, 3, 'A light turns on.')]
    assert result.open_event == {'start': 4, 'standby_rounds': 2}
    assert result.stats['unknown_rounds'] == 1 and result.stats['model_calls'] == 6
    # History carries the raw previous answer, as in the official script.
    assert model.calls[3][0][-2] == {'role': 'assistant', 'content': '</Response> A light turns on.'}


def test_fps_controls_frame_times(tmp_path):
    video = make_video(tmp_path / 'v.mp4', seconds=3)
    model = ScriptedModel([])
    sampler = sc.VideoFrameSampler(video, fps=2.0)
    result = sc.caption_video(sampler, model, 'Q', max_rounds=4)
    sampler.close()
    assert result.num_rounds == 6
    assert [(r['start'], r['end']) for r in result.rounds][:3] == [(0, 0.5), (0.5, 1.0), (1.0, 1.5)]
    assert model.calls[2][0][-1]['content'] == '<1s-1.5s>\n<image>'
    assert np.asarray(model.calls[2][1][-1]).mean() == pytest.approx(20, abs=3)


def test_max_steps_and_short_video(tmp_path):
    video = make_video(tmp_path / 'v.mp4', seconds=0.5)
    sampler = sc.VideoFrameSampler(video)
    assert sampler.num_rounds == 0
    result = sc.caption_video(sampler, ScriptedModel([]), 'Q')
    assert result.events == [] and result.stats['model_calls'] == 0
    sampler.close()
    sampler = sc.VideoFrameSampler(make_video(tmp_path / 'w.mp4', seconds=5), fps=1.0)
    assert sc.caption_video(sampler, ScriptedModel([]), 'Q', max_steps=2).num_rounds == 2
    sampler.close()


def test_unreadable_video_raises(tmp_path):
    bad = tmp_path / 'bad.mp4'
    bad.write_bytes(b'not a video')
    with pytest.raises(ValueError):
        sc.VideoFrameSampler(str(bad))
    with pytest.raises(ValueError):
        sc.VideoFrameSampler(str(tmp_path / 'missing.mp4'))


def test_main_writes_jsonl_and_skips_bad_videos(tmp_path):
    video = make_video(tmp_path / 'v.mp4', seconds=3)
    bad = tmp_path / 'bad.mp4'
    bad.write_bytes(b'x')
    out = tmp_path / 'out' / 'captions.jsonl'
    model = ScriptedModel(['</Standby>', '</Response> Done.'])
    code = sc.main(['--model', 'mock', '--video', video, str(bad), '--output', str(out),
                    '--prompt', 'incremental', '--quiet'], generator=model)
    assert code == 1
    records = [json.loads(line) for line in out.read_text().splitlines()]
    assert len(records) == 1
    rec = records[0]
    assert rec['prompt'] == 'incremental' and rec['question'] == sc.PROMPTS['incremental']
    assert rec['events'] == [{'start': 0, 'end': 2.0, 'caption': 'Done.', 'standby_rounds': 1,
                              'response_round': 1, 'boundary_source': 'model_state'}]
    assert 'image' not in json.dumps(rec['rounds'][0])
