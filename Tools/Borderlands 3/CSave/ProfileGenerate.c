#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include "OakShared.pb-c.h"
#include "OakProfile.pb-c.h"
#include "OakSave.pb-c.h"
#include "FileTranslator.h"
#include "HelperVars.h"
#include "Customizations.h"

#define FILESIZE_LIMIT 9000000

int i;
int j;
int k;
int loopContinue = 1;
uint8_t fileBuffer[FILESIZE_LIMIT];
uint8_t* outBuffer;
OakSave__Profile* profData;
size_t writeLen;
OakSave__OakCustomizationSaveGameData* custs;
int32_t newGKeys;
int numICL;
OakSave__InventoryCategorySaveData** icl;
char* command;
FILE* inFile;
FILE* outFile;
int fileLen;
char* cutText;
int32_t level;
int32_t newTokens;
int32_t seed;
int32_t id;
int found;
int numTokens;
OakSave__VaultCardSaveGameData* vcData;
int numVcPrevs;
OakSave__VaultCardPreviousChallenge** vcPrev;
int numVcRewards;
OakSave__VaultCardRewardList** vcRewards;
int numVcRewardsCurrent;
OakSave__VaultCardReward** vcRewardCurrent;

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
	profData = oak_save__profile__unpack(NULL, fileLen, fileBuffer);

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
		else if(strcmp("set goldenkeys\n", command) == 0) {
			icl = profData->bank_inventory_category_list;
			numICL = profData->n_bank_inventory_category_list;
			printf("CSAV001IMM How many golden keys do you want?\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			newGKeys = atoi(command);
			for(i = 0; i < numICL; i++) {
				if(icl[i]->base_category_definition_hash == currencyHashes[2]) {
					icl[i]->quantity = newGKeys;
				}
			}
			printf("CSAV001IMM Golden keys updated\n");
		}
		else if(strcmp("unlock all\n", command) == 0) {
			printf("CSAV001IMM Have you legit purchased all cosmetics?\n*Input\n");
			fgets(command, 1024, stdin);
			if(command[0] == 'y') {
				printf("CSAV001IMM Unlocking all customizations...\n");
				// 0. fool save file
				profData->n_unlocked_customizations = numAllAssets;
				// 1. allocate space for everything
				custs = malloc(sizeof(OakSave__OakCustomizationSaveGameData) * numAllAssets);
				// 2. copy them in
				for(i = 0; i < numAllAssets; i++) {
					custs[0].customization_asset_path = allAssetPaths[i];
				}
				// 3. store value
				//profData->unlocked_customizations = custs;
			}
		}
		else if(strcmp("set gtokens\n", command) == 0) {
			printf("CSAV001IMM Specify how many tokens you want\n*Input\n");
			fgets(command, 1024, stdin);
			newTokens = atoi(command);
			profData->guardian_rank->available_tokens = newTokens;
		}
		else if(strcmp("set grank\n", command) == 0) {
			printf("CSAV001IMM Specify guardian rank level\n*Input\n");
			fgets(command, 1024, stdin);
			level = atoi(command);
			profData->guardian_rank->guardian_rank = level;
		}
		else if(strcmp("set gexp\n", command) == 0) {
			printf("CSAV001IMM Specify guardian rank experience\n*Input\n");
			fgets(command, 1024, stdin);
			level = atoi(command);
			profData->guardian_rank->guardian_experience = level;
		}
		else if(strcmp("set gseed\n", command) == 0) {
			printf("CSAV001IMM Specify guardian rank random speed (integer form please)\n*Input\n");
			fgets(command, 1024, stdin);
			seed = atoi(command);
			profData->guardian_rank->guardian_reward_random_seed = seed;
		}
		else if(strcmp("set gnewexp\n", command) == 0) {
			printf("CSAV001IMM Specify new guardian rank experience\n*Input\n");
			fgets(command, 1024, stdin);
			level = atoi(command);
			profData->guardian_rank->new_guardian_experience = level;
		}
		else if(strcmp("set greward\n", command) == 0) {
			printf("CSAV001IMM Specify class path of reward\n*Input\n");
			fgets(command, 1024, stdin);
			cutText = malloc(strlen(command) - 1);
			strncpy(cutText, command, (strlen(command) - 1));
			cutText[strlen(command) - 1] = '\0';
			found = 0;
			for(i = 0; i < profData->guardian_rank->n_rank_rewards; i++) {
				if(strcmp(profData->guardian_rank->rank_rewards[i]->reward_data_path, cutText) == 0) {
					printf("CSAV001IMM Found\n");
					printf("CSAV001IMM Enter number of tokens for reward\n*Input\n");
					fgets(command, 1024, stdin);
					numTokens = atoi(command);
					profData->guardian_rank->rank_rewards[i]->num_tokens = numTokens;
				}
			}
			if(found == 0) {
				printf("CSAV001IMM Not found\n");
			}
		}
		else if(strcmp("set vckeys\n", command) == 0) {
                        icl = profData->bank_inventory_category_list;
                        numICL = profData->n_bank_inventory_category_list;
                        printf("CSAV001IMM How many Vault Card keys do you want?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        newGKeys = atoi(command);
                        for(i = 0; i < numICL; i++) {
                                if(icl[i]->base_category_definition_hash == currencyHashes[3]) {
                                        icl[i]->quantity = newGKeys;
                                }
                        }
                        printf("CSAV001IMM Vault Card keys updated\n");
                }
		else if(strcmp("set diamondkeys\n", command) == 0) {
                        icl = profData->bank_inventory_category_list;
                        numICL = profData->n_bank_inventory_category_list;
                        printf("CSAV001IMM How many diamond keys do you want?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        newGKeys = atoi(command);
                        for(i = 0; i < numICL; i++) {
                                if(icl[i]->base_category_definition_hash == currencyHashes[4]) {
                                        icl[i]->quantity = newGKeys;
                                }
                        }
                        printf("CSAV001IMM Diamond keys updated\n");
                }
		else if(strcmp("set vcid\n", command) == 0) {
			vcData = profData->vault_card;
			printf("CSAV001IMM What Vault Card do you want to make active?\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			id = atoi(command);
			vcData->last_active_vault_card_id = id;
			printf("CSAV001IMM Updated.\n");
		}
		else if(strcmp("set vcdayseed\n", command) == 0) {
			vcData = profData->vault_card;
			printf("CSAV001IMM Please specify the new Vault Card seed for today\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			seed = atoi(command);
			vcData->current_day_seed = seed;
			printf("CSAV001IMM Updated.\n");
		}
		else if(strcmp("set vcweekseed\n", command) == 0) {
                        vcData = profData->vault_card;
                        printf("CSAV001IMM Please specify the new Vault Card seed for this week\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        seed = atoi(command);
                        vcData->current_week_seed = seed;
                        printf("CSAV001IMM Updated.\n");
                }
		else if(strcmp("set vcrewardcardid\n", command) == 0) {
			vcData = profData->vault_card;
			vcRewards = vcData->vault_card_claimed_rewards;
        		numVcRewards = vcData->n_vault_card_claimed_rewards;
			printf("CSAV001WNG Warning! This is a potentially dangerous command. Use with caution.\n");
			printf("CSAV001IMM What card reward are you modifying?\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			i = atoi(command);
			printf("CSAV001IMM What do you want to set the ID to?\n");
			printf("*Input\n");
			fgets(command, 1024, stdin);
			id = atoi(command);
			vcRewards[i]->vault_card_id = id;
			printf("CSAV001IMM Updated.\n");
		}
		else if(strcmp("set vcexp\n", command) == 0) {
                        vcData = profData->vault_card;
                        vcRewards = vcData->vault_card_claimed_rewards;
                        numVcRewards = vcData->n_vault_card_claimed_rewards;
                        printf("CSAV001IMM What card reward are you modifying?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        i = atoi(command);
                        printf("CSAV001IMM What do you want to set the experience to?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        vcRewards[i]->vault_card_experience = atoi(command);
                        printf("CSAV001IMM Updated.\n");
                }
		else if(strcmp("set vcchests\n", command) == 0) {
                        vcData = profData->vault_card;
                        vcRewards = vcData->vault_card_claimed_rewards;
                        numVcRewards = vcData->n_vault_card_claimed_rewards;
                        printf("CSAV001IMM What card reward are you modifying?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        i = atoi(command);
                        printf("CSAV001IMM How many openable chests do you want?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        vcRewards[i]->vault_card_chests = atoi(command);
                        printf("CSAV001IMM Updated.\n");
                }
		else if(strcmp("set vcchestsopened\n", command) == 0) {
                        vcData = profData->vault_card;
                        vcRewards = vcData->vault_card_claimed_rewards;
                        numVcRewards = vcData->n_vault_card_claimed_rewards;
                        printf("CSAV001IMM What card reward are you modifying?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        i = atoi(command);
                        printf("CSAV001IMM How many chests do you want to have opened?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        vcRewards[i]->vault_card_chests_opened = atoi(command);
                        printf("CSAV001IMM Updated.\n");
                }
		else if(strcmp("set vcusedkeys\n", command) == 0) {
                        vcData = profData->vault_card;
                        vcRewards = vcData->vault_card_claimed_rewards;
                        numVcRewards = vcData->n_vault_card_claimed_rewards;
                        printf("CSAV001IMM What card reward are you modifying?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        i = atoi(command);
                        printf("CSAV001IMM How many spent keys do you want?\n");
                        printf("*Input\n");
                        fgets(command, 1024, stdin);
                        vcRewards[i]->vault_card_keys_spent = atoi(command);
                        printf("CSAV001IMM Updated.\n");
                }
		else {
			printf("CSAV001IMM Invalid command...\n");
		}
	}

// -------------------------- End main loop --------------------------


// Get packed size, allocate output buffer, pack the protobuf, and write it to a file
	writeLen = oak_save__profile__get_packed_size(profData);
	outBuffer = malloc(writeLen);
	oak_save__profile__pack(profData, outBuffer);
	printf("CSAV001END Writing output file...\n");
	fwrite(outBuffer, writeLen, 1, outFile);
	free(outBuffer);
	return 0;
}
