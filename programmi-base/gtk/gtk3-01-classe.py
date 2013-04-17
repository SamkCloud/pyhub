#!/usr/bin/python
# costruita la classe per gt3-base.py

from gi.repository import Gtk

class MiaGtkFinestra:
	def __init__(self):
		window = Gtk.Window()
		window.set_title("Prova finestra")
		window.connect('destroy',self.destroy)
		window.set_default_size(300,200)
		window.set_position(Gtk.WindowPosition.CENTER)
		
		button = Gtk.Button('Hit me!')
		button.connect('clicked',self.button_clicked)
	
		window.add(button)
	
		window.show_all()

	
	def button_clicked(self,button):
		print ("Premuto pulsante")

	def destroy(self,window):
		Gtk.main_quit()

def main():
	app = MiaGtkFinestra()
	Gtk.main()

if __name__ == '__main__':
	main()