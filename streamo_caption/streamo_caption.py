"""Generate streaming event captions with Streamo (no training, inference only).

Follows the official Streamo inference protocol (maifoundations/Streamo@6d1f1ab,
``inference.py``): one frame per round, each user turn tagged ``<Xs-Ys>``, a
sliding window of past rounds, and the model answers ``</Silence>``,
``</Standby>`` or ``</Response> <caption>``. On top of that this script

* samples frames at the real time ``round / fps`` (the official script reads
  ``round`` seconds regardless of ``target_fps``);
* parses every answer into a state and turns ``</Response>`` answers into
  events ``(start, end, caption)``;
* records per-round latency and cost counters;
* writes one JSON record per video.

Event boundaries are derived from the model's state sequence: an event starts
at the first ``</Standby>`` after the previous ``</Response>`` (or at the
responding round when no Standby preceded it) and ends at the end of the
responding round. They are model predictions, not ground-truth boundaries.

Usage (see README.md for environment setup)::

    python streamo_caption/streamo_caption.py \
        --model /path/to/streamo_or_qwen2.5-vl --video demo.mp4 \
        --output outputs/captions.jsonl
"""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional

# Same visual token budget as the official Streamo inference script.
os.environ.setdefault('MIN_PIXELS', '3136')
os.environ.setdefault('MAX_PIXELS', '100352')

# Verbatim from Streamo inference.py; the model was trained with this prompt.
SYSTEM = """
You are a helpful assistant specializing in streaming video analysis.
You will receive input frame by frame, each labeled with absolute time intervals
in the exact format <Xs-Ys> (e.g., <0s-1s>). Follow these rules precisely:

1. Use </Silence> when:
   - No relevant event has started, OR
   - The current input is irrelevant to the given question.

2. Use </Standby> when:
   - An event is in progress but has not yet completed, OR
   - The current input is relevant but the question cannot yet be answered.

3. Use </Response> only when:
   - An event has fully concluded, OR
   - The available information is sufficient to fully answer the question.
   Provide a complete description at this point.

Do not provide partial answers or speculate beyond the given information.
Whenever you deliver an answer, begin with </Response>.
"""

PROMPTS = {
    # Event-caption instruction used by the official Streamo demo.
    'event': 'Detect and summarize each event sequence in the video.',
    # Incremental caption instruction from task/task.md (9.23 notes).
    'incremental': (
        'Detect each new event in the video. When an event has concluded, describe only the visual '
        'information that is new compared with your previous descriptions: newly appearing people, '
        'objects or scenes; new actions of existing people or objects; changes of state; and new '
        'interactions or events. Do not repeat information that was already described and is '
        'unchanged, do not describe the mere continuation of the same action or state, and do not '
        're-describe an object only because it is still visible.'),
}

SILENCE, STANDBY, RESPONSE, UNKNOWN = 'silence', 'standby', 'response', 'unknown'
_STATE_RE = re.compile(r'<\s*/?\s*(Silence|Standby|Response)\s*>', re.IGNORECASE)

# generate(messages, images) -> raw model answer
Generator = Callable[[List[Dict[str, str]], list], str]


def parse_answer(raw: str):
    """Return ``(state, text)`` for one model answer.

    The first state token wins; ``text`` is whatever follows a Response token.
    Answers without any state token are ``unknown`` and never become events.
    """
    m = _STATE_RE.search(raw or '')
    if m is None:
        return UNKNOWN, (raw or '').strip()
    state = m.group(1).lower()
    if state != RESPONSE:
        return state, ''
    text = _STATE_RE.sub(' ', raw[m.end():])
    return RESPONSE, ' '.join(text.split())


def fmt_time(t: float) -> str:
    """Time tag value: ``3`` for whole seconds (Streamo's trained format), else ``3.5``."""
    t = round(t, 3)
    return str(int(t)) if t == int(t) else f'{t:g}'


def time_tag(start: float, end: float) -> str:
    return f'<{fmt_time(start)}s-{fmt_time(end)}s>'


