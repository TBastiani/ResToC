# ResToC

Python tool to embed binary resources as C source code.

# Usage

This tool is meant to be used as a separate step before source code compilation.

Step 1: Simply create a JSON file that describes the resources you want to embed into your executable. The JSON should consist of a single dictionary of strings where keys are the names of resources within your executables and values are their relative paths.

Step 2: Use your build system to run `restoc.py` as follows: `python restoc.py resources.json compiled_resources.c`

Step 3: Then it becomes a simple matter of including `generated_resources.h`, `generated_resources.c` and `compiled_resources.c` into your projects's source list.

# Access the resources from C source code

```
#include "generated_resources.h"

int main(int argc, char **argv)
{
	uint64_t resourceLength;
	const uint8_t *resource = GetNamedResource("resource name", &resourceLength);

	/* Do whatever you like with it */

	return 0;
}
```