# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/C006_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cC006_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['', '排序ID', '商品ID','商品名称','添加时间']  # 列表表头



    def mRight(self):

        sql = u"""
            select id,sort,gid,gname,to_char(ctime,'YYYY-MM-DD HH24:MI') 
                from hot_sell where coalesce(del_flag,0)=0  and usr_id=%s order by sort
        """ % self.usr_id_p


        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L


    
    def local_add_save(self):

        dR = {'code': '', 'MSG': '保存成功'}

        id = self.GP('id', '')  # 商品id
        goods_id = self.GP('goods_id', '')  # 商品id
        good_name = self.GP('good_name', '')  # 商品名称
        sort = self.GP('sort', '')  # 排序

        data = {
            'gid': goods_id,
            'gname': good_name,
            'sort': sort,
        }  # pt_conf

        if str(id) == '':  # insert
            data['usr_id'] = self.usr_id_p
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            self.db.insert('hot_sell', data)
            self.use_log('增加商品热销榜')

        else:  #update
            data['uid'] = self.usr_id
            data['utime'] = self.getToday(9)
            self.db.update('hot_sell', data, " id = %s " % (id))
            self.use_log('修改商品热销榜%s' % id)
        self.oGOODS_H.update(self.usr_id_p)

        dR['code'] = 0
        return dR


    def ajax_update_data(self):
        pk = self.pk
        dR = {'code': '', 'MSG': ''}

        sql = """select id,gid,gname,sort
                from  hot_sell     
                where id=%s
                        """
        d = self.db.fetch(sql, [pk])

        if str(d.get('id', '')) != pk:
            dR['code'] = '1'
            return dR
        dR['code'] = '0'
        dR['data'] = d

        return dR



    def ajax_del_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update hot_sell set del_flag=1 where id= %s" % pk)
        self.oPT_GOODS.update(pk)
        self.use_log('删除商品热销榜%s' % pk)
        dR['MSG']='删除成功'
        return dR

