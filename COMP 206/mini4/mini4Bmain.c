#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include"mini4Bphone.c"


int menu(void) {
    long choice;
    char input[100];
        
    
    printf("Phonebook Menu: ");
    printf("(1)Add (2)Find (3)List (4)Quit ");
    
    fgets(input, sizeof(input), stdin);

    char *endptr;
    choice = strtol(input, &endptr, 10);

    if (endptr == input || *endptr != '\n') {
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
    int size;
    printf("Enter the size of the phone book: ");
    scanf("%d", &size);
    getchar();
    phonebook = (struct PHONE_RECORD*) malloc(size * sizeof(struct PHONE_RECORD));

    if (phonebook == NULL) {
	printf("Error: unable to allocate memory, array too large.\n");
        return 1;
    }	


    int exist = loadCSV("phonebook.csv", phonebook, size);
    
    int choice;
    do {
        choice = menu();

	switch (choice) {
	    case 1:
	        addRecord(phonebook, size);
		exist = 0;
		break;
	    
	    case 2:
		findRecord(phonebook, size, exist);
		break;
	    
	    case 3:
		listRecords(phonebook, size, exist);
		break;
	    
	    case 4:
		saveCSV("phonebook.csv", phonebook, size, exist);
		break;	
	}
    } while (choice < 4);
    free(phonebook);
    return 0;
}

