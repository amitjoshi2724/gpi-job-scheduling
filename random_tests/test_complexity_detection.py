#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import time
import gc
import random
from scheduling_algos import gpi_weighted_job_scheduling

def generate_test_jobs(n):
    """Generate test jobs for complexity analysis"""
    MAX_VAL = 10**6
    jobs = [(random.randint(0, MAX_VAL), random.randint(0, MAX_VAL), random.randint(1, 100)) for _ in range(n)]
    jobs = [(min(s, e), max(s, e), w) for s, e, w in jobs]
    return jobs

def test_complexity_detection():
    """Test why O(n log n) algorithms can pass linear complexity tests"""
    
    # Set random seed for reproducibility
    RANDOM_SEED = 2724
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    # Test sizes - need larger range to see the difference
    sizes = list(range(1000, 100001, 5000))  # More data points
    
    # Test both linear and O(n log n) algorithms
    algorithms = {
        'Linear (Radix)': 'radix',
        'O(n log n) (Timsort)': 'default'
    }
    
    results = {}
    
    print("=== Complexity Detection Test ===")
    print("Testing why O(n log n) algorithms can pass linear tests...")
    print()
    
    for algo_name, sort_algo in algorithms.items():
        print(f"Testing {algo_name}:")
        print(f"{'Size':<8} {'Time (ms)':<12} {'Time/n':<12} {'Ratio':<8} {'Log(n)':<8}")
        print("-" * 60)
        
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
            
            # Calculate ratio to previous size
            ratio = time_per_n / prev_time_per_n if prev_time_per_n else 1.0
            
            # Calculate log(n) for comparison
            log_n = np.log(n)
            
            print(f"{n:<8} {total_time_ms:<12.3f} {time_per_n:<12.6f} {ratio:<8.3f} {log_n:<8.3f}")
            
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

def analyze_complexity_detection(results):
    """Analyze why the detection method fails"""
    print("=== Why O(n log n) Passes Linear Test ===")
    print()
    
    for algo_name, data in results.items():
        print(f"{algo_name}:")
        
        # Current method (log-log regression)
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
        
        # Calculate average ratio
        ratios = [d['ratio'] for d in data[1:]]
        avg_ratio = np.mean(ratios)
        
        print(f"  Current method - Slope (log-log): {slope:.3f}")
        print(f"  Current method - R-squared: {r_squared:.3f}")
        print(f"  Current method - Average ratio: {avg_ratio:.3f}")
        
        # Check if it passes the current test
        if abs(slope - 1.0) < 0.1 and r_squared > 0.95:
            print(f"  ❌ INCORRECTLY PASSES LINEAR TEST")
        else:
            print(f"  ✅ CORRECTLY FAILS LINEAR TEST")
        
        # Better analysis: Check if time_per_n increases with log(n)
        time_per_n = [d['time_per_n'] for d in data]
        log_n_values = [d['log_n'] for d in data]
        
        # Linear regression: time_per_n vs log(n)
        slope_time_per_n, _ = np.polyfit(log_n_values, time_per_n, 1)
        
        # R-squared for this fit
        y_pred_time_per_n = slope_time_per_n * np.array(log_n_values) + np.polyfit(log_n_values, time_per_n, 1)[1]
        ss_res_time_per_n = np.sum((np.array(time_per_n) - y_pred_time_per_n) ** 2)
        ss_tot_time_per_n = np.sum((np.array(time_per_n) - np.mean(time_per_n)) ** 2)
        r_squared_time_per_n = 1 - (ss_res_time_per_n / ss_tot_time_per_n)
        
        print(f"  Better method - Time per n vs log(n) slope: {slope_time_per_n:.6f}")
        print(f"  Better method - R-squared: {r_squared_time_per_n:.3f}")
        
        if slope_time_per_n > 0.0001 and r_squared_time_per_n > 0.7:
            print(f"  ✅ CORRECTLY IDENTIFIED AS O(n log n)")
        else:
            print(f"  ❌ INCORRECTLY IDENTIFIED AS LINEAR")
        
        print()

