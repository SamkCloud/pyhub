#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20150215
"""
Convert file to 
"""


import argparse
import sys
import subprocess

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(arguments):
	print ("Input file: %s" % arguments.input )

	if arguments.codifica == 'h264old':
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
		
		#video_options = "-vcodec libx264 -preset veryslow -crf 20 -threads 0"
		# Per Panasonic TZ5
		#audio_opt = "-acodec aac -ar 8000 -ab 32k -ac 1 -strict -2"  
		# per Olimpus XZ-1
		#audio_opt = "-acodec aac -ab 128k -ac 2 -strict -2"
		
		
		video_options 	= "-vcodec libx264 -preset veryslow -crf 20 -threads 0"
		audio_opt 		= "-acodec copy"

	elif arguments.codifica == 'h264':
		video_options 	= "-c:v libx264"
		audio_opt 		= "-c:a copy"
		
		
	elif arguments.codifica == 'h265':
		video_options 	= "-c:v libx265"
		audio_opt 		= "-c:a copy"
		
	
	elif arguments.codifica == 'loseless':
		video_options = "-c:v libx264 -preset veryslow -qp 0"
		audio_opt = "-acodec aac -ab 128k -ac 2 -strict -2"

	
	else:
		sys.exit("Error: Codifica non riconosciuta")
	
	output_filename = arguments.input+'.'+arguments.codifica+'.mkv'
	log_filename =arguments.input+'.log'
	comando = 'ffmpeg -y -i "' + arguments.input + '" ' + video_options + ' ' + audio_opt + ' "' + output_filename + '" 2> "' + log_filename + '"'
	print(comando)
	#output = subprocess.check_output(['ffmpeg','-y','-i',arguments.input,video_options,audio_opt,output_filename])
	
	pipe = subprocess.Popen([comando],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	stdout, stderr = pipe.communicate()
	print(stdout)
	print('---')
	print(stderr)
	

def main():
	

	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument('input')
	parser.add_argument('--codifica','-c',default='h264',help='Scegli il tipo di codifica (h264|loseless|h264old|h265)')
	
	arguments = parser.parse_args()

	run(arguments)

if __name__ == '__main__':
    main()
    
