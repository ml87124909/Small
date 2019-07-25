# -*- coding: utf-8 -*-


from imp import reload
from admin.vi import WxApi
reload(WxApi)

class csp_reply(WxApi.cWxApi):
    
    def setClassName(self):
        #设定要实例的 BIZ类和TPL类，为空则继承基类，可以能过判断part的值来设置不同的类名
        self.dl_name = 'sp_reply_dl'

    def specialinit(self):
        self.navTitle = '特殊回复'
        self.getBreadcrumb() #获取面包屑


    #管理公众号
    def goPartList(self):
        self.js.append('emotions.js')
        weid = self.weid
        wechat = {}
        if weid:
            wechat = self.dl.db.fetch("SELECT welcome , defaults FROM ims_wechats WHERE weid = '%s'"%weid)
            if not wechat :
                return self.mScriptMsg('抱歉，您操作的公众号不在存，请切换管理的公众号！',[['admin?viewid=common','返回公众号管理']])
        else:
            return self.mScriptMsg('抱歉，您操作的公众号不在存，请切换管理的公众号！',[['admin?viewid=common','返回公众号管理']])
        self.assign('wechat',wechat)
       
        return self.runApp('sp_reply.html')

    def goPartPost(self):
        pk = self.dl.GP('pk','')
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':'','pk':pk}  
        data = {
            'welcome':self.dl.GP("welcome_reply",'') , 'default' : self.dl.GP("default_reply",'')
        }
        if pk :
            self.dl.db.update("ims_wechats",data," weid='%s'" % pk)
        url = "admin?viewid=%s" % (self.dl.GP("viewid"))
        s=self.mScriptMsg('数据修改成功',[[url,'返回编辑']],'success')
        return s
