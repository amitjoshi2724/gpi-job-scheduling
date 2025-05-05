# experiment2_long_intervals.py

import random
import time
import bisect
import matplotlib.pyplot as plt

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
for n in range(1000, 100001, 1000):
    total_time = 0
    runs = 20
    for _ in range(runs):
        jobs = []
        for _ in range(n):
            start = random.randint(0, 10**6)
            duration = random.randint(10_000, 100_000)
            end = start + duration
            weight = random.randint(1, 100)
            jobs.append((start, end, weight))

        start_t = time.perf_counter()
        classic_weighted_interval_scheduling(jobs)
        end_t = time.perf_counter()
        total_time += (end_t - start_t)
    avg_time = total_time / runs
    results.append((n, avg_time))
    print(f"[Long Intervals] n = {n}, avg_time = {avg_time:.6f} sec")

ns, times = zip(*results)
plt.plot(ns, times, marker='s', label='Classic DP (Long Intervals)')
plt.xlabel('Number of Jobs (n)')
plt.ylabel('Average Runtime (s)')
plt.title('Runtime of Classic DP on Long Interval Jobs')
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.show()

