# -*- coding:utf8 -*-
# Time    : 2019/9/22 22:12
# Author  : Richard
# Email   : tangtao556@qq.com
# File    : api.py
import json
from inspect import isfunction
from json import JSONDecodeError


class Api:
    def __init__(self, **args):  # {p:xxx, m:xxx, h:xxx, d:xxx, r:xxx, s:xxx}
        self.__path = args.get('p')  # 接口地址
        self.__method = args.get('m')  # http请求方法
        self.__headers = args.get('h')  # 请求的header信息
        self.__data = args.get('d')  # 请求的数据
        self.__expect_response = args.get('r')  # 期待的响应数据
        self.__status = args.get('s') or 200  # http状态码
        self.__code = args.get('c')  # 接口状态码status

    @property
    def path(self):
        return self.__path

    @property
    def method(self):
        return self.__method

    @property
    def headers(self):
        return self.__headers

    @property
    def data(self):
        return self.__data

    @property
    def expect_response(self):
        return self.__expect_response

    @property
    def status(self):
        return self.__status

    @property
    def code(self):
        return self.__code

    @staticmethod
    def compare_response(response, status, expect, expect_code):
        log.debug("================%s===============" % u"结果检查")
        for k, v in {'response': HttpClient.remove_response_header(response), 'status': status,
                     'expect_code': expect_code, 'expect': expect}.items():
            log.debug([k, v])
        assert int(status) == int(response['status'])  # 判断http状态码
        if len(expect_code) > 0:
            assert int(expect_code) == int(response['data']['code'])  # 判断接口状态码
        if isfunction(expect):
            assert expect(response)
        else:
            try:
                response['data'] = json.loads(response['data'])
                expect = dict(expect)
                result = Util.find_obj(response, expect)
                log.debug("****************** %s *****************" % result)
                assert result
            except JSONDecodeError or TypeError as e:
                return response == expect
