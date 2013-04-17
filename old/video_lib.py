#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Autore GD
# Versione Iniziale: 20110217
# Ultima Modifica: 2011120
#
# File con tutte le funzioni necessarie alla elaborazione dei file video
# pacchetti necessario: dvdauthor (per spuunmux) ,imagemagick (per convert), tesseract-ocr (per tesseract)

import commands
import sys
import os
import  datetime

def execute_command(comando, options):
	"""
	Esegue un comando di sistema
	"""
	if options.verbose == True:
		print '--------------------------------------'
		print comando
		print '++++++++++++++++++++++++++++++++++++++'
	if options.simulate == False:
		
		(status,out) = commands.getstatusoutput(comando)

		if status > 0 :
			""" ok  il comando è andato a buon fine """
			print "errore: " 
			print comando
			print "------------------------"
			print out
			sys.exit(1)
		else:
			return out



def print_r(v):
	"""
	equivalente di print_r di php
	"""
	return '%s = %r %s' % (v, v, type(v))

def string_to_datetime(timestring, separatore=','):
	"""
	converte una data nel formato 00:14:48,400 (%H:%M:%S) in un campo datetime
	"""
	(timestring1, millisecondi) = timestring.split(separatore)
	(ore, minuti, secondi) = timestring1.split(':')

	return datetime.datetime(1900,1,1,int(ore),int(minuti),int(secondi),int(millisecondi)*1000)
	
def string_to_milliseconds(timestring, separatore=','):
	"""
	converte una data nel formato 00:14:48,400 (%H:%M:%S) in millisecondi
	"""
	(timestring1, millisecondi) = timestring.split(separatore)
	(ore, minuti, secondi) = timestring1.split(':')

	return int(millisecondi) + int(secondi) * 1000 + int(minuti) * 1000 * 60 + int(ore) * 1000 * 60 * 60

def milliseconds_to_string(milliseconds_in, formato="%02d:%02d:%02d,%03d"):
	"""
	converte i millisecondi in una data nel formato 00:14:48,400
	"""
	newtime = milliseconds_in

	ore = newtime / (60 * 60 * 1000)
	newtime = newtime % (60 * 60 * 1000)

	minuti = newtime / (60 * 1000)
	newtime = newtime % (60 * 1000)

	secondi  = newtime / 1000

	milliseconds = newtime % 1000


	out = formato % (ore, minuti, secondi,milliseconds)

	return  out 


	
def file_video_nella_directory(directory,fileExtList = ['.vob','.mov','.mkv']):
	"""
	restituisce tutti i file video presenti in una directory
	"""
	

	fileList = [os.path.normcase(f)
				for f in os.listdir(directory)]
	fileList = [os.path.join(directory, f)
			   for f in fileList
				if os.path.splitext(f)[1] in fileExtList]

	return sorted(fileList)


def old_data_2_data_in_italiano(data, separatore='_'):
	"""
	Converte un data dal formato: 2010_01_10 a 10 Gennaio 2010
	"""
	(anno, mese, giorno) = data.split(separatore)
	data_text = giorno + ' ' + mese_in_italiano(mese) + ' ' + anno
	return data_text
	
def mese_in_italiano(mese):
	"""
	converte un mese in italiano
	"""
	mesi = ("", "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre")
	return mesi[int(mese)]




def ocr_from_vob(nomefile, options=''):
	"""
	Estrae il testo di un sottotitolo da un file .vob
	"""
	import os
        if not os.path.isfile(nomefile + '.txt'):
            directory = os.path.dirname(nomefile)

            command = 'spuunmux "' + nomefile + '" -o "' + directory + '/sub"'
            execute_command(command, options)

            # ## OCR SUBTITLE
            # comando originale
            #command = 'convert "' + directory + '/sub00000.png" -depth 2 data "' + directory + '/ocr.tif"'
            command = 'convert "' + directory + '/sub00000.png" -depth 2  "' + directory + '/ocr.tif"'
            execute_command(command, options)

            command = 'tesseract "' + directory + '/ocr.tif" "' + directory + '/ocr"'
            execute_command(command, options)

            # ### rinomino il file in base al contenuto del file estratto tramite ocr
            file = open(directory + '/ocr.txt', 'r')
            testo = file.readline()
            file.close()

            # ##    metto a posto qualche errore possibile del ocr
            testo = testo.replace('A', '4')
            testo = testo.replace('S', '6')
            testo = testo.replace('¤', ':')
            testo = testo.replace('=', ':')
	

            file = open(nomefile + '.txt', 'w')
            file.write(testo)
            file.close()

            # ## Pulizia
            command = 'rm "' + directory + '/"sub0*.png "' + directory + '/"sub.xml "' + directory + '/"ocr.*'
            execute_command(command, options)
	
            return testo
        else:
            file = open(nomefile + '.txt', 'r')
            testo = file.read()
            file.close()
            return testo

