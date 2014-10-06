#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20141006
"""
join imaged splitted 

"""

import argparse
import os
import subprocess
import shlex

def run(args=None):
	lista_file = []
	for file in os.listdir(args.input):			
		lista_file.append(file)
	lista_file.sort()
	#print(lista_file)
	
	for indice in range(1,300):
		
		command_line='find ./tmp/img -iname index-'+str(indice)+'_*'
		comando = shlex.split(command_line)
		output = subprocess.check_output(comando)
		number_of_file = len(output.decode().split('\n'))-1
		if number_of_file > 0 :
			command_line = 'convert tmp/img/index-'+str(indice)+'_[1-'+str(number_of_file)+'].png -append latex/Images/index-'+str(indice)+'.png'
			print(command_line)
			comando = shlex.split(command_line)
			
			output = subprocess.check_output(comando)
		
		
		
		
		

def main():
	
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument("input", help='input directory ')
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
