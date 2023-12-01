#include <stdio.h>
#include <string.h>
#include "mini5phone.h"

void menu() {
    // Print menu header
    printf("Phonebook Menu: (1)Add, (2)Delete/Clear, (3)Find, (4)List, (5)Quit > ");
}

int main() {
    int choice, result;
    char name[50], birth[50], phone[50];
    char garbage[5];
    
    //load phonebook
    loadCSV("phonebook.csv");

    do {
	//print menu header
        menu();

        // Read the choice from the keyboard in main
        scanf("%d", &choice);
        fgets(garbage, 4, stdin);

        switch (choice) {
            case 1:
		//collect input to add new phonerecord
                printf("Name: ");
                fgets(name, 49, stdin);
                name[strlen(name) - 1] = '\0';
                printf("Birth: ");
                fgets(birth, 12, stdin);
                birth[strlen(birth) - 1] = '\0';
                printf("Phone: ");
                scanf(" %14[^\n]%*c", phone);
          
                //create new record with inputs
		result = addRecord(name, birth, phone);
		//check the return
                if (result != 0) printf("CSV is out of space\n");

                break;

            case 2:
		//delete or clear
		printf("(D)elete or (C)lear > ");
		char delete_or_clear;
		char input[10];
    		fgets(input, sizeof(input), stdin);
   	        sscanf(input, "%c", &delete_or_clear);

		//delete given name
		if (delete_or_clear == 'D' || delete_or_clear == 'd') {
			printf("Delete name: ");
			fgets(name, 49, stdin);
			name[strlen(name) - 1] = '\0';

			result = delete(name);
			if (result == -1) printf("Sorry not found\n");
			break;
		}
		//clear entire phonebook
		else if (delete_or_clear == 'C' || delete_or_clear == 'c') {
			char confirmation;
				//confirm clearing
				printf("Are you sure (Y/N) > ");
				scanf("%c", &confirmation);
				fgets(garbage, 4, stdin);
				if (confirmation == 'Y' || confirmation == 'y') {
					clear();
					break;
				} else if (confirmation == 'N' || confirmation == 'n') {
					break;
				} else {
					printf("Sorry wrong selection!\n");
				}
		} else {
			printf("Sorry wrong selection!\n");
			fgets(garbage, sizeof(garbage), stdin); // clear input buffer
			}
		break;



            case 3:
		//find given name
                printf("Find name: ");
                fgets(name, 49, stdin);
                name[strlen(name) - 1] = '\0';

                result = findRecord(name);
                if (result == -1) printf("Does not exist\n");

                else {
			//print out header & node at specific index
			printf("---- NAME ---- ---- BIRTH DATE ---- ---- PHONE ----\n");
                    	struct PHONE_NODE *foundNode = get_node_by_index(result);
			printf("%-14s %-20s %-10s\n", foundNode->name, foundNode->birthdate, foundNode->phone);
                }

                break;

            case 4:
		//list out phone records
                result = list();

                if (result != 0) printf("Phonebook.csv does not exist\n");
                break;

            case 5:
		//quit
                break;

            default:
                printf("Sorry wrong selection!\n");
        }
    } while (choice != 5);

    saveCSV("phonebook.csv");

    printf("End of phonebook program\n");

    return 0;
}
