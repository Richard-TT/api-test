# -*- coding:utf8 -*-
# Time    : 2019/9/17 10:52
# Author  : Richard
# Email   : tangtao556@qq.com
# File    : httpClient.py
import traceback
import urllib3
from src.framework.common.innerImport import *


def getDictConf(conf, key):
    if conf.__contains__(key) and type(conf.get(key)) == dict:
        return conf[key]
    else:
        return dict()


class HttpClient(object):

    def __init__(self, conf=None):
        if conf is not None:
            poolConf = dict(conf).copy()
            proxyConf = dict(getDictConf(poolConf, httpDefine.HTTP_PROXY))
            certConf = dict(getDictConf(poolConf, httpDefine.HTTP_CERT))
            httpConf = dict(getDictConf(poolConf, httpDefine.HTTP_POOL_CONF))
            self.requestConf = dict(getDictConf(poolConf, httpDefine.HTTP_REQUEST_CONF))
            self.pool = None
            try:
                allConf = dict(certConf, **httpConf)
                self.pool = self.__createPool(proxyConf.get('type'), proxyConf.get('value'), allConf)
            except Exception as e:
                log.info(e)
                traceback.print_exc()
        else:
            self.pool = urllib3.PoolManager()

    def __createPool(self, proxyType, proxyValue, conf):
        if len(conf) > 0 and conf.get(httpDefine.HTTP_SSL_CA) is not None:
            pass
        else:
            urllib3.disable_warnings()
        if proxyType == httpDefine.HTTP_PROXY_HTTP and len(proxyValue) > 0:
            if len(conf) > 0:
                return urllib3.ProxyManager(proxyValue, conf)
            else:
                return urllib3.ProxyManager(proxyValue)
        elif proxyType == httpDefine.HTTP_PROXY_SOCKS and len(proxyValue) > 0:
            if len(conf) > 0:
                return urllib3.SOCKSProxyManager(proxyValue, conf)
            else:
                return urllib3.ProxyManager(proxyValue)
        else:
            if len(conf) > 0:
                return urllib3.PoolManager(**conf)
            else:
                return urllib3.PoolManager()

    def request(self, reqParameter=None, conf=None):
        reqParameter = reqParameter or {}
        conf = conf or {}
        if len(reqParameter) == 0 and not reqParameter[httpDefine.HTTP_METHOD] and not \
                reqParameter[httpDefine.HTTP_URL]:
            return False
        try:
            self.requestConf = dict(self.requestConf, **conf)
            method = reqParameter.pop(httpDefine.HTTP_METHOD, None)
            url = reqParameter.pop(httpDefine.HTTP_URL, None)
            fields = reqParameter.pop(httpDefine.HTTP_FIELDS, None)
            headers = reqParameter.pop(httpDefine.HTTP_HEADERS, None) or {}
            reqParameter = dict(self.requestConf, **reqParameter)
            r = self.pool.request(method, url, fields=fields, headers=headers, **reqParameter)
            return self.response(r)
        except Exception as e:
            log.error(e)
            traceback.print_exc()
            return False

    @staticmethod
    def response(response, charset=''):
        if not isinstance(response, urllib3.response.HTTPResponse):
            return None
        # return {httpDefine.HTTP_RESPONSE_STATUS: response.status, httpDefine.HTTP_RESPONSE_DATA: response.data,
        #         httpDefine.HTTP_RESPONSE_HEADERS: response.headers}
        return {httpDefine.HTTP_RESPONSE_STATUS: response.status,
                httpDefine.HTTP_RESPONSE_DATA: response.data.decode(httpDefine.HTTP_CODING),
                httpDefine.HTTP_RESPONSE_HEADERS: response.headers}

    @staticmethod
    def remove_response_header(response):
        response.pop(httpDefine.HTTP_RESPONSE_HEADERS)
        return response
