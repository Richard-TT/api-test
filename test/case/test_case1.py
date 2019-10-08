# -*- coding:utf8 -*-
# Time    : 2019/9/22 22:37
# Author  : Richard
# Email   : tangtao556@qq.com
# File    : test_case1.py
import os

from test.utils.loginUser import LoginUser


class TestResource:
    def test_run(self):
        user = LoginUser()
        print(os.path.abspath(__file__))
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), './../config/user.ini')
        r = user.login(file)

        def check_response(response):
            print("预期的结果描述")
            pass


        ejson = {'status':200,'data':{"data":[{"id":1,"name":"aa","code":"bjlh"},{"id":2,"name":"bb","code":"cqlh"}],"code":10000,"msg":"成功"}}
        data = {"data":{"cityId":"","projectName":"","projectType":""},"pageInfo":{"pageNum":1,"pageSize":10}}
        cases = [
            [{'p': '/rms-sys-conf/web/city/all', 'm': 'GET', 'h': '', 'd': '', 'r': ejson, 's': '', 'c': ''}],
            [
                {'p': '/rms-sys-conf/web/project/query', 'm': 'POST', 'h': '', 'd': data, 'r': '', 's': '', 'c': ''},
                [
                    {'p': '/rms-sys-conf/web/project/allProject', 'm': 'GET', 'h': '', 'd': '', 'r': '', 's': '',
                     'c': ''}
                ]
            ]
        ]

        user.run(cases)
