#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20131125
"""
Find recursively particualr MP3 Tag
"""


import argparse
import os
import subprocess, re

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(args=None):
	set_tag_in_dir(args.directory)
	
def set_tag_in_dir(subdir):
	for dirpath, dirnames, filenames in os.walk (subdir):
		for subdir in dirnames:
			set_tag_in_dir(subdir)
		for nomefile in filenames:
			full_filename = os.path.join(dirpath,nomefile)
			(filebase,estensione) = os.path.splitext( full_filename )
			if (estensione.lower() == '.mp3'): 
				analize_file(full_filename)
				
			elif (estensione.lower() == '.ogg'): 			
				print(full_filename + " ----> Estensione .ogg")
			

def analize_file(full_filename):
	p = subprocess.Popen(['eyeD3',full_filename],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	stdout, stderr = p.communicate()

	pattern = re.compile(b'.*Image.*')
	match = pattern.search(stdout)
	if match:
		print(full_filename+"\t--->YES_COVER")
	else:
		print(full_filename+"\t--->NO_COVER")


def main():
	

	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('-d','--directory', help='Starting directory',required=True)
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


