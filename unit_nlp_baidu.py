# -*- coding: UTF-8 -*-
from aip import AipNlp
import time

verb_table = {'打开':1,'关闭':0}
device_table = {'电饭煲':1,'空调':2,'电视机':3,'窗帘':4}

# class parse_zh(object):

#     def __init__(self):
#         self._APP_ID = '10886222'
#         self._API_KEY = 'sZxHFVL5MkwBTH5TrUQ7By6e'
#         self._SECRET_KEY = '7sQYwp5XDxeUgWaP2Q5X7QLcgMgWrVsK'
#         self._nlpClient = AipNlp(self._APP_ID, self._API_KEY, self._SECRET_KEY)

#     def get_words(self, text):
#         return self._nlpClient.lexer(text)

def get_command_time(basic_words):
    cur_time = time.localtime(time.time())
    command_year = cur_time.tm_year
    command_mon = cur_time.tm_mon
    command_mday = cur_time.tm_mday
    command_hour = cur_time.tm_hour
    command_min = cur_time.tm_min

    


# client = parse_zh()
# msg = client.get_words('明天下午十点关闭电饭煲')
# print(msg)
# print(msg['items'])
# for item in msg['items']:
#     print(item)
#     if item['ne']=='TIME':
#         print('TIME Process')
#     elif item['ne']=='':
#         print('Other process')
#         if item['pos']=='v':
#             print('Verb',verb_table[item['item']])
#         elif item['pos']=='n':
#             print('device_table',device_table[item['item']])

cur_time = time.localtime(time.time())
print(cur_time)
print(type(cur_time))
print(cur_time.tm_year)
print(cur_time.tm_mon)
print(cur_time.tm_mday)
print(cur_time.tm_hour)
print(cur_time.tm_min)
