#!/usr/bin/env python3

import numpy as np
import boost_spreadsort
import traceback

def test_float_sort_tuples(n):
    print(f"Testing float_sort_tuples_by_key with n={n}")
    
    # Generate test data
    start_times = np.random.uniform(1e8, 1e9, n)
    end_times = start_times + np.random.uniform(1e6, 1e7, n)
    weights = np.random.uniform(1, 100, n)
    
    # Create 3-tuples
    jobs_3 = [(float(s), float(e), float(w)) for s, e, w in zip(start_times, end_times, weights)]
    
    # Create 4-tuples (with indices)
    jobs_4 = [(float(s), float(e), float(w), i) for i, (s, e, w) in enumerate(zip(start_times, end_times, weights))]
    
    try:
        # Test 3-tuple sorting
        result_3 = boost_spreadsort.float_sort_tuples_by_key(jobs_3, 0)  # Sort by start time
        print(f"  ✓ 3-tuple sorting successful")
        
        # Test 4-tuple sorting
        result_4 = boost_spreadsort.float_sort_tuples_4_by_key(jobs_4, 0)  # Sort by start time
        print(f"  ✓ 4-tuple sorting successful")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

sizes = [999, 1000, 1001, 1002, 1003, 1004, 1005, 2000, 5000, 10000, 20000, 50000, 100000]
for n in sizes:
    if not test_float_sort_tuples(n):
        print(f"Failed at n={n}")
        break
    print() 