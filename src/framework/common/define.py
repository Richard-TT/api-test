# -*- coding:utf8 -*-
# Time    : 2019/9/17 17:37
# Author  : Richard
# Email   : tangtao556@qq.com
# File    : define.py


class httpDefine(object):
    def __init__(self):
        self.HTTP_POST = 'POST'
        self.HTTP_GET = 'GET'
        self.HTTP_CERT = 'CERT'
        self.HTTP_PROXY = 'PROXY'
        self.HTTP_POOL_CONF = 'POOL_CONF'
        self.HTTP_REQUEST_CONF = 'REQUEST_CONF'
        self.HTTP_PROXY_HTTP = 'PROXY_HTTP'
        self.HTTP_PROXY_SOCKS = 'PROXY_SOCKS'
        self.HTTP_SSL_CA = 'ca_certs'
        self.CONTENT_TYPE_JSON = 'application/json'
        self.CONTENT_TYPE_STREAM = 'application/octet-stream'
        self.HTTP_METHOD = 'method'
        self.HTTP_URL = 'url'
        self.HTTP_FIELDS = 'fields'
        self.HTTP_HEADERS = 'headers'
        self.HTTP_RESPONSE_STATUS = 'status'
        self.HTTP_RESPONSE_DATA = 'data'
        self.HTTP_RESPONSE_HEADERS = 'headers'
        self.HTTP_CODING = 'utf-8'


httpDefine = httpDefine()
