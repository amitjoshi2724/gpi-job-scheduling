#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <boost/sort/spreadsort/float_sort.hpp>
#include <vector>
#include <tuple>
#include <algorithm>
#include <stdexcept>
#include <chrono>
#include <iostream>

namespace py = pybind11;
using namespace boost::sort::spreadsort;

// Helper function to get current time in microseconds
auto get_time() {
    return std::chrono::high_resolution_clock::now();
}

// Helper function to get duration in microseconds
template<typename T>
double get_duration_us(T start, T end) {
    return std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
}

// Sort a vector of doubles using float_sort
std::vector<double> float_sort_doubles(std::vector<double> vals) {
    float_sort(vals.begin(), vals.end());
    return vals;
}

// Custom struct for 3-tuples that can be sorted by spreadsort
struct SortableTuple3 {
    double key;
    std::tuple<double, double, double> data;
    
    SortableTuple3(double k, const std::tuple<double, double, double>& d) 
        : key(k), data(d) {}
    
    // Conversion operator for spreadsort
    operator double() const { return key; }
};

// Custom struct for 4-tuples that can be sorted by spreadsort
struct SortableTuple4 {
    double key;
    std::tuple<double, double, double, int> data;
    
    SortableTuple4(double k, const std::tuple<double, double, double, int>& d) 
        : key(k), data(d) {}
    
    // Conversion operator for spreadsort
    operator double() const { return key; }
};

// Sort 3-tuples by float key using float_sort on custom structs
std::vector<std::tuple<double, double, double>> float_sort_tuples_by_key(
    const std::vector<std::tuple<double, double, double>>& jobs, int key_index) {
    size_t n = jobs.size();
    
    // Create sortable structs
    std::vector<SortableTuple3> sortable_jobs;
    sortable_jobs.reserve(n);
    for (const auto& job : jobs) {
        double key = (key_index == 0) ? std::get<0>(job) : std::get<1>(job);
        sortable_jobs.emplace_back(key, job);
    }
    
    // Sort using float_sort (spreadsort)
    float_sort(sortable_jobs.begin(), sortable_jobs.end());
    
    // Extract sorted tuples
    std::vector<std::tuple<double, double, double>> sorted_jobs;
    sorted_jobs.reserve(n);
    for (const auto& item : sortable_jobs) {
        sorted_jobs.push_back(item.data);
    }
    
    return sorted_jobs;
}

// Sort 4-tuples by float key using float_sort on custom structs
std::vector<std::tuple<double, double, double, int>> float_sort_tuples_4_by_key(
    const std::vector<std::tuple<double, double, double, int>>& jobs, int key_index) {
    size_t n = jobs.size();
    
    // Create sortable structs
    std::vector<SortableTuple4> sortable_jobs;
    sortable_jobs.reserve(n);
    for (const auto& job : jobs) {
        double key = (key_index == 0) ? std::get<0>(job) : std::get<1>(job);
        sortable_jobs.emplace_back(key, job);
    }
    
    // Sort using float_sort (spreadsort)
    float_sort(sortable_jobs.begin(), sortable_jobs.end());
    
    // Extract sorted tuples
    std::vector<std::tuple<double, double, double, int>> sorted_jobs;
    sorted_jobs.reserve(n);
    for (const auto& item : sortable_jobs) {
        sorted_jobs.push_back(item.data);
    }
    
    return sorted_jobs;
}

// Combined function that does both sorts and adds indices in one call, returning a Python tuple
py::tuple float_sort_both_with_indices(const std::vector<std::tuple<double, double, double>>& jobs) {
    auto total_start = get_time();
    size_t n = jobs.size();
    
    // First sort by end time (index 1) - WITHOUT indices yet
    auto end_sort_start = get_time();
    std::vector<SortableTuple3> sortable_end;
    sortable_end.reserve(n);
    for (const auto& job : jobs) {
        double key = std::get<1>(job);  // end time
        sortable_end.emplace_back(key, job);
    }
    auto end_sort_mid = get_time();
    float_sort(sortable_end.begin(), sortable_end.end());
    auto end_sort_end = get_time();
    
    // Extract end-ordered jobs and ADD INDICES HERE (like the Python list comprehension)
    auto index_add_start = get_time();
    std::vector<std::tuple<double, double, double, int>> end_sorted;
    end_sorted.reserve(n);
    for (size_t i = 0; i < n; ++i) {
        const auto& item = sortable_end[i];
        end_sorted.emplace_back(std::get<0>(item.data), std::get<1>(item.data), std::get<2>(item.data), i + 1);
    }
    auto index_add_end = get_time();
    
    // Now sort by start time (index 0) for start-ordered jobs
    auto start_sort_start = get_time();
    std::vector<SortableTuple4> sortable_start;
    sortable_start.reserve(n);
    for (const auto& job : end_sorted) {
        double key = std::get<0>(job);  // start time
        sortable_start.emplace_back(key, job);
    }
    auto start_sort_mid = get_time();
    float_sort(sortable_start.begin(), sortable_start.end());
    auto start_sort_end = get_time();
    
    // Extract start-ordered jobs
    auto final_extract_start = get_time();
    std::vector<std::tuple<double, double, double, int>> start_sorted;
    start_sorted.reserve(n);
    for (const auto& item : sortable_start) {
        start_sorted.push_back(item.data);
    }
    auto final_extract_end = get_time();
    
    auto total_end = get_time();
    
    return py::make_tuple(py::cast(end_sorted), py::cast(start_sorted));
}

