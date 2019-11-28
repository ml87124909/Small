# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################

from imp import reload
from basic.publicw import DEBUG
if DEBUG=='1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cseetting(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'seetting_dl'

    def goPartList(self):

        self.assign('NL',self.dl.GNL)
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('I004_list.html')
        return s

    def initPagiUrl(self):
        url = self.sUrl
        tab = self.dl.tab

        if tab:
            url += "&tab=%s" % tab

        return url
    
    def goPartLocalfrm(self):
        self.navTitle = ''
        self.currentUrl = self.sUrl + "&part=localfrm"
        self.assign('currentUrl', self.currentUrl)
        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()

        L = self.dl.get_local_data()
        self.assign('item', L)

        return self.runApp('seetting.html')

    def goPartInsert(self):
        dR = self.dl.local_add_save()
        return self.jsons(dR)

