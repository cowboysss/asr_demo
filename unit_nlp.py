# -*- coding: UTF-8 -*-
from snownlp import SnowNLP

verb_table = {u'打开':1,u'关闭':0}
device_table = {u'电饭煲':1,u'空调':2,u'电视机':3,u'窗帘':4}

str_std = u'打开'
s = SnowNLP(u'明天下午十点关闭电饭煲，')
# print(s.words)
# tags = [x for x in s.tags]
# print(tags)
# print(s.pinyin)
for split_word in s.tags:
    if split_word[1] == 'v':
        command_v = verb_table[split_word[0]]
    elif split_word[1] == 'n':
        command_n = device_table[split_word[0]]
    print(split_word)
    print(type(split_word))
print(command_v,command_n)
