#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150224
"""
Manage adoc format
	-s Split the file in different file, one for each chapter
"""

import os
import re
import argparse
import unicodedata


def cmd_split(args=None):
	"""
	divide il file di input in più file, uno per capitolo
	"""
	
	out_main = open(args.output,'w',encoding='utf8')
	(out_basename,out_ext) = os.path.splitext(args.output)
	
	indice_capitolo = 0 
	
	with open(args.input,'r',encoding='utf8') as f:
		for line in f:
			if not re.search('== ', line,re.I):
				if (indice_capitolo == 0 ):
					out_main.write(line)
				else:
					out.write(line)
			else: 
				if (indice_capitolo > 0 ):
					out.close
				indice_capitolo = indice_capitolo +1
				# rimuovo gli accenti prima di inserirli nel file name
				line_sanitized = "".join([c for c in line if c.isalpha() or c.isdigit() or c==' ']).strip()

				out_filename = out_basename+'-'+str(indice_capitolo).zfill(3)+'-'+line_sanitized+out_ext
				out = open(out_filename,'w',encoding='utf8')
				out.write(line)
				line_main = 'include::'+out_filename+'[]\n'
				out_main.write(line_main)

				
def cmd_merge(args=None):
	"""
	ricrea il file dopo essere stato diviso
	"""
	out_main = open(args.output,'w',encoding='utf8')
	
	with open(args.input,'r',encoding='utf8') as f:
		for line in f:
			include_search = re.search('include::(.*)\[\]', line,re.I)
			if not include_search:
				out_main.write(line)
			else: 
				with open(include_search.group(1),'r',encoding='utf8') as f_chapther:
					for line_chapter in f_chapther:
						out_main.write(line_chapter)
				
				

				
def run(args=None):

	if args.split:
		cmd_split(args)
	elif args.merge: 
		cmd_merge(args)
				
	
def main():
	

	parser = argparse.ArgumentParser(description='Perform different task on adoc files')
	parser.add_argument("input", help='input file')
	parser.add_argument('-s','--split-chapter', dest='split',help='if set split the file in different file, one for each chapter',action='store_true')
	parser.add_argument('-m','--merge-chapter', dest='merge',help='if set merge the different file in one. It the opposite of -s',action='store_true')
	parser.add_argument('-o','--output',help='Output file name', default='output.adoc')
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    