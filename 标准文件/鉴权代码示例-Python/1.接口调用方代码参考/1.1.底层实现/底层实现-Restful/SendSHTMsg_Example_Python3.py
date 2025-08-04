#!/bin/python3 
#-*- coding: utf-8 -*-
 
#调用石化通消息推送服务，发送石化通群机器人消息示例 适配Python3 使用pycrytodome库实现AES CBC加密 
 
import requests,json,sys,os,datetime,hmac,hashlib,base64,uuid,urllib
from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad

# Begin AES 加密
# 密钥和初始化向量（从消息推送服务获取密钥接口获取）  
key = b'***********'  
iv = b'************'  

# CBC模式的加密函数，data为明文，key为16字节密钥,iv为偏移量  
def encrypt(data,key,iv): 
    # 补位
    data = pad(data, AES.block_size)             
    #创建加密对象
    aes = AES.new(key=key,mode=AES.MODE_CBC,iv=iv)  
    #encrypt AES加密  B64encode为base64转二进制编码
    result = base64.b64encode(aes.encrypt(data))
    # 以字符串的形式返回
    return str(result,'utf-8')        
# End AES加解密

# URL编码
def urlencode(s):  
    return urllib.parse.quote_from_bytes(s.encode('utf-8'))    # python3中使用
# URL编码

# HMAC算法 Begin
# ak和sk从智云能力开放中心（api网关）中查找应用HMAC认证对应的AppKey、AppSecret
ak = '**********'   # 对应AppKey
sk = '**********'   # 对应AppSecret

# 请求参数HMAC SHA256加密
def EncoderBySha256(str):  
    result = str.encode('utf-8')  # 转换为字节串  
    key = b''  # 初始化密钥为空字节串  
    hmacsha256 = hmac.new(key, result, digestmod=hashlib.sha256)  # 创建HMACSHA256对象，传入密钥和待哈希的字节串  
    output = hmacsha256.digest()  # 计算哈希值  
    strSha256 = base64.b64encode(output).decode('utf-8').replace('-', '').lower()  # 将哈希值转换为字符串，并去除'-'和转换为小写  
    return strSha256
# HMAC签名
def GetSignatureSha256(data, key):  
    key = bytes(key, 'utf-8')  # 将密钥转换为字节串  
    data = bytes(data, 'utf-8')  # 将数据转换为字节串  
    hmacsha256 = hmac.new(key, data, digestmod=hashlib.sha256)  # 创建HMACSHA256对象，传入密钥和待签名的数据  
    hashBytes = hmacsha256.digest()  # 计算哈希值  
    return base64.b64encode(hashBytes).decode('utf-8')  # 将哈希值转换为字符串
# HMAC算法 End

# webhook智云api网关接口地址
webhook="https://t01.gws.jtsh.icloud.sinopec.com/IMPushApi/api/WebhookIMPush/Create"
 
#说明：这里改为自己创建的机器人的webhook的值
#发给石化通机器人的令牌（hook_token）
user=b'*****************'
#发送的报警主题
subject=b'test'
#发送的报警内容
text=b'python test'

# 业务消息ID
msgid = str(uuid.uuid4())

# 消息内容
sendContent = str(subject) +'\n'+ str(text)

# 请求接口包体（此包体为text类型，加签验证示例）
sendMessage={
    "sendType": 1,
    "hook_token": ""+str(user)+"",
    "appId": "",
    "appSecret": "",
    "secret": "替换为自己群机器人中安全设置-加签的密钥",
    "id": ""+msgid+"",
    "msgType": "text",
    "data": "{\"text\":{\"content\":\""+urlencode(sendContent)+"\",\"reminder\":{\"all\":false,\"userIds\":[]}}}"
    }
sendMessage=json.dumps(sendMessage)
content = encrypt(sendMessage.encode(),key,iv)
# 接口请求参数
data={ 
    "content": content, 
    "appCode": "***********"  # 应用编码，同调用石化通消息推送服务获取密钥接口输入的一致
}

# 请求参数HMAC SHA256加密
reqContent = EncoderBySha256(json.dumps(data))
# 生成GMT时间datetime.datetime
# 当前CST时间  
cst_time = datetime.datetime.now()  
# 将CST时区转换为GMT时区  
gmt_time = cst_time - datetime.timedelta(hours=8)  
# 将GMT时间格式化为字符串  
gmt_time_str = gmt_time.strftime("%a, %d %b %Y %H:%M:%S GMT")  
# 组装签名数据
signature_str = 'x-date: '+ gmt_time_str + '\ncontent-sha256: ' + reqContent
# 生成HMAC签名
signature = GetSignatureSha256(signature_str, sk)
# 拼接Authorization Header
auth = "hmac accesskey=\"" + ak + "\", algorithm=\"hmac-sha256\", headers=\"x-date content-sha256\", signature=\"" + signature + "\""
 
headers = {
    "Authorization": auth,
    "X-Date": gmt_time_str,
    "Content-sha256": reqContent,
    'Content-Type': 'application/json'}

# 发送HTTP协议请求（此示例未对HTTPS请求进行证书验证处理，请自行补充）  
x=requests.post(url=webhook,data=json.dumps(data),headers=headers)

# 打开记录日志文件（日志文件存储路径自行调整） 
if os.path.exists("/var/log/example/shtsendmsg.log"):
 
    f=open("/var/log/example/shtsendmsg.log","a+")
 
else:
 
    f=open("/var/log/example/shtsendmsg.log","w+")
 
f.write("\n"+"--"*30)
# 获取返回结果文本，转成json
result = json.loads(x.text)

# 根据请求状态码处理业务（根据应用系统业务自行调整）
if x.status_code == 200:

    if result["status"] == "0":
 
        f.write("\n" + str(datetime.datetime.now()) + "    " + msgid + "    " + str(result["failureMsg"]) + "\n" + str(text))
 
        f.close()
 
    else:
 
        f.write("\n" + str(datetime.datetime.now()) + "    " + msgid + "    " + str(result["failureMsg"]) + "\n" + str(text))
 
        f.close()
else:
    
    f.write("\n" + str(datetime.datetime.now()) + "    " + msgid + "  " + str(x.status_code) + "\n" + str(text))
 
    f.close()
# 将发送的告警信息写入本地日志/var/log/example/shtsendmsg.log中