#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import time
import gc
import random
from scheduling_algos import gpi_weighted_job_scheduling
from collections import defaultdict

def generate_random_integer_jobs(n):
    """Experiment 1: Random Integer Times with Radix Sort"""
    MAX_VAL = 10**6
    jobs = [(random.randint(0, MAX_VAL), random.randint(0, MAX_VAL), random.randint(1, 100)) for _ in range(n)]
    jobs = [(min(s, e), max(s, e), w) for s, e, w in jobs]
    return jobs

def generate_normal_start_jobs(n):
    """Experiment 2: Normally Distributed Start Times with Spreadsort"""
    K = 10**9
    sigma = K / 10
    start_times = np.clip(np.random.normal(loc=K/2, scale=sigma, size=n), 0, K)
    durations = np.random.uniform(1.0, 10**6, size=n)
    end_times = start_times + durations
    weights = np.random.randint(1, 101, size=n)
    jobs = list(zip(start_times, end_times, weights))
    return jobs

def generate_zipf_duration_with_early_start_burst(n):
    """Experiment 3: Zipf Durations with Early Start Bursts with Spreadsort"""
    K = 10**9
    scale = K / 10
    start_times = np.random.exponential(scale=scale, size=n)
    start_times = np.clip(start_times, 0, K)
    
    raw_zipf = np.random.zipf(a=2.0, size=n)
    durations = np.minimum(100 * raw_zipf, 10**6)
    end_times = start_times + durations
    
    weights = np.random.randint(1, 101, size=n)
    jobs = list(zip(start_times, end_times, weights))
    return jobs

def generate_bucket_uniform_jobs(n):
    """Experiment 4: Bucket-Sort-Friendly Uniform Start Times with Bucket Sort"""
    K = 10**9
    start_times = np.random.uniform(0, K, size=n)
    durations = np.random.uniform(1.0, 10**6, size=n)
    end_times = start_times + durations
    weights = np.random.randint(1, 101, size=n)
    jobs = list(zip(start_times, end_times, weights))
    return jobs

def collect_gpi_linear_data():
    """Collect runtime data for gpi_linear from all 4 experiments"""
    
    # Set random seed for reproducibility
    RANDOM_SEED = 2724
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    # Test sizes (same as original experiments)
    sizes = list(range(1000, 100001, 1000))
    
    # Experiment configurations
    experiments = {
        'Random Integer (Radix)': {
            'generator': generate_random_integer_jobs,
            'sort_algo': 'default'
        },
        'Normal Start Times (Spreadsort)': {
            'generator': generate_normal_start_jobs,
            'sort_algo': 'default'
        },
        'Zipf Durations (Spreadsort)': {
            'generator': generate_zipf_duration_with_early_start_burst,
            'sort_algo': 'default'
        },
        'Uniform Bucket (Bucket Sort)': {
            'generator': generate_bucket_uniform_jobs,
            'sort_algo': 'default'
        }
    }
    
    results = {}
    
    print("=== Collecting gpi_linear Runtime Data ===")
    print("Testing all 4 experiments with gpi_linear algorithm...")
    print()
    
    for exp_name, config in experiments.items():
        print(f"Testing {exp_name}:")
        print(f"{'Size':<8} {'Time (ms)':<12} {'Time/n':<12} {'Ratio':<8}")
        print("-" * 45)
        
        exp_results = []
        prev_time_per_n = None
        
        for n in sizes:
            # Force garbage collection
            gc.collect()
            
            # Generate test data
            jobs = config['generator'](n)
            
            # Time gpi_linear
            start_time = time.perf_counter()
            _ = gpi_weighted_job_scheduling(jobs, sortAlgo=config['sort_algo'])
            end_time = time.perf_counter()
            
            # Calculate metrics
            total_time_ms = (end_time - start_time) * 1000
            time_per_n = total_time_ms / n
            
            # Calculate ratio to previous size (should be ~1 for linear scaling)
            ratio = time_per_n / prev_time_per_n if prev_time_per_n else 1.0
            
            print(f"{n:<8} {total_time_ms:<12.3f} {time_per_n:<12.6f} {ratio:<8.3f}")
            
            exp_results.append({
                'size': n,
                'time_ms': total_time_ms,
                'time_per_n': time_per_n,
                'ratio': ratio
            })
            
            prev_time_per_n = time_per_n
        
        results[exp_name] = exp_results
        print()
    
    return results

