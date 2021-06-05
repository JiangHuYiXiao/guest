# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/5/31 9:49
# @Software       : guest
# @Python_verison : 3.7

import sys,os
from pyrequest.db_fixture.mysql_db import DB
# 创建测试数据
datas ={
    'sign_event':[
        {'id':101,'name':'红米Pro发布会','guest_limit':1000,'status':1,'address':'北京会展中心','start_time':'2021-08-08 08:00:00','create_time':'2019-01-01 08:00:00'},
        {'id':102,'name':'可参加人数为0','guest_limit':0,'status':1,'address':'北京会展中心','start_time':'2021-08-08 08:00:00','create_time':'2019-01-01 08:00:00'},
        {'id':103,'name':'当前状态为0关闭','guest_limit':1000,'status':0,'address':'北京会展中心','start_time':'2021-08-08 08:00:00','create_time':'2019-01-01 08:00:00'},
        {'id':104,'name':'发布会已经结束','guest_limit':1000,'status':0,'address':'北京会展中心','start_time':'2020-08-08 08:00:00','create_time':'2019-01-01 08:00:00'},
        {'id':105,'name':'小米8发布会','guest_limit':1000,'status':1,'address':'北京会展中心','start_time':'2021-11-08 08:00:00','create_time':'2019-01-01 08:00:00'},
    ],
    'sign_guest':[
        {'id':101,'realname':'alen','phone':'13511001100','sign':0,'email':'alen@mail.com','create_time':'2021-01-01 00:00:00','event_id':101},
        {'id':102,'realname':'has sign','phone':'13511001101','sign':1,'email':'sign@mail.com','create_time':'2021-01-01 00:00:00','event_id':101},
        {'id':103,'realname':'tom','phone':'13511001102','sign':0,'email':'tom@mail.com','create_time':'2021-01-01 00:00:00','event_id':105},
    ]
}

# 将测试数据插入表
def init_data():
    db = DB()
    for table,data in datas.items():
        db.clear(table)
        for d in data:
            # print(d)
            db.insert(table,d)
    db.close()

if __name__ == '__main__':
    init_data()
