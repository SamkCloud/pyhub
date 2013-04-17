#!/usr/bin/python


import os,sys
import re
import shutil
sys.path.append("~/bin/")
import dvd_extract_vob_chapter



rootdir = './'

for subdir, dirs, files in os.walk(rootdir):
    for nome_file in files:
	(basename,extension) = os.path.splitext( nome_file )

	if ((extension == '.vob') and (basename[:8] == 'capitolo')):
                print nome_file
		dvd_extract_vob_chapter.modifica_nome_in_base_ai_sottotitoli(nome_file)

