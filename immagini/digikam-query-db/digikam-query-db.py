#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 
# first version 20130730
# version 20130803

"""
Query digikam db
"""



import optparse
import sqlite3
import os

def print_r(v):
	return '%s = %r %s' % (v, v, type(v))

def run(options=None,arguments=None):
	#print(options.digikam_db)
	# TODO check if the db is present
	conn = sqlite3.connect(options.digikam_db)
	c = conn.cursor()
	
	# Extract all album and insert them into a dictionary 
	a = c.execute('SELECT id,relativePath FROM Albums')
	album= {}
	for row in a:
		album[row[0]]=row[1]

	t = arguments
	c.execute('SELECT id FROM tags WHERE name=?', t)
	tag_id=c.fetchone()
	
	c.execute('SELECT album, name, id FROM Images INNER JOIN ImageTags ON (Images.id = ImageTags.imageid AND ImageTags.tagid=?) ORDER BY album',tag_id)
	for row in c:		
		file = album[row[0]]+'/'+row[1]
		if options.show=='List':
			line = file
		elif options.show=='ln':
			line = 'ln -s "'+os.path.expanduser('~')+'/Photos'+file+'"'
		elif options.show=='GPS':
			line = 'exiftool -GPSLongitudeRef=E -GPSLongitude='+options.GPSLongitude+' -GPSLatitudeRef=N -GPSLatitude='+options.GPSLatitude+' "'+os.path.expanduser('~')+'/Photos'+file+'"'
		print(line)
	


		 


def main():
	usage = "usage: %prog [options] Tags"
	p = optparse.OptionParser(usage)
				 
	p.add_option('--digikam-db',
				default=os.path.expanduser('~/tmp/digikam-test/digikam4.db'),
				help='Default db directory',
				dest='digikam_db')

	p.add_option('--show',
				'-s',
				default='List',
				help='How the data must be shown (List|ln|GPS)',
				dest='show')
	p.add_option('--GPSLatitude',
				default='',
				help='GPS Latitude coordinate to set es: 48.677952 ',
				dest='GPSLatitude')
	p.add_option('--GPSLongitude',
				default='',
				help='GPS Longitude coordinate to set es: 11.099678 ',
				dest='GPSLongitude')
	
	

	options, arguments = p.parse_args()

	if len(arguments) != 1:
		p.error("incorrect number of arguments Insert Tag Name")

	run(options,arguments)
 

if __name__ == '__main__':
	main()
	


