# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/5/21 17:07
# @Software       : guest
# @Python_verison : 3.7
import requests

# 发布会查询接口
url = 'http://127.0.0.1:8000/api/search_event/'
r = requests.get(url,params={'eid':101})
print(r)
result = r.json()
print(result)
# 断言接口返回值
assert result['status'] == 200
assert result['message'] == 'query success'
assert result['data']['name'] == '红米Pro发布会'
assert result['data']['address'] =='北京会展中心'
