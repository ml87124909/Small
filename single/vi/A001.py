# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/A001.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL


class cA001(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'A001_dl'

    def specialinit(self):
        self.tab_data = ['OSS存储设置','店铺信息', '商铺设置','订单设置', '小程序设置',
                         '会员设置','全局设置','积分规则设置','充值设置','快递鸟设置']
        self.assign('tab_data', self.tab_data)
        self.assign('tab', self.dl.tab)
        BTNS=''
        if str(self.dl.tab)=='1':
            BTNS='保存存储设置'
        elif str(self.dl.tab)=='2':
            BTNS='保存店铺信息'
        elif str(self.dl.tab)=='3':
            BTNS='保存商铺设置'
        elif str(self.dl.tab)=='4':
            BTNS='保存订单设置'
        elif str(self.dl.tab)=='5':
            BTNS='保存小程序设置'
        elif str(self.dl.tab)=='6':
            BTNS='保存会员设置'
        elif str(self.dl.tab)=='7':
            BTNS='保存全局设置'
        elif str(self.dl.tab)=='8':
            BTNS='保存积分规则设置'
        elif str(self.dl.tab)=='9':
            BTNS='保存充值设置'
        elif str(self.dl.tab)=='10':
            BTNS='保存快递鸟设置'
        self.assign('BTNS', BTNS)

    def goPartList(self):

        self.assign('NL',self.dl.GNL)
        self.navTitle = '店铺信息'
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        return self.runApp('A001_list.html')
    

    
    def goPartLocalfrm(self):
        self.navTitle = ''
        self.currentUrl = self.sUrl + "&part=localfrm"
        self.assign('currentUrl', self.currentUrl)
        self.need_editor = 1
        self.getBreadcrumb() #获取面包屑
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()

        self.item = self.dl.get_local_data()
        self.assign('item', self.item)
        if self.dl.tab=='4':
            self.assign('detail',self.dl.get_logistics_way())
        elif self.dl.tab=='6':
            self.assign('detail',self.dl.get_hy_up_level())
        # elif self.dl.tab=='7':
        #     self.assign('detail',self.dl.get_global_memo())
        elif self.dl.tab=='8':
            self.assign('detail',self.dl.get_score_set())
        elif self.dl.tab=='9':
            self.assign('detail',self.dl.get_gifts())

        self.assign('show_ticket', self.show_ticket())
        self.assign('show_Goods', self.Goods_mselect_mul())
        self.assign('show_Goods_id', self.Goods_mselect_mul_id())
        self.assign('order_Goods_id', self.Goods_mselect_mul_id_s())
        return self.runApp('A001_local.html')










    
    
        
 