# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/C006.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cC006(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'C006_dl'

    def goPartList(self):

        self.assign('NL',self.dl.GNL)
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        self.assign('hot_mselect', self.Hot_mselects())
        s = self.runApp('C006_list.html')
        return s

    def initPagiUrl(self):
        url = self.sUrl


        return url
    
    def goPartLocalfrm(self):
        self.navTitle = ''
        self.currentUrl = self.sUrl + "&part=localfrm"
        self.assign('currentUrl', self.currentUrl)
        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()

        PL, L = self.dl.get_local_data()
        self.assign('dataList', L)
        self.getPagination(PL)

        self.assign('hot_mselect', self.Hot_mselects())

        s = self.runApp('C006_local.html')
        return s


    def goPartajax_update(self):
        dR = self.dl.ajax_update_data()
        return self.jsons(dR)

