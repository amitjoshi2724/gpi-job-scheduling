#!/usr/bin/env python3

import sys
import os

# Add the build directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'build'))

try:
    from scheduling_algos import gpi_weighted_job_scheduling
    import random
    
    print("✓ Successfully imported scheduling algorithm")
    
    # Create some test jobs
    jobs = [
        (1, 4, 3),   # start, end, weight
        (2, 6, 5),
        (4, 7, 2),
        (6, 8, 4),
        (3, 9, 6)
    ]
    
    print(f"Test jobs: {jobs}")
    
    # Test with different sorting algorithms
    algorithms = ['default', 'spread']
    
    for algo in algorithms:
        try:
            result = gpi_weighted_job_scheduling(jobs, sortAlgo=algo)
            print(f"✓ {algo} algorithm result: {result}")
        except Exception as e:
            print(f"✗ {algo} algorithm failed: {e}")
    
    print("✓ All scheduling tests completed!")
    
except ImportError as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error during testing: {e}")
    sys.exit(1) 