# Wegram
!!! This project is now non-functional and needs to be repaired. !!!

Current Exceptions:

when search friendlist
```python
Traceback (most recent call last):
  File "/root/Wegram/Main.py", line 197, in <module>
    bot.polling()
  File "/usr/local/lib/python3.10/dist-packages/telebot/__init__.py", line 1043, in polling
    self.__threaded_polling(non_stop=non_stop, interval=interval, timeout=timeout, long_polling_timeout=long_polling_timeout,
  File "/usr/local/lib/python3.10/dist-packages/telebot/__init__.py", line 1118, in __threaded_polling
    raise e
  File "/usr/local/lib/python3.10/dist-packages/telebot/__init__.py", line 1074, in __threaded_polling
    self.worker_pool.raise_exceptions()
  File "/usr/local/lib/python3.10/dist-packages/telebot/util.py", line 147, in raise_exceptions
    raise self.exception_info
  File "/usr/local/lib/python3.10/dist-packages/telebot/util.py", line 90, in run
    task(*args, **kwargs)
  File "/usr/local/lib/python3.10/dist-packages/telebot/__init__.py", line 6801, in _run_middlewares_and_handler
    result = handler['function'](message)
  File "/root/Wegram/Main.py", line 122, in showlist
    if len(i.RemarkName)==0:
AttributeError: 'dict' object has no attribute 'RemarkName'
```

when login
```python
Traceback (most recent call last):
  File "/usr/local/lib/python3.10/dist-packages/itchat/components/login.py", line 239, in maintain_loop
    msgList = produce_msg(self, msgList)
  File "/usr/local/lib/python3.10/dist-packages/itchat/components/messages.py", line 56, in produce_msg
    utils.msg_formatter(m, 'Content')
  File "/usr/local/lib/python3.10/dist-packages/itchat/utils.py", line 69, in msg_formatter
    d[k]  = htmlParser.unescape(d[k])
AttributeError: 'HTMLParser' object has no attribute 'unescape'
```

# 通过hello world.py 在你的telegram上使用wechat
#使用方法

##安装必要的库
```
pip install itchat
pip install pytelegramBotAPI
pip install pillow
```
把token改成你的token

把chatid修改成你的chatid
# chatid查看方法
https://api.telegram.org/bot"token"/getUpdates

替换"token"为你的token，然后发送一条消息再刷新网页。可以看到消息详情。当中有一项为chatid，复制即可。
每个人和同一个机器人拥有唯一chatid，只需查看一次后一劳永逸


根据官方说明文档，修改chatid 到机器人与你的chatid
直接发送消息聊天，可以处理贴纸图片和表情
# /chat [name]
使用这个命令来选择与谁聊天
当有人给你发消息时，你可以直接在下面回复
# /friendlist
使用这个命令来查看好友列表
# /revoke
使用这个命令来撤回最后一条消息
# /login
使用这个命令来登陆，由于微信防止盗号机制，二维码只能使用摄像头扫描
