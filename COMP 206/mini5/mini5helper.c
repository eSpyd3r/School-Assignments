#include <stdio.h>
#include <stdlib.h>
#include "mini5phone.h"
#include "mini5helper.h"


struct PHONE_NODE *get_node_by_index(int index) {
    struct PHONE_NODE *current = head;
    int i;

    for (i = 0; i < index && current != NULL; i++) {
        current = current->next;
    }

    return current;
}

