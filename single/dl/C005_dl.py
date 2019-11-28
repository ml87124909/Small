# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/C005_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import time , random

class cC005_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['', '用户', '评论', '评分', '商品', '时间', '图片']


    def mRight(self):
            
        sql = u"""
            select id
                ,usr_name
                ,goods_reputation  --评论
                ,goods_star   --评分
                ,goods  --商品
                ,to_char(ctime,'YYYY-MM-DD HH24:MI')
                ,(select  array_agg(row_to_json(row(pic))) 
                from images_api where images_api.usr_id=r.usr_id and images_api.goodsid=r.order_detail_id) as pics
                from reputation_list r
                where COALESCE(del_flag,0)=0 and usr_id=%s
        """%self.usr_id_p

        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
            select usr_name
                   ,user_avatar
                   ,goods_id
                   ,goods
                   ,goods_star
                   ,star_id
                   ,goods_reputation
                   ,goods_reply
                   ,to_char(ctime,'YYYY-MM-DD HH24:MI')ctime
                    ,(select  array_agg(row_to_json(row(pic))) 
                from images_api where images_api.usr_id=r.usr_id and images_api.goodsid=r.order_detail_id) as pics
            from reputation_list r
            where  COALESCE(del_flag,0)=0 and usr_id=%s and id=%s

        """
        if pk != '':
            L = self.db.fetch(sql,[self.usr_id_p,pk])

        return L
    
    def local_add_save(self):

        pk = self.pk
        dR={'code':'','MSG':''}

        #获取表单参数
        usr_name=self.GP('usr_name','')#用户名字
        user_avatar=self.GP('user_avatar','')#用户头像
        goods_id = self.GP('goods_id', '')  # 商品
        goods = self.GP('good_name', '')  # 商品名称
        goods_reputation=self.GP('goods_reputation')#评论
        goods_star=self.GP('goods_star','')#评分
        star_id = self.GP('star_id', '')  # 是否vip
        goods_reply=self.GP('goods_reply','')#回复
        ctime = self.GP('ctime', '')  # 添加时间
        if ctime=='':
            ctime=self.getToday(6)

        data = {
                'usr_name':usr_name
                ,'user_avatar':user_avatar
                , 'goods_id': goods_id
                , 'goods': goods
                ,'goods_reputation':goods_reputation
                ,'goods_star': goods_star
                ,'star_id':star_id
                ,'goods_reply':goods_reply
                ,'usr_id':self.usr_id_p
                , 'ctime': ctime or None
        }

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data['uid']=self.usr_id
            data['utime']=self.getToday(6)
            self.db.update('reputation_list' , data , " id = %s " % pk)
            self.use_log('修改商品评价%s' % pk)
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data['cid']=self.usr_id
            cur_random_no = "%s%s" % (time.time(), random.random())
            data['random_no']=cur_random_no

            self.db.insert('reputation_list' , data)
            pk = self.db.fetchcolumn('select id from reputation_list where random_no=%s', cur_random_no)
            self.use_log('增加商品评价%s' % pk)

        dR['pk'] = pk
        dR['code']='0'
        return dR

    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update reputation_list set del_flag=1 where id= %s and usr_id=%s", [pk,self.usr_id_p])
        self.use_log('删除商品评价%s' % pk)
        return dR

