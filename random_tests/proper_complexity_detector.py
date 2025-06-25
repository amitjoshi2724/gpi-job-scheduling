#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import time
import gc
import random
from scheduling_algos import gpi_weighted_job_scheduling
import math

def generate_test_jobs(n):
    """Generate test jobs for complexity analysis"""
    MAX_VAL = 10**6
    jobs = [(random.randint(0, MAX_VAL), random.randint(0, MAX_VAL), random.randint(1, 100)) for _ in range(n)]
    jobs = [(min(s, e), max(s, e), w) for s, e, w in jobs]
    return jobs

def test_with_larger_range():
    """Test with much larger input ranges to see the difference"""
    
    # Set random seed for reproducibility
    RANDOM_SEED = 2724
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    # Much larger test sizes - this is where we'll see the difference
    sizes = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    
    # Test both algorithms
    algorithms = {
        'Linear (Radix)': 'radix',
        'O(n log n) (Timsort)': 'default'
    }
    
    results = {}
    
    print("=== PROPER COMPLEXITY DETECTION ===")
    print("Testing with larger ranges to see the real difference...")
    print()
    
    for algo_name, sort_algo in algorithms.items():
        print(f"Testing {algo_name}:")
        print(f"{'Size':<10} {'Time (ms)':<12} {'Time/n':<15} {'Log(n)':<10} {'Ratio':<10}")
        print("-" * 70)
        
        algo_results = []
        prev_time_per_n = None
        
        for n in sizes:
            # Force garbage collection
            gc.collect()
            
            # Generate test data
            jobs = generate_test_jobs(n)
            
            # Time algorithm
            start_time = time.perf_counter()
            _ = gpi_weighted_job_scheduling(jobs, sortAlgo=sort_algo)
            end_time = time.perf_counter()
            
            # Calculate metrics
            total_time_ms = (end_time - start_time) * 1000
            time_per_n = total_time_ms / n
            log_n = math.log(n)
            
            # Calculate ratio to previous size
            ratio = time_per_n / prev_time_per_n if prev_time_per_n else 1.0
            
            print(f"{n:<10} {total_time_ms:<12.3f} {time_per_n:<15.6f} {log_n:<10.3f} {ratio:<10.3f}")
            
            algo_results.append({
                'size': n,
                'time_ms': total_time_ms,
                'time_per_n': time_per_n,
                'ratio': ratio,
                'log_n': log_n
            })
            
            prev_time_per_n = time_per_n
        
        results[algo_name] = algo_results
        print()
    
    return results

