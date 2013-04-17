#!/usr/bin/python

# ----------------------------------------
#
# Created 20111115
# Author: Giuliano Dedda
# Version: 20111115.03
# Non uso più questa versione perché sono passato a gtk (usando glade come generatore di interfacce)
# ----------------------------------------

import glob
import os
import wx
from wx.lib.pubsub import Publisher

import sqlite3

########################################################################
class ViewerPanel(wx.Panel):
	""""""

	#----------------------------------------------------------------------
	def __init__(self, parent):
		"""Constructor"""
		wx.Panel.__init__(self, parent)
		
		width, height = wx.DisplaySize()
		self.picPaths = []
		self.currentPicture = 0
		self.totalPictures = 0
		self.photoMaxSize = height - 200
		Publisher().subscribe(self.updateImages, ("update images"))

		self.slideTimer = wx.Timer(None)
		self.slideTimer.Bind(wx.EVT_TIMER, self.update)
		
		self.layout()
		
	#----------------------------------------------------------------------
	def layout(self):
		"""
		Layout the widgets on the panel
		"""
		
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		img = wx.EmptyImage(self.photoMaxSize,self.photoMaxSize)
		self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, 
										 wx.BitmapFromImage(img))
		self.mainSizer.Add(self.imageCtrl, 0, wx.ALL|wx.CENTER, 5)
		self.imageLabel = wx.StaticText(self, label="")
		self.mainSizer.Add(self.imageLabel, 0, wx.ALL|wx.CENTER, 5)
		
		btnData = [("Previous", btnSizer, self.onPrevious),
				   ("Slide Show", btnSizer, self.onSlideShow),
				   ("Next", btnSizer, self.onNext)]
		for data in btnData:
			label, sizer, handler = data
			self.btnBuilder(label, sizer, handler)
			
		self.mainSizer.Add(btnSizer, 0, wx.CENTER)
		self.SetSizer(self.mainSizer)
			
	#----------------------------------------------------------------------
	def btnBuilder(self, label, sizer, handler):
		"""
		Builds a button, binds it to an event handler and adds it to a sizer
		"""
		btn = wx.Button(self, label=label)
		btn.Bind(wx.EVT_BUTTON, handler)
		sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
		
	#----------------------------------------------------------------------
	def loadImage(self, image):
		""""""
		image_name = os.path.basename(image)
		img = wx.Image(image, wx.BITMAP_TYPE_ANY)
		# scale the image, preserving the aspect ratio
		W = img.GetWidth()
		H = img.GetHeight()
		if W > H:
			NewW = self.photoMaxSize
			NewH = self.photoMaxSize * H / W
		else:
			NewH = self.photoMaxSize
			NewW = self.photoMaxSize * W / H
		img = img.Scale(NewW,NewH)

		self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
		self.imageLabel.SetLabel(image_name)
		self.Refresh()
		Publisher().sendMessage("resize", "")
		
	#----------------------------------------------------------------------
	def nextPicture(self):
		"""
		Loads the next picture in the directory
		"""
		if self.currentPicture == self.totalPictures-1:
			self.currentPicture = 0
		else:
			self.currentPicture += 1
		
		self.loadImage(self.picPaths[self.currentPicture])
		
	#----------------------------------------------------------------------
	def previousPicture(self):
		"""
		Displays the previous picture in the directory
		"""
		if self.currentPicture == 0:
			self.currentPicture = self.totalPictures - 1
		else:
			self.currentPicture -= 1
		self.loadImage(self.picPaths[self.currentPicture])
		
	#----------------------------------------------------------------------
	def update(self, event):
		"""
		Called when the slideTimer's timer event fires. Loads the next
		picture from the folder by calling th nextPicture method
		"""
		self.nextPicture()
		
	#----------------------------------------------------------------------
	def updateImages(self, msg):
		"""
		Updates the picPaths list to contain the current folder's images
		msg.data contains the url of the image to show. 
		"""
		
		self.picPaths = msg.data
		self.totalPictures = len(self.picPaths)
		
		self.loadImage(self.picPaths[0])
		
	#----------------------------------------------------------------------
	def onNext(self, event):
		"""
		Calls the nextPicture method
		"""
		self.nextPicture()
	
	#----------------------------------------------------------------------
	def onPrevious(self, event):
		"""
		Calls the previousPicture method
		"""
		self.previousPicture()
	
	#----------------------------------------------------------------------
	def onSlideShow(self, event):
		"""
		Starts and stops the slideshow
		"""
		btn = event.GetEventObject()
		label = btn.GetLabel()
		if label == "Slide Show":
			self.slideTimer.Start(3000)
			btn.SetLabel("Stop")
		else:
			self.slideTimer.Stop()
			btn.SetLabel("Slide Show")
		
		
########################################################################
class ViewerFrame(wx.Frame):
	""""""

	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, None, title="Image Viewer")
		panel = ViewerPanel(self)
		self.folderPath = ""
		Publisher().subscribe(self.resizeFrame, ("resize"))
		
		self.initToolbar()
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		
		self.Show()
		self.sizer.Fit(self)
		self.Center()
		
		
	#----------------------------------------------------------------------
	def initToolbar(self):
		"""
		Initialize the toolbar
		"""
		self.toolbar = self.CreateToolBar()
		self.toolbar.SetToolBitmapSize((16,16))
		
		open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
		openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open an Image Directory")
		self.Bind(wx.EVT_MENU, self.onOpenDirectory, openTool)

		open_ico = wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR, (16,16))
		openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "F-spot", "Open F-Spot Favorites Images")
		self.Bind(wx.EVT_MENU, self.OpenFSpotDB, openTool)
		
		open_ico = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_TOOLBAR, (16,16))
		openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Configuration", "Configure Parameters")
		self.Bind(wx.EVT_MENU, self.OpenFSpotDB, openTool)
		
		self.toolbar.Realize()
		
	#----------------------------------------------------------------------
	def onOpenDirectory(self, event):
		"""
		Opens a DirDialog to allow the user to open a folder with pictures
		"""
		dlg = wx.DirDialog(self, "Choose a directory",
						   style=wx.DD_DEFAULT_STYLE)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.folderPath = dlg.GetPath()
			picPaths = glob.glob(self.folderPath + "/*.jpg")
		Publisher().sendMessage("update images", picPaths)
		
		
	#----------------------------------------------------------------------
	def OpenFSpotDB(self,event):
		"""
		Open F-spot DB and select all favorite photos
		"""
		conn = sqlite3.connect('/mnt/md0/giuliano/.config/f-spot/photos.db')
		c = conn.cursor()
		LineSQL = "SELECT base_uri,filename FROM photos, photo_tags WHERE photos.id=photo_id AND tag_id=1;"
		
		c.execute(LineSQL)
		PicPaths = []
		for row in c:
			LongFileName = row[0]+"/"+row[1]
			Dummy,FileName = LongFileName.split("//",1)
			PicPaths.append(FileName)
		
		Publisher().sendMessage("update images", PicPaths)
	
	#----------------------------------------------------------------------
	def resizeFrame(self, msg):
		""""""
		self.sizer.Fit(self)
		
#----------------------------------------------------------------------
if __name__ == "__main__":
	app = wx.PySimpleApp()
	frame = ViewerFrame()
		
	app.MainLoop()
	
