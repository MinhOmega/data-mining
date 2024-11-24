from datetime import datetime
from kafka import KafkaConsumer
from helper.minio_config import MinIOClient
import json

class YodyProductLoader:
    def __init__(self, kafka_topic, minio_bucket):
        self.kafka_topic = kafka_topic
        self.minio_client = MinIOClient()
        self.minio_bucket = minio_bucket

        # Ensure bucket exists
        if not self.minio_client.client.bucket_exists(self.minio_bucket):
            self.minio_client.client.make_bucket(self.minio_bucket)
            print(f"Bucket '{self.minio_bucket}' created successfully.")

    def load_to_minio(self):
        consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers="localhost:19092",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )
        all_data = []

        for message in consumer:
            all_data.append(message.value)
            if len(all_data) >= 1000:  # Save every 1000 messages
                self.save_to_minio(all_data)
                all_data = []

        # Save any remaining data
        if all_data:
            self.save_to_minio(all_data)

    def save_to_minio(self, data):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f"yody/product/raw_data_{timestamp}.json"
        self.minio_client.client.put_object(
            bucket_name=self.minio_bucket,
            object_name=file_path,
            data=json.dumps(data).encode("utf-8"),
            length=len(json.dumps(data)),
        )