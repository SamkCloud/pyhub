#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 201409
"""
Parse a file (utf-8 compatible
"""


import argparse
import re

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(args=None):

	out = open(args.output,'w',encoding='utf8')
	
	with open(args.input,'r',encoding='utf8') as f:
		for line in f:
			espressione = 'reg_exp_da_trovare'
			if not re.search(espressione, line,re.I):
				out.write(line)
			else: 
				out.write('NEW_STRING\n')
			

def main():
	
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument("input", help='directory in cui ci sono i film da analizzare')
	parser.add_argument('-o','--output',help='Output file name', default='output.txt')
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


