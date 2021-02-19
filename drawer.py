# imports and settings

from kivy.app import App
 
from kivy.uix.widget import Widget

from kivy.config import Config

from kivy.uix.button import Button

from kivy.graphics import (Color, Ellipse, Rectangle, Line)

from kivy.core.window import Window

import time

import os

from kivy.graphics import *

Window.clearcolor = (.60, .60, .60, 1)

from kivy.config import Config

Config.set('graphics', 'resizable', '0')

# Draw controls
class PainterWidget(Widget):

	def on_touch_down(self,touch):
		with self.canvas:
			Color(0 , 1 , 0 , 1)
			rad = 30
			Ellipse(pos = (touch.x - rad/2, touch.y - rad/2), size = (rad, rad))
			touch.ud['line'] = Line(points = (touch.x, touch.y), width = 15)
	def on_touch_move(self, touch):
		touch.ud['line'].points += (touch.x, touch.y)

# Buttons
class PaintApp(App):
	def build(self):
		self.icon = "web.png"
		icon = "web.png"
		parent = Widget()
		self.painter = PainterWidget()
		parent.add_widget(self.painter)
		parent.add_widget(Button(text = 'Clear', on_press = self.clear_canvas, size = (100, 50)))
		parent.add_widget(Button(text = 'Save', on_press = self.save, size = (100, 50), pos = (100, 0)))
		parent.add_widget(Button(text = 'Screen', on_press = self.screen, size = (100, 50), pos = (200, 0)))
		parent.add_widget(Button(text = 'Delete image', on_press = self.delete, size = (100, 50), pos = (300, 0)))
		parent.add_widget(Button(text = 'Delete two screenshots', on_press = self.deletescreen, size = (200, 50), pos = (400, 0)))
		parent.add_widget(Button(text = 'Delete one screenshot', on_press = self.deletescreen1, size = (200, 50), pos = (600, 0)))

		return parent

# button commands
	def clear_canvas(self, instance):
		self.painter.canvas.clear()

	def save(self, instance):
		self.painter.size = (Window.size[0], Window.size[1])
		self.painter.export_to_png('image.png')
		print("image succesfully created!")

	def screen(self, instance):
		Window.screenshot('screen.png')
		print("screenshot succesfully created!")

	def delete(self, instance):
		os.remove("image.png")
		print("image succesfully deleted!")

	def deletescreen(self, instance):
		os.remove("screen0001.png")
		os.remove("screen0002.png")
		print("screenshot succesfully deleted")

	def deletescreen1(self, instance):
		os.remove("screen0001.png")
		print("screenshot succesfully deleted")
	
if __name__ == '__main__':
	PaintApp().run()
