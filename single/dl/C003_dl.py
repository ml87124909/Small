# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/C003_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cC003_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['','品牌ID','品牌排序','品牌名称','品牌图标','热门品牌']


    def mRight(self):
            
        sql = u"""
            select id,sort,cname,pic_icon,case when hot=0 then '否' else '是' end
            from brand 
            where COALESCE(del_flag,0)=0 and usr_id=%s
        """%self.usr_id_p

        sql+=" ORDER BY sort "
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L


    def save_brand(self):#保存品牌

        url = self.GPRQ("url", '')
        cname = self.GP("cname", '')
        sort = self.GP("sort", '')
        hot = self.GP("hot", '')
        status = self.GP("status", '')
        dR = {'code': '', 'MSG': ''}

        try:

            sql = "insert into brand(usr_id,cname,sort,pic_icon,hot,status,cid,ctime)values(%s,%s,%s,%s,%s,%s,%s,now())"
            self.db.query(sql, [self.usr_id_p,cname, sort,url,hot,status, self.usr_id])
            # self.oGOODS_D.update()
            # self.oGOODS.update()
            # self.oGOODS_N.update()
            self.use_log('增加商品品牌')
            dR['code'] = '0'
            dR['MSG'] = '增加商品品牌成功'
            return dR
        except:
            dR['code'] = '1'
            dR['MSG'] = '增加商品品牌失败'
            return dR


    def edit_brand(self):#修改品牌
        url = self.GPRQ("url", '')
        cname = self.GP("cname", '')
        sort = self.GP("sort", '')
        hot = self.GP("hot", '')
        status = self.GP("status", '')
        id = self.GP("id", '')

        dR = {'code': '', 'MSG': ''}

        try:
            dR['MSG'] = '修改商品品牌成功'
            sql = "update brand set pic_icon=%s,cname=%s,sort=%s,hot=%s,status=%s,uid=%s,utime=now() where id=%s "
            self.db.query(sql, [url, cname, sort, hot,status,self.usr_id, id])
            # self.oGOODS_D.update()
            # self.oGOODS.update()
            # self.oGOODS_N.update()
            self.use_log('修改商品品牌%s' % id)
            dR['code'] = '0'
            return dR
        except:
            dR['MSG'] = '修改商品品牌失败'
            dR['code'] = '1'
            return dR

    def ajax_delete_data(self):
        pk = self.pk
        dR = {'code':'', 'MSG':''}
        self.db.query("update brand set del_flag=1,uid=%s,utime=now() where id= %s", [self.usr_id,pk])
        # self.oGOODS_D.update()
        # self.oGOODS.update()
        # self.oGOODS_N.update()
        self.use_log('删除商品品牌%s' % pk)
        dR['MSG'] = '删除商品品牌成功！'
        return dR


    def ajax_update_data(self):
        id = self.GP('pk','')
        dR = {'code': '', 'MSG': ''}
        data=self.db.fetch("select id,pic_icon,cname,sort,hot,status from  brand where id= %s" ,id)
        if data:
            dR['data'] = data
            dR['code'] = '0'
        return dR




