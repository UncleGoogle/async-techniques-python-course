"""
Stopping single thread in Python is tricky.
`threading` API has no method to stop a thread except killing all deamon threads at the end.
Main reason is to not burden resources kept by a thread.
So you can either use a system API (ex. ctypes) or any kind of signal (callback, threading.Event, gevent...)
in your code to cleanup and finish thread job on your own.
Check out different solutions in this tread:
https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread

Here, I'm implement one of the simplest solutions: callback-based signal to stop generating any data.
"""

import datetime
import colorama
import random
import threading
import typing
import time


def main():
    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)
    data = []

    stop_generate = False

    threads = [
        threading.Thread(target=generate_data, args=(10, data, lambda: stop_generate), daemon=True),
        threading.Thread(target=generate_data, args=(20, data, lambda: stop_generate), daemon=True),
        threading.Thread(target=process_all_data, args=(data,), daemon=True)
    ]

    abort_thread = threading.Thread(target=check_cancel, daemon=True)
    abort_thread.start()

    [t.start() for t in threads]

    while any([t.is_alive() for t in threads]):
        [t.join(.001) for t in threads]
        if not abort_thread.is_alive():
            print("Cancelling data generation on your request!", flush=True)
            stop_generate = True
            break

    [t.join() for t in threads]  # continue data processing till finish

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)

def check_cancel():
    print(colorama.Fore.RED + "Press enter to cancel...", flush=True)
    input()

def generate_data(num: int, data: list, stop_callback: typing.Callable):
    for idx in range(1, num + 1):
        if stop_callback():
            break

        item = idx * idx
        data.append((item, datetime.datetime.now()))

        print(colorama.Fore.YELLOW + f" -- generated item {idx}", flush=True)
        time.sleep(random.random() + .5)

def process_all_data(data: list):
    processed = 0
    while data:
        item = None

        if data:
            item = data.pop(0)
        if not item:
            time.sleep(.01)
            continue

        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t

        print(colorama.Fore.CYAN +
              " +++ Processed value {} after {:,.2f} sec.".format(value, dt.total_seconds()), flush=True)
        time.sleep(1)


if __name__ == '__main__':
    main()
