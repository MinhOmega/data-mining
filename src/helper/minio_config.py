from minio import Minio
from minio.error import S3Error
import json
from datetime import datetime


class MinIOClient:
    def __init__(self):
        self.client = Minio(
            "localhost:9000", 
            access_key="minioadmin", 
            secret_key="minioadmin",
            secure=False, 
        )
        self.bucket_name = "datalake"

        # Create bucket if it doesn't exist
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
            print(f"Bucket '{self.bucket_name}' created successfully.")

    def upload_json(self, data: dict, file_path: str):
        """Upload JSON data to MinIO."""
        temp_file = f"/tmp/{file_path.replace('/', '_')}.json"

        # Save data to temporary file
        with open(temp_file, "w") as f:
            json.dump(data, f)

        # Upload to MinIO
        try:
            self.client.fput_object(
                bucket_name=self.bucket_name,
                object_name=file_path,  
                file_path=temp_file,  
            )
            print(f"Uploaded {file_path} to MinIO successfully.")
        except S3Error as e:
            print("Error occurred while uploading to MinIO:", e)
