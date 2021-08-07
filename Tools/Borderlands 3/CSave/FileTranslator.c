#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "FileTranslator.h"


size_t read_buffer(int max_length, uint8_t* out, FILE* f) {
	size_t cur_len = 0;
	size_t nread;
	while ((nread = fread(out + cur_len, 1, max_length - cur_len, f)) != 0) {
		cur_len += nread;
		if (cur_len == max_length) {
			fprintf(stderr, "CSAVAB100B Buffer exceeded!\n");
			exit(1);
		}
	}
	return cur_len;
}

char PrefixMagic[] = {
	0x71, 0x34, 0x36, 0xB3, 0x56, 0x63, 0x25, 0x5F,
	0xEA, 0xE2, 0x83, 0x73, 0xF4, 0x98, 0xB8, 0x18,
	0x2E, 0xE5, 0x42, 0x2E, 0x50, 0xA2, 0x0F, 0x49,
	0x87, 0x24, 0xE6, 0x65, 0x9A, 0xF0, 0x7C, 0xD7
};

char XorMagic[] = {
	0x7C, 0x07, 0x69, 0x83, 0x31, 0x7E, 0x0C, 0x82,
	0x5F, 0x2E, 0x36, 0x7F, 0x76, 0xB4, 0xA2, 0x71,
	0x38, 0x2B, 0x6E, 0x87, 0x39, 0x05, 0x02, 0xC6,
	0xCD, 0xD8, 0xB1, 0xCC, 0xA1, 0x33, 0xF9, 0xB6
};

char ProfilePrefixMagic[] = {
	0xD8, 0x04, 0xB9, 0x08, 0x5C, 0x4E, 0x2B, 0xC0,
	0x61, 0x9F, 0x7C, 0x8D, 0x5D, 0x34, 0x00, 0x56,
	0xE7, 0x7B, 0x4E, 0xC0, 0xA4, 0xD6, 0xA7, 0x01,
	0x14, 0x15, 0xA9, 0x93, 0x1F, 0x27, 0x2C, 0x8F
};

char ProfileXorMagic[] = {
	0xE8, 0xDC, 0x3A, 0x66, 0xF7, 0xEF, 0x85, 0xE0,
	0xBD, 0x4A, 0xA9, 0x73, 0x57, 0x99, 0x30, 0x8C,
	0x94, 0x63, 0x59, 0xA8, 0xC9, 0xAE, 0xD9, 0x58,
	0x7D, 0x51, 0xB0, 0x1E, 0xBE, 0xD0, 0x77, 0x43
};

char ProfilePrefixMagic_PS4[] = {
	0xad, 0x1e, 0x60, 0x4e, 0x42, 0x9e, 0xa9, 0x33, 0xb2, 0xf5, 0x01, 0xe1, 0x02, 0x4d, 0x08, 0x75,
	0xb1, 0xad, 0x1a, 0x3d, 0xa1, 0x03, 0x6b, 0x1a, 0x17, 0xe6, 0xec, 0x0f, 0x60, 0x8d, 0xb4, 0xf9
};

char ProfileXorMagic_PS4[] = {
	0xba, 0x0e, 0x86, 0x1d, 0x58, 0xe1, 0x92, 0x21, 0x30, 0xd6, 0xcb, 0xf0, 0xd0, 0x82, 0xd5, 0x58,
	0x36, 0x12, 0xe1, 0xf6, 0x39, 0x44, 0x88, 0xea, 0x4e, 0xfb, 0x04, 0x74, 0x07, 0x95, 0x3a, 0xa2
};

char PrefixMagic_PS4[] = {
	0xd1, 0x7b, 0xbf, 0x75, 0x4c, 0xc1, 0x80, 0x30, 0x37, 0x92, 0xbd, 0xd0, 0x18, 0x3e, 0x4a, 0x5f, 0x43,
	0xa2, 0x46, 0xa0, 0xed, 0xdb, 0x2d, 0x9f, 0x56, 0x5f, 0x8b, 0x3d, 0x6e, 0x73, 0xe6, 0xb8
};


