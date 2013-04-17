#!/usr/bin/python
# 20090412 GD 
# modifica 20101228
# 
# Estrae da i file vob i singoli capitoli. Usa il programma dvdxchap per sapere il numero di capitoli e
# mplayer per estrarli veramente. 
#
# utilizzo: 
# cd Video/video-giuliano/video16/2/
# ~/bin/dvd_extract_vob_chapter.py  ~/Video/video-giuliano/video16_orig/2_4/VIDEO_TS/

# serve dvdxchap e mplayer

# per i sottotitoli serve anche i pacchetto ffmpeg e dvdauthor
# e per l'ocr dei sottotitoli tesseract-ocr e imagemagik



import sys

import os
import re
import shutil

def modifica_nome_in_base_ai_sottotitoli(nome_file):
    (basename, extension) = os.path.splitext(nome_file)
    capitolo = basename[8:10]

	
    #########################################################
    # Estraggo i sottotitoli
    linea = "ffmpeg -i " + nome_file + " -y -scodec copy -an -vn -f dvd sottotitoli" + capitolo + ".sub >> log" + capitolo + ".txt 2>&1"
    # -i input
    # -y force yes
    # -an
    # -vn
    # -f

    print linea
    os.system(linea)

    linea = "spuunmux  sottotitoli" + capitolo + ".sub"
    print linea
    os.system(linea)

    shutil.move('sub00000.png', 'data' + capitolo + '.png')


    ### OCR SOTTOTITOLI
    linea = 'convert data' + capitolo + '.png -depth 2 data' + capitolo + '.tif'
    print linea
    os.system(linea)

    linea = 'tesseract data' + capitolo + '.tif ocr' + capitolo
    print linea
    os.system(linea)

    #### rinomino il file in base al contenuto del file estratto tramite ocr
    file = open('ocr' + capitolo + '.txt', 'r')
    testo = file.readline()
    file.close()


    ### metto a posto qualche errore possibile del ocr
    testo = testo.replace('A', '4')
    testo = testo.replace('S', '6')

    data_video = testo.split(' ')
    anno = data_video[2]
    mese = format(int(data_video[1]), '02d')
    giorno = format(int(data_video[0]), '02d')



    nuovo_nome_file = anno + '_' + mese + '_' + giorno + ' ' + nome_file

    shutil.move(nome_file, nuovo_nome_file)

    # faccio un po' di pulizia
    linea = 'rm sub0*.png'
    print linea
    os.system(linea)

    linea = 'rm *.tif'
    print linea
    os.system(linea)

    linea = 'rm *.sub'
    print linea
    os.system(linea)

    linea = 'rm sub.xml'
    print linea
    os.system(linea)

    linea = 'rm ocr*.txt'
    print linea
    os.system(linea)

    linea = 'rm *.png'
    print linea
    os.system(linea)

    linea = 'rm log*.txt'
    print linea
    os.system(linea)




def main():
    # directory_dvd_sorgente e' la directory che contiene la directory VIDEO_TS
    directory_dvd_sorgente = sys.argv[1]

    # directory_vob_destinazione e' la directory in cui vengono posizionati i file vob
    # 				se il parametro non e' presente usa ./
    if len(sys.argv) > 2:
        directory_vob_destinazione = sys.argv[2]
    else:
        directory_vob_destinazione = "./"

    output_dvdxchap = os.popen("dvdxchap " + directory_dvd_sorgente + " 2>/dev/null")
    for linea in output_dvdxchap.readlines():
        if re.search('CHAPTER..=', linea, re.I):
            dvd_chapters = linea[7:9]

    # dvd_chapters e' il numero di capitoli in un dvd
    print "numero capitoli: " + dvd_chapters
    dvd_chapters = int(dvd_chapters)


    for capitolo_int in range(1, dvd_chapters + 1):
        if capitolo_int < 10:
            capitolo = "0" + str(capitolo_int)
            nome_file  = "capitolo" + "0" + str(capitolo_int) + ".vob"
        else:
            capitolo = str(capitolo_int)
            nome_file  = "capitolo" + str(capitolo_int) + ".vob"

        linea = "mplayer dvd:// -dvd-device " + directory_dvd_sorgente + " -chapter " + capitolo + "-" + capitolo + " -v -dumpstream -dumpfile " + directory_vob_destinazione + "/" + nome_file + "> log" + capitolo + ".txt 2>&1"

        print linea
        os.system(linea)
        modifica_nome_in_base_ai_sottotitoli(nome_file)



# __________________________________ MAIN _________________________________

if __name__ == "__main__":
    main()




