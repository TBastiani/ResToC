/*
Copyright (c) 2014-2016, Thomas Bastiani
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the organization nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>

#include "generated_resources.h"

#define PREFIX "restoc_resource_"
#define SUFFIX "_length"
#define PREFIX_LEN 16
#define SUFFIX_LEN 7
#define MAX_LEN 256

#ifdef __cplusplus
extern "C" {
#endif

const uint8_t *GetNamedResource(const char *name, uint64_t *length)
{
	/* Check arguments */
	if (name == NULL)
		return NULL;
	if (length == NULL)
		return NULL;

	/* Open current executable */
	void *handle = dlopen(NULL, RTLD_LAZY);
	if (handle == NULL)
		return NULL;

	/* Resolve resource symbol */
	size_t nameLength = strnlen(name, MAX_LEN);
	char symbol[PREFIX_LEN + SUFFIX_LEN + MAX_LEN + 1];
	size_t offset = 0;

	memcpy(symbol + offset, PREFIX, PREFIX_LEN);
	offset += PREFIX_LEN;
	memcpy(symbol + offset, name, nameLength);
	offset += nameLength;
	symbol[offset] = '\0';

	uint64_t *resourceLength;
	const uint8_t *resource = (const uint8_t *) dlsym(handle, symbol);
	if (resource == NULL)
		goto end;

	/* Resolve resource length symbol */
	memcpy(symbol + offset, SUFFIX, SUFFIX_LEN);
	offset += SUFFIX_LEN;
	symbol[offset] = '\0';

	resourceLength = (uint64_t *) dlsym(handle, symbol);
	if (resourceLength == NULL)
	{
		resource = NULL;
		goto end;
	}

	/* Output length */
	*length = *resourceLength;

end:
	dlclose(handle);
	return resource;
}

#ifdef __cplusplus
};
#endif
