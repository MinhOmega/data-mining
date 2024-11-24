This is A data mining project

At first, create Warehouse by using DBT (data build tool)

Run these commands:

- cd src/
- dbt init <name> (warehouse)
'''
Enter a number: 1
host (hostname for the instance): localhost
port [5432]: 
user (dev username): admin
pass (dev password): 
dbname (default database that dbt will build objects in): data_mining
schema (default schema that dbt will build objects in): public
threads (1 or more) [1]: 4
'''



# Tạo các topic cho kafka broker
kafka-topics --bootstrap-server kafka-broker-1:9092 \
--create --topic connect-configs --partitions 1 --replication-factor 1 --config cleanup.policy=compact

kafka-topics --bootstrap-server kafka-broker-1:9092 \
--create --topic connect-offsets --partitions 50 --replication-factor 1 --config cleanup.policy=compact

kafka-topics --bootstrap-server kafka-broker-1:9092 \
--create --topic connect-status --partitions 10 --replication-factor 1 --config cleanup.policy=compact
# Chạy lại kafka-connect