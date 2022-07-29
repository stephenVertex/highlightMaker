#!/usr/bin/env python3

import requests
import shutil
import subprocess
import time
import os

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


def convert_image_to_video(local_fpath, output_fpath, t_duration = 2):
    y = subprocess.run(["./mk2k-still.sh", local_fpath, str(t_duration), output_fpath])
    return(y)

def secsToHMS(s):
    return(time.strftime('%H:%M:%S', time.gmtime(s)))


def trim_video(local_fpath, output_fpath, t_duration, t_offset = 0):
    y = subprocess.run(["./trim-video.sh", local_fpath, secsToHMS(t_offset), secsToHMS(t_duration), output_fpath])
    return(y)

def concat_videos(input_paths, output_fpath):
    #ffmpeg -i $1 -i $2 -filter_complex "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" $3
    # input_paths = ['d3/kkapr.mp4', 'd3/ms2.mp4', 'd3/twitter-end.mp4' ]
    n = len(input_paths)
    ffmpeg_cmds = ["ffmpeg"]

    for fp in input_paths:
        ffmpeg_cmds.append("-i")
        ffmpeg_cmds.append(fp)

    ffmpeg_cmds.append("-filter_complex")
    ixstr = []
    for i in range(n):
        ixstr.append(f"[{i}:v] [{i}:a]")
    ixstr.append(f"concat=n={n}:v=1:a=1 [v] [a]")
    filter_complex = " ".join(ixstr)

    ffmpeg_cmds.append(f"\"{filter_complex}\"")
    ffmpeg_cmds.append("-map")
    ffmpeg_cmds.append("\"[v]\"")
    ffmpeg_cmds.append("-map")
    ffmpeg_cmds.append("\"[a]\"")
    ffmpeg_cmds.append(output_fpath)


    y = subprocess.run(ffmpeg_cmds)
    return(y)

def trim_convert_append(
    local_base_fpath,
    local_output_fpath, 
    prev_image_fpath,
    t_duration,
    t_offset
):
    # Create paths
    base_name  = os.path.basename(local_base_fpath)
    base_noext, ext = os.path.splitext(local_base_fpath)
    trimmed_fpath = base_noext + "--trimmed" + ext
    imgvid_fpath = os.path.splitext(prev_image_fpath)[0] + ".mp4"
    # Do conversions
    print(f"Trimming, generating {trimmed_fpath}")
    y_t = trim_video(local_base_fpath, trimmed_fpath, t_duration, t_offset)

    y_i = convert_image_to_video(prev_image_fpath, output_fpath=imgvid_fpath)
    y_c = concat_videos(imgvid_fpath, trimmed_fpath, local_output_fpath)
    return(y_t, y_i, y_c)

def testTrim():
    local_base_fpath   = "d2/macie-recode.mp4"
    local_output_fpath = "d2/joined.mp4"
    prev_image_fpath   = "d2/kkapr.jpg"

    trim_convert_append(local_base_fpath, local_output_fpath, prev_image_fpath, 30, 15)
