#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150215
"""
Convert file to 
"""


import argparse
import sys

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(arguments):
	print ("Input file: %s" % arguments.input )

	if arguments.codifica == 'h264':
		video_options 	= "-vcodec libx264 -preset veryslow -crf 20 -threads 0"
		audio_opt 		= "-acodec aac -ab 128k -ac 2 -strict -2"
		estensione_tmp 	= '.mp4'
	
	elif arguments.codifica == 'loseless':
		video_options = "-c:v libx264 -preset veryslow -qp 0"
		audio_opt = "-acodec aac -ab 128k -ac 2 -strict -2"
		estensione_tmp = '.mkv'
	
	else:
		sys.exit("Error: Codifica non riconosciuta")
		
		
	

def main():
	

	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('input')
	parser.add_argument('--codifica','-c',default='h264',help='Scegli il tipo di codifica (h264|loseless)')
	
	arguments = parser.parse_args()

	run(arguments)

if __name__ == '__main__':
    main()
    
