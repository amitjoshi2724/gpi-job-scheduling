import boost_spreadsort
import numpy as np

# Simple test
print("Testing basic functions...")

# Test 1: Basic float_sort
vals = [3.14, 1.41, 2.71, 0.58]
result = boost_spreadsort.float_sort_doubles(vals)
print("float_sort_doubles:", result)

# Test 2: Simple tuple sort
jobs = [(1.0, 3.0, 10), (2.0, 4.0, 20), (0.5, 2.5, 15)]
print("Original jobs:", jobs)

try:
    result = boost_spreadsort.float_sort_tuples_by_key(jobs, 0)
    print("float_sort_tuples_by_key (by start):", result)
except Exception as e:
    print("Error in float_sort_tuples_by_key:", e)

try:
    result = boost_spreadsort.float_sort_tuples_by_key(jobs, 1)
    print("float_sort_tuples_by_key (by end):", result)
except Exception as e:
    print("Error in float_sort_tuples_by_key:", e)

# Test 3: Optimized function
try:
    end_ordered, start_ordered = boost_spreadsort.gpi_linear_optimized(jobs)
    print("gpi_linear_optimized - end_ordered:", end_ordered)
    print("gpi_linear_optimized - start_ordered:", start_ordered)
except Exception as e:
    print("Error in gpi_linear_optimized:", e)

print("Debug test completed.") 