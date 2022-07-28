#!/bin/bash

# Inputs: 
#  JPG file
#  Duration in seconds
#  MP4 output file name
# ./mk2k-still.sh donut.jpg 2 donut-vid.mp4

ffmpeg -framerate 30 -i $1 -t $2 \
    -c:v libx265 -x265-params lossless=1 \
    -pix_fmt yuv420p -vf "scale=1920:1080,loop=-1:1" \
    -movflags faststart \
    $3