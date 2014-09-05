#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20120326
"""
Program to read Google contact CSV and export to PDF
Export in Outlook FORMAT CSV

Work with in-file ANSI and UNIX CR
"""

"""
TODO
sort elements by Last Name 


"""

import optparse
import csv

from datetime import *


def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def emit_html_header_table(fields):
	dim = int(round(100/len(fields)))
	out = "<table>\n<thead>\n\t<tr>\n"
	for field in fields:
		out +=  '\t\t<th width="'+str(dim)+'%">'+field+"</th>\n"
	out +=  "\t</tr>\n</thead><tbody>"
	
	return out

def emit_html_footer_table():
	out = "</tbody></table>\n"
	return out

	
def run(options=None,arguments=None):
	
	printed_fileds = ["First Name","Last Name","Home Phone","Business Phone","Mobile Phone","Pager","Birthday"]
	pdf_fields = ["Nome","Casa","Ufficio","Cell","Tel2","Compleanno"]
	
	csv_file_input = arguments[0]
	
	
	out_html = emit_html_header_table(printed_fileds)
	
	
	data_row = []
	
	try:
		
		row_list = csv.reader(open(csv_file_input))
		
		
		for row in row_list:
			line = [row['Last Name']+' '+row["First Name"],row["Home Phone"],row["Business Phone"],row["Mobile Phone"],row["Pager"],row["Birthday"]]
			data_row.append(line)
			out_html = out_html + "<tr>"
			for filed in printed_fileds:
				out_html = out_html +  "<td>"+str(row[filed])+"</td>\n"
			out_html = out_html + "</tr>"
			
	finally:
		dommy = 0
	
	footer = emit_html_footer_table()
	
	out_html = out_html + footer
	f = open("html_output.html", 'w')
	f.write(out_html)
	f.close()
	
	data_row.sort()
		
	# ############# PDF
	mypdf=MyFPDF(orientation='L',unit='mm',format='A4')
	mypdf.add_page()
	mypdf.FancyTable(pdf_fields,data_row);
	mypdf.output('contacts.pdf','F')

	


	

		
	
#    if options.show_person:
#        print 'Hello %s' % options.show_person
#
#    if options.show_home:
#        print 'La casa è: %s' % options.show_home
#         


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


    options, arguments = p.parse_args()

    if len(arguments) != 1:
        p.error("incorrect number of arguments")

    run(options,arguments)
 

if __name__ == '__main__':
    main()
    


