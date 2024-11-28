# Data Mining Project

## Prerequisites
- Docker and Docker Compose installed
- At least 8GB RAM available

## Initial Setup

1. Create Environment File
First, create a `.env` file in the root directory:

```sh
# Database for Airflow
AIRFLOW_DB=airflow
AIRFLOW_DB_USER=airflow
AIRFLOW_DB_PASSWORD=airflow
AIRFLOW_DB_HOST=postgres
AIRFLOW_DB_PORT=5432

# Database for Application
POSTGRES_DB=data_mining
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Django
SECRET_KEY=your-secret-key
ENVIRONMENT=development
DEBUG=True

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=minioserver:9000

# Airflow
AIRFLOW_UID=50000
AIRFLOW_GID=50000
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__LOAD_EXAMPLES=false
AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth
AIRFLOW__WEBSERVER__AUTH_BACKEND=airflow.api.auth.backend.basic_auth
AIRFLOW__CORE__FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
```

2. Create Required Directories
```sh
mkdir -p src/airflow/{dags,logs,plugins,config}
mkdir -p src/warehouse
```

3. Start Services
```sh
# Build and start all services
docker-compose up -d

# Wait for all services to be healthy (2-3 minutes)
docker-compose ps
```

4. Create Kafka Topics
After Kafka is up, create the required topics:

```sh
# Connect to kafka-broker-1 container
docker exec -it data-mining-kafka-broker-1-1 bash

# Create topics
kafka-topics --bootstrap-server localhost:9092 \
--create --topic connect-configs --partitions 1 --replication-factor 1 --config cleanup.policy=compact

kafka-topics --bootstrap-server localhost:9092 \
--create --topic connect-offsets --partitions 50 --replication-factor 1 --config cleanup.policy=compact

kafka-topics --bootstrap-server localhost:9092 \
--create --topic connect-status --partitions 10 --replication-factor 1 --config cleanup.policy=compact

kafka-topics --bootstrap-server localhost:9092 \
--create --topic yody-products --partitions 1 --replication-factor 1
```

5. Initialize DBT
```sh
# Connect to airflow container
docker exec -it airflow-webserver bash

# Navigate to warehouse directory
cd src/warehouse

# Initialize DBT project (if not already done)
dbt init warehouse

# When prompted, enter these values:
# Enter a number: 1 (for postgres)
# host: postgres
# port: 5432
# user: admin
# pass: admin123
# dbname: data_mining
# schema: public
# threads: 4

# Install DBT dependencies
dbt deps

# Run DBT
dbt run
```

6. Access Services
After everything is up, you can access:
- Airflow UI: http://localhost:8088 (username: admin, password: admin)
- MinIO Console: http://localhost:9001 (username: minioadmin, password: minioadmin)
- Kafka Control Center: http://localhost:9021
- Dremio: http://localhost:9047
- PostgreSQL: localhost:5433
- Django API: http://localhost:8000

7. Test the Pipeline
```sh
# Create a bucket in MinIO
- Login to MinIO console at http://localhost:9001
- Create a bucket named "datalake"

# Step 1: Extract data from Yody website to MinIO
curl -X POST http://localhost:8000/api/v1/crawler/yody/extract \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'

# Step 2: Load data from MinIO to PostgreSQL
curl -X POST http://localhost:8000/api/v1/crawler/yody/load \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'

# Step 3: Trigger Airflow DAG to process data from MinIO to Kafka
curl -X POST http://localhost:8000/api/v1/crawler/yody/dag/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "bucket_name": "datalake",
    "object_name": "yody-products.json"
  }'

# Verify data flow:
1. Check MinIO (http://localhost:9001)
   - Look for yody-products.json in "datalake" bucket
2. Check PostgreSQL (localhost:5433)
   - Database: data_mining
   - Table: core_coreproduct
3. Check Kafka (http://localhost:9021)
   - Topic: yody-products
4. Monitor DAG (http://localhost:8088)
   - DAG: minio_to_kafka_dynamic
```

8. Monitoring
- Monitor Airflow DAGs: http://localhost:8088
- Monitor Kafka: http://localhost:9021
- Monitor MinIO: http://localhost:9001
- Monitor Django API: http://localhost:8000

9. Troubleshooting
```sh
# View logs for a specific service
docker-compose logs -f [service-name]

# Available service names:
- django
- airflow-webserver
- airflow-scheduler
- airflow-init
- postgres
- minioserver
- dremio
- zookeeper
- kafka-broker-1
- schema-registry
- control-center
- kafka-connect
- nessie

# Restart a service
docker-compose restart [service-name]

# Reset everything
docker-compose down -v
docker-compose up -d
```

## Project Components
- Django: Web API and Crawler
- Airflow: Workflow orchestration
- Kafka: Message streaming
- MinIO: Object storage
- PostgreSQL: Data storage
- DBT: Data transformation
- Dremio: Data visualization

## System Requirements
- Docker Engine
- Docker Compose
- Minimum 8GB RAM
- 20GB free disk space
