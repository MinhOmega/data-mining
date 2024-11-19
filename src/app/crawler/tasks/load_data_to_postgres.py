import json
from celery import shared_task

from helper.minio_config import MinIOClient


class LoadProductData:
    def __init__(self, bucket_name: str, object_name: str):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.minio_client = MinIOClient()

    @shared_task
    def execute(self):
        response = self.minio_client.client.get_object(self.bucket_name, self.object_name)

        return json.loads(response.read().decode("utf-8"))
