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

def run(options=None):
	#print(options.digikam_db)
	# TODO check if the db is present
	conn = sqlite3.connect(options.digikam_db)
	c = conn.cursor()
	
	# Extract all album and insert them into a dictionary 
	a = c.execute('SELECT id,relativePath FROM Albums')
	album= {}
	for row in a:
		album[row[0]]=row[1]
		
	
	t = (options.tag,)
	c.execute('SELECT id FROM tags WHERE name=?', t)
	tag_id=c.fetchone()
	
	c.execute('SELECT album, name FROM Images INNER JOIN ImageTags ON (Images.id = ImageTags.imageid AND ImageTags.tagid=?)',tag_id)
	#print(c.fetchone())
	for row in c:		
		file = album[row[0]]+'/'+row[1]
		
		if options.show=='List':
			print(file)
		elif options.show=='ln':
			line = 'ln -s "'+os.path.expanduser('~')+'/Photos'+file+'"'
			print(line)
		
	
	
#	if options.show_person:
#		print('Hello %s' % options.show_person)

#	if options.show_home:
#		print('La casa è: %s' % options.show_home)
	
	
		 


def main():
	usage = "usage: %prog [options]"
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

	p.add_option('--show',
				'-s',
				default='List',
				help='How the data must be shown (List|ln)',
				dest='show')

	

	options, arguments = p.parse_args()

	if len(arguments) != 0:
		p.error("incorrect number of arguments")

	run(options)
 

if __name__ == '__main__':
	main()
	


