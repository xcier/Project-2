#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "OakSave.pb-c.h"
#include "OakProfile.pb-c.h"
#include "OakShared.pb-c.h"
#include "FileTranslator.h"

#define FILESIZE_LIMIT 2000000

extern struct Save save_t;
int saveMode;
FILE* inFile;
char* outFileName;
FILE* outFile;

int main(int argc, char** argv) {
	saveMode = 2;
	printf("CSAV001CNV Save to Protocol Buffer Data Translation Program (for profile saves)\n");
	if(argc < 2) {
		printf("CSAV001ABN Incorrect number of arguments (specify an input file and optionally a platform code)\n");
		exit(1);
	}
	if(argc > 2) {
		printf("CSAV001CNV using user-specified platform...\n");
		saveMode = atoi(argv[2]);
	}
		
	inFile = fopen(argv[1], "r");
	if(inFile == NULL) {
		printf("CSAV001ABN File not found\n");
		exit(1);
	}
	outFileName = strcat(argv[1], ".proto");
	printf("CSAV00200I Output file = %s\n", outFileName);
	outFile = fopen(outFileName, "w");
	if(outFile == NULL) {
		printf("CSAV001ABN Failed to open output file (read-only file system or bad DDNAME?)\n"),
		exit(1);
	}

	//uint8_t inputBuffer[FILESIZE_LIMIT];
	//int fileLen = read_buffer(FILESIZE_LIMIT, inputBuffer, inFile);
	//rewind(inFile); // Rewind the tape drive like it's 1981
	//printf("CSAV00200I File size = %d\n", fileLen);
	readSave(inFile, saveMode);
	fwrite(save_t.remaining_data, sizeof(char), save_t.remaining_data_len, outFile);
	printf("CSAV001CNV Execution complete\n");
	return 0;
}