def plot_complexity_comparison(results):
    """Plot comparison between linear and O(n log n) algorithms"""
    plt.figure(figsize=(16, 12))
    
    # Plot 1: Time vs Size (log-log)
    plt.subplot(2, 3, 1)
    for algo_name, data in results.items():
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        plt.loglog(sizes, times, 'o-', label=algo_name, alpha=0.7, markersize=4)
    
    # Add reference lines
    x_ref = np.array([1000, 100000])
    plt.loglog(x_ref, x_ref * 0.001, '--', alpha=0.5, label='O(n) reference')
    plt.loglog(x_ref, x_ref * np.log(x_ref) * 0.0001, '--', alpha=0.5, label='O(n log n) reference')
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (ms)')
    plt.title('Time vs Input Size (Log-Log)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Time per element vs Size
    plt.subplot(2, 3, 2)
    for algo_name, data in results.items():
        sizes = [d['size'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        plt.semilogx(sizes, time_per_n, 'o-', label=algo_name, alpha=0.7, markersize=4)
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time per Element (ms)')
    plt.title('Time per Element vs Input Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Time per element vs log(n)
    plt.subplot(2, 3, 3)
    for algo_name, data in results.items():
        log_n = [d['log_n'] for d in data]
        time_per_n = [d['time_per_n'] for d in data]
        plt.plot(log_n, time_per_n, 'o-', label=algo_name, alpha=0.7, markersize=4)
    
    plt.xlabel('log(n)')
    plt.ylabel('Time per Element (ms)')
    plt.title('Time per Element vs log(n)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Ratio analysis
    plt.subplot(2, 3, 4)
    for algo_name, data in results.items():
        sizes = [d['size'] for d in data[1:]]
        ratios = [d['ratio'] for d in data[1:]]
        plt.semilogx(sizes, ratios, 'o-', label=algo_name, alpha=0.7, markersize=4)
    
    plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Linear reference')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time Ratio (current/previous)')
    plt.title('Scaling Ratio Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 5: Theoretical vs Actual
    plt.subplot(2, 3, 5)
    for algo_name, data in results.items():
        sizes = [d['size'] for d in data]
        times = [d['time_ms'] for d in data]
        
        if 'Linear' in algo_name:
            # Plot against O(n)
            plt.loglog(sizes, times, 'o-', label=f'{algo_name} (actual)', alpha=0.7, markersize=4)
            plt.loglog(sizes, np.array(sizes) * 0.001, '--', label=f'{algo_name} (theoretical O(n))', alpha=0.5)
        else:
            # Plot against O(n log n)
            plt.loglog(sizes, times, 's-', label=f'{algo_name} (actual)', alpha=0.7, markersize=4)
            plt.loglog(sizes, np.array(sizes) * np.log(np.array(sizes)) * 0.0001, '--', label=f'{algo_name} (theoretical O(n log n))', alpha=0.5)
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (ms)')
    plt.title('Theoretical vs Actual Performance')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 6: Complexity detection
    plt.subplot(2, 3, 6)
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
    
    plt.tight_layout()
    plt.savefig('complexity_detection_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def explain_why_detection_fails():
    """Explain why the current detection method fails"""
    print("=== Why Current Method Fails to Detect O(n log n) ===")
    print()
    
    reasons = [
        {
            "issue": "Limited Input Range",
            "description": "The range 1000-100000 is too small to see the log(n) factor clearly.",
            "solution": "Test with larger ranges (e.g., 1000 to 10^6 or 10^7)"
        },
        {
            "issue": "Log-Log Plot Masking",
            "description": "On log-log plots, O(n log n) can appear linear for small ranges.",
            "solution": "Use time_per_n vs log(n) plots instead"
        },
        {
            "issue": "System Overhead Dominance",
            "description": "Python-C++ overhead and system effects mask the algorithmic complexity.",
            "solution": "Test with pure algorithmic implementations"
        },
        {
            "issue": "Loose Thresholds",
            "description": "Slope tolerance of 0.1 is too loose for detecting O(n log n).",
            "solution": "Use stricter thresholds or different metrics"
        },
        {
            "issue": "R-squared Focus",
            "description": "High R-squared doesn't guarantee linear complexity.",
            "solution": "Focus on the actual slope value, not just fit quality"
        }
    ]
    
    for i, reason in enumerate(reasons, 1):
        print(f"{i}. {reason['issue']}")
        print(f"   {reason['description']}")
        print(f"   Solution: {reason['solution']}")
        print()

def improved_complexity_test():
    """Demonstrate an improved complexity detection method"""
    print("=== Improved Complexity Detection Method ===")
    print()
    
    print("Better approach:")
    print("1. Plot time_per_n vs log(n)")
    print("2. If slope > threshold, it's O(n log n)")
    print("3. If slope ≈ 0, it's O(n)")
    print("4. Use larger input ranges")
    print("5. Test with pure algorithmic implementations")
    print()

if __name__ == "__main__":
    # Test complexity detection
    results = test_complexity_detection()
    
    # Analyze why detection fails
    analyze_complexity_detection(results)
    
    # Explain the issues
    explain_why_detection_fails()
    
    # Show improved method
    improved_complexity_test()
    
    # Plot comparison
    try:
        plot_complexity_comparison(results)
        print("\nPlots saved as 'complexity_detection_analysis.png'")
    except Exception as e:
        print(f"\nCould not create plots: {e}")
        print("Analysis completed successfully.") 