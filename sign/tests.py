from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User
# Create your tests here.
# django.test.TestCase也是继承的unnitest.TestCaseD的，在test.py文件中编写针对模型（Event，Guest）的测试用例


# 一个简单的例子
class Modeltest(TestCase):
    '''测试数据的插入和查询，使用python manage.py 不会真正往数据库插入数据，只是一个测试'''
    def setUp(self):
        Event.objects.create(id=1,name='詹姆斯退役发布会',limit=2000,status=True,address='洛杉矶',start_time='2025-10-05 10:00:00')
        Guest.objects.create(id=1,event_id=1,realname='kebo',sign=False,phone='182707176666',email='182707176666@163.com')

    def test_event_models(self):
        result = Event.objects.get(name='詹姆斯退役发布会')
        self.assertEqual(result.address,'洛杉矶')
        self.assertTrue(result.status)
    def test_guest_models(self):
        result = Guest.objects.get(realname='kebo')
        self.assertEqual(result.phone,'182707176666')
        self.assertFalse(result.sign)




# 执行django专门提供了test命令来运行测试
# python manage.py test    默认执行项目下所有以test开头的方法
# python manage.py test sign  运行sign下的所有测试用例
# python manage.py test sign.tests  运行sign下的tests.py下的所有测试用例
# python manage.py test sign.tests.Modeltest  运行sign.tests.Modeltes下的所有测试用例
# python manage.py test sign.tests.Modeltest.test_event_models  运行sign.tests.Modeltes.test_event_models的测试用例
# python manage.py test -p test*.py 运行以test开头的py结尾的测试文件


# 客户端测试
# python manage.py shell 进入shell模式
# setup_test_environment()  测试环境初始化
# 在django中，django.test.Client类充当一个虚拟的网络浏览器，可以测试视图view与django的应用程序以编程方式交互。这里使用self.client
# 1、测试首页
class IndexPageTest(TestCase):
    '''测试登录首页index'''
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')




# 2、测试登录动作
class LoginActionTest(TestCase):
    '''测试登录动作'''
    def setUp(self):
        User.objects.create_user('admin','admin@email.com','admin123456')

    def test_add_admin(self):
        '''测试添加用户'''
        user = User.objects.get(username='admin')
        self.assertEqual(user.username,'admin')
        self.assertEqual(user.email,'admin@email.com')


    def test_login_action_username_password_null(self):
        '''测试用户名和密码为空'''
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password null',response.content)


    def test_login_action_username_password_error(self):
        '''测试用户和密码错误'''
        test_data = {'username':'abc','password':'123'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error',response.content)

    def test_login_action_success(self):
        '''测试用户和密码正确'''
        test_data = {'username':'admin','password':'admin123456'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,302)


class EventManageTest(TestCase):
    '''发布会管理'''
    def setUp(self):
        User.objects.create_user('LBJ','LBJ@email.com','LBJ123456')
        Event.objects.create(name='xiaomi5',limit=2000,address='beijing',status=True,start_time='2017-08-10 12:30:00')
        self.login_user = {'username':'LBJ','password':'LBJ123456'}

    def test_event_manage_success(self):
        '''测试发布会：xiaomi5'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'xiaomi5',response.content)
        self.assertIn(b'beijing',response.content)

    def test_event_search(self):
        '''测试发布会搜索'''
        response = self.client.post('login_action/',data=self.login_user)
        response = self.client.post('/search_name/',{'name':'xiaomi5'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'xiaomi5',response.content)
        self.assertIn(b'beijing',response.content)
