#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20140904

import argparse
import subprocess
import os
import string 

def print_r(v):
	return '%s = %r %s' % (v, v, type(v))


def lanch_command(dir,outdir):
    for nomefile in os.listdir(dir):
        nome_file_completo = os.path.join(dir,nomefile)
        (filebase,estensione) = os.path.splitext( nomefile )
        if ((estensione.lower() == '.mkv') or (estensione.lower() == '.avi') or (estensione.lower() == '.m4v') or (estensione.lower() == '.mp4')): 
            film_elements = filebase.split('-',2)
            nuovo_nomefile = outdir+film_elements[1].strip()+' - '+film_elements[0].replace('[', '(').replace(']', ')')+'-'+film_elements[2]+'.mkv'
            comando = 'mv "'+ nome_file_completo+ '" "'+nuovo_nomefile+'"'
            print(nuovo_nomefile)
            #print(comando)
            output = subprocess.check_output(['mv', nome_file_completo,nuovo_nomefile])


def run(args=None):
    lanch_command (args.dirname , args.outdir)
	
def main():
    parser = argparse.ArgumentParser(description='Demo of argparse')
    parser.add_argument("dirname", help='directory in cui ci sono i film da analizzare')
    parser.add_argument("outdir", help='directory in cui ci sono i nuovi nomi con i link')
    args = parser.parse_args()
    run(args)

if __name__ == '__main__':
    main()
