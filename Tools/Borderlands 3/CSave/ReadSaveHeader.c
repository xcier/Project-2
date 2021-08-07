#include <stdio.h>
#include <stdlib.h>
#include "FileTranslator.h"

#define FILESIZE_LIMIT 2000000

extern struct Save save_t;
FILE* inFile;

int main(int argc, char** argv) {
	printf("CSAV001RSH Read Save Header utility\n");
	if(argc < 2) {
		printf("CSAV001ABN Incorrect number of arguments (specify an input file)\n");
		exit(1);
	}
	inFile = fopen(argv[1], "r");

	readSaveHeader(inFile);
	printf("CSAV001RSH Execution complete\n");
	return 0;
}

