# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/D001_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import time , random

class cD001_dl(cBASE_DL):
    def init_data(self):
        

        self.GNL = ['编号','名称','类型','适用形式','适用商品','时间',
                    '总数量','剩余数量','状态']


    def mRight(self):
            
        sql = u"""
            select  c.id,
                c.cname ,
                c.type_str,
                c.apply_str,
                c.apply_goods_str,
                c.use_time_str,
                c.total,  
                c.total-c.remain_total,
                case when to_char(dateend,'YYYY-MM-DD')<to_char(now(),'YYYY-MM-DD') then '已过期' 
                when c.total-c.remain_total=0 then '已领完' else '正常' end
                from coupons c
                where COALESCE(c.del_flag,0)=0 and c.usr_id=%s
        """
        parm=[self.usr_id_p]
        self.qqid = self.GP('qqid','')
        self.pageNo=self.GP('pageNo','')
        if self.pageNo=='':
            self.pageNo='1'
        self.pageNo=int(self.pageNo)
        if self.qqid!='':
            sql+= "AND cname LIKE %s "
            parm.append('%%%s%%'%(self.qqid))

        sql+=" ORDER BY id DESC"

        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo,L=parm)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L#[1,2,3,4],[]#

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
            select
                id
                ,cname
                ,remark,
                total ,
                amount ,
                type_id,
                type_str,
                type_ext,
                apply_id,
                apply_str,
                apply_ext_num,
                apply_ext_money,
                apply_goods,
                apply_goods_str,
                apply_goods_id,
                use_time,
                use_time_str,
                datestart,
                dateend,
                validday,
                icons,
                pics,
                isshow
                from coupons
                where id=%s and usr_id =%s and COALESCE(del_flag,0)=0
        """
        if pk != '':
            L = self.db.fetch( sql,[pk,self.usr_id_p] )
        return L


    
    def local_add_save(self):

        pk = self.pk

        dR={'R':'','MSG':''}

        #获取表单参数

        cname = self.REQUEST.get('cname','')  #优惠券名称
        remark = self.REQUEST.get('remark','')  #优惠券备注
        total = self.REQUEST.get('total','')  #优惠券数量
        amount   = self.REQUEST.get('amount','')    #每人限领(张)
        type_id  = self.REQUEST.get('type_id','')  #优惠类型
        type_str = self.REQUEST.get('type_str', '')  # 优惠类型
        type_ext = self.REQUEST.get('type_ext', '')  # 积分或口令
        apply_id = self.REQUEST.get('apply_id', '')  # 适用形式
        apply_str = self.REQUEST.get('apply_str', '')  # 适用形式
        apply_ext_num = self.REQUEST.get('apply_ext_num', '')  # 满减/折扣
        apply_ext_money = self.REQUEST.get('apply_ext_money', '')  # 起用金额
        apply_goods = self.REQUEST.get('apply_goods', '')  # 适用商品
        apply_goods_str = self.REQUEST.get('apply_goods_str')  # 适用商品
        apply_goods_id = self.REQUEST.get('goods_id', '')  # 商品id
        #apply_goods_name = self.REQUEST.get('good_name', '')  # 商品名称
        use_time = self.REQUEST.get('use_time', '')  # 使用时间
        use_time_str = self.REQUEST.get('use_time_str', '')  # 使用时间
        datestart = self.REQUEST.get('datestart', '')  # 开始时间
        dateend = self.REQUEST.get('dateend', '')  # 结束时间
        validday = self.REQUEST.get('validday', '')  # 有效期
        icons = self.REQUEST.get('icons', '')  # 图标
        pics = self.REQUEST.get('pics', '')  # 图片
        isshow = self.REQUEST.get('isshow', '')  # 是否显示

        
        data = {
                'cname': cname ,
                'remark': remark,
            'total': total or None,
            'amount': amount or None,
                'type_id':type_id,
                'type_str': type_str,
                'type_ext':type_ext or None,
                'apply_id': apply_id,
                'apply_str': apply_str,
                'apply_ext_num':apply_ext_num or None,
                'apply_ext_money':apply_ext_money or None,
                'apply_goods':apply_goods,
                'apply_goods_str': apply_goods_str,
                'apply_goods_id': apply_goods_id or None,
                #'apply_goods_name': apply_goods_name,
                'use_time':use_time,
                'use_time_str':use_time_str,
                'datestart': datestart or None,
                'dateend': dateend or None,
                'validday': validday or None,
                'icons': icons,
                'pics': pics,
                'usr_id':self.usr_id_p,
                'isshow':isshow or None


        }
        cur_random_no = "%s%s" % (time.time(), random.random())
        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data['uid']=self.usr_id
            data['utime']=self.getToday(9)
            #data.pop('random')

            self.db.update('coupons' , data , " id = %s " % pk)
            self.use_log('修改优惠券%s' % pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            data['remain_total']=0
            data['random_no']=cur_random_no
            self.db.insert('coupons' , data)
            pk = self.db.fetchcolumn('select id from coupons where random_no=%s' ,cur_random_no)
            self.use_log('增加优惠券%s' % pk)
        dR['pk'] = pk
        
        return dR


    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update coupons set del_flag=1 where id= %s and usr_id=%s", [pk,self.usr_id_p])
        self.use_log('删除优惠券%s' % pk)
        return dR

    def check_ps_data(self):
        dR = {'code': '0', 'MSG': ''}
        cid =self.GP('cid','')
        sql="select id from coupons where type_ext=%s and usr_id=%s "
        l,t=self.db.select(sql,[cid,self.usr_id_p])
        if t>0:
            dR['code']=1
            dR['MSG']='口令不能与其它优惠券的口令重复，请修改口令！'
        return dR