char XorMagic_PS4[] = {
	0xfb, 0xfd, 0xfd, 0x51, 0x3a, 0x5c, 0xdb, 0x20, 0xbb, 0x5e, 0xc7, 0xaf, 0x66, 0x6f, 0xb6, 0x9a, 0x9a,
	0x52, 0x67, 0x0f, 0x19, 0x5d, 0xd3, 0x84, 0x15, 0x19, 0xc9, 0x4a, 0x79, 0x67, 0xda, 0x6d
};


size_t decryptSave(uint8_t* buffer, int offset, int length) {
	int i;
	char b;
	for(i = length - 1; i >= 0; i--) {
		if(i < 32) {
			b = PrefixMagic[i];
		}
		else {
			b = buffer[i - 32];
		}
		b ^= XorMagic[i % 32];
		buffer[i] ^= b;
	}
	return length;
}

size_t encryptSave(uint8_t* buffer, int offset, int length) {
	int i;
	char b;
	for(i = 0; i < length; i++) {
		if(i < 32) {
			b = PrefixMagic[i];
		}
		else {
			b = buffer[i - 32];
		}
		b ^= XorMagic[i % 32];
		buffer[i] ^= b;
	}
	return length;
}

size_t decryptProfile(uint8_t* buffer, int offset, int length) {
	int i;
	char b;
	for(i = length - 1; i >= 0; i--) {
		if(i < 32) {
			b = ProfilePrefixMagic[i];
		}
		else {
			b = buffer[i - 32];
		}
		b ^= ProfileXorMagic[i % 32];
		buffer[i] ^= b;
	}
	return length;
}

size_t encryptProfile(uint8_t* buffer, int offset, int length) {
	int i;
	char b;
	for(i = 0; i < length; i++) {
		if(i < 32) {
			b = ProfilePrefixMagic[i];
		}
		else {
			b = buffer[i - 32];
		}
		b ^= ProfileXorMagic[i % 32];
		buffer[i] ^= b;
	}
	return length;
}


size_t decryptSave_PS4(uint8_t* buffer, int offset, int length) {
	int i;
	char b;
	for(i = length - 1; i >= 0; i--) {
		if(i < 32) {
			b = PrefixMagic_PS4[i];
		}
		else {
			b = buffer[i - 32];
		}
		b ^= XorMagic_PS4[i % 32];
		buffer[i] ^= b;
	}
	return length;
}

size_t encryptSave_PS4(uint8_t* buffer, int offset, int length) {
	int i;
	char b;
	for(i = 0; i < length; i++) {
		if(i < 32) {
			b = PrefixMagic_PS4[i];
		}
		else {
			b = buffer[i - 32];
		}
		b ^= XorMagic_PS4[i % 32];
		buffer[i] ^= b;
	}
	return length;
}

size_t decryptProfile_PS4(uint8_t* buffer, int offset, int length) {
	int i;
	char b;
	for(i = length - 1; i >= 0; i--) {
		if(i < 32) {
			b = ProfilePrefixMagic_PS4[i];
		}
		else {
			b = buffer[i - 32];
		}
		b ^= ProfileXorMagic_PS4[i % 32];
		buffer[i] ^= b;
	}
	return length;
}

size_t encryptProfile_PS4(uint8_t* buffer, int offset, int length) {
	int i;
	char b;
	for(i = 0; i < length; i++) {
		if(i < 32) {
			b = ProfilePrefixMagic_PS4[i];
		}
		else {
			b = buffer[i - 32];
		}
		b ^= ProfileXorMagic_PS4[i % 32];
		buffer[i] ^= b;
	}
	return length;
}

// KLUDGE TO GET THIS TO COMPILE WITH THE WATCOM C COMPILER
struct Save save_t;
struct keyValuePair* kvp_t;
int payloadStart;
int processedLen;

