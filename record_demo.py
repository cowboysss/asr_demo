# -*- coding: UTF-8 -*-
import wave
from pyaudio import PyAudio,paInt16
from datetime import datetime
import numpy as np

#define of params
NUM_SAMPLES = 1024
framerate = 16000
channels = 1
sampwidth = 2
#record time
TIME = 4

def save_wave_file(filename, data):
    '''save the date to the wav file'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


def record_wave():
    #open the input of wave
    pa = PyAudio()
    stream = pa.open(format = paInt16, channels = 1,
            rate = framerate, input = True,
            frames_per_buffer = NUM_SAMPLES)
    save_buffer = []
    print('recording...')
    for i in range(0, int(framerate/NUM_SAMPLES*TIME)):
        data = stream.read(NUM_SAMPLES)
        save_buffer.append(data)

    stream.stop_stream()
    stream.close()
    pa.terminate()
 
    filename = "16k.wav"  # datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".wav"
    save_wave_file(filename, save_buffer)
    save_buffer = []
    print(filename, "saved")

record_wave()

