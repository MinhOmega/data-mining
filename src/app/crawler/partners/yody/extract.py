from typing import Generator
from datetime import datetime

from app.crawler.partners.yody.api import YodyAPI
from app.crawler import etl
from helper.kafka_config import KafkaClient


class ExtractYodyProduct(etl.Extract):
    def __init__(self, status: str, topic: str):
        self.api = YodyAPI()
        self.status = status
        self.kafka_client = KafkaClient()
        self.topic = topic

    def execute(self) -> Generator:
        page = 1
        while True:
            response = self.api.call_products(page, self.status)
            if not response["items"]:
                break
            page += 1
            for product in response["items"]:
                print("step")
                self.kafka_client.get_producer().send(self.topic, value=product)
                yield product
            
        # Save all data to MinIO after extraction
        # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # file_path = f"yody/product/raw_data_{timestamp}.json"
        # self.minio_client.upload_json(all_data, file_path)


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
            
