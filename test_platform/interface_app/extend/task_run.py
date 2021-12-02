# coding:utf-8
import json
import unittest
import requests
import xmlrunner
from ddt import ddt, data, file_data, unpack
from os.path import dirname, abspath
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
TASK_DIR = BASE_DIR + '/resourse/tasks/'
print(TASK_DIR)

@ddt
class MyTest(unittest.TestCase):

    @unpack
    # @data({'url': 'http://httpbin.org/post', 'method': 'post', 'parameter': '{}'},
    #       {'url': 'http://www.baidu.com', 'method': 'get', 'parameter': '{}'},
    #       {'url': 'http://httpbin.org/post', 'method': 'post', 'parameter': '{"name":"tom","age":"22"}'}
    #       )
    @file_data(TASK_DIR + 'cases_data.json')
    def test_run_case(self, url, method, ptype, header, parameter, assert_):
        try:
            header = json.loads(header.replace("'", "\""))
            parameter = json.loads(parameter.replace("'", "\""))
        except json.JSONDecodeError:
            return '请求头或者参数输入错误'

        if method == 'get':
            req = requests.get(url, headers=header, data=parameter)
            self.assertIn(assert_, req.text)
        if method == 'post':
            req = requests.post(url, headers=header, data=parameter)
            self.assertIn(assert_, req.text)


if __name__ == '__main__':
    with open(TASK_DIR + 'results.xml', 'wb')as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False
        )