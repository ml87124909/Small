# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""basic/base.py"""


class set_cookie:
    def __init__(self, REQUEST, CLIENT_NAME):
        # self.cookie = Cookie.SimpleCookie()
        self.REQUEST = REQUEST
        self.authkey = '%s-239-hyj891-22558863' % CLIENT_NAME
        self.keyname = CLIENT_NAME
        self.set = []

    # 基础设置 cookie 调用zope 的cookies处理
    def setcookie(self, key, value,  expires=0, path='/'):
        self.set.append(["%s%s" % (self.keyname, key), value, expires, path])
        return key, value

    def responeCookie(self, response):
        for v in self.set:
            response.set_cookie(v[0], value=v[1], max_age=7200, expires=v[2], path=v[3])  # flask


    def getcookie(self, key):
        return self.REQUEST.cookies.get("%s%s" % (self.keyname, key))

    # 设置cookies
    def isetcookie(self, key, value='', expires=0, path='/'):
        cookiestr = self.auth_code(value)
        self.setcookie(key, cookiestr,  expires, path)
        return 1

    # 读取cookies
    def igetcookie(self, key):
        value = self.getcookie(key)
        if value:
            value = self.auth_code(value, 'DECODE')
            if len(value) > 0:
                return {'value': value, 'hash': 'CCTMTQT=T=TMTQT=T=MQ=='}
            else:
                return None
        else:
            return None

    # 清空cookies
    def clearcookie(self, key):
        self.setcookie(key, '', -1000)

    def auth_code(self, cstr, type='ENCODE'):
        import base64, random, hashlib
        key = hashlib.md5(self.authkey.encode('utf-8')).hexdigest()
        keylen = len(key)
        temp = ''
        if type == 'ENCODE':
            cstr = "%s" % cstr
            new_code = ''
            cstr = base64.b64encode(cstr.encode('utf-8')).decode('ascii')
            tc = "%07d" % random.randint(1, 9999999)
            timecode = hashlib.md5(tc.encode('utf-8')).hexdigest()
            timelen = len(timecode)
            strlen = len(cstr)
            for i in list(range(strlen)):
                k = i % timelen
                new_code += '%s%s%s' % (timecode[k], timecode[0], cstr[i])  # TTMWTQ9T=uT=
            strlen = len(new_code)
            for i in list(range(strlen)):
                k = i % keylen
                temp += '%s%s' % (key[k], new_code[i])  # IT1TNMTWgT4QN9jTM==uIT1=
            return base64.b64encode(temp.encode('utf-8')).decode(
                'ascii')  # SVQxVE5NVFdnVDRRTjlqVE09PXVJVDE9#SVQxVE5NVFdnVDRRTjlqVE09PXVJVDE9
        else:
            cstr = "%s=" % cstr
            cstr = base64.b64decode(cstr.encode('utf-8')).decode('ascii')
            strlen = len(cstr)
            for i in list(range(strlen)):
                if i % 2 != 0:
                    temp += cstr[i]
            strlen = len(temp)
            new_code = ''
            for i in list(range(strlen)):
                if i % 3 == 2:
                    new_code += temp[i]
            new_code = '%s==' % new_code
            return base64.b64decode(new_code.encode('utf-8')).decode('ascii')








