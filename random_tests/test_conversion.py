#!/usr/bin/env python3

import numpy as np
import boost_spreadsort

def test_conversion_values():
    """Test the double_to_uint64 conversion with various values"""
    print("Testing double_to_uint64 conversion...")
    
    # Test with the actual values from our data
    test_values = [
        444279307.78592724,
        517133499.48149186,
        562853978.4134754,
        491501532.1797497,
        348800119.9228498,
        556462119.0753621
    ]
    
    for i, val in enumerate(test_values):
        print(f"  Test {i+1}: {val}")
        try:
            # Create a single tuple and try to sort it
            jobs = [(val, val + 1000000, 50.0)]
            result = boost_spreadsort.spreadsort_floats(jobs, 0)
            print(f"    ✓ Conversion successful")
        except Exception as e:
            print(f"    ✗ Error: {e}")
            return False
    
    return True

def test_conversion_with_size(n):
    """Test conversion with a specific size"""
    print(f"Testing conversion with n={n}")
    
    # Generate test data similar to what we use
    start_times = np.random.uniform(1e8, 1e9, n)
    end_times = start_times + np.random.uniform(1e6, 1e7, n)
    weights = np.random.uniform(1, 100, n)
    
    jobs = [(float(s), float(e), float(w)) for s, e, w in zip(start_times, end_times, weights)]
    
    print(f"  Created {len(jobs)} jobs")
    print(f"  First job: {jobs[0]}")
    
    try:
        # Test the conversion by sorting
        result = boost_spreadsort.spreadsort_floats(jobs, 0)
        print(f"  ✓ Conversion successful for n={n}")
        return True
    except Exception as e:
        print(f"  ✗ Error with n={n}: {e}")
        return False

# Test individual values first
if test_conversion_values():
    print("\nIndividual value tests passed. Testing with sizes...")
    
    # Test with problematic sizes
    problematic_sizes = [999, 1000, 1001, 1002]
    for n in problematic_sizes:
        success = test_conversion_with_size(n)
        if not success:
            print(f"Failed at n={n}")
            break
        print()
else:
    print("Individual value tests failed!") 