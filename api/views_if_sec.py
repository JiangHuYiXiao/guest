# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/6/9 8:53
# @Software       : guest
# @Python_verison : 3.7
from django.contrib import auth as django_auth
import base64
import hashlib,time
from django.core.exceptions import ObjectDoesNotExist

from sign.models import Event

# 接口添加用户认证
from django.http import JsonResponse

def user_auth(request):
    '''用户基本认证'''
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

# 接口添加数字签名

def user_sign(request):
    '''用户签名+时间戳'''
    if request.method == 'POST':
        client_time = request.POST.get('time','')
        client_sign = request.POST.get('sign','')

    else:
        return 'error'
    if client_sign =='' or client_time=='':
        return 'sign null'

    # 服务器时间：
    now_time = time.time()
    server_time =str(now_time).split('.')[0]
    time_diff = int(server_time) - int(client_time)
    if time_diff >=60:
        return 'sign timeout'


    # 签名检查
    md5 = hashlib.md5()
    sign_str = client_time + '&Guest-Bugmaster'
    sign_bytes_utf8 = sign_str.encode(encoding = 'utf-8')
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()

    # h = hashlib.md5(bytes('盐', encoding='utf-8'))
    # h.update(b'jianghu')  # 1e96f616dbeda20c6d50f69af939435b
    # user = h.hexdigest()
    # print(user)  # 6b6429a834dbb43e0c80175f52d31e94
    if server_sign != client_sign:
        return 'sign fail'
    else:
        return 'sign success'



# 查询发布会接口，增加用户认证
def search_event_auth(request):
    auth_result = user_auth(request)      # 调用认证函数
    if auth_result == 'null':
        return JsonResponse({'status':10011,'message':'user auth null'})
    if auth_result == 'fail':
        return JsonResponse({'status':10012,'message':'user auth fail'})

    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')

    # 发布会eid和name都为空，提示parameter
    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        # 发布会eid不存在，查询为空
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})

        else:
            event['name'] = result.name
            event['guest_limit'] = result.guest_limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'query success', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['guest_limit'] = r.guest_limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': 'query success', 'data': datas})
    else:
        return JsonResponse({'status': 10022, 'message': 'query result is empty'})

