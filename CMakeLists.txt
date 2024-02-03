cmake_minimum_required(VERSION 3.10)
project(DartScoreRecorder)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(DartScoreRecorder main.cpp DartDetector.cpp ScoreCalculator.cpp CameraCapture.cpp)
target_link_libraries(DartScoreRecorder ${OpenCV_LIBS})
