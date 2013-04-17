#!/usr/bin/python

# author = GD
# First Release 20111121
# Version 20111122.01
# Programma che mostra le foto in f-spot definite come preferite

# TODO
# - Fare il resize dell'immagine, in base alla finestra
# - Inserire il nome della foto dopo i bottoni



import os
import sys
import sqlite3
import random

try:
	import gtk
	import gtk.glade
except:
	print "Devi installare le librerie GTK di Python"
	sys.exit(1)

# Variabili GLOBALI
global_vars={}
global_vars['index']=0


class GladeGD:
	""" Generazione interfaccia Glade """
	
	picture_list = []
	
	def on_window1_destroy(self,data=None):
		gtk.main_quit()
	
	def __init__(self):
		
		#picture_list = self.OpenFSpotDB()
		self.picture_list = list(self.OpenFSpotDB())
		file_glade = '/'.join([os.path.dirname(sys.argv[0]), 'mainwindows.glade'])
		try:
			self.gladeFile = gtk.glade.XML(file_glade)
		except:
			print "Impossibile aprire il file " + file_glade
			sys.exit(1)

		segnali = {
			'on_window1_destroy': self.on_window1_destroy,
			'on_button1_clicked': self.show_previous_picture,
			'on_button3_clicked': self.show_next_picture,
			'on_window1_check_resize': self.window1_check_resize,
			
		}

		window1 = self.gladeFile.get_widget('window1')
		self.gladeFile.signal_autoconnect(segnali)

		

		self.SetImage(self.picture_list[global_vars['index']],'image1')
		
		if window1:
			window1.show()
			gtk.main()
	
	def show_next_picture(self,var_due):
		global_vars['index'] = (global_vars['index'] + 1) % len(self.picture_list)
		self.SetImage(self.picture_list[global_vars['index']],'image1')
	
	def show_previous_picture(self,var_due):
		print global_vars['index']
		global_vars['index'] = (global_vars['index'] - 1 + len(self.picture_list))% len(self.picture_list)
		self.SetImage(self.picture_list[global_vars['index']],'image1')

	
	def SetImage(self,picture_path,nome_widget):
		"""Imposta l'immagine ridimensionata sul widget"""
		
		widget = self.gladeFile.get_widget(nome_widget)
		pixbuf = gtk.gdk.pixbuf_new_from_file(picture_path)
		
		 # Get the size of the source pixmap
		src_width, src_height = pixbuf.get_width(), pixbuf.get_height()
		#print src_width
		dst_width=900
		dst_height=800
		
		#allocation=widget.get_allocation()
		#print allocation.get_width()
		
		# Scale preserving ratio
		
		scale = min(float(dst_width)/src_width, float(dst_height)/src_height)
		new_width = int(scale*src_width)
		new_height = int(scale*src_height)
		
		#scaled_buf = pixbuf.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
		scaled_buf = pixbuf.scale_simple(new_width,new_height,gtk.gdk.INTERP_BILINEAR)
		widget.set_from_pixbuf(scaled_buf)
		
		# Set the name of the picture
		label = self.gladeFile.get_widget('label1')
		label.set_label(picture_path)
	
	def OpenFSpotDB(self):
		"""
		Open F-spot DB and select all favorite photos
		"""
		# Open f-spot db
		conn = sqlite3.connect(os.path.expanduser('~')+'/.config/f-spot/photos.db')
		c = conn.cursor()
		
		# select favorite photos
		# find favories category
		LineSQL = "SELECT id FROM tags WHERE category_id=1"
			
		c.execute(LineSQL)
		id_categorie=['1']
		for row in c:
			id_categorie.append(str(row[0]))
		
		

		# SELECT base_uri,filename FROM photos, photo_tags WHERE photos.id=photo_id AND tag_id IN (1,66,98,111)
		LineSQL = 'SELECT base_uri,filename FROM photos, photo_tags WHERE photos.id=photo_id AND tag_id IN ('+','.join(id_categorie)+');'
	
		c.execute(LineSQL)
		PicPaths = []
		for row in c:
			LongFileName = row[0]+"/"+row[1]
			Dummy,FileName = LongFileName.split("//",1)
			PicPaths.append(FileName)
		
		#Random PicsPath
		PicPathsRandom = []

		# Riorganizza a caso la lista delle foto
		while PicPaths:                        
			element = random.choice(PicPaths)
			PicPaths.remove(element)
			PicPathsRandom.append(element)
		
		return PicPathsRandom
	
	
	
	def window1_check_resize(self,info):
		#print('Resized')
		dummy=1
			

	
if __name__ == "__main__":


	out = GladeGD()

   