class VideoFrameSampler:
    """Uniformly samples frames at ``fps``; round ``i`` covers ``[i/fps, (i+1)/fps)``."""

    def __init__(self, video_path: str, fps: float = 1.0):
        import cv2
        if fps <= 0:
            raise ValueError(f'fps must be positive, got {fps}')
        self._cv2 = cv2
        self.video_path = video_path
        self.fps = fps
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f'Cannot open video: {video_path}')
        self.video_fps = self.cap.get(cv2.CAP_PROP_FPS) or 0.0
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.video_fps <= 0 or self.total_frames <= 0:
            self.close()
            raise ValueError(f'Video has no readable frames or fps: {video_path}')
        self.duration = self.total_frames / self.video_fps
        self.num_rounds = int(self.duration * fps)

    def interval(self, i: int):
        return i / self.fps, min((i + 1) / self.fps, self.duration)

    def frame(self, i: int):
        from PIL import Image
        start, _ = self.interval(i)
        idx = min(int(round(start * self.video_fps)), self.total_frames - 1)
        self.cap.set(self._cv2.CAP_PROP_POS_FRAMES, idx)
        ok, bgr = self.cap.read()
        if not ok:
            raise ValueError(f'Cannot read frame {idx} ({start:.3f}s) from {self.video_path}')
        return Image.fromarray(self._cv2.cvtColor(bgr, self._cv2.COLOR_BGR2RGB))

    def close(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None


def build_window(system: str, question: str, rounds: List[dict], max_rounds: int,
                 global_question: bool = True, question_round: int = 0):
    """Messages and images for the latest round, keeping the last ``max_rounds`` rounds.

    Mirrors ``get_data_stream_video_window``: the question goes into the first
    user turn of the window (always with ``global_question``), otherwise only
    into the turn of ``question_round``; earlier answers are kept as assistant turns.
    """
    window = rounds[-max_rounds:]
    messages = [{'role': 'system', 'content': system}] if system else []
    for k, r in enumerate(window):
        with_q = r['index'] == question_round or (k == 0 and global_question)
        tag = f"{time_tag(r['start'], r['end'])}\n<image>"
        messages.append({'role': 'user', 'content': f'{question}\n{tag}' if with_q else tag})
        if r.get('raw') is not None:
            messages.append({'role': 'assistant', 'content': r['raw']})
    return messages, [r['image'] for r in window]


@dataclass
class Event:
    start: float
    end: float
    caption: str
    standby_rounds: int
    response_round: int
    boundary_source: str = 'model_state'


@dataclass
class CaptionResult:
    video_path: str
    duration: float
    fps: float
    num_rounds: int
    rounds: List[dict] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    open_event: Optional[dict] = None
    stats: Dict[str, float] = field(default_factory=dict)


class EventAggregator:
    """Turns the per-round state sequence into timestamped events."""

    def __init__(self):
        self.events: List[Event] = []
        self._pending_start: Optional[float] = None
        self._pending_rounds = 0

    def update(self, index: int, start: float, end: float, state: str, text: str):
        if state == STANDBY:
            if self._pending_start is None:
                self._pending_start = start
            self._pending_rounds += 1
        elif state == RESPONSE:
            ev_start = start if self._pending_start is None else self._pending_start
            if text:
                self.events.append(Event(ev_start, end, text, self._pending_rounds, index))
            self._pending_start, self._pending_rounds = None, 0

    def open_event(self) -> Optional[dict]:
        """Standby run that never reached a Response before the video ended."""
        if self._pending_start is None:
            return None
        return {'start': self._pending_start, 'standby_rounds': self._pending_rounds}


def caption_video(sampler, generate: Generator, question: str, system: str = SYSTEM,
                  max_rounds: int = 16, max_steps: Optional[int] = None,
                  global_question: bool = True, verbose: bool = False) -> CaptionResult:
    """Run the Streamo streaming loop over one video, one model call per sampled frame."""
    n = sampler.num_rounds if max_steps is None else min(max_steps, sampler.num_rounds)
    result = CaptionResult(sampler.video_path, round(sampler.duration, 3), sampler.fps, n)
    agg = EventAggregator()
    history: List[dict] = []
    counts = {SILENCE: 0, STANDBY: 0, RESPONSE: 0, UNKNOWN: 0}
    total_latency = 0.0
    for i in range(n):
        start, end = sampler.interval(i)
        history.append({'index': i, 'start': start, 'end': end, 'image': sampler.frame(i), 'raw': None})
        history = history[-max_rounds:]
        messages, images = build_window(system, question, history, max_rounds, global_question)
        t0 = time.perf_counter()
        raw = generate(messages, images)
        latency = time.perf_counter() - t0
        total_latency += latency
        history[-1]['raw'] = raw
        state, text = parse_answer(raw)
        counts[state] += 1
        agg.update(i, start, end, state, text)
        result.rounds.append({'index': i, 'start': round(start, 3), 'end': round(end, 3),
                              'state': state, 'text': text, 'raw': raw,
                              'latency_s': round(latency, 4)})
        if verbose:
            print(f'{time_tag(start, end)} {raw}', flush=True)
    result.events = agg.events
    result.open_event = agg.open_event()
    result.stats = {'frames': n, 'model_calls': n, 'window_rounds': max_rounds,
                    'total_latency_s': round(total_latency, 3),
                    **{f'{k}_rounds': v for k, v in counts.items()},
                    'events': len(agg.events)}
    return result


def make_swift_generator(model: str, backend: str = 'pt', max_tokens: int = 512,
                         max_model_len: int = 32768) -> Generator:
    """Generator backed by the ``swift`` package shipped in the Streamo repository."""
    from swift.llm import InferRequest, RequestConfig
    if backend == 'pt':
        import torch
        from swift.llm import PtEngine
        if torch.cuda.is_available():
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        else:
            dtype = torch.float32
        engine = PtEngine(model, torch_dtype=dtype, max_batch_size=1, attn_impl='sdpa')
    elif backend == 'vllm':
        from swift.llm import VllmEngine
        engine = VllmEngine(model, max_model_len=max_model_len, limit_mm_per_prompt={'image': 500},
                            tensor_parallel_size=1, enable_prefix_caching=True)
    else:
        raise ValueError(f'Unknown backend: {backend}')
    config = RequestConfig(max_tokens=max_tokens, temperature=0.0)

    def generate(messages, images):
        resp = engine.infer([InferRequest(messages=messages, images=images)], config)
        return resp[0].choices[0].message.content

    return generate


def to_record(result: CaptionResult, meta: dict) -> dict:
    record = {**meta, **asdict(result)}
    record['events'] = [{**e, 'start': round(e['start'], 3), 'end': round(e['end'], 3)}
                        for e in record['events']]
    return record


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument('--model', required=True, help='Streamo checkpoint or Qwen2.5-VL directory / HF id')
    p.add_argument('--video', required=True, nargs='+', help='One or more video files')
    p.add_argument('--output', required=True, help='JSONL file; one record per video is appended')
    p.add_argument('--backend', default='pt', choices=['pt', 'vllm'])
    p.add_argument('--prompt', default='event', choices=sorted(PROMPTS),
                   help='event: official Streamo instruction; incremental: task.md incremental caption')
    p.add_argument('--question', default=None, help='Custom instruction (overrides --prompt)')
    p.add_argument('--fps', type=float, default=1.0,
                   help='Sampling rate; Streamo was trained with 1 fps / integer-second tags')
    p.add_argument('--max-rounds', type=int, default=16, help='Sliding window size in rounds')
    p.add_argument('--max-steps', type=int, default=None, help='Only process the first N rounds')
    p.add_argument('--max-tokens', type=int, default=512)
    p.add_argument('--quiet', action='store_true')
    return p.parse_args(argv)


def main(argv=None, generator: Optional[Generator] = None):
    args = parse_args(argv)
    if args.max_rounds < 1:
        raise SystemExit('--max-rounds must be >= 1')
    question = args.question or PROMPTS[args.prompt]
    if args.fps != 1.0:
        print('warning: Streamo was trained on 1 fps integer-second tags; other rates are untested',
              file=sys.stderr)
    generate = generator or make_swift_generator(args.model, args.backend, args.max_tokens)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    meta = {'model': args.model, 'backend': args.backend, 'prompt': 'custom' if args.question else args.prompt,
            'question': question, 'max_rounds': args.max_rounds}
    failures = 0
    for video in args.video:
        try:
            sampler = VideoFrameSampler(video, args.fps)
        except ValueError as e:
            print(f'skip: {e}', file=sys.stderr)
            failures += 1
            continue
        try:
            result = caption_video(sampler, generate, question, max_rounds=args.max_rounds,
                                   max_steps=args.max_steps, verbose=not args.quiet)
        finally:
            sampler.close()
        with open(args.output, 'a', encoding='utf-8') as f:
            f.write(json.dumps(to_record(result, meta), ensure_ascii=False) + '\n')
        print(f'{video}: {len(result.events)} events, {result.num_rounds} rounds, '
              f"{result.stats['total_latency_s']}s model time -> {args.output}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
