# ResToC

Python tool to embed binary resources as C source code.

# Usage

This tool is meant to be used as a separate step before source code compilation.

Step 1: Simply create a JSON file that describes the resources you want to embed into your executable. The JSON should consist of a single dictionary of strings where keys are the names of resources within your executables and values are their relative paths.

Step 2: Use your build system to run `restoc_gen.py` as follows: `python restoc_gen.py resources.json compiled_resources.c`

Step 3: Include `generated_resources.h` and add `generated_resources.c` and `compiled_resources.c` into your projects's source list.

Step 4: Use your build system to run `restoc_embed.py` as follows: `python restoc_embed.py resources.json <your_binary>`

# Access the resources from C

```C
#include "generated_resources.h"

int main(int argc, char **argv)
{
	uint64_t resourceLength;
	const uint8_t *resource = GetNamedResource("resource name", &resourceLength);

	/* Do whatever you like with it */

	return 0;
}
```

# Notes

We used to generate source files with data inside. The problem with this approach was that it would be very slow at compile time for some of the larger resource files. The new "2-step" approach is slightly more convoluted and harder to integrate but it runs much faster and doesn't consume as much memory.
