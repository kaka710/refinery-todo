#!/bin/python3 
#-*- coding: utf-8 -*-
 
#����ʯ��ͨ��Ϣ���ͷ��񣬷���ʯ��ͨȺ��������Ϣʾ�� ����Python3 ʹ��pycrytodome��ʵ��AES CBC���� 
 
import requests,json,sys,os,datetime,hmac,hashlib,base64,uuid,urllib
from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad

# Begin AES ����
# ��Կ�ͳ�ʼ������������Ϣ���ͷ����ȡ��Կ�ӿڻ�ȡ��  
key = b'***********'  
iv = b'************'  

# CBCģʽ�ļ��ܺ�����dataΪ���ģ�keyΪ16�ֽ���Կ,ivΪƫ����  
def encrypt(data,key,iv): 
    # ��λ
    data = pad(data, AES.block_size)             
    #�������ܶ���
    aes = AES.new(key=key,mode=AES.MODE_CBC,iv=iv)  
    #encrypt AES����  B64encodeΪbase64ת�����Ʊ���
    result = base64.b64encode(aes.encrypt(data))
    # ���ַ�������ʽ����
    return str(result,'utf-8')        
# End AES�ӽ���

# URL����
def urlencode(s):  
    return urllib.parse.quote_from_bytes(s.encode('utf-8'))    # python3��ʹ��
# URL����

# HMAC�㷨 Begin
# ak��sk�����������������ģ�api���أ��в���Ӧ��HMAC��֤��Ӧ��AppKey��AppSecret
ak = '**********'   # ��ӦAppKey
sk = '**********'   # ��ӦAppSecret

# �������HMAC SHA256����
def EncoderBySha256(str):  
    result = str.encode('utf-8')  # ת��Ϊ�ֽڴ�  
    key = b''  # ��ʼ����ԿΪ���ֽڴ�  
    hmacsha256 = hmac.new(key, result, digestmod=hashlib.sha256)  # ����HMACSHA256���󣬴�����Կ�ʹ���ϣ���ֽڴ�  
    output = hmacsha256.digest()  # �����ϣֵ  
    strSha256 = base64.b64encode(output).decode('utf-8').replace('-', '').lower()  # ����ϣֵת��Ϊ�ַ�������ȥ��'-'��ת��ΪСд  
    return strSha256
# HMACǩ��
def GetSignatureSha256(data, key):  
    key = bytes(key, 'utf-8')  # ����Կת��Ϊ�ֽڴ�  
    data = bytes(data, 'utf-8')  # ������ת��Ϊ�ֽڴ�  
    hmacsha256 = hmac.new(key, data, digestmod=hashlib.sha256)  # ����HMACSHA256���󣬴�����Կ�ʹ�ǩ��������  
    hashBytes = hmacsha256.digest()  # �����ϣֵ  
    return base64.b64encode(hashBytes).decode('utf-8')  # ����ϣֵת��Ϊ�ַ���
# HMAC�㷨 End

# webhook����api���ؽӿڵ�ַ
webhook="https://t01.gws.jtsh.icloud.sinopec.com/IMPushApi/api/WebhookIMPush/Create"
 
#˵���������Ϊ�Լ������Ļ����˵�webhook��ֵ
#����ʯ��ͨ�����˵����ƣ�hook_token��
user=b'*****************'
#���͵ı�������
subject=b'test'
#���͵ı�������
text=b'python test'

# ҵ����ϢID
msgid = str(uuid.uuid4())

# ��Ϣ����
sendContent = str(subject) +'\n'+ str(text)

# ����ӿڰ��壨�˰���Ϊtext���ͣ���ǩ��֤ʾ����
sendMessage={
    "sendType": 1,
    "hook_token": ""+str(user)+"",
    "appId": "",
    "appSecret": "",
    "secret": "�滻Ϊ�Լ�Ⱥ�������а�ȫ����-��ǩ����Կ",
    "id": ""+msgid+"",
    "msgType": "text",
    "data": "{\"text\":{\"content\":\""+urlencode(sendContent)+"\",\"reminder\":{\"all\":false,\"userIds\":[]}}}"
    }
sendMessage=json.dumps(sendMessage)
content = encrypt(sendMessage.encode(),key,iv)
# �ӿ��������
data={ 
    "content": content, 
    "appCode": "***********"  # Ӧ�ñ��룬ͬ����ʯ��ͨ��Ϣ���ͷ����ȡ��Կ�ӿ������һ��
}

# �������HMAC SHA256����
reqContent = EncoderBySha256(json.dumps(data))
# ����GMTʱ��datetime.datetime
# ��ǰCSTʱ��  
cst_time = datetime.datetime.now()  
# ��CSTʱ��ת��ΪGMTʱ��  
gmt_time = cst_time - datetime.timedelta(hours=8)  
# ��GMTʱ���ʽ��Ϊ�ַ���  
gmt_time_str = gmt_time.strftime("%a, %d %b %Y %H:%M:%S GMT")  
# ��װǩ������
signature_str = 'x-date: '+ gmt_time_str + '\ncontent-sha256: ' + reqContent
# ����HMACǩ��
signature = GetSignatureSha256(signature_str, sk)
# ƴ��Authorization Header
auth = "hmac accesskey=\"" + ak + "\", algorithm=\"hmac-sha256\", headers=\"x-date content-sha256\", signature=\"" + signature + "\""
 
headers = {
    "Authorization": auth,
    "X-Date": gmt_time_str,
    "Content-sha256": reqContent,
    'Content-Type': 'application/json'}

# ����HTTPЭ�����󣨴�ʾ��δ��HTTPS�������֤����֤���������в��䣩  
x=requests.post(url=webhook,data=json.dumps(data),headers=headers)

# �򿪼�¼��־�ļ�����־�ļ��洢·�����е����� 
if os.path.exists("/var/log/example/shtsendmsg.log"):
 
    f=open("/var/log/example/shtsendmsg.log","a+")
 
else:
 
    f=open("/var/log/example/shtsendmsg.log","w+")
 
f.write("\n"+"--"*30)
# ��ȡ���ؽ���ı���ת��json
result = json.loads(x.text)

# ��������״̬�봦��ҵ�񣨸���Ӧ��ϵͳҵ�����е�����
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
# �����͵ĸ澯��Ϣд�뱾����־/var/log/example/shtsendmsg.log��