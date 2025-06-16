import numpy as np
from running import run_experiment

def generate_normal_start_jobs(n):
    K = 10**9
    sigma = K / 10
    # Truncated normal start times in [0, K]
    start_times = np.clip(np.random.normal(loc=K/2, scale=sigma, size=n), 0, K)
    durations = np.random.uniform(1.0, 1000.0, size=n)
    end_times = start_times + durations
    weights = np.random.randint(1, 101, size=n)
    jobs = list(zip(start_times, end_times, weights))
    return jobs

run_experiment(
    exp_title="Normally Distributed Start Times",
    gpi_linear_sort = "recursive bucket",
    gpi_linear_sort_label="(Recursive Bucket Sort)",
    job_generator=generate_normal_start_jobs
)