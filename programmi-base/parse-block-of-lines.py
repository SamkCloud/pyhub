#!/usr/bin/python
# fa il parse di un file con i dati in multiriga
"""
file.txt =
ID: 1
Name: X
FamilyN: Y
Age: 20

ID: 2
Name: H
FamilyN: F
Age: 23

ID: 3
Name: S
FamilyN: Y
Age: 13

ID: 4
Name: M
FamilyN: Z
Age: 25
"""
import itertools

def isa_group_separator(line):
    return line=='\n'

with open('file.txt') as f:
	for key,group in itertools.groupby(f,isa_group_separator):
		#print(key,list(group))  # uncomment to see what itertools.groupby does.
		if not key:
			data={}
			for item in group:
				field,value=item.split(':')
				value=value.strip()
				data[field]=value
			print('{FamilyN} {Name} {Age}'.format(**data))

