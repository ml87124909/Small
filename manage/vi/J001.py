# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/vi/J001.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL


class cJ001(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'J001_dl'
        self.inframe = 1
    def specialinit(self):
        pass

    def goPartList(self):
       
        self.assign('NL',self.dl.GNL)
        self.navTitle = '人员管理'
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        
        s = self.runApp('J001_list.html')
        return s
    
    def initPagiUrl(self):
        lb_code = self.REQUEST.get('lb_code','')
        brand_id = self.REQUEST.get('brand_id','')
        status = self.REQUEST.get('status','')
        ctype = self.REQUEST.get('ctype','')
        qqid = self.REQUEST.get('qqid','')

        unit_sel_ids = self.REQUEST.get('unit_sel_ids','')
        off_sel_ids = self.REQUEST.get('off_sel_ids','')

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
        if unit_sel_ids:
            url +="&unit_sel_ids=%s"%unit_sel_ids
        if off_sel_ids:
            url +="&off_sel_ids=%s"%off_sel_ids
        
        return url
    
    def goPartLocalfrm(self):
        self.navTitle = '人员管理'

        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
       
        self.getBackBtn()
        
        #html = self.tpl.html_Localfrm()
        self.item = self.dl.get_local_data(self.pk)
        self.assign('item',self.item)
        mode = self.dl.GP('mode')
        self.assign('mode', mode)
        statuslist=self.dl.get_status()
        self.assign('statuslist',statuslist)
        
        s = self.runApp('J001_local.html')
        return s
		

    
    
    
        
 