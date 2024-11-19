from app.crawler.partners.yody.extract import ExtractYodyProduct
from celery import shared_task
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


class YodyProductCrawler:
    # @shared_task
    def run_extract(self, status: str):
        extractor = ExtractYodyProduct(status=status, topic="yody-products")
        for _ in extractor.execute():
            pass  # Extractor already saves data to MinIO
    
    with DAG(
        dag_id="yody_kafka_producer",
        schedule_interval="0 0 * * *",  # Run daily
        start_date=datetime(2023, 1, 1),
        catchup=False,
    ) as dag:
        producer_task = PythonOperator(
            task_id="produce_yody_data",
            python_callable=run_extract,
        )