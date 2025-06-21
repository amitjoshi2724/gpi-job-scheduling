cmake_minimum_required(VERSION 3.14)
project(boost_spreadsort)

set(CMAKE_CXX_STANDARD 17)

# Add this block to fetch pybind11 automatically
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        stable
)
FetchContent_MakeAvailable(pybind11)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(Boost REQUIRED)

pybind11_add_module(boost_spreadsort spreadsort.cpp)
target_include_directories(boost_spreadsort PRIVATE ${Boost_INCLUDE_DIRS})

