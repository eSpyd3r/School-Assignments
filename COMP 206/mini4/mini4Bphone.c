#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct PHONE_RECORD {
	char name[50];
	char birthdate[12];
	char phone[15];
} *phonebook;

int loadCSV(char* filename, struct PHONE_RECORD phonebook[], int size) { //return errorcode, otherwise load data structure
    FILE* fp;
    fp = fopen(filename, "r");
    if (fp == NULL) { //file does not exist
	return 1;
    }
    int i;
    for (i = 0; i < size; i++) { //loading information into phonebook, knowing that csvs separate data by commas as mentioned in class
	if (fscanf(fp, "%49[^,],%11[^,],%14[^\n]\n", phonebook[i].name, phonebook[i].birthdate, phonebook[i].phone) == EOF){
            break;
	}
    }
    fclose(fp);
    return 0;
}

int saveCSV(char* filename, struct PHONE_RECORD phonebook[], int size, int exist) { //return errorcode, otherwise save data structure
    if (exist == 1) {
	    printf("No phonebook exists and no additional records to store\n");
	    return 1;
    }
    
    FILE* fp;
    fp = fopen(filename, "w");

    for (int i = 0; i < size; i++) { //saving to filename using csv format mentioned in class, iterating through each index of phone book
	    if (strcmp(phonebook[i].name, "") == 0) break;
	    fprintf(fp, "%s,%s,%s\n", phonebook[i].name, phonebook[i].birthdate, phonebook[i].phone);
	    
    }
    fclose(fp);

    return 0;

}

int addRecord(struct PHONE_RECORD phonebook[], int size) { //return errorcode, otherwise add a new phone entry
    int i;
    for (i = 0; i < size; i++) { //adding to the phonebook directly after each input
	if (strcmp(phonebook[i].name, "") == 0){
	printf("Enter name:\n");
        scanf(" %49[^\n]%*c", phonebook[i].name);
	
	printf("Enter birthdate:\n");
	scanf(" %11[^\n]%*c", phonebook[i].birthdate);
        
	printf("Enter phone number:\n");
	scanf(" %14[^\n]%*c", phonebook[i].phone);

	return 0;

	}

    }
    printf("No more space in csv file.\n");
    return 1;
}

int findRecord(struct PHONE_RECORD phonebook[], int size, int exist) { //return errorcode, otherwise return index of found record
        if (exist == 1) {
	    printf("File does not exist, nothing to search.\n");
	    return 1;
	}//file does not exist

	char name[50];
	printf("Enter name to search for:\n");
	fgets(name, 50, stdin);
	name[strcspn(name, "\n")] = '\0';
	for (int i = 0; i < size; i++) { //iterating through phonebook, looking for matching name. note that this searches by string similarity
		if (strcmp(phonebook[i].name, name) == 0) {
		    printf("Name: %s\nBirthdate: %s\nPhone: %s\n", phonebook[i].name, phonebook[i].birthdate, phonebook[i].phone);
		    return i;}
	}
        printf("Does not exist.\n");
	return 1;

}

int listRecords(struct PHONE_RECORD phonebook[], int size, int exist) { //return errorcode, otherwise displays
    if (exist == 1) {
        printf("File does not exist, nothing to list\n");
	return 1;
    } //file does not exist
    printf("----NAME--------- ------BIRTHDATE------ -----PHONE-------\n");
    for (int i = 0; i < size; i++) {
	    if (strcmp(phonebook[i].name, "") != 0) {
	        printf("%s             %s          %s\n", phonebook[i].name, phonebook[i].birthdate, phonebook[i].phone);
            }
    }
    return 0;    
}


