# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2014
#      Author:  
# Start  Date:  2014/09/04
# Last modify:  2014/09/05
#
##############################################################################
from imp import reload
import admin.vi.BASE_TPL as BASE_TPL
reload(BASE_TPL)

class cfans(BASE_TPL.cBASE_TPL):
    
    def setClassName(self):
        #设定要实例的 BIZ类和TPL类，为空则继承基类，可以能过判断part的值来设置不同的类名
        self.dl_name = 'fans_dl'
        #self.inframe = 1

    def specialinit(self):
        self.navTitle = '粉丝管理'
        self.getBreadcrumb() #获取面包屑
        #self.isFile=1

    def goPartList(self):
        
        self.assign('NL',self.dl.GNL)
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)

        s = self.runApp('fanslist.html')
        return s
    
    def initPagiUrl(self):
        qqid = self.REQUEST.get('qqid','')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        return url
    

        
 