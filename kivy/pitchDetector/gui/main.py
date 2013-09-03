import kivy
kivy.require('1.1.1')

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock

from jnius import autoclass

import autocorrelation
import random


class PitchDetector(Widget):
    pitchLabel = ObjectProperty()

    AudioRecord = autoclass('android.media.AudioRecord')
    Buffer  = autoclass('java.nio.ByteBuffer')
    AudioFormat = autoclass('android.media.AudioFormat')
    AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
    buff = Buffer.allocateDirect(3400*2)
    bufferSize = AudioRecord.getMinBufferSize(44100, AudioFormat.CHANNEL_CONFIGURATION_MONO, AudioFormat.ENCODING_PCM_16BIT);
    mAudio = AudioRecord(AudioSource.MIC, 44100, AudioFormat.CHANNEL_CONFIGURATION_MONO, AudioFormat.ENCODING_PCM_16BIT, bufferSize)
     
    def build(self):
      self.noteLabel.text = "No key pressed"
      self.mAudio.startRecording()

    def startRecord(self, dummy):
      Clock.schedule_interval(self.record, .500)
      
    
    def record(self, dt):
      startTime = time()	
    
      # create out recorder
      read = self.mAudio.read(self.buff, 3400)
      data = self.buff.array()
      read += self.mAudio.read(self.buff, 3400)
      data += self.buff.array()
      
      #print data
      strg = ""
      for d in data:
            strg += "%c"%d
      self.noteVal, self.note = autocorrelation.autoCorrelation(strg, 3400, 1e6, 0.9)
      last = (time() - startTime)
      self.noteLabel.text = "%d Samples Recorded : %s in %f with E = %f"%(read, self.note, last, E)

class PitchDetectorApp(App):
    def build(self):
        self.pitch = PitchDetector(name="pitch")
        self.pitch.build()
        return self.pitch

PianoMasterApp().run()
