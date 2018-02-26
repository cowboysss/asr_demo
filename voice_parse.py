# -*- coding: UTF-8 -*-
from aip import AipSpeech
from playsound import playsound
import os
class parse_zh(object):

    def __init__(self):
        self._APP_ID = '10852898'
        self._API_KEY = '7GsURiUfKWzPz0Ppl4tjipTg'
        self._SECRET_KEY = '9d2a195cc287eaef7e96572e0370b67b'
        self._client = AipSpeech(self._APP_ID, self._API_KEY, self._SECRET_KEY)

    # 读取文件
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    
    def get_result(self):
        self._req = self._client.asr(self.get_file_content('16k.wav'), 'pcm', 16000, {
            'lan': 'zh',
        })
        return self._req['result'][0],self._req['err_no']

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

def record_voice(savename):
    pass
