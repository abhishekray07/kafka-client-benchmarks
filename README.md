
# Performance Comparison for Different Kafka Python Clients

## Caveats

Tests run on a Macbook Pro (2017):
- 3.1 GHz Intel Core i5


Test setup:

- Single Kafka broker


## Producer Results

1. Confluent Kafka Python Library

```bash
Confluent Kafka Python producer Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time for 100000 messages: 4.487483406066895 seconds.
Messages / sec: 22284.204965483343
MB / sec : 2.1251873937114087
```

2. Kafka Python

```bash
Kafka-Python producer Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time for 100000 messages: 8.761995649337768 seconds.
Messages / sec: 11412.92509173501
MB / sec : 1.0884213535056122
```

3. AIOKafka

```bash
AIOKafka Producer Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time for 100000 messages: 2.2214564800262453 seconds.
Messages / sec: 45015.51162452598
MB / sec : 4.2930137276197415
```

## Consumer Results

1. Confluent Kafka

```bash
Confluent Kafka Python consumer Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time for 100000 messages: 1.6225053787231445 seconds.
Messages / sec: 61633.07765345994
MB / sec : 5.8777883199176735
```

2. Kafka-Python

```bash
Kafka-Python consumer Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time for 100000 messages: 9.437553405761719 seconds.
Messages / sec: 10595.966528671406
MB / sec : 1.010510113589421
```

3. AIOKafka

```bash
AIOKafka Consumer Results:
Number of Runs: 5, Number of messages: 100000, Message Size: 100 bytes.
Average Time for 100000 messages: 1.6015226364135742 seconds.
Messages / sec: 62440.57856337173
MB / sec : 5.954797607743428
```
