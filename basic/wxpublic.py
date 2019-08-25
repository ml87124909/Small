# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""basic/wxpublic.py"""
from jinja2 import Environment, PackageLoader
from flask import request
from .base import set_cookie
from .publicw import CLIENT_NAME




class wxpublic():

    def __init__(self,PackageLoader=''):
        self.tpl_path = ''
        self.client_name = ''
        self.tpl = 'template'

        self.pl = PackageLoader
        self.var = {}
        self.pf = []
        self.cookieprefix = CLIENT_NAME
        self.cookie = set_cookie(self.objHandle, CLIENT_NAME)
        self.debug = 1
        pass

    def setPackge(self,PackageLoader=''):
        self.pl = PackageLoader

    def setcookie(self , key , value , expires = 0, path='/'):
        return self.cookie.setcookie(key , value , expires , path)

    def getcookie(self,key):
        return self.cookie.getcookie(key)

    def isetcookie(self , key , value = '' , expires = 0, path='/'):
        return self.cookie.isetcookie(key , value , expires , path)

    def igetcookie(self,key):
        return self.cookie.igetcookie(key)

    def clearcookie(self,key):
        self.cookie.clearcookie(key)

    def printf(self,*data):
        for d in data:
            self.pf.append(d)

    def display(self,template):
        if not template or template == '':
            return ''
        env = Environment(loader=PackageLoader('%s'% (self.pl), self.tpl))
        def dateformat(value, format="%Y-%m"):
            import time
            t = time.localtime(value)
            return time.strftime(format,t) 
        env.filters['dateformat'] = dateformat 
        template = env.get_template('%s' % template)
        self.var['cookieprefix'] = self.cookieprefix
        html = template.render(self.var)
        if len(self.pf) > 0:
            temp = ''
            for p in self.pf:
                temp += p

            html = temp + html
        return  html

    def echo(self,html=''):
        if len(self.pf) > 0:
            temp = ''
            for p in self.pf:
                temp += p

            html = temp + html
        return  html

    def assign(self , param , value = None):
        if type(param) == str:
            self.var[param] = value
        elif type(param) == dict:
            for k,v in param.items():
                self.var[k] = v