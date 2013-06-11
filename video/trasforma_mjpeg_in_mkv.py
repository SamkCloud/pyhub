#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd
# versione iniziale 20091128
# ultima modifica 20130324

# da finire la conversione per python 3


"""
script per convertire i file della macchina fotografica dal formato mjpeg in h264 o vorbis
es: ~/bin/pyhub/video/trasforma_mjpeg_in_mkv.py  *.MOV
"""

import sys

import optparse
import os
import re
import string

def get_title_from_filename(filename):
   if re.search('^\d{1,4}-\d{1,2}-\d{1,2}-*-*', filename, re.I):
        data_filename = filename[0:10]
        extra_filename = filename[11:].split('-')
        dt = data_filename.split('-')
        data_titolo = dt[2] + ' ' + dt[1] + ' ' + dt[0]
        if len(extra_filename) > 1:
            titolo_filename = '-'.join(extra_filename[1:])
            titolo_seriale = extra_filename[0]
        else:
            titolo_filename = extra_filename[0]
            titolo_seriale = extra_filename[0]
        titolo = data_titolo + ' - ' + titolo_filename
   else:
        titolo = filename
   return titolo

def execute_command(comando, options):
    if options.quiet == False:
        print('--------------------------------------')
        print(comando)
        print('++++++++++++++++++++++++++++++++++++++')
    if options.simulate == False:
        os.system(comando)
	

def run(options=None, arguments=''):

	if options.codifica == 'h264':
		# le opzioni prese da: http://ubuntuforums.org/showthread.php?t=786095
		# il parametro -crf imposta la qualità  (più basso = migliore( valori da 18 a 28)
		# con 22 la qualità  è molto buona
		# Opzioni:
		# ar: Campionamento
		# ab Bitrate
		# ac numero cananli 1 mono 2 stereo 
		# strict per abilitare i parametri sperimentali (es aac il 26/3/2013 era considerato sperimentale)
		## 20130326 l'encoder audio aac è sperimentale , bisogna usare l'opzione -strict -2 per usarlo
		# NB per i filmati .MOV della Panasonic TZ5 usare bitrate 32kb
		
		video_options = "-vcodec libx264 -preset veryslow -crf 20 -threads 0"
		# Per Panasonic TZ5
		#audio_opt = "-acodec aac -ar 8000 -ab 32k -ac 1 -strict -2"  
		# per Olimpus XZ-1
		audio_opt = "-acodec aac -ab 128k -ac 2 -strict -2"
		estensione_tmp = '.mp4'

	elif options.codifica == 'vorbis':
		video_options = "-vcodec libtheora -b 6000k"
		audio_opt = "-acodec libvorbis -ar 8000 -ab 32k -ac 1"
		estensione_tmp = '.ogv'
	
	elif options.codifica == 'loseless':
		video_options = "-c:v libx264 -preset veryslow -qp 0"
		audio_opt = "-acodec aac -ab 128k -ac 2 -strict -2"
		estensione_tmp = '.mkv'

	else:
		print('codifica non supportata')
		sys.exit(2)


	for nome_file in arguments:
		(filename, extension) = os.path.splitext(os.path.basename(nome_file))
		titolo = get_title_from_filename(filename)
		nome_tmp = nome_file + estensione_tmp
		nome_log = nome_file + '.log'

	if (extension.lower() == '.mov') or (extension.lower() == '.avi'):
		print('_________________________________________________________________')
		comando = 'ffmpeg -y -i "' + nome_file + '" ' + video_options + ' ' + audio_opt + ' "' + nome_tmp + '" 2> "' + nome_log + '"'
		execute_command(comando, options)
		#trasformo in matroska:
		comando = 'mkvmerge "'+nome_tmp +'" -o "'+nome_tmp+'.mkv" --title "'+titolo+'"'
		execute_command(comando,options)
		
		comando = 'rm -f "'+nome_tmp+'"'
		execute_command(comando,options)
	else:
		print('estenzione non .mov o .avi')

def main():
    usage = "usage: %prog [options] files"
    p = optparse.OptionParser(usage)
    p.add_option('--codifica',
                 '-c',
                 default='h264',
                 help='Scegli il tipo di codifica (h264|vorbis|loseless)',
                 dest='codifica')

    p.add_option('--quiet',
                 '-q',
                 default=False,
                 help='Non mostra l\'output dei comandi',
                 dest='quiet',
                 action='store_true')

    p.add_option('--simulate',
                 '-s',
                 default=False,
                 help='Simula l\'esecuzione dei comandi',
                 dest='simulate',
                 action='store_true')


    options, arguments = p.parse_args()
    if len(arguments) < 1:
        p.error("Scrivi il nome dei files ")

    run(options, arguments)
 

if __name__ == '__main__':
    main()
    


