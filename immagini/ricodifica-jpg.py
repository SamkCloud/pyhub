#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150319

"""
riconverte un'immagine jpg per ridurre la qualità e la dimensione

 convert -strip -interlace Plane -gaussian-blur 0.05 -quality 85% src.jpg dst.jpg
"""

import argparse
import subprocess
import shlex

def emit_verbose(line):
	# if verbose is on emit the string
	if args.verbose:
		print(line)
					
def exec_cmd(command_line):
	# esegue un comando
	a_cmd = shlex.split(command_line)
	emit_verbose(command_line)
	p = subprocess.call(a_cmd) 			

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run():
	command_line = 'convert -strip -interlace Plane -gaussian-blur 0.05 -quality %s%% %s %s' % (args.quality, args.input, args.input)
	exec_cmd(command_line)

def main():
	global args
	
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument("input", help='input file da ridurre')
	parser.add_argument('-v','--verbose', help='Verbose',action='store_true')
	parser.add_argument('-q','--quality', help='Quality of the jpg (default 85) ',type=int,default=85)
	args = parser.parse_args()

	run()

if __name__ == '__main__':
    main()
    

