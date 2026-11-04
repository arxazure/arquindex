#!/usr/bin/env python3
"""Generate SRT subtitles from authorized audio using local Whisper."""
import argparse
from pathlib import Path
import whisper


def stamp(seconds):
    millis = round(seconds * 1000)
    h, remainder = divmod(millis, 3600000)
    m, remainder = divmod(remainder, 60000)
    s, ms = divmod(remainder, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("--model", default="base")
    parser.add_argument("--language", default="pt")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.audio.is_file():
        parser.error("Audio file does not exist")
    model = whisper.load_model(args.model)
    result = model.transcribe(str(args.audio), language=args.language, fp16=False)
    target = args.output or args.audio.with_suffix(".srt")
    with target.open("w", encoding="utf-8") as file:
        for index, segment in enumerate(result["segments"], 1):
            file.write(f'{index}\\n{stamp(segment["start"])} --> {stamp(segment["end"])}\\n{segment["text"].strip()}\\n\\n')
    print(target)


if __name__ == "__main__":
    main()
