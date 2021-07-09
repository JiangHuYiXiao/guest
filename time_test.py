# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/5/12 8:34
# @Software       : guest
# @Python_verison : 3.7
# a = {'a':'111','b':'222'}
# # for key in a:
# #     a[key] = ','+str(a[key])+','
#     # print(a[key])
# result1 =','.join(a.keys())
# result2 =','.join(a.values())
# print(result2)

# name = input('请输入用户名：')
# pwd = input('请输入密码：')
# import pymysql
# # # 创建连接
# class DB:
#     def __init__(self,table_name,table_data):
#         self.table_name =table_name
#         self.table_data = table_data
#         conn = pymysql.connect(host='localhost',user='root',password='123',database='guest')
#         self.cursor = conn.cursor()
#     def insert_sql(self):
#         for value in table_data:
#             table_data[value] ="'"+str(table_data[value])+"'"
#             print(table_data[value])
#         key = ','.join(self.table_data.keys())
#         value =','.join(self.table_data.values())
#         print(key)
#         print(value)
#         insert_sql = 'insert into '+ self.table_name +'('+key+') values('+value+')'
#         print(insert_sql)
#         # 执行sql
#         self.cursor.execute(insert_sql)
# table_name = 'sign_event'
# table_data = {'id':46,'name':'hongmi','guest_limit':2000,'status':1,'address':'shanghai','start_time':'2021-08-08 08:00:00','create_time':'2021-01-01 08:00:00'}
# db = DB(table_name,table_data)
# db.insert_sql()


# 4、变量增加
# user_name='long'
# password=123
# import pymysql
# conn = pymysql.connect(host='127.0.0.1',user='root',password='',database='db1')
# cursor = conn.cursor()
# sql = "insert into t_user_info(password,user_name) values(%s,%s);"
# cursor.execute(sql,[password,user_name])
# conn.commit()           # 提交
# conn.close()
# cursor.close()

# test_dict = {'a':'123','b':'456'}
#
# print(','.join(test_dict.keys()))
# print(','.join(test_dict.values()))
#
#
# tuple = (11,'jianghu',12,'abc')
# s1 = 's'.join('%s' %id for id in tuple)
# print(s1)

# import hashlib
# import hashlib
# h = hashlib.md5()
# h.update(b'@admin123')         # 必须是字节类型的
# user = h.hexdigest()         # 转化为16进制的结果
# print(user)
#
#
import hashlib
# h = hashlib.md5(bytes('12',encoding='utf-8'))
# h.update(b'jianghu')            # 1e96f616dbeda20c6d50f69af939435b
# user = h.hexdigest()
# print(user)         # 6b6429a834dbb43e0c80175f52d31e94
# import time
# now_time = time.time()
# print(now_time,type(now_time))
# str_now_time = str(now_time)
# print(str_now_time,type(str_now_time))
# sever_time = str_now_time.split('.')[0]
# print(sever_time)


h = hashlib.md5(bytes('&guest-Bugmaster', encoding='utf-8'))  # 加盐处理
h.update()
sever_sign = h.hexdigest()