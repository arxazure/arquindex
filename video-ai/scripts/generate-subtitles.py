#!/usr/bin/env python3
"""Generate SRT subtitles from authorized audio using local Whisper."""
import argparse
from pathlib import Path
import math


def stamp(seconds):
    millis = round(seconds * 1000)
    h, remainder = divmod(millis, 3600000)
    m, remainder = divmod(remainder, 60000)
    s, ms = divmod(remainder, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def write_srt(segments, target):
    """Write validated, sequential UTF-8 cues; reject ambiguous overlaps."""
    cues = []
    previous_end = 0
    for index, segment in enumerate(segments, 1):
        start, end = segment["start"], segment["end"]
        if any(isinstance(t, bool) or not isinstance(t, (int, float)) or
               not math.isfinite(t) or t < 0 for t in (start, end)):
            raise ValueError("Cue times must be finite nonnegative numbers")
        start_ms, end_ms = round(start * 1000), round(end * 1000)
        if start_ms < previous_end or end_ms <= start_ms:
            raise ValueError("Cues must be ordered, nonoverlapping and positive in duration")
        text = " ".join(segment["text"].split())
        if not text or "-->" in text:
            raise ValueError("Cue text must be nonempty and contain no timing delimiter")
        cues.append(f"{index}\n{stamp(start)} --> {stamp(end)}\n{text}\n\n")
        previous_end = end_ms
    if not cues:
        raise ValueError("No subtitle cues")
    Path(target).write_text("".join(cues), encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("--model", default="base")
    parser.add_argument("--language", default="pt")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.audio.is_file():
        parser.error("Audio file does not exist")
    import whisper  # Optional dependency: tests and SRT writing do not need a model.
    model = whisper.load_model(args.model)
    result = model.transcribe(str(args.audio), language=args.language, fp16=False)
    target = args.output or args.audio.with_suffix(".srt")
    write_srt(result["segments"], target)
    print(target)


if __name__ == "__main__":
    main()