// Optimized struct for better performance
struct Job {
    double start, end, weight;
    
    Job(double s, double e, double w) : start(s), end(e), weight(w) {}
    Job(const std::tuple<double, double, double>& t) 
        : start(std::get<0>(t)), end(std::get<1>(t)), weight(std::get<2>(t)) {}
    
    std::tuple<double, double, double> to_tuple() const {
        return {start, end, weight};
    }
};

// Optimized struct for 4-tuple jobs
struct JobWithIndex {
    double start, end, weight;
    int index;
    
    JobWithIndex(double s, double e, double w, int i) : start(s), end(e), weight(w), index(i) {}
    JobWithIndex(const Job& job, int i) : start(job.start), end(job.end), weight(job.weight), index(i) {}
    
    std::tuple<double, double, double, int> to_tuple() const {
        return {start, end, weight, index};
    }
};

// Optimized sortable structs
struct SortableJob {
    double key;
    Job data;
    
    SortableJob(double k, const Job& d) : key(k), data(d) {}
    operator double() const { return key; }
};

struct SortableJobWithIndex {
    double key;
    JobWithIndex data;
    
    SortableJobWithIndex(double k, const JobWithIndex& d) : key(k), data(d) {}
    operator double() const { return key; }
};

// Optimized combined function with reduced allocations and copying
py::tuple float_sort_both_with_indices_optimized(const std::vector<std::tuple<double, double, double>>& jobs) {
    auto total_start = get_time();
    size_t n = jobs.size();
    
    // Convert to Job structs once (more efficient than repeated tuple access)
    auto convert_start = get_time();
    std::vector<Job> job_structs;
    job_structs.reserve(n);
    for (const auto& job : jobs) {
        job_structs.emplace_back(job);
    }
    auto convert_end = get_time();
    
    // First sort by end time
    auto end_sort_start = get_time();
    std::vector<SortableJob> sortable_end;
    sortable_end.reserve(n);
    for (const auto& job : job_structs) {
        sortable_end.emplace_back(job.end, job);
    }
    auto end_sort_mid = get_time();
    float_sort(sortable_end.begin(), sortable_end.end());
    auto end_sort_end = get_time();
    
    // Add indices to end-sorted jobs
    auto index_add_start = get_time();
    std::vector<JobWithIndex> end_sorted_with_indices;
    end_sorted_with_indices.reserve(n);
    for (size_t i = 0; i < n; ++i) {
        end_sorted_with_indices.emplace_back(sortable_end[i].data, i + 1);
    }
    auto index_add_end = get_time();
    
    // Sort by start time
    auto start_sort_start = get_time();
    std::vector<SortableJobWithIndex> sortable_start;
    sortable_start.reserve(n);
    for (const auto& job : end_sorted_with_indices) {
        sortable_start.emplace_back(job.start, job);
    }
    auto start_sort_mid = get_time();
    float_sort(sortable_start.begin(), sortable_start.end());
    auto start_sort_end = get_time();
    
    // Convert back to tuples for Python
    auto final_convert_start = get_time();
    std::vector<std::tuple<double, double, double, int>> end_sorted;
    std::vector<std::tuple<double, double, double, int>> start_sorted;
    end_sorted.reserve(n);
    start_sorted.reserve(n);
    
    for (const auto& job : end_sorted_with_indices) {
        end_sorted.push_back(job.to_tuple());
    }
    for (const auto& item : sortable_start) {
        start_sorted.push_back(item.data.to_tuple());
    }
    auto final_convert_end = get_time();
    
    auto total_end = get_time();
    
    return py::make_tuple(py::cast(end_sorted), py::cast(start_sorted));
}

PYBIND11_MODULE(boost_spreadsort, m) {
    m.doc() = "Boost Spreadsort bindings using pybind11";
    m.def("float_sort_doubles", &float_sort_doubles, "Sort vector of doubles using float_sort", py::arg("vals"));
    m.def("float_sort_tuples_by_key", &float_sort_tuples_by_key, "Sort 3-tuples by float key using float_sort", py::arg("jobs"), py::arg("key_index"));
    m.def("float_sort_tuples_4_by_key", &float_sort_tuples_4_by_key, "Sort 4-tuples by float key using float_sort", py::arg("jobs"), py::arg("key_index"));
    m.def("float_sort_both_with_indices", &float_sort_both_with_indices, "Sort jobs by both end and start times with indices in one call", py::arg("jobs"));
    m.def("float_sort_both_with_indices_optimized", &float_sort_both_with_indices_optimized, "Optimized version with reduced allocations", py::arg("jobs"));
}
