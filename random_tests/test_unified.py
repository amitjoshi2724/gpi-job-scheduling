#!/usr/bin/env python3

import sys
import os

# Add the build directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'build'))

try:
    import boost_spreadsort
    print("✓ Successfully imported boost_spreadsort module")
    
    # Test with some sample data
    import random
    
    print("\n=== Testing Unified Int Functions ===")
    
    # Test 3-element int tuples
    int_jobs_3 = [(random.randint(1, 100), random.randint(1, 100), random.random()) for _ in range(3)]
    print(f"Original int jobs (3): {int_jobs_3}")
    
    sorted_int_3 = boost_spreadsort.spreadsort_ints_unified(int_jobs_3.copy(), 0)
    print(f"Sorted by first element: {sorted_int_3}")
    
    # Test 4-element int tuples
    int_jobs_4 = [(random.randint(1, 100), random.randint(1, 100), random.random(), random.randint(1, 10)) for _ in range(3)]
    print(f"\nOriginal int jobs (4): {int_jobs_4}")
    
    sorted_int_4 = boost_spreadsort.spreadsort_ints_unified(int_jobs_4.copy(), 0)
    print(f"Sorted by first element: {sorted_int_4}")
    
    print("\n=== Testing Unified Float Functions ===")
    
    # Test 3-element float tuples
    float_jobs_3 = [(random.random() * 100, random.random() * 100, random.random()) for _ in range(3)]
    print(f"Original float jobs (3): {float_jobs_3}")
    
    sorted_float_3 = boost_spreadsort.spreadsort_floats_unified(float_jobs_3.copy(), 0)
    print(f"Sorted by first element: {sorted_float_3}")
    
    # Test 4-element float tuples
    float_jobs_4 = [(random.random() * 100, random.random() * 100, random.random(), random.randint(1, 10)) for _ in range(3)]
    print(f"\nOriginal float jobs (4): {float_jobs_4}")
    
    sorted_float_4 = boost_spreadsort.spreadsort_floats_unified(float_jobs_4.copy(), 0)
    print(f"Sorted by first element: {sorted_float_4}")
    
    print("\n✓ All unified spreadsort tests passed!")
    
except ImportError as e:
    print(f"✗ Failed to import boost_spreadsort: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error during testing: {e}")
    sys.exit(1) 