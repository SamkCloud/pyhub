#!/usr/bin/python
import os


def show_file_in_dir(dir):
	for dirpath, dirnames, filenames in os.walk (dir):
		for subdir in dirnames:
			show_file_in_dir(subdir)
		for nomefile in filenames:
			print dirpath+'/'+nomefile
	
show_file_in_dir('./')
