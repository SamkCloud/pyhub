#!/usr/bin/python2
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

from fpdf import FPDF
from datetime import *


class MyFPDF(FPDF):
	def header(self):
		# self.image('tutorial/logo_pb.png',10,8,33)
		#self.set_font('Arial','B',12)
		#self.cell(80)
		#self.cell(30,10,'Title',1,0,'C')
		#self.ln(20)
		none = 0 

	def footer(self):
		self.set_y(-15)
		self.set_font('Arial','I',8)
		#txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
		txt = str(date.today().day) + '/' + str(date.today().month) + '/' + str(date.today().year)
		self.cell(0,10,txt,0,0,'C')
	
	def FancyTable(self,headers,data):
		""" output a coulored  table """
		self.set_fill_color(255,0,0)
		self.set_text_color(255)
		self.set_draw_color(128,0,0)
		self.set_line_width (.3)
		self.set_font('Arial','B',9)
		#Header
		col_width=[60,40,40,40,40,30]
		#for($i=0;$i<count($header);$i++)
		i = 0
		for single_header in  headers:
		#	this.Cell($w[$i],7,$header[$i],1,0,'C',true);
			self.cell(col_width[i],7,single_header,1,0,'C',True)
			i += 1
		#this.Ln();
		self.ln()
		#	//Color and font restoration
		self.set_fill_color(224,235,255)
		self.set_text_color(0)
		self.set_font('')
#			//Data
		fill = False
		for row in data:
			i = 0
			for field in headers:
				self.cell(col_width[i],5,row[i],'LR',0,'L',fill)
				i += 1
			self.ln()
			fill =  not fill
			#self.cell(250,0,'','T')
	#this.Cell(array_sum($w),0,'','T');

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(options=None,arguments=None):
	
	printed_fileds = ["First Name","Last Name","Home Phone","Business Phone","Mobile Phone","Pager","Birthday"]
	pdf_fields = ["Nome","Casa","Ufficio","Cell","Tel2","Compleanno"]
	
	csv_file_input = arguments[0]
	
	
	out_html = emit_html_header_table(printed_fileds)
	
	
	data_row = []
	f = open(csv_file_input, 'rt')
	try:
		reader = csv.DictReader(f)
		
		
		for row in reader:
			line = [row['Last Name']+' '+row["First Name"],row["Home Phone"],row["Business Phone"],row["Mobile Phone"],row["Pager"],row["Birthday"]]
			data_row.append(line)
			out_html += "<tr>"
			for filed in printed_fileds:
				out_html += "<td>"+str(row[filed])+"</td>\n"
			out_html += "</tr>"
	finally:
		f.close()
	
	out_html += emit_html_footer_table()
	f = open("html_output.html", 'w')
	f.write(out_html)
	f.close()
	
	data_row.sort()
		
	# ############# PDF
	mypdf=MyFPDF(orientation='L',unit='mm',format='A4')
	mypdf.add_page()
	mypdf.FancyTable(pdf_fields,data_row);
	mypdf.output('contacts.pdf','F')

	

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
    


