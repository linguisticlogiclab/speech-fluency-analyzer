# Speech Fluency Analyzer

A lightweight Python toolkit for analyzing speech fluency features from audio.

## Features

- speech duration
- silence ratio
- pause detection
- speech segments

Input: one `.wav` file  
Output: JSON fluency metrics

```json
{
  "speech_duration": 25.3,
  "silence_ratio": 0.18,
  "pause_count": 6,
  "avg_pause_length": 0.42,
  "speech_segments": 7
}
```

## Project Structure

```text
speech-fluency-analyzer/
├── speech_fluency/
│   ├── __init__.py
│   └── analyzer.py
├── cli.py
├── demo.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### CLI

```bash
python cli.py example.wav
```

Optional:

```bash
python cli.py example.wav --top-db 30
```

### Python API

```python
from speech_fluency import analyze_audio

result = analyze_audio("example.wav")
print(result)
```

### Demo

```bash
python demo.py
```

## Metrics Definition

- `speech_duration`: total non-silent speech time (seconds)
- `silence_ratio`: silence time / total audio time
- `pause_count`: number of pauses between adjacent speech segments
- `avg_pause_length`: average pause length (seconds)
- `speech_segments`: number of detected non-silent segments

## Open Source License

MIT License. See [LICENSE](./LICENSE).

## Project Background

This tool was originally developed during the development of Cosu, an AI speaking coach designed for TOEFL and IELTS speaking practice.

