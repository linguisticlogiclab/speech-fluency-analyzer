"""Small demo for programmatic usage."""

from __future__ import annotations

import json
from pathlib import Path

from speech_fluency import analyze_audio


def main() -> None:
    example = Path("example.wav")
    if not example.exists():
        print("Please put a WAV file named 'example.wav' in the project root.")
        return

    metrics = analyze_audio(str(example))
    print("Speech fluency metrics:")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

