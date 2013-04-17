#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Script to choose random pictures from the digikam database
Copyright (C) 2008  Andreas Goelzer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


This program takes one random picture out of a sqlite-database
made by digikam.
This is useful for screensavers, xscreensaver-glslideshow in particular.
"""

#import sys;
#ef=open('/home/goelzera/Documents/Programme/python/xscreensaver-errlog','a')
#sys.stderr = ef

good_extensions = ('jpg', 'jpeg', 'pjpeg', 'pjpg', 'png', 'gif', 'tif', 'tiff', 'xbm', 'xpm')
bad_tags = "('private','me','Nophoto','Notmeanttobenice')"
#good_tags = "('public')"
good_tags = ""
attempts = 200


import sqlite3;
from sys import argv, exit;
from os.path import splitext;

digikamversion = "4";

if(len(argv) > 1):
	dirname = argv[len(argv) - 1]
	## Questi parametri dovrebbero essere passati dalla linea di comando
	db_dir = "/mnt/md0/giuliano/Immagini/digikam-config/"
	dirname = "/mnt/md0/giuliano/Photos"
else:
	##dirname = "/home/goelzera/Documents/Pictures"
	db_dir = "/mnt/md0/giuliano/Immagini/digikam-config/"
	dirname = "/mnt/md0/giuliano/Photos"
	
con = sqlite3.connect(db_dir + "/digikam" + digikamversion + ".db")
if(digikamversion == "4"):
	url = "relativePath"
	dirid = "album"
else:
	url = "url"
	dirid = "dirid"
	
#from time import time
#f=open('/home/goelzera/Documents/Programme/python/xscreensaver-log','a')
#f.write(str(time()) + '\t' + str(argv) + '\t')

#get tagids for bad tags
def getTagIdsFromNames(names):
	tag_ids = ' ';
	for row in con.execute("SELECT id FROM Tags WHERE name IN "+ names):
		tag_ids += str(row[0]) + ','
	tag_ids = '(' + tag_ids[:-1] + ')'
	return tag_ids

if(bad_tags != ""): bad_tag_ids = getTagIdsFromNames(bad_tags)
if(good_tags != ""): good_tag_ids = getTagIdsFromNames(good_tags)

file = 'none';
#search for images, take a random one out of the db and see if it fulfills the criteria
for attempt in range(attempts):
	#get a random picture, i guess this is the wrong way, performs horrible
	#truely random, but painfully slow
	#row = con.execute("SELECT id, name, $dirid FROM Images ORDER BY RANDOM() LIMIT 0,1").fetchone()
	#fast, but not as random
	row = con.execute("SELECT id, name, "+ dirid+" FROM Images WHERE id >= (abs(RANDOM()) % (SELECT max(id) FROM Images)) LIMIT 0,1").fetchone()
	#f.write(str(row[0]) + ',')
	
	#check for bad tag
	if(bad_tags != ""):
		if(con.execute("SELECT 1 FROM ImageTags WHERE imageid = " + str(row[0]) + " AND tagid IN "+ bad_tag_ids).fetchone()): continue

	#check for good tag
	if(good_tags != ""):
		if(not con.execute("SELECT 1 FROM ImageTags WHERE imageid = " + str(row[0]) + " AND tagid IN "+ good_tag_ids).fetchone()): continue


	#check for invalid extension
	ext = splitext(row[1])
	ext = ext[1][1:].lower()
	if(not ext in good_extensions): continue
	
	#not rejected, get directory
	drow = con.execute("SELECT "+url+" FROM Albums WHERE id = " + str(row[2])).fetchone()
	file = dirname + drow[0] + '/' + row[1]
	break

print file.encode('utf-8')

#f.write(file.encode('latin-1') + '\n')





