#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include"mini4Aphone.c"


int menu(void) {
    long choice;
    char input[100];
        
    
    printf("Phonebook Menu: "); //displaying menu
    printf("(1)Add (2)Find (3)List (4)Quit ");
    
    fgets(input, sizeof(input), stdin);

    char *endptr;
    choice = strtol(input, &endptr, 10);

    if (endptr == input || *endptr != '\n') { //checking if input is what's expected
        printf("Invalid input. Please enter a number between 1 and 4.\n");
	return menu();
    }

    if (choice < 1 || choice > 4) {
	printf("Invalid input. Please enter a number between 1 and 4.\n");
	return menu();
    }

    return (int)choice;
}

int main(void) {
   
    int exist = loadCSV("phonebook.csv", phonebook); //loading data from csv, informing if file exists
    
    int choice;
    do { //tracking the 'session', ending only when Quit is selected
        choice = menu();

	switch (choice) {
	    case 1:
	        addRecord(phonebook);
		exist = 0;
		break;
	    
	    case 2:
		findRecord(phonebook, exist);
		break;
	    
	    case 3:
		listRecords(phonebook, exist);
		break;
	    
	    case 4:
		saveCSV("phonebook.csv", phonebook, exist);
		break;	
	}
    } while (choice < 4);
 
    return 0;
}

