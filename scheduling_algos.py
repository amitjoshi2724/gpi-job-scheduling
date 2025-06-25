# Copyright 2025 Amit Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Amit Joshi
# Email 1: amitjoshi2724@gmail.com
# Email 2: amit.joshiusa@gmail.com
# GitHub: https://github.com/amitjoshi2724

import boost_spreadsort
import numpy as np

# bisect_right, a binary search
def find_pred(jobs, start_i):
    lo, hi = 0, len(jobs)
    while lo < hi:
        mid = (lo + hi) // 2
        if jobs[mid][1] <= start_i:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1  # correctly gives index of latest non-overlapping job

# O(n log(n)) DP solution for WIS, our baseline to improve upon
def classic_weighted_interval_scheduling(jobs, sortAlgo='default'):
    if sortAlgo == 'radix':
        jobs = radix_sort(jobs, key_index=1) # sort by end time with radix sort
    else:
        jobs.sort(key=lambda x: x[1])  # sort by end time with comparison-based sorting
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

def bucket_sort(jobs, key_index):
    n = len(jobs)
    if n == 0:
        return []

    min_val = min(job[key_index] for job in jobs)
    max_val = max(job[key_index] for job in jobs)
    if max_val == min_val:
        return jobs.copy()

    # Create n buckets
    buckets = [[] for _ in range(n)]
    scale = (n - 1) / (max_val - min_val + 1e-9)  # avoid div by 0

    # Assign jobs to buckets
    for job in jobs:
        idx = int((job[key_index] - min_val) * scale)
        buckets[idx].append(job)

    # Sort each bucket and concatenate
    sorted_jobs = []
    for bucket in buckets:
        sorted_jobs.extend(sorted(bucket, key=lambda job: job[key_index]))
    return sorted_jobs

def recursive_adaptive_bucket_sort(jobs, key_index, depth=0, max_depth=10, min_bucket_size=16):
    if len(jobs) <= min_bucket_size or depth >= max_depth:
        return sorted(jobs, key=lambda job: job[key_index])

    min_val = min(job[key_index] for job in jobs)
    max_val = max(job[key_index] for job in jobs)
    if max_val == min_val:
        return jobs.copy()  # already sorted

    num_buckets = len(jobs)
    scale = num_buckets / (max_val - min_val + 1e-9)
    buckets = [[] for _ in range(num_buckets)]
    for job in jobs:
        idx = int((job[key_index] - min_val) * scale)
        idx = min(idx, num_buckets - 1)
        buckets[idx].append(job)

    sorted_jobs = []
    for bucket in buckets:
        sorted_jobs.extend(recursive_adaptive_bucket_sort(bucket, key_index, depth + 1, max_depth, min_bucket_size))
    return sorted_jobs


# Our novel O(n) Multi-Phase Preprocessing and DP Solution for WJS or WIS
def gpi_weighted_job_scheduling(jobs, sortAlgo='default'):
    n = len(jobs)
    if sortAlgo == 'radix':
        end_ordered = radix_sort(jobs, key_index=1)  # sort by end time, 0-indexed array
        end_ordered = [(t[0], t[1], t[2], i+1) for i, t in enumerate(end_ordered)]
        start_ordered = radix_sort(end_ordered, key_index=0)  # sort by start time, 0-indexed array
    elif sortAlgo == 'bucket':
        end_ordered = bucket_sort(jobs, key_index=1)  # sort by end time, 0-indexed array
        end_ordered = [(t[0], t[1], t[2], i+1) for i, t in enumerate(end_ordered)]
        start_ordered = bucket_sort(end_ordered, key_index=0)  # sort by start time, 0-indexed array
    elif sortAlgo == 'recursive bucket':
        end_ordered = recursive_adaptive_bucket_sort(jobs, key_index=1)  # sort by end time, 0-indexed array
        end_ordered = [(t[0], t[1], t[2], i+1) for i, t in enumerate(end_ordered)]
        start_ordered = recursive_adaptive_bucket_sort(end_ordered, key_index=0)  # sort by start time, 0-indexed array
    elif sortAlgo == 'spread':
        # Use the optimized function that does both sorts and adds indices in one C++ call
        end_ordered, start_ordered = boost_spreadsort.float_sort_both_with_indices(jobs)
    else:
        end_ordered = sorted(jobs, key = lambda x: x[1])
        end_ordered = [(t[0], t[1], t[2], i+1) for i, t in enumerate(end_ordered)]
        start_ordered = sorted(end_ordered, key = lambda x: x[0])

    p = [0] * (n + 1) # apparently a 1-indexed array
    endIndex = find_pred(end_ordered, start_ordered[n-1][0])+1 # endIndex is made to be 1-indexed
    #endIndex = n
    for startIndex in range(n,0,-1): # startIndex is 1-indexed
        while endIndex >= 1 and end_ordered[endIndex-1][1] > start_ordered[startIndex-1][0]:
            endIndex -= 1
        if endIndex <= 0:
            break
        p[start_ordered[startIndex-1][3]] = endIndex
    
    dp = [0] * (n + 1) #1-indexed

    for i in range(1, n + 1):
        start_i, end_i, weight_i,end_order_i = end_ordered[i - 1]
        include = weight_i + dp[p[i]]
        dp[i] = max(dp[i - 1], include)

    return dp[n]
