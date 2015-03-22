#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150322
"""
CSV for python
"""


import csv


# ------------------- Using writerow

f = open('tmp_base.csv', 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('Title 1', 'Title 2', 'Title 3') )
    for i in range(10):
        writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
finally:
    f.close()

print(open('tmp_base.csv', 'rt').read())


# ------------------- Using DIC

with open('tmp_dict.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})


with open('tmp_dict.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		print(row['first_name'], row['last_name'])