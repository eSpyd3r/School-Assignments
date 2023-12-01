#!/usr/bin/bash
#Ethan Lim, Faculty of Science U1, ethan.lim@mail.mcgill.ca 261029610

if [ $# != 2 ] #checking if there are exactly 2 input arguments
then
	echo "Error: Expected two input parameters."
	echo "Usage: ./backup.bash <backupdirectory> <fileordirtobackup>"
	exit 1
fi

DIR="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")" #absolute paths, regardless
BKP="$(cd "$(dirname "$2")"; pwd)/$(basename "$2")"
DTE="$(date '+%Y%m%d')"

if [ ! -d $DIR ]; then #checking if $DIR and $BKP are valid arguments
	echo "Error: The directory '$DIR' does not exist"
	exit 2
elif [ ! -e $BKP ]; then
	echo "Error: The file or directory '$BKP' does not exist."
	exit 2
elif [ $DIR == $BKP ]; then
	echo "Error: Both arguments refer to the same directory."
	exit 2
fi

if [ -e "$DIR/$(basename $2).$DTE.tar" ]; then #if backup already exists, will prompt user to confirm overwrite
	while true; do
		read -p "Backup file '$BKP.$DTE.tar' already exists. Overerite? (y/n) " yn
		
		case $yn in
			[y] ) break;;
			* ) exit 3;;
		esac
	done
fi

tar -cvf "$BKP.$DTE.tar" $BKP

if [ $PWD != $DIR ] #won't attempt un-needed move if desired directory is equal to pwd
then
	mv "$BKP.$DTE.tar" $DIR
fi

