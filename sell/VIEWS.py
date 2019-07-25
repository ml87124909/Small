# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
"""sell/VIEWS.py"""
import jwt
import time
import os
from flask import jsonify
from basic.publicw import cSELL,ATTACH_ROOTR,db, oSHOP,oUSER,oMALL,oQINIU,oGOODS,oGOODS_D,oORDER_SET,\
    oGOODS_N,oGOODS_G,oOPENID,oSHOP_T,oCATEGORY,oGOODS_SELL,oTOLL,oGOODS_PT,oGOODS_DPT,oPT_GOODS,oUSERS,oUSERS_OSS,oGOODS_H
from basic.wxbase import wx_minapp_login

class cVIEWS(cSELL):

    def __init__(self, request):

        self.objHandle = request
        # if self.objHandle.method == 'POST':
        #     self.REQUEST = self.objHandle.form
        # else:
        #     self.REQUEST = self.objHandle.args
        self.REQUEST = request.values
        self.ATTACH_ROOT = ATTACH_ROOTR
        self.db = db
        self.jsons = jsonify
        self.usr_id = 0
        self.usr_id_p = 0
        self.app_id = ''
        self.secret = ''
        self.classpath = 'sell'
        self.SECRET_KEY = '5bf030dbb13422031ea802a9ab75900a'
        self.error_code = {
            -1: u'服务器内部错误',
            0: u'接口调用成功',
            403: u'禁止访问',
            405: u'错误的请求类型',
            501: u'数据库错误',
            502: u'并发异常，请重试',
            600: u'缺少参数',
            601: u'无权操作:缺少 token',
            602: u'签名错误',
            700: u'暂无数据',
            701: u'该功能暂未开通',
            702: u'资源余额不足',
            901: u'登录超时',
            300: u'缺少{}参数',
            400: u'域名错误',
            401: u'该域名已删除',
            402: u'该域名已禁用',
            404: u'暂无数据',
            10000: u'微信用户未注册',
            'ok': 'success'
        }
        # 获取网址请求过来的常用参数
        self.viewid = self.GP('viewid', 'home')  # viewid值
        self.part = self.GP('part', 'begin')
        self.appid = self.GP('appid', '')
        self.malitoken = self.objHandle.headers.get('malitoken', '')
        if self.malitoken == '':
            self.malitoken = self.REQUEST.get('malitoken', '')  # token值

        if self.malitoken and self.part not in ['login', 'Gologin']:
            dR = self.checktoken(self.malitoken)
            if dR['code'] == 0:
                self.usr_id = int(dR['usr_id'])
                self.usr_id_p = self.get_usr_id_p(self.usr_id)
        # *****************************************************************

        self.oSHOP = oSHOP
        self.oUSER = oUSER
        self.oMALL = oMALL
        self.oQINIU = oQINIU
        #self.oKUAIDI = oKUAIDI
        self.oGOODS = oGOODS
        self.oGOODS_D = oGOODS_D
        self.oORDER_SET = oORDER_SET
        self.oGOODS_N = oGOODS_N
        self.oGOODS_G = oGOODS_G
        self.oOPENID = oOPENID
        self.oSHOP_T = oSHOP_T
        self.oCATEGORY = oCATEGORY
        self.oUSERS = oUSERS
        self.oGOODS_SELL = oGOODS_SELL
        self.oTOLL = oTOLL
        self.oGOODS_PT = oGOODS_PT
        self.oGOODS_DPT = oGOODS_DPT
        self.oPT_GOODS = oPT_GOODS
        # ###########################################
        self.app_id = self.oMALL.get(0).get('appid', '')
        self.secret = self.oMALL.get(0).get('secret', '')
        self.api = wx_minapp_login(self.app_id, self.secret)



    def make_sub_path(self, sPATH):
        """检查os的最后一级子目录，如果不存在，生成之"""
        if os.path.exists(sPATH) == 0:
            os.makedirs(sPATH)
        return 0

    def get_usr_id_p(self, usr_id):
        sql = """
               SELECT 
                     case when COALESCE(u.usr_id_p,0)=0 then U.usr_id else u.usr_id_p end 
                  FROM users U 
                  WHERE U.usr_id=%s AND  U.status=1
               """

        lT, iN = self.db.select(sql, usr_id)
        if not iN:
            return 0
        return lT[0][0]

    def getToday(self,format=3):
        t = time.time()
        date_ary = time.localtime(t)
        if format == 1:
            x = time.strftime("%Y%m%d", date_ary)
        elif format == 2:
            x = time.strftime("%H:%M", date_ary)
        elif format == 3:
            x = time.strftime("%Y/%m/%d", date_ary)
        elif format == 4:
            x = time.strftime("%Y/%m/%d %H:%M", date_ary)
        elif format == 5:
            x = time.strftime("%y%m%d", date_ary)
        elif format == 6:
            x = time.strftime("%Y-%m-%d", date_ary)
        elif format == 7:
            x = time.strftime("%Y/%m/%d %H:%M:%S", date_ary)
        elif format == 8:
            x = time.strftime("%Y-%m-%d %H:%M", date_ary)
        elif format == 9:
            x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
        elif format == 10:
            x = time.strftime("%Y年%m月%d日 %H:%M", date_ary)
        else:
            x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
        return x

    # 代替了self.REQUEST.get()
    # key为参数名， default为默认值，type为是否需要过滤字符
    def GP(self, key, default=None, ctype=1):
        value = self.REQUEST.get(key, default)
        L_error = ['"', "'", '%', '#', '&', '*', '(', ')', '@', '`', '\\', ']', '=', '<', '>', '?', '/']
        if ctype == 1 and value and isinstance(value, str):
            for c in L_error:
                if c in value:
                    value = value.replace(c, '')
        return value

    def create_token(self, usr_id):

        payloads = {
            #"exp": int(time.time()) + 60 * 60 * 2,  # 60*60*24  一天
            "aud": "janedao",
            "usr_id": usr_id
        }
        encoded_jwt = jwt.encode(payloads, 'secret', algorithm='HS256')
        token = encoded_jwt.decode('utf-8')
        return token

    def checktoken(self, token):
        dR = {'MSG': '', 'code': '', 'usr_id': ''}
        try:
            payload = jwt.decode(token, 'secret', audience='janedao', algorithms=['HS256'])
        except:
            dR['code'] = 1
            dR['MSG'] = 'token无效,解密失败'
            return dR

        if not payload:
            dR['code'] = 1
            dR['MSG'] = 'token无法解密a'
            return dR

        # if payload['exp'] < int(time.time()):
        #     dR['code'] = 1
        #     dR['MSG'] = 'token无效，登录超时'
        #     return dR

        if payload['aud'] != "janedao":
            dR['code'] = 1
            dR['MSG'] = 'token无法解密b'
            return dR

        dR['usr_id'] = payload['usr_id']
        dR['code'] = 0
        return dR





