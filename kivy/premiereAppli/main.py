#copier ce code dans ~/projects/kivy/premiereAppli/main.py
from kivy.app import App 
from kivy.uix.button import Button 

class TestApp(App): 
	def build(self): 
		return Button(text='Hello World') 

TestApp().run()
