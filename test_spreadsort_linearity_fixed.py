#!/usr/bin/env python3

import boost_spreadsort
import numpy as np
import time
import random
import matplotlib.pyplot as plt
from collections import defaultdict
import gc

def generate_uniform_data(n):
    """Generate uniform random data - ideal for spreadsort"""
    return [(random.uniform(0, 1000), random.uniform(0, 1000), random.uniform(1, 100)) for _ in range(n)]

def generate_normal_data(n):
    """Generate normally distributed data"""
    return [(np.random.normal(500, 100), np.random.normal(500, 100), random.uniform(1, 100)) for _ in range(n)]

def generate_clustered_data(n):
    """Generate clustered data (multiple normal distributions)"""
    data = []
    for _ in range(n):
        cluster = random.choice([0, 1, 2])
        if cluster == 0:
            start = np.random.normal(100, 20)
            end = np.random.normal(200, 20)
        elif cluster == 1:
            start = np.random.normal(500, 20)
            end = np.random.normal(600, 20)
        else:
            start = np.random.normal(900, 20)
            end = np.random.normal(1000, 20)
        data.append((start, end, random.uniform(1, 100)))
    return data

def generate_zipf_data(n):
    """Generate Zipf-distributed data"""
    # Generate Zipf-distributed integers and convert to floats
    zipf_values = np.random.zipf(1.5, n)
    normalized = [(v % 1000) + random.random() for v in zipf_values]
    return [(normalized[i], normalized[i] + random.uniform(1, 100), random.uniform(1, 100)) for i in range(n)]

def test_single_distribution(dist_name, dist_func):
    """Test a single distribution in isolation"""
    
    # Test sizes (logarithmically spaced)
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    
    print(f"Testing {dist_name} distribution:")
    print(f"{'Size':<8} {'Time (ms)':<12} {'Time/n':<12} {'Ratio':<8}")
    print("-" * 45)
    
    results = []
    prev_time_per_n = None
    
    for n in sizes:
        # Force garbage collection before each test
        gc.collect()
        
        # Generate test data
        jobs = dist_func(n)
        
        # Warm up the function with a small test
        if n == 100:
            _ = boost_spreadsort.float_sort_both_with_indices(jobs[:10])
            time.sleep(0.01)  # Brief pause
        
        # Time the spreadsort
        start_time = time.time()
        end_ordered, start_ordered = boost_spreadsort.float_sort_both_with_indices(jobs)
        end_time = time.time()
        
        # Calculate metrics
        total_time_ms = (end_time - start_time) * 1000
        time_per_n = total_time_ms / n
        
        # Calculate ratio to previous size (should be ~1 for linear scaling)
        ratio = time_per_n / prev_time_per_n if prev_time_per_n else 1.0
        
        print(f"{n:<8} {total_time_ms:<12.3f} {time_per_n:<12.6f} {ratio:<8.3f}")
        
        results.append({
            'size': n,
            'time_ms': total_time_ms,
            'time_per_n': time_per_n,
            'ratio': ratio
        })
        
        prev_time_per_n = time_per_n
    
    print()
    return results

def test_spreadsort_complexity():
    """Test spreadsort complexity across different data distributions"""
    
    # Data distributions to test
    distributions = {
        'Uniform': generate_uniform_data,
        'Normal': generate_normal_data,
        'Clustered': generate_clustered_data,
        'Zipf': generate_zipf_data
    }
    
    results = {}
    
    print("=== Boost Spreadsort Linear Time Complexity Test ===")
    print("Testing different data distributions and input sizes...")
    print()
    
    # Test each distribution in isolation
    for dist_name, dist_func in distributions.items():
        # Force garbage collection between distributions
        gc.collect()
        time.sleep(0.1)  # Brief pause between distributions
        
        results[dist_name] = test_single_distribution(dist_name, dist_func)
    
    return results

def analyze_results(results):
    """Analyze the results to check for linear scaling"""
    print("=== Analysis ===")
    print()
    
    for dist_name, data in results.items():
        print(f"{dist_name} Distribution:")
        
        # Calculate average ratio (should be close to 1.0 for linear scaling)
        ratios = [d['ratio'] for d in data[1:]]  # Skip first entry (no previous)
        avg_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)
        
        # Calculate R-squared for linear fit
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        
        # Linear regression
        log_sizes = np.log10(sizes)
        log_times = np.log10(times)
        slope, intercept = np.polyfit(log_sizes, log_times, 1)
        
        # R-squared calculation
        y_pred = slope * log_sizes + intercept
        ss_res = np.sum((log_times - y_pred) ** 2)
        ss_tot = np.sum((log_times - np.mean(log_times)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        print(f"  Average ratio: {avg_ratio:.3f} ± {std_ratio:.3f}")
        print(f"  Slope (log-log): {slope:.3f}")
        print(f"  R-squared: {r_squared:.3f}")
        
        if abs(slope - 1.0) < 0.1 and r_squared > 0.95:
            print(f"  ✓ LINEAR TIME COMPLEXITY CONFIRMED")
        elif abs(slope - 1.0) < 0.2:
            print(f"  ~ NEARLY LINEAR TIME COMPLEXITY")
        else:
            print(f"  ✗ NOT LINEAR TIME COMPLEXITY")
        print()

def plot_results(results):
    """Plot the results to visualize linear scaling"""
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Time vs Size (log-log)
    plt.subplot(2, 2, 1)
    for dist_name, data in results.items():
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        plt.loglog(sizes, times, 'o-', label=dist_name, alpha=0.7)
    
    # Add reference lines for different complexities
    x_ref = np.array([100, 1000000])
    plt.loglog(x_ref, x_ref * 0.001, '--', alpha=0.5, label='O(n) reference')
    plt.loglog(x_ref, x_ref * np.log(x_ref) * 0.0001, '--', alpha=0.5, label='O(n log n) reference')
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (ms)')
    plt.title('Boost Spreadsort: Time vs Input Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Time per element vs Size
    plt.subplot(2, 2, 2)
    for dist_name, data in results.items():
        sizes = [d['size'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        plt.semilogx(sizes, time_per_n, 'o-', label=dist_name, alpha=0.7)
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time per Element (ms)')
    plt.title('Time per Element vs Input Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Ratio analysis
    plt.subplot(2, 2, 3)
    for dist_name, data in results.items():
        sizes = [d['size'] for d in data[1:]]  # Skip first
        ratios = [d['ratio'] for d in data[1:]]
        plt.semilogx(sizes, ratios, 'o-', label=dist_name, alpha=0.7)
    
    plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Linear reference')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time Ratio (current/previous)')
    plt.title('Scaling Ratio Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Distribution comparison
    plt.subplot(2, 2, 4)
    x_pos = np.arange(len(results))
    avg_ratios = []
    dist_names = []
    
    for dist_name, data in results.items():
        ratios = [d['ratio'] for d in data[1:]]
        avg_ratios.append(np.mean(ratios))
        dist_names.append(dist_name)
    
    bars = plt.bar(x_pos, avg_ratios, alpha=0.7)
    plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Linear reference')
    plt.xlabel('Data Distribution')
    plt.ylabel('Average Scaling Ratio')
    plt.title('Average Scaling by Distribution')
    plt.xticks(x_pos, dist_names, rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('spreadsort_linearity_analysis_fixed.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Run the experiment
    results = test_spreadsort_complexity()
    
    # Analyze the results
    analyze_results(results)
    
    # Plot the results
    try:
        plot_results(results)
        print("Plots saved as 'spreadsort_linearity_analysis_fixed.png'")
    except Exception as e:
        print(f"Could not create plots: {e}")
        print("Results analysis completed successfully.") 