def analyze_with_better_metrics(results):
    """Analyze with better metrics to detect complexity"""
    print("=== BETTER COMPLEXITY ANALYSIS ===")
    print()
    
    for algo_name, data in results.items():
        print(f"{algo_name}:")
        
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        log_n_values = [d['log_n'] for d in data]
        
        # Method 1: Log-log regression (current method)
        log_sizes = np.log10(sizes)
        log_times = np.log10(times)
        slope_loglog, _ = np.polyfit(log_sizes, log_times, 1)
        
        # Method 2: Time per n vs log(n) (better method)
        slope_time_per_n, _ = np.polyfit(log_n_values, time_per_n, 1)
        
        # Method 3: Ratio analysis
        ratios = [d['ratio'] for d in data[1:]]
        avg_ratio = np.mean(ratios)
        ratio_trend = np.polyfit(range(len(ratios)), ratios, 1)[0]  # Slope of ratios
        
        # Method 4: Theoretical prediction
        # For O(n): time_per_n should be constant
        # For O(n log n): time_per_n should increase with log(n)
        theoretical_slope = slope_time_per_n
        
        print(f"  Log-log slope: {slope_loglog:.3f}")
        print(f"  Time per n vs log(n) slope: {slope_time_per_n:.6f}")
        print(f"  Average ratio: {avg_ratio:.3f}")
        print(f"  Ratio trend: {ratio_trend:.6f}")
        
        # Improved detection logic
        is_linear = True
        reasons = []
        
        if slope_time_per_n > 0.0001:  # Significant increase with log(n)
            is_linear = False
            reasons.append(f"Time per n increases with log(n) (slope: {slope_time_per_n:.6f})")
        
        if ratio_trend > 0.01:  # Ratios are increasing
            is_linear = False
            reasons.append(f"Ratios are increasing (trend: {ratio_trend:.6f})")
        
        if abs(slope_loglog - 1.0) > 0.05:  # Log-log slope not close to 1
            is_linear = False
            reasons.append(f"Log-log slope not linear ({slope_loglog:.3f})")
        
        # Check if the increase is significant enough
        if len(time_per_n) >= 3:
            first_half = time_per_n[:len(time_per_n)//2]
            second_half = time_per_n[len(time_per_n)//2:]
            increase_factor = np.mean(second_half) / np.mean(first_half)
            
            if increase_factor > 1.5:  # More than 50% increase
                is_linear = False
                reasons.append(f"Significant increase in time per n ({increase_factor:.2f}x)")
        
        if is_linear:
            print(f"  ✅ DETECTED AS LINEAR")
        else:
            print(f"  ❌ DETECTED AS O(n log n)")
            for reason in reasons:
                print(f"    - {reason}")
        
        print()

def test_pure_sorting():
    """Test pure sorting algorithms without Python-C++ overhead"""
    print("=== PURE SORTING COMPLEXITY TEST ===")
    print("Testing pure sorting to isolate algorithmic complexity...")
    print()
    
    # Test sizes
    sizes = [1000, 5000, 10000, 50000, 100000, 500000]
    
    # Pure sorting algorithms
    algorithms = {
        'Python Timsort': lambda arr: sorted(arr),
        'Python Radix (simulated)': lambda arr: sorted(arr, key=lambda x: x[0])  # Sort by first element
    }
    
    results = {}
    
    for algo_name, sort_func in algorithms.items():
        print(f"Testing {algo_name}:")
        print(f"{'Size':<10} {'Time (ms)':<12} {'Time/n':<15} {'Log(n)':<10}")
        print("-" * 55)
        
        algo_results = []
        
        for n in sizes:
            # Generate test data
            data = [(random.randint(0, 10**6), random.randint(0, 10**6), random.randint(1, 100)) for _ in range(n)]
            
            # Time sorting
            start_time = time.perf_counter()
            _ = sort_func(data)
            end_time = time.perf_counter()
            
            # Calculate metrics
            total_time_ms = (end_time - start_time) * 1000
            time_per_n = total_time_ms / n
            log_n = math.log(n)
            
            print(f"{n:<10} {total_time_ms:<12.3f} {time_per_n:<15.6f} {log_n:<10.3f}")
            
            algo_results.append({
                'size': n,
                'time_ms': total_time_ms,
                'time_per_n': time_per_n,
                'log_n': log_n
            })
        
        results[algo_name] = algo_results
        print()
    
    return results

def plot_comprehensive_analysis(results, pure_results=None):
    """Create comprehensive plots showing complexity detection"""
    plt.figure(figsize=(20, 15))
    
    # Plot 1: Time vs Size (log-log) - Main algorithms
    plt.subplot(3, 4, 1)
    for algo_name, data in results.items():
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        plt.loglog(sizes, times, 'o-', label=algo_name, alpha=0.7, markersize=6)
    
    # Add reference lines
    x_ref = np.array([1000, 1000000])
    plt.loglog(x_ref, x_ref * 0.001, '--', alpha=0.5, label='O(n) reference')
    plt.loglog(x_ref, x_ref * np.log(x_ref) * 0.0001, '--', alpha=0.5, label='O(n log n) reference')
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (ms)')
    plt.title('Time vs Input Size (Log-Log)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Time per element vs Size
    plt.subplot(3, 4, 2)
    for algo_name, data in results.items():
        sizes = [d['size'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        plt.semilogx(sizes, time_per_n, 'o-', label=algo_name, alpha=0.7, markersize=6)
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time per Element (ms)')
    plt.title('Time per Element vs Input Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Time per element vs log(n)
    plt.subplot(3, 4, 3)
    for algo_name, data in results.items():
        log_n = [d['log_n'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        plt.plot(log_n, time_per_n, 'o-', label=algo_name, alpha=0.7, markersize=6)
    
    plt.xlabel('log(n)')
    plt.ylabel('Time per Element (ms)')
    plt.title('Time per Element vs log(n)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Ratio analysis
    plt.subplot(3, 4, 4)
    for algo_name, data in results.items():
        sizes = [d['size'] for d in data[1:]]
        ratios = [d['ratio'] for d in data[1:]]
        plt.semilogx(sizes, ratios, 'o-', label=algo_name, alpha=0.7, markersize=6)
    
    plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Linear reference')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time Ratio (current/previous)')
    plt.title('Scaling Ratio Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 5: Pure sorting comparison (if available)
    if pure_results:
        plt.subplot(3, 4, 5)
        for algo_name, data in pure_results.items():
            sizes = [d['size'] for d in data]
            times = [d['time_ms'] for d in data]
            plt.loglog(sizes, times, 'o-', label=algo_name, alpha=0.7, markersize=6)
        
        plt.xlabel('Input Size (n)')
        plt.ylabel('Time (ms)')
        plt.title('Pure Sorting: Time vs Input Size')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 6: Pure sorting time per element
        plt.subplot(3, 4, 6)
        for algo_name, data in pure_results.items():
            log_n = [d['log_n'] for d in data]
            time_per_n = [d['time_per_n'] for d in data]
            plt.plot(log_n, time_per_n, 'o-', label=algo_name, alpha=0.7, markersize=6)
        
        plt.xlabel('log(n)')
        plt.ylabel('Time per Element (ms)')
        plt.title('Pure Sorting: Time per Element vs log(n)')
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    # Plot 7: Complexity detection summary
    plt.subplot(3, 4, 7)
    algo_names = []
    slopes = []
    colors = []
    
    for algo_name, data in results.items():
        log_n = [d['log_n'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        slope, _ = np.polyfit(log_n, time_per_n, 1)
        
        algo_names.append(algo_name.split('(')[0].strip())
        slopes.append(slope * 1000)  # Convert to μs for readability
        colors.append('green' if 'Linear' in algo_name else 'red')
    
    bars = plt.bar(range(len(algo_names)), slopes, color=colors, alpha=0.7)
    plt.xlabel('Algorithm')
    plt.ylabel('Slope (μs per log(n))')
    plt.title('Complexity Detection: Time per n vs log(n)')
    plt.xticks(range(len(algo_names)), algo_names, rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    
    # Plot 8: Theoretical vs Actual
    plt.subplot(3, 4, 8)
    for algo_name, data in results.items():
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        
        if 'Linear' in algo_name:
            plt.loglog(sizes, times, 'o-', label=f'{algo_name} (actual)', alpha=0.7, markersize=6)
            plt.loglog(sizes, np.array(sizes) * 0.001, '--', label=f'{algo_name} (theoretical O(n))', alpha=0.5)
        else:
            plt.loglog(sizes, times, 's-', label=f'{algo_name} (actual)', alpha=0.7, markersize=6)
            plt.loglog(sizes, np.array(sizes) * np.log(np.array(sizes)) * 0.0001, '--', label=f'{algo_name} (theoretical O(n log n))', alpha=0.5)
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (ms)')
    plt.title('Theoretical vs Actual Performance')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 9: Increase factor analysis
    plt.subplot(3, 4, 9)
    algo_names = []
    increase_factors = []
    
    for algo_name, data in results.items():
        time_per_n = [d['time_per_n'] for d in data]
        if len(time_per_n) >= 3:
            first_half = time_per_n[:len(time_per_n)//2]
            second_half = time_per_n[len(time_per_n)//2:]
            increase_factor = np.mean(second_half) / np.mean(first_half)
            
            algo_names.append(algo_name.split('(')[0].strip())
            increase_factors.append(increase_factor)
    
    bars = plt.bar(range(len(algo_names)), increase_factors, alpha=0.7)
    plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='No increase')
    plt.xlabel('Algorithm')
    plt.ylabel('Increase Factor')
    plt.title('Time per Element Increase Factor')
    plt.xticks(range(len(algo_names)), algo_names, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 10: Ratio trend analysis
    plt.subplot(3, 4, 10)
    algo_names = []
    ratio_trends = []
    
    for algo_name, data in results.items():
        ratios = [d['ratio'] for d in data[1:]]
        if len(ratios) > 1:
            trend = np.polyfit(range(len(ratios)), ratios, 1)[0]
            
            algo_names.append(algo_name.split('(')[0].strip())
            ratio_trends.append(trend)
    
    bars = plt.bar(range(len(algo_names)), ratio_trends, alpha=0.7)
    plt.axhline(y=0.0, color='red', linestyle='--', alpha=0.7, label='No trend')
    plt.xlabel('Algorithm')
    plt.ylabel('Ratio Trend')
    plt.title('Ratio Trend Analysis')
    plt.xticks(range(len(algo_names)), algo_names, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('proper_complexity_detection.png', dpi=300, bbox_inches='tight')
    plt.show()

def final_verdict(results):
    """Give final verdict on algorithm complexities"""
    print("=== FINAL COMPLEXITY VERDICT ===")
    print()
    
    for algo_name, data in results.items():
        print(f"{algo_name}:")
        
        # Collect all evidence
        evidence = []
        
        # Evidence 1: Time per n vs log(n) slope
        log_n = [d['log_n'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        slope_time_per_n, _ = np.polyfit(log_n, time_per_n, 1)
        
        if slope_time_per_n > 0.0001:
            evidence.append(f"Time per n increases with log(n) (slope: {slope_time_per_n:.6f})")
        else:
            evidence.append(f"Time per n is constant (slope: {slope_time_per_n:.6f})")
        
        # Evidence 2: Increase factor
        if len(time_per_n) >= 3:
            first_half = time_per_n[:len(time_per_n)//2]
            second_half = time_per_n[len(time_per_n)//2:]
            increase_factor = np.mean(second_half) / np.mean(first_half)
            
            if increase_factor > 1.5:
                evidence.append(f"Significant increase in time per n ({increase_factor:.2f}x)")
            else:
                evidence.append(f"Minimal increase in time per n ({increase_factor:.2f}x)")
        
        # Evidence 3: Ratio trend
        ratios = [d['ratio'] for d in data[1:]]
        if len(ratios) > 1:
            ratio_trend = np.polyfit(range(len(ratios)), ratios, 1)[0]
            
            if ratio_trend > 0.01:
                evidence.append(f"Ratios are increasing (trend: {ratio_trend:.6f})")
            else:
                evidence.append(f"Ratios are stable (trend: {ratio_trend:.6f})")
        
        # Make verdict
        linear_evidence = sum(1 for e in evidence if 'constant' in e or 'Minimal' in e or 'stable' in e)
        nlogn_evidence = sum(1 for e in evidence if 'increases' in e or 'Significant' in e or 'increasing' in e)
        
        print("  Evidence:")
        for e in evidence:
            print(f"    - {e}")
        
        if nlogn_evidence > linear_evidence:
            print(f"  🎯 VERDICT: O(n log n)")
        else:
            print(f"  🎯 VERDICT: O(n)")
        
        print()

if __name__ == "__main__":
    print("🚀 LAUNCHING PROPER COMPLEXITY DETECTOR 🚀")
    print("=" * 50)
    
    # Test with larger ranges
    results = test_with_larger_range()
    
    # Analyze with better metrics
    analyze_with_better_metrics(results)
    
    # Test pure sorting
    try:
        pure_results = test_pure_sorting()
    except Exception as e:
        print(f"Pure sorting test failed: {e}")
        pure_results = None
    
    # Final verdict
    final_verdict(results)
    
    # Plot comprehensive analysis
    try:
        plot_comprehensive_analysis(results, pure_results)
        print("\nComprehensive plots saved as 'proper_complexity_detection.png'")
    except Exception as e:
        print(f"\nCould not create plots: {e}")
    
    print("\n🎯 COMPLEXITY DETECTION COMPLETE! 🎯") 