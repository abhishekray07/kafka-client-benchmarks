import asyncio
import click
import os
import time
import utils
import uvloop
from aiokafka import AIOKafkaProducer


@click.command()
@click.option('--brokers', help='List of brokers.', required=True)
@click.option('--topic', help='Topic to send message to.', required=True)
@click.option('--num_messages', type=click.INT, help='Number of messages to send to broker.', required=True)
@click.option('--msg_size', type=click.INT, help='Size of each message.', required=True)
@click.option('--num_runs', type=click.INT, help='Number of times to run the test.', required=True)
def producer_benchmark(brokers, topic, num_messages, msg_size, num_runs):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_producer_benchmark(brokers, topic, num_messages, msg_size, num_runs))
    loop.close()

async def _producer_benchmark(brokers, topic, num_messages, msg_size, num_runs):
    payload = bytearray(b"m" * msg_size)
    producer_config = dict(
        bootstrap_servers=brokers,
    )
    
    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(loop=loop, **producer_config)
    await producer.start()
    
    print("Starting benchmark for AIOKafka Producer.")
    run_times = []
    
    try:
        for _ in range(num_runs):
            run_start_time = time.time()
            await _produce(producer, topic, payload, num_messages)
            run_time_taken = time.time() - run_start_time
            run_times.append(run_time_taken)
    except asyncio.CancelledError:
        pass
    finally:
        await producer.stop()

    utils.print_results(
        "AIOKafka Producer", run_times, num_messages, msg_size
    )
    

async def _produce(producer, topic, payload, num_messages):
    for _ in range(num_messages):
        await producer.send(topic, payload)
    


if __name__ == '__main__':
    producer_benchmark()
