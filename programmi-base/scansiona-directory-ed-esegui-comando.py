#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20141117
"""
Scansiona una directory ed esegue un comando per tipologia di file

"""
import os
import subprocess

# run a command for every file in one directory  in this example 


def recusively_lanch_command(dir):
	for dirpath, dirnames, filenames in os.walk (dir):
		for subdir in dirnames:
			recusively_lanch_command(subdir)
		for nomefile in filenames:
			nome_file_completo = os.path.join(dirpath,nomefile)
			(filebase,estensione) = os.path.splitext( nome_file_completo )
			if (estensione.lower() == '.py'): 			
#				os.system('ls -la "'+ nome_file_completo+'"')
				output = subprocess.check_output(['ls', '-la',nome_file_completo])
				print(output)
	



#------------------------------- MAIN --------------------------------

processing_directory = './'
recusively_lanch_command(processing_directory)
