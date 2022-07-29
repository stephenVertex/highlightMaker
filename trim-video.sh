#!/bin/bash

echo "TRIM VIDEO: $1"
echo "TRIM START: $2"
echo "TRIM DURATION: $3"
echo "OUTPUT FILE: $4"

ffmpeg -i $1 -ss $2 -t $3 -c:v copy -c:a copy $4

