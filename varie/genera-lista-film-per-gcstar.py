#!/usr/bin/python
import os


def show_file_in_dir(dir):
  for dirpath, dirnames, filenames in os.walk (dir):
    for subdir in dirnames:
      show_file_in_dir(subdir)
    for nomefile in filenames:
      #print (nomefile)
      parts = nomefile.split("-") # Will raise exception if too many options 
      parts += [None] * (8 - len(parts)) # Assume we can have max. 4 items. Fill in missing entries with None.  
      (anno,titolo,lingue,qualita,op1,opt2,opt3,opt4)=parts
      
      print (titolo+';'+nomefile)
      

print ("Titolo;NomeFile")
show_file_in_dir('./')

