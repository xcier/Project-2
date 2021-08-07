#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include "OakShared.pb-c.h"
#include "OakSave.pb-c.h"
#include "FileTranslator.h"
#include "HelperVars.h"

#define FILESIZE_LIMIT 9000000

/* Common loop var defs to save memory */
int i;
int j;
int k;
int loopContinue = 1;

/* The file data buffer */
uint8_t fileBuffer[FILESIZE_LIMIT];
uint8_t* outBuffer;

/* The character data itself */
OakSave__Character* charData;

/* File-related properties */
FILE* inFile;
FILE* outFile;
int fileLen;

/* Current command */
char* command;

/* Related to string looping and processing */
size_t writeLen;
int found = 0;
char* cutText;

/* Game data */
OakSave__ChallengeSaveGameData** challenge_data;
size_t n_challenge_data;
int newState;
int choice;
int missionDFPLen;
OakSave__MissionStatusPlayerSaveGameData** missionDataForPlaythrough;
int missionDataLen;
OakSave__MissionPlaythroughSaveGameData** missionData;
int newSDUValue;
int sduDataSize;
OakSave__OakSDUSaveGameData** sduData;
size_t writeLenCmd;
int32_t newPoints;
OakSave__OakPlayerAbilitySaveGameData* tree;
int32_t newEridium;
int numICL;
OakSave__InventoryCategorySaveData** icl;
int xpLevel;
int32_t newEXPointsCount;
int playthrough;
int sgDataLen;
OakSave__GameStateSaveData** sgData;
uint32_t newMHLevel;
int32_t newMoney;



