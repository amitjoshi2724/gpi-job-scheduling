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
# GitHub: https://github.com/amitjoshi24


def find_pred(jobs, start_i):
    lo, hi = 0, len(jobs)
    while lo < hi:
        mid = (lo + hi) // 2
        if jobs[mid][1] <= start_i:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1  # correctly gives index of latest non-overlapping job

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

# Template for your linear-time implementation
def linear_time_weighted_scheduling(jobs):
    n = len(jobs)
    end_ordered = radix_sort(jobs, key_index=1)  # sort by end time, 0-indexed array

    end_ordered = [(t[0], t[1], t[2], i+1) for i, t in enumerate(end_ordered)]

    start_ordered = radix_sort(end_ordered, key_index=0)  # sort by start time, 0-indexed array

    p = [0] * (n + 1) # apparently a 1-indexed array
    endIndex = find_pred(end_ordered, start_ordered[n-1][0])+1 # endIndex is made to be 1-indexed
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
