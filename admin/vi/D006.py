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
from basic.publicw import DEBUG

if DEBUG=='1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL

from admin.vi.mselect  import mselect_forM

class cD006(cBASE_TPL):

    def setClassName(self):

        self.dl_name = 'D006_dl'
        #self.inframe = 1


    def specialinit(self):
        self.navTitle = '发布投票'
        self.getBreadcrumb() #获取面包屑
        #self.isFile=1

    def goPartList(self):

        self.assign('NL',self.dl.GNL)
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        zszt = self.dl.GP('zszt','')
        istp = self.dl.GP('istp','')
        ft=self.dl.getmtcdata('RSXZT',zszt)
        self.assign('zszt',ft)
        self.assign('zsztval',zszt)
        s = self.runApp('D006_list.html')
        return s

    def initPagiUrl(self):
        zszt = self.REQUEST.get('zszt','')
        qqid = self.REQUEST.get('qqid','')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        if zszt:
            url += "&zszt=%s" % zszt
        return url

    def goPartLocalfrm(self):
        self.backurl = 'admin?viewid=D006'
        #self.need_editor = 1
        self.initHiddenLocal()#初始隐藏域

        self.getBackBtn()
        self.assign('NL',self.dl.GNL)
        item,itemlist = self.dl.get_local_data(self.pk)
        #明细对象
        self.assign('item',item)
        self.assign('itemlist',itemlist)

        QTYPE = self.dl.getmtcdata('QTYPE','','')
        self.assign('QTYPE',QTYPE)

        self.assign('Rmselect',self.Rt_mselect())

        s = self.runApp('D006_local.html')
        return s

    def Rt_mselect(self):
        mSelect = mselect_forM('rt',nl=[], title='商品选择',wh=[950, 350])
        mSelect.sUrl = 'admin?viewid=D006&part=ajax&action=getSelectItem'
        mSelect.nl =  ['货号','条码','商品名称','面值','零售价','类别编码','类别名称']

        # mSelect.setUrlArg({'jf_type': "$('[name=jf_type]:checked').val()"})
        mSelect.confirmjs = '''
                datas = sData.split("###");
                row = parseInt($("input[name=SelRow]").val())+1;
                var table= $("#matListTable");
                var tr = $(table.find('tr')[row]);
                var input_item_id = $(tr.find("input[name='item_id1']")[0]);
                var input_tm = $(tr.find("input[name='tm']")[0]);
                var input_itname = $(tr.find("input[name='itname']")[0]);
                var input_price = $(tr.find("input[name='price']")[0]);
                var input_ls_price = $(tr.find("input[name='ls_price']")[0]);
                var input_lb_code = $(tr.find("input[name='lb_code']")[0]);
                var input_td8 = $(tr.find("td")[8]);
                input_item_id.val(datas[0]);
                input_tm.val(datas[1]);
                input_itname.val(datas[2]);
                input_price.val(datas[3]);
                input_ls_price.val(datas[4]);
                input_lb_code.val(datas[5]);
                input_td8.html(datas[6]);
                '''
        return mSelect.getHTML()

    def goPartlotstop(self):
        L = self.dl.lotstop()
        return self.dl.json_encode(L)

    def goPartlotstar(self):
        L = self.dl.lotstar()
        return self.dl.json_encode(L)

