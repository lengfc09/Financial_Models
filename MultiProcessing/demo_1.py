import concurrent.futures
import time

start = time.perf_counter()


def do_something(seconds):
    print(f"Sleeping {seconds} second(s)...\n")
    time.sleep(seconds)
    return f"Done Sleeping...{seconds}"


with concurrent.futures.ProcessPoolExecutor() as executor:
    secs = [5, 1, 2, 3, 4, 5, 5]
    results = executor.map(do_something, secs)

    for result in results:
        print(result)

finish = time.perf_counter()

print(f"Finished in {round(finish-start, 2)} second(s)")

