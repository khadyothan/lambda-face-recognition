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
    
    output_bucket = "1229729607-stage-1"
    folder_name = object_key.split(".")[0]
    upload(output_dir, output_bucket, folder_name)
    
    return {"statusCode": 200, "body": output}

def video_splitting_cmdline(video_filename, output_dir):
    filename = os.path.basename(video_filename)
    split_cmd = '/usr/bin/ffmpeg -ss 0 -r 1 -i ' +video_filename+ ' -vf fps=1/10 -start_number 0 -vframes 10 ' + output_dir + "/" + 'output_%02d.jpg -y'
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)
    print("Success")
    return "Success"

def upload(output_dir, bucket_name, folder_name):
    print("Inside upload")
    for filename in os.listdir(output_dir):
        print("filename: ", filename)
        if filename.endswith(".jpg"):
            local_path = os.path.join(output_dir, filename)
            print("local path: " + local_path)
            s3_key = f"{folder_name}/{filename}"
            print("S3 key: " + s3_key)
            print(f"Uploading {s3_key} to bucket {bucket_name}")
            s3.upload_file(local_path, bucket_name, s3_key)
            print(f"Uploaded {s3_key} to bucket {bucket_name}")
            
    print("Upload complete")
    return "Success"