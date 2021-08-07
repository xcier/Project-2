#include <stdlib.h>
#include <string.h>
#include <dirent.h>

/*
 * A (very poorly written) menu for CSave
 * Yes, it looks like ISPF
 *  
 * Some compiling notes:
 * - This will compile just fine with an
 *   X/Open compliant Curses.
 * - For whatever reason, pdCurses doesn't
 *   work (clarification needed)
 * - OSF/1 AXP 5.1 works
 * - FreeBSD 4.0+ works
 * - AIX 6.1 supposedly works
 * - You have to compile this with GNU C
 *   (proof needed)
 */

// Do you have a modern enough NCurses?
#define NCURSES

#ifdef NCURSES
// If so, use its header
#include <ncurses.h>
#else
// No, gotta use the crappy old one
#include <curses.h>
#endif

char* menuHeaderText = "CSave Functions Menu"; // This only exists because strlen.

// Default terminal size -- change me if you want
int row = 24;
int col = 80;
char* currentFile;
int loopContinue = 1;
char filename[1024];
FILE* fp;
char path[8192];
char* command;
int outRow = 4;
int outCol = 2;
char* myLine;
char choice;


void drawMainMenu() {
	clear();
	attron(A_BOLD);
	attron(COLOR_PAIR(1));
	mvprintw(0, (col - strlen(menuHeaderText)) / 2, "%s", menuHeaderText);
	attroff(A_BOLD);
	attroff(COLOR_PAIR(1));
	attron(COLOR_PAIR(2));
	mvprintw(2, 2, "0    File Save Files");
	mvprintw(3, 2, "1    Find Protobuf Files");
	mvprintw(4, 2, "2    Convert Save to Protobuf Format");
	mvprintw(5, 2, "3    Convert Protobuf Format to Save");
	mvprintw(6, 2, "4    Convert Profile to Protobuf Format");
	mvprintw(7, 2, "5    Convert Protobuf Format to Profile");
	mvprintw(8, 2, "6    Get Save Information");
	mvprintw(9, 2, "7    Get Profile Information");
	mvprintw(10, 2, "8    Start Save Editor");
	mvprintw(11, 2, "9    Start Profile Editor");
	mvprintw(12, 2, "Z    Exit");
	attroff(COLOR_PAIR(2));
	attron(COLOR_PAIR(3));
	mvprintw((row - 2), 2, "Enter option --> ");
	attroff(COLOR_PAIR(3));
	refresh();
}

void defineColors() {
	init_pair(1, COLOR_BLUE, COLOR_BLACK);
	init_pair(2, COLOR_GREEN, COLOR_BLACK);
	init_pair(3, COLOR_CYAN, COLOR_BLACK);
	init_pair(4, COLOR_RED, COLOR_BLACK);
}

void listDirectory(char* path, char* grep) {
	struct dirent* de;
	DIR* dr = opendir(path);
	if(dr == NULL) {
		clear();
		attron(COLOR_PAIR(4));
		mvprintw(0, 0, "Failed to open directory!");
		refresh();
		getch();
		attroff(COLOR_PAIR(4));
		clear();
		refresh();
		return;
	}
	int line = 2;
	clear();
	attron(COLOR_PAIR(1));
	mvprintw(0, (col - strlen("File Listing")) / 2, "File Listing");
	attroff(COLOR_PAIR(1));
	attron(COLOR_PAIR(2));
	while((de = readdir(dr)) != NULL) {
		move(line, 2);
		if(strstr(de->d_name, grep) != NULL) {
			printw("%s\n", de->d_name);
			line++;
		}
	}
	attroff(COLOR_PAIR(2));
	refresh();
	getch();
}

