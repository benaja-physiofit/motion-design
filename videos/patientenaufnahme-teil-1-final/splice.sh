#!/bin/bash
# Keeps frames 0-1031 (0-17.2 s) of the original Teil-1 animation and appends the new ending,
# rendered losslessly as PNGs (renders/ende-frames), so both parts share one encode and match in colour.
#   npx hyperframes render --quality looks --fps 60 --format png-sequence --output renders/ende-frames
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -v error -y -i assets/original/teil-1-final.mp4 -framerate 60 -i renders/ende-frames/frame_%06d.png -filter_complex \
  "[0:v]trim=end_frame=1032,setpts=PTS-STARTPTS,format=rgb24[a];[1:v]setpts=PTS-STARTPTS,format=rgb24[b];[a][b]concat=n=2:v=1:a=0,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]" \
  -map "[v]" -r 60 -c:v libx264 -crf 14 -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -movflags +faststart renders/teil-1-final-neu.mp4
