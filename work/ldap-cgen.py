#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20130804
"""
launch a command for every row in the input file es:
  ./ldap-cgen.py -i ../../../prg/work/input.txt -c ../../../prg/work/commands.txt
"""

import argparse
import subprocess 
import re



def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(args=None):
	c = open(args.command,'r')
	comando = c.readline()

	f = open(args.input, 'r')
	for line in f.readlines():
		campo = line.rstrip()
		comando1 = comando.replace("###1###",campo)
		#print(comando1)
		print(campo)
		print("###a###")
		result = (subprocess.getoutput(comando1))
		print(result)
		print(result[2])
		print("###b###")

def main():
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('-i','--input', help='Input file name',required=True)
	parser.add_argument('-c','--command', help='Command file name',required=True)
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    
