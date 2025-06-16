import matplotlib.pyplot as plt

def make_plots(EXP_TITLE, GPI_SORT, results_classic, results_gpi_tim, results_gpi_linear):
    ns_classic, times_classic = zip(*results_classic)
    ns_tim, times_tim = zip(*results_gpi_tim)
    ns_linear, times_linear = zip(*results_gpi_linear)

    ns = ns_classic  # assumed same across all

    per_job_classic = [t / n for t, n in zip(times_classic, ns)]
    per_job_tim = [t / n for t, n in zip(times_tim, ns)]
    per_job_linear = [t / n for t, n in zip(times_linear, ns)]

    # Total Runtime Plot
    plt.figure(figsize=(10, 5))
    plt.plot(ns_classic, times_classic, marker='o', label='Classical DP')
    plt.plot(ns_tim, times_tim, marker='s', label='GPI DP (Timsort)')
    plt.plot(ns_linear, times_linear, marker='^', label=f'GPI DP {GPI_SORT}')
    plt.xlabel('Number of Jobs (n)')
    plt.ylabel('Average Runtime (s)')
    plt.title('Overall Runtime Comparison: ' + EXP_TITLE)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(EXP_TITLE.replace(' ', '_') + "_runtime_total.pdf")

    # Per-Job Runtime Plot
    plt.figure(figsize=(10, 5))
    plt.plot(ns, per_job_classic, marker='o', label='Classical DP per job')
    plt.plot(ns, per_job_tim, marker='s', label='GPI DP per job (Timsort)')
    plt.plot(ns, per_job_linear, marker='^', label=f'GPI DP per job {GPI_SORT}')
    plt.xlabel('Number of Jobs (n)')
    plt.ylabel('Average Runtime per Job (s)')
    plt.title('Per-Job Runtime Comparison: ' + EXP_TITLE)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(EXP_TITLE.replace(' ', '_') + "_runtime_per_job.pdf")

    plt.show()
