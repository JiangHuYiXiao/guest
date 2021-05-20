from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from sign.models import Event, Guest
import time

# Create your views here.


# 发布会添加接口
def add_event(request):
    eid = request.POST.get('eid','')
    name = request.POST.get('name','')
    limit = request.POST.get('limit','')
    status = request.POST.get('status','')
    address = request.POST.get('address','')
    start_time = request.POST.get('start_time','')
    if eid== '' or name =='' or limit == '' or status =='' or address =='' or start_time =='':
        return JsonResponse({'status':10021,'message':'parameter error'})

    result = Event.objects.filter(id = eid)
    if result:
        return JsonResponse({'status':10022,'message':'event id already exists'})
    result = Event.objects.filter(name =name)
    if result:
        return JsonResponse({'status':10023,'message':'event name already exists'})
    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid,name=name,limit=limit,status=status,address=address,start_time=start_time)

    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format'
        return JsonResponse({'status':10024,'message':'error'})
    return JsonResponse({'status':200,'message':'add event success'})


# 发布会查询接口
def search_event(request):
    eid = request.GET.get('eid','')
    name = request.GET.get('name','')


    if eid == '' and name == '':
        return JsonResponse({'status':10021,'message':'parameter error'})
    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'query result is empty'})

        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status':200,'message':'query success','data':event})

    if name !='':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event ={}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status':200,'message':'query success','data':datas})
    else:
        return JsonResponse({'status':10022,'message':'query result is empty'})

# 添加嘉宾接口

def add_guest(request):
    eid = request.POST.get('eid','')
    realname = request.POST.get('realname','')
    phone = request.POST.get('phone','')
    email = request.POST.get('email','')

    # 判断eid，phone，realname是否为空
    if eid=='' or phone=='' or realname=='':
        return JsonResponse({'status0':10021,'message':'parameter is error'})

    # 判断eid是否在Event表存在
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'eid not in event'})

    # 判断发布会状态是否发布
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023,'message':'event status not available'})

    # 判断发布会已经添加的人数是否饱和
    guest_limit = Guest.objects.filter(event_id=eid)            # 发布会已经添加的人数
    event_limit = Event.objects.get(id = eid).limit                   # 发布会限制的人数
    if len(guest_limit)>=event_limit:
        return JsonResponse({'status':10024,'message':'event number is full'})

    # 判断当前时间是否大于发布会的开始时间
    now_time = time.time()                      # 当前时间的时间戳
    event_start_time = str(Event.objects.get(id=eid).start_time)             # 发布会的格式化时间
    event_struct_time = time.strptime(event_start_time,'%Y-%m-%d %H:%M:%S')             # 发布会的结构化时间
    event_time = time.mktime(event_struct_time)
    if now_time>event_time:
        return JsonResponse({'status':10025,'message':'event has started'})

    # 当前时间不大于发布会的开始时间则添加嘉宾
    try:
        Guest.objects.create(realname=realname,phone =int(phone),email = email,sign =0,event_id = int(eid))

    # 因为event_id 和phone是联合主键
    except IntegrityError:
        return JsonResponse({'status':10026,'message':'the event guest phone number repeat'})

    return JsonResponse({'status':200,'message':'add guest success'})



# 嘉宾查询接口
def search_guest(request):
    eid = request.GET.get('eid','')
    phone = request.GET.get('phone','')

    # 判断嘉宾关联的发布会id是否为空
    if eid== '':
        return JsonResponse({'status':10021,'message':'eid can not empty'})

    # 判断eid或者
    if eid != '' and phone =='':
        datas = []
        result = Guest.objects.filter(event_id=eid)
        if result:
            for i in result:
                guest={}
                guest['realname'] = i.realname
                guest['phone'] = i.phone
                guest['sign'] = i.sign
                guest['email'] = i.email
                datas.append(guest)
            return JsonResponse({'status':200,'message':'query success','data':datas})
        else:
            return JsonResponse({'status':10022,'message':'query is empty'})
    # 判断eid和phone是否都存在
    if eid !='' and phone !='':
        guest ={}
        try:
            result = Guest.objects.get(event_id=eid,phone=phone)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'query is empty'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['sign'] = result.sign
            guest['email'] = result.email
            return JsonResponse({'status':200,'message':'query success','data':guest})



# 发布会签到接口
def user_sign(request):
    eid =request.POST.get('eid','')
    phone = request.POST.get('phone','')

    # 判断发布会eid和phone两个参数是否为空
    if eid =='' or phone =='':
        return JsonResponse({'status':10021,'message':'parameter is error'})

    # # 判断发布会id是否为空
    # if eid == '':
    #     return JsonResponse({'status':10022,'message':'event is empty'})
    #
    # # 判断phone是否为空
    # if phone == '':
    #     return JsonResponse({'status':10023,'message':'phone is empty'})



    # 判断填写的eid是否在event存在
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'eid not in event'})

    # 判断eid的发布会是否已经发布
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023,'message':'event is not available'})

    # 判断发布会eid和phone都不会空，则更新签到状态
    if eid !='' and phone !='':
        now_time = time.time()
        event_start_time = str(Event.objects.get(id=eid).start_time)
        event_struct_time = time.strptime(event_start_time,'%Y-%m-%d %H:%M:%S')
        event_time = time.mktime(event_struct_time)

        # 判断发布会开始时间是否小于现在的时间
        if event_time < now_time:
            return JsonResponse({'status':10024,'message':'event has started'})

        # 判断手机号是否在Guest存在
        result = Guest.objects.filter(phone=phone)
        if not result:
            return JsonResponse({'status':10025,'message':'phone is not exist'})

        # 判断eid和手机号是否匹配
        result = Guest.objects.filter(event_id=eid,phone=phone)
        if not result:
            return JsonResponse({'status':10026,'message':'eid not match phone '})

        # 如果匹配则更新sign签到状态
        result = Guest.objects.get(event_id=eid,phone=phone).sign
        if result:
            return JsonResponse({'status':10027,'message':'user has sign in'})
        else:
            Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
            return JsonResponse({'status':200,'message':'sign success'})
