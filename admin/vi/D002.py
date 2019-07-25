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



class cD002(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'D002_dl'
        self.inframe = 1
    def specialinit(self):
        self.tab_data = ['积分规则设置','积分商品设置']
        self.assign('tab_data', self.tab_data)
        self.assign('tab', self.dl.tab)
        BTNS=''
        if str(self.dl.tab)=='1':
            BTNS='<input type="submit" class="btn btn-success span2" name="add_save" value="保存积分规则设置"/>'
        elif str(self.dl.tab)=='2':
            BTNS='<input type="submit" class="btn btn-success span2" name="add_save" value="保存积分商品"/>'
        # elif str(self.dl.tab)=='3':
        #     BTNS='保存订单设置'
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
        s = self.runApp('D002_list.html')
        return s
    

    
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
        if self.dl.tab=='1':
            self.assign('detail',self.dl.get_score_set())
        if self.dl.tab=='2':
            self.assign('detail',self.dl.get_score_goods())
        # if self.dl.tab=='5':
        #     self.assign('detail',self.dl.get_hy_up_level())
        # if self.dl.tab=='6':
        #     self.assign('detail',self.dl.get_global_memo())

        self.assign('save_alert',self.dl.GP('save_alert','0'))
        self.assign('jf_mselect', self.Goods_mselect())
        self.assign('show_Goods', self.Goods_mselect_mul())
        self.assign('show_Goods_id', self.Goods_mselect_mul_id())
        self.assign('order_Goods_id', self.Goods_mselect_mul_id_s())
        s = self.runApp('D002_local.html')
        return s

    def goPartInsert(self):
        dR = self.dl.local_add_save()
        res = dR.get('code','')

        if res==0:
            save_alert = 1
        else:
            save_alert = 2

        url = "admin?viewid=%s&part=localfrm&save_alert=%s" % (self.viewid,save_alert)
        if self.dl.tab:
            url = "admin?viewid=%s&part=localfrm&tab=%s&save_alert=%s" % (self.viewid, self.dl.tab,save_alert)

        return self.redirect(url)








    
    
        
 