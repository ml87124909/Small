# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/H006.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL

class cH006(cBASE_TPL):
    
    def setClassName(self):
        #设定要实例的 dl类和TPL类，为空则继承基类，可以能过判断part的值来设置不同的类名
        '''
        if self.part == 'xxx':
            self.dl_name = 'xxx_dl'
        '''
        self.dl_name = 'H006_dl'
        self.inframe = 1
    def specialinit(self):
        pass

    def goPartList(self):

        self.getBreadcrumb()  # 获取面包屑
        self.assign('NL',self.dl.GNL)
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('H006_list.html')
        return s
    
    def initPagiUrl(self):
        parent_id = self.REQUEST.get('parent_id','')
        qqid = self.REQUEST.get('qqid','')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        if parent_id:
            url += "&parent_id=%s" % parent_id
        return url

    def goPartJS(self):
        usr_id = self.dl.GP('uid', '')
        sql = "update users set login_lock = 0 , login_lock_time = NULL where usr_id = %s"
        self.dl.db.query(sql,usr_id)
        return '1'



    

    
    
    
        
 