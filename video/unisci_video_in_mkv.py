#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Autore GD
# Versione Iniziale: 20110108
# Ultima Modifica: 20111120
#
# pacchetti necessari (oltre a quelli presenti in video_lib)
# 	mkvtoolnix
#
# Unisce più file in un unico mkv con capitoli
# unisce sia vob (con ocr dei sottotitoli) oppure mkv
# utilizzo:
# unisci_video_in_mkv.py -o output.mkv directory_con_video
# la directory deve avere la forma
# aaaa_mm_gg - Titolo
# 2007_03_29 - Giulia gioca con lo scatolone

# TODO
# da vedere la parte di aeidon ... una libreria per manipolare i sottotitoli (in particolare Advanced SubStation Alpha)
# la funzione analizza_nome_directory potrebbe restituire lo unixtime invece che una stringa
# si potrebbe estrarre con ocr i sottotitoli ed inserire quelli come con l'ora

# BUG
# con la simuzlazione non funziona. 

import sys

import optparse
import os
import re

sys.path.append("./")
#from video_lib import execute_command
from video_lib import *

def run(options, arguments):


	directory_in = arguments[0].strip('/')

	file_sottotitoli = directory_in + '/sottotitoli.ass'
	file_tags = directory_in + '/tags.xml'
	file_capitoli = directory_in + '/capitoli.txt'

	(titolo, data) = analizza_nome_directory(directory_in)
	file_video = file_video_nella_directory(directory_in)

	if re.search('\d\d\d\d_\d\d_\d\d', data,re.I):
		separatore = '_'
	elif re.search('\d\d\d\d-\d\d-\d\d', data,re.I):
		separatore = '-'
	else:
		print 'errore nel formato data : + data'
		exit(1)
	(anno, mese, giorno) = data.split(separatore)

#	data_italiano = giorno + ' ' + mese_in_italiano(mese) + ' ' + anno
	

		
	# Ocr capitoli
	for video in file_video:
		(root,ext) = os.path.splitext(video)			
		if ext=='.vob':
			ocr_from_vob(video,options)
	
	# ##genera i capitoli
	tempo_capitoli = crea_file_capitoli(file_capitoli, file_video, options)

  
	# # Genero i sottotitoli con la data
	inizializza_file_ass(file_sottotitoli, titolo)
	aggiungi_dialogo_a_file_ass(file_sottotitoli,file_video,tempo_capitoli )


	# ## genero il file con i tags
	crea_file_con_i_tags(file_tags, titolo, data)

	#unisci tutto
	crea_file_mkv(directory_in,file_video,file_sottotitoli,file_tags,file_capitoli,options)




def crea_file_mkv(directory_out,filelist,file_sottotitoli,file_tags,file_capitoli,options):
	"""
	unisce tutto in un file mkv
	"""

#	filelist = file_video_nella_directory(directory_in)

	comando = 'mkvmerge --default-language ita '
	comando = comando + '-o "'+directory_out+'.mkv" '
	comando = comando + '--tags 0:"'+ file_tags +'" '

	for i in range(len(filelist)):
		### aggiungo il '+' al nomefile solo dal secondo titolo in poi
		if i==0:
			comando = comando + '"'+filelist[i]+'" '
		else:
			comando = comando + '+"'+filelist[i]+'" '
		
	if os.path.isfile(file_sottotitoli):
		comando = comando + '"'+file_sottotitoli+'" '

	if os.path.isfile(file_capitoli):
		comando = comando + '--chapters "'+ file_capitoli +'" '

	text_file = open(directory_out+'/linea_comando.txt', "w")
	text_file.write(comando)
	text_file.close()
	execute_command(comando,options)

def crea_file_capitoli(file_capitoli, file_in, options):
	"""
	Genera un file con i capitoli del tipo:
	CHAPTER01=00:00:00,000
	CHAPTER01NAME=Auto chapter 1
	CHAPTER02=00:14:48,000
	CHAPTER02NAME=Auto chapter 2
	"""
	num_capitolo = 1
	tempo_totale = 0

	tempo_capitoli = []
	text_file = open(file_capitoli, "w")

	for nomefile in file_in:

		file_ocr = nomefile+'.txt'
		if os.path.isfile(file_ocr):		
			file_txt = open(file_ocr,'r')
			testo_ocr = file_txt.readline()
			file_txt.close()
			(gg,mm,aa,tempo) = testo_ocr.split(' ')
			(ore,min,sec) = tempo.split(':')
			testo_dialogo = ("%s %s %s %s:%s\n")%(gg,mese_in_italiano(mm),aa,ore,min)
		else:
			testo_dialogo = '--'
		
		comando = "ffmpeg -i \"" + nomefile  + "\" 2>&1 | grep \"Duration\" | cut -d ' ' -f 4 | sed s/,//"
		tempo_capitolo = execute_command(comando, options)
		linea_capitolo = 'CHAPTER%0*d' % (2, num_capitolo) + '=' + milliseconds_to_string(tempo_totale)

