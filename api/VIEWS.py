# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""api/VIEWS.py"""
import os
import time
from flask import jsonify
from basic.publicw import cAPI,ATTACH_ROOTR,md5code,db,oSHOP,oUSER,oMALL,oQINIU,oGOODS,oGOODS_D,oORDER_SET\
    ,oGOODS_N,oGOODS_G,oOPENID,oSHOP_T,oCATEGORY,oGOODS_SELL,oGOODS_PT,oGOODS_DPT,oPT_GOODS,oTOLL


class cVIEWS(cAPI):

    def __init__(self, request,subid):

        self.objHandle = request
        self.REQUEST = self.objHandle.values
        self.ATTACH_ROOT=ATTACH_ROOTR
        self.subusr_id = subid
        self.md5code=md5code
        self.db = db
        self.jsons=jsonify
        #self.text=text
        self.classpath = 'api'
        self.SECRET_KEY='5bf030dbb13422031ea802a9ab75900a'
        # 获取网址请求过来的常用参数
        self.viewid = self.RQ('viewid', 'home')  # viewid值
        self.part = self.RQ('part', 'begin')
        self.appid = self.RQ('appid', '')
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
                            'ok':'success'
                        }
        # *****************************************************************

        self.oSHOP=oSHOP
        self.oUSER=oUSER
        self.oMALL=oMALL
        self.oQINIU = oQINIU
        #self.oKUAIDI = oKUAIDI
        self.oGOODS=oGOODS
        self.oGOODS_D=oGOODS_D
        self.oORDER_SET=oORDER_SET
        self.oGOODS_N=oGOODS_N
        self.oGOODS_G=oGOODS_G
        self.oOPENID=oOPENID
        self.oSHOP_T=oSHOP_T
        self.oCATEGORY=oCATEGORY
        self.oGOODS_SELL=oGOODS_SELL
        self.oGOODS_PT = oGOODS_PT
        self.oGOODS_DPT = oGOODS_DPT
        self.oPT_GOODS = oPT_GOODS
        self.oTOLL = oTOLL
    # ###########################################
    #     ########七牛用户自有调用
        self.qiniu_ctype = self.oQINIU.get(self.subusr_id).get('ctype', '')
        self.qiniu_access_key = self.oQINIU.get(self.subusr_id).get('access_key', '')
        self.qiniu_secret_key = self.oQINIU.get(self.subusr_id).get('secret_key', '')
        self.qiniu_bucket_name = self.oQINIU.get(self.subusr_id).get('name', '')
        self.qiniu_domain = self.oQINIU.get(self.subusr_id).get('domain', '')
        self.endpoint = self.oQINIU.get(self.subusr_id).get('endpoint', '')
    #     ########七牛公共调用
        self.qiniu_ctype_all = self.oQINIU.get(1).get('ctype', '')
        self.qiniu_access_key_all = self.oQINIU.get(1).get('access_key', '')
        self.qiniu_secret_key_all = self.oQINIU.get(1).get('secret_key', '')
        self.qiniu_bucket_name_all = self.oQINIU.get(1).get('name', '')
        self.qiniu_domain_all = self.oQINIU.get(1).get('domain', '')
        self.endpoint_all = self.oQINIU.get(1).get('endpoint', '')
        ##
        self.base_url = self.oTOLL.get().get('base_url')  # 平台支付回调域名

    def RQ(self, key, default=None, ctype=1):
        value = self.REQUEST.get(key, default)
        L_error = ['"', "'", '%', '#', '&', '*', '(', ')', '@', '`', '\\', ']', '=', '<', '>','?','/']
        if ctype==1 and value and isinstance(value, str):
            for c in L_error:
                if c in value:
                    value=value.replace(c,'')
        return value

    def make_sub_path(self, sPATH):
        """检查os的最后一级子目录，如果不存在，生成之"""
        if os.path.exists(sPATH) == 0:
            os.makedirs(sPATH)
        return 0



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



    def webapge_log(self,cname,errors):
        sql="insert into webapge_log(cname,errors,ctime)values(%s,%s,now())"
        self.db.query(sql,[cname,errors])
        return





