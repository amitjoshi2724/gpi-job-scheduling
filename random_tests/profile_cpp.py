#!/usr/bin/env python3

import boost_spreadsort
import numpy as np
import time
import random

def generate_test_jobs(n):
    """Generate n random jobs for testing"""
    jobs = []
    for _ in range(n):
        start = random.uniform(0, 1000)
        duration = random.uniform(1, 100)
        end = start + duration
        weight = random.uniform(1, 100)
        jobs.append((start, end, weight))
    return jobs

def profile_cpp_function():
    """Profile the C++ function with different input sizes"""
    sizes = [1000, 5000, 10000, 50000, 100000]
    
    print("=== C++ Function Profiling Comparison ===")
    print("Testing original vs optimized versions...")
    print()
    
    for n in sizes:
        print(f"Testing with n = {n}")
        
        # Generate test data
        jobs = generate_test_jobs(n)
        
        # Test original version
        print("  Original version:")
        start_time = time.time()
        end_ordered1, start_ordered1 = boost_spreadsort.float_sort_both_with_indices(jobs)
        end_time = time.time()
        original_time = (end_time - start_time) * 1000000
        
        # Test optimized version
        print("  Optimized version:")
        start_time = time.time()
        end_ordered2, start_ordered2 = boost_spreadsort.float_sort_both_with_indices_optimized(jobs)
        end_time = time.time()
        optimized_time = (end_time - start_time) * 1000000
        
        # Verify results are the same
        assert len(end_ordered1) == len(end_ordered2)
        assert len(start_ordered1) == len(start_ordered2)
        
        print(f"  Original time: {original_time:.2f} μs")
        print(f"  Optimized time: {optimized_time:.2f} μs")
        print(f"  Speedup: {original_time/optimized_time:.2f}x")
        print("-" * 50)
        print()

if __name__ == "__main__":
    profile_cpp_function() 