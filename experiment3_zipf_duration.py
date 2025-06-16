import numpy as np
from running import run_experiment

def generate_zipf_duration_with_early_start_burst(n):
    K = 10**9  # Upper bound of time domain
    # Clustered start times near 0 using truncated exponential
    scale = K / 10  # Controls clustering tightness; lower = tighter near 0
    start_times = np.random.exponential(scale=scale, size=n)
    start_times = np.clip(start_times, 0, K)  # Ensure within [0, K]

    # Zipf durations, scaled and capped
    raw_zipf = np.random.zipf(a=2.0, size=n)
    durations = np.minimum(100 * raw_zipf, 1e6)
    end_times = start_times + durations

    weights = np.random.randint(1, 101, size=n)
    jobs = list(zip(start_times, end_times, weights))
    return jobs

run_experiment(
    exp_title="Zipf Durations with Early Start Bursts",
    gpi_linear_sort = "recursive bucket",
    gpi_linear_sort_label="(Recursive Bucket Sort)",
    job_generator=generate_zipf_duration_with_early_start_burst
)


