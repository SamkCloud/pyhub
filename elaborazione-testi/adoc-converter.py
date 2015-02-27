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
	p = subprocess.Popen(a_cmd) 					


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
		
		
	# esegue le conversioni	
	if args.conversion == 'adoc2html-asciidoctor':
		command_line = 'asciidoctor ' + args.input + ' -D '+args.output_dir
		exec_cmd(command_line)
		
def main():
	
	global args
	parser = argparse.ArgumentParser(description='Perform different task on adoc files')
	parser.add_argument("input", help='input file')
	parser.add_argument('-c','--conversion',help='type of conversion',
		choices=['adoc2html-asciidoctor', 'paper', 'scissors'])
	parser.add_argument('-D','--output-dir',help='Output Directory',default='./')
	parser.add_argument('--img-dir',help='Directory where are stored the img',default='img')
	parser.add_argument('-v','--verbose',help='Verbose',action='store_true')
	
	args = parser.parse_args()


	run()

	
if __name__ == '__main__':
    main()
    