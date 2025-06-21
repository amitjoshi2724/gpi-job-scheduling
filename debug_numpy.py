#!/usr/bin/env python3

import numpy as np
import boost_spreadsort

# Simulate the job generation from experiment2
def generate_normal_start_jobs(n):
    K = 10**9
    sigma = K / 10
    start_times = np.clip(np.random.normal(loc=K/2, scale=sigma, size=n), 0, K)
    durations = np.random.uniform(1.0, 10**6, size=n)
    end_times = start_times + durations
    weights = np.random.randint(1, 101, size=n)
    jobs = list(zip(start_times, end_times, weights))
    return jobs

print("Testing numpy array handling...")

# Generate some test jobs
jobs = generate_normal_start_jobs(5)
print(f"Original jobs type: {type(jobs)}")
print(f"First job type: {type(jobs[0])}")
print(f"First job: {jobs[0]}")
print(f"First job elements: {type(jobs[0][0])}, {type(jobs[0][1])}, {type(jobs[0][2])}")

# Convert to Python types
jobs_python = [(float(t[0]), float(t[1]), float(t[2])) for t in jobs]
print(f"Python jobs type: {type(jobs_python)}")
print(f"First Python job: {jobs_python[0]}")

# Test spreadsort
print("Testing spreadsort...")
try:
    end_ordered = boost_spreadsort.spreadsort_floats(jobs_python, 1)
    print("✓ First spreadsort successful")
    print(f"End ordered: {end_ordered}")
    
    # Add indices
    end_ordered_with_indices = [(t[0], t[1], t[2], i+1) for i, t in enumerate(end_ordered)]
    print(f"With indices: {end_ordered_with_indices}")
    
    # Test second spreadsort
    start_ordered = boost_spreadsort.spreadsort_floats_4(end_ordered_with_indices, 0)
    print("✓ Second spreadsort successful")
    print(f"Start ordered: {start_ordered}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc() 