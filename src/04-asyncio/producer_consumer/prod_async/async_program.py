import asyncio
import time
import random


def main():

    loop = asyncio.get_event_loop()

    t0 = time.time()
    print("| App started.", flush=True)

    q = asyncio.Queue()

    producers = [
        generate_data(3, q),
        generate_data(0.3, q),
        generate_data(10, q),
    ]
    consumers_number = 1
    consumers = [process_data(q) for i in range(consumers_number)]

    [loop.create_task(job) for job in producers + consumers]

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Exit on demand')
        dt = time.time() - t0
        print("| App exiting, total time: {:,.2f} sec.".format(dt))



async def generate_data(rate: float, q: asyncio.Queue):
    idx = 0
    while True:
        idx += 1
        item = idx*idx
        await q.put((item, time.time()))

        print("-->> Generated item {}".format(idx))
        await asyncio.sleep(random.random() + 1 / rate)


async def process_data(q: asyncio.Queue):
    while True:
        item = await q.get()

        value, t = item
        dt = time.time() - t

        print("<< Processed value {} after {:,.2f} sec.".format(value, dt))
        await asyncio.sleep(.5)


if __name__ == '__main__':
    main()
