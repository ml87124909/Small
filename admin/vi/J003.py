# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/vi/J003.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL

class cJ003(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'J003_dl'
        self.inframe = 1
    def specialinit(self):
        pass

    def goPartList(self):

        self.getBreadcrumb()  # 获取面包屑
        self.assign('NL',self.dl.GNL)
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('J003_list.html')
        return s
    
    def initPagiUrl(self):
        parent_id = self.REQUEST.get('parent_id','')
        qqid = self.REQUEST.get('qqid','')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        if parent_id:
            url += "&parent_id=%s" % parent_id
        return url
    
    def goPartLocalfrm(self):
        self.navTitle = '人员授权'
        self.need_editor = 1
        self.initHiddenLocal()#初始隐藏域
        self.getBreadcrumb()  # 获取面包屑
        self.getBackBtn()

        item = self.dl.get_local_data(self.pk)
        self.assign('item',item)
        s = self.runApp('J003_local.html')
        return s
    
    
    
        
 