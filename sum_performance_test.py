import time
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

def sum_numbers(n):
    """Sum numbers from 1 to n"""
    return sum(range(1, n + 1))

def test_sum_performance(n, num_trials=10):
    """Test performance of summing 1 to n with multiple trials"""
    times = []
    
    for _ in range(num_trials):
        start_time = time.time()
        result = sum_numbers(n)
        end_time = time.time()
        times.append(end_time - start_time)
    
    return mean(times), result

def run_performance_experiment():
    """Run the performance experiment with n from 1000 to 1e7"""
    # Define n values with step size of 1000
    n_values = list(range(1000, int(1e7) + 1, 1000))
    
    results = []
    
    print("Running performance test...")
    print(f"Testing n values from {n_values[0]} to {n_values[-1]}")
    print(f"Number of trials per n: 10")
    print(f"Total number of n values: {len(n_values)}")
    print("-" * 50)
    
    for i, n in enumerate(n_values):
        avg_time, result = test_sum_performance(n, num_trials=10)
        per_job_time = avg_time / n
        
        results.append((n, avg_time, per_job_time, result))
        
        # Progress indicator - show every 1000th test or every 10%
        if (i + 1) % 1000 == 0 or (i + 1) % (len(n_values) // 10) == 0 or i == len(n_values) - 1:
            print(f"Completed {i + 1}/{len(n_values)}: n={n:,}, avg_time={avg_time:.6f}s, per_job={per_job_time:.2e}s")
    
    return results

def plot_results(results):
    """Plot the performance results"""
    n_values, total_times, per_job_times, _ = zip(*results)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Total Runtime Plot
    ax1.plot(n_values, total_times, marker='o', markersize=6, linewidth=2, color='blue')
    ax1.set_xlabel('Number of Jobs (n)', fontsize=12)
    ax1.set_ylabel('Total Runtime (s)', fontsize=12)
    ax1.set_title('Total Runtime: Sum 1 to n', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Per-Job Runtime Plot
    ax2.plot(n_values, per_job_times, marker='s', markersize=6, linewidth=2, color='red')
    ax2.set_xlabel('Number of Jobs (n)', fontsize=12)
    ax2.set_ylabel('Runtime per Job (s)', fontsize=12)
    ax2.set_title('Per-Job Runtime: Sum 1 to n', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('sum_performance_analysis.pdf', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary statistics
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    print(f"Smallest n: {n_values[0]:,}")
    print(f"Largest n: {n_values[-1]:,}")
    print(f"Total runtime range: {min(total_times):.6f}s - {max(total_times):.6f}s")
    print(f"Per-job runtime range: {min(per_job_times):.2e}s - {max(per_job_times):.2e}s")
    
    # Check if per-job runtime is constant (should be for simple sum)
    per_job_variance = np.var(per_job_times)
    print(f"Per-job runtime variance: {per_job_variance:.2e}")
    print(f"Expected complexity: O(n) for total, O(1) for per-job")

def main():
    """Main function to run the experiment"""
    print("Sum Performance Test")
    print("Testing runtime of summing numbers from 1 to n")
    print("="*50)
    
    # Run the experiment
    results = run_performance_experiment()
    
    # Plot the results
    plot_results(results)
    
    # Save results to file
    with open('sum_performance_results.txt', 'w') as f:
        f.write("n,total_time,per_job_time,result\n")
        for n, total_time, per_job_time, result in results:
            f.write(f"{n},{total_time:.6f},{per_job_time:.2e},{result}\n")
    
    print(f"\nResults saved to 'sum_performance_results.txt'")
    print(f"Plot saved to 'sum_performance_analysis.pdf'")

if __name__ == "__main__":
    main() 