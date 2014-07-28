#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20130804

import os
import argparse
import subprocess
import shlex
import re

def print_r(v):
	return '%s = %r %s' % (v, v, type(v))

def show_file_in_dir(dir):
	for dirpath, dirnames, filenames in os.walk (dir):
		for subdir in dirnames:
			show_file_in_dir(subdir)
		for nomefile in filenames:
			nome_file_completo = os.path.join(dirpath,nomefile)
			#print (nomefile)
			parts = nomefile.split("-") 
		
			if(len(parts)==4):
				(anno,titolo,lingue,qualita)=parts
			else:
				titolo=nomefile
			
			command_line = "ffprobe INPUT"
			command_line = command_line.replace('INPUT', nome_file_completo)
			
			command_line_list = shlex.split(command_line)
			p = subprocess.Popen(command_line_list,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			output = p.communicate()
			out_list = (str( output[0], encoding='utf8' )).split("\n")
			commento = ''
			for line in out_list:
				if re.search('Stream #', line,re.I):
					commento += line+"|"

			
			
			print (''+titolo+';'+nome_file_completo+';'+commento+'')

def run(args):
	print ("Titolo;Trailer;Commento")
	show_file_in_dir(args.dirname)	 
	
	 
def main():

	parser = argparse.ArgumentParser(description='Genera la lista film in csv da importare in gcstar')
	parser.add_argument("dirname", help='directory in cui ci sono i film da analizzare')
	args = parser.parse_args()
	
	run(args)



if __name__ == '__main__':
	main()