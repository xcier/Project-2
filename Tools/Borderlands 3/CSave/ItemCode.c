#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "OakShared.pb-c.h"
#include "OakSave.pb-c.h"
#include "OakProfile.pb-c.h"
#include "ItemCode.h"

#ifndef PREFIX
#define PREFIX ./
#endif

/*

A general explanation of what's going on here:
1. You have an array of filenames that point to required dist files.
2. These files contain lines of text that map the element number in the item serial
   to an object. The usefulness of this is debatable.
3. You first have to find what number lookup table you're after. There's a spiffy function
   to automate this.
4. After you figure out what table you need to search, search it and pull out what value
   you actually need.

*/


// File descriptors for lookup tables
FILE** lookupTableFiles;

// Array of strings containing all that good stuff
// Explanation:
// X, Y, Z. X is the current table, Y is the line, and Z is the character.
char lookupTable[50][500][2000];

// Number of LT files (this value is hardcoded):
int lookupTableCount = 48;

// Filenames to lookup tables
const char lookupTableFilenames[50][256] = {
	"LookupTables/BPInvPart_AR_COV_C.txt",
	"LookupTables/BPInvPart_AR_DAL_C.txt",
	"LookupTables/BPInvPart_AR_TOR_C.txt",
	"LookupTables/BPInvPart_Artifact_C.txt",
	"LookupTables/BPInvPart_ATL_AR_C.txt",
	"LookupTables/BPInvPart_ATL_HW_C.txt",
	"LookupTables/BPInvPart_ClassMod_C.txt",
	"LookupTables/BPInvPart_Customization_Head_C.txt",
	"LookupTables/BPInvPart_Customization_Skin_C.txt",
	"LookupTables/BPInvPart_Dahl_SMG_C.txt",
	"LookupTables/BPInvPart_GrenadeMod_C.txt",
	"LookupTables/BPInvPart_HW_COV_C.txt",
	"LookupTables/BPInvPart_HW_TOR_C.txt",
	"LookupTables/BPInvPart_HW_VLA_C.txt",
	"LookupTables/BPInvPart_Hyperion_Shotgun_C.txt",
	"LookupTables/BPInvPart_JAK_AR_C.txt",
	"LookupTables/BPInvPart_Jakobs_Pistol_C.txt",
	"LookupTables/BPInvPart_MAL_SR_C.txt",
	"LookupTables/BPInvPart_Maliwan_SMG_C.txt",
	"LookupTables/BPInvPart_PS_ATL_C.txt",
	"LookupTables/BPInvPart_PS_COV_C.txt",
	"LookupTables/BPInvPart_PS_DAL_C.txt",
	"LookupTables/BPInvPart_PS_MAL_C.txt",
	"LookupTables/BPInvPart_PS_TOR_C.txt",
	"LookupTables/BPInvPart_PS_VLA_C.txt",
	"LookupTables/BPInvPart_SG_JAK_C.txt",
	"LookupTables/BPInvPart_SG_MAL_C.txt",
	"LookupTables/BPInvPart_SG_TED_C.txt",
	"LookupTables/BPInvPart_SG_Torgue_C.txt",
	"LookupTables/BPInvPart_Shield_C.txt",
	"LookupTables/BPInvPart_SM_Hyperion_C.txt",
	"LookupTables/BPInvPart_SM_TED_C.txt",
	"LookupTables/BPInvPart_SR_DAL_C.txt",
	"LookupTables/BPInvPart_SR_HYP_C.txt",
	"LookupTables/BPInvPart_SR_JAK_C.txt",
	"LookupTables/BPInvPart_Tediore_Pistol_C.txt",
	"LookupTables/BPInvPart_VLA_AR_C.txt",
	"LookupTables/BPInvPart_VLA_SR_C.txt",
	"LookupTables/BPInvPartData_EridianFabricator_C.txt",
	"LookupTables/BPVehiclePart_C.txt",
	"LookupTables/DownloadableEntitlementPartData.txt",
	"LookupTables/InventoryBalanceData.txt",
	"LookupTables/InventoryCustomizationPartData.txt",
	"LookupTables/InventoryData.txt",
	"LookupTables/InventoryGenericPartData.txt",
	"LookupTables/ItemPoolData.txt",
	"LookupTables/ManufacturerData.txt",
	"LookupTables/OakDownloadableContentLicenseData.txt"
};

