#!/bin/sh
set -eu
if [ "$#" -ne 2 ]; then
  echo "Usage: sh scripts/prepare-social.sh input.mp4 output.mp4" >&2
  exit 2
fi
ffmpeg -hide_banner -y -i "$1" -c:v libx264 -pix_fmt yuv420p -crf 22 -preset medium -c:a aac -b:a 128k -movflags +faststart "$2"
