import asyncio
import click
import os
import time
import utils
import uuid
import uvloop
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer


@click.command()
@click.option('--client_type', help='Test: producer or consumer', required=True)
@click.option('--brokers', help='List of brokers.', required=True)
@click.option('--topic', help='Topic to send message to.', required=True)
@click.option('--num_messages', type=click.INT, help='Number of messages to send to broker.', required=True)
@click.option('--msg_size', type=click.INT, help='Size of each message.', required=True)
@click.option('--num_runs', type=click.INT, help='Number of times to run the test.', required=True)
def benchmark(client_type, brokers, topic, num_messages, msg_size, num_runs):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    loop = asyncio.get_event_loop()
    if client_type == "producer":
        loop.run_until_complete(_producer_benchmark(brokers, topic, num_messages, msg_size, num_runs))
    else:
        loop.run_until_complete(_consumer_benchmark(brokers, topic, num_messages, msg_size, num_runs))
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


async def _consumer_benchmark(brokers, topic, num_messages, msg_size, num_runs):
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        topic, group_id=str(uuid.uuid1()),
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        loop=loop
    )

    await consumer.start()

    print("Starting benchmark for AIOKafka Consumer.")
    run_times = []

    try:
        for _ in range(num_runs):
            run_start_time = time.time()
            await _consume(consumer, num_messages)
            run_time_taken = time.time() - run_start_time
            run_times.append(run_time_taken)
    except asyncio.CancelledError:
        pass
    finally:
        await consumer.stop()

    utils.print_results(
        "AIOKafka Consumer", run_times, num_messages, msg_size
    )


async def _consume(consumer, num_messages):
    num_messages_consumed = 0
    async for msg in consumer:
        num_messages_consumed += 1
        if num_messages_consumed > num_messages:
            return

    # msg_set = await consumer.getmany(timeout_ms=1000)
    # if not msg_set:
    #     return

    # for msgs in msg_set.values():
    #     len_msgs = len(msgs)
    #     num_messages_consumed += len_msgs
    # if num_messages_consumed > num_messages:
    #     return


if __name__ == '__main__':
    benchmark()
