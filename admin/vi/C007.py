# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/C007.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL



class cC007(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'C007_dl'
        self.inframe = 1
    def specialinit(self):
        pass

    def goPartList(self):

        self.assign('NL',self.dl.GNL)
        self.navTitle = '商品评价'
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)

        self.getPagination(PL)
        s = self.runApp('C007_list.html')
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
        self.navTitle = '商品反馈'

        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域

        self.getBackBtn()

        self.item = self.dl.get_local_data(self.pk)
        self.assign('item', self.item)
        self.assign('Goods_mselect', self.Goods_mselect())
        self.assign('save_alert', self.dl.GP('save_alert', '0'))
        s = self.runApp('C007_local.html')
        return s

    def goPartInsert(self):
        dR = self.dl.local_add_save()
        res = dR.get('code','')
        pk = dR.get('pk', '')
        if res=='0':
            save_alert = 1
        else:
            save_alert = 2

        url = "admin?viewid=%s&part=localfrm&save_alert=%s" % (self.viewid,save_alert)
        if pk!='':
            url = "admin?viewid=%s&part=localfrm&pk=%s&save_alert=%s" % (self.viewid, pk,save_alert)

        return self.redirect(url)


    
    
    
        
 