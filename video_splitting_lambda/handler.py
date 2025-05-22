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
    output_dir = "/tmp/output/"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    s3.download_file(bucket_name, object_key, video_filename)
    print(f"Downloaded {object_key} from bucket {bucket_name}")
    output_file = video_splitting_cmdline(video_filename, output_dir, object_key)
    print(f"Completed executing video_splitting_cmdline function")
    
    output_bucket = "1229729607-stage-1"
    file_name = object_key.split(".")[0] + '.jpg'
    upload(output_file, output_bucket, file_name)
    print(f"Stored output in output bucket")
    
    invoke_face_recognition_lambda(output_bucket, file_name)
    return {"statusCode": 200, "body": "Frame extracted and uploaded successfully"}

def video_splitting_cmdline(video_filename, output_dir, object_key):
    output_file = os.path.join(output_dir, f"{object_key.split('.')[0]}.jpg")
    split_cmd = f"/usr/bin/ffmpeg -ss 0 -i {video_filename} -vframes 1 {output_file} -y"
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)
    return output_file

def upload(output_file, bucket_name, file_name):
    if output_file.endswith(".jpg"):
        s3_key = file_name
        s3.upload_file(output_file, bucket_name, s3_key)
        print(f"Uploaded {s3_key} to bucket {bucket_name}")
    return "Success"

def invoke_face_recognition_lambda(bucket_name, image_file_name):
    print("Calling the face recognition function")
    lambda_client = boto3_client("lambda")
    payload = {
        "bucket_name": bucket_name,
        "image_file_name": image_file_name
    }
    try:
        response = lambda_client.invoke(
            FunctionName="face-recognition",
            InvocationType="Event",
            Payload=json.dumps(payload)
        )
        print(f"Face recognition Lambda invoked with response: {response}")
    except Exception as e:
        print(f"Error invoking face-recognition Lambda: {e}")