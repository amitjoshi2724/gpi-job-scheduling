#!/usr/bin/env python3

import boost_spreadsort
import numpy as np
import time
import random

def generate_normal_data(n):
    """Generate normally distributed data"""
    return [(np.random.normal(500, 100), np.random.normal(500, 100), random.uniform(1, 100)) for _ in range(n)]

def debug_small_inputs():
    """Debug why small inputs are slow"""
    
    print("=== Debugging Small Input Performance ===")
    print()
    
    # Test with n=100 multiple times
    print("Testing n=100 with Normal distribution (10 trials):")
    times = []
    
    for trial in range(10):
        # Generate data
        jobs = generate_normal_data(100)
        
        # Time the sorting
        start_time = time.time()
        end_ordered, start_ordered = boost_spreadsort.float_sort_both_with_indices(jobs)
        end_time = time.time()
        
        total_time_ms = (end_time - start_time) * 1000
        times.append(total_time_ms)
        
        print(f"  Trial {trial+1}: {total_time_ms:.3f} ms")
    
    print(f"  Average: {np.mean(times):.3f} ms")
    print(f"  Std Dev: {np.std(times):.3f} ms")
    print(f"  Min: {np.min(times):.3f} ms")
    print(f"  Max: {np.max(times):.3f} ms")
    print()
    
    # Test if it's a warmup issue
    print("Testing warmup effect:")
    jobs = generate_normal_data(100)
    
    # First call
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs)
    end_time = time.time()
    first_call = (end_time - start_time) * 1000
    print(f"  First call: {first_call:.3f} ms")
    
    # Second call immediately after
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs)
    end_time = time.time()
    second_call = (end_time - start_time) * 1000
    print(f"  Second call: {second_call:.3f} ms")
    
    # Third call after a pause
    time.sleep(0.1)
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs)
    end_time = time.time()
    third_call = (end_time - start_time) * 1000
    print(f"  Third call (after pause): {third_call:.3f} ms")
    print()

def test_different_distributions():
    """Test if the issue is specific to certain distributions"""
    
    print("=== Testing Different Distributions (n=100) ===")
    print()
    
    # Uniform distribution
    jobs_uniform = [(random.uniform(0, 1000), random.uniform(0, 1000), random.uniform(1, 100)) for _ in range(100)]
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs_uniform)
    end_time = time.time()
    uniform_time = (end_time - start_time) * 1000
    print(f"Uniform: {uniform_time:.3f} ms")
    
    # Normal distribution
    jobs_normal = generate_normal_data(100)
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs_normal)
    end_time = time.time()
    normal_time = (end_time - start_time) * 1000
    print(f"Normal: {normal_time:.3f} ms")
    
    # Simple normal (without numpy)
    jobs_simple = [(random.gauss(500, 100), random.gauss(500, 100), random.uniform(1, 100)) for _ in range(100)]
    start_time = time.time()
    _ = boost_spreadsort.float_sort_both_with_indices(jobs_simple)
    end_time = time.time()
    simple_time = (end_time - start_time) * 1000
    print(f"Simple Normal: {simple_time:.3f} ms")
    print()

def test_data_characteristics():
    """Test if the data characteristics are causing the issue"""
    
    print("=== Testing Data Characteristics ===")
    print()
    
    # Generate normal data and examine it
    jobs = generate_normal_data(100)
    
    # Extract start and end times
    starts = [job[0] for job in jobs]
    ends = [job[1] for job in jobs]
    
    print(f"Start times - Min: {min(starts):.2f}, Max: {max(starts):.2f}, Range: {max(starts) - min(starts):.2f}")
    print(f"End times - Min: {min(ends):.2f}, Max: {max(ends):.2f}, Range: {max(ends) - min(ends):.2f}")
    
    # Check for any extreme values
    print(f"Any negative values: {any(s < 0 or e < 0 for s, e, _ in jobs)}")
    print(f"Any NaN values: {any(np.isnan(s) or np.isnan(e) for s, e, _ in jobs)}")
    print(f"Any infinite values: {any(np.isinf(s) or np.isinf(e) for s, e, _ in jobs)}")
    print()

if __name__ == "__main__":
    debug_small_inputs()
    test_different_distributions()
    test_data_characteristics() 