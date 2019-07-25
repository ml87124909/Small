# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.vi.BASE_TPL

    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL import cBASE_TPL


class cE004(cBASE_TPL):

    def setClassName(self):

        self.dl_name = 'E004_dl'
        self.inframe = 1

    def specialinit(self):
        pass

    def goPartList(self):

        self.assign('NL', self.dl.GNL)
        self.navTitle = ''
        self.getBreadcrumb()  # 获取面包屑
        PL, L = self.dl.mRight()

        self.assign('dataList', L)

        self.getPagination(PL)
        s = self.runApp('E004_list.html')
        return s

    def initPagiUrl(self):
        lb_code = self.REQUEST.get('lb_code', '')
        brand_id = self.REQUEST.get('brand_id', '')
        status = self.REQUEST.get('status', '')
        ctype = self.REQUEST.get('ctype', '')
        qqid = self.REQUEST.get('qqid', '')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        if lb_code:
            url += "&lb_code=%s" % lb_code
        if brand_id:
            url += "&brand_id=%s" % brand_id
        if status:
            url += "&status=%s" % status
        if ctype:
            url += "&ctype=%s" % ctype
        return url

    def goPartaddm(self):
        dR = self.dl.addm_data()
        return self.jsons(dR)
