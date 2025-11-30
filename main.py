import random
import copy
from timeit import timeit


def generate_random_list(size):
    return [random.randint(0, 100000) for _ in range(size)]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def python_sort(arr):
    return sorted(arr)


def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)


def run_benchmarks():
    sizes = [1000, 5000, 10000, 20000]

    results = {}
    for size in sizes:
        print(f"\n--- Testing array size: {size} ---")

        test_list = generate_random_list(size)

        num_runs_fast = 10 if size < 10000 else 1

        timsort_time = timeit(
            stmt="data.sort()",
            setup="data = copy.copy(test_list)",
            globals={"test_list": test_list, "copy": copy},
            number=num_runs_fast,
        )
        print(f"Timsort time: {timsort_time:.5f} s (Runs: {num_runs_fast})")

        merge_time = timeit(
            stmt="merge_sort(data_merge)",
            setup=f"data_merge = copy.copy(test_list); from __main__ import merge_sort",
            globals={"test_list": test_list, "copy": copy, "merge_sort": merge_sort},
            number=num_runs_fast,
        )
        print(f"Merge Sort time: {merge_time:.5f} s (Runs: {num_runs_fast})")

        num_runs_insertion = 1 if size > 10000 else 10

        insertion_time = timeit(
            stmt="insertion_sort(data_insert)",
            setup=f"data_insert = copy.copy(test_list); from __main__ import insertion_sort",
            globals={
                "test_list": test_list,
                "copy": copy,
                "insertion_sort": insertion_sort,
            },
            number=num_runs_insertion,
        )
        print(
            f"Insertion Sort time: {insertion_time:.5f} s (Runs: {num_runs_insertion})"
        )

        results[size] = {
            "Timsort": timsort_time,
            "Insertion": insertion_time,
            "Merge": merge_time,
        }

    return results


if __name__ == "__main__":

    benchmark_data = run_benchmarks()
