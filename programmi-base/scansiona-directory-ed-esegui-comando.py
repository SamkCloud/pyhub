#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150215
"""
Scansiona una directory ed esegue un comando per tipologia di file

"""
import os
import subprocess
import argparse

# run a command for every file in one directory  in this example 


def recusively_lanch_command(dir):
	for dirpath, dirnames, filenames in os.walk (dir):
		print(dirpath, dirnames, filenames)
		for nomefile in filenames:
			nome_file_completo = os.path.join(dirpath,nomefile)
			(filebase,estensione) = os.path.splitext( nome_file_completo )
			output = subprocess.check_output(['ls', '-la',nome_file_completo])
			print(output)
	



#------------------------------- MAIN --------------------------------

parser = argparse.ArgumentParser(description='Esegue un comando per ogni directory e subdirectory')
parser.add_argument('input_dir')
arguments = parser.parse_args()

processing_directory = arguments.input_dir
print('dir input: '+processing_directory)
recusively_lanch_command(processing_directory)
