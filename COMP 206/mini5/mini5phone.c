#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mini5phone.h"
#include "mini5helper.h"
struct PHONE_NODE *head = NULL; //// Declare the head pointer for the linked list as a global variable


// Load phone records from a CSV file and add them to the linked list
int loadCSV(char *filename) {
    FILE *p = fopen(filename, "rt");
    char buffer[1000];
    int i, j;

    if (p == NULL) {
        return 1;
    }

    fgets(buffer, 999, p);

    struct PHONE_NODE *current = NULL;
    fgets(buffer, 999, p);
    while (!feof(p)) {
        struct PHONE_NODE *newNode = (struct PHONE_NODE *) malloc(sizeof(struct PHONE_NODE));

        for (j = 0, i = 0; i < 999 && buffer[i] != '\0' && buffer[i] != ','; i++, j++)
            newNode->name[j] = buffer[i];

        newNode->name[j] = '\0';
        i++;

        for (j = 0; i < 999 && buffer[i] != '\0' && buffer[i] != ','; i++, j++)
            newNode->birthdate[j] = buffer[i];

        newNode->birthdate[j] = '\0';
        i++;

        for (j = 0; i < 999 && buffer[i] != '\0' && buffer[i] != '\n'; i++, j++)
            newNode->phone[j] = buffer[i];

        newNode->phone[j] = '\0';

        newNode->next = NULL;
        if (head == NULL) {
            head = newNode;
        } else {
            current->next = newNode;
        }
        current = newNode;

        fgets(buffer, 999, p);
    }

    fclose(p);

    return 0;
}
// Save phone records from the linked list to a CSV file
int saveCSV(char *filename) {
    FILE *p = fopen(filename, "wt");

    if (p == NULL) return 1;

    fprintf(p, "name,birthdate,phone\n");

    struct PHONE_NODE *current = head;
    while (current != NULL) {
        fprintf(p, "%s,%s,%s\n", current->name, current->birthdate, current->phone);
        current = current->next;
    }

    fclose(p);

    return 0;
}
// Delete a phone record from the linked list by name
int delete(char name[]) {
	struct PHONE_NODE *current = head;
	struct PHONE_NODE *previous = NULL;
	//'removing' or 'disconecting' node from node structure
	while (current != NULL) {
		if (strcmp(current->name, name) == 0) {
			if (previous == NULL) {
				head = current->next;
			}
			else {
				previous->next = current->next;
			}
			free(current);
			return 0;
		}
		previous = current;
		current = current->next;
	}
	return -1;
}
// Clear all phone records from the linked list
int clear() {
    struct PHONE_NODE *current = head;
    struct PHONE_NODE *temp;

    while (current != NULL) {
        temp = current;
        current = current->next;
        free(temp);
    }

    head = NULL;

    return 0;
}
// Add a new phone record to the linked list
int addRecord(char name[], char birth[], char phone[]) {
    struct PHONE_NODE *newNode = (struct PHONE_NODE *) malloc(sizeof(struct PHONE_NODE));

    if (newNode == NULL) return 1;

    strcpy(newNode->name, name);
    strcpy(newNode->birthdate, birth);
    strcpy(newNode->phone, phone);
    newNode->next = NULL;

    if (head == NULL) {
        head = newNode;
    } else {
        struct PHONE_NODE *current = head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = newNode;
    }

    return 0;
}


// Find the index of a phone record in the linked list by name
int findRecord(char name[]) {
    struct PHONE_NODE *current = head;
    int index = 0;

    while (current != NULL) {
        if (strcmp(current->name, name) == 0) {
            return index;
        }
        current = current->next;
        index++;
    }

    return -1;
}



// Print all phone records in the linked list to the console
int list() {
    if (head == NULL) {
        return 1;
    }

    printf("---- NAME ---- ---- BIRTH DATE ---- ---- PHONE ----\n");

    struct PHONE_NODE *current = head;
    while (current != NULL) {
	printf("%-14s %-20s %-10s\n", current->name, current->birthdate, current->phone);
        current = current->next;
    }

    return 0;
}



