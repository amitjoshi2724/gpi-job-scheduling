#!/usr/bin/env python3

import numpy as np
import time
import gc
import random
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

print("Testing spreadsort-only experiment...")

# Set the same random seed as the experiment
RANDOM_SEED = 2724
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Test with just one n value and one trial
n = 1000
trials = 1

for trial in range(trials):
    print(f"\nTrial {trial + 1}")
    try:
        jobs = generate_normal_start_jobs(n)
        print(f"Generated {len(jobs)} jobs")
        
        # Test ONLY with spreadsort (no other algorithms)
        gc.enable(); gc.collect(); gc.disable()
        start = time.perf_counter()
        gpiLinearAnswer = gpi_weighted_job_scheduling(jobs, sortAlgo="spread")
        end = time.perf_counter()
        
        print(f"✓ Spreadsort result: {gpiLinearAnswer}")
        print(f"✓ Time: {end - start:.6f} seconds")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        break 