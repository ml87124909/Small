# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/F002.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cF002(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'F002_dl'
        self.inframe = 1
    def specialinit(self):
        pass

    def goPartList(self):
      
        self.assign('NL',self.dl.GNL)
        self.navTitle = '充值查询'
        self.getBreadcrumb() #获取面包屑

        PL,L = self.dl.mRight()
        self.assign('dataList',L)

        self.getPagination(PL)
        s = self.runApp('F002_list.html')
        return s
    

    
    def goPartLocalfrm(self):
        self.navTitle = '充值查询'

        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
       
        self.getBackBtn()

        self.item = self.dl.get_local_data()
        self.assign('item', self.item)

        s = self.runApp('G004_local.html')
        return s

    def goPartsync_data(self):
        dR=self.dl.sync_data()
        return self.jsons(dR)
    
    
    
        
 