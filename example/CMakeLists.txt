cmake_minimum_required(VERSION 2.8.11)

project(ResToC)

include_directories(..)

set(CMAKE_C_FLAGS "-std=c99 -g3 -O0 -ldl -rdynamic")

add_executable(example main.c ../generated_resources.c resources_gen.c)

# Generate resources_gen before building target
add_custom_command(
	OUTPUT resources_gen.c
	PRE_BUILD
	COMMAND ../restoc_gen.py resources_config.json ${CMAKE_CURRENT_BINARY_DIR}/resources_gen.c
	DEPENDS dummy.txt
	COMMENT "Generating C source code for resource embedding"
	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

# Embed resources after building target
add_custom_command(
	TARGET example
	POST_BUILD
	COMMAND ../restoc_embed.py resources_config.json ${CMAKE_CURRENT_BINARY_DIR}/example
	COMMENT "Embedding resource binaries"
	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
