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



class cF003(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'F003_dl'
        self.inframe = 1
    def specialinit(self):
        pass

    def goPartList(self):
      
        self.assign('NL',self.dl.GNL)
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑

        PL,L = self.dl.mRight()
        self.assign('dataList',L)

        self.getPagination(PL)
        s = self.runApp('F003_list.html')
        return s
    

    
    def goPartLocalfrm(self):
        self.navTitle = ''

        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
       
        self.getBackBtn()

        self.item = self.dl.get_local_data()
        self.assign('item', self.item)

        s = self.runApp('F003_local.html')
        return s

    # def goPartsync_data(self):
    #     dR=self.dl.sync_data()
    #     return self.jsons(dR)
    #
    
    
        
 