int main(int argc, char** argv) {
	if(argc < 3) {
		printf("CSAV001ABD Missing filenames (specify input file and output file)\n");
		exit(1);
	}
	if(strcmp(argv[1], argv[2]) == 0) {
		printf("CSAV001ABD The input and output files cannot be the same.\n");
		exit(1);
	}

// Open input and output files
	
	inFile = fopen(argv[1], "r");
	outFile = fopen(argv[2], "w");
	if(inFile == NULL) {
		printf("CSAV001ABD Failed to open input file\n");
		exit(1);
	}
	if(outFile == NULL) {
		printf("CSAV001ABD Failed to open output file\n");
		exit(1);
	}
	fileLen = read_buffer(FILESIZE_LIMIT, fileBuffer, inFile);

// Print the welcome message
	printf("CSAV00100I Borderlands 3 CSave\n");
	printf("CSAV00100I by HackerSmacker\n");
	printf("CSAV00100S Save file size = %d\n", fileLen);

// Define the object, and read the data from the buffer (i.e. unpack it)
	charData = oak_save__character__unpack(NULL, fileLen, fileBuffer);

// Get some basic info about the save file.
	printf("CSAV001GEN Name: %s\n", charData->preferred_character_name);	
	printf("CSAV001GEN Save game identifier: %lu\n", charData->save_game_id);
	printf("CSAV001GEN Last save timestamp: %lu\n", charData->last_save_timestamp);
	printf("CSAV001GEN Total time played, in seconds: %lu\n", charData->time_played_seconds);
	printf("CSAV001GEN Playthroughs completed: %d\n", charData->playthroughs_completed);
	printf("CSAV001GEN Save GUID: %s\n", charData->save_game_guid);

// -------------------- Immediate mode main loop ---------------------
	command = malloc(1024);
	printf("CSAV001IMM Execution begins...\n");
	while (loopContinue == 1) {
		printf("*Go\n");
		fgets(command, 1024, stdin);
		if((strcmp("quit\n", command) == 0) | (strcmp("exit\n", command) == 0)) {
			printf("CSAV001IMM Done\n");
			break;
		}
		else if(strcmp("help\n", command) == 0) {
			printf("CSAV001IMM I guess you could say there's no help for the wicked\n");
		}
		else if(strcmp("set name\n", command) == 0) {
			printf("CSAV001IMM Specify new name now...\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			cutText = malloc(strlen(command) - 1);
			strncpy(cutText, command, (strlen(command) - 1));
			cutText[strlen(command) - 1] = '\0';
			charData->preferred_character_name = cutText;
			printf("CSAV001IMM Name set complete\n");
		}
		else if(strcmp("set mayhemlevel\n", command) == 0) {
			printf("CSAV001IMM Specify new Mayhem level now (0-10)...\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			newMHLevel = atoi(command);
			sgData = charData->game_state_save_data_for_playthrough;
			sgDataLen = charData->n_game_state_save_data_for_playthrough;
			printf("CSAV001IMM Enter playthrough to modify\n*Input\n");
			fgets(command, 1024, stdin);
			playthrough = atoi(command);
			sgData[playthrough]->mayhem_level = newMHLevel;
			printf("CSAV001IMM Mayhem level updated\n");
		}
		else if(strcmp("set expoints\n", command) == 0) {
			printf("CSAV001IMM Specify number of experience points...\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			newEXPointsCount = atoi(command);
			charData->experience_points = newEXPointsCount;
			printf("CSAV001IMM Experience point counter updated\n");
		}
		else if(strcmp("set level\n", command) == 0) {
			printf("CSAV001IMM Enter new level\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			xpLevel = atoi(command);
			charData->experience_points = levelToXP[xpLevel];
			printf("CSAV001IMM Level set and XP counter updated\n");
		}
		else if(strcmp("set guardianrank\n", command) == 0) {
			printf("CSAV001FNI Feature not implemented. Please contact the support center for a PTF.\n");
		}
		else if(strcmp("set money\n", command) == 0) {
			icl = charData->inventory_category_list;
			numICL = charData->n_inventory_category_list;
			printf("CSAV001IMM Enter how much money you want\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			newMoney = atoi(command);
			for(i = 0; i < numICL; i++) {
				if(icl[i]->base_category_definition_hash == currencyHashes[0]) {
					icl[i]->quantity = newMoney;
				}
			}
			printf("CSAV001IMM Money updated\n");
		}
		else if(strcmp("set eridium\n", command) == 0) {
			icl = charData->inventory_category_list;
			numICL = charData->n_inventory_category_list;
			printf("CSAV001IMM Enter how much Eridium you want\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			newEridium = atoi(command);
			for(i = 0; i < numICL; i++) {
				if(icl[i]->base_category_definition_hash == currencyHashes[1]) {
					icl[i]->quantity = newEridium;
				}
			}
			printf("CSAV001IMM Eridium updated\n");

		}
		else if(strcmp("unlock skilltree\n", command) == 0) {
			tree = charData->ability_data;
			printf("CSAV001IMM Unlocking skill tree...\n");
			tree->tree_grade = 2;
			printf("CSAV001IMM Tree unlocked\n");	
		}
		else if(strcmp("set skillpoints\n", command) == 0) {
			tree = charData->ability_data;
			printf("CSAV001IMM Enter how many skill points you want\n*Input\n");
			fgets(command, 1024, stdin);
			newPoints = atoi(command);
			tree->ability_points = newPoints;
			printf("CSAV001IMM Skill points set\n");
		}
		else if(strcmp("xyzzy\n", command) == 0) {
			printf("CSAV001IMM Nothing happens\n");
		}
		else if((strcmp("save\n", command) == 0) | (strcmp("write\n", command) == 0)) {
			writeLenCmd = oak_save__character__get_packed_size(charData);
			outBuffer = malloc(writeLenCmd);
			oak_save__character__pack(charData, outBuffer);
			printf("CSAV001END Writing output file...\n");
			fwrite(outBuffer, writeLenCmd, 1, outFile);
			free(outBuffer);
		}
		else if(strcmp("set class\n", command) == 0) {
			printf("CSAV001IMM Specify class now, read manual for input format\n*Input\n");
			fgets(command, 1024, stdin);
			choice = atoi(command);
			charData->player_class_data->player_class_path = playerClassToObject[choice];
			printf("CSAV001IMM Player class updated\n");
		}
		else if(strcmp("set sdu\n", command) == 0) {
			sduData = charData->sdu_list;
        	sduDataSize = charData->n_sdu_list;
			printf("CSAV001IMM Starting SDU list\n");
			for(i = 0; i < sduDataSize; i++) {
				printf("CSAV001IMM Enter new value for SDU %s\n*Input (RETURN for default)\n", sduData[i]->sdu_data_path);
				fgets(command, 1024, stdin);
				if(strcmp(command, "\n") == 0) {
					newSDUValue = sduData[i]->sdu_level;
				}
				else { 
					newSDUValue = atoi(command);
				}
				sduData[i]->sdu_level = newSDUValue;
			}
			printf("CSAV001IMM SDU edits complete\n");
		}
		else if(strcmp("set quest\n", command) == 0) {
			printf("CSAV001IMM Enter quest path name\n*Input\n");
			fgets(command, 1024, stdin);
			cutText = malloc(strlen(command) - 1);
			strncpy(cutText, command, (strlen(command) - 1));
			//cutText[strlen(command) - 1] = '\0';
			missionData = charData->mission_playthroughs_data;
			missionDataLen = charData->n_mission_playthroughs_data;
			printf("CSAV001IMM Which playthrough to search on?\n*Input\n");
			fgets(command, 1024, stdin);
			i = atoi(command);
			missionDataForPlaythrough = missionData[i]->mission_list;
			missionDFPLen = missionData[i]->n_mission_list;
			printf("CSAV001IMM Searching for %s\n", cutText);
			for(j = 0; j < missionDFPLen; j++) {
				if((strcmp(missionDataForPlaythrough[j]->mission_class_path, cutText) == 0) && (found == 0)) {
					found = 1;
					printf("CSAV001IMM Found quest. Enter state (consult manual for input type):\n*Input\n");
					fgets(command, 1024, stdin);
					newState = atoi(command);
					missionDataForPlaythrough[i]->status = newState;
					printf("CSAV001IMM Do you want to change individual mission states too? (1 for yes and 2 for no)\n*Input\n");
					fgets(command, 1024, stdin);
					choice = atoi(command);
					if(choice == 1) {
						printf("CSAV001IMM There are %d objectives/mission states.\n", missionDataForPlaythrough[j]->n_objectives_progress);
						for(k = 0; k < missionDataForPlaythrough[j]->n_objectives_progress; k++) {
							printf("CSAV001IMM Enter state for objective %d\n*Input\n", k);
							fgets(command, 1024, stdin);
							missionDataForPlaythrough[j]->objectives_progress[k] = atoi(command);
						}
					}
				}
			}
			if(found == 0) {
				printf("CSAV001IMM Quest not found.\n");
			}
		}
		else if(strcmp("set challenge\n", command) == 0) {
			challenge_data = charData->challenge_data;
			n_challenge_data = charData->n_challenge_data;
			printf("CSAV001IMM Enter challenge name/class path\n*Input\n");
			fgets(command, 1024, stdin);
			cutText = malloc(strlen(command) - 1);
			strncpy(cutText, command, (strlen(command) - 1));
			//cutText[strlen(command) - 1] = '\0';
			for(i = 0; i < n_challenge_data; i++) {
				//printf("%s\n", challenge_data[i]->challenge_class_path);
				if((strstr(cutText, challenge_data[i]->challenge_class_path) != NULL) & (found == 0)) {
					found = 1;
					printf("CSAV001IMM Found challenge. Enter completion state (0 for no and 1 for yes)\n*Input\n");
					fgets(command, 1024, stdin);
					newState = atoi(command);
					challenge_data[i]->currently_completed = newState;
					printf("CSAV001IMM Updated to %d\n", challenge_data[i]->currently_completed);
				}
			}
			if(found == 0) {
				printf("CSAV001IMM Challenge not found.\n");
			}
		}
		else if(strcmp("set leagueid\n", command) == 0) {
			printf("CSAV001IMM What league ID do you want to activate?\n*Input\n");
			fgets(command, 1024, stdin);
			charData->last_active_league = atoi(command);
			printf("CSAV001IMM Updated to %d\n", charData->last_active_league);
		}
		else if(strcmp("set leagueinst\n", command) == 0) {
                        printf("CSAV001IMM What league instance do you want to activate?\n*Input\n");
                        fgets(command, 1024, stdin);
                        charData->last_active_league_instance = atoi(command);
                        printf("CSAV001IMM Updated to %d\n", charData->last_active_league_instance);
                }


		else {
			printf("CSAV001ERR Invalid command...\n");
		}
	}

// -------------------------- End main loop --------------------------


// Get packed size, allocate output buffer, pack the protobuf, and write it to a file
	writeLen = oak_save__character__get_packed_size(charData);
	outBuffer = malloc(writeLen);
	oak_save__character__pack(charData, outBuffer);
	printf("CSAV001END Writing output file...\n");
	fwrite(outBuffer, writeLen, 1, outFile);
	free(outBuffer);
	return 0;
}
