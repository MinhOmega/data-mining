from typing import Generator
from datetime import datetime

from app.crawler.partners.yody.api import YodyAPI
from app.crawler import etl
from helper.minio_config import MinIOClient

# Extract and save Yody products to MinIO
class ExtractYodyProduct(etl.Extract):
    def __init__(self, status: str):
        self.api = YodyAPI()
        self.status = status
        self.minio_client = MinIOClient()

    def execute(self) -> Generator:
        page = 1
        all_data = []
        while True:
            response = self.api.call_products(page, self.status)
            if not response["items"]:
                break
            page += 1
            for product in response["items"]:
                all_data.append(product)
                yield product
            
        # Save all data to MinIO after extraction
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f"yody/product/raw_data_{timestamp}.json"
        self.minio_client.upload_json(all_data, file_path)


class ExtractYodyCategory(etl.Extract):
    def __init__(self, status: str):
        self.api = YodyAPI()
        self.status = status

    def execute(self) -> Generator:
        page = 1
        while True:
            response = self.api.call_products(page, self.status)
            if not response["items"]:
                break
            page += 1
            for category in response["items"]:
                yield category
            
