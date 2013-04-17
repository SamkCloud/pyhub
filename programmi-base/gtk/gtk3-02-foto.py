#!/usr/bin/python
# visualizzatore di foto tratto da
# http://vimeo.com/dgsiegel/videos


from gi.repository import Gtk

class MiaGtkFinestra:
	def __init__(self):
		window = Gtk.Window()
		window.set_title("Prova finestra")
		window.connect('destroy',self.destroy)
		
		box = Gtk.Box()
		box.set_spacing(5)
		box.set_orientation(Gtk.Orientation.VERTICAL)
		window.add(box)	
	
		self.image = Gtk.Image()
		box.add(self.image)
		
		button = Gtk.Button('apri una foto')
		button.connect_after('clicked',self.on_open_clicked)
		box.add(button)
		
		window.show_all()

	
	def on_open_clicked(self,button):
		dialog = Gtk.FileChooserDialog('Open Image',button.get_toplevel(),Gtk.FileChooserAction.OPEN)
		dialog.add_button(Gtk.STOCK_CANCEL,0)
		dialog.add_button(Gtk.STOCK_OPEN,1)
		dialog.set_default_response(1)

		filefilter = Gtk.FileFilter()
		filefilter.add_pixbuf_formats()
		dialog.set_filter(filefilter)

		if dialog.run() == 1:
			self.image.set_from_file(dialog.get_filename())
		dialog.destroy()


	def destroy(self,window):
		Gtk.main_quit()

def main():
	app = MiaGtkFinestra()
	Gtk.main()

if __name__ == '__main__':
	main()
