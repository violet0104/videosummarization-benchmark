# Streamo 流式 event caption（免训练推理）

`streamo_caption.py` 按 [Streamo](https://github.com/maifoundations/Streamo)（`6d1f1ab`）官方推理协议逐帧读取视频：每轮输入一帧和 `<Xs-Ys>` 时间标签，模型回答 `</Silence>`、`</Standby>` 或 `</Response> 描述`。脚本把这些回答整理成带时间戳的事件 caption，并输出 JSONL。

> Streamo 官方目前**未公开模型权重**。拿到作者提供的 checkpoint 前，可用公开的 `Qwen/Qwen2.5-VL-3B-Instruct`（Streamo 的训练起点）跑通流程。这样得到的是 **Qwen prompt-only baseline**，不能当作 Streamo 的复现结果。

## 相对官方 `inference.py` 的改动

- 消息窗口与官方 `get_data_stream_video_window` 逐条一致（1 fps 下已对照验证），系统提示词原样保留。
- 取帧时间为 `round / fps`；官方脚本固定读取第 `round` 秒，只改 `target_fps` 时，帧和时间标签会错位。Streamo 训练时使用 1 fps 和整数秒标签，其他采样率未经验证。
- 解析每轮状态，并把 Response 转成事件 `(start, end, caption)`。
- 记录每轮状态、原始输出、延迟，以及帧数、模型调用次数和总耗时。
- `--prompt incremental` 使用 `task/task.md` 中“只描述新增信息”的增量 caption 指令；默认 `event` 使用官方 demo 指令。

## 环境（Linux + NVIDIA GPU）

依赖 Streamo 仓库自带的修改版 `swift`，版本约束沿用 VA-7 中整理的配置：

```bash
conda create -n streamo python=3.10 pip -y
conda activate streamo
python -m pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124

git clone https://github.com/maifoundations/Streamo.git
cd Streamo && git checkout --detach 6d1f1ab59ea037505a068c96d222c9e0a4e45e43
cat > constraints-streamo.txt <<'EOF'
torch==2.6.0
torchvision==0.21.0
transformers==4.57.1
huggingface-hub==0.36.0
qwen-vl-utils==0.0.11
accelerate==1.10.1
peft==0.17.1
trl==0.23.1
numpy==1.26.4
EOF
python -m pip install -c constraints-streamo.txt -e . qwen-vl-utils decord==0.6.0 opencv-python-headless==4.11.0.86 msgspec  # msgspec: swift imports it but Streamo does not declare it
cd ..

# 没有 Streamo checkpoint 时下载公开基线模型
hf download Qwen/Qwen2.5-VL-3B-Instruct --local-dir ./models/Qwen2.5-VL-3B-Instruct
```

## 运行

```bash
# 冒烟测试：只跑前 30 秒
python streamo_caption/streamo_caption.py \
    --model ./models/Qwen2.5-VL-3B-Instruct \
    --video Streamo/demo/cook.mp4 \
    --output outputs/streamo_captions.jsonl \
    --max-steps 30

# 完整视频，增量 caption 指令
python streamo_caption/streamo_caption.py \
    --model /path/to/streamo_checkpoint \
    --video a.mp4 b.mp4 \
    --output outputs/streamo_captions.jsonl \
    --prompt incremental --max-rounds 16
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--backend` | `pt` | `pt`：PyTorch + SDPA；`vllm`：需另装 vLLM |
| `--max-rounds` | 16 | 滑动窗口保留的轮数（帧数）；官方 demo 用 300。显存不足时调小，但可见历史也会变短 |
| `--max-steps` | 全部 | 只处理前 N 轮，用于调试 |
| `--fps` | 1.0 | 采样率；建议保持 1 |
| `--question` | — | 自定义指令，覆盖 `--prompt` |

每个视频运行一轮需调用一次模型：1 小时视频在 1 fps 下要调用 3600 次。

## 输出

每个视频向 `--output` 追加一行 JSON：

```json
{
  "model": "...", "prompt": "event", "question": "...", "max_rounds": 16,
  "video_path": "a.mp4", "duration": 190.583, "fps": 1.0, "num_rounds": 190,
  "rounds": [{"index": 0, "start": 0, "end": 1, "state": "silence", "text": "", "raw": "</Silence>", "latency_s": 0.41}],
  "events": [{"start": 12, "end": 18, "caption": "...", "standby_rounds": 5, "response_round": 17, "boundary_source": "model_state"}],
  "open_event": null,
  "stats": {"frames": 190, "model_calls": 190, "total_latency_s": 80.2, "silence_rounds": 120, "standby_rounds": 55, "response_rounds": 14, "unknown_rounds": 1, "events": 14}
}
```

- 事件起点：上次 Response 后首个 Standby 的开始时间；没有 Standby 时用 Response 当轮的开始时间。事件终点：Response 当轮的结束时间。边界由模型状态推出，**不是真值**，用作 benchmark 参考答案前需另行校验。
- `open_event`：视频结束时仍处于 Standby、尚未输出描述的事件。
- 没有状态标记的回答记为 `unknown`，不生成事件；原文保留在 `rounds[].raw`。
- 输出含模型生成的视频描述，默认写入 `outputs/`（已加入 `.gitignore`），不要提交。

## 测试

测试使用合成视频和 mock 模型，不需要 GPU、模型权重或 `swift`：

```bash
python -m pip install pytest opencv-python-headless numpy pillow
python -m pytest tests
```
