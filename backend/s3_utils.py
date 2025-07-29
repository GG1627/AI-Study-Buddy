import boto3
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# set AWS S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def download_from_s3(file_key: str, local_path: str):
    bucket_name = os.getenv("S3_BUCKET_NAME")

    try: 
        s3_client.download_file(bucket_name, file_key, local_path)
        return local_path
    except Exception as e:
        raise Exception(f"❌ Error downloading file from S3: {e}")