import json
from kafka import KafkaProducer

class KafkaClient:
    def __init__(self):
        self.kafka_server = "localhost:9092"
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_server,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def get_producer(self):
        return self.producer