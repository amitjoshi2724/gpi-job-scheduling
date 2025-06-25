#!/usr/bin/env python3

import numpy as np
import boost_spreadsort

def test_spreadsort_only(n):
    """Test only the spreadsort functionality with n elements"""
    print(f"Testing spreadsort with n={n}")
    
    # Generate simple test data
    start_times = np.random.uniform(1e8, 1e9, n)
    end_times = start_times + np.random.uniform(1e6, 1e7, n)
    weights = np.random.uniform(1, 100, n)
    
    # Create 3-tuples
    jobs_3 = [(float(s), float(e), float(w)) for s, e, w in zip(start_times, end_times, weights)]
    
    # Create 4-tuples (with indices)
    jobs_4 = [(float(s), float(e), float(w), i) for i, (s, e, w) in enumerate(zip(start_times, end_times, weights))]
    
    print(f"  Created {len(jobs_3)} 3-tuples and {len(jobs_4)} 4-tuples")
    
    try:
        # Test 3-tuple sorting
        print("  Testing 3-tuple sorting...")
        sorted_3 = boost_spreadsort.spreadsort_floats(jobs_3, 0)  # Sort by start time
        print("  ✓ 3-tuple sorting successful")
        
        # Test 4-tuple sorting
        print("  Testing 4-tuple sorting...")
        sorted_4 = boost_spreadsort.spreadsort_floats_4(jobs_4, 0)  # Sort by start time
        print("  ✓ 4-tuple sorting successful")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test with the problematic sizes
problematic_sizes = [999, 1000, 1001, 1002, 1003, 1004, 1005]
for n in problematic_sizes:
    success = test_spreadsort_only(n)
    if not success:
        print(f"Failed at n={n}")
        break
    print() 