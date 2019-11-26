# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
from imp import reload

from basic.publicw import DEBUG
if DEBUG=='1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)

    import basic.WxApi
    reload(basic.WxApi)
from admin.vi.BASE_TPL             import cBASE_TPL
from basic.WxApi import cWxApi

class cfans(cBASE_TPL):
    
    def setClassName(self):
        #设定要实例的 BIZ类和TPL类，为空则继承基类，可以能过判断part的值来设置不同的类名
        self.dl_name = 'fans_dl'
        #self.inframe = 1

    def specialinit(self):
        self.navTitle = '粉丝管理'
        self.api = cWxApi()
        self.account = self.api.account
        self.weid = self.api.weid
        self.uid = self.api.uid

    def goPartList(self):
        
        self.assign('NL',self.dl.GNL)
        PL,L = self.dl.mRight(self.weid)
        self.assign('dataList',L)
        self.getPagination(PL)
        return self.runApp('fanslist.html')
    
    def initPagiUrl(self):
        qqid = self.REQUEST.get('qqid','')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        return url
    

        
 