cmake_minimum_required(VERSION 2.8)
project( videoRealTime )

# version number
set(videoRealTime_VERSION_MAJOR 0)
set(videoRealTime_VERSION_MINOR 1)

include_directories( "${PROJECT_SOURCE_DIR}" )
include_directories( "${PROJECT_BINARY_DIR}" )

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( demo realtime_demo.cpp )
target_link_libraries( demo ${OpenCV_LIBS})

add_executable( videoAnalysis realtime_analysis.cpp frame_analysis.cpp)
target_link_libraries( videoAnalysis ${OpenCV_LIBS} )
