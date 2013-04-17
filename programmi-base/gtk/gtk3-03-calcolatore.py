#!/usr/bin/python
# calcolatrice
# http://vimeo.com/dgsiegel/videos


from gi.repository import Gtk, Pango, Gdk

class MiaGtkFinestra:
	def __init__(self):
		window = Gtk.Window()
		window.set_title("Prova finestra")
		window.set_position(Gtk.WindowPosition.CENTER)
		window.set_default_size(300,300)
		window.set_icon_name('accessoies-calculator')
		window.connect('destroy',self.destroy)

		box_main=Gtk.Box.new(Gtk.Orientation.VERTICAL,5)
		window.add(box_main)

		self.entry = Gtk.Entry()
		self.entry.set_alignment(1)
		self.entry.set_size_request(-1,50)
		self.entry.set_can_focus(False)

		font_description = self.entry.get_style().font_desc
		font_description.set_absolute_size(24 * Pango.SCALE)
		self.entry.modify_font(font_description)

		box_main.add(self.entry)


		buttons = [7,8,9,"/",
			  4,5,6,"*",
			  1,2,3,"-",
			  0,"C","=","+"]

		for i in range(4):
			hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,5)
			hbox.set_homogeneous(5)
			box_main.pack_start(hbox,True,True,0)
			for j in range(4):
				button = Gtk.Button(buttons[i*4+j])
				button.connect_after("clicked",self.button_clicked)
				button.set_can_focus(False)
				hbox.add(button)

		window.show_all()

	def button_clicked(self, button):
		self.calculate(button.get_label())
	
	def calculate(self,item):
		if item == "=":
			try:
				value = repr(eval(str(self.entry.get_text())))
			except:
				self.entry.override_color(Gtk.StateType.NORMAL,Gdk.RGBA(red=1.0,green=0,blue=0))
			self.entry.set_text(value)
		elif item == "C":
			self.entry.override_color(Gtk.StateType.NORMAL,None)
			self.entry.set_text("")
		else:
			self.entry.override_color(Gtk.StateType.NORMAL,None)
			self.entry.insert_text(str(item),-1)

	def destroy(self,window):
		Gtk.main_quit()

def main():
	app = MiaGtkFinestra()
	Gtk.main()

if __name__ == '__main__':
	main()

