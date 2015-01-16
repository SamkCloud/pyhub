#!/bin/python
# leggi ed elabora / fai il parse dei file html / xml
# tramite BeautifulSoup
# gd 20150116

from bs4 import BeautifulSoup
import sys
import codecs

fileObj = codecs.open( sys.argv[1], "r", "utf-8" )
html_data = fileObj.read()

soup = BeautifulSoup(html_data)

# converti tutto l'html in testo semplice
s=str(soup.get_text())

f = open('output.txt', 'wt', encoding='utf-8')
f.write(s)

# mostra tutti i link <a>
#for anchor in soup.find_all('a'):
#	print(anchor.get('href', '/'))