void readSave(FILE* file, int fileType) {
	int i;
	printf("CSAV001RWS Reading file...\n");
	// The actual save.
	// Read it byte by byte.
	save_t.header = malloc(4);
	fread(save_t.header, sizeof(char), 4, file);
	fread(&save_t.sg_version, sizeof(int32_t), 1, file);
	fread(&save_t.pkg_version, sizeof(int32_t), 1, file);
	fread(&save_t.engine_major, sizeof(int16_t), 1, file);
	fread(&save_t.engine_minor, sizeof(int16_t), 1, file);
	fread(&save_t.engine_patch, sizeof(int16_t), 1, file);
	fread(&save_t.engine_build, sizeof(uint32_t), 1, file);
	fread(&save_t.build_id_length, sizeof(int32_t), 1, file);
	save_t.build_id = malloc(save_t.build_id_length);
	fread(save_t.build_id, sizeof(char), save_t.build_id_length, file);
	fread(&save_t.fmt_version, sizeof(int32_t), 1, file);
	fread(&save_t.fmt_count, sizeof(int32_t), 1, file);
	kvp_t = malloc(save_t.fmt_count * sizeof(struct keyValuePair));
	
	for(i = 0; i < save_t.fmt_count; i++) {
		kvp_t[i].guid = malloc(16);
		fread(kvp_t[i].guid, sizeof(char), 16, file);
		//printf("%d, ", ftell(file));
		fread(&kvp_t[i].entry, sizeof(int32_t), 1, file);
		//printf("%d, ", ftell(file));
	}
	//printf("%d, ", ftell(file));
	fread(&save_t.sg_type_len, sizeof(int32_t), 1, file);
	save_t.sg_type = malloc(save_t.sg_type_len);
	fread(save_t.sg_type, sizeof(char), save_t.sg_type_len, file);
	fread(&save_t.remaining_data_len, sizeof(int32_t), 1, file);
	payloadStart = ftell(file);
	save_t.remaining_data = malloc(save_t.remaining_data_len);
	fread(save_t.remaining_data, sizeof(char), save_t.remaining_data_len, file);

	printf("CSAV001RWS Save information:\n");
	printf("Header: %s\n", save_t.header);
	printf("SG version: %d\n", save_t.sg_version);
	printf("Package version: %d\n", save_t.pkg_version);
	printf("Engine version: %d.%d.%d\n", save_t.engine_major, save_t.engine_minor, save_t.engine_patch);
	printf("Build ID length: %d\n", save_t.build_id_length);
	printf("Build ID: %s\n", save_t.build_id);
	printf("Custom format version: %d\n", save_t.fmt_version);
	printf("Custom format count: %d\n", save_t.fmt_count);
	//for(i = 0; i < save_t.fmt_count; i++) {
	//	printf("Custom format %d: GUID: %x, entry %d\n", i, kvp_t[i].guid, kvp_t[i].entry);
	//}
	printf("Save type length: %d\n", save_t.sg_type_len);
	printf("Save type: %s\n", save_t.sg_type);
	printf("Payload start position: %d\n", payloadStart);
	printf("Payload length: %d\n", save_t.remaining_data_len);

	if(fileType == 1) {
		processedLen = decryptSave(save_t.remaining_data, 0, save_t.remaining_data_len);
	}
	else if(fileType == 2) {
		processedLen = decryptProfile(save_t.remaining_data, 0, save_t.remaining_data_len);
	}
	else if(fileType == 3) {
		processedLen = decryptSave_PS4(save_t.remaining_data, 0, save_t.remaining_data_len);
	}
	else if(fileType == 4) {
		processedLen = decryptProfile_PS4(save_t.remaining_data, 0, save_t.remaining_data_len);
	}
}

