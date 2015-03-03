#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd
# inital release 20140908
# version 20140909


#
#Ricordarsi di stampare l'agenda con l'opzione fronte-retro : (short edge TOP )
#

"""
Program to read Google contact CSV and export to PDF
Export in Outlook FORMAT CSV
Work with csv-in-file ANSI (iso-8859-1) 
"""

"""
TODO

"""

import argparse
import csv
import fileinput
import os

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def default_multiple_page_tex():
	out = '''\\documentclass[a4paper,12pt]{article}
\\title{Agenda}

% imposta la lingua italiana
\\usepackage[italian]{babel}
\\usepackage[utf8x]{inputenc}

%disabilita l'identazione 
\\setlength{\parindent}{0pt}

% genera il libretto 
\\usepackage{geometry}
\\geometry {centering,nohead }
\\geometry{width=108.5mm,height=170mm}


\\usepackage[print,1to1]{booklet}
\\nofiles
\\pagespersignature{36}
%


\\begin{document}
\\setpdftargetpages
\\maketitle
\\newpage
###CONTENT###
\\end{document}
'''
	return out
	
def default_single_page_tex():

	out = '''\\documentclass[a4paper,landscape,12pt]{article}
\\usepackage[utf8x]{inputenc}
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
	# i campi complessivi sono
	#First Name	Middle Name	Last Name	Title	Suffix	Initials	Web Page	Gender	Birthday	Anniversary	Location	Language	Internet Free Busy	Notes	E-mail Address	E-mail 2 Address	E-mail 3 Address	Primary Phone	Home Phone	Home Phone 2	Mobile Phone	Pager	Home Fax	Home Address	Home Street	Home Street 2	Home Street 3	Home Address PO Box	Home City	Home State	Home Postal Code	Home Country	Spouse	Children	Manager's Name	Assistant's Name	Referred By	Company Main Phone	Business Phone	Business Phone 2	Business Fax	Assistant's Phone	Company	Job Title	Department	Office Location	Organizational ID Number	Profession	Account	Business Address	Business Street	Business Street 2	Business Street 3	Business Address PO Box	Business City	Business State	Business Postal Code	Business Country	Other Phone	Other Fax	Other Address	Other Street	Other Street 2	Other Street 3	Other Address PO Box	Other City	Other State	Other Postal Code	Other Country	Callback	Car Phone	ISDN	Radio Phone	TTY/TDD Phone	Telex	User 1	User 2	User 3	User 4	Keywords	Mileage	Hobby	Billing Information	Directory Server	Sensitivity	Priority	Private	Categories

	printed_fileds = ["Home Phone","Business Phone","Mobile Phone","Pager","Other Phone"]
	tranlated_fields = {"Home Phone":"Casa","Business Phone":"Ufficio","Mobile Phone":"Cellulare","Pager":"Tel2","Other Phone":"Altro Telefono"}
	#"Last Name","First Name ... " are append at the beginning
	data_row = []
	
#	with open(args.csvfile , newline='', encoding='iso-8859-1') as csv_file_input:
	with open(args.csvfile , 'rU', encoding='iso-8859-1') as csv_file_input:
		csv_row = csv.DictReader(csv_file_input, delimiter=',')
		for row in csv_row:
			line_latex = ''
			campi_tmp = []
	
			# Aggiungo il titolo (Last name + first name + Middle Name)
			if(row["Company"] != ''):
				line = '\\textbf{'+row["Company"]+' '+row["Last Name"]+' '+row["First Name"]+' '+row["Middle Name"]+'}'
			else:
				line = '\\textbf{'+row["Last Name"]+' '+row["First Name"]+' '+row["Middle Name"]+'}'
		
			if (row["Job Title"] != ''):
				line = line + '('+row["Job Title"]+')'
				
			line = line + '\\newline'
			campi_tmp.append(line)
			
			for filed in printed_fileds:
				if(row[filed] != ''): # evito di scrivere i campi vuoti
					campi_tmp.append(tranlated_fields[filed]+': '+row[filed]+'\\newline')	
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
		csv_row = csv.DictReader(csv_file_input, delimiter=',')
		for row in csv_row:
	
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
		print ("Ricordarsi di stampare l'agenda con l'opzione fronte-retro : (short edge TOP )")
	else:
		print('Format not know')

	if (args.template != ''):
		print("TODO: caricare un template")
	
	if (args.include != ''):
		file_senza_estensione , estensione = os.path.splitext(args.include)
		latext_core = latext_core + '\\include{'+file_senza_estensione+'}'
	
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
	parser.add_argument('-i','--include',help='include extra latex file at the end (useful for adding custom pages)', default = '')
	
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()
