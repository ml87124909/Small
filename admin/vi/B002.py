# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/B002.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cB002(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'B002_dl'

    def specialinit(self):
        pass

    def goPartList(self):
        self.assign('NL',self.dl.GNL)
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑

        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('B002_list.html')
        return s
    

    
    def goPartLocalfrm(self):
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()
        self.item = self.dl.get_local_data()
        self.assign('item', self.item)
        s = self.runApp('B002_local.html')
        return s

    def goPartSave_tag(self):
        dR=self.dl.save_tag()
        return self.jsons(dR)


    
    
        
 