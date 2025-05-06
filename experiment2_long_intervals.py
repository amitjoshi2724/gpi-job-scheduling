# experiment2_long_intervals.py
import random
import time
import bisect
import gc
import matplotlib.pyplot as plt
from scheduling_algos import classic_weighted_interval_scheduling, linear_time_weighted_scheduling

def classic_weighted_interval_scheduling(jobs):
    jobs.sort(key=lambda x: x[1])
    n = len(jobs)
    dp = [0] * (n + 1)
    end_times = [job[1] for job in jobs]

    for i in range(1, n + 1):
        start_i, end_i, weight_i = jobs[i - 1]
        pred_idx = bisect.bisect_right(end_times, start_i) - 1
        include = weight_i + (dp[pred_idx + 1] if pred_idx != -1 else 0)
        dp[i] = max(dp[i - 1], include)
    return dp[n]

results = []
for n in range(1000, 100000+1, 1000):
    total_classic = 0
    total_linear = 0
    runs = 20
    MAX_VAL = 10**6
    for _ in range(runs):
        jobs = []
        for _ in range(n):
            start = random.randint(0, 10**6)
            duration = random.randint(10_000, 100_000)
            end = start + duration
            weight = random.randint(1, 100)
            jobs.append((start, end, weight))
        # Classic
        gc.collect()
        start = time.perf_counter()
        classicAnswer = classic_weighted_interval_scheduling(jobs)
        end = time.perf_counter()
        total_classic += (end - start)

        # Linear (call your real implementation here)
        gc.collect()
        start = time.perf_counter()
        linearTimeAnswer = linear_time_weighted_scheduling(jobs)
        end = time.perf_counter()
        total_linear += (end - start)

        if classicAnswer != linearTimeAnswer:
            print ('INCORRECT ANSWER', classicAnswer, linearTimeAnswer)
            exit()

    avg_classic = total_classic / runs
    avg_linear = total_linear / runs
    results_classic.append((n, avg_classic))
    results_linear.append((n, avg_linear))
    print(f"n = {n}, classic = {avg_classic:.6f} s, linear = {avg_linear:.6f} s")

# Plot
ns_classic, times_classic = zip(*results_classic)
ns_linear, times_linear = zip(*results_linear)

plt.plot(ns_classic, times_classic, marker='o', label='Classic DP')
plt.plot(ns_linear, times_linear, marker='o', label='Linear-Time DP')
plt.xlabel('Number of Jobs (n)')
plt.ylabel('Average Runtime (s)')
plt.title('Runtime Comparison: Classic DP vs Linear-Time DP')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

