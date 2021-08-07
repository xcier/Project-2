#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "OakSave.pb-c.h"
#include "OakProfile.pb-c.h"
#include "OakShared.pb-c.h"
#include "FileTranslator.h"

#define FILESIZE_LIMIT 9000000
#define OUTPUT_EXTENSION ".edited.sav"

extern struct Save save_t;
int saveMode;
FILE* inFile;
char* outFileName;
FILE* outFile;
FILE* origFile;
uint8_t* protoData;
int inFileLen;

int main(int argc, char** argv) {
	saveMode = 1;
	printf("CSAV001CNV Save to Protocol Buffer Data Translation Program\n");
	if(argc < 3) {
		fprintf(stderr, "CSAV001ABN Incorrect number of arguments: input.proto, original.sav, (optional) platform code\n");
		exit(1);
	}
	if(argc > 3) {
		printf("CSAV001CNV using user-specified platform...\n");
		saveMode = atoi(argv[3]);
	}
	inFile = fopen(argv[1], "r");
	if(inFile == NULL) {
		fprintf(stderr, "CSAV001ABN Failed to open input file.\n");
		exit(1);
	}
	outFileName = malloc(strlen(argv[1]) + strlen(OUTPUT_EXTENSION));
	strcpy(outFileName, argv[1]);
	strcat(outFileName, OUTPUT_EXTENSION);
	printf("CSAV00100I Output file = %s\n", outFileName);

	origFile = fopen(argv[2], "r");
	if(origFile == NULL) {
		fprintf(stderr, "CSAV001ABN Failed to open original file.\n");
		exit(1);
	}

	outFile = fopen(outFileName, "w");
	if(outFile == NULL) {
		fprintf(stderr, "CSAV001ABN Failed to open output file (read-only file system or bad DDNAME?)\n"),
		exit(1);
	}

	fseek(inFile, 0, SEEK_END);
	inFileLen = ftell(inFile);
	fseek(inFile, 0, SEEK_SET);
	protoData = malloc(inFileLen);
	if(!protoData) {
		printf("CSAV001ABD OUT OF MEMORY.\n");
		exit(420);
	}
	fread(protoData, inFileLen, sizeof(uint8_t), inFile);
	fclose(inFile);
	printf("CSAV001CNV Input protobuf file length: %d\n", inFileLen);
	writeSave(origFile, outFile, protoData, inFileLen, saveMode);
	printf("CSAV001CNV Execution complete\n");
	return 0;
}

