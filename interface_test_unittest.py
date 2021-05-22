# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/5/22 10:35
# @Software       : guest
# @Python_verison : 3.7
import requests
import unittest


# 结合unittest
# 发布会查询接口测试
class Test_search_event(unittest.TestCase):
    '''发布会查询接口'''
    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/search_event/'
    def tearDown(self):
        pass
    def test_get_event_error(self):
        '''eid和name为空'''
        r = requests.get(self.url,params={'eid':'','name':''})
        result = r.json()
        self.assertEqual(result['status'],10021)
        self.assertEqual(result['message'],'parameter error')

if __name__ == '__main__':
    unittest.main()