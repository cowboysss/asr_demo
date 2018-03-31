#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from aip import AipNlp
from datetime import datetime,timedelta
import unicodedata
import machine_id as mi

verb_table = {'打开':1,'开X':1,'开':1,'关闭':0,'关上':0,'关':0,'读取':2,'获取':2}
device_table = \
{\
    '台灯':mi.Desklamp0,\
    '床头灯':mi.Bedlamp0,\
    '客厅灯':mi.SittingroomLight0,\
    '房门':mi.BedroomAccess,\
    '空调':mi.Aircontion0,\
    '房间温度':mi.Temperature0,\
    '客厅温度':mi.Temperature1,\
    '室外温度':mi.Temperature2,\
    '室内湿度':mi.Humidity0,\
    '室外湿度':mi.Humidity1,\
    '电饭煲':mi.Ecooker0,\
    '灯':mi.AllLamp,\
    '门':mi.BedroomAccess\
    }
days_offset_table = {'今天': 0, '明天':1, '后天':2}
hours_offset_base = {'上午':0,'早上':0,'凌晨':0,'下午':12,'晚上':12}

'''
控制命令的类，包含了控制的时间、动作（打开/关闭/读取等动作）
'''
class Control_Command(object):

    def __init__(self, control_time=None, control_action = None, control_device = None, control_params = None):
        self._control_time = control_time
        self._control_action = control_action
        self._control_device = control_device
        self._control_params = control_params

    def set_command(self, control_time=None, control_action = None, control_device = None, control_params = None):
        if control_time is not None:
            self._control_time = control_time
        if control_action is not None:
            self._control_action = control_action
        if control_device is not None:
            self._control_device = control_device
        if control_params is not None:
            self._control_params = control_params

    def ctrl_time(self):
        return self._control_time

    def ctrl_action(self):
        return self._control_action
    
    def ctrl_device(self):
        return self._control_device

    def ctrl_params(self):
        return self._control_params

    def __str__(self):
        if self._control_time is None:
            return 'Control Command:\n{\n\tTime: Now\n\tAction: %r\n\tDevice: %r\n}' % (self._control_action, self._control_device)
        else:
            return 'Control Command:\n{\n\tTime: %r\n\tAction: %r\n\tDevice: %r\n}' % (self._control_time.strftime("%Y-%m-%d %H:%M:%S") ,self._control_action, self._control_device)

'''
从一句中文消息中，解析出控制指令的类
'''
class ParseCommand(object):

    def __init__(self):
        self._APP_ID = '10886222'
        self._API_KEY = 'sZxHFVL5MkwBTH5TrUQ7By6e'
        self._SECRET_KEY = '7sQYwp5XDxeUgWaP2Q5X7QLcgMgWrVsK'
        self._nlpClient = AipNlp(self._APP_ID, self._API_KEY, self._SECRET_KEY)

    def get_words(self, text):
        return self._nlpClient.lexer(text)

    '''TODO: 需要完善解析的过程'''
    def get_command(self,msg:str)->Control_Command:
        parsed_msg = self.get_words(msg)
        print(parsed_msg)
        control_time = None
        control_action = None
        control_device = None

        # code 20180331
        item_number=len(parsed_msg['items'])
        for i in range(item_number):
            item=parsed_msg['items'][i]
            print(item)
            if item['ne']=='TIME':
                control_time = get_command_time(item['basic_words'])
                # print('[1] TIME:', control_time)
            elif item['ne']=='' and item['pos']=='v':
                # 关灯、开灯等词作为动词出现，需提取出设备名 灯、门等 
                verb_tmp = item['item']
                if verb_tmp[1] == '灯' or  verb_tmp[1]=='门':
                    control_device = device_table[verb_tmp[1]]
                    control_action = verb_table[verb_tmp[0]]
                elif verb_tmp in verb_table:
                    control_action = verb_table[verb_tmp]
                else:
                    control_action = -1
                # print('[2] Verb:',control_action)
            elif item['ne']=='' and item['pos']=='n':
                # 把items中连在一起的名词合并成一个名词，作为设备名，例如客厅灯，床头灯等
                # 当名词不在列表里面的时候，设备号为-2或者其他
                device_name_tmp=item['item']
                item_tmp=parsed_msg['items'][i+1]
                while item_tmp['ne']=='' and item_tmp['pos']=='n':
                    device_name_tmp+=item_tmp['item']
                    i+=1
                    item_tmp=parsed_msg['items'][i+1]
                print(i,device_name_tmp)
                if device_name_tmp in device_table:
                    control_device = device_table[device_name_tmp]
                else:
                    control_device = mi.NULL_DEVICE

                # print('[3] Device:',control_device)
        ctrl_command = Control_Command(control_time,control_action,control_device)
        # print(ctrl_command)
        return ctrl_command

