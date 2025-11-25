import time
from algorithms.BubbleSort import bubble_sort
from algorithms.MergeSort import merge_sort
from validate.Validate import load_dataset

# -------------------------------
# CONFIGURATION
# -------------------------------
DATASETS = {
    "1,000 elements": "data/dataset_1000.txt",
    "10,000 elements": "data/dataset_10000.txt",
    "50,000 elements": "data/dataset_50000.txt"
}

TRIALS = 5  # Run each algorithm multiple times
# -------------------------------


def test_algorithm(algorithm, data):
    """Runs a sorting algorithm and returns execution time."""
    start = time.perf_counter()
    algorithm(data)
    end = time.perf_counter()
    return end - start


def benchmark():
    print("\n===== SORTING ALGORITHM BENCHMARK =====\n")

    for label, path in DATASETS.items():
        print(f"\n--- Dataset: {label} ---")

        dataset = load_dataset(path)
        if not dataset:
            continue

        # Repeat trials for better accuracy
        bubble_times = []
        merge_times = []

        print(f"Running {TRIALS} trials each...\n")

        for t in range(TRIALS):
            print(f"  Trial {t+1}/{TRIALS}")

            bubble_time = test_algorithm(bubble_sort, dataset)
            merge_time = test_algorithm(merge_sort, dataset)

            bubble_times.append(bubble_time)
            merge_times.append(merge_time)

        # Compute average
        avg_bubble = sum(bubble_times) / TRIALS
        avg_merge = sum(merge_times) / TRIALS

        print("\nResults:")
        print(f"  Bubble Sort Average Time: {avg_bubble:.6f} seconds")
        print(f"  Merge Sort  Average Time: {avg_merge:.6f} seconds\n")


if __name__ == "__main__":
    benchmark()