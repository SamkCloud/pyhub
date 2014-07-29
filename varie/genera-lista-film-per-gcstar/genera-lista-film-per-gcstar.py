#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20130804

##########
#
# Quando si fa l'import su GCSTAR ricordarsi di impostare i seguenti campi nel seguente ordine:
#
# Titolo; Trailer; Commento
#
#

import os
import argparse
import subprocess
import shlex
import re
import time

def print_r(v):
	return '%s = %r %s' % (v, v, type(v))

def show_file_in_dir(dir,args):
	f = open(args.output,'a')
	for dirpath, dirnames, filenames in os.walk (dir):
		for subdir in dirnames:
			show_file_in_dir(subdir,args)
		for nomefile in filenames:
			nome_file_completo = os.path.join(dirpath,nomefile)
			(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(nome_file_completo)

			print (nomefile)
			parts = nomefile.split("-") 
		
			if(len(parts)==4):
				(anno,titolo,lingue,qualita)=parts
			else:
				titolo=nomefile
			
			command_line = 'ffprobe "INPUT"'
			command_line = command_line.replace('INPUT', nome_file_completo)
			
			command_line_list = shlex.split(command_line)
			p = subprocess.Popen(command_line_list,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			output = p.communicate()
			out_list = (str( output[0], encoding='utf8' )).split("\n")
			commento = ''
			lista_commenti = []
			for line in out_list:
				if re.search('Stream #', line,re.I):
					lista_commenti.append(line.strip())

			if (mtime > int(args.newer_time)):
				commento = '|'.join(lista_commenti)
				f.write(''+titolo+';'+nome_file_completo+';'+commento+'\n') 
	f.close()		

def run(args):
	
	f = open(args.output,'w')
	f.write("Titolo;Trailer;Commento\n") 
	f.close()
	show_file_in_dir(args.dirname,args)	 

	ora = int(time.time())
	print("Command excecuted:",time.ctime(ora))
	print("Command excecuted UNIX TIME:",ora)
	
	 
def main():

	parser = argparse.ArgumentParser(description='Genera la lista film in csv da importare in gcstar')
	parser.add_argument("dirname", help='directory in cui ci sono i film da analizzare')
	parser.add_argument('-o','--output',help='Output file name', default='lista-film.csv')
	parser.add_argument('-t','--newer-time',help='Only file newer than (Unix Time)', default=0)
	args = parser.parse_args()
	
	run(args)



if __name__ == '__main__':
	main()