#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20131024
# last change: 20141216
 
"""
Video Catalog to csv
scansiona una directory con le subdirectory e esporta in un file le informazioni relative ai file video
"""

# TODO
# capire se fa anceh le subdirectory .... probabilmente no

import argparse
import os
import subprocess, re
import csv


def print_log(line):
	"""Write the log """
	print("YYYYMMAA-HHMM:"+line)

def print_r(v):
	return '%s = %r %s' % (v, v, type(v))

 
def get_videoinfo(pathtovideo):
	file_info =  {}
	
	
	p = subprocess.Popen(['ffprobe', '-i', pathtovideo],
	stdout=subprocess.PIPE,
	stderr=subprocess.PIPE)
	stdout, stderr = p.communicate()


	# Video pixel Size
	pattern = re.compile(b'Stream.*Video.*([0-9]{3,})x([0-9]{3,})')
	match = pattern.search(stderr)
	if match:
		file_info['Xsize'] , file_info['Ysize']  = map(int, match.groups())
	else:
		file_info['Xsize'] = file_info['Ysize']  = 0

	# Video Codec  
	pattern = re.compile(b'Stream.*Video.*:\s([a-z0-9]{,})')
	match = pattern.search(stderr)
	if match:
		Vcodec1= match.groups()[0]
		file_info['Vcodec'] = Vcodec1.decode(encoding='UTF-8')
	else:
		file_info['Vcodec']  = "NONE"
	# Bitrate
	pattern = re.compile(b'Duration.*bitrate.*:\s([0-9]{,})')
	match = pattern.search(stderr)
	if match:
		file_info['bitrate'] = int(match.groups()[0])
	else:
		file_info['bitrate'] = "NONE"

	# Duration
	pattern = re.compile(b'Duration.*([0-9]{2,2}):([0-9]{2,2}):([0-9]{2,2})')
	match = pattern.search(stderr)
	if match:
		h,m,s = map(int, match.groups())
		file_info['duration'] = h*3600+m*60+s

	else:
		file_info['duration'] =  0
	# Audio Codec  
	pattern = re.compile(b'Stream.*Audio.*:\s([a-z0-9_]{,})')
	match = pattern.search(stderr)
	if match:
		Acodec1= match.groups()[0]
		file_info['Acodec']= Acodec1.decode(encoding='UTF-8')
		
	else:
		file_info['Acodec'] = "NONE"


	# Container
	pattern = re.compile(b'Input.*,\s([a-z0-9]{,}),')
	match = pattern.search(stderr)
	if match:
		Container= match.groups()[0]
		file_info['Container']= Container.decode(encoding='UTF-8')
		
	else:
		file_info['Container']= "NONE"
	return file_info
	
def get_fileinfo(filename):
	file_info =  {}
	
	(file_info['path'],file_info['filename']) = os.path.split(filename)
		
	statinfo = os.stat(filename)
	file_info['filesize']=(statinfo.st_size)
	
	#TODO if VIDEOFILE
	file_info1 =  dict (file_info, **(get_videoinfo(filename) ))
	
	return file_info1


def add_directory(dirname,args):
	f = open(args.output, 'wt')
	fieldnames = ('path','filename','bitrate', 'Container', 'Acodec', 'duration', 'Ysize', 'Xsize', 'filesize', 'Vcodec' )
	writer = csv.DictWriter(f, fieldnames=fieldnames)
	headers = dict( (n,n) for n in fieldnames )
	writer.writerow(headers)	
	
	# add all the movie in a directory
	if args.verbose :
		print_log("Analizing "+ dirname)
	for dirpath, dirnames,files in os.walk(dirname):
		for filename in files:
			file_full_path = os.path.join(dirpath, filename)
			#			print(file_full_path,args)
			file_info = get_fileinfo(file_full_path)
			file_info_keys = file_info.keys()
			file_info_values = list(file_info.values())
			print(file_info)
			writer.writerow(file_info)
	
	f.close()
	
			

def run(args=None):
	
	
	print ("Output file: %s" % args.output )
	
	if args.directory_input:
		add_directory(args.directory_input,args)


def main():
	
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('-d','--directory-input',help='Directory where are ')
	parser.add_argument('-o','--output',help='Output file name', default='videocat.csv')
	parser.add_argument('-v','--verbose',help='Verbose',action="store_true")
	
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


