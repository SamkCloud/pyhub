#!/usr/bin/python
# gd 20081211
# last modify 201305121
# copia (o sposta) le immagini di una directory in una sottoserie di cartelle divise per data ed 2009_03_02






def getExifDate(fileName):
		sys.path.append("~/bin/immagini")
		import EXIF
		file = open(fileName,"rb")
		data = EXIF.process_file(file)
		if not data:
			return "No EXIF Information available."
		
		timestamp = data['EXIF DateTimeDigitized']
		print(timestamp)
		data = str(timestamp)
		out = data[0:10].replace(':','_')
		return out
		
import os,sys
import shutil
from os.path import join, getsize

directory_base = sys.argv[1]
print (directory_base)

for root, dirs, files in os.walk(directory_base):
	for name in files:
		file = os.path.join(root, name)
		dir = directory_base+'/'+getExifDate(file)
		if not os.path.exists(dir):
			os.mkdir(dir)
		print(file+'  '+dir+'/'+name)
		shutil.copyfile(file,dir+'/'+name)			
		#shutil.move(file,dir+'/'+name)
	
