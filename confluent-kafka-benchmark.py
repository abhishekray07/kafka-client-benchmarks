import click
import os
import time
import utils
from confluent_kafka import Producer


@click.command()
@click.option('--brokers', help='List of brokers.', required=True)
@click.option('--topic', help='Topic to send message to.', required=True)
@click.option('--num_messages', type=click.INT, help='Number of messages to send to broker.', required=True)
@click.option('--msg_size', type=click.INT, help='Size of each message.', required=True)
@click.option('--num_runs', type=click.INT, help='Number of times to run the test.', required=True)
def producer_benchmark(brokers, topic, num_messages, msg_size, num_runs):
    payload = b"m" * msg_size
    
    conf = {"bootstrap.servers": brokers}
    producer = Producer(**conf)
    
    print("Starting benchmark for Confluent Kafka Producer.")
    
    run_times = []
    
    for _ in range(num_runs):
        run_start_time = time.time()
        _produce(producer, topic, payload, num_messages)
        run_time_taken = time.time() - run_start_time
        run_times.append(run_time_taken)

    utils.print_results(
        "Confluent Kafka Python", run_times, num_messages, msg_size)
    

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


if __name__ == '__main__':
    producer_benchmark()