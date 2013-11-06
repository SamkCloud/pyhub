#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20131024
# last change: 20131026
 
"""
Video Catalog
"""

# TODO

import argparse
import os
import sqlite3
import subprocess, re

sqlite3_structre = "videocat_structre.sql"

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
	statinfo = os.stat(filename)
	file_info['size']=(statinfo.st_size)
	return file_info

def check_library(args):
	# check if the library exists and if not, create it
	print (args.library)
	conn = sqlite3.connect(args.library)
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	conn.commit()
	if cursor.fetchall() == []:
		if args.verbose :
			print_log("Database don't exists ... I'll create it")
		f = open(sqlite3_structre,'r')
		sql = f.read() 
		cursor.executescript(sql)
		if args.verbose :
			print_log("Database created")

		
def add_video_to_db(filename,args):
	# Add single video to the DB
	file_info = get_fileinfo(filename)
	print(file_info)
	
	conn = sqlite3.connect(args.library)
	cursor = conn.cursor()
	sql = "INSERT INTO file_list ('name','filesize') VALUES (?,?);"
	cursor.execute(sql,(filename,0000))
	conn.commit()
	
	if args.verbose :
		print_log("Added  "+ filename)
	

	
def add_directory(dirname,args):
	# add all the movie in a directory
	if args.verbose :
		print_log("Analizing "+ dirname)
	for dirpath, dirnames,files in os.walk(dirname):
		for filename in files:
			file_full_path = os.path.join(dirpath, filename)
			add_video_to_db(file_full_path,args)
			

def run(args=None):
	
	check_library(args)
	
	print ("Output file: %s" % args.output )
	if args.add_video:
		add_video(args.add_video,args)
	if args.directory_input:
		add_directory(args.directory_input,args)
		
	


def main():
	
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('-a','--add-video', help='Add single Video')
	parser.add_argument('-d','--directory-input',help='Directory where are ')
	parser.add_argument('-o','--output',help='Output file name', default='videocat.html')
	parser.add_argument('--library',help='Library name',default="videocat.sqlite")
	parser.add_argument('-v','--verbose',help='Verbose',action="store_true")
	
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
    


