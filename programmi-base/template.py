#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150301
"""
Template for python
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

def run(args=None):
	print ("Input file: %s" % args.input )
	print ("Output file: %s" % args.output )
	print ("Output file: %s" % args.num )


def main():
	
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument("dirname", help='directory in cui ci sono i film da analizzare')
	parser.add_argument('-i','--input', help='Input file name',required=True)
	parser.add_argument('-v','--verbose', help='Verbose',action='store_true')
	parser.add_argument('-o','--output',help='Output file name', default='file.txt')
	parser.add_argument('-n','--number',help='Numer of times', dest="num", type=int )
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


