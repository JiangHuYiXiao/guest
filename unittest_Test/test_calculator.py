# -*- coding:utf-8 -*-
# @Author         : 江湖一笑
# @Time           : 2021/4/26 8:46
# @Software       : guest
# @Python_verison : 3.7
import unittest
from unittest_Test.module import Calculator

class Calculator_Test(unittest.TestCase):
    def setUp(self):
        self.cal = Calculator(8,4)

    def test_add(self):
        result = self.cal.add()
        self.assertEqual(result,12)

    def test_sub(self):
        result = self.cal.sub()
        self.assertEqual(result,4)

    def test_mul(self):
        result = self.cal.mul()
        self.assertEqual(result,32)

    def test_div(self):
        result = self.cal.div()
        self.assertEqual(result,2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Calculator_Test('test_add'))
    suite.addTest(Calculator_Test('test_sub'))
    suite.addTest(Calculator_Test('test_mul'))
    suite.addTest(Calculator_Test('test_div'))

    unittest.TextTestRunner().run(suite)
