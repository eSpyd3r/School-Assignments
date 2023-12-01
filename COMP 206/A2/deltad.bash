#!/usr/bin/bash
#Ethan Lim, Faculty of Science U1, ethan.lim@mail.mcgill.ca 261029610

if [ $# != 2 ]; then #checks if exactly 2 arguments were provided
	echo "Error: Expected two input parameters"
	echo "Usage: ./deltad.bash <originaldirectory> <comparisondirectory>"
	exit 1
fi

if [ ! -d $1 ]; then #checks if first argument is directory
	echo "Error: Input parameter '$1' is not a directory."
	echo "Usage: ./deltad.bash <originaldirectory> <comparisondirectory>"
	exit 2

elif [ ! -d $2 ]; then #checks if second argument is directory
	echo "Error: Input parameter '$2' is not a directory."
	echo "Usage: ./deltad.bash <originaldirectory> <comparisondirectory>"
	exit 2
fi


DIR1="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
DIR2="$(cd "$(dirname "$2")"; pwd)/$(basename "$2")"

if [ $DIR1 == $DIR2 ]; then #checks if directories are equal
	echo "Error: Input parameters refer to the same directory."
	exit 2
fi

if [ ! "$(ls -A $DIR1)" ] && [ ! "$(ls -A $DIR2)" ] ; then #if both are empty, there are technically no differences, so exits with code 0
	exit 0
fi

if [ ! "$(ls -A $DIR1)" ] ; then #if DIR1 is empty
	for FILE in $DIR2/*; do
		echo $1/$(basename $FILE) is missing
	done
	exit 3

elif [ ! "$(ls -A $DIR2)" ]; then #if DIR2 is empty
	for FILE in $DIR1/*; do
		echo $2/$(basename $FILE) is missing
	done
	exit 3
fi

different=false

for FILE in $DIR1/*; do #if both arugments are directories and are not empty, will iterate through both directories and compare
	fileName=$(basename $FILE)
	if [ -f $DIR2/$fileName ] && [ ! -d $DIR1/$fileName ]; then #if files match, will compare contents
		diff $DIR1/$fileName $DIR2/$fileName &>/dev/null
		if [ $? -ne 0 ]; then
		echo $1/$fileName differs
		different=true
		fi
	elif [ -d $DIR1/$fileName ]; then #if subdirectory, skips
		continue
	else
		echo $2/$fileName is missing
		different=true
	fi
done

for FILE in $DIR2/*; do #checks second argument/directory
	if [ ! -f $DIR1/$(basename $FILE) ] && [ ! -d $DIR1/$(basename $FILE) ]; then
		echo $1/$(basename $FILE) is missing
		different=true
	fi
done

if [ $different == false ]; then #code 0 if directories are the same
	exit 0
else
	exit 3 #code 3 if directories are different
fi
