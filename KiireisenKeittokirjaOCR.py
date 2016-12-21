

#import regex library and open the combined textfile

import re
import pandas as pd
import numpy as np


infile = open('kokoteksti.txt')
text = infile.read()
infile.close()



#transform _ into hyphens where needed
correctHyphens = re.sub(r'_\n', r'-\n',text )


#removes characters that should not BE
removeUseless = re.sub(r'[;Šš*_«»<>›”““\'\^]','', correctHyphens)
#print removeuseless


#remove dots from start of lines
removeDots = re.sub(r'(?<=\n)\.', '', removeUseless)


#replace a's m's, w's and dots next to digits or dashes with dashes
#TÄÄ EI TUNNISTA KAIKKIA!! riko kahteen osaan, eka tunnistaa edessä olevat numerot/viivat, toinen jäljessä olevat
mwToDash = re.sub(r'(?<=[\d-])[\.mwMW](?=[\d-])', '-', removeDots)


#replase z's next to dashes with 2's
zTo2 = re.sub(r'(?<=-)[Zz]', '2', mwToDash)


#transforms l's after white space BUT NOT BEFORE DIGITS and before a space, a dash or m to 1's
lto1 = re.sub(r'(?<!\d)\sl(?=[\sm-])', '\n1', zTo2)
#print lto1


#remove extra dashes
removeDashes = re.sub(r'(?<=\d)--+','-', lto1)


#remove hyphens & line changes
removeHyphens = re.sub(r'-\n', '', removeDashes)


#remove empytlines
removeEmpty = re.sub(r'\n \n','', removeHyphens)


#remove invidual Q's, O's and similar
RemoveQ = re.sub(r'\s[QO]\s', '', removeEmpty)
#print RemoveQ


#remove wrong commas
removeCommas = re.sub('(?<=[\d\s]),', '', RemoveQ)


#replace gzn with g:n
grams = re.sub('gzn', 'g:n', removeCommas)


#replace lOO with 100
loosToHundreds = re.sub('lOO', '100', grams)


#replace lO with 10
losToTens = re.sub('lO', '10', loosToHundreds)


#remove pagenumbers and lone numbers at the start of lines
removeLoneNumbers = re.sub(r'\n\d+(?!.*[A-Za-z])', '', losToTens)
removePageNumbers = re.sub(r'\n\d+.*RUOAT|\n\d+.*SEKALAISET|\n\d+.*KEITOT|\n\d+.*JÄÄTELÖÄ|\n\d+.*TUOTTEET|\n\d+.*MARJAT|\n\d+.*HEDELMÄT','', removeLoneNumbers) #lisää tähän kaikki muutkin luokat, kuten KEITOT ja vastaavat
#print removePageNumbers




#regex with which to find all ingredient lines and add '*' to the start of these lines

#lines starting with digits
starDigits = re.sub(r'\n ?(?=\d)', r'\n*', removePageNumbers)

#lines starting with I or V
starIV = re.sub(r'\n(III |II |IV |I |V )', '\n*', starDigits)

#lines starting with noin, hiukkasen, suolaa, voita, öljyä and other similar recipewords
starWords = re.sub(r'\n(?=[Nn]oin|[Hh]ienonnettua|.*[Ss]uolaa|.*[Öö]ljyä|.*[Vv]oita|[Hh]iukan|hiukkasen|[Pp]ala\b|[Nn]okare|.*pippuria|[Ss]inappia|.*juustoa|[Pp]ersiljaa|.*leipää|hunajaa|sokeria|mantelilastuja|likööriä)', '\n*', starIV )



#read all lines starting with * into a list

ingredients=re.findall(r'\*.*',starWords)

#since lists cannot be cleaned with regex, write the ingredients into a string
ingredientsString = ''
for entry in ingredients:
    ingredientsString = ingredientsString + entry

#Final cleanup! Let's clean the ingredients of the last OCR-crud.
    
#let's make the string all lowercase
ingredientsString = ingredientsString.lower()
#remove characters that should not BE
ingredientsString = re.sub(r'[\*\d,/)(\!\?+"\.-]', ' ', ingredientsString)
#remove teaspoons, grams, and's, or's from the ingredients
ingredientsString = re.sub(r' tai | tl |rkl|g:n|kg:n|kg| ja |noin|dl| [a-ö] ', ' ', ingredientsString)

#convert cleaned ingredientsList back to list-form so we can...

ingredientsList = ingredientsString.split()

#transform it into a dictionary!

ingredientsDic = {}

for entry in ingredientsList:
    if entry not in ingredientsDic:
        ingredientsDic[entry] = 1
    else:
        ingredientsDic[entry] += 1



#but this dictionary is not ordered! It's somewhat impossible to sort an ordered dictionary in python,but we can produce from it an ordered list of tuples, like so

import operator

sorted_ingredients = sorted(ingredientsDic.items(), key=operator.itemgetter(1))

#now that the ingredients have been sorted we'll produce two lists, first of the ingredients and the second of their occurrences

keys, values = zip(*sorted_ingredients)

#the lists are sorted from least occurrences to most, so let's reverse their order

keys = keys[::-1]
values = values[::-1]

#we are only interested in the top ingredients, so le'ts cut the top 15 from both lists

top15keys = keys[:15]
top15values = values[:15]

#and now using the plotly library we can produce a nifty bar graph of the ingredients!
#there are many different libararies you could use to visualize your project!

import plotly as py
import plotly.graph_objs as go


#plotly requires making an account, here I'm logging into mine
py.tools.set_credentials_file(username='USERNAME', api_key='APIKEY')

data = [go.Bar(
            x=top15keys,
            y=top15values
    )]

py.offline.iplot(data, filename='basic-bar')

#the resulting bar graph can be seen in the jpg.file

