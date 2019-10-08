# -*- coding:utf8 -*-
# Time    : 2019/9/19 18:44
# Author  : Richard
# Email   : tangtao556@qq.com
# File    : util.py
import os
import traceback


class Util(object):
    @staticmethod
    def intCheck(data):
        return True

    @staticmethod
    def floatCheck(data):
        return True

    @staticmethod
    def strCheck(data):
        if len(data) > 0:
            return True
        return False

    @staticmethod
    def listCheck(data):
        if len(data) > 0:
            for i in data:
                if not Util.checkEmpty(i):
                    return False
            return True
        return False

    @staticmethod
    def tupleCheck(data):
        if len(data) > 0:
            for i in data:
                if not Util.checkEmpty(i):
                    return False
            return True
        return False

    @staticmethod
    def setCheck(data):
        if len(data) > 0:
            for i in data:
                if not Util.checkEmpty(i):
                    return False
            return True
        return False

    @staticmethod
    def dictCheck(data):
        if len(data) > 0:
            for i in data:
                if not Util.checkEmpty(i):
                    return False
            return True
        return False

    @staticmethod
    def checkNone(data):
        if type(None) != type(data):
            return True
        return False

    @staticmethod
    def checkEmpty(variate, recursion=False):
        key = None
        if isinstance(variate, int):
            key = "int"
        elif isinstance(variate, str):
            key = "str"
        elif isinstance(variate, float):
            key = "float"
        elif isinstance(variate, list):
            key = "list"
        elif isinstance(variate, tuple):
            key = "tuple"
        elif isinstance(variate, dict):
            key = "dict"
        elif isinstance(variate, set):
            key = "set"
        data = variate
        switch = {
            "int": lambda x: Util.intCheck(data),
            "float": lambda x: Util.floatCheck(data),
            "str": lambda x: Util.strCheck(data),
            "list": lambda x: Util.listCheck(data),
            "tuple": lambda x: Util.tupleCheck(data),
            "set": lambda x: Util.setCheck(data),
            "dict": lambda x: Util.dictCheck(data)
        }

        try:
            return switch[key](data)
        except KeyError as e:
            traceback.print_exc()
            return True

    @staticmethod
    def get_path(rel_path):
        if os.path.isabs(rel_path):
            return rel_path
        else:
            return os.getcwd() + "/" + rel_path

    @staticmethod
    def complex_compare(src, obj, strict=False):
        if strict:
            if len(src) != len(obj):
                return False
        if isinstance(obj, dict):
            for k, v in obj.items():
                if not Util.find_obj(src.get(k), obj.get(k), strict):
                    return False
            return True
        elif isinstance(obj, (list, tuple)):
            if strict:
                for i in range(len(obj) - 1):
                    if not Util.find_obj(src[i], obj[i], strict):
                        return False
                return True
            else:
                out_success = True
                for item_obj in obj:
                    in_success = False
                    for item_src in src:
                        if Util.find_obj(item_src, item_obj, strict):
                            in_success = True
                            break
                    out_success = out_success and in_success
                    if not out_success:
                        break
                return out_success
        elif isinstance(obj, set):
            out_success = True
            for i in obj:
                in_success = False
                for j in src:
                    if Util.find_obj(j, i, strict):
                        in_success = True
                        break
                out_success = out_success and in_success
                if not out_success:
                    break
            return out_success
        return None

    @staticmethod
    def base_compare(src, obj):
        return src == obj

    @staticmethod
    def find_obj(src, obj, strict=False):
        type_src = type(src)
        type_obj = type(obj)
        if type_src != type_obj:
            return False
        if type_obj in [dict, tuple, list, set]:
            return Util.complex_compare(src, obj, strict)
        else:
            return Util.base_compare(src, obj)
