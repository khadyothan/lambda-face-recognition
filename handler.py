from boto3 import client as boto3_client
import os
import subprocess
import json

def handler(event, context):
    print("Event: ", event)
    video_filename = "/home/app/test_0.mp4"
    output_dir = "/home/app/output"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.exists(video_filename):
        print(f"Video file {video_filename} not found!")
        return {"statusCode": 404, "body": "Video file not found"}

    output = video_splitting_cmdline(video_filename, output_dir)
    return {"statusCode": 200, "body": output}

def video_splitting_cmdline(video_filename, output_dir):
    filename = os.path.basename(video_filename)
    split_cmd = '/usr/bin/ffmpeg -ss 0 -r 1 -i ' +video_filename+ ' -vf fps=1/10 -start_number 0 -vframes 10 ' + output_dir + "/" + 'output_%02d.jpg -y'
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)
    return "Success"