cmake_minimum_required(VERSION 3.20)
project(f1_telemetry_simulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(CURL REQUIRED)

include_directories(include)

add_executable(f1_telemetry_simulator
    src/main.cpp
    src/car_simulator.cpp
    src/telemetry_generator.cpp
    src/track_model.cpp
    src/replay_engine.cpp
    src/utils.cpp
)

target_link_libraries(f1_telemetry_simulator PRIVATE CURL::libcurl)

enable_testing()

add_executable(simulator_tests
    tests/simulator_tests.cpp
    src/car_simulator.cpp
    src/track_model.cpp
    src/utils.cpp
)

add_test(NAME simulator_tests COMMAND simulator_tests)
