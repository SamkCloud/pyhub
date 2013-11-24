#!/usr/bin/python
import os
# mostra o imposta i tag idv3 ricorsivamente utilizzando il comando esterno id3v2



def set_tag_in_dir(dir,tag):
	for dirpath, dirnames, filenames in os.walk (dir):
		for subdir in dirnames:
			set_tag_in_dir(subdir,tag)
		for nomefile in filenames:
			nome_file_completo = os.path.join(dirpath,nomefile)
			(filebase,estensione) = os.path.splitext( nome_file_completo )
			if (estensione.lower() == '.ogg'): 			
				os.system('vorbiscomment -w "'+ nome_file_completo+'" -t "ENCODED-BY='+tag+'"')
# con l'mp3 ha si può usare ex-faso
# id3v2 NON supporta i tag 2.4 !!! meglio usare eye3D
			if (estensione.lower() == '.mp3'): 			
				os.system('id3v2 --TENC "'+tag+'" "' + nome_file_completo+'"')

				#print nome_file_completo



#------------------------------- MAIN --------------------------------
tag = 'Raf'
directory_da_processare = './'
set_tag_in_dir(directory_da_processare,tag)
