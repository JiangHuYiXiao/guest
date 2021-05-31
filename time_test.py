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
import pymysql
# # 创建连接
class DB:
    def __init__(self,table_name,table_data):
        self.table_name =table_name
        self.table_data = table_data
        conn = pymysql.connect(host='localhost',user='root',password='123',database='guest')
        self.cursor = conn.cursor()
    def insert_sql(self):
        for value in table_data:
            table_data[value] ="'"+str(table_data[value])+"'"
            print(table_data[value])
        key = ','.join(self.table_data.keys())
        value =','.join(self.table_data.values())
        print(key)
        print(value)
        insert_sql = 'insert into '+ self.table_name +'('+key+') values('+value+')'
        print(insert_sql)
        # 执行sql
        self.cursor.execute(insert_sql)
table_name = 'sign_event'
table_data = {'id':46,'name':'hongmi','guest_limit':2000,'status':1,'address':'shanghai','start_time':'2021-08-08 08:00:00','create_time':'2021-01-01 08:00:00'}
db = DB(table_name,table_data)
db.insert_sql()


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