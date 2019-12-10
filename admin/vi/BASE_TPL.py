# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/BASE_TPL.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.VIEWS
    reload(admin.vi.VIEWS)
from admin.vi.VIEWS             import cVIEWS
from admin.vi.mselect import mselect_forGoods_Info, mselect_forGoods_Infos, mselect_forMList, mselect_forMList_mul, \
    mselect_forMList_spec

class cBASE_TPL(cVIEWS):

    def goPartUpload(self):
        url = self.dl.Upload()
        return self.jsons({'url': url})

    def goPartPem_upload(self):
        url = self.dl.Pem_upload()
        return self.jsons({'url': url})

    def goPartSave_type(self):#增加广告类型
        dR=self.dl.save_type()
        return self.jsons(dR)

    def goPartSave_ctype(self):#增加广告类型
        dR=self.dl.save_ctype()
        return self.jsons(dR)

    def goPartDel_qiniu_pic(self):#删除七牛照片
        dR=self.dl.del_qiniu_pic()
        return self.jsons(dR)

    def Goods_mselect(self):
        mSelect = mselect_forGoods_Info('Goods', ['ID', '商品名称'], '商品列表',
                                wh=[500, 300], dnl=[0, 1, 2, 3], search_holder='请输入商品名称')
        mSelect.sUrl = 'admin?viewid=home&part=ajax&action=goods'
        mSelect.confirmjs = '''
                datas = sData.split("###");
                $('input[name="goods_id"]').val(datas[0]);
                $('input[name="good_name"]').val(datas[1]);
                '''
        mSelect.clearjs = '''
                $('input[name="goods_id"]').val('');
                $('input[name=good_name]').val('');
                '''
        return mSelect.getHTML()

    def Goods_mselect_mul(self):
        ##明细表材料选择
        nL = ['货号', '条码', '名称', '规格', '单位', '进价', '零售价', '会员价', '批发价', '库存']
        dnl = [0, 1, 2, 3, 4, 5, 6, 15, 14, 13]
        TmSelect=mselect_forMList('TmSelect',viewid=self.viewid,nl=nL,wh=[900, 400],title='选择商品',dnl=dnl,canjp='')
        TmSelect.sUrl = 'admin?viewid=home&part=ajax&action=getGoods'
        TmSelect.confirmjs = '''
        if(sData != ''){
            $('input[name="goods_id"]').val(sData);
            
        }
        else{
            alert("您没有选择商品!");
        }
        '''
        TmSelect.clearjs = '''
                        $('input[name="goods_id"]').val('');
                       
                        '''
        return TmSelect.getHTML()

    def Goods_mselect_mul_id(self):#自定方法
        ##明细表材料选择
        nL = ['货号', '条码', '名称', '规格', '单位', '进价', '零售价', '会员价', '批发价', '库存']
        dnl = [0, 1, 2, 3, 4, 5, 6, 15, 14, 13]
        TmSelect=mselect_forMList_mul('TmSelect_mul',viewid=self.viewid,nl=nL,wh=[900, 400],title='选择商品',dnl=dnl,canjp='')
        TmSelect.sUrl = 'admin?viewid=home&part=ajax&action=getGoods'
        TmSelect.confirmjs = '''
        if(sData != ''){
            $('input[name="goods_ids"]').val(sData);
        }
        else{
            alert("您没有选择商品!");
        }
        '''
        TmSelect.clearjs = '''
                        $('input[name="goods_ids"]').val('');
                       
                        '''
        return TmSelect.getHTML()

    def Goods_mselect_mul_id_s(self):  # 自定方法
        ##明细表材料选择
        nL = ['货号', '条码', '名称', '规格', '单位', '进价', '零售价', '会员价', '批发价', '库存']
        dnl = [0, 1, 2, 3, 4, 5, 6, 15, 14, 13]
        TmSelect = mselect_forMList_mul('TmSelect_mul_s', viewid=self.viewid, nl=nL, wh=[900, 400], title='选择商品', dnl=dnl,
                                        canjp='')
        TmSelect.sUrl = 'admin?viewid=home&part=ajax&action=getGoods'
        TmSelect.confirmjs = '''
        if(sData != ''){
            $('input[name="order_goods_id"]').val(sData);
        }
        else{
            alert("您没有选择商品!");
        }
        '''
        TmSelect.clearjs = '''
                        $('input[name="order_goods_id"]').val('');

                        '''
        return TmSelect.getHTML()

    def show_ticket(self):
        mSelect = mselect_forGoods_Info('Ticket', ['ID', '优惠券名称','类型','适用形式','备注'], '优惠券选择',
                                wh=[500, 300], dnl=[0, 1, 2, 3,4], search_holder='请输入优惠券名称')
        mSelect.sUrl = 'admin?viewid=home&part=ajax&action=ticket'

        mSelect.btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList('')">选择优惠券</button>''' %'Ticket'
        mSelect.confirmjs = '''
                datas = sData.split("###");
                $('input[name="return_ticket"]').val(datas[0]);
                $('input[name="return_ticket_str"]').val(datas[1]);
                '''
        mSelect.clearjs = '''
                $('input[name="return_ticket"]').val('');
                $('input[name=return_ticket_str]').val('');
                '''
        return mSelect.getHTML()

    def Goods_mselects(self):
        mSelect = mselect_forGoods_Infos('Goods', ['ID', '商品名称'], '拼团商品列表',
                                         wh=[500, 300], dnl=[0, 1, 2, 3], search_holder='请输入商品名称')
        mSelect.sUrl = 'admin?viewid=home&part=ajax&action=pt_goods'
        mSelect.confirmjs = '''
                datas = sData.split("###");
                $('input[name="goods_id"]').val(datas[0]);
                $('input[name="good_name"]').val(datas[1]);
                '''
        mSelect.clearjs = '''
                $('input[name="goods_id"]').val('');
                $('input[name=good_name]').val('');
                '''
        return mSelect.getHTML()

    def Spec_mselect_child(self):  # 自定方法
        ##明细表材料选择
        nL = ['货号', '条码', '名称', '规格', '单位', '进价', '零售价', '会员价', '批发价', '库存']
        dnl = [0, 1, 2, 3, 4, 5, 6, 15, 14, 13]
        TmSelect = mselect_forMList_spec('spec_mul', viewid=self.viewid, nl=nL, wh=[900, 400], title='选择规格型号', dnl=dnl,
                                         canjp='')
        TmSelect.sUrl = 'admin?viewid=C004&part=ajax&action=getSpecChild'
        TmSelect.confirmjs = '''
        if(sData != ''){
            
            spec_types=$('input[name=spec_type]').val();
            spec_child_vs=$('input[name="spec_child'+spec_types+'"]').val()
            //$('input[name="spec_child'+spec_type+'"]').val(sData);
            $.ajax({
                url:"admin?viewid=C004&part=set_spec_child&sid="+spec_types+"&spec_cids="+sData,
                type:"post",
                async:false,
                success:function(data){
                    if (data.code=='0'){
                        
                        $('#pb'+spec_types+'').append(data.data)
                        if (spec_child_vs==''){
                            $('input[name=spec_child'+data.sid+']').val(data.ids)
                        }else{
                            spec_child_vs+=','+data.ids
                            $('input[name=spec_child'+data.sid+']').val(spec_child_vs)
                        }
                        show_spec();


                    }else{
                        layer.msg(data.MSG);
                    }
                }
            });
            f_clearCheckedspec_mul()
        }
        else{
            alert("您没有选择商品!");
        }
        '''
        TmSelect.clearjs = '''
                        $('input[name="goods_ids"]').val('');

                        '''
        return TmSelect.getHTML()

    def Hot_mselects(self):
        mSelect = mselect_forGoods_Infos('Goods', ['ID', '商品名称'], '商品列表',
                                         wh=[500, 300], dnl=[0, 1, 2, 3], search_holder='请输入商品名称')
        mSelect.sUrl = 'admin?viewid=C006&part=ajax&action=hot_goods'
        mSelect.confirmjs = '''
                datas = sData.split("###");
                $('input[name="goods_id"]').val(datas[0]);
                $('input[name="good_name"]').val(datas[1]);
                '''
        mSelect.clearjs = '''
                $('input[name="goods_id"]').val('');
                $('input[name=good_name]').val('');
                '''
        return mSelect.getHTML()
