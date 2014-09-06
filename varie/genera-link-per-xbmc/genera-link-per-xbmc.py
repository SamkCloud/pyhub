#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20140904

import argparse
import subprocess
import os
import string 

def print_r(v):
	return '%s = %r %s' % (v, v, type(v))


def recusively_lanch_command(dir,outdir):
    for dirpath, dirnames, filenames in os.walk (dir):
        for subdir in dirnames:
        #    recusively_lanch_command(subdir,outdir)
            for nomefile in filenames:
                nome_file_completo = os.path.join(dirpath,nomefile)
                (filebase,estensione) = os.path.splitext( nomefile )
                if (estensione.lower() == '.mkv'): 
                    film_elements = filebase.split('-')
                    nuovo_nomefile = outdir+film_elements[1].strip()+' - '+film_elements[0].replace('[', '(').replace(']', ')')+'.mkv'
                    print(nuovo_nomefile)
                    
                    output = subprocess.check_output(['ln', '-s',nome_file_completo,nuovo_nomefile])


def run(args=None):
    recusively_lanch_command (args.dirname , args.outdir)
	
def main():
    parser = argparse.ArgumentParser(description='Demo of argparse')
    parser.add_argument("dirname", help='directory in cui ci sono i film da analizzare')
    parser.add_argument("outdir", help='directory in cui ci sono i nuovi nomi con i link')
    args = parser.parse_args()
    run(args)

if __name__ == '__main__':
    main()
