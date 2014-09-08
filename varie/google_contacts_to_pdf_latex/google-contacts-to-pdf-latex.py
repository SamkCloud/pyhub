#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20140908


"""
Program to read Google contact CSV and export to PDF
Export in Outlook FORMAT CSV

Work with csv-in-file ANSI (iso-8859-1) and UNIX CR
"""

"""
TODO

"""

import argparse
import csv
import fileinput

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def default_multiple_page_tex():
	out = '''\\documentclass[a4paper,12pt]{article}
\\begin{document}
###CONTENT###
\\end{document}
'''
	return out
	
def default_single_page_tex():

	out = '''\\documentclass[a4paper,landscape,12pt]{article}
\\usepackage{longtable}
\\usepackage{graphicx}
\\usepackage[table,xcdraw]{xcolor}
\\usepackage[margin=1.5cm]{geometry}

%per mettere la data nel footnote
\\usepackage{fancyhdr}
\\usepackage[italian]{babel}
\\usepackage{datetime}
\\renewcommand{\\today}{ \\the\\day\\ \\monthname\\ \\the\\year}

\\fancyhf{}
\\fancyfoot[C]{\\today\\ \\currenttime}
\\pagestyle{fancy}
%

\\begin{document}
\\footnotesize  % Switch from 12pt to 11pt; otherwise, table won't fit
\\begin{longtable}{@{\\extracolsep}lllllll}

\\hline\\hline %inserts double horizontal lines
\\rowcolor[HTML]{FF0000} 
 	{\\color[HTML]{FFFFFF} \\textbf{Cognome}} & 
	{\\color[HTML]{FFFFFF} \\textbf{Nome}} & 
	{\\color[HTML]{FFFFFF} \\textbf{Casa}} & 
	{\\color[HTML]{FFFFFF} \\textbf{Ufficio}} & 
	{\\color[HTML]{FFFFFF} \\textbf{Cell}} & 
	{\\color[HTML]{FFFFFF} \\textbf{Tel2}} & 
	{\\color[HTML]{FFFFFF} \\textbf{Compleanno}} \\\\
	
\\hline\\hline %inserts double horizontal lines	
\\endhead
###CONTENT###
\\end{longtable}

\\end{document}
'''
	
	return out

def emit_multiple_page(args=None):
	# genera un latex con tutti i dati in versione agendina
	printed_fileds = ["Last Name","First Name","Home Phone","Business Phone","Mobile Phone","Pager","Birthday"]
	data_row = []
	
	with open(args.csvfile , newline='', encoding='iso-8859-1') as csv_file_input:
		for row in csv.DictReader(csv_file_input, delimiter=','):
			line_latex = ''
			campi_tmp = []
			for filed in printed_fileds:
				if (filed == "Last Name"):
					campi_tmp.append(filed+': \\textbf{'+row[filed]+'}\\newline')	
				else: 
					campi_tmp.append(filed+': '+row[filed]+'\\newline')	
			line_latex = "\n".join(campi_tmp)
			data_row.append(line_latex)
			data_row.append('\\rule{\\textwidth}{1pt}')
	
	return "\n".join(data_row)
	
	
	
def emit_single_page(args=None):
	# genera un latex con tutti i dati in versione tabellare (es da mettere in portafoglio)
	
	
	printed_fileds = ["Last Name","First Name","Home Phone","Business Phone","Mobile Phone","Pager","Birthday"]
	row_color = ['FFFFFF','DDDDDD','FFFFFF']
	data_row = []
	i = -1
	
	with open(args.csvfile , newline='', encoding='iso-8859-1') as csv_file_input:
		for row in csv.DictReader(csv_file_input, delimiter=','):
	
			line_latex = ''
			campi_tmp = []
			for filed in printed_fileds:
				campi_tmp.append(row[filed])
				
			line_latex = "&".join(campi_tmp)
			
			i = (i+1) % len(row_color)
			data_row.append('\\rowcolor[HTML]{'+row_color[i]+'}')
			data_row.append(line_latex+'\\\\')
	
	return "\n".join(data_row)



	
def run(args=None):
	if (args.format == 's'): 
		latext_core = emit_single_page(args)
		template = default_single_page_tex()
	elif (args.format == 'm'): 
		latext_core = emit_multiple_page(args)
		template = default_multiple_page_tex()
	else:
		print('Format not know')

	if (args.template != ''):
		print("TODO: caricare un template")
	
	out = template.replace("###CONTENT###",latext_core)

	if (args.outfile == ''):
		print(out)
	else:
		f = open(args.outfile, 'wt')
		f.write(out)
	
	
def main():
	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument("csvfile", help='File CSV con le informazioni (in formato Outlook)')
	parser.add_argument('-t','--template',help='Latex template', default = '')
	parser.add_argument('-f','--format',help='Format s: single_page  m: multiple_page ', default = 's')
	parser.add_argument('-o','--outfile',help='Outputfile', default = '')
	
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
