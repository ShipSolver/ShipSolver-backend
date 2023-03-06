import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv


class S3Controller:
    TENANT = "test-tenant2"
    BUCKET = f"{TENANT}-bucket"
    
    aws_access_key_id = os.environ["aws_access_key_id"]
    aws_secret_access_key = os.environ["aws_secret_access_key"]
    
    def __init__(self):
        self.s3 = boto3.resource('s3', region_name='us-east-2', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, config=Config(signature_version='s3v4'))
        self.s3_client = boto3.client('s3', region_name='us-east-2', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, config=Config(signature_version='s3v4'))
        self.bucket = self.s3.Bucket(self.BUCKET)

    def _upload_file(self, local_file_path, remote_file_path):

        return self.bucket.upload_file(local_file_path, remote_file_path)
    

    def _generate_presigned_url(self, remote_file_path, timeout=3600):  
        if remote_file_path is None:
            return None
        try:
            view_url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={'Bucket': self.BUCKET, 'Key': remote_file_path},
                ExpiresIn=timeout
            )
        except Exception as e:
            return None

        return view_url