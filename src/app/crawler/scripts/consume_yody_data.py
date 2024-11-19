from app.crawler.consum import KafkaToDatalakeConsumer


def consume_yody_data():
    consumer = KafkaToDatalakeConsumer(topic="yody-products", group_id="etl-group")
    consumer.consume_and_store()