void saveToProto() {
	clear();
	attron(COLOR_PAIR(1));
	mvprintw(0, (col - strlen("Save to Protobuf")) / 2, "Save To Protobuf");
	attroff(COLOR_PAIR(1));
	attron(COLOR_PAIR(2));
	mvprintw(1, 0, "Please specify a filename.");
	attroff(COLOR_PAIR(2));
	attron(COLOR_PAIR(3));
	refresh();
	mvprintw((row - 2), 2, "Enter file --> ");
	attroff(COLOR_PAIR(3));
	getstr(filename);
	attron(COLOR_PAIR(2));
	mvprintw(2, 0, "Will convert %s", filename);
	refresh();
	command = malloc(strlen("SaveToProto ") + strlen(filename) + 1);
	strcpy(command, "SaveToProto ");
	strcat(command, filename);
	fp = popen(command, "r");
	if(fp == NULL) {
		attron(COLOR_PAIR(4));
		mvprintw(row - 1, 0, "Failed to execute SaveToProto!");
		attroff(COLOR_PAIR(4));
		refresh();
		getch();
		return;
	}
	outRow = 4;
	outCol = 2;
	attron(COLOR_PAIR(3));
	move(outRow, outCol);
	while(fgets(path, sizeof(path), fp) != NULL) {
		myLine = malloc(col - 4);
		memcpy(myLine, path, col - 4);
		if(outRow > row - 4) {
			getch();
			clear();
			outRow = 4;
		}
		mvprintw(outRow, outCol, "%s", myLine);
		outRow++;
	}
	pclose(fp);
	getch();
	attroff(COLOR_PAIR(3));
	attron(COLOR_PAIR(2));
	mvprintw(row - 1, 0, "Execution complete");
	attroff(COLOR_PAIR(2));
	getch();
}

void saveToProtoProfile() {
	clear();
	attron(COLOR_PAIR(1));
	mvprintw(0, (col - strlen("Profile to Protobuf")) / 2, "Profile To Protobuf");
	attroff(COLOR_PAIR(1));
	attron(COLOR_PAIR(2));
	mvprintw(1, 0, "Please specify a filename.");
	attroff(COLOR_PAIR(2));
	attron(COLOR_PAIR(3));
	refresh();
	mvprintw((row - 2), 2, "Enter file --> ");
	attroff(COLOR_PAIR(3));
	getstr(filename);
	attron(COLOR_PAIR(2));
	mvprintw(2, 0, "Will convert %s", filename);
	refresh();
	command = malloc(strlen("ProfileToProto ") + strlen(filename) + 1);
	strcpy(command, "ProfileToProto ");
	strcat(command, filename);
	fp = popen(command, "r");
	if(fp == NULL) {
		attron(COLOR_PAIR(4));
		mvprintw(row - 1, 0, "Failed to execute ProfileToProto!");
		attroff(COLOR_PAIR(4));
		refresh();
		getch();
		return;
	}
	outRow = 4;
	outCol = 2;
	attron(COLOR_PAIR(3));
	move(outRow, outCol);
	while(fgets(path, sizeof(path), fp) != NULL) {
		myLine = malloc(col - 4);
		memcpy(myLine, path, col - 4);
		if(outRow > row - 4) {
			getch();
			clear();
			outRow = 4;
		}
		mvprintw(outRow, outCol, "%s", myLine);
		outRow++;
	}
	pclose(fp);
	getch();
	attroff(COLOR_PAIR(3));
	attron(COLOR_PAIR(2));
	mvprintw(row - 1, 0, "Execution complete");
	attroff(COLOR_PAIR(2));
	getch();
}

