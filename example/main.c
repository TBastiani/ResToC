#include "generated_resources.h"

#include <stdio.h>

int main()
{
	uint64_t len;
	const uint8_t *data = GetNamedResource("dummy", &len);
	if (data == NULL)
	{
		printf("Named resource not found\n");
		return -1;
	}

	printf("Named resource: %s\n", data);

	return 0;
}
