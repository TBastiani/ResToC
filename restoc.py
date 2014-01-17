#!/usr/bin/env python27

import sys
import json
import os

def printUsage():
	print("Usage:")
	print("\t./bintoc.py <resource_config.json> <resources_gen.c>")
	exit(-1)

# Validate arguments
if len(sys.argv) != 3:
	printUsage()

# Read JSON
with open(sys.argv[1], "r") as jsonFile:
	jsonStr = jsonFile.read()
resourceDesc = json.loads(jsonStr)

# Generate *.c file
# Open ouput file
outputFile = open(sys.argv[2], "w")

# Write file header
headerStr = "#include \"generated_resources.h\"\n"
outputFile.write(headerStr)

# Write content
resourceIndex = 0
for key in resourceDesc:
	data = open(resourceDesc[key], "r").read()
	
	# Write data
	outputFile.write("static const uint8_t data_field_")
	outputFile.write(str(resourceIndex))
	outputFile.write("[] = {")
	
	for index in range(0, len(data)):
		outputFile.write(hex(ord(data[index])))
		outputFile.write(",")
	
	outputFile.write("};\n")

	# Write struct
	outputFile.write("resource_t resource_")
	outputFile.write(str(resourceIndex))
	outputFile.write(" = {\"")
	outputFile.write(key)
	outputFile.write("\",")
	outputFile.write(str(os.stat(resourceDesc[key]).st_size))
	outputFile.write(",data_field_")
	outputFile.write(str(resourceIndex))
	outputFile.write(",};\n")
	
	resourceIndex = resourceIndex + 1

# Write global array
outputFile.write("extern const resource_t *__named_resources_table[] = {")
resourceIndex = 0
for key in resourceDesc:
	outputFile.write("(const resource_t *) (&resource_")
	outputFile.write(str(resourceIndex))
	outputFile.write("),")

	resourceIndex = resourceIndex + 1

outputFile.write("};\n")
outputFile.write("extern const unsigned __named_resources_count = ")
outputFile.write(str(resourceIndex))
outputFile.write(";\n\n")

outputFile.close()

print("Successfully generated c source file")
exit(0)