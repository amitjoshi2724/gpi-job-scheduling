import numpy as np
from running import run_experiment

def generate_bucket_uniform_jobs(n):
    K = 10**9  # Large time domain
    # Uniform start times over [0, K]
    start_times = np.random.uniform(0, K, size=n)

    # Uniform float durations
    durations = np.random.uniform(1.0, 10**6, size=n)
    end_times = start_times + durations

    weights = np.random.randint(1, 101, size=n)
    jobs = list(zip(start_times, end_times, weights))
    return jobs

run_experiment(
    exp_title="Bucket-Sort-Friendly Uniform Start Times",
    gpi_linear_sort = "bucket",
    gpi_linear_sort_label="(Bucket Sort)",
    job_generator=generate_bucket_uniform_jobs
)




