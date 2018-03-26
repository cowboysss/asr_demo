# -*- coding: UTF-8 -*-
from aip import AipNlp
from datetime import datetime,timedelta
import unicodedata
import machine_id as mi

verb_table = {'打开':1,'开X':1,'开':1,'关闭':0,'关上':0,'关':0}
device_table = \
{\
    '台灯':mi.Desklamp0,\
    '床头灯':mi.Bedlamp0,\
    '客厅灯':mi.SittingroomLight0,\
    '房门':mi.BedroomAccess,\
    '空调':mi.Aircontion0,\
    '房间内温度':mi.Temperature0,\
    '客厅温度':mi.Temperature1,\
    '室外温度':mi.Temperature2,\
    '室内湿度':mi.Humidity0,\
    '室外湿度':mi.Humidity1,\
    '电饭煲':mi.Ecooker0\
    }
days_offset_table = {'明天':1, '后天':2}
hours_offset_base = {'上午':0,'早上':0,'凌晨':0,'下午':12,'晚上':12}
class parse_zh(object):

    def __init__(self):
        self._APP_ID = '10886222'
        self._API_KEY = 'sZxHFVL5MkwBTH5TrUQ7By6e'
        self._SECRET_KEY = '7sQYwp5XDxeUgWaP2Q5X7QLcgMgWrVsK'
        self._nlpClient = AipNlp(self._APP_ID, self._API_KEY, self._SECRET_KEY)

    def get_words(self, text):
        return self._nlpClient.lexer(text)

def get_command_time(basic_words:list)->datetime:
    now = datetime.now()
    control_hours_tmp = 0
    control_minute_tmp = 0
    # print(basic_words)
    # print(now)
    # print(len(basic_words))
    for i in range(0,len(basic_words),1):
        str = basic_words[i]
        # print(str)
        # print(i)
        if str=='明天' or str == '后天':
            control_time_tmp = now+timedelta(days=days_offset_table[str])
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
def get_number_str_from_nlp(basic_words:list,index)->str:
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


client = parse_zh()
msg = client.get_words('明天晚上十一点五十分关闭电饭煲')
# print(msg)
# print(msg['items'])
for item in msg['items']:
    # print(item)
    if item['ne']=='TIME':
        control_time = get_command_time(item['basic_words'])
        print('TIME Process:', control_time)
    elif item['ne']=='':
        print('Other process')
        if item['pos']=='v':
            print('Verb',verb_table[item['item']])
        elif item['pos']=='n':
            print('device_table',device_table[item['item']])
