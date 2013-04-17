#!/usr/bin/python
# programma che genera un file batch per convertire tutte le sottodirectory in mkv
# da eseguire così:
# cd directory_madre
# python ~/tmp/programmazione/walk-dir.py > mkv-mov.sh
# bash mkv-mov.sh 

import os
for root,dir,files in os.walk(os.getcwd()):
        
	for di in dir:
		print "cd \""+os.path.join(root,di)+"\""
		print "py/video/trasforma_mjpeg_in_mkv.py *.MOV"