const char lookupTableIndex[50][256] = {
	"BPInvPart_AR_COV_C.txt",
	"BPInvPart_AR_DAL_C.txt",
	"BPInvPart_AR_TOR_C.txt",
	"BPInvPart_Artifact_C.txt",
	"BPInvPart_ATL_AR_C.txt",
	"BPInvPart_ATL_HW_C.txt",
	"BPInvPart_ClassMod_C.txt",
	"BPInvPart_Customization_Head_C.txt",
	"BPInvPart_Customization_Skin_C.txt",
	"BPInvPart_Dahl_SMG_C.txt",
	"BPInvPart_GrenadeMod_C.txt",
	"BPInvPart_HW_COV_C.txt",
	"BPInvPart_HW_TOR_C.txt",
	"BPInvPart_HW_VLA_C.txt",
	"BPInvPart_Hyperion_Shotgun_C.txt",
	"BPInvPart_JAK_AR_C.txt",
	"BPInvPart_Jakobs_Pistol_C.txt",
	"BPInvPart_MAL_SR_C.txt",
	"BPInvPart_Maliwan_SMG_C.txt",
	"BPInvPart_PS_ATL_C.txt",
	"BPInvPart_PS_COV_C.txt",
	"BPInvPart_PS_DAL_C.txt",
	"BPInvPart_PS_MAL_C.txt",
	"BPInvPart_PS_TOR_C.txt",
	"BPInvPart_PS_VLA_C.txt",
	"BPInvPart_SG_JAK_C.txt",
	"BPInvPart_SG_MAL_C.txt",
	"BPInvPart_SG_TED_C.txt",
	"BPInvPart_SG_Torgue_C.txt",
	"BPInvPart_Shield_C.txt",
	"BPInvPart_SM_Hyperion_C.txt",
	"BPInvPart_SM_TED_C.txt",
	"BPInvPart_SR_DAL_C.txt",
	"BPInvPart_SR_HYP_C.txt",
	"BPInvPart_SR_JAK_C.txt",
	"BPInvPart_Tediore_Pistol_C.txt",
	"BPInvPart_VLA_AR_C.txt",
	"BPInvPart_VLA_SR_C.txt",
	"BPInvPartData_EridianFabricator_C.txt",
	"BPVehiclePart_C.txt",
	"DownloadableEntitlementPartData.txt",
	"InventoryBalanceData.txt",
	"InventoryCustomizationPartData.txt",
	"InventoryData.txt",
	"InventoryGenericPartData.txt",
	"ItemPoolData.txt",
	"ManufacturerData.txt",
	"OakDownloadableContentLicenseData.txt"
};
uint8_t currentByte = 0;
int dataLen;
uint8_t* out;

// de-XOR the save file.
uint8_t* xorSaveData(uint8_t* data, uint8_t seed) {
	int i;
	dataLen = strlen(data);
	out = malloc(dataLen);
	if(seed == 0) {
		strcpy(out, data);
	}
	for(i = 0; i < dataLen; i++) {
		currentByte = (seed >> 5) & 0xFFFFFFFF;
		currentByte = ((currentByte * 0x10A860C1) % 0xFFFFFFFB);
		out[i] = ((data[i] ^ currentByte) & 0xFF);
	}
	return out;
}


uint32_t xorMaskItself;
uint8_t* temp;

// de-XOR an item serial.
uint8_t* xorItemSerialData(uint8_t* data, uint32_t seed, int len) {
	int i;
	xorMaskItself = (seed >> 5) & 0xFFFFFFFF;
	temp = malloc(len);
	if(seed == 0) {
		return data;
	}
	for(i = 0; i < len; i++) {
		xorMaskItself = (xorMaskItself * 0x10A860C1) % 0xFFFFFFFB;
		temp[i] = ((data[i] ^ xorMaskItself) & 0xFF);
	}
	return temp;
}

