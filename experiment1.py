import random
import time
import matplotlib.pyplot as plt





results_classic = []
results_linear = []

for n in range(1000, 100001, 1000):
    total_classic = 0
    total_linear = 0
    runs = 20
    MAX_VAL = 10**6
    for _ in range(runs):
        jobs = [(random.randint(0, MAX_VAL), random.randint(0, MAX_VAL), random.randint(1, 100)) for _ in range(n)]
        jobs = [(min(s, e), max(s, e), w) for s, e, w in jobs]
        #jobs = [(52, 60, 76), (82, 86, 9), (10, 49, 63), (63, 75, 33)]
        #print (jobs)
        # Classic
        start = time.perf_counter()
        classicAnswer = classic_weighted_interval_scheduling(jobs)
        end = time.perf_counter()
        total_classic += (end - start)

        # Linear (call your real implementation here)
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
plt.plot(ns_linear, times_linear, marker='x', label='Linear-Time DP')
plt.xlabel('Number of Jobs (n)')
plt.ylabel('Average Runtime (s)')
plt.title('Runtime Comparison: Classic DP vs Linear-Time DP')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()