# -*- coding: utf-8 -*-



from imp import reload
from admin.vi import WxApi
reload(WxApi)

import flask,re


class cmenu(WxApi.cWxApi):

    def specialinit(self):
        self.navTitle = '自定义菜单'
        self.getBreadcrumb()  # 获取面包屑
        # self.api=WxApi.cWxApi()
        # self.account = self.api.account
        # self.weid = self.api.weid
        # self.uid = self.api.uid
        #self.action = self.REQUEST.get('action','index')
        #self.name = self.REQUEST.get('part',self.action)


    def goPartList(self):
        menu = self.dl.cookie.getcookie('menu_%s' % self.weid)

        if menu:
            menu = re.sub('\'', '\"', menu)
            menu = flask.json.loads(menu)
        
        if not menu or not isinstance(menu , dict):
            #WeEngine = engine.cEngine(self.account)
            res = self.menuQuery()
            #print(res,'0000000')
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
        self.menuDelete()
        self.dl.cookie.isetcookie('menu_%s' % self.weid , '' , -3600)
        return self.mScriptMsg("菜单数据已删除",[['admin?viewid=menu','返回菜单设计']],'success')

    def goPartSaveMenu(self):
        dat = self.dl.REQUEST.get('do','')
        #WeEngine = engine.cEngine(self.account)
        # menu='''{
        #         "button": %s
        #     }
        # '''%dat
        #print(dat,type(dat),type(flask.json.loads(dat)))
        #exec ('menu = {"button":%s}'% dat) #这里遇到了问题，在python里一定要用这种方法声明一个menu变量，不然会出现各种问题，已亲测N次
        #print(menu, '----------')
        menu = {"button": flask.json.loads(dat)}
        #print(menu,'----------')
        res = self.menuCreate(menu)
        if res == 0:
            self.dl.cookie.isetcookie('menu_%s' % self.weid , '' , -3600)
            return self.mScriptMsg("菜单数据已保存",[['admin?viewid=menu','返回菜单设计']],'success')
        else:
            return self.mScriptMsg("菜单数据保存失败，错误代码：%s[%s]" % (res,self.weixin_code(res)) ,[['admin?viewid=menu','返回菜单设计']],'error')



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
        res = self.menuCreate(menu)
        return str(res)
