#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20130730
"""
Query digikam db
"""



import optparse
import sqlite3
import os

def print_r(v):
	return '%s = %r %s' % (v, v, type(v))

def run(options=None):
	print(options.digikam_db)
	# TODO check if the db is present
	conn = sqlite3.connect(options.digikam_db)
	c = conn.cursor()
	
	t = (options.tag,)
	c.execute('SELECT id FROM tags WHERE name=?', t)
	tag_id=c.fetchone()
	
	c.execute('SELECT album, name FROM Images INNER JOIN ImageTags ON (Images.id = ImageTags.imageid AND ImageTags.tagid=?)',tag_id)
	print(c.fetchone())
	
	
#	if options.show_person:
#		print('Hello %s' % options.show_person)

#	if options.show_home:
#		print('La casa è: %s' % options.show_home)
	
	
		 


def main():
	usage = "usage: %prog [options] arg"
	p = optparse.OptionParser(usage)
	p.add_option('--person',
				 '-p',
				 default='world',
				 help='scegli il tipo di pesona',
				 dest='show_person')

	p.add_option('--casa',
				 '-c',
				 default='',
				 help='Mostra la casa',
				 dest='show_home')
				 
	p.add_option('--digikam-db',
				default=os.path.expanduser('~/tmp/digikam4.db'),
				help='Default db directory',
				dest='digikam_db')
	
	p.add_option('--tag',
				default='Barca',
				help='Tag to search',
				dest='tag')


	options, arguments = p.parse_args()

	if len(arguments) != 1:
		p.error("incorrect number of arguments")

	run(options)
 

if __name__ == '__main__':
	main()
	


