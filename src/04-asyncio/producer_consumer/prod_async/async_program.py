import asyncio
import time
import random


def main():

    loop = asyncio.get_event_loop()

    t0 = time.time()
    print("| App started.", flush=True)

    q = asyncio.Queue()

    consumers_no = 2
    producers_no = 3
    consumers = [process_data(q, throughput=1.4) for i in range(consumers_no)]
    producers = [generate_data(q, rate=1.0) for i in range(producers_no)]

    [loop.create_task(job) for job in producers + consumers]

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Exit on demand')
        dt = time.time() - t0
        print("| App exiting, total time: {:,.2f} sec.".format(dt))


async def generate_data(q: asyncio.Queue, rate: float = 1.0):
    """
    :param: items per second
    """
    idx = 0
    while True:
        idx += 1
        item = idx*idx
        await q.put((item, time.time()))

        print("-->> Generated item {}".format(idx))
        await asyncio.sleep(1 / rate)


async def process_data(q: asyncio.Queue, throughput: float = 1.0):
    while True:
        item = await q.get()

        value, t = item
        dt = time.time() - t

        print("<< Processed value {} after {:,.2f} sec.".format(value, dt))
        await asyncio.sleep(1 / throughput)


if __name__ == '__main__':
    main()
