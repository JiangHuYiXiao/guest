from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from sign.models import Event,Guest
# Create your views here.

# 1、不使用html文件时候的访问方式
# def index(request):
#     return HttpResponse('Hello Django!')


# 2、使用html的文件的访问方式



def index(request):
    return render(request,"index.html")

# 登录

def login_action(request):
    if request.method == 'POST':
        login_username = request.POST.get('username','')   # 对应form表单中的input标签的name属性
        login_password = request.POST.get('password','')

        if login_username =='' or login_password=='':
            return render(request, "index.html", {"error": "username or password null"})
        else:
            user = auth.authenticate(username=login_username, password=login_password)
            if user is not None:
                auth.login(request,user)                # 登录
                # return HttpResponse('login success!')
                # response.set_cookie('user',username,3600)     # 添加浏览器cookie  第一个参数表示cookie名，第二个参数表示输入的用户名即是admin，第三个参数表示cookie在浏览器保持的时间秒。
                response = HttpResponseRedirect('/event_manage/')       # 重定向
                request.session['user'] = login_username              # 将session信息记录到浏览器
                return response
            else:
                return render(request,'index.html',{'error':'username or password error!'})
    else:
        return render(request,'index.html')


# 登录成功后重定向到发布会管理页面
@login_required              # 加上装饰器，login_required表示需要先登录才能访问这个视图函数
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user','')               # 读取浏览器session
    # username = request.COOKIES.get('user','')                    # 读取浏览器cookie
    return render(request,'event_manage.html',{'user':username,'events':event_list})

# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get("name","")
    print(search_name)
    event_list = Event.objects.filter(name__contains=search_name)
    # print(event_list)
    print(event_list)
    return render(request,'event_manage.html',{'user':username,'events':event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,4)
    page = request.GET.get('page')              # 获取当前要显示的第几页数据
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request,'guest_manage.html',{'user':username,'guests':contacts})


# 嘉宾名称搜索
@login_required
def search_realname(request):
    username = request.session.get('user','')
    search_realname = request.GET.get('realname','')
    print(search_realname)
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    print(guest_list)
    return render(request,'guest_manage.html',{'user':username,'guests':guest_list})


# 签到界面
@login_required
def sign_index(request,event_id):
    click_event = get_object_or_404(Event,id=event_id)           # 查询Event ，条件是id为event_id，eid通过urls.py中的正则表达式获取
    return render(request,'sign_index.html',{'event':click_event})


# 发布会签到
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    guest_list=Guest.objects.filter(event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = 0
    sign_data += 1
    for guest in guest_list:
        if guest.sign == True:
            sign_data +=1
    phone = request.POST.get('phone','')
    print(phone)

    # 判断手机号是否在Guest表存在
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error'})

    # 判断手机号和发布会是否匹配
    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone or event_id error', 'guest': guest_data, 'sign': sign_data})

    #
    result = Guest.objects.get(phone =phone,event_id=event_id)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in', 'guest': guest_data, 'sign': sign_data})

    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success', 'user':result,'guest': guest_data, 'sign': str(int(sign_data)+1)})


# 退出登录
@login_required
def logout(request):
    auth.logout(request)            # logout自动删除缓存
    response = HttpResponseRedirect('/index/')   # 重定向
    return response

# 数据迁移命令migrate 和makemigrations区别
# python manage.py makemigrations这个命令是记录我们对models.py的所有改动，并且将这个改动迁移到migrations这个文件下生成一个文
# 件例如：0001文件，如果你接下来还要进行改动的话可能生成就是另外一个文件不一定都是0001文件，但是这个命令并没有作用到数据库，
# 这个刚刚我们在上面的操作过程之后已经看到了，
# ————————————————
# 而当我们执行python manage.py migrate 命令时
# 这条命令的主要作用就是把这些改动作用到数据库也就是执行migrations里面新改动的迁移文件更新数据库，比如创建数据表，或者增加字段属性
