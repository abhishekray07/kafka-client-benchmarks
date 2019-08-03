#!/bin/bash

echo "Stopping any running docker containers..."
docker-compose stop

echo "Starting Docker containers for Kafka and Zookeeper"
docker-compose up -d

echo "Waiting for Brokers to come up..."
sleep 30

BROKERS=localhost:9092
TOPIC=benchmark-test-topic
NUM_MESSAGES=100000
MSG_SIZE=100
NUM_RUNS=5

echo "Running Tests for Confluent Kafka"
python confluent-kafka-benchmark.py --client_type producer --brokers $BROKERS --topic $TOPIC --num_messages $NUM_MESSAGES --msg_size $MSG_SIZE --num_runs $NUM_RUNS
python confluent-kafka-benchmark.py --client_type consumer --brokers $BROKERS --topic $TOPIC --num_messages $NUM_MESSAGES --msg_size $MSG_SIZE --num_runs $NUM_RUNS --consumer_group_id confluent_kafka_grp
echo "==================="

echo "Running Tests for Kafka-Python"
python kafka-python-benchmark.py --client_type producer --brokers $BROKERS --topic $TOPIC --num_messages $NUM_MESSAGES --msg_size $MSG_SIZE --num_runs $NUM_RUNS
python kafka-python-benchmark.py --client_type consumer --brokers $BROKERS --topic $TOPIC --num_messages $NUM_MESSAGES --msg_size $MSG_SIZE --num_runs $NUM_RUNS
echo "==================="

echo "Running Tests for AIOKafka"
python aiokafka-benchmark.py --brokers $BROKERS --topic $TOPIC --num_messages $NUM_MESSAGES --msg_size $MSG_SIZE --num_runs $NUM_RUNS
echo "==================="


echo "Cleaning up..."
docker-compose stop