#!/usr/bin/env python3

import numpy as np
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

print("Testing minimal experiment...")

# Try a range of n values to find the threshold
n_values = [10, 50, 100, 200, 400, 600, 800, 900, 950, 990, 999, 1000, 1001, 1100, 1500, 2000, 5000, 10000]
for n in n_values:
    print(f"\nTesting with n={n}")
    try:
        jobs = generate_normal_start_jobs(n)
        print(f"Generated {len(jobs)} jobs")
        
        # Debug: Check for NaN/Inf values
        jobs_python = [(float(t[0]), float(t[1]), float(t[2])) for t in jobs]
        has_nan = any(np.isnan(x[0]) or np.isnan(x[1]) or np.isnan(x[2]) for x in jobs_python)
        has_inf = any(np.isinf(x[0]) or np.isinf(x[1]) or np.isinf(x[2]) for x in jobs_python)
        print(f"Has NaN: {has_nan}, Has Inf: {has_inf}")
        
        # Debug: Check value ranges
        start_vals = [x[0] for x in jobs_python]
        end_vals = [x[1] for x in jobs_python]
        weight_vals = [x[2] for x in jobs_python]
        print(f"Start range: {min(start_vals):.2e} to {max(start_vals):.2e}")
        print(f"End range: {min(end_vals):.2e} to {max(end_vals):.2e}")
        print(f"Weight range: {min(weight_vals)} to {max(weight_vals)}")
        
        # Debug: Check first few values
        print(f"First 3 jobs: {jobs_python[:3]}")
        
        # Test with spreadsort
        result = gpi_weighted_job_scheduling(jobs, sortAlgo="spread")
        print(f"✓ Spreadsort result: {result}")
        
    except Exception as e:
        print(f"✗ Error with n={n}: {e}")
        import traceback
        traceback.print_exc()
        break 