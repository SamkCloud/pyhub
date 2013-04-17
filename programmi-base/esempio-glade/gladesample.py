#!/usr/bin/python
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "GD"
__date__ = "$9-nov-2010 12.08.25$"


import os
import sys

try:
    import gtk
    import gtk.glade
except:
    print "Devi installare le librerie GTK di Python"
    sys.exit(1)


class GladeGD:
    """ Prova glade di GD """

    def on_window1_destroy(self,data=None):
	gtk.main_quit()

    def __init__(self):
        file_glade = '/'.join([os.path.dirname(sys.argv[0]), 'mainwindows.glade'])
        #file_glade = '/'.join([os.path.dirname(sys.argv[0]), 'IPFinder.glade'])
        try:
            self.gladeFile = gtk.glade.XML(file_glade)
        except:
            print "Impossibile aprire il file " + file_glade
            sys.exit(1)

        segnali = {
            'on_window1_destroy': self.on_window1_destroy,
        }

        window1 = self.gladeFile.get_widget('window1')
        self.gladeFile.signal_autoconnect(segnali)

        if window1:
            window1.show()
            gtk.main()
    
if __name__ == "__main__":
    out = GladeGD()
   
   
