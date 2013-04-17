#!/usr/bin/python
#
# gd 20120218
# programma per trasferire dalla videocamera Sony HDR-CX115E i 
# i video impostando il nome file con la data. 
#
# TODO
# con le opzioni inserire un verbose in modo che mostri cosa sta trasferendo


DIRECTORY_SRC = "/media/FC30-3DA9/PRIVATE/AVCHD/BDMV/STREAM/"

DIRECTORY_DST  ='/mnt/md0/giuliano/Video/video-giuliano/da-sistemare'

import os, time, shutil
for root,dir,files in os.walk(DIRECTORY_SRC):
		
	for file in files:
		filename =  os.path.join(root,file)
		data_creazione = os.path.getctime(filename)
# da :		 http://www.doughellmann.com/PyMOTW/time/
		parsed = time.strptime(time.ctime(data_creazione))
		data_video = time.strftime("%Y_%m_%d", parsed)
		filename_destinazione = data_video+"-"+file
		directory_con_data = DIRECTORY_DST+"/"+data_video
		if (not os.path.isdir(directory_con_data)):
			os.makedirs(directory_con_data)
		shutil.copyfile(filename,directory_con_data+'/'+filename_destinazione)
