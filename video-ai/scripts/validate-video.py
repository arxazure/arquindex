#!/usr/bin/env python3
"""Probe and decode the entire sample, failing on incompatible output."""
import json
from pathlib import Path
import subprocess
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'out/arquindex-promo.mp4')
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
video = [s for s in probe['streams'] if s['codec_type'] == 'video']
if len(video) != 1:
    raise SystemExit('Expected one video stream')
s = video[0]
checks = [(s['width'], 1080), (s['height'], 1920), (s['avg_frame_rate'], '30/1'),
          (s['codec_name'], 'h264'), (s['pix_fmt'], 'yuv420p'), (int(s['nb_frames']), 450)]
if any(actual != expected for actual, expected in checks) or abs(float(probe['format']['duration']) - 15) > 1/30:
    raise SystemExit(f'Unexpected sample properties: {checks}')
subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'], check=True)
print(json.dumps(probe, indent=2))
