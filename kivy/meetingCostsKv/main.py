import kivy
kivy.require('1.1.1')

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Color, Line, Rectangle

from datetime import datetime, timedelta
import time

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class Graph(Widget):
    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)
        self.secondsElapsed = 0.0
        self.totalCost = 0.
        self.hourCost = 15.
        self.nbParticipants = 0
        self.maxY = 10 #dollars
        self.maxX = 5 * 60 #seconds
        self.points = []

    def update_cost(self, dt):
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

class MeetingCost(Screen):
    costLabel = ObjectProperty()
    elapsedLabel = ObjectProperty()
    slider = ObjectProperty()
    participantsLabel = ObjectProperty()
    graph = ObjectProperty()
    startButton = ObjectProperty()
    info = StringProperty()
    
    def __init__(self, **kwargs):
        super(MeetingCost, self).__init__(**kwargs)
        self.stopped = True
        self.elapsedTime = 0

    def build(self):
        self.participantsLabel.text = "#Participants = %d"%0
        self.costLabel.text = "Meeting cost : %.2f"%0.
        self.elapsedLabel.text = "Elapsed time : %.2d:%.2d:%.2d"%(0,0,0) 
        self.slider.bind(value=self.update_participants)

    def start_stop_pressed(self)  :
        if self.stopped: 
            self.start_meeting()
        else:
            self.stop_meeting()
    
    def start_meeting(self):
        if self.stopped:
            self.startButton.text = "Pause Meeting"
            Clock.schedule_interval(self.update, 1.0)
            self.stopped = False 

    def stop_meeting(self):
        if not self.stopped:
            self.startButton.text = "Start Meeting"
            Clock.unschedule(self.update)
            self.stopped = True 

    def on_resize(self, width, height):
        self.canvas.clear()

    def update_participants(self, instance, value):
        self.graph.nbParticipants = value
        self.participantsLabel.text = "#Participants = %d"%value

    def update_cost(self, dt):
        self.costLabel.text = "Meeting cost : %.2f"%self.graph.totalCost

    def update_elasped(self, dt):
        self.elapsedTime = self.elapsedTime + dt 
        hours = self.elapsedTime / 3600
        minutes = (self.elapsedTime / 60 ) % 60
        secondes = self.elapsedTime % 60
        self.elapsedLabel.text = "Elapsed time : %.2d:%.2d:%.2d"%(hours,minutes,secondes) 

    def update(self, dt):
        self.graph.update_cost(dt)
        self.update_cost(dt)
        self.update_elasped(dt)

class MeetingCostApp(App):
    def __init__(self, **kwargs):
        super(MeetingCostApp, self).__init__(**kwargs)
        self.cost = None
        self.menu = None
        self.meetingWasStopped = None
        self.sm = None
    
    def build(self):
        self.sm = ScreenManager()
        self.cost = MeetingCost(name="cost")
        self.menu = MenuScreen(name="menu")
        self.settings = SettingsScreen(name="settings")
        self.cost.build()
        self.sm.add_widget(self.cost)
        self.sm.add_widget(self.menu)
        self.sm.add_widget(self.settings)
        self.sm.curent = "cost"
        self.bind(on_start = self.post_build_init) 
        return self.sm

    def on_pause(self):
        self.meetingWasStopped = self.cost.stopped
        self.cost.stop_meeting()
        return True

    def on_stop(self):
        self.meetingWasStopped = self.cost.stopped
        self.cost.stop_meeting()
        return True

    def on_resume(self):
        if not self.meetingWasStopped:
            self.cost.start_meeting()

    def _key_handler(self, key, scanCode, codePoint, modifier, args):
        if codePoint == 4:
            if self.sm.current != "menu":
                self.sm.current = "menu"
            else:
                App.get_running_app().stop()

    def post_build_init(self,ev): 
        import android 
        import pygame 

        android.map_key(android.KEYCODE_BACK, 1001) 
        win = self._app_window 
        win.bind(on_keyboard=self._key_handler) 

if __name__=='__main__':
    MeetingCostApp().run()
