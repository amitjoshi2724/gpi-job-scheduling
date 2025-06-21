#!/usr/bin/env python3

import boost_spreadsort
import numpy as np
import time
import random

def generate_normal_data(n):
    """Generate normally distributed data"""
    return [(np.random.normal(500, 100), np.random.normal(500, 100), random.uniform(1, 100)) for _ in range(n)]

def debug_timing_anomaly():
    """Debug the timing anomaly"""
    
    print("=== Debugging Timing Anomaly ===")
    print()
    
    # Test the problematic sizes multiple times
    sizes = [100, 500]
    num_trials = 10
    
    for n in sizes:
        print(f"Testing n = {n} ({num_trials} trials):")
        times = []
        
        for trial in range(num_trials):
            # Generate fresh data each time
            jobs = generate_normal_data(n)
            
            # Warm up (first call might be slower due to compilation/caching)
            if trial == 0:
                _ = boost_spreadsort.float_sort_both_with_indices(jobs)
                time.sleep(0.1)  # Brief pause
            
            # Time the actual call
            start_time = time.time()
            end_ordered, start_ordered = boost_spreadsort.float_sort_both_with_indices(jobs)
            end_time = time.time()
            
            total_time_ms = (end_time - start_time) * 1000
            times.append(total_time_ms)
            
            print(f"  Trial {trial+1}: {total_time_ms:.3f} ms")
        
        avg_time = np.mean(times)
        std_time = np.std(times)
        print(f"  Average: {avg_time:.3f} ± {std_time:.3f} ms")
        print(f"  Time per element: {avg_time/n:.6f} ms")
        print()

def test_warmup_effect():
    """Test if there's a warmup effect causing the anomaly"""
    
    print("=== Testing Warmup Effect ===")
    print()
    
    # Generate data once
    jobs_100 = generate_normal_data(100)
    jobs_500 = generate_normal_data(500)
    
    print("First call (cold start):")
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs_100)
    end_time = time.time()
    print(f"  n=100: {(end_time - start_time) * 1000:.3f} ms")
    
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs_500)
    end_time = time.time()
    print(f"  n=500: {(end_time - start_time) * 1000:.3f} ms")
    
    print("\nSecond call (warm):")
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs_100)
    end_time = time.time()
    print(f"  n=100: {(end_time - start_time) * 1000:.3f} ms")
    
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs_500)
    end_time = time.time()
    print(f"  n=500: {(end_time - start_time) * 1000:.3f} ms")

def test_data_generation_time():
    """Test if data generation is causing the issue"""
    
    print("=== Testing Data Generation Time ===")
    print()
    
    for n in [100, 500]:
        # Time data generation
        start_time = time.time()
        jobs = generate_normal_data(n)
        end_time = time.time()
        gen_time = (end_time - start_time) * 1000
        
        # Time sorting
        start_time = time.time()
        end_ordered, start_ordered = boost_spreadsort.float_sort_both_with_indices(jobs)
        end_time = time.time()
        sort_time = (end_time - start_time) * 1000
        
        print(f"n = {n}:")
        print(f"  Data generation: {gen_time:.3f} ms")
        print(f"  Sorting: {sort_time:.3f} ms")
        print(f"  Total: {gen_time + sort_time:.3f} ms")
        print()

if __name__ == "__main__":
    debug_timing_anomaly()
    print("\n" + "="*50 + "\n")
    test_warmup_effect()
    print("\n" + "="*50 + "\n")
    test_data_generation_time() 