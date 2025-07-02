# Global Predecessor Indexing: Avoiding Binary Search in Weighted Job Scheduling

This repository contains the implementation and benchmarking code for my original (Global Predecessor Indexing) for solving the classic Weighted Interval Scheduling (WIS) or Weighted Job Scheduling (WJS) problem without Binary Search. Over time domains distributions that admit linear sorting, this results in a linear-time solution as described in my research paper:
<https://arxiv.org/abs/2506.22922>


**Title**: Global Predecessor Indexing: Avoiding Binary Search in Weighted Job Scheduling
**Author**: Amit Joshi  
**Email(s)**:  
- amitjoshi2724@gmail.com  
- amit.joshiusa@gmail.com  
**GitHub**: [@amitjoshi2724](https://github.com/amitjoshi2724)

---

## Overview

The classic Weighted Job Scheduling problem is traditionally solved using dynamic programming and binary search with a time complexity of $O(n \log(n))$. My solution and this implementation provides a linear-time algorithm, assuming job times can be sorted in linear time (such as if they are bounded integers (Radix Sort) or come from an approximately uniform distribution (Bucket Sort) or are even non-uniform (Spreadsort achieves $O(n)$ average case). Even if they can't be sorted in linear time, and only comparison-based sorting is available, my algorithm provides significant practical speedups (2-3x for 100k jobs) over the classical approach. My main contribution is avoiding repeated binary searches with a custom multi-phase preprocessing algorithm. Coupled with linear-time sorting algorithms, we can now solve Weighted Job Scheduling in $O(n)$ under very realistic assumptions.

### Files

- `scheduling_algos.py`: Contains both the classical DP algorithm and the linear-time DP version with radix sort and preprocessing.
- `experiment*.py`: Run runtime benchmarks for both the classical and linear-time approaches, across varying input sizes.
- `running.py`: Runs experiments in a controlled environment with multiple trials and measures time for solving instances
- `plotting.py`: Code for plotting the overall runtime and the per-job runtime for experiments to visualize scaling trends of GPI.
- `spreadsort.cpp`: C++ code for Spreadsort on Job Tuples, to be used in Python via Pybind
- `boost_spreadsort.cpython-313-darwin.so`: Compiled version of `spreadsort.cpp`
- `run_experiments.sh`: shell script to run all experiments
- `LICENSE`: Apache License 2.0 declaration.
- `preprint.pdf`: Preprint submitted to arXiv
- `main.tex`: Latex of the preprint
- `references.bib`: Bibliography
- `publication.pdf`: Final paper accepted to IPL

---

## Usage

### API Reference

#### `classical_weighted_interval_scheduling(jobs, sortAlgo='default')`

The classical dynamic programming solution for Weighted Interval Scheduling with O(n log n) time complexity.

**Parameters:**
- `jobs` (List[Tuple[int, int, int]]): List of job tuples where each job is (start_time, end_time, weight)
- `sortAlgo` (str, optional): Sorting algorithm to use. Options:
  - `'default'`: Python's built-in Timsort (comparison-based)
  - `'radix'`: Radix sort for bounded integer times

**Returns:**
- `int`: Maximum total weight achievable by selecting non-overlapping jobs

**Example:**
```python
from scheduling_algos import classical_weighted_interval_scheduling

# Define jobs as (start_time, end_time, weight) tuples
jobs = [
    (1, 4, 3),   # Job 1: starts at 1, ends at 4, weight 3
    (2, 6, 5),   # Job 2: starts at 2, ends at 6, weight 5
    (4, 7, 2),   # Job 3: starts at 4, ends at 7, weight 2
    (6, 8, 4)    # Job 4: starts at 6, ends at 8, weight 4
]

# Solve using classical algorithm
max_weight = classical_weighted_interval_scheduling(jobs)
print(f"Maximum weight: {max_weight}")  # Output: Maximum weight: 7
```

#### `gpi_weighted_job_scheduling(jobs, sortAlgo='default')`

The linear-time Global Predecessor Indexing solution for Weighted Job Scheduling.

**Parameters:**
- `jobs` (List[Tuple[int, int, int]]): List of job tuples where each job is (start_time, end_time, weight)
- `sortAlgo` (str, optional): Sorting algorithm to use. Options:
  - `'default'`: Python's built-in Timsort (comparison-based)
  - `'radix'`: Radix sort for bounded integer times
  - `'bucket'`: Bucket sort for approximately uniform distributions
  - `'recursive bucket'`: Adaptive recursive bucket sort
  - `'spread'`: Spreadsort (requires compiled C++ extension)

**Returns:**
- `int`: Maximum total weight achievable by selecting non-overlapping jobs

**Example:**
```python
from scheduling_algos import gpi_weighted_job_scheduling

# Define jobs as (start_time, end_time, weight) tuples
jobs = [
    (1, 4, 3),   # Job 1: starts at 1, ends at 4, weight 3
    (2, 6, 5),   # Job 2: starts at 2, ends at 6, weight 5
    (4, 7, 2),   # Job 3: starts at 4, ends at 7, weight 2
    (6, 8, 4)    # Job 4: starts at 6, ends at 8, weight 4
]

# Solve using GPI algorithm with different sorting options
max_weight_default = gpi_weighted_job_scheduling(jobs)
max_weight_radix = gpi_weighted_job_scheduling(jobs, sortAlgo='radix')
max_weight_bucket = gpi_weighted_job_scheduling(jobs, sortAlgo='bucket')

print(f"Maximum weight (default): {max_weight_default}")    # Output: Maximum weight: 7
print(f"Maximum weight (radix): {max_weight_radix}")        # Output: Maximum weight: 7
print(f"Maximum weight (bucket): {max_weight_bucket}")      # Output: Maximum weight: 7
```

### Input Format

Jobs should be provided as a list of tuples, where each tuple contains:
- **start_time** (int): When the job begins
- **end_time** (int): When the job ends (must be > start_time)
- **weight** (int): The value/weight of the job

### Algorithm Selection Guide

Choose the sorting algorithm based on your data characteristics:

- **`'default'`**: Use for general-purpose scenarios or when unsure
- **`'radix'`**: Use when job times are bounded integers (e.g., 0-1000)
- **`'bucket'`**: Use when job times follow approximately uniform distribution
- **`'recursive bucket'`**: Use for non-uniform distributions that benefit from adaptive bucketing
- **`'spread'`**: Use for best performance with the compiled C++ extension, has Python-C++ conversion overhead

### Benchmarking

To run performance benchmarks:

```bash
# Run specific experiment
python experiment1_random_intervals.py
python experiment2_normal_start_times.py
python experiment3_zipf_duration.py
python experiment4_uniform_bucket_ideal.py

# Run all experiments
./run_experiments.sh
```

### Integration Example

```python
from scheduling_algos import classical_weighted_interval_scheduling, gpi_weighted_job_scheduling
import numpy as np

# Generate random job data
np.random.seed(42)
n_jobs = 1000
start_times = np.random.randint(0, 1000, n_jobs)
durations = np.random.randint(1, 100, n_jobs)
end_times = start_times + durations
weights = np.random.randint(1, 50, n_jobs)

jobs = list(zip(start_times, end_times, weights))

# Compare both algorithms
classical_result = classical_weighted_interval_scheduling(jobs)
gpi_result = gpi_weighted_job_scheduling(jobs, sortAlgo='radix')

print(f"Classical algorithm result: {classical_result}")
print(f"GPI algorithm result: {gpi_result}")
assert classical_result == gpi_result, "Results should be identical"
```

---

## Notes

- GPI WJS uses your desired sort and a custom $O(n)$ preprocessing routine to locate each job's predecessor, my main contribution.
- The experiments simulate job instances with different distributions: random integer start/end times, normal start times, Zipf-like early-burst, and uniform start/end times.

---

## License

Licensed under the Apache License 2.0. See the `LICENSE` file for details.
