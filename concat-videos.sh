#!/bin/bash

echo "Video concatenator"
echo "VID.1: $1"
echo "VID.2: $2"


## This is the concat demuxer
ffmpeg -i $1 -i $2 -filter_complex "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" output.mkv

## We can then use handbrake-cli to fix it up
