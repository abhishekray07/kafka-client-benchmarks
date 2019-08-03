
# Performance Comparison for Different Kafka Python Clients

Tests run on a Macbook Pro:

## Producer Test Results

1. Confluent Kafka Python Library

```bash
Confluent Kafka Python Test Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time to send 100000: 2.6532379627227782 seconds.
Messages / sec: 37689.79692171261
MB / sec : 3.5943791314804656
```

2. Kafka Python

```bash
Kafka-Python Producer Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time to send 100000: 8.682069730758666 seconds.
Messages / sec: 11517.990882487611
MB / sec : 1.0984412081229793
```

3. AIOKafka

```bash
AIOKafka Producer Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time to send 100000: 2.2853951930999754 seconds.
Messages / sec: 43756.108484833705
MB / sec : 4.17290768478715
```