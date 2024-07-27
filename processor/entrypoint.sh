#!/bin/bash
set -e

# Wait for Spark Master to be ready
echo "Waiting for Spark Master to be ready..."
while ! nc -z spark-master 7077; do
    sleep 1
done
echo "Spark Master is ready"

# Submit PySpark application
echo "Submitting PySpark application..."
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-avro_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.5.1 --master spark://spark-master:7077 /work/main.py

