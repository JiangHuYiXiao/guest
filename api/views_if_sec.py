# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/6/9 8:53
# @Software       : guest
# @Python_verison : 3.7
from django.contrib import auth as django_auth
import base64

# 用户认证
def user_auth(request):
    # request.META是一个Python的字典，包含了本次HTTP请求的Header信息，例如用户认证、IP地址、用户Agent（通常是浏览器的名词和版本）
    # 桌面应用程序也通过HTTP协议跟Web服务器交互， 桌面应用程序一般不会使用cookie, 而是把"用户名+冒号+密码"
    # 用BASE64算法加密后的字符串放在http request中的headerAuthorization中发送给服务端， 这种方式叫HTTP基本认证(Basic Authentication)
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')     # HTTP_AUTHORIZATION基本认证

    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')   # 对拆分后的list中的索引为1的加密字符串进行解码，然后使用utf-8进行编码，使用：进行分割
    except IndexError:
        return 'null'
    username,password = auth_parts[0],auth_parts[2]
    user = django_auth.authenticate(username=username,password=password)
    if user is not None:
        django_auth.login(request,user)
        return 'success'
    else:
        return 'fali'
