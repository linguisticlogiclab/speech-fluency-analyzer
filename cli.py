"""Command line interface for speech fluency analysis."""

from __future__ import annotations

import argparse
import json
import sys

from speech_fluency import analyze_audio


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze speech fluency features from a WAV file."
    )
    parser.add_argument("audio_path", help="Path to input WAV file")
    parser.add_argument(
        "--top-db",
        type=int,
        default=30,
        help="Silence threshold in dB for non-silent split (default: 30)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = analyze_audio(args.audio_path, top_db=args.top_db)
    except Exception as exc:  # pragma: no cover - tiny CLI wrapper
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

