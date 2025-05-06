# Linear-Time Weighted Job Scheduling with Integer Times via Multi-Phase Preprocessing

This repository contains the implementation and benchmarking code for my original linear-time algorithm for solving the classic Weighted Interval Scheduling (WIS) or Weighted Job Scheduling problem over bounded integer time domains, as described in my research paper:

**Title**: Linear-Time Weighted Job Scheduling over Integer Time Domains via Multi-Phase Preprocessing
**Author**: Amit Joshi  
**Email(s)**:  
- amitjoshi2724@gmail.com  
- amit.joshiusa@gmail.com  
**GitHub**: [@amitjoshi24](https://github.com/amitjoshi24)

---

## Overview

The classic Weighted Job Scheduling problem is traditionally solved using dynamic programming and binary search with a time complexity of $O(n \log n)$. My solution and this implementation provides a linear-time algorithm, assuming job times are integers within a bounded range. My main contribution is avoiding repeated binary searches with a custom multi-phase preprocessing algorithm. Coupled with linear-time sorting algorithms such as Radix Sort, we can now solve Weighted Job Scheduling in $O(n)$ under very realistic assumptions.

### Files

- `scheduling_algos.py`: Contains both the classical DP algorithm and the linear-time DP version with radix sort and preprocessing.
- `experiment*.py`: Run runtime benchmarks for both the classical and linear-time approaches, across varying input sizes.
- `LICENSE`: Apache License 2.0 declaration.
- `Figure_1.png`: Example output showing empirical runtime comparison.
- `preprint.pdf`: Preprint submitted to arXiv
- `publication.pdf`: Final paper accepted to IPL

---

## Usage

To benchmark the algorithms:

```bash
python experiment.py
```

To integrate or use the algorithms independently:

```python
from scheduling_algos import classic_weighted_interval_scheduling, linear_time_weighted_scheduling
```

---

## Notes

- The linear algorithm uses radix sort and a custom $O(n)$ preprocessing routine to locate each job's predecessor, my main contribution.
- The experiments simulate job instances with different distributions: random, long intervals, and Zipf-like.

---

## License

Licensed under the Apache License 2.0. See the `LICENSE` file for details.
