#!/bin/bash

# Run all experiment Python files
echo "Running experiment1_random_intervals.py..."
python3 experiment1_random_intervals.py

echo "Running experiment2_normal_start_times.py..."
python3 experiment2_normal_start_times.py

echo "Running experiment3_zipf_duration.py..."
python3 experiment3_zipf_duration.py

echo "Running experiment4_uniform_bucket_ideal.py..."
python3 experiment4_uniform_bucket_ideal.py

echo "All experiments completed!"
