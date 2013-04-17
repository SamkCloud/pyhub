#!/usr/bin/python
# 20090412 GD
# Copia i file mov dalla directory PHoto in quella MOV modificando il nome con la data. 
# usando Rapid Photo Downloder Non serve più
# usare cosi':
# ./move-video.py

import os,sys
import shutil

home = os.environ["HOME"]

#directory_base = sys.argv[1]
directory_base = home+"/Photos"
directory_destination = home+"/Video/video-giuliano/MOV/2009"


for root, dirs, files in os.walk(directory_base):
	for name in files:
		file = os.path.join(root, name)
		(shortname, extension) = os.path.splitext(file)
		if extension == ".mov":
			new_filname = file
			new_filname = new_filname.replace(directory_base+'/', '')	
			new_filname = new_filname.replace('/', '-') 	

			print new_filname
#			shutil.copyfile(file,directory_destination+'/'+new_filname)
			shutil.move(file,directory_destination+'/'+new_filname)

