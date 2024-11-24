#!/usr/bin/env bash

set -eo pipefail

# Kafka directories
KAFKA_HOME=${KAFKA_HOME:-/opt/kafka}
KAFKA_CONNECT_PLUGINS_DIR=${KAFKA_CONNECT_PLUGINS_DIR:-/opt/kafka/plugins}
JDBC_PLUGIN_DIR="$KAFKA_CONNECT_PLUGINS_DIR/jdbc"

# Ensure plugin directory exists
mkdir -p "$JDBC_PLUGIN_DIR"

# Copy built-in Kafka File Source and Sink connector JARs (optional)
echo "Copying Kafka built-in connectors..."
cp "$KAFKA_HOME"/libs/connect-file-*.jar "$KAFKA_CONNECT_PLUGINS_DIR"
cp "$KAFKA_HOME"/libs/kafka-clients-*.jar "$KAFKA_CONNECT_PLUGINS_DIR"
cp "$KAFKA_HOME"/libs/connect-api-*.jar "$KAFKA_CONNECT_PLUGINS_DIR"
cp "$KAFKA_HOME"/libs/connect-transforms-*.jar "$KAFKA_CONNECT_PLUGINS_DIR"

echo "Kafka built-in connectors set up in $KAFKA_CONNECT_PLUGINS_DIR."

# Download the JDBC Sink Connector
echo "Downloading Kafka JDBC Sink Connector..."
curl -o "$JDBC_PLUGIN_DIR/kafka-connect-jdbc.jar" https://packages.confluent.io/maven/io/confluent/kafka-connect-jdbc/10.8.0/kafka-connect-jdbc-10.8.0.jar

# Download database-specific JDBC driver (PostgreSQL example)
echo "Downloading PostgreSQL JDBC Driver..."
curl -o "$JDBC_PLUGIN_DIR/postgresql-connector.jar" https://jdbc.postgresql.org/download/postgresql-42.6.0.jar

# Verify installation
echo "Installed connectors in $JDBC_PLUGIN_DIR:"
ls -1 "$JDBC_PLUGIN_DIR"

# Optional: Add any additional setup commands here
echo "Kafka Connect plugins installation complete."
