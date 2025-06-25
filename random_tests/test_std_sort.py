#!/usr/bin/env python3

import numpy as np
import boost_spreadsort

def test_std_sort(n):
    """Test the std::sort function with n elements"""
    print(f"Testing std::sort with n={n}")
    
    # Generate test data
    start_times = np.random.uniform(1e8, 1e9, n)
    end_times = start_times + np.random.uniform(1e6, 1e7, n)
    weights = np.random.uniform(1, 100, n)
    
    jobs = [(float(s), float(e), float(w)) for s, e, w in zip(start_times, end_times, weights)]
    
    print(f"  Created {len(jobs)} jobs")
    
    try:
        # Test std::sort
        result = boost_spreadsort.std_sort_test(jobs)
        print(f"  ✓ std::sort successful for n={n}")
        return True
    except Exception as e:
        print(f"  ✗ Error with n={n}: {e}")
        return False

# Test with problematic sizes
problematic_sizes = [999, 1000, 1001, 1002, 1003, 1004, 1005]
for n in problematic_sizes:
    success = test_std_sort(n)
    if not success:
        print(f"Failed at n={n}")
        break
    print() 