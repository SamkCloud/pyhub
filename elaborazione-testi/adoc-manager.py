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


def cmd_split():
	"""
	divide il file di input in più file, uno per 
	"""
	
	out_main = open(args.output,'w',encoding='utf8')
	(out_basename,out_ext) = os.path.splitext(args.output)
	
	indice_ = 0 
	
	with open(args.input,'r',encoding='utf8') as f:
		for line in f:
			if not re.search('== ', line,re.I):
				if (indice_ == 0 ):
					out_main.write(line)
				else:
					out.write(line)
			else: 
				if (indice_ > 0 ):
					out.close
				indice_ = indice_ +1
				# rimuovo gli accenti prima di inserirli nel file name
				line_sanitized = "".join([c for c in line if c.isalpha() or c.isdigit() or c==' ']).strip()

				out_filename = out_basename+'-'+str(indice_).zfill(3)+'-'+line_sanitized+out_ext
				out = open(out_filename,'w',encoding='utf8')
				out.write(line)
				line_main = 'include::'+out_filename+'[]\n'
				out_main.write(line_main)

				
def cmd_merge():
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
				
	
def cmd_divide_paragraph():
	# inserisce un '\n' dopo ogni . ! ? a fine riga
	out_main = open(args.output,'w',encoding='utf8')
	lines = open(args.input,'r',encoding='utf8').readlines()
	
	for line in lines:
		new_line1 = re.sub(r'\.\n', '.\n\n', line)
		new_line2 = re.sub(r'!\n', '!\n\n', new_line1)
		new_line3 = re.sub(r'\?\n', '?\n\n', new_line2)
		
		new_line = new_line3
		out_main.write(new_line)

	
	
				
def run():

	if args.split:
		cmd_split()
	elif args.merge: 
		cmd_merge()
	elif args.divide_paragraph:
		cmd_divide_paragraph()
				
	
def main():
	
	global args

	parser = argparse.ArgumentParser(description='Perform different task on adoc files')
	parser.add_argument("input", help='input file')
	parser.add_argument('-s','--split-chapter', dest='split',help='if set split the file in different file, one for each chapter',action='store_true')
	parser.add_argument('-m','--merge-chapter', dest='merge',help='if set merge the different file in one. It the opposite of -s',action='store_true')
	parser.add_argument('--divide-paragraph',help='insert a blanc line \n after a full stop or equivalent (.!?)',action='store_true')
	parser.add_argument('-o','--output',help='Output file name', default='output.adoc')
	args = parser.parse_args()

	run()

if __name__ == '__main__':
    main()
    