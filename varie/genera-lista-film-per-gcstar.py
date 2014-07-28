#!/usr/bin/python
import os


def show_file_in_dir(dir):
  for dirpath, dirnames, filenames in os.walk (dir):
    for subdir in dirnames:
      show_file_in_dir(subdir)
    for nomefile in filenames:
      #print (nomefile)
      parts = nomefile.split("-") 
      
      if(len(parts)==4):
        (anno,titolo,lingue,qualita)=parts
      else:
        titolo=nomefile
        
      print (titolo+';'+nomefile+';II;VV')
      

print ("Titolo;NomeFile;Identifier;Video")
show_file_in_dir('./')
