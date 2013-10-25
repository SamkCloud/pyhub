#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20130804
"""
Simple argparse python script
"""


import argparse

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(args=None):
	
	print ("Input file: %s" % args.add_video )
	print ("Output file: %s" % args.output )
	print ("Output file: %s" % args.directory_input )


def main():
	

	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('-a','--add-video', help='Add single Video')
	parser.add_argument('-d','--directory-input',help='Directory where are ')
	parser.add_argument('-o','--output',help='Output file name', default='videocat.html')
	
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


