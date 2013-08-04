#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# gd 20091128
"""
Semplice programma per fare il parsing delle ozioni di input
nota che si può usare anche già il comando --help
"""

# Note optsparse is DEPRECATED in favour of argparse

import optparse

def print_r(v):
    return '%s = %r %s' % (v, v, type(v))

def run(options=None):
    if options.show_person:
        print('Hello %s' % options.show_person)

    if options.show_home:
        print('La casa è: %s' % options.show_home)
         


def main():
    usage = "usage: %prog [options] arg"
    p = optparse.OptionParser(usage)
    p.add_option('--person',
                 '-p',
                 default='world',
                 help='scegli il tipo di pesona',
                 dest='show_person')

    p.add_option('--casa',
                 '-c',
                 default='',
                 help='Mostra la casa',
                 dest='show_home')


    options, arguments = p.parse_args()

    if len(arguments) != 1:
        p.error("incorrect number of arguments")

    run(options)
 

if __name__ == '__main__':
    main()
    


