cmake_minimum_required( VERSION 3.0)
project(apue)

set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

set(CXX_FLAGS -std=c++11 -g -ggdb -Wall)

string(REPLACE ";" " " CMAKE_CXX_FLAGS "${CXX_FLAGS}")

set(CMAKE_CXX_COMPILER      "clang++" )
set(CMAKE_CXX_FLAGS_DEBUG   "-O0" )
set(CMAKE_CXX_FLAGS_RELEASE "-O2 -finline-limit=1000 -DNDEBUG " )


file(GLOB_RECURSE SRC_FILES ${PROJECT_SOURCE_DIR}/src/*.cpp)

include_directories(${PROJECT_SOURCE_DIR}/src/include)
include_directories(${PROJECT_SOURCE_DIR}/../../)
include_directories(${PROJECT_SOURCE_DIR}/../../include)

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/build/bin)
set(LIBRARY_OUTPUT_PATH    ${PROJECT_SOURCE_DIR}/build/lib)

link_directories    ( ${LIBRARY_OUTPUT_PATH})
include(${PROJECT_SOURCE_DIR}/../../include/gtest/CMakeLists.txt)   # build libgtest.a

foreach(f ${SRC_FILES})
    message(${f})
endforeach()

add_definitions(-DAPUE)

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/build/bin)
add_executable(${PROJECT_NAME} ${SRC_FILES})

set(LINK_LIBS gtest)
target_link_libraries(${PROJECT_NAME} ${LINK_LIBS})

