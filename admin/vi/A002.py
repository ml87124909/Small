# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/A002.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL
from admin.vi.mselect  import mselect_forJF_type,mselect_forHT,mselect_forYK

class cA002(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'A002_dl'


    def initPagiUrl(self):
        qqid = self.REQUEST.get('qqid','')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        return url

    def goPartList(self):
        self.getBreadcrumb()  # 获取面包屑
        self.assign('NL',self.dl.GNL)
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        banner=self.dl.banner_data()
        self.assign('banner', banner)
        s = self.runApp('A002_list.html')
        return s
    
    def goPartLocalfrm(self):
        self.navTitle = ''

        self.initHiddenLocal()#初始隐藏域
        self.getBreadcrumb()  # 获取面包屑
        self.getBackBtn()
        self.assign('jf_mselect',self.JF_mselect())
        item = self.dl.get_local_data()
        self.assign('item',item)
        self.assign('pic_type',self.dl.pic_type())
        s = self.runApp('A002_local.html')
        return s

    def JF_mselect(self):
        mSelect = mselect_forYK('jf', ['ID', '商品名称'], '商品列表',
                                wh=[500, 300], dnl=[0, 1, 2, 3], search_holder='请输入商品名称')
        mSelect.sUrl = 'admin?viewid=A002&part=ajax&action=jftype'
        # mSelect.setUrlArg({'jf_type': "$('[name=jf_type]:checked').val()"})
        mSelect.confirmjs = '''
                datas = sData.split("###");
                $('input[name="business_id"]').val(datas[0]);
                $('input[name="good_name"]').val(datas[1]);

                '''
        mSelect.clearjs = '''
                $('input[name="business_id"]').val('');
                $('input[name=good_name]').val('');

                '''
        return mSelect.getHTML()

    def goPartAjax_update(self):
        dR=self.dl.ajax_update()
        return self.jsons(dR)

    # def goPartInsert(self):
    #     dR = self.dl.local_add_save()
    #     res = dR.get('code','')
    #     pk = dR.get('pk', '')
    #     if res==0:
    #         save_alert = 1
    #     else:
    #         save_alert = 2
    #
    #     url = "admin?viewid=%s&part=localfrm&save_alert=%s" % (self.viewid,save_alert)
    #     if pk!='':
    #         url = "admin?viewid=%s&part=localfrm&pk=%s&save_alert=%s" % (self.viewid, pk,save_alert)
    #
    #     return self.redirect(url)

    def goPartSave_type(self):#增加广告类型
        dR=self.dl.save_type()
        return self.jsons(dR)

    def goPartSave_type_u(self):#修改广告类型
        dR=self.dl.save_type_data()
        return self.jsons(dR)

    # def goPartSave_ctype(self):#增加广告类型
    #     dR=self.dl.save_ctype()
    #     return self.jsons(dR)




    