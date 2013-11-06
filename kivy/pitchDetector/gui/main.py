import kivy
kivy.require('1.1.1')

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from jnius import autoclass

import autocorrelation
import random
from time import time

keyName = ["Not found", "A0", "A0#", "B0", 
           "C1", "C1#", "D1", "D1#", "E1", "F1", "F1#", "G1", "G1#", "A1", "A1#", "B1",
           "C2", "C2#", "D2", "D2#", "E2", "F2", "F2#", "G2", "G2#", "A2", "A2#", "B2",
           "C3", "C3#", "D3", "D3#", "E3", "F3", "F3#", "G3", "G3#", "A3", "A3#", "B3",
           "C4", "C4#", "D4", "D4#", "E4", "F4", "F4#", "G4", "G4#", "A4", "A4#", "B4",
           "C5", "C5#", "D5", "D5#", "E5", "F5", "F5#", "G5", "G5#", "A5", "A5#", "B5",
           "C6", "C6#", "D6", "D6#", "E6", "F6", "F6#", "G6", "G6#", "A6", "A6#", "B6",
           "C7", "C7#", "D7", "D7#", "E7", "F7", "F7#", "G7", "G7#", "A7", "A7#", "B7",
           "C8"]

def computeCorrelation(samples, size, offset):
    dist = 0.0
    for idx in range(0, size):
        s  = float(samples[2*idx] + 255 * samples[2*idx+1] )
        st = float(samples[int(2*(idx))%size] + 255 * samples[int(2*(idx+offset)+1)%size]) 
        dist += s * st
    return dist

def keyFreq(key):
    return  pow(2, (key-49.0) / 12.0) * 440.0

def slowPitchDetection(samples, size, Athres):
    dist = 0
    note = 0
    freq = keyFreq(note)
    maxDist = Athres
    offset = round(44100.0 / freq)


    ct0 = float(computeCorrelation(samples, size, 0))
    dist = computeCorrelation(samples, size, offset) / ct0
    for key in range(27, 53):
        freq = keyFreq(key)
        offset = round(44100.0 / freq)
        dist = computeCorrelation(samples, size, offset) / ct0
#        print "dist : ", dist, " -> ", ct0, " len: ", len(samples)
        if dist > maxDist:
            maxDist = dist
            note = key
    return note, keyName[note]


class PitchDetector(FloatLayout):
    pitchLabel = ObjectProperty()
    pitchLabelPython = ObjectProperty()

    AudioRecord = autoclass('android.media.AudioRecord')
    Buffer  = autoclass('java.nio.ByteBuffer')
    AudioFormat = autoclass('android.media.AudioFormat')
    AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
    buff = Buffer.allocateDirect(3400*2)
    bufferSize = AudioRecord.getMinBufferSize(44100, AudioFormat.CHANNEL_CONFIGURATION_MONO, AudioFormat.ENCODING_PCM_16BIT);
    mAudio = AudioRecord(AudioSource.MIC, 44100, AudioFormat.CHANNEL_CONFIGURATION_MONO, AudioFormat.ENCODING_PCM_16BIT, bufferSize)
    enablePythonCode = True
     
    def build(self):
      self.mAudio.startRecording()

    def startRecord(self):
      Clock.schedule_interval(self.record, .500)
      
    def stopRecord(self):
      Clock.unschedule(self.record)

    def togglePython(self):
      self.enablePythonCode = not self.enablePythonCode     

    def record(self, dt):
      threshold = 0.8
      # create out recorder
      read = self.mAudio.read(self.buff, 3400)
      data = self.buff.array()

      startTime = time()      
      strg = ""
      for d in data:
            strg += "%c"%d

     # Call C code
      self.noteVal, self.note = autocorrelation.autoCorrelation(strg, 3400, threshold)
      last = (time() - startTime)
      if self.note != "Not found":
          self.pitchLabel.text = "%d Samples Recorded : %s in %f"%(read, self.note, last)

      # Call Python code
      startTime = time()
      self.noteVal, self.note = slowPitchDetection(data, 3400, threshold)
      last = (time() - startTime)
      if self.enablePythonCode:
          if self.note != "Not found":
              self.pitchLabelPython.text = "%d Samples Recorded : %s in %f"%(read, self.note, last)
      else:
          self.pitchLabelPython.text = "Python code disabled"

class PitchDetectorApp(App):
    def build(self):
        self.pitch = PitchDetector(name="pitch")
        self.pitch.build()
        return self.pitch

PitchDetectorApp().run()
