#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# rb 20130208
"""
Semplice programma per fare il parsing delle ozioni di input
nota che si può usare anche giò uil comando --help
"""

import optparse
import os
import random
import shutil

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(options=None):

	files = os.listdir(options.rootdir)
	src = options.rootdir+'/'+ random.choice(files)
	shutil.copyfile(src,options.destfile) # copia file


def main():
    usage = "usage: %prog [options] arg"
    p = optparse.OptionParser(usage)

    p.add_option('--rootdir',
                 '-r',
                 default='./',
                 help='Root Dir for the images',
                 dest='rootdir')

    p.add_option('--outputfile',
                 '-o',
                 default=os.path.expanduser("~")+"/.cache/ldxm-background.jpg",
                 help='Destination file',
                 dest='destfile')


    options, arguments = p.parse_args()

#    if len(arguments) != 1:
#        p.error("incorrect number of arguments")

    run(options)
 

if __name__ == '__main__':
    main()
    


