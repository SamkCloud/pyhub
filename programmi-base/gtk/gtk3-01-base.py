#!/usr/bin/python
# esempio che fa una finestra con un pulsante 
# tratto da: 
# http://vimeo.com/dgsiegel/videos

from gi.repository import Gtk

def main():
	window = Gtk.Window()
	window.set_title("Prova finestra")
	window.connect('destroy',destroy)
	window.set_default_size(300,200)
	window.set_position(Gtk.WindowPosition.CENTER)
	
	button = Gtk.Button('Hit me!')
	button.connect('clicked',button_clicked)
	
	window.add(button)
	
	window.show_all()
	Gtk.main()

def button_clicked(button):
	print ("Premuto pulsante")

def destroy(window):
	Gtk.main_quit()
	
if __name__ == '__main__':
	main()