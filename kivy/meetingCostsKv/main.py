import kivy
kivy.require('1.1.1')

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Color, Line, Rectangle

from datetime import datetime, timedelta
import time

#Builder.load_file('meetingcost.kv')

class MenuScreen(Screen):
    pass

class Graph(Widget):
    secondsElapsed = 0.0
    totalCost = 0.
    hourCost = 15.
    nbParticipants = 0
    maxY = 10 #dollars
    maxX = 5 * 60 #seconds
    points = []

    def updateCost(self, dt):
      self.totalCost = self.totalCost + dt / 3600.0 * self.hourCost * self.nbParticipants
      self.secondsElapsed = self.secondsElapsed + dt 
      self.points.append( (self.secondsElapsed, self.totalCost) )
      if self.totalCost > self.maxY or self.secondsElapsed > self.maxX:
        self.rescale()
      
      data = reduce(lambda r, x : r + (self.pos[0] + x[0] * self.size[0] / self.maxX, self.pos[1] + x[1] * self.size[1] / self.maxY), self.points, ())
      with self.canvas:
        Color(1.0, 0., 0.)
        Line(points=data)

    def on_resize(self, width, height):
        self.canvas.clear()

    def rescale(self):
      self.maxY = 2.0 * self.maxY
      self.maxX = 2.0 * self.maxX
      self.canvas.clear()
      with self.canvas:
        Rectangle(pos=self.pos, size=self.size)
      print "rescale !!!! "

class MeetingCost(Screen):
    costLabel = ObjectProperty()
    elapsedLabel = ObjectProperty()
    slider = ObjectProperty()
    participantsLabel = ObjectProperty()
    graph = ObjectProperty()
    startButton = ObjectProperty()
    info = StringProperty()
    stopped = True
    elapsedTime = 0

    def build(self):
      self.participantsLabel.text = "#Participants = %d"%0
      self.costLabel.text = "Meeting cost : %.2f"%0.
      self.elapsedLabel.text = "Elapsed time : %.2d:%.2d:%.2d"%(0,0,0) 
      self.slider.bind(value=self.updateParticipants)

    def startStopPressed(self)  :
      if self.stopped: 
        self.startMeeting()
      else:
        self.stopMeeting()
    
    def startMeeting(self):
      if self.stopped:
        self.startButton.text = "Pause Meeting"
        Clock.schedule_interval(self.update, 1.0)
        self.stopped = False 

    def stopMeeting(self):
      if not self.stopped:
        self.startButton.text = "Start Meeting"
        Clock.unschedule(self.update)
        self.stopped = True 

    def on_resize(self, width, height):
        self.canvas.clear()

    def updateParticipants(self, instance, value):
      self.graph.nbParticipants = value
      self.participantsLabel.text = "#Participants = %d"%value

    def updateCost(self, dt):
      self.costLabel.text = "Meeting cost : %.2f"%self.graph.totalCost

    def updateElapsed(self, dt):
      self.elapsedTime = self.elapsedTime + dt 
      hours = self.elapsedTime / 3600
      minutes = (self.elapsedTime / 60 ) % 60
      secondes = self.elapsedTime % 60
      self.elapsedLabel.text = "Elapsed time : %.2d:%.2d:%.2d"%(hours,minutes,secondes) 

    def update(self, dt):
     self.graph.updateCost(dt)
     self.updateCost(dt)
     self.updateElapsed(dt)

class MeetingCostApp(App):
    #timeStop = None
    cost = None
    menu = None
    meetingWasStopped = None
    sm = None
    
    def build(self):
        self.sm = ScreenManager()
        self.cost = MeetingCost(name="cost")
        self.menu = MenuScreen(name="menu")
	self.cost.build()
        self.sm.add_widget(self.cost)
        self.sm.add_widget(self.menu)
	self.sm.curent = "cost"
	self.bind(on_start = self.post_build_init) 
        return self.sm

    def on_pause(self):
        self.meetingWasStopped = self.cost.stopped
        self.cost.stopMeeting()
        return True

    def on_stop(self):
        self.meetingWasStopped = self.cost.stopped
        self.cost.stopMeeting()
        return True

    def on_resume(self):
	if not self.meetingWasStopped:
          self.cost.startMeeting()

    def _key_handler(self, key, scanCode, codePoint, modifier, args):
	self.cost.startButton.text =  'codePoint ' + str(codePoint)
        if codePoint == 4:
	  self.sm.current = "menu"

    def post_build_init(self,ev): 
        #import android 
        #import pygame 

        #android.map_key(android.KEYCODE_MENU, 1000) 
        #android.map_key(android.KEYCODE_BACK, 1001) 
        #android.map_key(android.KEYCODE_HOME, 1002) 
        #android.map_key(android.KEYCODE_SEARCH, 1003) 
        #win = self._app_window 
        #win.bind(on_keyboard=self._key_handler) 
        pass
if __name__ == '__main__':
    MeetingCostApp().run()
