# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/5/26 8:25
# @Software       : guest
# @Python_verison : 3.7
import os
import configparser                    # 是用来读取配置文件的包
from pymysql import connect, cursors
from pymysql.err import OperationalError
#  ============ 读取db_config.ini文件设置 ============


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = base_dir + '\db_config.ini'
print(file_path)

# parent_dir1 = os.path.dirname((os.path.abspath(__file__)))  当前文件的父目录
# parent_dir2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    当前文件的父目录的父目录
# os.path.abspath(__file__)  获取当前脚本的完整路径


config = configparser.ConfigParser()
config.read(file_path,encoding='utf-8')
host = config.get("mysqlconf","host")
port = config.get("mysqlconf","port")
user = config.get("mysqlconf","user")
password = config.get("mysqlconf","password")
db_name = config.get("mysqlconf","db_name")


#  ============ 封装mysql基本操作 ============

class DB:
    # 链接数据库
    def __init__(self):
        try:
            self.conn = connect(
                host = host,
                user = user,
                password = password,
                db =db_name,
                charset = 'utf8mb4',            # MySQL在5.5.3版本之后增加了这个utf8mb4的编码，mb4就是most bytes 4的意思，专门用来兼容四字节的unicode。
                cursorclass= cursors.DictCursor
                
            )
        except OperationalError as e:
            print('Mysql Error %d:%s'%(e.args[0],e.args[1]))
            # python报OperationalError: (1366, "Incorrect string value..."

    # 清除表数据
    def clear(self,table_name):
        clear_sql = 'delete from '+table_name+';'
        with self.conn.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')   #  来禁用外键约束.
            cursor.execute(clear_sql)
        self.conn.commit()

    # 插入表数据
    def insert(self,table_name,table_data):
        for value in table_data:
            table_data[value] ="'"+str(table_data[value])+"'"
            print(table_data[value])
        key = ','.join(table_data.keys())
        print(key)
        value = ','.join(table_data.values())
        print(value,type(value))
        '=================='
        insert_sql = 'insert into '+ table_name +'('+key+') values('+value+')'
        # 编写sql
        # insert_sql = "insert into t_user_info where user_name=%s and password=%s"
        print(insert_sql)
        # 执行sql
        # cursor.execute(SQL, [name, pwd])
        print(insert_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(insert_sql)
        self.conn.commit()

    # 关闭数据库连接
    def close(self):
        self.conn.close()


if __name__ =='__main__':
    db = DB()
    table_name = 'sign_guest'
    # 因为limit为sql关键字所以将表字段修改为guest_limit
    table_data = {'id':10,'realname':'alen','phone':'13511001100','sign':0,'email':'alen@mail.com','create_time':'2021-01-01 00:00:00','event_id':101}
    db.clear(table_name)
    db.insert(table_name,table_data)
    db.close()
