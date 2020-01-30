import multiprocessing as mp
import numpy as np
from time import time
#
# # print("Number of processors: ", mp.cpu_count())
#
# # Given a 2D matrix (or list of lists), count how many numbers are present between a given range in each row.
#
# Prepare data
np.random.RandomState(100)
arr = np.random.randint(0, 10, size=[200000, 5])
data = arr.tolist()
data[:5]
#
#
# # Solution Without Parallelization
# def howmany_within_range(row, minimum=4, maximum=8):
#     """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
#     count = 0
#     for n in row:
#         if minimum <= n <= maximum:
#             count = count + 1
#     return count
#
# start_n = time()
# results = []
# for row in data:
#     results.append(howmany_within_range(row, minimum=4, maximum=8))
# end_n = time()
# total_time_n = format(end_n - start_n, '.2f')
# print("Total time Without Parallelization :", total_time_n, "s")
# print(results[:10])
# start = time()
# pool = mp.Pool(mp.cpu_count())
# results = pool.map(howmany_within_range, [row for row in data])
# pool.close()
# end = time()
# total_time = format(end - start, '.2f')
# print("Total time by Parallelization :", total_time, "s")
#
# start = time()
# pool = mp.Pool(mp.cpu_count())
#
# results = pool.starmap(howmany_within_range, [(row, 4, 8) for row in data])
#
# pool.close()
# end = time()
# total_time = format(end - start, '.2f')
# print("Total time by Parallelization :", total_time, "s")
# print(results[:10])

# Parallel processing with Pool.apply_async()
pool = mp.Pool(mp.cpu_count())

results = []

# Step 1: Redefine, to accept `i`, the iteration number
def howmany_within_range2(i, row, minimum, maximum):
    """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return (i, count)


# Step 2: Define callback function to collect the output in `results`
def collect_result(result):
    global results
    results.append(result)

if __name__ == '__main__':
    start = time()
    # Step 3: Use loop to parallelize
    for i, row in enumerate(data):
        pool.apply_async(howmany_within_range2, args=(i, row, 4, 8), callback=collect_result)

    # Step 4: Close Pool and let all the processes completegit
    pool.close()
    pool.join()  # postpones the execution of next line of code until all processes in the queue are done.

    # Step 5: Sort results [OPTIONAL]
    results.sort(key=lambda x: x[0])
    results_final = [r for i, r in results]
    end = time()
    total_time = format(end - start, '.2f')
    print("Total time by async Paralleization :", total_time, "s")
    print(results_final[:10])