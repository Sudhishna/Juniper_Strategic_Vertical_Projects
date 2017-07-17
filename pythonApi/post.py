#!/usr/bin/env python

import sys
import json
import cgi
import re
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.text import Text
from nltk.stem.porter import *

fs = cgi.FieldStorage()

sys.stdout.write("Content-Type: application/json")

sys.stdout.write("\n")
sys.stdout.write("\n")

result = {}

prods = fs.getvalue("ProductsLst")
prods = prods.replace("=on", "")
products = prods.split(",")

search = fs.getvalue("SearchTxt")
search = search.replace("SearchText=", "")
searchWords = search.split("+")

def fetchData(word, raw):
    data = ""
    
    sentences = sent_tokenize(raw)
    for sentence in sentences:
        if word in word_tokenize(sentence) or word.title() in word_tokenize(sentence) or word.lower() in word_tokenize(sentence) or word.upper() in word_tokenize(sentence) or re.search(word,sentence,re.IGNORECASE):
            data += "<p>" + u"\u2022" + u"\u0020" + sentence + "</p>"
    return data 

def searchpdf(pdfNames):
    rawList = ""
    for pdf in pdfNames:
	pdf = pdf.replace(".pdf", "")
	file = "products_database/" + pdf + ".txt"
        f = open(file, 'rU')
	raw = f.read().decode('utf8')
	raw = raw.replace(u"\u2022", '.')

	for word in searchWords:
	    raw = fetchData(word, raw)

        rawList += raw

    return rawList

removeList = list()
for i,product in enumerate(products[:-1]):
    str = products[i+1]
    substr = products[i]
    if not str.find(substr):
        removeList.append(substr)

for remove in removeList:
    products.remove(remove)

with open('products_database/hierarchy.json') as data_file:    
    data = json.load(data_file)

for product in products:
    product_keys = product.split("*")
    if len(product_keys) == 2:
	pro = product_keys[1]
	dat = searchpdf(data[product_keys[0]][product_keys[1]]["default"])
	if dat == "":
	    result[pro] = "Not Available/ Not Supported"
	else:
	    result[pro] = dat
	
    elif len(product_keys) == 3:
	pro = product_keys[2]
	dat = searchpdf(data[product_keys[0]][product_keys[1]][product_keys[2]])
	if dat == "":
	    result[pro] = "Not Available/ Not Supported"
	else:
	    result[pro] = dat

sys.stdout.write(json.dumps(result,indent=1))
sys.stdout.write("\n")

sys.stdout.close()
