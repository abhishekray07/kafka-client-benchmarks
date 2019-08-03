import click
import os
import time
import utils
from confluent_kafka import Consumer, Producer


@click.command()
@click.option('--client_type', help='Test: producer or consumer', required=True)
@click.option('--brokers', help='List of brokers.', required=True)
@click.option('--topic', help='Topic to send message to.', required=True)
@click.option('--num_messages', type=click.INT, help='Number of messages to send to broker.', required=True)
@click.option('--msg_size', type=click.INT, help='Size of each message.', required=True)
@click.option('--num_runs', type=click.INT, help='Number of times to run the test.', required=True)
@click.option('--consumer_group_id', help='Consumer Group Id')
def benchmark(client_type, brokers, topic, num_messages, msg_size, num_runs, consumer_group_id):
    payload = b'm' * msg_size
    conf = {'bootstrap.servers': brokers}
    
    if client_type == 'producer':
        client = Producer(**conf)
        benchmark_fn = _produce
    elif client_type == 'consumer':
        conf['auto.offset.reset'] = 'earliest'
        conf['group.id'] = consumer_group_id
        client = Consumer(**conf)
        client.subscribe([topic])
        benchmark_fn = _consume

    print(f'Starting benchmark for Confluent Kafka {client_type}.')
    
    run_times = []
    
    try:
        for _ in range(num_runs):
            run_start_time = time.time()
            benchmark_fn(client, topic, payload, num_messages)
            run_time_taken = time.time() - run_start_time
            run_times.append(run_time_taken)
    except Exception:
        pass
    finally:
        if client_type == "consumer":
            client.close()

    utils.print_results(
        f'Confluent Kafka Python {client_type}', run_times, num_messages, msg_size)
    

def _produce(producer, topic, payload, num_messages):
    for _ in range(num_messages):
        try:
            producer.produce(topic, payload)
        except BufferError:
            pass

        # Serve delivery callback queue.
        # NOTE: Since produce() is an asynchronous API this poll() call
        #       will most likely not serve the delivery callback for the
        #       last produce()d message.
        producer.poll(0)

    # Wait until all messages have been delivered
    # sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    producer.flush()


def _consume(consumer, topic, payload, num_messages):

    num_messages_consumed = 0
    while True:
        msg = consumer.poll(timeout=1.0)
        num_messages_consumed += 1
        
        if num_messages_consumed >= num_messages:
            break


if __name__ == '__main__':
    benchmark()
