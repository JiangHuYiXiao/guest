# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/4/25 11:00
# @Software       : guest
# @Python_verison : 3.7
class Calculator():
    '''实现两个数的加、减、乘、除'''
    def __init__(self,a,b):
        self.a = int(a)
        self.b = int(b)

    # 加法
    def add(self):
        return(self.a + self.b)

    # 减法
    def sub(self):
        return(self.a - self.b)

    # 乘法
    def mul(self):
        return(self.a*self.b)

    # 除法
    def div(self):
        return(self.a/self.b)