void writeSave(FILE* file, FILE* outFile, char* data, int32_t dataLen, int fileType) {
	int i;
	// 1. Load in an existing file as a template
	printf("CSAV001RWS Loading existing file...\n");
	save_t.header = malloc(4);
	fread(save_t.header, sizeof(char), 4, file);
	fread(&save_t.sg_version, sizeof(int32_t), 1, file);
	fread(&save_t.pkg_version, sizeof(int32_t), 1, file);
	fread(&save_t.engine_major, sizeof(int16_t), 1, file);
	fread(&save_t.engine_minor, sizeof(int16_t), 1, file);
	fread(&save_t.engine_patch, sizeof(int16_t), 1, file);
	fread(&save_t.engine_build, sizeof(uint32_t), 1, file);
	fread(&save_t.build_id_length, sizeof(int32_t), 1, file);
	save_t.build_id = malloc(save_t.build_id_length);
	fread(save_t.build_id, sizeof(char), save_t.build_id_length, file);
	fread(&save_t.fmt_version, sizeof(int32_t), 1, file);
	fread(&save_t.fmt_count, sizeof(int32_t), 1, file);
	kvp_t = malloc(save_t.fmt_count * sizeof(struct keyValuePair));
	for(i = 0; i < save_t.fmt_count; i++) {
		kvp_t[i].guid = malloc(16);
		fread(kvp_t[i].guid, sizeof(char), 16, file);
		fread(&kvp_t[i].entry, sizeof(int32_t), 1, file);
	}
	fread(&save_t.sg_type_len, sizeof(int32_t), 1, file);
	save_t.sg_type = malloc(save_t.sg_type_len);
	fread(save_t.sg_type, sizeof(char), save_t.sg_type_len, file);
	fread(&save_t.remaining_data_len, sizeof(int32_t), 1, file);
	payloadStart = ftell(file);
	save_t.remaining_data = malloc(save_t.remaining_data_len);
	fread(save_t.remaining_data, sizeof(char), save_t.remaining_data_len, file);

	// 3. Encrypt it
	if(fileType == 1) {
		processedLen = encryptSave(data, 0, dataLen);
	}
	else if(fileType == 2) {
		processedLen = encryptProfile(data, 0, dataLen);
	}
	else if(fileType == 3) {
		processedLen = encryptSave_PS4(data, 0, dataLen);
	}
	else if(fileType == 4) {
		processedLen = encryptProfile_PS4(data, 0, dataLen);
	}

	//printf("CSAV001RWS Encrypted payload length: %d\n", processedLen);
	printf("CSAV001RWS Original save information:\n");
	printf("Header: %s\n", save_t.header);
	printf("SG version: %d\n", save_t.sg_version);
	printf("Package version: %d\n", save_t.pkg_version);
	printf("Engine version: %d.%d.%d\n", save_t.engine_major, save_t.engine_minor, save_t.engine_patch);
	printf("Build ID length: %d\n", save_t.build_id_length);
	printf("Build ID: %s\n", save_t.build_id);
	printf("Custom format version: %d\n", save_t.fmt_version);
	printf("Custom format count: %d\n", save_t.fmt_count);
	//for(i = 0; i < save_t.fmt_count; i++) {
	//	printf("Custom format %d: GUID: %x, entry %d\n", i, kvp_t[i].guid, kvp_t[i].entry);
	//}
	printf("Save type length: %d\n", save_t.sg_type_len);
	printf("Save type: %s\n", save_t.sg_type);
	printf("Payload start position: %d\n", payloadStart);
	printf("Payload length: %d\n", save_t.remaining_data_len);



	// 4. Crank it out to a file and hope for the best! Protip: It's not the best!
	printf("CSAV001CNV Writing new file...\n");
	fwrite(save_t.header, sizeof(char), 4, outFile);
	fwrite(&save_t.sg_version, sizeof(int32_t), 1, outFile);
	fwrite(&save_t.pkg_version, sizeof(int32_t), 1, outFile);
	fwrite(&save_t.engine_major, sizeof(int16_t), 1, outFile);
	fwrite(&save_t.engine_minor, sizeof(int16_t), 1, outFile);
	fwrite(&save_t.engine_patch, sizeof(int16_t), 1, outFile);
	fwrite(&save_t.engine_build, sizeof(uint32_t), 1, outFile);
	fwrite(&save_t.build_id_length, sizeof(int32_t), 1, outFile);
	fwrite(save_t.build_id, sizeof(char), save_t.build_id_length, outFile);
	fwrite(&save_t.fmt_version, sizeof(int32_t), 1, outFile);
	fwrite(&save_t.fmt_count, sizeof(int32_t), 1, outFile);
	for(i = 0; i < save_t.fmt_count; i++) {
		fwrite(kvp_t[i].guid, sizeof(char), 16, outFile);
		fwrite(&kvp_t[i].entry, sizeof(int32_t), 1, outFile);
	}
	fwrite(&save_t.sg_type_len, sizeof(int32_t), 1, outFile);
	fwrite(save_t.sg_type, sizeof(char), save_t.sg_type_len, outFile);
	fwrite(&dataLen, sizeof(int32_t), 1, outFile);
	fwrite(data, sizeof(char), dataLen, outFile);
}


