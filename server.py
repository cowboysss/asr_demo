#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2018-03-25 9:08
# @Author  : Joseph Wang
# @File    : server.py

import voice_parse as vp

class control_server(object):
    
    def __init__(self):
        '''run mode参数的定义'''
        self.RUN_ONCE=0
        self.RUN_WHEN_KEY_CTRL=1

        self.client = vp.parse_zh()
        # TODO: NLP相关类的初始化
        # TODO: Iot Interface相关类的初始化


    def wait_key_press(self):
        '''
        return true if key is pressed
        return false if key isn't press
        '''
        # TODO: 增加获取按键状态的指令
        return False

    def speech_and_control(self):
        '''
        1' record speech
        2' parse speech
        3' get control command according to the speech
        4' control device
        '''
        self.client.record_voice()
        self.msg,self.num = self.client.get_result()
        if self.num!=0:
            print('voice did not parse!')
            self.client.get_voice('未能正确识别语音')
        else:
            print(self.msg,self.num)
            # TODO: 对msg进行解析并获得control command 
            # TODO: 根据control command进行control控制
            self.client.get_voice('识别成功')

    def run(self, mode=0):
        '''
        mode:
        0 表示只运行一次
        '''
        if mode==self.RUN_ONCE:
            self.speech_and_control()
        elif mode == self.RUN_WHEN_KEY_CTRL:
            while 1:
                if self.wait_key_press():
                    self.speech_and_control()
                else:
                    # TODO: delay and wait net loop
                    pass
    

if __name__=="__main__":
    main_client = control_server()
    main_client.run()
