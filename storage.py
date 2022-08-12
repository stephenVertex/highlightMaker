# The following code is a stub for adding DynamoDB support

import boto3

def mkS3Key(fpath):
    return("bucket/" + fpath)

def uploadHighlight(fpath):
    s3_key = mkS3Key(fpath)
    print(f"Uploading {fpath=}")
    return(s3_key)

