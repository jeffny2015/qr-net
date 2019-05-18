#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import ImageTk,Image
import time

class display_qr():

	def __init__(self, quantity):
		self.quantity = quantity
		self.cont = 0
		self.root = Tk()
		self.canvas = Canvas(self.root, width = 600, height = 600)
		self.canvas.pack()
		self.name = "images\\frame" + str(self.cont) + ".png"
		self.img = ImageTk.PhotoImage(Image.open(self.name))
		self.canvas.create_image(0, 0, anchor=NW, image=self.img)
		self.canvas.after(1000, self.update)
		self.root.mainloop()

	def update(self):
		self.cont += 1
		if(self.cont < self.quantity):
			self.name = "images\\frame" + str(self.cont) + ".png"
			self.img = ImageTk.PhotoImage(Image.open(self.name))
			self.canvas.create_image(0, 0, anchor=NW, image=self.img)
			self.canvas.after(1000, self.update)
		else:
			self.root.destroy()
		

'''def main():
	disp = display_qr(3)
	disp.display()

if __name__ == '__main__':
	main()
'''