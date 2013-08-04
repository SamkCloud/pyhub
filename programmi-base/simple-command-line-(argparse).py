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
	print ("Input file: %s" % args.input )
	print ("Output file: %s" % args.output )
	print ("Output file: %s" % args.num )


def main():
	

	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('-i','--input', help='Input file name',required=True)
	parser.add_argument('-o','--output',help='Output file name', default='file.txt')
	parser.add_argument('-n','--number',help='Numer of times', dest="num", type=int )
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


