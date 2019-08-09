# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/D003.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cD003(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'D003_dl'
        self.inframe = 1
    def specialinit(self):
        self.tab_data = ['拼团列表', '开团记录', '拼团记录','促团设置']
        self.assign('tab_data', self.tab_data)
        self.assign('tab', self.dl.tab)
        BTNS = ''
        # if str(self.dl.tab)=='1':
        #     BTNS='<input type="submit" class="btn btn-success span2" name="add_save" value="保存拼团列表"/>'
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
        self.navTitle = '店铺信息'
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('D003_list.html')
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

        PL, L = self.dl.get_local_data()
        self.assign('dataList', L)
        self.getPagination(PL)

        self.assign('save_alert', self.dl.GP('save_alert', '0'))
        self.assign('go_mselect', self.Goods_mselects())

        s = self.runApp('D003_local.html')
        return s

    def goPartInsert(self):
        dR = self.dl.local_add_save()
        return self.jsons(dR)

    def goPartajax_update(self):
        dR = self.dl.ajax_update_data()
        return self.jsons(dR)

    def goPartajax_add(self):
        dR = self.dl.ajax_add_data()
        return self.jsons(dR)

    def goPartajax_edit(self):
        dR = self.dl.ajax_edit_data()
        return self.jsons(dR)

    def goPartoktype(self):
        dR = self.dl.oktype_data()
        return self.jsons(dR)

    def goPartgo_ok(self):
        dR = self.dl.go_ok_data()
        return self.jsons(dR)

    def goPartgo_fail(self):
        dR = self.dl.go_fail_data()
        return self.jsons(dR)
