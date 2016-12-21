#!/bin/bash
tif=".tif"
empty=""

for file in $(\ls orig $filenames)
do
	echo $file
	filetext=${file//$tif/$empty}
	./textcleaner -g -e normalize -f 15 -o 5 -s 0 -a 1 orig/$file out/$file 
	tesseract out/$file text/$filetext -l fin 
done
echo "OCR IS DONE"

