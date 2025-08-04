#!/bin/python 
#-*- coding: utf-8 -*-
 
#����ʯ��ͨ��Ϣ���ͷ��񣬷���ʯ��ͨȺ��������Ϣʾ�� ����Python2.7 ʹ��pycryto��ʵ��AES CBC����
 
import requests,json,sys,os,datetime,hmac,hashlib,base64,uuid,urllib
from Crypto.Cipher import AES  

# Begin AES ����
# ��Կ�ͳ�ʼ������������Ϣ���ͷ����ȡ��Կ�ӿڻ�ȡ��  
key = b'***********'  
iv = b'************'  

# CBCģʽ�ļ��ܺ�����dataΪ���ģ�keyΪ16�ֽ���Կ,ivΪƫ����        
def encrypt(data,key,iv):
    data=pad(data, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)    
    result = base64.b64encode(cipher.encrypt(data.encode('utf-8')))
    return result.decode('utf-8')

def pad(data, block_size):
    padding_size = block_size - (len(data) % block_size)
    padding = chr(padding_size) * padding_size
    return data + padding
# End AES�ӽ���

# URL����
def urlencode(s):  
    return urllib.quote(s.encode('utf-8'))  # python2.7��ʹ��quote
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
    key = bytes(key)  # ����Կת��Ϊ�ֽڴ�  
    data = bytes(data)  # ������ת��Ϊ�ֽڴ�  
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
sendContent = subject.decode('utf-8') +'\n'+ text.decode('utf-8')

# ����ӿڰ��壨�˰���Ϊtext���ͣ���ǩ��֤ʾ����
sendMessage={
    "sendType": 1,
    "hook_token": ""+user.decode('utf-8')+"",
    "appId": "",
    "appSecret": "",
    "secret": "�滻Ϊ�Լ�Ⱥ�������а�ȫ����-��ǩ����Կ",
    "id": ""+msgid+"",
    "msgType": "text",
    "data": "{\"text\":{\"content\":\""+ urlencode(sendContent) +"\",\"reminder\":{\"all\":false,\"userIds\":[]}}}"
    }
sendMessage=json.dumps(sendMessage,ensure_ascii=False)
content = encrypt(sendMessage,key,iv)
# �ӿ��������
data={ 
    "content": content, 
    "appCode": "***********"    # Ӧ�ñ��룬ͬ����ʯ��ͨ��Ϣ���ͷ����ȡ��Կ�ӿ������һ��
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
 
        # ��text��ASCII����ΪUnicode�ַ���
        decoded_rtext = result["failureMsg"]
        # ��Unicode�ַ�������ΪUTF-8�ֽ�����
        encoded_rtext = decoded_rtext.encode('utf-8')
        
        f.write("\n" + str(datetime.datetime.now()) + "    " + msgid + "    " + encoded_rtext + "\n" + str(text))
 
        f.close()
 
    else:
        
        # ��text��ASCII����ΪUnicode�ַ���
        decoded_rtext = result["failureMsg"]
        # ��Unicode�ַ�������ΪUTF-8�ֽ�����
        encoded_rtext = decoded_rtext.encode('utf-8')
        
        f.write("\n" + str(datetime.datetime.now()) + "    " + msgid + "    " + encoded_rtext + "\n" + str(text))
 
        f.close()
else:
    
    f.write("\n" + str(datetime.datetime.now()) + "    " + msgid + "  " + str(x.status_code) + "\n" + str(text))
 
    f.close()
# �����͵���Ϣд�뱾����־/var/log/example/shtsendmsg.log��