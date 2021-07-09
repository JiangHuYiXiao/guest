# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/5/6 9:37
# @Software       : guest
# @Python_verison : 3.7
from django.urls import path
from api import views,views_if_sec
urlpatterns =[
    # sign system interface
    # ex:/add_event/
    path('add_event/',views.add_event,name='add_event'),
    # ex:/search_event/
    path('search_event/',views.search_event,name='search_event'),
    # ex:/add_guest/
    path('add_guest/',views.add_guest,name='add_guest'),
    # ex:/search_guest/
    path('search_guest/',views.search_guest,name='search_guest'),
    # ex:/user_sign/ 发布会签到
    path('user_sign/',views.user_sign,name='user_sign'),
    # 发布会查询接口增加，基本认证auth
    path('search_event_auth/',views_if_sec.search_event_auth,name='search_event_auth'),
]