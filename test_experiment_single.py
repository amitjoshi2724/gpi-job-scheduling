#!/usr/bin/env python3

import numpy as np
import time
import gc
from scheduling_algos import gpi_weighted_job_scheduling

def generate_normal_start_jobs(n):
    K = 10**9
    sigma = K / 10
    start_times = np.clip(np.random.normal(loc=K/2, scale=sigma, size=n), 0, K)
    durations = np.random.uniform(1.0, 10**6, size=n)
    end_times = start_times + durations
    weights = np.random.randint(1, 101, size=n)
    jobs = list(zip(start_times, end_times, weights))
    return jobs

print("Testing single experiment iteration...")

# Test with the actual experiment parameters
n = 1000  # n_start from experiment
trials = 1  # Just one trial

for trial in range(trials):
    print(f"\nTrial {trial + 1}")
    try:
        jobs = generate_normal_start_jobs(n)
        print(f"Generated {len(jobs)} jobs")
        
        # Test with spreadsort
        gc.enable(); gc.collect(); gc.disable()
        start = time.perf_counter()
        result = gpi_weighted_job_scheduling(jobs, sortAlgo="spread")
        end = time.perf_counter()
        
        print(f"✓ Spreadsort result: {result}")
        print(f"✓ Time: {end - start:.6f} seconds")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        break 