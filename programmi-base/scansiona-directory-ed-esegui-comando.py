#!/usr/bin/python
import os
# run a command for every file in one directory  in this example 


def recusively_lanch_command(dir):
	for dirpath, dirnames, filenames in os.walk (dir):
		for subdir in dirnames:
			recusively_lanch_command(subdir)
		for nomefile in filenames:
			nome_file_completo = os.path.join(dirpath,nomefile)
			(filebase,estensione) = os.path.splitext( nome_file_completo )
			if (estensione.lower() == '.py'): 			
				os.system('ls -la "'+ nome_file_completo+'"')
				# al posto di os.system meglio usare subprocess
				# es: 
				#import subprocess
				#output = subprocess.check_output(['ls', '-1'])
	



#------------------------------- MAIN --------------------------------

processing_directory = './'
recusively_lanch_command(processing_directory)
