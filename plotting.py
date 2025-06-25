import matplotlib.pyplot as plt
import os

def make_plots(EXP_TITLE, GPI_SORT, results_classic, results_gpi_tim, results_gpi_linear):
    # Create figures directory if it doesn't exist
    figures_dir = "figures"
    if not os.path.exists(figures_dir):
        os.makedirs(figures_dir)
    
    ns_classic, times_classic = zip(*results_classic)
    ns_tim, times_tim = zip(*results_gpi_tim)
    ns_linear, times_linear = zip(*results_gpi_linear)

    ns = ns_classic  # assumed same across all

    per_job_classic = [t / n for t, n in zip(times_classic, ns)]
    per_job_tim = [t / n for t, n in zip(times_tim, ns)]
    per_job_linear = [t / n for t, n in zip(times_linear, ns)]
    MARKER_SIZE = 4
    # Total Runtime Plot
    plt.figure(figsize=(9,5))
    plt.plot(ns_classic, times_classic, marker='o', markersize=MARKER_SIZE, label='Classical')
    plt.plot(ns_linear, times_linear, marker='^', markersize=MARKER_SIZE, label=f'GPI Linear {GPI_SORT}')
    plt.plot(ns_tim, times_tim, marker='s', markersize=MARKER_SIZE, label='GPI (Timsort)')

    plt.xlabel('Number of Jobs (n)', fontsize=12)
    plt.ylabel('Average Runtime (s)', fontsize=12)
    plt.title('Overall Runtime Comparison: ' + EXP_TITLE)
    plt.legend(fontsize=12, markerscale=1.5)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, EXP_TITLE.replace(' ', '_') + "_runtime_total.pdf"))

    # Per-Job Runtime Plot
    plt.figure(figsize=(9,5))
    plt.plot(ns, per_job_classic, marker='o', markersize=MARKER_SIZE, label='Classical per job')
    plt.plot(ns, per_job_linear, marker='^', markersize=MARKER_SIZE, label=f'GPI Linear per job {GPI_SORT}')
    plt.plot(ns, per_job_tim, marker='s', markersize=MARKER_SIZE, label='GPI per job (Timsort)')
    plt.xlabel('Number of Jobs (n)', fontsize=12)
    plt.ylabel('Average Runtime per Job (s)', fontsize=12)
    plt.title('Per-Job Runtime Comparison: ' + EXP_TITLE)
    plt.legend(fontsize=12, markerscale=1.5)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, EXP_TITLE.replace(' ', '_') + "_runtime_per_job.pdf"))

    # Comment out line below if you don't want to see plots
    #plt.show()
