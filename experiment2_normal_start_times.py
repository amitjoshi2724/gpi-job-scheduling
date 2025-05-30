import random
import time
import gc
import matplotlib.pyplot as plt
import numpy as np
from scheduling_algos import classic_weighted_interval_scheduling, linear_time_weighted_scheduling

RANDOM_SEED = 2724
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

results_classic = []
results_linear = []

for n in range(1000, 100000 + 1, 1000):
    total_classic = 0
    total_linear = 0
    trials = 10
    K = 10**9
    sigma = K / 10
    for _ in range(trials):
        # Truncated normal start times in [0, K]
        start_times = np.clip(np.random.normal(loc=K/2, scale=sigma, size=n), 0, K)
        durations = np.random.uniform(1.0, 1000.0, size=n)
        end_times = start_times + durations
        weights = np.random.randint(1, 101, size=n)
        jobs = list(zip(start_times, end_times, weights))

        # Classic
        gc.enable()
        gc.collect()
        gc.disable()
        start = time.perf_counter()
        classicAnswer = classic_weighted_interval_scheduling(jobs, sortAlgo="default")
        end = time.perf_counter()
        total_classic += (end - start)

        # Linear
        gc.enable()
        gc.collect()
        gc.disable()
        start = time.perf_counter()
        linearTimeAnswer = linear_time_weighted_scheduling(jobs, sortAlgo="spread")
        end = time.perf_counter()
        total_linear += (end - start)

        if classicAnswer != linearTimeAnswer:
            print('INCORRECT ANSWER', classicAnswer, linearTimeAnswer)
            exit()

    avg_classic = total_classic / trials
    avg_linear = total_linear / trials
    results_classic.append((n, avg_classic))
    results_linear.append((n, avg_linear))
    print(f"n = {n}, classic = {avg_classic:.6f} s, linear = {avg_linear:.6f} s")

EXP_TITLE = "Normally Distributed Start Times (Smooth Clustered Inputs)"
GPI_SORT = "(Spread Sort)"
# Plot
ns_classic, times_classic = zip(*results_classic)
ns_linear, times_linear = zip(*results_linear)

ns = ns_classic # same values of n
per_job_classic = [t / n for t, n in zip(times_classic, ns)]
per_job_linear = [t / n for t, n in zip(times_linear, ns)]

plt.plot(ns, per_job_classic, marker='o', label='Classic DP per job')
plt.plot(ns, per_job_linear, marker='s', label='GPI Linear-Time DP per job' + GPI_SORT)
plt.xlabel('Number of Jobs (n)')
plt.ylabel('Average Runtime (s)')
plt.title('Runtime Comparison: ', EXP_TITLE)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

fig2 = plt.figure(figsize=(10, 5))
plt.plot(ns, per_job_classic, marker='o', label='Classic DP (per job)')
plt.plot(ns, per_job_linear, marker='s', label='GPI Linear-Time DP' + GPI_SORT + '(per job)')
plt.xlabel('Number of Jobs (n)')
plt.ylabel('Average Runtime per Job (s)')
plt.title('Per-Job Runtime: ', EXP_TITLE)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Display both at the same time
plt.show(block=False)
input("Press Enter to exit and close plots...")
