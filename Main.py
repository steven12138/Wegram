import telebot
import itchat
import threading
from PIL import Image
import imghdr
import time
import os

bot=telebot.TeleBot("<token>")  #change to your TOKEN
chatid='<chatid>'       #change to your CHATID
me=None
myid=None
lasti=""
lastmsgid=""
lastmsg= {}
auto="happy"
loginflag=0

class sendpic(threading.Thread):
    def __init__(self,threadid,name):
        threading.Thread.__init__(self)
        self.threadid=threadid
        self.name=name
    def run(self):
        bot.send_message(chatid,"relogin")
        time.sleep(5)
        qr=open("QR.png",mode='rb')
        bot.send_photo(chatid,qr)

@bot.message_handler(commands=['login'])
def relogin(msg):
    itchat.logout()
    global loginflag
    sendp =  sendpic(1,'sendpic')
    sendp.start()
    itchat.auto_login()
    bot.send_message(chatid,"login")
    loginflag=1
    global me,myid
    me=itchat.search_friends()
    print(me)
    myid = me['UserName']


#处理微信发来的图片
@itchat.msg_register(itchat.content.PICTURE)
def backphotototg(msg):
    global lastid
    s=msg['FileName']
    l=len(s)
    userid=msg['FromUserName']
    friend=itchat.search_friends(userName=userid)
    nickname=friend['RemarkName']
    if len(nickname)==0:
        nickname=friend['NickName']
    name='totg'+s[l-4:]
    msg['Text'](name)
    img=open(name,mode='rb')
    if imghdr.what(img)!=s[l-3:] and s[l-3:]=="gif":    #如果微信发的表情包无法正常转换成为gif
        bot.send_message(chatid,"Unsupported message type")
        return
    bot.send_photo(chatid,img,caption=nickname)       #发送图片到telegram
    lastid = msg['FromUserName']                      #记录ID，方便直接回话
    return


#处理文字消息
@itchat.msg_register(itchat.content.TEXT)
def getmsg(msg):
    #print(msg)
    global lastid
    nick= itchat.search_friends(userName=msg['FromUserName'])       #查找发信人的昵称或备注
    nick=nick['RemarkName']
    print(nick)
    if len(nick)==0:
        nick=itchat.search_friends(userName=msg['FromUserName'])['NickName']
    lastid=msg['FromUserName']
    if msg['FromUserName']!=myid:
        bot.send_message(chatid,"%s\n" % nick+msg.text)             #过滤自己发送的信息

#处理chat命令
@bot.message_handler(commands=['chat'])
def startchat(msg):
    global loginflag
    if loginflag==0:
        bot.send_message(chatid,"you haven't login")
        return
    global lastid
    name=msg.text[6:]
    if len(name)==0:        #处理错误选项
        bot.send_message(chatid,"Error")
        return
    last=itchat.search_friends(remarkName=name)
    if len(last)==0:
        last=itchat.search_friends(nickName=name)
        if len(last)==0:
            bot.send_message(chatid,"Con't find user named %s" % name)
        else:
            lastid=last[0]['UserName']
            bot.send_message(chatid,"You can talk with %s" % name)
    else:
        lastid=last[0]['UserName']
        bot.send_message(chatid,"You can talk with %s" % name)
#撤回revoke命令
@bot.message_handler(commands=['revoke'])
def revoke(msg):
    global lastmsg,lastmsgid
    lastmsg=itchat.revoke(lastmsgid,lastid)

#查询好友列表
@bot.message_handler(commands=['friendlist'])
def showlist(msg):
    global loginflag
    if loginflag == 0:
        bot.send_message(chatid, "you haven't login")
        return
    bot.send_message(chatid,"Searching, it maybe takes a while") #提示开始搜索，心理安慰
    s=itchat.get_friends(update=True)[0:]
    list=""
    cnt=0
    for i in s:
        if len(i.RemarkName)==0:
            list+=i.NickName
        else:
            list+=i.RemarkName
        list+='\n'
        if cnt%100==0:
            bot.send_message(chatid, list)
            list=""
        cnt+=1
    bot.send_message(chatid,"查询完毕，总共%d位好友"%cnt)

#处理telegram发送的图片
@bot.message_handler(content_types=['photo'])
def image(message):
    global loginflag
    if loginflag == 0:
        bot.send_message(chatid, "you haven't login")
        return
    global lastmsg,lastmsgid
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)             #保存图片
    if lastid=='':
        bot.send_message(chatid,'no user')
    else:
        itchat.send_image('image.jpg',toUserName=lastid)

#telegram表情包
@bot.message_handler(content_types=['sticker'])
def sticker(message):
    global loginflag
    if loginflag == 0:
        bot.send_message(chatid, "you haven't login")
        return
    global lastmsg,lastmsgid
    fileID=message.sticker.file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image1.webp", 'wb') as new_file:
        new_file.write(downloaded_file)             #保存
    im = Image.open('image1.webp').convert("RGB")   #格式转换webp to jpg
    im.save("image1.jpg", "JPEG")
    if lastid=="":
        bot.send_message(chatid,"no user")
    else:
        itchat.send_image('image1.jpg',toUserName=lastid)

#处理文字消息
@bot.message_handler()
def send(msg):
    global loginflag
    if loginflag == 0:
        bot.send_message(chatid, "you haven't login")
        return
    global lastmsg,lastmsgid
    if lastid=="":
        bot.send_message(chatid,"no user")
    else:
        lastmsg=itchat.send(msg.text,toUserName=lastid)
        lastmsgid=lastmsg['MsgID']                      #记录msgid，以便于撤回


#新建线程处理微信，主线程处理tg
class wechatlistener(threading.Thread):
    def __init__(self,threadid,name):
        threading.Thread.__init__(self)
        self.threadid=threadid
        self.name=name
    def run(self):
        itchat.run()

wechatlistener=wechatlistener(1,"thread1")
wechatlistener.start()
bot.polling()
