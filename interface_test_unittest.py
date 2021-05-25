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

    def test_get_event_empty(self):
        '''eid不存在'''
        r = requests.get(self.url,params={'eid':2000})
        result = r.json()
        self.assertEqual(result['status'],10022)
        self.assertEqual(result['message'],'query result is empty')

    def test_get_event_success(self):
        '''查询成功'''
        r = requests.get(self.url,params={'eid':1})
        result = r.json()
        self.assertEqual(result['status'],200)
        self.assertEqual(result['message'],'query success')
        self.assertEqual(result['data']['name'],'小米发布会1')
        self.assertEqual(result['data']['address'],'北京')
        self.assertEqual(result['data']['start_time'],'2021-04-09T08:00:00')


if __name__ == '__main__':
    unittest.main()