# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/6/10 18:18
# @Software       : guest
# @Python_verison : 3.7

# 用户认证接口测试用例
import unittest
import requests

# 查询发布会接口 ---用户认证
class GetEventList(unittest.TestCase):
    def setUp(self):
        self.base_url = '127.0.0.1:8000/api/search_event_auth/'

    def tearDown(self):
        print('一条用例执行完成')

    # auth 为空
    def test_get_event_list_auth_null(self):
        r = requests.get(self.base_url,params=({'eid':101}))
        result = r.json()
        self.assertEqual(result['status'],10011)
        self.assertEqual(result['message'],'user auth null')

    # auth 为fail
    def test_get_event_list_auth_fail(self):
        auth_user = ('abc','123')
        r = requests.get(self.base_url,auth = auth_user,params={'eid':101})
        result =r.json()
        self.assertEqual(result['status'],10012)
        self.assertEqual(result['message'],'user auth fail')


    # eid and name 为空
    def test_get_event_list_auth_eid_name_null(self):
        auth_user = ('admin','admin123456')
        r = requests.get(self.base_url,auth = auth_user,params={'eid':''})
        result = r.json()
        self.assertEqual(result['status'],10021)
        self.assertEqual(result['message'],'parameter error')

    # eid不存在
    def test_get_event_list_eid_empty(self):
        auth_user = ('admin','admin123456')
        r = requests.get(self.base_url,auth = auth_user,params={'eid':2})
        result = r.json()
        self.assertEqual(result['status'],10022)
        self.assertEqual(result['message'],'query result is empty')

    # 查询成功
    def test_get_event_list_success(self):
        auth_user = ('admin','admin123456')
        r = requests.get(self.base_url,auth = auth_user,params={'eid':101})
        result = r.json()
        self.assertEqual(result['status'],200)
        self.assertEqual(result['message'],'query success')
