#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# programma che genera un file batch per convertire tutte le sottodirectory in mkv
# da eseguire così:
# cd directory principale
# ~/bin/pyhub/video/genera-batch-per-convertire-tutti-i-mov ./ > mkv-mov.sh
# bash mkv-mov.sh 

COMANDO = "~/bin/pyhub/video/trasforma_mjpeg_in_mkv.py "

import os
import sys
fileList = []
rootdir = sys.argv[1]
for root, subFolders, files in os.walk(rootdir):
	for file in files:
		filename= os.path.join(root,file)
		fileList.append(filename)
		print(COMANDO+" \""+filename+"\"")


