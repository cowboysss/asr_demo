# -*- coding: UTF-8 -*-
import voice_parse as vp

client = vp.parse_zh()

# msg,num = client.get_result()
# if num!=0:
#     print('voice did not parse!')
# else:
#     print(msg,num)

client.get_voice('北京科技')
