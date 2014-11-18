#!/usr/bin/python
# gd 20081211
# last modify 201305121
# copia (o sposta) le immagini di una directory in una sottoserie di cartelle divise per data es 2009_03_02
# utilizza imagemagic

import os,sys
import shutil
from os.path import join, getsize
import subprocess

def execute_command(comando):
	"""
	Esegue un comando di sistema
	"""
	verbose=False
	simulate=False
	if verbose == True:
		print ('--------------------------------------')
		print (comando)
		print ('++++++++++++++++++++++++++++++++++++++')
	if simulate == False:
		
		status = 0
#		comando = "identify"
		

		out = subprocess.check_output(comando,shell=True)
		return out


def getExifDate(fileName):
		comando = 'identify -format "%[EXIF:DateTime]" "' + fileName+'"'
		output = execute_command(comando)
		out2=str(output)
	
		out = out2[2:12].replace(':','_')
		return out
		
directory_base = sys.argv[1]
directory_dest = sys.argv[2]

for root, dirs, files in os.walk(directory_base):
	for name in files:
		file = os.path.join(root, name)
		dir = directory_dest+'/'+getExifDate(file)
#		if not os.path.exists(dir):
#			os.mkdir(dir)
		print(file+'  '+dir+'_'+name)
#		shutil.copyfile(file,dir+'_'+name)			
		shutil.move(file,dir+'_'+name)
	
