#!/usr/bin/env python2

# Copyright (c) 2014-2016, Thomas Bastiani
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the organization nor the
#      names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys      # argv
import json     # config file
import hashlib  # sha1


def printUsage():
    print("Usage:")
    print("\t./restoc_gen.py <resource_config.json> <resources_gen.c>")
    exit(-1)

# Validate arguments
if len(sys.argv) != 3:
    printUsage()

# Read JSON
jsonStr = open(sys.argv[1], "r").read()
resourceDesc = json.loads(jsonStr)

# Generate *.c file
# Open ouput file
outputFile = open(sys.argv[2], "wb")

# Write file header
headerStr = "#include \"generated_resources.h\"\n"
outputFile.write(headerStr)

# Write content
resourceIndex = 0
for key in resourceDesc:
    data = open(resourceDesc[key], "rb").read()

    h = hashlib.sha1()
    h.update(key)
    sha1 = h.digest()

    # Write data
    outputFile.write(
        "static const uint8_t data_field_{}[{}] = {{".format(
            resourceIndex, max(len(data) + 1, h.digest_size)))

    for i in range(0, len(sha1)):
        outputFile.write(hex(ord(sha1[i])))
        outputFile.write(",")

    outputFile.write("};\n")

    # Write struct
    outputFile.write(
            """resource_t resource_{} = """
            """{{"{}",{},data_field_{},}};\n""".format(
                resourceIndex, key, len(data), resourceIndex))

    resourceIndex = resourceIndex + 1

# Write global array
outputFile.write("const resource_t *__named_resources_table[] = {")
resourceIndex = 0
for key in resourceDesc:
    outputFile.write(
            "(const resource_t *) (&resource_{}),".format(resourceIndex))
    resourceIndex = resourceIndex + 1

outputFile.write("}};\nconst unsigned __named_resources_count = {};\n\n"
        .format(resourceIndex))
outputFile.close()

print("Successfully generated c source file")
exit(0)
