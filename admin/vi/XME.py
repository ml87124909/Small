# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG=='1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL

class cXME(cBASE_TPL):
    
    def setClassName(self):
        
        self.dl_name = 'XME_dl'
        self.inframe = 1

    def specialinit(self):
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑

        self.can_del=True
        self.can_add=True
        self.can_upd=True

    def goPartList(self):

        self.assign('NL',self.dl.GNL)
        self.assign('filter',self.dl.get_xhmss_data())
        filter=self.dl.GP('filter','')
        self.assign('param',{'filter':filter})
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        self.assign({'checkAllBtn':False})
        s = self.runApp('XME_list.html')
        return s

    
    def initPagiUrl(self):
        qqid = self.REQUEST.get('qqid','')
        filter=self.REQUEST.get('filter','')
        orderbydir = self.REQUEST.get('orderbydir','')
        
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        if filter:
            url += "&filter=%s" % filter
        if orderbydir:
            url += "&orderbydir=%s" % orderbydir
        
        return url
    
    def goPartLocalfrm(self):
        self.backurl = 'admin?fid=XME'
        self.need_editor = 1
        self.initHiddenLocal()#初始隐藏域

        #self.getUploadHtml()
        self.getBackBtn()
        pk=self.REQUEST.get('pk','')
        if pk=='':pk='new'
        self.assign('pk',pk)

        s = self.runApp('XME_local.html')
        return s

    def goPartMain_old(self):
        #self.assign('top_btns',self.top_btns())
        self.navTitle = '公众号信息' #% self.objHandle.method
        self.getBreadcrumb() #获取面包屑
        item = self.dl.db.fetch('''select * from ims_wechats ''')
        item['qrcode'] = self.Html.uploadfile('qrcode',item.get('qrcode',''))
        item['headimg'] = self.Html.uploadfile('headimg',item.get('headimg',''))
        self.assign('item',item)
        self.assign({'site_url':self.objHandle.environ.get('HTTP_HOST') , 'base_path':localurl})
        self.dl.cookie.setcookie("__flag",self.dl.save_flag)
        #import platform
        #self.printf(platform.python_version())
        s = self.runApp('base_main.html')
        return s
    
    
    
    
        
 