void protoToSave() {
	clear();
	attron(COLOR_PAIR(1));
	mvprintw(0, (col - strlen("Protobuf To Save")) / 2, "Protobuf To Save");
	attroff(COLOR_PAIR(1));
	attron(COLOR_PAIR(2));
	mvprintw(1, 0, "Please specify a filename.");
	attroff(COLOR_PAIR(2));
	attron(COLOR_PAIR(3));
	refresh();
	mvprintw((row - 2), 2, "Enter file --> ");
	attroff(COLOR_PAIR(3));
	getstr(filename);
	attron(COLOR_PAIR(2));
	mvprintw(2, 0, "Will convert %s", filename);
	refresh();
	command = malloc(strlen("ProtoToSave ") + strlen(filename) + 1);
	strcpy(command, "ProtoToSave ");
	strcat(command, filename);
	fp = popen(command, "r");
	if(fp == NULL) {
		attron(COLOR_PAIR(4));
		mvprintw(row - 1, 0, "Failed to execute ProtoToSave");
		attroff(COLOR_PAIR(4));
		refresh();
		getch();
		return;
	}
	outRow = 4;
	outCol = 2;
	attron(COLOR_PAIR(3));
	move(outRow, outCol);
	while(fgets(path, sizeof(path), fp) != NULL) {
		myLine = malloc(col - 4);
		memcpy(myLine, path, col - 4);
		if(outRow > row - 4) {
			getch();
			clear();
			outRow = 4;
		}
		mvprintw(outRow, outCol, "%s", myLine);
		outRow++;
	}
	pclose(fp);
	getch();
	attroff(COLOR_PAIR(3));
	attron(COLOR_PAIR(2));
	mvprintw(row - 1, 0, "Execution complete");
	attroff(COLOR_PAIR(2));
	getch();
}

void protoToSaveProfile() {
	clear();
	attron(COLOR_PAIR(1));
	mvprintw(0, (col - strlen("Protobuf To Profile")) / 2, "Protobuf To Profile");
	attroff(COLOR_PAIR(1));
	attron(COLOR_PAIR(2));
	mvprintw(1, 0, "Please specify a filename.");
	attroff(COLOR_PAIR(2));
	attron(COLOR_PAIR(3));
	refresh();
	mvprintw((row - 2), 2, "Enter file --> ");
	attroff(COLOR_PAIR(3));
	getstr(filename);
	attron(COLOR_PAIR(2));
	mvprintw(2, 0, "Will convert %s", filename);
	refresh();
	command = malloc(strlen("ProtoToProfile ") + strlen(filename) + 1);
	strcpy(command, "ProtoToProfile ");
	strcat(command, filename);
	fp = popen(command, "r");
	if(fp == NULL) {
		attron(COLOR_PAIR(4));
		mvprintw(row - 1, 0, "Failed to execute ProtoToProfile");
		attroff(COLOR_PAIR(4));
		refresh();
		getch();
		return;
	}
	outRow = 4;
	outCol = 2;
	attron(COLOR_PAIR(3));
	move(outRow, outCol);
	while(fgets(path, sizeof(path), fp) != NULL) {
		myLine = malloc(col - 4);
		memcpy(myLine, path, col - 4);
		if(outRow > row - 4) {
			getch();
			clear();
			outRow = 4;
		}
		mvprintw(outRow, outCol, "%s", myLine);
		outRow++;
	}
	pclose(fp);
	getch();
	attroff(COLOR_PAIR(3));
	attron(COLOR_PAIR(2));
	mvprintw(row - 1, 0, "Execution complete");
	attroff(COLOR_PAIR(2));
	getch();
}

void saveUnpack() {
	clear();
	attron(COLOR_PAIR(1));
	mvprintw(0, (col - strlen("Save Info")) / 2, "Save Info");
	attroff(COLOR_PAIR(1));
	attron(COLOR_PAIR(2));
	mvprintw(1, 0, "Please specify a filename.");
	attroff(COLOR_PAIR(2));
	attron(COLOR_PAIR(3));
	refresh();
	mvprintw((row - 2), 2, "Enter file --> ");
	attroff(COLOR_PAIR(3));
	getstr(filename);
	attron(COLOR_PAIR(2));
	mvprintw(2, 0, "Will process %s", filename);
	refresh();
	command = malloc(strlen("SaveUnpack ") + strlen(filename) + 1);
	strcpy(command, "SaveUnpack ");
	strcat(command, filename);
	fp = popen(command, "r");
	if(fp == NULL) {
		attron(COLOR_PAIR(4));
		mvprintw(row - 1, 0, "Failed to execute SaveUnpack!");
		attroff(COLOR_PAIR(4));
		refresh();
		getch();
		return;
	}
	outRow = 4;
	outCol = 2;
	attron(COLOR_PAIR(3));
	move(outRow, outCol);
	while(fgets(path, sizeof(path), fp) != NULL) {
		myLine = malloc(col - 4);
		memcpy(myLine, path, col - 4);
		if(outRow > row - 4) {
			getch();
			clear();
			outRow = 4;
		}
		mvprintw(outRow, outCol, "%s", myLine);
		outRow++;
	}
	pclose(fp);
	getch();
	attroff(COLOR_PAIR(3));
	attron(COLOR_PAIR(2));
	mvprintw(row - 1, 0, "Execution complete");
	attroff(COLOR_PAIR(2));
	getch();
}

