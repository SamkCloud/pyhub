#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150224
"""
Convert adoc format in different output format
"""

import os
import re
import argparse
import shlex
import subprocess

def emit_verbose(line):
	# if verbose is on emit the string
	if args.verbose:
		print(line)
					
def exec_cmd(command_line):
	# esegue un comando
	a_cmd = shlex.split(command_line)
	emit_verbose(command_line)
	p = subprocess.call(a_cmd) 					


def create_directory():	
	# Create the output directory if not exists
	if not os.path.exists(args.output_dir):
		emit_verbose("Directory "+args.output_dir+ " don't exists ... I'll create it")
		os.makedirs(args.output_dir)
		
def create_img_link():
	# crea il link alle immagini se non esistente
	output_img_dir = os.path.realpath(args.output_dir)+'/'+args.img_dir
	input_img_dir = os.path.dirname(os.path.realpath(args.input))+'/'+args.img_dir
	
	if not os.path.exists(output_img_dir):
		os.symlink(input_img_dir,output_img_dir)

def run():
	
	emit_verbose("script start")
	
	create_directory()
	create_img_link()
	
	file_basename = os.path.splitext(os.path.basename(args.input))[0]
	
		
	# esegue le conversioni	
	if args.conversion == 'adoc2html-asciidoctor':
		command_line = 'asciidoctor ' + args.input + ' -D '+args.output_dir
		exec_cmd(command_line)
		output_filename = os.path.join(args.output_dir,file_basename+'.html')
			
		
	elif args.conversion == 'adoc2docbook-asciidoctor':
		command_line =	'asciidoctor -b docbook ' + args.input + ' -D '+args.output_dir
		exec_cmd(command_line)
		output_filename = os.path.join(args.output_dir,file_basename+'.xml')
	
	elif args.conversion == 'docbook2epub-xsltproc':
		output_filename = os.path.join(args.output_dir,file_basename+'.epub')
	#	xsltproc /usr/share/xml/docbook/xsl-stylesheets-1.78.1/epub/docbook.xsl $INPUT_FILE 
	#	echo "application/epub+zip" > mimetype
	#	cd OEBPS
	#	ln -s ../../../2.edit/img/ img
	#	cd ..
	#	zip -0Xq  $filename.epub mimetype
	#	zip -Xr9D $filename.epub OEBPS META-INF 
	#	rm -fr OEBPS META-INF mimetype'''
		
		command_line =	'xsltproc /usr/share/xml/docbook/xsl-stylesheets-1.78.1/epub/docbook.xsl -o '+args.output_dir + '/ ' + args.input 
		exec_cmd(command_line)
		
		emit_verbose("write 'application/epub+zip' in  mimetype")
		with open(os.path.join(args.output_dir,'mimetype'), "wt") as out_file:
			out_file.write("application/epub+zip")
		
		### USARE il modulo zipfile ... 
		
		command_line =	'zip -0Xq  '+ output_filename +' '+args.output_dir+'/mimetype' +' '+args.output_dir+'/mimetype'
		#command_line =	'7z a -tzip '+ output_filename +' '+args.output_dir+'/mimetype' +' '+args.output_dir+'/mimetype'
		exec_cmd(command_line)
		
		command_line =	'zip -Xr9D  '+ output_filename +' '+args.output_dir+'/OEBPS '+args.output_dir+'/META-INF '+ args.output_dir+'/'+args.img_dir
		#command_line =	'7z a -l -tzip  '+ output_filename +' '+args.output_dir+'/OEBPS '+args.output_dir+'/META-INF '+ args.output_dir+'/'+args.img_dir
		exec_cmd(command_line)
		
	
	

	# applica le patch se presenti
	if((args.patch_file != None) and (os.path.isfile(args.patch_file))):
		emit_verbose("Patch output file")
		command_line = 'patch '+ output_filename + ' '+args.patch_file
		exec_cmd(command_line)		
		
		
def main():
	
	global args
	parser = argparse.ArgumentParser(description='Perform different task on adoc files')
	parser.add_argument("input", help='input file')
	parser.add_argument('-c','--conversion',help='type of conversion',
		choices=[	'adoc2html-asciidoctor', 
					'adoc2docbook-asciidoctor',
					'docbook2epub-xsltproc',
					])
	parser.add_argument('-D','--output-dir',help='Output Directory',default='./')
	parser.add_argument('--img-dir',help='Directory where are stored the img',default='img')
	parser.add_argument('--patch-file',help='Directory where are stored the patch',default=None)
	parser.add_argument('-v','--verbose',help='Verbose',action='store_true')
	
	args = parser.parse_args()


	run()

	
if __name__ == '__main__':
    main()
    