from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import boto3
import os


class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
    file_overwrite = False


class MediaDelete:
    def s3_delete(self, url):
        new_string = url.replace("%20", " ")
        file_url = url
        file_name = "/".join(file_url.split("/")[3:])
        bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        s3_client = boto3.client("s3")
        response = s3_client.delete_object(Bucket=bucket_name, Key=file_name)