uint8_t* data;
int len;
uint8_t magicNumber;
uint32_t xorSeed;
int xorDataLen;
uint8_t* xorData;
uint8_t* decryptedData;

// Print out info about a serial to the console.
void dumpSerial(ProtobufCBinaryData item_serial_number) {
	int i;
	// The actual data and the length.
	data = item_serial_number.data;
	len = item_serial_number.len;
	// Print out the data, char by char.
	printf("CSAV001INV Parsing serial ");
	for(i = 0; i < len; i++) {
		printf("%x", data[i]);
	}
	printf("\n");
	// Done printing; get the magic number and make sure it's 1 - removed because this is dumb
	magicNumber = data[0];
	// Do some shifts to obtain the XOR seed. Keep in mind this code won't work on big-endian machines (so no SGI machines).
	xorSeed = data[1] | (data[2] << 8) | (data[3] << 8) | (data[4] << 8);
	printf("CSAV001INV XOR seed for this item: %x\n", xorSeed);
	// Take off 5 bytes for the magic number and seed, the rest is the XOR'd data.
	xorDataLen = len - 5;
	xorData = malloc(len - 5);
	// Copy the rest of the serial to the buffer so it can be de-XOR'd.
	memcpy(xorData, data + 5, xorDataLen);
	// Call the un-XOR function.
	decryptedData = xorItemSerialData(xorData, xorSeed, xorDataLen);
	// Print out the encrypted and decrypted data
	printf("CSAV001INV Payload length: %d\n", xorDataLen);
	printf("CSAV001INV Data encrypted: ");
	for(i = 0; i < xorDataLen; i++) {
		printf("%x", xorData[i]);
	}
	printf("\n");
	printf("CSAV001INV Data decrypted: ");
	for(i = 0; i < xorDataLen; i++) {
		printf("%x", decryptedData[i]);
	}
	printf("\n");

}


char line[2048];

// Load the lookup tables into memory.
void loadLookupTables() {
	int i;
	int j, k;
	// Define variables
	// Allocate space for some FILEs
	lookupTableFiles = malloc(sizeof(FILE*) * lookupTableCount);
	// Print messages
	printf("CSAV001FIL Loading lookup tables... will load %d files.\n", lookupTableCount);
	// Iterate through each file...
	for(i = 1; i < lookupTableCount; i++) {
		// ...print out a message to the user...
		printf("CSAV001FIL Loading file %d: %s\n", i, lookupTableFilenames[i]);
		// ...open the file...
		lookupTableFiles[i] = fopen(lookupTableFilenames[i], "r");
		// ...make sure it actually did.
		if(lookupTableFiles[i] == NULL) {
			fprintf(stderr, "CSAV001FIL FATAL PROCESSING ERROR WHEN OPENING FILE %s\n. EXECUTION MAY NOT CONTINUE.\n", lookupTableFilenames[i]);
		}
		// Now, read the file:
		// j is the line indicator, i is the file number
		j = 0;
		while (fgets(line, sizeof(line), lookupTableFiles[i])) {
			strtok(line, "\n");
			//printf("%s\n", line);
			strcpy(lookupTable[i][j], line);
			//printf("%s\n", lookupTable[i][j]);
			j++;
		}
    	}
	printf("CSAV001FIL Lookup table load complete\n");
}

// Function to get a value from the lookup table without using extern char*** lookupTable
// This is for decoding item serials
char* lookupInTable(int tableIndex, int lineNumber) {
	return lookupTable[tableIndex][lineNumber];
}

// Find something in a table. AKA the line number in a table file.
// This is for generating item serials
int findInTable(int tableIndex, char* searchText) {
	int i;
	// 500 is the arbitrary max... this is horrifically dangerous
	for(i = 0; i < 500; i++) {
		if(strcmp(searchText, lookupTable[tableIndex][i]) == 0) {
			return i;
		}
	}
}

// Find a lookup table's index.
int findLookupTable(char* searchText) {
	int i;
	for(i = 0; i < lookupTableCount; i++) {
		if(strcmp(searchText, lookupTableIndex[i]) == 0) {
			return i;
		}
		else {
			return -1;
		}
	}
}


struct Item parseItemCode(size_t length, uint8_t* data, int outcome) {

}
