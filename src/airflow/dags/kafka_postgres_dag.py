from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import requests


def configure_kafka_connector():
    url = "http://kafka-connect:8083/connectors"
    payload = {
        "name": "postgres-sink-connector",
        "config": {
            "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
            "tasks.max": "1",
            "topics": "yody-products",
            "connection.url": "jdbc:postgresql://postgres:5432/data_mining",
            "connection.user": "postgres",
            "connection.password": "warehouse",
            "table.name.format": "core_coreproduct",
            "insert.mode": "upsert",
            "pk.fields": "id",
            "pk.mode": "record_key",
            "auto.create": "false",
            "auto.evolve": "true",
            "key.converter": "org.apache.kafka.connect.storage.StringConverter",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "value.converter.schemas.enable": "false"
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        print("Kafka connector created successfully")
    elif response.status_code == 409:
        print("Kafka connector already exists")
    else:
        raise RuntimeError(f"Failed to create Kafka connector: {response.content}")

with DAG(
    "kafka_to_postgres_dbt",
    schedule_interval=None,
    start_date=datetime(2024, 11, 22),
    catchup=False,
) as dag:
    
    configure_connector = PythonOperator(
        task_id="configure_kafka_connector",
        python_callable=configure_kafka_connector,
    )

    refresh_dbt = BashOperator(
        task_id="refresh_dbt",
        bash_command="cd ./src/warehouse && dbt run --select stg_core_product",
    )

    configure_connector >> refresh_dbt
