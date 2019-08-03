import click
import os
import time
import utils
import uuid
from kafka import KafkaProducer, KafkaConsumer


@click.command()
@click.option('--client_type', help='Test: producer or consumer', required=True)
@click.option('--brokers', help='List of brokers.', required=True)
@click.option('--topic', help='Topic to send message to.', required=True)
@click.option('--num_messages', type=click.INT, help='Number of messages to send to broker.', required=True)
@click.option('--msg_size', type=click.INT, help='Size of each message.', required=True)
@click.option('--num_runs', type=click.INT, help='Number of times to run the test.', required=True)
def benchmark(client_type, brokers, topic, num_messages, msg_size, num_runs):
    payload = b"m" * msg_size
    
    if client_type == 'producer':
        client = KafkaProducer(bootstrap_servers=brokers)
        benchmark_fn = _produce
    elif client_type == 'consumer':
        client = KafkaConsumer(topic, bootstrap_servers=brokers, group_id=str(uuid.uuid1()), auto_offset_reset="earliest")
        client.subscribe([topic])
        benchmark_fn = _consume
    
    print(f"Starting benchmark for Kafka-Python {client_type}.")
    
    run_times = []
    for _ in range(num_runs):
        run_start_time = time.time()
        benchmark_fn(client, topic, payload, num_messages)
        run_time_taken = time.time() - run_start_time
        run_times.append(run_time_taken)

    utils.print_results(
        f"Kafka-Python {client_type}", run_times, num_messages, msg_size)


def _produce(producer, topic, payload, num_messages):
    for _ in range(num_messages):
        try:
            producer.send(topic, payload)
        except Exception:
            pass
    
    # Wait until all messages have been delivered
    # sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    producer.flush()

def _consume(consumer, topic, payload, num_messages):
    num_messages_consumed = 0
    for msg in consumer:
        num_messages_consumed += 1        
        if num_messages_consumed >= num_messages:
            break


if __name__ == '__main__':
    benchmark()
