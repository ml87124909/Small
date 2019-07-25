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

class cD004(cBASE_TPL):
    
    def setClassName(self):
        
        self.dl_name = 'D004_dl'
        #self.inframe = 1
        

    def specialinit(self):
        self.navTitle = '抢购管理'
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
        s = self.runApp('D004_list.html')
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
        self.backurl = 'admin?viewid=D004'
        self.need_editor = 1
        self.initHiddenLocal()#初始隐藏域
        #self.getUploadHtml()
        self.getBackBtn()
        self.assign('NL',self.dl.GNL)
        item,itemlist = self.dl.get_local_data(self.pk)
        #明细对象
        self.assign('item',item)
        self.assign('itemlist',itemlist)
        
        self.assign('Rmselect',self.Rt_mselect())

        s = self.runApp('D004_local.html')
        return s

    def Rt_mselect(self):
        mSelect = mselect_forM('rt',nl=[], title='商品选择',wh=[950, 350])
        mSelect.sUrl = 'admin?viewid=D004&part=ajax&action=getSelectItem'
        mSelect.nl =  ['ID','商品名称','会员价']
        
        # mSelect.setUrlArg({'jf_type': "$('[name=jf_type]:checked').val()"})
        mSelect.confirmjs = '''
                datas = sData.split("###");
                row = parseInt($("input[name=SelRow]").val())+1;
                var table= $("#matListTable");
                var tr = $(table.find('tr')[row]);
                var input_item_id = $(tr.find("input[name='gid']")[0]);
                var input_itname = $(tr.find("input[name='itname']")[0]);
                var input_price = $(tr.find("input[name='price']")[0]);
                input_item_id.val(datas[0]);
                input_itname.val(datas[1]);
                input_price.val(datas[2]);
                '''
        return mSelect.getHTML()
    
    def goPartlotstop(self):
        L = self.dl.lotstop()
        return self.dl.json_encode(L)

    def goPartlotstar(self):
        L = self.dl.lotstar()
        return self.dl.json_encode(L)
           
 