#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include "ItemCode.h"
#include "OakShared.pb-c.h"
#include "OakSave.pb-c.h"

int loopContinue;
char command[1024];
int table;
int item;


int main() {
	loopContinue = 1;
	
	printf("CSAV001ILT Item Lookup Test Program\n");
	loadLookupTables();
	printf("CSAV001ILT ^^^ If any errors occurred in the above process, stop the process or cancel the job now please.\n");
	while(loopContinue == 1) {
		printf("*Go\n");
		fgets(command, 1024, stdin);
		if(strcmp(command, "findtable\n") == 0) {
			printf("CSAV001ILT What table do you want to find?\n*Input\n");
			fgets(command, 1024, stdin);
			strtok(command, "\n");
			printf("CSAV001ILT Searching for %s\n", command);
			printf("CSAV001ILT Table number: %d\n", findLookupTable(command));
		}
		else if(strcmp(command, "getindex\n") == 0) {
			printf("CSAV001ILT Enter the table index you want to pull from:\n*Input\n");
			fgets(command, 1024, stdin);
			strtok(command, "\n");
			table = atoi(command);
			printf("CSAV001ILT Enter item index/number:\n*Input\n");
			fgets(command, 1024, stdin);
			strtok(command, "\n");
			item = atoi(command);
			printf("CSAV001ILT Result: %s\n", lookupInTable(table, item));
		}
		else if(strcmp(command, "findindex\n") == 0) {
			printf("CSAV001ILT Enter the table index you want to search:\n*Input\n");
			fgets(command, 1024, stdin);
			strtok(command, "\n");
			table = atoi(command);
			printf("CSAV001ILT Enter the search query:\n*Input\n");
			fgets(command, 1024, stdin);
			strtok(command, "\n");
			printf("CSAV001ILT Searching for %s\n", command);
			printf("CSAV001ILT Result: %d\n", findInTable(table, command));
		}
		else if(strcmp(command, "exit\n") == 0) {
			loopContinue = 0;
		}
	}
	printf("CSAV001ILT Table processing complete\n");
	return 0;
}