void readSaveHeader(FILE* file) {
	int i;
	printf("CSAV001RWS Reading file...\n");
	// The actual save.
	// Read it byte by byte.
	save_t.header = malloc(4);
	fread(save_t.header, sizeof(char), 4, file);
	fread(&save_t.sg_version, sizeof(int32_t), 1, file);
	fread(&save_t.pkg_version, sizeof(int32_t), 1, file);
	fread(&save_t.engine_major, sizeof(int16_t), 1, file);
	fread(&save_t.engine_minor, sizeof(int16_t), 1, file);
	fread(&save_t.engine_patch, sizeof(int16_t), 1, file);
	fread(&save_t.engine_build, sizeof(uint32_t), 1, file);
	fread(&save_t.build_id_length, sizeof(int32_t), 1, file);
	save_t.build_id = malloc(save_t.build_id_length);
	fread(save_t.build_id, sizeof(char), save_t.build_id_length, file);
	fread(&save_t.fmt_version, sizeof(int32_t), 1, file);
	fread(&save_t.fmt_count, sizeof(int32_t), 1, file);
	kvp_t = malloc(save_t.fmt_count * sizeof(struct keyValuePair));
	for(i = 0; i < save_t.fmt_count; i++) {
		kvp_t[i].guid = malloc(16);
		fread(kvp_t[i].guid, sizeof(char), 16, file);
		//printf("%d, ", ftell(file));
		fread(&kvp_t[i].entry, sizeof(int32_t), 1, file);
		//printf("%d, ", ftell(file));
	}
	//printf("%d, ", ftell(file));
	fread(&save_t.sg_type_len, sizeof(int32_t), 1, file);
	save_t.sg_type = malloc(save_t.sg_type_len);
	fread(save_t.sg_type, sizeof(char), save_t.sg_type_len, file);
	fread(&save_t.remaining_data_len, sizeof(int32_t), 1, file);
	payloadStart = ftell(file);
	save_t.remaining_data = malloc(save_t.remaining_data_len);
	fread(save_t.remaining_data, sizeof(char), save_t.remaining_data_len, file);

	printf("CSAV001RWS Save information:\n");
	printf("Header: %s\n", save_t.header);
	printf("SG version: %d\n", save_t.sg_version);
	printf("Package version: %d\n", save_t.pkg_version);
	printf("Engine version: %d.%d.%d\n", save_t.engine_major, save_t.engine_minor, save_t.engine_patch);
	printf("Build ID length: %d\n", save_t.build_id_length);
	printf("Build ID: %s\n", save_t.build_id);
	printf("Custom format version: %d\n", save_t.fmt_version);
	printf("Custom format count: %d\n", save_t.fmt_count);
	//for(i = 0; i < save_t.fmt_count; i++) {
	//	printf("Custom format %d: GUID: %x, entry %d\n", i, kvp_t[i].guid, kvp_t[i].entry);
	//}
	printf("Save type length: %d\n", save_t.sg_type_len);
	printf("Save type: %s\n", save_t.sg_type);
	printf("Payload start position: %d\n", payloadStart);
	printf("Payload length: %d\n", save_t.remaining_data_len);
}
