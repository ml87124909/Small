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

class csp_reply(cBASE_TPL):
    
    def setClassName(self):
        #设定要实例的 BIZ类和TPL类，为空则继承基类，可以能过判断part的值来设置不同的类名
        self.dl_name = 'sp_reply_dl'

    def specialinit(self):
        self.navTitle = '特殊回复'
        self.api = cWxApi()
        self.account = self.api.account
        self.weid = self.api.weid
        self.uid = self.api.uid


    #管理公众号
    def goPartList(self):
        weid = self.weid

        wechat = {}
        if weid:
            wechat = self.dl.db.fetch("SELECT welcome , defaults FROM ims_wechats WHERE weid = %s"%weid)
            if not wechat :
                return self.mScriptMsg('抱歉，您操作的公众号不在存，请切换管理的公众号！',[['admin?viewid=menu','返回公众号管理']])
        else:
            return self.mScriptMsg('抱歉，您操作的公众号不在存，请切换管理的公众号！',[['admin?viewid=menu','返回公众号管理']])
        self.assign('weid',weid)
        self.assign('wechat',wechat)
        return self.runApp('sp_reply.html')

    def goPartPost(self):
        pk = self.dl.GP('pk','')
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':'','pk':pk}  
        data = {
            'welcome':self.dl.GP("welcome_reply",'') , 'defaults' : self.dl.GP("default_reply",'')
        }
        if pk :
            self.dl.db.update("ims_wechats",data," weid=%s" % pk)
        url = "admin?viewid=%s" % (self.dl.GP("viewid"))
        s=self.mScriptMsg('数据修改成功',[[url,'返回编辑']],'success')
        return s
