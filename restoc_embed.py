#!/usr/bin/env python2

# Copyright (c) 2016, Thomas Bastiani
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
import os       # stat
import hashlib  # sha1
import numpy    # fromstring


def printUsage():
    print("Usage:")
    print("\t./restoc_embed.py <resource_config.json> <target_binary>")
    exit(-1)

# Validate arguments
if len(sys.argv) != 3:
    printUsage()

# Read JSON
jsonStr = open(sys.argv[1], "r").read()
resourceDesc = json.loads(jsonStr)

# Read target file
targetFile = open(sys.argv[2], "rb+")
targetData = targetFile.read()
targetData = numpy.fromstring(targetData, dtype=numpy.uint8)

# Embed one resource at a time
resourceIndex = 0
for key in resourceDesc:
    # Compute the "marker" that we should be looking for
    h = hashlib.sha1()
    h.update(key)
    sha1 = h.digest()

    # Search for marker occurences
    occurences = []
    for off in range(len(targetData)):
        found = 0
        for i in range(len(sha1)):
            if ord(sha1[i]) != targetData[off + i]:
                break
            found = found + 1

        if found == len(sha1):
            occurences.append(off)
            break

    if len(occurences) == 0:
        print("No marker for resource '{}' in file '{}'"
            .format(key, sys.argv[2]))
        sys.exit(-1)

    # Write resource at marker
    offset = occurences[0]
    resourceData = open(resourceDesc[key], "rb").read()
    resourceData = numpy.fromstring(resourceData, dtype=numpy.uint8)
    if len(targetData) < offset + len(resourceData):
        print("Not enough space reserved in file '{}' for resource '{}'"
            .format(sys.argv[2], key))
        sys.exit(-1)

    targetFile.seek(offset)
    targetFile.write(resourceData)
    targetFile.write(numpy.uint8(0))

    resourceIndex = resourceIndex + 1

print("Successfully embedded resources")
exit(0)
