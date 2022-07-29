# Generate Highlights Video

## Functionality

This function does video processing for making highlights videos.
In particular, it does:

(1) Create a "preview" video suitable for Twitter. This preview takes the following inputs

- `T_thumb` seconds of thumbnail.
- `postamble_video` S3 path to postamble video. This is going to be a 2 second video that says "for the full video, click here!"
- `T_main` how many seconds of the main video to include. Default is 30 seconds.

(2) Create a full length one for LinkedIn live

- `T_thumb` seconds of thumbnail



## Inputs


```json
{
    "T_thumb"   : 2,
    "main_video_url" : "https://.....",
    "preamble_video_url" : "https://....",
    "destination_s3_bucket" : "s3://some-bucket-name",
    "destination_s3_prefix" : "some/special/path"
}
```

## Outputs

```json
{    
    "preview_video_url" : "https://s3-.....",
    "preview_video_s3_uri" : "s3://....",
    "full_video_url" : "https://s3-",
    "full_video_s3_uri" : "s3://...."
}
```

## How to

- Convert and image to video: https://shotstack.io/learn/use-ffmpeg-to-convert-images-to-video/ 

- Trimming video: https://shotstack.io/learn/use-ffmpeg-to-trim-video/

- Concatenate mp4 files: https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg

# Notes

I need to upgrade the lambda function that downloads the Twitch video to use Handbrake CLI.