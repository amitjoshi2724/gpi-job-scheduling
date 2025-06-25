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
    
    # Test integer sorting
    int_jobs = [(random.randint(1, 100), random.randint(1, 100), random.random()) for _ in range(10)]
    print(f"Original int jobs: {int_jobs[:3]}...")
    
    sorted_int_jobs = boost_spreadsort.spreadsort_ints(int_jobs.copy(), 0)
    print(f"Sorted by first element: {sorted_int_jobs[:3]}...")
    
    # Test float sorting
    float_jobs = [(random.random() * 100, random.random() * 100, random.random()) for _ in range(10)]
    print(f"Original float jobs: {float_jobs[:3]}...")
    
    sorted_float_jobs = boost_spreadsort.spreadsort_floats(float_jobs.copy(), 0)
    print(f"Sorted by first element: {sorted_float_jobs[:3]}...")
    
    print("✓ All tests passed!")
    
except ImportError as e:
    print(f"✗ Failed to import boost_spreadsort: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error during testing: {e}")
    sys.exit(1) 