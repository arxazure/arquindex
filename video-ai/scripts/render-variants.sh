#!/bin/sh
set -eu
mkdir -p out
npm run render:sample
ffmpeg -hide_banner -loglevel error -y -i out/arquindex-promo.mp4 -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -pix_fmt yuv420p -crf 22 -an -movflags +faststart out/arquindex-square.mp4
ffmpeg -hide_banner -loglevel error -y -i out/arquindex-promo.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -pix_fmt yuv420p -crf 22 -an -movflags +faststart out/arquindex-landscape.mp4
