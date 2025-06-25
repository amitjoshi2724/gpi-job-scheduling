import random
from running import run_experiment

def generate_random_integer_jobs(n):
    MAX_VAL = 10**6
    jobs = [(random.randint(0, MAX_VAL), random.randint(0, MAX_VAL), random.randint(1, 100)) for _ in range(n)]
    jobs = [(min(s, e), max(s, e), w) for s, e, w in jobs]
    return jobs

run_experiment(
    exp_title="Random Integer Times",
    gpi_linear_sort = "radix",
    gpi_linear_sort_label="(Radix Sort)",
    n_step=1000,
    job_generator=generate_random_integer_jobs
)




