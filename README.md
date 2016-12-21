# DH2016-salpakari

Digital Humanities course work. OCR and datavisualization.

What does it do?

Two bash scripts and a small python program to OCR a handscanned cookbook and to clean OCR-errors from the text and list the most used ingredients.

Corpus and research questions

My corpus isn't much of a corpus, just a single book, 'Kiireisen keittokirja' by Juha Heikinheimo and Marjaleena Nordlund from 1975. My goal is to produce a list of ingredients and how many times they are mentioned. The project is also supposed to be a prove of concept kinda thing to test if computational methods could be used as a part of my master's thesis.

Workflow

1. Decide to scan a Finnish cookbook from the 1970's (part of my master's thesis) and to make it machine readable.
2. Firstly try to use pictures taken with cellphone, realise they aren't adequate at all. Scan the book instead with a scanner instead in black and white and in high quality TIF-format
3. Write a script to split the multipaged tif-files into single page files, since the script used to prepare them for OCR can't understand multipage files.
4. Split the files with splitter.sh
5. Use textcleaner sript from Fred's Imagemagick (http://www.fmwconcepts.com/imagemagick/textcleaner/) to prepare the TIF-files and tesseract (https://github.com/tesseract-ocr) to OCR them.
6. Write the script tiff-filt-ocr.sh to automate this process.
7. Upload the OCR'd text to a IPython notebook and following tutorials from The Programming Historian (http://programminghistorian.org/lessons/cleaning-ocrd-text-with-regular-expressions) and Python's re library clean the text from OCR-errors
8. Write the ingredients and their occurrences into two lists, which can be used with the plotly library to produce a graph of the most used ingredients.

Additional information and instructions can be found in comments of the code files.
For copyright reasons I can't upload the full OCR'd text.

Conclusions

The code is extremely clanky. There are numerous (possibly) unrequired conversions from string to list to dict and back. Also some non-ingredients made it into the final graph. Nevertheless the project was a fine tutorial to regular expressions and text processing in Python. For further development the code could be simplified A LOT and methods could be perfected. For example now the word with most occurrences on the list is 'can'. The code could be modified to list this as can of something. Same could be done with the word 'minced' that is the sixth on the list
