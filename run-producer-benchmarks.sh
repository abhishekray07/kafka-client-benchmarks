#!/bin/bash

echo "Stopping any running docker containers..."
docker-compose stop

echo "Starting Docker containers for Kafka and Zookeeper"
docker-compose up -d

BROKERS=localhost:9092
TOPIC=benchmark-test-topic
NUM_MESSAGES=100000
MSG_SIZE=100
NUM_RUNS=5

echo "Running Tests for Confluent Kafka"
python confluent-kafka-benchmark.py --brokers $BROKERS --topic $TOPIC --num_messages $NUM_MESSAGES --msg_size $MSG_SIZE --num_runs $NUM_RUNS
echo "==================="

echo "Running Tests for Kafka-Python"
python kafka-python-benchmark.py --brokers $BROKERS --topic $TOPIC --num_messages $NUM_MESSAGES --msg_size $MSG_SIZE --num_runs $NUM_RUNS
echo "==================="

echo "Running Tests for AIOKafka"
python aiokafka-benchmark.py --brokers $BROKERS --topic $TOPIC --num_messages $NUM_MESSAGES --msg_size $MSG_SIZE --num_runs $NUM_RUNS
echo "==================="


echo "Cleaning up..."
docker-compose stop