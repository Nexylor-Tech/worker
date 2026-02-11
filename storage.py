import boto3
import io
from botocore.config import Config as BotoConfig
from config import Config


def get_S3_client():
    return boto3.client(
        "s3",
        endpoint_url=Config.AWS_ENDPOINT_URL,
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        config=BotoConfig(s3={"addressing_style": "path"}),
    )


def download_file_content(storage_key: str):
    s3 = get_S3_client()
    try:
        res = s3.get_object(Bucket="cognexa_media_assets", Key=storage_key)
        file_content = res["Body"].read()
        return file_content.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Failed to download file {storage_key}: {e}")
