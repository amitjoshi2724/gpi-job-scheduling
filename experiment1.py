import random
import time
import bisect
import matplotlib.pyplot as plt

def find_pred(jobs, start_i):
    lo, hi = 0, len(jobs)
    while lo < hi:
        mid = (lo + hi) // 2
        if jobs[mid][1] <= start_i:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1  # correctly gives index of latest non-overlapping job

def classic_weighted_interval_scheduling(jobs):
    #jobs.sort(key=lambda x: x[1])  # sort by end time
    jobs = radix_sort(jobs, key_index=1) # sort by end time
    n = len(jobs)
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        start_i, end_i, weight_i = jobs[i - 1]
        pred_idx = find_pred(jobs, start_i)
        include = weight_i + dp[pred_idx + 1] #dp[0] = 0
        dp[i] = max(dp[i - 1], include)

    return dp[n]

# Radix sort helper: sorts list of tuples by key_index
def radix_sort(jobs, key_index):
    max_val = max(job[key_index] for job in jobs)
    exp = 1
    base = 10
    while max_val // exp > 0:
        count = [[] for _ in range(base)]
        for job in jobs:
            digit = (job[key_index] // exp) % base
            count[digit].append(job)
        jobs = [job for bucket in count for job in bucket]
        exp *= base
    return jobs

# Template for your linear-time implementation
def linear_time_weighted_scheduling(jobs):
    n = len(jobs)
    end_ordered = radix_sort(jobs, key_index=1)  # sort by end time, 0-indexed array

    end_ordered = [(t[0], t[1], t[2], i+1) for i, t in enumerate(end_ordered)]

    start_ordered = radix_sort(end_ordered, key_index=0)  # sort by start time, 0-indexed array

    #print ("eo:", end_ordered)
    #print ("so:", start_ordered)
    p = [0] * (n + 1) # apparently a 1-indexed array
    endIndex = find_pred(end_ordered, start_ordered[n-1][0])+1 # endIndex is made to be 1-indexed
    for startIndex in range(n,0,-1): # startIndex is 1-indexed
        while endIndex >= 1 and end_ordered[endIndex-1][1] > start_ordered[startIndex-1][0]:
            endIndex -= 1
        if endIndex <= 0:
            break
        p[start_ordered[startIndex-1][3]] = endIndex
    
    #print ("p:", p)
    dp = [0] * (n + 1) #1-indexed

    for i in range(1, n + 1):
        start_i, end_i, weight_i,end_order_i = end_ordered[i - 1]
        include = weight_i + dp[p[i]]
        dp[i] = max(dp[i - 1], include)
        #print ('modifying index', i)
    #print (dp)
    return dp[n]



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