#!/usr/bin/env python3

import requests
import shutil
import subprocess
import time
import os
from pymediainfo import MediaInfo
from collections import namedtuple
import uuid
import shotstack 
import sjbs3

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
                "transition": {
                    "in": "fade",
                    "out": "fade"
                }
         })

## ------------------------------------------------------------------
def make_vid_clip(vid_uri, start, duration, trim = 0):
    return({
              "asset": {
                "type": "video",
                "src": vid_uri,
                "volume" : 1,
                "trim" : trim
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
        start_time = start_time + v.duration_s

    req_data = { "timeline" : { "tracks" : tracks},
                 "output": { 
                     "format" : "mp4",
                     "resolution" : "sd"
                 }
                }
    print(req_data)
    return(shotstack.test_merge(req_data))


def construct_highlight_video_short(thumbnail_uri, vid_data):
    # Get vids locally
    # Get their duration


    image_time = 2

    tracks = []
    tracks.append({"clips": [make_image_clip(thumbnail_uri)]})

    start_time = image_time
    for v in vid_data:
        eff_duration = min(v.duration_s, 30)
        if v.duration_s > 30:
            tracks.append({"clips" : [make_vid_clip(v.remote_uri, start_time, eff_duration, trim=30)]})            
        else:
            tracks.append({"clips" : [make_vid_clip(v.remote_uri, start_time, eff_duration)]})
        start_time = start_time + eff_duration

    req_data = { "timeline" : { "tracks" : tracks},
                 "output": { 
                     "format" : "mp4",
                     "resolution" : "sd"
                 }
                }
    print(req_data)
    return(shotstack.test_merge(req_data))

def test_construct():
    vid_1 = VidData(remote_uri="https://devgraph-aws-made-easy.s3.amazonaws.com/hl-auto/macie-recode.mp4", duration_s=481)
    vid_2 = VidData(remote_uri= "https://devgraph-aws-made-easy.s3.amazonaws.com/hl-auto/twitter-end.mp4", duration_s=5)
    thumbnail_uri = "https://devgraph-aws-made-easy.s3.amazonaws.com/hl-auto/macie-thumb.jpeg"
    r = construct_highlight_video_short(thumbnail_uri, [vid_1, vid_2])
    return None



def download_file(remote_url, local_fpath):
    # URL of the image to be downloaded is defined as image_url
    r = requests.get(remote_url) # create HTTP response object

    # send a HTTP request to the server and save
    # the HTTP response in a response object called r
    with open(local_fpath,'wb') as f:
        # Saving received content as a png file in
        # binary format
        # write the contents of the response (r.content)
        # to a new file in binary mode.
        f.write(r.content)

def do_fn(thumb_uri, main_uri):
    vid_1 = VidData(remote_uri=main_uri, duration_s=481)
    vid_2 = VidData(remote_uri= "https://devgraph-aws-made-easy.s3.amazonaws.com/hl-auto/twitter-end.mp4", duration_s=5)
    r = construct_highlight_video_short(thumb_uri, [vid_1, vid_2])
    xid = r.json()['response']['id']

    r = shotstack.check_render(xid)    
    while(r.json()['response']['status'] != 'done'):
        time.sleep(30)
        r = shotstack.check_render(xid)
    url = r.json()['response']['url']

    ur = str(uuid.uuid4()).split('-')[1]
    fname_local = os.path.splitext(main_uri.split('/')[-1])[0] + "--twitterclip-" + ur + ".mp4"
    download_file(url, fname_local)
    sjbs3.upload_file(fname_local, "devgraph-aws-made-easy", object_name="hl-auto/" + fname_local)

    print("NEW URI:")
    new_uri = f"https://devgraph-aws-made-easy.s3.amazonaws.com/hl-auto/{fname_local}"
    print(new_uri)

import csv

def do_loop():
    with open('hl-map.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            print("--------------")
            print(row[1])
            thumb = row[3]
            main_v = row[4]
            print(thumb)
            print(main_v)
            if thumb == "thumbnail":
                continue
            do_fn(thumb, main_v)