#		linea2_capitolo = 'CHAPTER%02dNAME=CAPITOLO %02d - ' % (num_capitolo,num_capitolo) + testo_ocr
		linea2_capitolo = 'CHAPTER%02dNAME=%02d. ' % (num_capitolo,num_capitolo) + testo_dialogo
		tempo_capitoli.append(milliseconds_to_string(tempo_totale))
		tempo_totale = tempo_totale + string_to_milliseconds(tempo_capitolo, '.')
		text_file.write(linea_capitolo+"\n")
		text_file.write(linea2_capitolo+"\n")
		num_capitolo = num_capitolo + 1

	text_file.close()
	return tempo_capitoli


def crea_file_con_i_tags(nomefile, titolo, data):
	"""
	genera un file con i tags per mkv
	"""
	data_con_meno = data.replace('_', '-').strip(' ')
	linea = """<Tags>
<!-- movie -->
<Tag>

	<Simple>
	<Name>TITLE</Name>
	<String>""" + titolo + """</String>
	</Simple>

	<Simple>
	<Name>DATE_RELEASE</Name>
	<String>""" + data_con_meno + """</String>
	</Simple>

	</Tag>
</Tags>"""

	text_file = open(nomefile, "w")
	text_file.write(linea)
	text_file.close()


def analizza_nome_directory(directory_in):
	"""
	Restituisce il titolo e la data di una directory nel formato: 2010_01_10-Giulia con i nanetti
	"""
	(data_generica, titolo) = directory_in.rsplit('-',1)
	titolo = titolo.strip('/')

	data_generica = data_generica[data_generica.rfind('/'):]
	print "data: "+data_generica
	return titolo, data_generica


def inizializza_file_ass(nomefile, titolo):
	"""
	Scrive la parte inizale di un file ass (Advanced SubStation Alpha)
	"""

	linea = """[Script Info]
Title:""" + titolo + """
Original Script:
Original Translation:
Original Editing:
Original Timing:
Synch Point:
Script Updated By:
Update Details:
ScriptType: v4.00+
Collisions: Normal
PlayResY:
PlayResX:
PlayDepth:
Timer: 100.0000
WrapStyle:

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Cronos Pro Light,16,&H00F0F9F5,&H0000FFFF,&H00000000,&H00042505,-1,0,0,0,100,100,0,0,1,2,1,2,10,10,10,0

[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
"""
	text_file = open(nomefile, "w")
	text_file.write(linea)
	text_file.close()



def aggiungi_dialogo_a_file_ass(file_sottotitoli,file_vob,tempo_capitoli ):
	text_file = open(file_sottotitoli, "a")
	indice = 0
	ritardo_partenza_sottotitoli = 3
	for file_video in file_vob:
		(root,ext) = os.path.splitext(file_video)			
		if ext=='.vob':
			file_ocr = file_video+'.txt'
			file_txt = open(file_ocr,'r')
			testo = file_txt.readline()
			file_txt.close()
		
		
	
			tempo_inizio_datetime = string_to_datetime(tempo_capitoli[indice])+datetime.timedelta(seconds=ritardo_partenza_sottotitoli)
			tempo_inizio = tempo_inizio_datetime.strftime('%k:%M:%S').lstrip(' ')+'.'+str(tempo_inizio_datetime.microsecond/1000)
			
			tempo_fine_datetime = string_to_datetime(tempo_capitoli[indice])+datetime.timedelta(seconds=ritardo_partenza_sottotitoli+5)
			tempo_fine = tempo_fine_datetime.strftime('%k:%M:%S').lstrip(' ')+'.'+str(tempo_fine_datetime.microsecond/1000)
			
			(gg,mm,aa,tempo) = testo.split(' ')
			(ore,min,sec) = tempo.split(':')
			testo_dialogo = ("%s %s %s %s:%s\n")%(gg,mese_in_italiano(mm),aa,ore,min)
			linea = 'Dialogue: 0,'+tempo_inizio+','+tempo_fine+',Default,,0000,0000,0030,,' + testo_dialogo
			indice = indice +1
			text_file.write(linea)
			ritardo_partenza_sottotitoli = 0
	text_file.close


def main():
	usage = "usage: %prog [options] files"
	p = optparse.OptionParser(usage)
	p.add_option('--output',
				 '-o',
				 default='output.mvk',
				 help='File di uscita',
				 dest='output_file')


	p.add_option('--verbose',
				 '-v',
				 default=False,
				 help='Verbose',
				 dest='verbose',
				 action='store_true')

	p.add_option('--simulate',
				 '-s',
				 default=False,
				 help='Simula l\'esecuzione dei comandi',
				 dest='simulate',
				 action='store_true')


	options, arguments = p.parse_args()

	if len(arguments) < 1:
		p.error("incorrect number of arguments")

	run(options, arguments)

 

if __name__ == '__main__':
	main()
	
