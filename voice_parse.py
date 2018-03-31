# -*- coding: UTF-8 -*-
from aip import AipSpeech
from playsound import playsound
import wave
from pyaudio import PyAudio,paInt16
import os

class parse_zh(object):

    def __init__(self):
        self._APP_ID = '10852898'
        self._API_KEY = '7GsURiUfKWzPz0Ppl4tjipTg'
        self._SECRET_KEY = '9d2a195cc287eaef7e96572e0370b67b'
        self._client = AipSpeech(self._APP_ID, self._API_KEY, self._SECRET_KEY)

        self._chuck = 4096
        self._sample_rate =44100
        self._channels = 1
        self._samplewidth = 2
        self._sample_time = 4 # s

        self._record_speech_name = 'recorded_speech.wav' 

    # 读取文件
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    
    def get_result(self):
        # self.record_voice()
        print('parsing speech...')
        self._req = self._client.asr(self.get_file_content("recorded_speech.pcm"), 'pcm', 16000, {
            'lan': 'zh',
        })
        print(self._req)
        if self._req['err_no']==0:
            return self._req['result'][0],self._req['err_no']
        else:
            return None,self._req['err_no']

    def get_voice(self, msg):
        self._ret_voice  = self._client.synthesis(msg, 'zh', 1, {
            'vol': 5,
        })
        if not isinstance(self._ret_voice, dict):
            with open('audio.mp3', 'wb') as f:
                f.write(self._ret_voice)
            os.system('omxplayer audio.mp3')
            # playsound('audio.mp3')
        return self._ret_voice

    def save_wave_file(self,filename, data):
        '''save the date to the wav file'''
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self._channels)
        wf.setsampwidth(self._samplewidth)
        wf.setframerate(self._sample_rate)
        wf.writeframes(b"".join(data))
        wf.close()

    def record_voice(self):
        #open the input of wave
        pa = PyAudio()
        stream = pa.open(format = paInt16, channels = self._channels, rate = self._sample_rate, input = True,input_device_index=2 ,frames_per_buffer = self._chuck)
        save_buffer = []
        print('recording...')
        for i in range(0, int(self._sample_rate/self._chuck*self._sample_time)):
            data = stream.read(self._chuck, exception_on_overflow = False)
            save_buffer.append(data)

        stream.stop_stream()
        stream.close()
        pa.terminate()
    
        # datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".wav"
        self.save_wave_file(self._record_speech_name, save_buffer)
        save_buffer = []
        print(self._record_speech_name, "saved")
        print('speech record OK!')
        os.system("ffmpeg -y -f s16le -ac 1 -ar 44100 -i recorded_speech.wav -acodec pcm_s16le -f s16le -ac 1 -ar 16000 recorded_speech.pcm -loglevel -8")
    
