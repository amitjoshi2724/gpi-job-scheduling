#!/usr/bin/env python3

import numpy as np
import boost_spreadsort

def test_simple_spreadsort(n):
    """Test the simple spreadsort function with n elements"""
    print(f"Testing simple spreadsort with n={n}")
    
    # Generate simple test data
    start_times = np.random.uniform(1e8, 1e9, n)
    end_times = start_times + np.random.uniform(1e6, 1e7, n)
    weights = np.random.uniform(1, 100, n)
    
    # Create 3-tuples
    jobs_3 = [(float(s), float(e), float(w)) for s, e, w in zip(start_times, end_times, weights)]
    
    print(f"  Created {len(jobs_3)} 3-tuples")
    
    try:
        # Test simple sorting
        print("  Testing simple sorting...")
        sorted_3 = boost_spreadsort.spreadsort_simple_test(jobs_3)
        print("  ✓ Simple sorting successful")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test with the problematic sizes
problematic_sizes = [999, 1000, 1001, 1002, 1003, 1004, 1005]
for n in problematic_sizes:
    success = test_simple_spreadsort(n)
    if not success:
        print(f"Failed at n={n}")
        break
    print() 