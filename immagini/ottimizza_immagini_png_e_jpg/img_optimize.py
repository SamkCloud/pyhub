#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20141117
"""
Ottimizza le immagini in una directory (e sottodirectory) 
"""

import argparse
import os
import subprocess
import shutil

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def recusively_lanch_command(dir,args):
	
	for dirpath, dirnames, filenames in os.walk (dir):
		for subdir in dirnames:
			recusively_lanch_command(subdir,args)
		for nomefile in filenames:
			nome_file_completo = os.path.join(dirpath,nomefile)
			(filebase,estensione) = os.path.splitext( nome_file_completo )
			if (estensione.lower() == '.png'): 		
				file_bk = filebase+'.orig'+estensione
				print(file_bk)
				shutil.move(nome_file_completo, file_bk)
				output = subprocess.check_output(['zopflipng',file_bk,nome_file_completo])
				if (not args.keep_orig) : 
					os.remove(file_bk)
				print(output)
	
def run(args=None):
	
	
	#print("dir da ottimizare",args.dirname)
	dir = args.dirname
	recusively_lanch_command(dir,args)

def main():
	
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument("dirname", help='directory da ottimizzare')
	parser.add_argument('-k','--keep_orig',help='Keep the original file', action='store_true')
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


