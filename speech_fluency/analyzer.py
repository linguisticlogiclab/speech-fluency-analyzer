"""Core fluency feature extraction from a WAV file."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import librosa
import numpy as np


def _safe_float(value: float) -> float:
    """Convert to plain float and avoid tiny negative values from precision."""
    return max(float(value), 0.0)


def analyze_audio(audio_path: str, top_db: int = 30) -> Dict[str, float | int]:
    """
    Analyze a speech WAV file and return basic fluency metrics.

    Parameters
    ----------
    audio_path:
        Path to a WAV audio file.
    top_db:
        The threshold (in decibels) below reference to consider as silence.

    Returns
    -------
    dict
        JSON-serializable metrics:
        - speech_duration
        - silence_ratio
        - pause_count
        - avg_pause_length
        - speech_segments
    """
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # 1) Load audio
    y, sr = librosa.load(path, sr=None, mono=True)
    if y.size == 0:
        raise ValueError(f"Audio file is empty: {audio_path}")

    # 2) Total duration (seconds)
    total_duration = _safe_float(librosa.get_duration(y=y, sr=sr))
    if total_duration == 0:
        raise ValueError(f"Audio duration is zero: {audio_path}")

    # 3) Detect non-silent intervals in samples, shape: (n_segments, 2)
    intervals = librosa.effects.split(y, top_db=top_db)
    speech_segments = int(len(intervals))

    if speech_segments == 0:
        return {
            "speech_duration": 0.0,
            "silence_ratio": 1.0,
            "pause_count": 0,
            "avg_pause_length": 0.0,
            "speech_segments": 0,
        }

    # 4) Metrics
    speech_durations = (intervals[:, 1] - intervals[:, 0]) / sr
    speech_duration = _safe_float(np.sum(speech_durations))

    silence_duration = _safe_float(total_duration - speech_duration)
    silence_ratio = silence_duration / total_duration

    # Pause = silence gap between two consecutive speech segments.
    if speech_segments > 1:
        gap_starts = intervals[1:, 0] / sr
        gap_ends = intervals[:-1, 1] / sr
        pause_durations = np.maximum(gap_starts - gap_ends, 0.0)
    else:
        pause_durations = np.array([], dtype=float)

    pause_count = int(len(pause_durations))
    avg_pause_length = _safe_float(np.mean(pause_durations)) if pause_count else 0.0

    return {
        "speech_duration": round(speech_duration, 3),
        "silence_ratio": round(float(silence_ratio), 3),
        "pause_count": pause_count,
        "avg_pause_length": round(avg_pause_length, 3),
        "speech_segments": speech_segments,
    }

