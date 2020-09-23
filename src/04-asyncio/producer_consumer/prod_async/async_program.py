import asyncio
import time
import random


def main():

    loop = asyncio.get_event_loop()

    t0 = time.time()
    print("| App started.", flush=True)

    data = asyncio.Queue()

    task1 = loop.create_task(generate_data(10, data))
    task2 = loop.create_task(generate_data(8, data))
    task3 = loop.create_task(process_data(40, data))

    final_task = asyncio.gather(task1, task2, task3)
    loop.run_until_complete(final_task)

    dt = time.time() - t0
    print("| App exiting, total time: {:,.2f} sec.".format(dt), flush=True)


async def generate_data(num: int, data: asyncio.Queue):
    for idx in range(1, num + 1):
        item = idx*idx
        await data.put((item, time.time()))

        print("-->> Generated item {}".format(idx), flush=True)
        await asyncio.sleep(random.random() + .5)


async def process_data(num: int, data: asyncio.Queue):
    processed = 0
    while processed < num:
        item = await data.get()

        processed += 1
        value, t = item
        dt = time.time() - t

        print("<< Processed value {} after {:,.2f} sec.".format(value, dt), flush=True)
        await asyncio.sleep(.5)


if __name__ == '__main__':
    main()
