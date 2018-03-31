## 程序文件说明
demo.py为录音和语音识别的测试运行文件
record_demo.py 是录音的测试运行文件
unit_nlp.py 是SnowNlp的测试运行文件

server.py 是main文件，服务部分的程序运行该文件
voice_parse.py为录音和语音识别的class文件和函数文件
nlp_baidu.py 是利用百度云进行NLP的相关程序，可以直接从提取的汉语文字中进行控制指令的提取
machine_id.py 是设备的id号


基于Python 3.5开发

## 依赖文件如下
1. 百度语音SDK库文件，安装方法`pip install baidu-aip`
2. playsound包，播放语音用，安装方法`pip install playsound`


## 程序实现步骤：
1. 录音，并保存文件，录音格式 PCM 16k 16bit位深单声道，不超过60s，文件名demo.pcm
    - 录音部分目前思路：通过按键按下录音，按键释放，录音结束
    - 升级目标：按键按一下开始录音，自动判断不说话时停止录音
    - 终极目标：通过指定的语音唤醒，例如，小派帮我打开空调！
2. 语音识别并获取返回数据，封装成函数
3. 进行命令匹配，获取控制指令，输出操作
4. 对控制指令进行语音合成并播放（提前获取需要播放的语音指令，并进行播放）

## 写一个Bash脚本，实现功能，对一些需要的python包进行安装，[稍后实现]
1. aipspeech 百度在线语音识别包
2. playsound包，播放语音用
