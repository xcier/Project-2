#!/bin/sh
rm file_index.txt
for f in *.sav; do 
	echo "------- $f -------" >> file_index.txt;  
	ReadSaveHeader $f | grep "Build ID: " >> file_index.txt; 
done
