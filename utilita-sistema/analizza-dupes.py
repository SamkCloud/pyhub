#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150318
"""
esamina i file prodotti da 'fdupes -R ./ > dup.txt' e evidenzia quelli da cancellare in base ad alle directory di preferenza


TODO: 
* [ ] Usare la libreria csv per creare il csv
"""


import argparse
import itertools

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def isa_group_separator(line):
    return line=='\n'


def run(args=None):
	
	f_out= open(args.output, 'wt') 
	f_out.write("priorita\tfile\tT-C\tcomando\n")
	
	if args.directory_discarded == None:
		args.directory_discarded = list()
	
	if args.directory_wanted == None:
		args.directory_wanted = list()
		
	
	with open(args.input) as f_in:
		for key,group in itertools.groupby(f_in,isa_group_separator):
			new_list = list()
			#print(list(group))
			for line in list(group):
				new_item = (len(args.directory_wanted),line)
				for index_dir,dir in enumerate(args.directory_wanted):
					if line.startswith(dir):
						priority = index_dir
						new_item = (index_dir,line)

				for index_dir,dir in enumerate(args.directory_discarded):
					if line.startswith(dir):
						priority = len(args.directory_wanted)+len(args.directory_discarded)+1-index_dir
						new_item = (priority,line)
	
				new_list.append(new_item)

			new_list.sort()
			
			tieni_o_cancella = 'T'
			for (key,item) in new_list:
				# se item non è una riga vuota
				if item.strip():
					if tieni_o_cancella == 'C':
						comando_rm = 'rm "'+item.strip()+'"'
					else:
						comando_rm = ''
					linea=str(key)+"\t"+item.strip()+"\t"+tieni_o_cancella+'\t'+comando_rm+"\n"
					tieni_o_cancella = 'C'
					f_out.write(linea)
			f_out.write("\n")
	

def main():
	
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('input', help='file dup.txt da analizzare')
	parser.add_argument('-d','--directory-wanted',help='directory di preferenza (può essere usato più volte)',action='append',default=None)
	parser.add_argument('-D','--directory-discarded',help='directory Da scartare (può essere usato più volte)',action='append',default=None)
	parser.add_argument('-o','--output',help='output file',default='output.csv')
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