def get_command_time(basic_words:list)->datetime:
    now = datetime.now()
    control_time_tmp = now
    control_hours_tmp = 0
    control_minute_tmp = 0
    # print(basic_words)
    # print(now)
    # print(len(basic_words))
    for i in range(0,len(basic_words),1):
        str = basic_words[i]
        # print(str)
        # print(i)
        if str=='明天' or str == '后天' or str == '今天':
            control_time_tmp = control_time_tmp+timedelta(days=days_offset_table[str])
        elif str=='上午' or str == '下午' or str == '晚上' or str == '凌晨':
            control_hours_tmp = hours_offset_base[str]
            # print(control_hours_tmp)
        elif str[-1]=='点':
            # 获得小时数
            # 1' 获得点之前的数字
            hour_str = get_number_str_from_nlp(basic_words,i)
            # print(hour_str)
            # 2' 数字转int
            # control_hours_tmp_2 = zh_to_digital(hour_str)
            control_hours_tmp += zh_to_digital(hour_str)
        elif str[-1]=='分':
            # 获得分钟数
            # 1' 获得点之前的数字
            minute_str = get_number_str_from_nlp(basic_words,i)
            # print(minute_str)
            # 2' 数字转int
            # control_minute_tmp_2 = zh_to_digital(minute_str)
            control_minute_tmp = zh_to_digital(minute_str)
    # print(control_time_tmp)
    # print(hour_str,control_hours_tmp,'小时')
    # print(minute_str,control_minute_tmp,'分钟')    
    control_time = datetime(control_time_tmp.year, control_time_tmp.month, control_time_tmp.day, control_hours_tmp, control_minute_tmp)
    # print('控制时间',control_time)
    # print(type(control_time))
    return control_time

'''获得点，分等关键字前面的数字字符串，并将这些字符串连起来'''
def get_number_str_from_nlp(basic_words:list,index:int)->str:
    ret_str = ''
    flag = True
    loc = index

    while flag:
        loc = loc - 1
        tmp_str = basic_words[loc]
        tmp_str_len = len(tmp_str)
        # print(loc,tmp_str,tmp_str_len)
        for i in range(tmp_str_len):
            flag = flag and is_number(tmp_str[i])
    loc = loc+1
    while loc < index:
        ret_str=ret_str+basic_words[loc]
        loc = loc+1

    # 单独处理含点的字符串
    tmp_str = basic_words[index]
    tmp_str_len = len(tmp_str)
    # print(index,tmp_str,tmp_str_len)
    flag = True
    if tmp_str_len>1:
        for i in range(tmp_str_len-1):
            # print(is_number(tmp_str[i]))
            flag = flag and is_number(tmp_str[i])
    if flag:
        ret_str=ret_str+tmp_str[0:tmp_str_len-1]
        
    # print(ret_str)
    return ret_str    

'''判断是否为数字'''
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

'''两位数及以下的中文数字转int'''
def zh_to_digital(str:str)->int:
    str_len = len(str)
    ten_loc = -1
    ret_val = 0
    for i in range(str_len):
        if str[i]=='十':
            ten_loc = i
    
    if ten_loc == 0:
        ret_val = unicodedata.numeric(str[ten_loc])
        if ten_loc < str_len-1:
            ret_val += unicodedata.numeric(str[ten_loc+1])
    elif ten_loc == 1:
        ret_val = unicodedata.numeric(str[ten_loc-1])*10
        if ten_loc < str_len-1:
            ret_val += unicodedata.numeric(str[ten_loc+1])
    elif ten_loc == -1:
        ret_val = unicodedata.numeric(str[ten_loc+1])

    return int(ret_val)

''' NOTICE: 使用本文件NLP的正确姿势 '''
def main():
    client = ParseCommand()
    command = client.get_command('明天晚上十一点五十分关闭电饭煲')
    print(command)

'''
明天晚上十一点五十分打开电饭煲
打开卧室灯
明天上午十点关闭客厅灯
开门
关灯
开灯
关上卧室灯
'''
def test_single(client, msg):
    command = client.get_command(msg)
    print(msg,'\n', command)

def unit_test():
    client =  ParseCommand()
    test_single(client, '明天晚上十一点五十分打开电饭煲')
    # test_single(client, '打开卧室灯') # 卧室和灯分开解析，初步是第一个名词下一个是否为名词，是就合并在一起作为一个名词
    # test_single(client, '明天上午十点关闭灯') # 客厅和灯分开
    # test_single(client, '开门') # 开门是连在一起的
    # test_single(client, '关灯') # 关灯是连在一起的
    # test_single(client, '开灯') # 开灯是连在一起的
    test_single(client, '打开电饭煲')
    test_single(client, '晚上十点打开灯')
    test_single(client, '今天晚上十点打开灯')


if __name__ == '__main__':
    # main()
    unit_test()
