#!/usr/bin/python

# versione 20100430.01

# esempio
# ./scarica-alle8dellasera-ram.py fed2/
# in fed2 ci sono tutti i file .ra scaricati dal sito rai

import os
import sys

path=sys.argv[1]
dirList=os.listdir(path)
for fname in dirList:
	filename = path+fname
	(shortname, extension) = os.path.splitext(filename)
	if (extension == '.ram'): 
		#print filename
		newfile = filename+'.new.ra'
		input = open(filename,'r')	
		s = input.read()
		comando1 = 'mplayer -dumpstream -dumpfile '+newfile+' -bandwidth 4000000 ' + s
		
		print comando1
		os.system(comando1)
	
		comando2 = 'ffmpeg -i '+newfile+' -f wav - | lame -V 7 - '+shortname+'.mp3'
		print comando2
		os.system(comando2)





