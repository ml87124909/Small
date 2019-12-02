# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
from imp import reload
from basic.publicw import DEBUG
if DEBUG=='1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cI001(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'I001_dl'

    def specialinit(self):
        #self.tab_data = ['收费设置', '付费记录']
        self.tab_data = ['平台设置']
        self.assign('tab_data', self.tab_data)
        self.assign('tab', self.dl.tab)
        BTNS = ''
        if str(self.dl.tab) == '1':
            BTNS = '<input type="button" class="btn btn-success span2" onclick="go_addsave()" name="add_save" value="保存"/>'

        self.assign('BTNS', BTNS)

    
    def goPartLocalfrm(self):
        self.navTitle = ''
        self.currentUrl = self.sUrl + "&part=localfrm"
        self.assign('currentUrl', self.currentUrl)
        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()
        # if self.dl.tab == '1':
        #     L = self.dl.get_local_data()
        #     self.assign('item', L)
        # else:
        #     PL, L = self.dl.get_local_data()
        #     self.assign('dataList', L)
        #     self.getPagination(PL)
        L = self.dl.get_local_data()
        self.assign('item', L)

        s = self.runApp('I001_local.html')
        return s

    def goPartInsert(self):
        dR = self.dl.local_add_save()
        return self.jsons(dR)

    def goPartSearch(self):
        dR = self.dl.Search_data()
        return self.jsons(dR)
