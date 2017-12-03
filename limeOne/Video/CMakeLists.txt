cmake_minimum_required(VERSION 2.8)
project( videoRealTime )

# version number
set(videoRealTime_VERSION_MAJOR 0)
set(videoRealTime_VERSION_MINOR 1)

include_directories( "${PROJECT_SOURCE_DIR}" )
include_directories( "${PROJECT_BINARY_DIR}" )

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( videoAnalysis realtime_analysis.cpp frame_analysis.cpp progress_bar.cpp)
target_link_libraries( videoAnalysis ${OpenCV_LIBS} )
