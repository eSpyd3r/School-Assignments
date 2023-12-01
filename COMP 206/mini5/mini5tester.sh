#!/bin/bash
echo "--- setting up the environment ---"
make
echo
echo "--- assignment description example test ---"

./phonebook << INPUT
4
1
Bob Smith
2000-01-15
514-333-4444
1
Mary Zhang
1999-05-20
1-234-567-1234
4
2
Mary Zhang
2
D
Tom Bombadil
4
2
C
Y
4
5
INPUT

echo
echo "---- TEST SCRIPT DONE ----"
echo "Note: TA will add additional tests. You should too."

