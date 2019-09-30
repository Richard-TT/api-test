# -*- coding:utf8 -*-
# Time    : 2019/9/18 17:17
# Author  : Richard
# Email   : tangtao556@qq.com
# File    : loginUser.py
import json
import re
import urllib3
import codecs
import configparser


class LoginUser:
    def __init__(self):
        self.username = None
        self.passwd = None
        self.token = None
        self.header = {}
        self.body = None
        self.url = None
        self.content_type = httpDefine.CONTENT_TYPE_JSON
        self.method = httpDefine.HTTP_GET
        self.http = None

    def get_http(self, force=False):
        if force or (self.http is None):
            self.http = HttpClient({'POOL_CONF': {'timeout': urllib3.Timeout(connect=2.0, read=5.0)}})  # {'PROXY':{
        # 'type':'value'}, # 'CERT':{}, 'POOL_CONF':{}}
        return self.http

    def login(self, file):
        if not os.path.isfile(file):
            log.error(u"用户配置文件查找失败:%s" % file)
            return False
        cp = configparser.ConfigParser()
        with codecs.open(file, 'r', encoding='utf-8') as f:
            cp.read_file(f)
        self.username = cp.get('User', 'name')
        self.passwd = cp.get('User', 'passwd')
        self.url = cp.get('User', 'login_url')
        if not Util.checkEmpty([self.username, self.passwd, self.url]):
            log.error(u'登录用户信息格式错误')
            return False
        self.method = httpDefine.HTTP_POST
        fields = {'username': self.username, 'password': self.passwd}
        r = self.get_http().request({'method': self.method, 'url': self.url, 'fields': fields})
        pattern = re.compile(r'sso_sessionid=(.*?);')
        cookie = r.get(httpDefine.HTTP_RESPONSE_HEADERS)['Set-Cookie']
        match = pattern.match(cookie)
        if match:
            self.header['c2-sso-sessionid'] = match.group()[len('sso_sessionid='):-1]
        return r

    def json_request(self, method, url, body=None, headers=None):
        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        headers = dict(self.header, **headers)
        request_data = {httpDefine.HTTP_METHOD: method, httpDefine.HTTP_URL: url, httpDefine.HTTP_HEADERS: headers}
        if not isinstance(body, bytes):
            try:
                body = json.dumps(body).encode('utf-8')
            except ValueError as e:
                pass
        if body:
            request_data['body'] = body
        return self.get_http().request(request_data)

    def xml_request(self, method, url, body=None, headers=None):
        headers = headers or {}
        request_data = {httpDefine.HTTP_METHOD: method, httpDefine.HTTP_URL: url, httpDefine.HTTP_HEADERS: headers}
        if body:
            request_data['body'] = body
        return self.get_http().request(request_data)

    def base_request(self, method, url, body=None, headers=None):
        headers = headers or {}
        request_data = {httpDefine.HTTP_METHOD: method, httpDefine.HTTP_URL: url, httpDefine.HTTP_HEADERS: headers}
        if body and isinstance(body, bytes):
            request_data['body'] = body
        elif body:
            request_data['fields'] = body
        return self.get_http().request(request_data)

    def request(self, method, url, body=None, headers=None):
        headers = headers or {}
        headers['Content-Type'] = headers.get('Content-Type') or 'application/json'
        if headers.get('Content-Type') == 'application/json':
            return self.json_request(method, url, body, headers)
        elif headers.get('Content-Type') == 'application/xml':
            return self.xml_request(method, url, body, headers)
        else:
            return self.base_request(method, url, body, headers)

    @staticmethod
    def get_full_url(url, file=os.path.join(os.path.dirname(os.path.abspath(__file__)), './../config/env.ini')):
        cp = configparser.ConfigParser()
        prefix = ''
        try:
            with codecs.open(file, 'r', encoding='utf-8') as f:
                cp.read_file(f)
                active = cp.get('Active', 'active')
                prefix = cp.get(active, 'prefix_url')
        except KeyError as e:
            pass
        url = prefix + url
        return url

    def run(self, cases):
        # [{path:xxx, mtd:xxx, req_h:xxx, req_d:xxx, exp_r:xxx, exp_s:xxx, exp_c:xxx}...],{p:xxx, m:xxx, h:xxx, d:xxx,
        # r:xxx, s:xxx, c:xxx}
        for item in cases:
            if isinstance(item, list):  # case数组（可能多级）
                self.run(item)
            elif isinstance(item, dict):  # case
                api = Api(**item)
                r = self.json_request(api.method, self.get_full_url(api.path), api.data, api.headers)
                Api.compare_response(r, api.status, api.expect_response, api.code)
                # print(r['status'], r['data'].decode('utf8'))
