# Wegram
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
#chatid查看方法
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
