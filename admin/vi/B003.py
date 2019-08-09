# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/B003.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL


class cB003(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'B003_dl'

    def goPartList(self):
        self.assign('NL',self.dl.GNL)
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('B003_list.html')
        return s

    def initPagiUrl_Local(self):
        url = 'admin?viewid=B003&part=localfrm'
        return url

    def getPagination(self, PL):
        self.cur_page = PL[0]
        self.total_pages = PL[1]
        PagiUrl = self.initPagiUrl_Local()
        html_pager = self.pagination(PL[2], self.cur_page, url=PagiUrl)
        self.assign('html_pager', html_pager)

    
    def goPartLocalfrm(self):
        self.assign('NL', ['模板ID','模板名称'])
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()
        PL, L = self.dl.get_local_data()
        self.assign('dataList', L)
        self.getPagination(PL)
        s = self.runApp('B003_local.html')
        return s

    def goPartSave_temp(self):
        dR=self.dl.save_temp()
        return self.jsons(dR)


    
    
    
        
 