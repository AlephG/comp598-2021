#!/bin/bash

#Print out the number of lines
nlines=$(<$1 wc -l)
nlines=${nlines##*()}
if ((nlines >= 10000));
then
	echo $nlines
else
	echo "This file has less than 10000 lines" > /dev/stderr
	exit 1
fi

#Print the first line of the input file
head -n 1 $1

#Print the number of lines in the last 10000 rows that contain the string "potus"
tail -n 10000 $1 | grep -c -i "potus"

#Print the number of lines in the rows 100 to 200 that contain the word "fake"
sed -n '100,200p' $1 | grep -c "fake"
