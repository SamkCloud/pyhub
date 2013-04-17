#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# programma in python per scaricare le immagini da google
# versione 0.5 20101129
#
# es: ./download-album-art.py /mnt/md0/giuliano/Musica/MUSICA/Artisti\ -\ Italiani/Jovanotti/Buon\ Sangue/

#
# url google:
# http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=battiato&start=0

# pezzi presi da:
# http://stackoverflow.com/questions/257409/download-image-file-from-the-html-page-source-using-python

import sys

import cgi
import os
import pprint
import simplejson
import urllib


def google_image_download(query, num_img, out_folder='./img-tmp/', output_format='html'):
    """
	query: stringa da cercare in google: es  'Vasco Rossi vado al massimo'
	num_img: e' il numero di immagini da scaricare moltiplicato per 4
	out_folder: la directory dove vengono scritte le immagini
	output_format: è il tuipo di formato in uscita (xml o html)
	"""
    

    #scrive l'output su un file html
    # Scrive un file.
    if (output_format == 'html'):
        out_file = open("album-art-tmp.html", "w")
        linea = '<table border="1">\n'
        linea += '<tr><th>nome</th><th>link</th><th>dimensioni</th><th>dimensioni</th><th>url</th></tr>\n'
        out_file.write(linea)
    elif 	(output_format == 'xml'):
        out_file = open("album-art-tmp.xml", "w")
        linea = "<?xml version='1.0' standalone='yes'?>\n"
        linea += "<pictures>\n"
        out_file.write(linea)

    for j in range(0, num_img):
	print '.'
        start = j * 4
        url_query = urllib.urlencode({'q': query, 'start':start})
        url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&%s'  % (url_query)
        #print url
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        results = json['responseData']['results']
        indice = int(start)
        for i in results:
            #pprint.pprint(i)
            filename = i['url'].split("/")[-1]
            (nomefile_inutilizzato, estensione) = os.path.splitext(filename)
            outpath = os.path.join(out_folder, str(indice+1)) + estensione
            urllib.urlretrieve(i['unescapedUrl'], outpath)
            titolo = cgi.escape(i['title'])
            if (output_format == 'html'):
                linea = '<tr>'
                linea += '<td>'+str(indice+1)+'</td><td><img src="' + outpath + '"</td>'
                linea += "<td>" + i['height'] + ' x ' + i['width'] + '</td>'
                linea += "<td>" + titolo + "</td>"
                linea += '<td>' + i['url'] + "</td></tr>\n"
				
            elif (output_format == 'xml'):
                linea = '\t<element>\n'
                linea += '\t\t<imgpath>' + outpath + '</imgpath>\n'
                linea += '\t\t<title>' + titolo + '</title>\n'
                linea += '\t\t<height>' + i['height'] + '</height>\n'
                linea += '\t\t<width>' + i['width'] + '</width>\n'
                linea += '\t\t<url>' + i['url'] + '</url>\n'
                linea += '\t</element>\n'

            linea = linea.encode('ascii', 'ignore')		# questo comando modifica le url ... bisogna capire come mai
            out_file.write(linea)

			
            indice = indice + 1
    if (output_format == 'html'):
        linea = "</table>"
    elif (output_format == 'xml'):
        linea = "</pictures>\n"

    out_file.write(linea)
    out_file.close()

def path2ricerca(path):
    """
    trasforma il path in una stringa per la ricerca
    """
    if path.endswith('/'):
        path = path[0:len(path)-1]
    list_out = path.split('/')
    out = list_out[-2]+' '+list_out[-1]
    return out

def copia_immagine(immagine,path):
    """
    copia l'immagine dalla directory alla destinazione rinominandolo in folder
    controlla che non esista già un file che si chiama folder
    """
    import shutil
    if (os.path.exists(path+'/folder.jpg')):
        print 'folder.jpg esite già'
        destinazione = path+'/folder--new.jpg'
        shutil.copy(immagine,destinazione)
    else:
        destinazione = path+'/folder.jpg'
        shutil.copy(immagine,destinazione)

if __name__ == "__main__":
    print 'connessione con il server di google in corso '
    dir_img_tmp =  './img-tmp/'
    os.system('rm -f '+dir_img_tmp+'*')

    path = sys.argv[1]
        

    ricerca = path2ricerca(path)
    google_image_download(ricerca,4,dir_img_tmp)

    num_immagine = raw_input("Scegli il la copertina dal file html ")
    immagine = dir_img_tmp+num_immagine+'.jpg'
    copia_immagine(immagine,path)




