#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "OakSave.pb-c.h"
#include "OakProfile.pb-c.h"
#include "OakShared.pb-c.h"
#include "FileTranslator.h"

#define FILESIZE_LIMIT 2000000

FILE* outFile;
FILE* inFile;

struct Save saveIn_t;
struct keyValuePair* kvpIn_t;

struct Save saveOut_t;
struct keyValuePair* kvpOut_t;


int main(int argc, char** argv) {
	int payloadStart;
	int processedLen;
	int pc_in = 0;
	int pc_out = 0;
	int i;
	printf("CSAV001SCA Binary Save Conversion Program\n");
	if(argc < 4) {
		printf("CSAV001ABN Incorrect number of arguments! SaveConvert in.sav out.sav platformcode_in platformcode_out\n");
		exit(1);
	}
	inFile = fopen(argv[1], "r");
	if(inFile == NULL) {
		printf("CSAV001ABN File not found\n");
		exit(1);
	}
	outFile = fopen(argv[2], "w");
	if(outFile == NULL) {
		printf("CSAV001ABN Failed to open output file (read-only file system or bad DDNAME?)\n"),
		exit(1);
	}
	pc_in = atoi(argv[3]);
	pc_out = atoi(argv[4]);
	
	

	printf("CSAV001SCA Reading file...\n");
	saveIn_t.header = malloc(4);
	fread(saveIn_t.header, sizeof(char), 4, inFile);
	fread(&saveIn_t.sg_version, sizeof(int32_t), 1, inFile);
	fread(&saveIn_t.pkg_version, sizeof(int32_t), 1, inFile);
	fread(&saveIn_t.engine_major, sizeof(int16_t), 1, inFile);
	fread(&saveIn_t.engine_minor, sizeof(int16_t), 1, inFile);
	fread(&saveIn_t.engine_patch, sizeof(int16_t), 1, inFile);
	fread(&saveIn_t.engine_build, sizeof(uint32_t), 1, inFile);
	fread(&saveIn_t.build_id_length, sizeof(int32_t), 1, inFile);
	saveIn_t.build_id = malloc(saveIn_t.build_id_length);
	fread(saveIn_t.build_id, sizeof(char), saveIn_t.build_id_length, inFile);
	fread(&saveIn_t.fmt_version, sizeof(int32_t), 1, inFile);
	fread(&saveIn_t.fmt_count, sizeof(int32_t), 1, inFile);
	kvpIn_t = malloc(saveIn_t.fmt_count * sizeof(struct keyValuePair));
	for(i = 0; i < saveIn_t.fmt_count; i++) {
		kvpIn_t[i].guid = malloc(16);
		fread(kvpIn_t[i].guid, sizeof(char), 16, inFile);
		fread(&kvpIn_t[i].entry, sizeof(int32_t), 1, inFile);
	}
	fread(&saveIn_t.sg_type_len, sizeof(int32_t), 1, inFile);
	saveIn_t.sg_type = malloc(saveIn_t.sg_type_len);
	fread(saveIn_t.sg_type, sizeof(char), saveIn_t.sg_type_len, inFile);
	fread(&saveIn_t.remaining_data_len, sizeof(int32_t), 1, inFile);
	payloadStart = ftell(inFile);
	saveIn_t.remaining_data = malloc(saveIn_t.remaining_data_len);
	fread(saveIn_t.remaining_data, sizeof(char), saveIn_t.remaining_data_len, inFile);

	printf("CSAV001SCA Input save information:\n");
	printf("CSAV001SCA Header: %s\n", saveIn_t.header);
	printf("CSAV001SCA SG version: %d\n", saveIn_t.sg_version);
	printf("CSAV001SCA Package version: %d\n", saveIn_t.pkg_version);
	printf("CSAV001SCA Engine version: %d.%d.%d\n", saveIn_t.engine_major, saveIn_t.engine_minor, saveIn_t.engine_patch);
	printf("CSAV001SCA Build ID length: %d\n", saveIn_t.build_id_length);
	printf("CSAV001SCA Build ID: %s\n", saveIn_t.build_id);
	printf("CSAV001SCA Custom format version: %d\n", saveIn_t.fmt_version);
	printf("CSAV001SCA Custom format count: %d\n", saveIn_t.fmt_count);
	//for(i = 0; i < saveIn_t.fmt_count; i++) {
	//	printf("Custom format %d: GUID: %x, entry %d\n", i, kvp_t[i].guid, kvp_t[i].entry);
	//}
	printf("CSAV001SCA Save type length: %d\n", saveIn_t.sg_type_len);
	printf("CSAV001SCA Save type: %s\n", saveIn_t.sg_type);
	printf("CSAV001SCA Payload start position: %d\n", payloadStart);
	printf("CSAV001SCA Payload length: %d\n", saveIn_t.remaining_data_len);

	if(pc_in == 1) {
		processedLen = decryptSave(saveIn_t.remaining_data, 0, saveIn_t.remaining_data_len);
	}
	else if(pc_in == 2) {
		processedLen = decryptProfile(saveIn_t.remaining_data, 0, saveIn_t.remaining_data_len);
	}
	else if(pc_in == 3) {
		processedLen = decryptSave_PS4(saveIn_t.remaining_data, 0, saveIn_t.remaining_data_len);
	}
	else if(pc_in == 4) {
		processedLen = decryptProfile_PS4(saveIn_t.remaining_data, 0, saveIn_t.remaining_data_len);
	}
	if(pc_in == 7) {
		processedLen = decryptSave(saveIn_t.remaining_data, 0, saveIn_t.remaining_data_len);
	}
	else if(pc_in == 8) {
		processedLen = decryptProfile(saveIn_t.remaining_data, 0, saveIn_t.remaining_data_len);
	}


	saveOut_t = saveIn_t;
	kvpOut_t = kvpIn_t;
	

	if(pc_out == 1) {
		saveOut_t.build_id = "OAK-PATCHWIN641-118";
	}
	else if(pc_out == 2) {
		saveOut_t.build_id = "OAK-PATCHWIN641-118";
	}
	else if(pc_out == 3) {
		saveOut_t.build_id = "OAK-PADPS41-31";
	}
	else if(pc_out == 4) {
		saveOut_t.build_id = "OAK-PADPS41-31";
	}
	else if(pc_out == 7) {
		saveOut_t.build_id = "OAK-PATCHDIESEL0-200";
	}
	else if(pc_out == 8) {
		saveOut_t.build_id = "OAK-PATCHDIESEL0-200";
	}


	printf("CSAV001SCA Output save information:\n");
	printf("CSAV001SCA Header: %s\n", saveOut_t.header);
	printf("CSAV001SCA SG version: %d\n", saveOut_t.sg_version);
	printf("CSAV001SCA Package version: %d\n", saveOut_t.pkg_version);
	printf("CSAV001SCA Engine version: %d.%d.%d\n", saveOut_t.engine_major, saveOut_t.engine_minor, saveOut_t.engine_patch);
	printf("CSAV001SCA Build ID length: %d\n", saveOut_t.build_id_length);
	printf("CSAV001SCA Build ID: %s\n", saveOut_t.build_id);
	printf("CSAV001SCA Custom format version: %d\n", saveOut_t.fmt_version);
	printf("CSAV001SCA Custom format count: %d\n", saveOut_t.fmt_count);
	//for(i = 0; i < saveOut_t.fmt_count; i++) {
	//	printf("Custom format %d: GUID: %x, entry %d\n", i, kvpOut_t[i].guid, kvpOut_t[i].entry);
	//}
	printf("CSAV001SCA Save type length: %d\n", saveOut_t.sg_type_len);
	printf("CSAV001SCA Save type: %s\n", saveOut_t.sg_type);
	printf("CSAV001SCA Payload start position: %d\n", payloadStart);
	printf("CSAV001SCA Payload length: %d\n", saveOut_t.remaining_data_len);

	if(pc_out == 1) {
		processedLen = encryptSave(saveOut_t.remaining_data, 0, saveOut_t.remaining_data_len);
	}
	else if(pc_out == 2) {
		processedLen = encryptProfile(saveOut_t.remaining_data, 0, saveOut_t.remaining_data_len);
	}
	else if(pc_out == 3) {
		processedLen = encryptSave_PS4(saveOut_t.remaining_data, 0, saveOut_t.remaining_data_len);
	}
	else if(pc_out == 4) {
		processedLen = encryptProfile_PS4(saveOut_t.remaining_data, 0, saveOut_t.remaining_data_len);
	}

	printf("CSAV001SCA Writing new file...\n");
	fwrite(saveOut_t.header, sizeof(char), 4, outFile);
	fwrite(&saveOut_t.sg_version, sizeof(int32_t), 1, outFile);
	fwrite(&saveOut_t.pkg_version, sizeof(int32_t), 1, outFile);
	fwrite(&saveOut_t.engine_major, sizeof(int16_t), 1, outFile);
	fwrite(&saveOut_t.engine_minor, sizeof(int16_t), 1, outFile);
	fwrite(&saveOut_t.engine_patch, sizeof(int16_t), 1, outFile);
	fwrite(&saveOut_t.engine_build, sizeof(uint32_t), 1, outFile);
	fwrite(&saveOut_t.build_id_length, sizeof(int32_t), 1, outFile);
	fwrite(saveOut_t.build_id, sizeof(char), saveOut_t.build_id_length, outFile);
	fwrite(&saveOut_t.fmt_version, sizeof(int32_t), 1, outFile);
	fwrite(&saveOut_t.fmt_count, sizeof(int32_t), 1, outFile);
	for(i = 0; i < saveOut_t.fmt_count; i++) {
		fwrite(kvpOut_t[i].guid, sizeof(char), 16, outFile);
		fwrite(&kvpOut_t[i].entry, sizeof(int32_t), 1, outFile);
	}
	fwrite(&saveOut_t.sg_type_len, sizeof(int32_t), 1, outFile);
	fwrite(saveOut_t.sg_type, sizeof(char), saveOut_t.sg_type_len, outFile);
	fwrite(&saveOut_t.remaining_data_len, sizeof(int32_t), 1, outFile);
	fwrite(saveOut_t.remaining_data, sizeof(char), saveOut_t.remaining_data_len, outFile);


	printf("CSAV001SCA Execution complete\n");
	return 0;
}

