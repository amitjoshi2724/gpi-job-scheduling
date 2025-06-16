import time
import gc
import numpy as np
import matplotlib.pyplot as plt
import random
from scheduling_algos import classic_weighted_interval_scheduling, gpi_weighted_job_scheduling
from plotting import make_plots


def run_experiment(exp_title, gpi_linear_sort, gpi_linear_sort_label, job_generator, trials=10, n_start=1000, n_end=100000, n_step=1000):
    RANDOM_SEED = 2724
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    results_classic = []
    results_gpi_linear = []
    results_gpi_tim = []

    for n in range(n_start, n_end+1, n_step):
        total_classic = 0
        total_gpi_tim = 0
        total_gpi_linear = 0
        trials = 10
        MAX_VAL = 10**6
        for _ in range(trials):
            jobs = job_generator(n)
            # Classic
            gc.enable(); gc.collect(); gc.disable()
            start = time.perf_counter()
            classicAnswer = classic_weighted_interval_scheduling(jobs, sortAlgo="default") # as opposed to "default"
            end = time.perf_counter()
            total_classic += (end - start)

            # GPI Timsort
            gc.enable(); gc.collect(); gc.disable()
            start = time.perf_counter()
            gpiTimAnswer = gpi_weighted_job_scheduling(jobs, sortAlgo="default")
            end = time.perf_counter()
            total_gpi_tim += (end - start)

            # GPI Linear Sort
            gc.enable(); gc.collect(); gc.disable()
            start = time.perf_counter()
            gpiLinearAnswer = gpi_weighted_job_scheduling(jobs, sortAlgo=gpi_linear_sort)
            end = time.perf_counter()
            total_gpi_linear += (end - start)

            if not (classicAnswer == gpiTimAnswer == gpiLinearAnswer):
                print ('INCORRECT ANSWER', classicAnswer, gpiTimAnswer, gpiLinearAnswer)
                exit()

        avg_classic = total_classic / trials
        avg_gpi_tim = total_gpi_tim / trials
        avg_gpi_linear = total_gpi_linear / trials
        results_classic.append((n, avg_classic))
        results_gpi_tim.append((n, avg_gpi_tim))
        results_gpi_linear.append((n, avg_gpi_linear))
        print(f"n = {n}, classic = {avg_classic:.6f} s, gpi_tim = {avg_gpi_tim:.6f} s, gpi_linear={avg_gpi_linear:.6f} s")
    make_plots(exp_title, gpi_linear_sort_label, results_classic, results_gpi_tim, results_gpi_linear)
