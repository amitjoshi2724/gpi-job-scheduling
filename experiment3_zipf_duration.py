# experiment_zipf.py
import random
import time
import gc
import numpy as np
import os
import matplotlib.pyplot as plt
from scheduling_algos import classic_weighted_interval_scheduling, linear_time_weighted_scheduling

# Setup
RANDOM_SEED = 2724
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ["OMP_NUM_THREADS"] = "1" # disable multi-thread noise
os.makedirs("figures", exist_ok=True)

results_classic = []
results_linear = []
results_classic_per_n = []
results_linear_per_n = []

for n in range(1000, 100001, 1000):
    total_classic = 0
    total_linear = 0
    runs = 20
    MAX_END = 10**6
    MAX_DURATION = 10**5

    for _ in range(runs):
        jobs = []
        for _ in range(n):
            end = random.randint(0, MAX_END)
            raw = np.random.zipf(2)
            duration = min(MAX_DURATION, max(1, int(100 * raw)))
            start = max(0, end - duration)
            weight = random.randint(1, 100)
            jobs.append((start, end, weight))
        
        jobs2 = jobs.copy()

        # Classic DP
        gc.collect()
        start = time.perf_counter()
        classic_answer = classic_weighted_interval_scheduling(jobs)
        end = time.perf_counter()
        total_classic += (end - start)

        # Linear-Time DP
        gc.collect()
        start = time.perf_counter()
        linear_answer = linear_time_weighted_scheduling(jobs2)
        end = time.perf_counter()
        total_linear += (end - start)

        if classic_answer != linear_answer:
            print("INCORRECT ANSWER", classic_answer, linear_answer)
            exit()

    avg_classic = total_classic / runs
    avg_linear = total_linear / runs
    results_classic.append((n, avg_classic))
    results_linear.append((n, avg_linear))
    results_classic_per_n.append((n, avg_classic / n))
    results_linear_per_n.append((n, avg_linear / n))
    print(f"n = {n}, classic = {avg_classic:.6f} s, linear = {avg_linear:.6f} s")

# Unpack for plotting
ns, classic_times = zip(*results_classic)
_, linear_times = zip(*results_linear)
_, classic_per_n = zip(*results_classic_per_n)
_, linear_per_n = zip(*results_linear_per_n)

# Plot 1: Total runtime
plt.figure(figsize=(8, 5))
plt.plot(ns, classic_times, marker='o', label='Classic DP with Binary Search')
plt.plot(ns, linear_times, marker='o', label='Our Linear-Time DP with Preprocessing')
plt.xlabel('Number of Jobs (n)')
plt.ylabel('Average Runtime (s)')
plt.title('Experiment 3 Zipf Durations (Wide Predecessor Spread): Total Runtime')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/experiment3_total_runtime.pdf")
plt.show()

# Plot 2: Runtime per job
plt.figure(figsize=(8, 5))
plt.plot(ns, classic_per_n, marker='o', label='Classic DP with Binary Search (per job)')
plt.plot(ns, linear_per_n, marker='o', label='Our Linear-Time DP with Preprocessing (per job)')
plt.xlabel('Number of Jobs (n)')
plt.ylabel('Average Runtime per Job (s)')
plt.title('Experiment 3 Zipf Durations (Wide Predecessor Spread): Runtime per Job')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/experiment3_per_job_runtime.pdf")
plt.show()

