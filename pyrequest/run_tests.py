# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/5/25 9:22
# @Software       : guest
# @Python_verison : 3.7

# 执行所有的接口测试用例的主程序

import unittest,os,time
from HTMLTestRunner import HTMLTestRunner
from pyrequest.db_fixture import test_data


test_dir = './interface'
print(test_dir)
discover = unittest.defaultTestLoader.discover(test_dir,pattern='*_test.py')

if __name__ == '__main__':
    # 初始化接口数据
    test_data.init_data()

    now_time = time.strftime('%Y-%m-%d %H_%M_%S')

    # 生成到指定目录
    file_name = './report/' + now_time + '_result.html'
    # 生成到当前目录
    # file_name = './' + now_time + 'result_html'

    with open(file=file_name,mode='wb') as file:
        runner = HTMLTestRunner(stream=file,title='测试报告',description='用例执行情况：')
        runner.run(discover)