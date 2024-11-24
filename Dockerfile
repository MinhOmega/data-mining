FROM apache/airflow:2.7.0-python3.10

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt