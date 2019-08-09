# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/E004.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cE004(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'E004_dl'
        self.inframe = 1


    def goPartList(self):
       
        self.assign('NL',self.dl.GNL)
        self.navTitle = '采购订单'
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)

        self.getPagination(PL)
        s = self.runApp('E004_list.html')
        return s
    
    def initPagiUrl(self):
        lb_code = self.REQUEST.get('lb_code','')
        brand_id = self.REQUEST.get('brand_id','')
        status = self.REQUEST.get('status','')
        ctype = self.REQUEST.get('ctype','')
        qqid = self.REQUEST.get('qqid','')
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
    
    def goPartLocalfrm(self):
        self.navTitle = '商城公告'

        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
       
        self.getBackBtn()

        self.item = self.dl.get_local_data(self.pk)
        self.assign('item', self.item)

        s1 = self.Html.editor(self.item.get('content',''),'container', '1000px', '300px')
        self.assign('editor', s1)

        fl = self.dl.getfllist()
        fllist = self.Html.select(fl, 'fenlei', self.item.get('fenlei', 0), {'class': 'form-control'})
        self.assign('fllist', fllist)
        s = self.runApp('E004_local.html')
        return s

    def goPartOrder_reply(self):
        dR=self.dl.get_order_reply_data()
        return self.jsons(dR)

    def goPartRetweet(self):
        dR=self.dl.get_retweet_data()
        return self.jsons(dR)

    def goPartRetweet_v(self):
        dR=self.dl.get_retweetv_data()
        return self.jsons(dR)

    def goPartOrder_ok(self):
        dR=self.dl.get_order_ok_data()
        return self.jsons(dR)

    def goPartOrder_ig(self):
        dR=self.dl.get_order_ig_data()
        return self.jsons(dR)

    def goPartOrder_ig_save(self):
        dR=self.dl.get_order_ig_save_data()
        return self.jsons(dR)

    def goPartRetweet_ig(self):
        dR=self.dl.get_retweet_ig_data()
        return self.jsons(dR)

    def goPartOrder_ig_r(self):
        dR=self.dl.get_order_ig_r_data()
        return self.jsons(dR)

    def goPartOrder_ig_reply(self):
        dR=self.dl.get_order_ig_reply_data()
        return self.jsons(dR)
    
    
    
        
 