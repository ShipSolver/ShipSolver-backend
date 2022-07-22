from black import out
import boto3
import sys
import hashlib
from uuid import uuid4
from enum import Enum
from botocore.client import Config

sys.path.insert(0, "..")  # import parent folder

from models.__init__ import aws_secret_access_key, aws_access_key_id, tenant


class FileTypes:
    image = "images"
    text = "text"


class StorageController:

    bucket_name = f"{tenant}-bucket"

    def __init__(self):
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        self.bucket = self.s3.Bucket(self.bucket_name)

        self.s3_client = boto3.client(
            "s3",
            region_name="ca-central-1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )

    def upload_file(self, local_file, storage_type=FileTypes.image) -> bool:

        prefix = storage_type

        timeout = 5000
        while timeout > 0:
            try:

                image_uuid = str(uuid4())
                object_id = f"{prefix}/{image_uuid}"
                s3_path = f"s3://{self.bucket_name}:{object_id}"

                self.bucket.upload_file(local_file, object_id)
                return s3_path
            except Exception as e:
                pass
            timeout -= 50

        return False

    def generate_presigned_url(
        self, s3_key
    ):  # returns output_path on success, else None

        bucket = s3_key.split("/")[2].split(":")[0]
        image_name = s3_key.split("/")[2].split(":")[1] + "/" + s3_key.split("/")[3]
        print(s3_key.split("/"))
        print("print(bucket, image_name)")
        print(bucket, image_name)

        timeout = 1000
        while timeout > 0:

            # try:

            view_url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": image_name},
                ExpiresIn=3600,
            )

            return view_url
            # except Exception as e:
            #     pass
            timeout -= 50

        return None
