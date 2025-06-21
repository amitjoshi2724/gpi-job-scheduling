#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <boost/sort/spreadsort/float_sort.hpp>
#include <vector>
#include <tuple>
#include <algorithm>
#include <stdexcept>

namespace py = pybind11;
using namespace boost::sort::spreadsort;

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
    size_t n = jobs.size();
    // First sort by end time (index 1) - WITHOUT indices yet
    std::vector<SortableTuple3> sortable_end;
    sortable_end.reserve(n);
    for (const auto& job : jobs) {
        double key = std::get<1>(job);  // end time
        sortable_end.emplace_back(key, job);
    }
    float_sort(sortable_end.begin(), sortable_end.end());
    // Extract end-ordered jobs and ADD INDICES HERE (like the Python list comprehension)
    std::vector<std::tuple<double, double, double, int>> end_sorted;
    end_sorted.reserve(n);
    for (size_t i = 0; i < n; ++i) {
        const auto& item = sortable_end[i];
        end_sorted.emplace_back(std::get<0>(item.data), std::get<1>(item.data), std::get<2>(item.data), i + 1);
    }
    // Now sort by start time (index 0) for start-ordered jobs
    std::vector<SortableTuple4> sortable_start;
    sortable_start.reserve(n);
    for (const auto& job : end_sorted) {
        double key = std::get<0>(job);  // start time
        sortable_start.emplace_back(key, job);
    }
    float_sort(sortable_start.begin(), sortable_start.end());
    // Extract start-ordered jobs
    std::vector<std::tuple<double, double, double, int>> start_sorted;
    start_sorted.reserve(n);
    for (const auto& item : sortable_start) {
        start_sorted.push_back(item.data);
    }
    return py::make_tuple(py::cast(end_sorted), py::cast(start_sorted));
}

PYBIND11_MODULE(boost_spreadsort, m) {
    m.doc() = "Boost Spreadsort bindings using pybind11";
    m.def("float_sort_doubles", &float_sort_doubles, "Sort vector of doubles using float_sort", py::arg("vals"));
    m.def("float_sort_tuples_by_key", &float_sort_tuples_by_key, "Sort 3-tuples by float key using float_sort", py::arg("jobs"), py::arg("key_index"));
    m.def("float_sort_tuples_4_by_key", &float_sort_tuples_4_by_key, "Sort 4-tuples by float key using float_sort", py::arg("jobs"), py::arg("key_index"));
    m.def("float_sort_both_with_indices", &float_sort_both_with_indices, "Sort jobs by both end and start times with indices in one call", py::arg("jobs"));
}
