#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# programma per trovare le directory senza albumart ( folder.jpg)


import os
import sys
fileList = []
rootdir = sys.argv[1]
for root, subFolders, files in os.walk(rootdir):
    for subFolder in subFolders:
        folder = os.path.join(root,subFolder)
        albumart = folder + '/folder.jpg'
        if (not os.path.isfile(albumart)):
                print folder