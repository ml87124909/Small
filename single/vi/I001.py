# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" single/vi/I001.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import single.vi.BASE_TPL
    reload(single.vi.BASE_TPL)
from single.vi.BASE_TPL             import cBASE_TPL



class cI001(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'I001_dl'
        self.inframe = 1
    def specialinit(self):
        self.tab_data = ['收费设置', '付费记录']
        self.assign('tab_data', self.tab_data)
        self.assign('tab', self.dl.tab)
        BTNS = ''
        if str(self.dl.tab) == '1':
            BTNS = '<input type="button" class="btn btn-success span2" onclick="go_addsave()" name="add_save" value="保存"/>'
        # elif str(self.dl.tab)=='2':
        #     BTNS='<input type="submit" class="btn btn-success span2" name="add_save" value="保存积分商品"/>'
        # elif str(self.dl.tab)=='3':
        #     BTNS='<input type="submit" class="btn btn-success span2" name="add_save" value="保存积分商品"/>'
        # elif str(self.dl.tab)=='4':
        #     BTNS='保存小程序设置'
        # elif str(self.dl.tab)=='5':
        #     BTNS='保存会员设置'
        # elif str(self.dl.tab)=='6':
        #     BTNS='保存全局设置'
        self.assign('BTNS', BTNS)

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
        if self.dl.tab == '1':
            L = self.dl.get_local_data()
            self.assign('item', L)
        else:
            PL, L = self.dl.get_local_data()
            self.assign('dataList', L)
            self.getPagination(PL)

        s = self.runApp('I001_local.html')
        return s

    def goPartInsert(self):
        dR = self.dl.local_add_save()
        return self.jsons(dR)

    def goPartSearch(self):
        dR = self.dl.Search_data()
        return self.jsons(dR)

