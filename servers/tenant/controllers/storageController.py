from tkinter.messagebox import NO
from black import out
import boto3
import sys
import hashlib
from uuid import uuid4
from enum import Enum

sys.path.insert(0, "..")  # import parent folder

from models.__init__ import aws_secret_access_key, aws_access_key_id, tenant

class FileTypes:
    image = "image"
    text = "text"

class StorageController:
    
    bucket_name = f"{tenant}-bucket"
    
    def __init__(self):
        self.s3 = boto3.resource(
            's3', 
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key
        )

        self.bucket = self.s3.Bucket(self.bucket_name)


    def upload_file(self, local_file, storage_type=FileTypes.text) -> bool: 

        prefix = storage_type

        timeout =  5000
        while (timeout > 0):
            try:
                folder_uuid = uuid4()

                self.bucket.upload_file(local_file, prefix + "/" + folder_uuid)
                return True
            except Exception as e:
                pass
            timeout -= 50

        return False

        
    def download_file(self, s3_key):  # returns output_path on success, else None 
        folder_uuid = uuid4()

        output_path = "~/" + folder_uuid

        timeout =  1000
        while (timeout > 0):
            try:
                self.s3.download_file(s3_key, output_path)
                
                return output_path
            except Exception as e:
                pass
            timeout -= 50

        return None