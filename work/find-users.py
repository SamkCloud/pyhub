#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20130804
"""
launch a command for every row in the input file es:
 ./find-users.py -i ../../work/input.txt -c ../../work/commands.txt
"""


import argparse
import subprocess 
import re



def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(args=None):
	c = open(args.command,'r')
	(modo, comando) = (c.readline()).split("\t")
	
	f = open(args.input, 'r')
	for line in f.readlines():
		(nome,cognome) = (line.rstrip()).split('. ')
		comando1 = comando.replace("###1###",cognome)
		result = (subprocess.getoutput(comando1)).split("\n")
		#print(result)
		for result_line in result:
			if re.search('(^cn:)', result_line,re.I):
				res_split = result_line.split(" ")
				res_split.append('#')
				nom1= res_split[2]
				if nom1[0] == nome:
					print(line.rstrip()+"\t"+result_line)

def main():
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('-i','--input', help='Input file name',required=True)
	parser.add_argument('-c','--command', help='Command file name',required=True)
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    
