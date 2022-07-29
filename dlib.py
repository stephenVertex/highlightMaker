#!/usr/bin/env python3

import requests
import shutil
import subprocess
import time
import os
from pymediainfo import MediaInfo
from collections import namedtuple
import uuid


VidData = namedtuple("VidData", ["remote_uri", "duration_s"])


## ------------------------------------------------------------------
## We may assume that we know this outside this function
def make_video_data(local_path):
    ## Upload the video to s3
    # 
    return(VidData(remote_uri, duration_s))

## ------------------------------------------------------------------
def make_image_clip(image_uri):
    return({
                "asset": {
                    "type": "image",
                    "src": image_uri
                },
                "start": 0,
                "length": 2,
                "effect": "zoomIn",
                "transition": {
                    "in": "fade",
                    "out": "fade"
                }
         })

## ------------------------------------------------------------------
def make_vid_clip(vid_uri, start, duration):
    return({
              "asset": {
                "type": "video",
                "src": vid_uri
              },
              "start": start,
              "length": duration
            })


## ------------------------------------------------------------------
def construct_highlight_video(thumbnail_uri, vid_data):
    # Get vids locally
    # Get their duration


    image_time = 2

    tracks = []
    tracks.append({"clips": [make_image_clip(thumbnail_uri)]})

    start_time = image_time
    for v in vid_data:
        tracks.append({"clips" : [make_vid_clip(v.remote_uri, start_time, v.duration_s)]})
        start_time = start_time = v.duration_s

    req_data = { "timeline" : { "tracks" : tracks},
                 "output": { 
                     "format" : "mp4",
                     "resolution" : "sd"
                 }
                }
    print(req_data)



def test_construct():
    vid_1 = VidData(remote_uri="https://devgraph-aws-made-easy.s3.amazonaws.com/hl-auto/macie-recode.mp4", duration_s=481)
    vid_2 = VidData(remote_uri= "https://devgraph-aws-made-easy.s3.amazonaws.com/hl-auto/twitter-end.mp4", duration_s=5)
    thumbnail_uri = "https://devgraph-aws-made-easy.s3.amazonaws.com/hl-auto/macie-thumb.jpeg"
    construct_highlight_video(thumbnail_uri, [vid_1, vid_2])
    return None