void profUnpack() {
	clear();
	attron(COLOR_PAIR(1));
	mvprintw(0, (col - strlen("Profile Info")) / 2, "Profile Info");
	attroff(COLOR_PAIR(1));
	attron(COLOR_PAIR(2));
	mvprintw(1, 0, "Please specify a filename.");
	attroff(COLOR_PAIR(2));
	attron(COLOR_PAIR(3));
	refresh();
	mvprintw((row - 2), 2, "Enter file --> ");
	attroff(COLOR_PAIR(3));
	getstr(filename);
	attron(COLOR_PAIR(2));
	mvprintw(2, 0, "Will process %s", filename);
	refresh();
	command = malloc(strlen("ProfileUnpack ") + strlen(filename) + 1);
	strcpy(command, "ProfileUnpack ");
	strcat(command, filename);
	fp = popen(command, "r");
	if(fp == NULL) {
		attron(COLOR_PAIR(4));
		mvprintw(row - 1, 0, "Failed to execute ProfileUnpack!");
		attroff(COLOR_PAIR(4));
		refresh();
		getch();
		return;
	}
	outRow = 4;
	outCol = 2;
	attron(COLOR_PAIR(3));
	move(outRow, outCol);
	while(fgets(path, sizeof(path), fp) != NULL) {
		myLine = malloc(col - 4);
		memcpy(myLine, path, col - 4);
		if(outRow > row - 4) {
			getch();
			clear();
			outRow = 4;
		}
		mvprintw(outRow, outCol, "%s", myLine);
		outRow++;
	}
	pclose(fp);
	getch();
	attroff(COLOR_PAIR(3));
	attron(COLOR_PAIR(2));
	mvprintw(row - 1, 0, "Execution complete");
	attroff(COLOR_PAIR(2));
	getch();
}

int main(int argc, char** argv) {
	initscr();
	start_color();
	defineColors();
#ifdef NCURSES
	getmaxyx(stdscr, row, col);
#else
#warning Compiling with older X/Open Curses, problems may result!
#endif
	// Start.
	do {
		drawMainMenu();
		choice = getch();
		if(choice == 'z') {
			loopContinue = 0;
		}
		else if(choice == '0') {
			listDirectory(".", ".sav");
		}
		else if(choice == '1') {
			listDirectory(".", ".proto");
		}
		else if(choice == '2') {
			saveToProto();
		}
		else if(choice == '3') {
			protoToSave();
		}
		else if(choice == '4') {
			saveToProtoProfile();
		}
		else if(choice == '5') {
			protoToSaveProfile();
		}
		else if(choice == '6') {
			saveUnpack();
		}
		else if(choice == '7') {
			profUnpack();
		}
		else {
			attron(COLOR_PAIR(4));
			mvprintw(row - 1, 0, "Please enter one of the options listed above.");
			getch();
			attroff(COLOR_PAIR(4));
			refresh();
		}
	} while(loopContinue == 1);

	// Exit.
	clear();
	mvprintw(0, 0, "Strike any key to continue");
	refresh();
	getch();
	endwin();
}
