# Serverless Face Recognition

A serverless face recognition system using AWS Lambda, S3, and PyTorch.
This project detects and recognizes faces in images uploaded to an S3 bucket, leveraging deep learning models in a scalable, cloud-native architecture.

## Features

- Face detection and recognition using [facenet-pytorch](https://github.com/timesler/facenet-pytorch)
- AWS Lambda function for serverless execution
- S3 integration for input/output storage
- Dockerized for easy deployment

## How It Works

1. Upload an image to the specified S3 bucket.
2. The Lambda function is triggered, downloads the image, and runs face recognition.
3. The recognized name is saved as a `.txt` file in the output S3 bucket.

## Project Structure

```
lambda/
  handler.py         # Lambda function code
  requirements.txt   # Python dependencies
  Dockerfile         # Lambda deployment container
  entry.sh           # Entrypoint script
  data.pt            # Face embeddings database
grader_script_p1.py  # grading/utility scripts
workload_generator.py
...
```

## Quick Start

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/serverless-face-recognition.git
   cd serverless-face-recognition/Lambda2
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Run locally (for testing)**

   ```sh
   python handler.py
   ```

4. **Deploy to AWS Lambda**
   - Build the Docker image and push to AWS ECR.
   - Create a Lambda function using the image.
   - Set up S3 triggers.

---

> **Note:** This project was developed as part of coursework at Arizona State University.
