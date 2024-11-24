from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import json

from kafka import KafkaProducer
from minio import Minio


def minio_config():
    client = Minio(
            "minioserver:9000", 
            access_key="AccZyeMH0S93Dmy6N28Q", 
            secret_key="wevH7ArzyTDVTxb9oOQjlByTRhZuNJZ5pcHX0Z35",
            secure=False, 
        )
    return client

def kafka_config():
    producer = KafkaProducer(
            bootstrap_servers=['kafka-broker-1:9092'],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
    return producer


def create_minio_to_kafka_dag(dag_id, bucket_name, object_name, kafka_topic):
    def extract_from_minio(**context):
        try:
            minio_client = minio_config()
            response = minio_client.get_object(bucket_name, object_name)
            data = json.loads(response.read().decode("utf-8"))
            print("Testttt", data)
            context['ti'].xcom_push(key='minio_data', value=data)
        except Exception as e:
            raise RuntimeError(f"Error in extract_from_minio: {e}")

    def publish_to_kafka(**context):
        try:
            data = context['ti'].xcom_pull(key='minio_data', task_ids='extract_from_minio')
            if not data:
                raise ValueError("No data pulled from XCom for key 'minio_data'")
            
            producer = kafka_config()
            for record in data:
                print("Record", record)
                producer.send(kafka_topic, value=record)
            producer.flush()
        except Exception as e:
            raise RuntimeError(f"Error in publish_to_kafka: {e}")

    with DAG(
        dag_id=dag_id,
        schedule_interval=None,  # Trigger manually
        start_date=datetime(2024, 11, 21),
        catchup=False,
    ) as dag:
        extract_task = PythonOperator(
            task_id="extract_from_minio",
            python_callable=extract_from_minio,
        )

        publish_task = PythonOperator(
            task_id="publish_to_kafka",
            python_callable=publish_to_kafka,
        )

        extract_task >> publish_task

    return dag


DAG_ID = "minio_to_kafka_dynamic"
BUCKET_NAME = "datalake"
OBJECT_NAME = "yody/product/raw_data_20241123015705.json"
KAFKA_TOPIC = "yody-products"
globals()[DAG_ID] = create_minio_to_kafka_dag(DAG_ID, BUCKET_NAME, OBJECT_NAME, KAFKA_TOPIC)