def analyze_gpi_linear_complexity(results):
    """Analyze the results to check for linear scaling"""
    print("=== gpi_linear Complexity Analysis ===")
    print()
    
    for exp_name, data in results.items():
        print(f"{exp_name}:")
        
        # Calculate average ratio (should be close to 1.0 for linear scaling)
        ratios = [d['ratio'] for d in data[1:]]  # Skip first entry (no previous)
        avg_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)
        
        # Calculate R-squared for linear fit
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        
        # Linear regression on log-log plot
        log_sizes = np.log10(sizes)
        log_times = np.log10(times)
        slope, intercept = np.polyfit(log_sizes, log_times, 1)
        
        # R-squared calculation
        y_pred = slope * log_sizes + intercept
        ss_res = np.sum((log_times - y_pred) ** 2)
        ss_tot = np.sum((log_times - np.mean(log_times)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Calculate average time per element
        avg_time_per_n = np.mean([d['time_per_n'] for d in data])
        
        print(f"  Average ratio: {avg_ratio:.3f} ± {std_ratio:.3f}")
        print(f"  Slope (log-log): {slope:.3f}")
        print(f"  R-squared: {r_squared:.3f}")
        print(f"  Avg time per element: {avg_time_per_n:.6f} ms")
        
        if abs(slope - 1.0) < 0.1 and r_squared > 0.95:
            print(f"  ✓ LINEAR TIME COMPLEXITY CONFIRMED")
        elif abs(slope - 1.0) < 0.2:
            print(f"  ~ NEARLY LINEAR TIME COMPLEXITY")
        else:
            print(f"  ✗ NOT LINEAR TIME COMPLEXITY")
        print()

def plot_gpi_linear_analysis(results):
    """Plot the results to visualize linear scaling"""
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Time vs Size (log-log)
    plt.subplot(2, 2, 1)
    for exp_name, data in results.items():
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        plt.loglog(sizes, times, 'o-', label=exp_name, alpha=0.7, markersize=3)
    
    # Add reference lines for different complexities
    x_ref = np.array([1000, 100000])
    plt.loglog(x_ref, x_ref * 0.001, '--', alpha=0.5, label='O(n) reference')
    plt.loglog(x_ref, x_ref * np.log(x_ref) * 0.0001, '--', alpha=0.5, label='O(n log n) reference')
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (ms)')
    plt.title('gpi_linear: Time vs Input Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Time per element vs Size
    plt.subplot(2, 2, 2)
    for exp_name, data in results.items():
        sizes = [d['size'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        plt.semilogx(sizes, time_per_n, 'o-', label=exp_name, alpha=0.7, markersize=3)
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time per Element (ms)')
    plt.title('gpi_linear: Time per Element vs Input Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Ratio analysis
    plt.subplot(2, 2, 3)
    for exp_name, data in results.items():
        sizes = [d['size'] for d in data[1:]]  # Skip first
        ratios = [d['ratio'] for d in data[1:]]
        plt.semilogx(sizes, ratios, 'o-', label=exp_name, alpha=0.7, markersize=3)
    
    plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Linear reference')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time Ratio (current/previous)')
    plt.title('gpi_linear: Scaling Ratio Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Distribution comparison
    plt.subplot(2, 2, 4)
    x_pos = np.arange(len(results))
    avg_ratios = []
    exp_names = []
    
    for exp_name, data in results.items():
        ratios = [d['ratio'] for d in data[1:]]
        avg_ratios.append(np.mean(ratios))
        exp_names.append(exp_name)
    
    bars = plt.bar(x_pos, avg_ratios, alpha=0.7)
    plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Linear reference')
    plt.xlabel('Experiment')
    plt.ylabel('Average Scaling Ratio')
    plt.title('gpi_linear: Average Scaling by Experiment')
    plt.xticks(x_pos, [name.split('(')[0].strip() for name in exp_names], rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('gpi_linear_complexity_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def summary_statistics(results):
    """Provide summary statistics for all experiments"""
    print("=== Summary Statistics ===")
    print()
    
    all_slopes = []
    all_r_squared = []
    all_avg_ratios = []
    
    for exp_name, data in results.items():
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        
        # Linear regression
        log_sizes = np.log10(sizes)
        log_times = np.log10(times)
        slope, _ = np.polyfit(log_sizes, log_times, 1)
        
        # R-squared
        y_pred = slope * log_sizes + np.polyfit(log_sizes, log_times, 1)[1]
        ss_res = np.sum((log_times - y_pred) ** 2)
        ss_tot = np.sum((log_times - np.mean(log_times)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Average ratio
        ratios = [d['ratio'] for d in data[1:]]
        avg_ratio = np.mean(ratios)
        
        all_slopes.append(slope)
        all_r_squared.append(r_squared)
        all_avg_ratios.append(avg_ratio)
    
    print(f"Average slope across all experiments: {np.mean(all_slopes):.3f} ± {np.std(all_slopes):.3f}")
    print(f"Average R-squared across all experiments: {np.mean(all_r_squared):.3f} ± {np.std(all_r_squared):.3f}")
    print(f"Average scaling ratio across all experiments: {np.mean(all_avg_ratios):.3f} ± {np.std(all_avg_ratios):.3f}")
    
    # Check if all experiments show linear complexity
    linear_count = sum(1 for slope in all_slopes if abs(slope - 1.0) < 0.1)
    print(f"Experiments showing linear complexity: {linear_count}/{len(all_slopes)}")
    
    if linear_count == len(all_slopes):
        print("🎉 ALL EXPERIMENTS CONFIRM LINEAR TIME COMPLEXITY!")
    else:
        print("⚠️  Some experiments may not show linear complexity")

if __name__ == "__main__":
    # Collect runtime data
    results = collect_gpi_linear_data()
    
    # Analyze the results
    analyze_gpi_linear_complexity(results)
    
    # Summary statistics
    summary_statistics(results)
    
    # Plot the results
    try:
        plot_gpi_linear_analysis(results)
        print("\nPlots saved as 'gpi_linear_complexity_analysis.png'")
    except Exception as e:
        print(f"\nCould not create plots: {e}")
        print("Results analysis completed successfully.") 