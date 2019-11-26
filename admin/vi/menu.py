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
import flask,re


class cmenu(cBASE_TPL):

    def specialinit(self):
        self.navTitle = '自定义菜单'
        self.WxApi=cWxApi()
        self.account = self.WxApi.account
        self.weid = self.WxApi.weid
        self.uid = self.WxApi.uid



    def goPartList(self):
        menu = self.dl.cookie.getcookie('menu_%s' % self.weid)

        if menu:
            menu = re.sub('\'', '\"', menu)
            menu = flask.json.loads(menu)
        #res = self.WxApi.menuQuery()
        if not menu or not isinstance(menu , dict):
            res = self.WxApi.menuQuery()

            self.dl.cookie.setcookie('menu_%s' % self.weid , str(res) , 86400)
        else:
            res = menu
        self.assign('menu',res)
        return self.runApp('menu.html')

    def goPartRefresh(self):
        self.dl.cookie.isetcookie('menu_%s' % self.weid , '' , -3600)
        return self.mScriptMsg("菜单数据已刷新",[['admin?viewid=menu','返回菜单设计']],'success')

    def goPartDelete(self):
        #WeEngine = engine.cEngine(self.account)
        self.WxApi.menuDelete()
        self.dl.cookie.isetcookie('menu_%s' % self.weid , '' , -3600)
        return self.mScriptMsg("菜单数据已删除",[['admin?viewid=menu','返回菜单设计']],'success')

    def goPartSaveMenu(self):

        dat = self.dl.REQUEST.get('do','')
        menu = {"button": flask.json.loads(dat)}
        res = self.WxApi.menuCreate(menu)
        if res == 0:
            self.dl.cookie.isetcookie('menu_%s' % self.weid , '' , -3600)
            dR = {'code': '0', 'MSG': '保存成功!'}
            return self.jsons(dR)
            #return self.mScriptMsg("菜单数据已保存",[['admin?viewid=menu','返回菜单设计']],'success')
        else:
            dR = {'code': '1', 'MSG': '保存失败!'}
            #return self.mScriptMsg("菜单数据保存失败，错误代码：%s[%s]" % (res,self.WxApi.weixin_code(res)) ,[['admin?viewid=menu','返回菜单设计']],'error')
            return self.jsons(dR)



    def goPartCreateMenu(self):
        self.specialinit()
        #WeEngine = engine.cEngine(self.account)
        menu = {
             "button":[
                 {  
                      "type":"view",
                      "name":"患者入口",
                      "url":"http://shen.szszyy.cn/szjk/index?module=personal"
                  },
                  { 
                      "type":"view",
                      "name":"医生入口",
                      "url":"http://shen.szszyy.cn/szjk/expert?module=home"
                  }
               ]
            }
        res = self.WxApi.menuCreate(menu)
        return str(res)
