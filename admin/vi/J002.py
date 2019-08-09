# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/vi/J002.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL

class cJ002(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'J002_dl'
        self.inframe = 1
    def specialinit(self):
        pass

    def goPartList(self):

        self.assign('NL',self.dl.GNL)
        self.navTitle = '个人账号管理'
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()

        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('J002_list.html')
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
        self.navTitle = '角色授权'
        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()
        self.item = self.dl.get_local_data(self.pk)
        self.assign('item',self.item)
        L = self.dl.get_My_Roles(self.pk)
        R=[]
        for i in L:
            if i.get('t_can_see') == 1 or i.get('t_can_add') == 1 or i.get('t_can_del') == 1 or i.get('t_can_upd') == 1:
                R.append(i)

        self.assign('rolelist',R)
        s = self.runApp('J002_local.html')
        return s
    
    
    
        
 