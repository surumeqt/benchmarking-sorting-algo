import time
import psutil
import tracemalloc
from algorithms.BubbleSort import bubble_sort
from algorithms.MergeSort import merge_sort
from validate.Validate import load_dataset
import threading

# -----------------------------
# CONFIGURATION
# -----------------------------
DATASETS = {
    "1,000 elements": "data/dataset_1000.txt",
    "5,000 elements": "data/dataset_5000.txt",
    "10,000 elements": "data/dataset_10000.txt"
}

TRIALS = 5
# -----------------------------

def benchmark_algorithm(algorithm, data):
    """Benchmark an algorithm and record execution time, CPU usage, memory usage, and energy consumption."""

    process = psutil.Process()

    # CPU sampling
    cpu_usage_samples = []
    running = True

    def sample_cpu():
        while running:
            cpu_usage_samples.append(psutil.cpu_percent(interval=0.05))

    cpu_thread = threading.Thread(target=sample_cpu)
    cpu_thread.start()

    # Start memory tracking
    tracemalloc.start()

    # TIME MEASUREMENT
    start_time = time.perf_counter()
    algorithm(data)
    end_time = time.perf_counter()

    # Stop CPU sampling
    running = False
    cpu_thread.join()

    # MEMORY: peak memory from tracemalloc
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_memory_mb = peak / (1024 * 1024)

    # CPU: average CPU usage
    avg_cpu_usage = sum(cpu_usage_samples) / len(cpu_usage_samples) if cpu_usage_samples else 0

    # ENERGY (estimated)
    energy_consumption = avg_cpu_usage * (end_time - start_time)

    return {
        "execution_time": end_time - start_time,
        "avg_cpu": avg_cpu_usage,
        "memory_used": peak_memory_mb,
        "energy": energy_consumption
    }


def benchmark():
    print("\n===== ENHANCED SORTING BENCHMARK (WITH OVERALL RUNTIME) =====\n")

    for label, path in DATASETS.items():
        print(f"\n--- Dataset: {label} ---")

        dataset = load_dataset(path)
        if not dataset:
            continue

        bubble_results = []
        merge_results = []

        # Track total runtime of all 5 trials
        total_runtime_bubble = 0
        total_runtime_merge = 0

        for t in range(TRIALS):
            print(f"  Trial {t+1}/{TRIALS}")

            b_res = benchmark_algorithm(bubble_sort, dataset)
            m_res = benchmark_algorithm(merge_sort, dataset)

            bubble_results.append(b_res)
            merge_results.append(m_res)

            total_runtime_bubble += b_res["execution_time"]
            total_runtime_merge += m_res["execution_time"]

        # Averages
        avg_bubble = {
            "time": sum(r["execution_time"] for r in bubble_results) / TRIALS,
            "cpu": sum(r["avg_cpu"] for r in bubble_results) / TRIALS,
            "mem": sum(r["memory_used"] for r in bubble_results) / TRIALS,
            "energy": sum(r["energy"] for r in bubble_results) / TRIALS
        }

        avg_merge = {
            "time": sum(r["execution_time"] for r in merge_results) / TRIALS,
            "cpu": sum(r["avg_cpu"] for r in merge_results) / TRIALS,
            "mem": sum(r["memory_used"] for r in merge_results) / TRIALS,
            "energy": sum(r["energy"] for r in merge_results) / TRIALS
        }

        print("\nResults Summary:")
        print(f"  Bubble Sort:")
        print(f"     Execution Time (avg) : {avg_bubble['time']:.6f} sec")
        print(f"     Avg CPU Usage        : {avg_bubble['cpu']:.2f}%")
        print(f"     Peak Memory Used     : {avg_bubble['mem']:.4f} MB")
        print(f"     Energy Consumption   : {avg_bubble['energy']:.6f}")
        print(f"     Overall Runtime (5 trials) : {total_runtime_bubble:.6f} sec")

        print(f"\n  Merge Sort:")
        print(f"     Execution Time (avg) : {avg_merge['time']:.6f} sec")
        print(f"     Avg CPU Usage        : {avg_merge['cpu']:.2f}%")
        print(f"     Peak Memory Used     : {avg_merge['mem']:.4f} MB")
        print(f"     Energy Consumption   : {avg_merge['energy']:.6f}")
        print(f"     Overall Runtime (5 trials) : {total_runtime_merge:.6f} sec")

        print("\n---------------------------------------------")

if __name__ == "__main__":
    benchmark()