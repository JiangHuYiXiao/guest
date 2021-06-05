# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/6/1 19:33
# @Software       : guest
# @Python_verison : 3.7
import unittest
import requests
from pyrequest.db_fixture import test_data

class Add_Event_Test(unittest.TestCase):
    '''发布会添加接口'''
    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/add_event/'

    def tearDown(self):
        print(self.result,':用例执行完成')
        # print(self.result)

    # @unittest.skip('无条件的跳过这条用例')
    def test_add_event_all_null(self):
        '''有参数为空'''
        # eid == '' or name == '' or guest_limit == '' or status == '' or address == '' or start_time == ''
        r = requests.post(self.url,
                          data={'eid': '', 'name': '鸿蒙OS发布会1', 'guest_limit': 20000, 'address': '深圳华为基地', 'status': 0,
                                 'start_time': '2021-11-11 20:00:00', 'create_time': '2021-01-01 20:00:00'})
        self.result = r.json()
        self.assertEqual(self.result['status'],10021)
        self.assertEqual(self.result['message'],'parameter error')

    # @unittest.skip('无条件的跳过这条用例')
    def test_add_event_eid_exists(self):
        '''eid已经在sign_event表存在'''
        r = requests.post(self.url,data={'eid': 101, 'name': '鸿蒙OS发布会2', 'guest_limit': 20000, 'address': '深圳华为基地2', 'status': 0,
                                 'start_time': '2021-11-11 20:00:00', 'create_time': '2021-01-01 20:00:00'})
        self.result =r.json()
        self.assertEqual(self.result['status'],10022)
        self.assertEqual(self.result['message'],'event id already exists')

    # @unittest.skip('无条件的跳过这条用例')
    def test_add_event_name_exists(self):
        '''name已经存在'''
        r = requests.post(self.url,data={'eid': 106, 'name': '红米Pro发布会', 'guest_limit': 20000, 'address': '北京小米基地1', 'status': 0,
                                 'start_time': '2021-11-11 20:00:00', 'create_time': '2021-01-01 20:00:00'})
        self.result = r.json()
        self.assertEqual(self.result['status'],10023)
        self.assertEqual(self.result['message'],'event name already exists')

    # @unittest.skip('无条件的跳过这条用例')
    def test_add_event_time_error(self):
        '''时间格式不对'''
        r = requests.post(self.url,data={'eid': 107, 'name': '云之家发布会', 'guest_limit': 20000, 'address': '金蝶软家园', 'status': 0,
                                 'start_time': '2021:11:11 20:00:00', 'create_time': '2021-01-01 20:00:00'})
        self.result = r.json()
        self.assertEqual(self.result['status'],10024)
        self.assertEqual(self.result['message'],'error')

    # @unittest.skip('无条件的跳过这条用例')
    def test_add_event_success(self):
        '''发布会添加成功'''
        r = requests.post(self.url,data={'eid': 108, 'name': '红米Note发布会', 'guest_limit': 20000, 'address': '北京小米基地1', 'status': 0,
                                 'start_time': '2021-11-11 20:00:00', 'create_time': '2021-01-01 20:00:00'})
        self.result = r.json()
        self.assertEqual(self.result['status'],200)
        self.assertEqual(self.result['message'],'add event success')

if __name__ == '__main__':
    test_data.init_data()
    unittest.main()