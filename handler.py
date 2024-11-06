from boto3 import client as boto3_client
import os
import subprocess
import json

s3 = boto3_client("s3")

def handler(event, context):
    print("Event: ", event)
    
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    
    video_filename = "/tmp/" + object_key
    output_dir = "/tmp/output/" + object_key.split(".")[0]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    s3.download_file(bucket_name, object_key, video_filename)
    print(f"Downloaded {object_key} from bucket {bucket_name}")

    output = video_splitting_cmdline(video_filename, output_dir)
    print(f"Completed executing video_splitting_cmdline function")
    
    output_bucket = "1229729607-stage-1"
    folder_name = object_key.split(".")[0]
    
    upload(output_dir, output_bucket, folder_name)
    print(f"Stored output in output bucket")
    
    return {"statusCode": 200, "body": output}

def video_splitting_cmdline(video_filename, output_dir):
    split_cmd = '/usr/bin/ffmpeg -ss 0 -r 1 -i ' +video_filename+ ' -vf fps=1/10 -start_number 0 -vframes 10 ' + output_dir + "/" + 'output_%02d.jpg -y'
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)
    return "Success"

def upload(output_dir, bucket_name, folder_name):
    for filename in os.listdir(output_dir):
        if filename.endswith(".jpg"):
            local_path = os.path.join(output_dir, filename)
            s3_key = f"{folder_name}/{filename}"
            s3.upload_file(local_path, bucket_name, s3_key)
            print(f"Uploaded {s3_key} to bucket {bucket_name}")
    return "Success"