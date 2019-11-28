# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/vi/I002.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cI002(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'I002_dl'

    def specialinit(self):
        pass

    def goPartList(self):
        self.assign('NL',self.dl.GNL)
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('I002_list.html')
        return s

    def goPartLocalfrm(self):
        self.navTitle = ''
        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()
        self.item = self.dl.get_local_data()
        self.assign('item', self.item)
        s = self.runApp('I002_local.html')
        return s
    
    
    
        
 