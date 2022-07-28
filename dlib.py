#!/usr/bin/env python3

import requests
import shutil

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


def convert_image_to_video(local_fpath, t_duration = 2):
    