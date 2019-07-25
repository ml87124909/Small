# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) janedao
# Author：hyj
# Start  Date:  2019
##############################################################################

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':    
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import hashlib , os , time , random

class cD002_dl(cBASE_DL):
    def init_data(self):
        self.GNL=['','积分规则设置','积分商品设置'] #列表表头



    #在子类中重新定义         
    def myInit(self):
        self.src = 'D002'
        self.part = self.GP('part','Localfrm')
        self.tab = self.GP("tab", "1")



    def get_local_data(self):
        """获取 local 表单的数据
        """
        L={}
        sql=""
        if str(self.tab)=='1':
            sql="""select vip_integral,integral,new_score
                    from  score_conf where usr_id=%s """

        # elif str(self.tab)=='2':
        #     sql='select cname,address,contact,wd,jd from  shopconfig where usr_id=%s'
        #
        # elif str(self.tab)=='3':
        #     sql='select use_money,close_time,cancel_id,send_id,evaluate_id,complete_id from order_set where usr_id=%s'
        #
        # elif str(self.tab)=='4':
        #     sql = 'select appid,secret,mchid,mchkey,base_url from mall where usr_id=%s'
        #
        # elif str(self.tab)=='5':
        #     sql="select vip_price,up_type,discount,up_type_str from member where usr_id=%s"
        #
        # elif str(self.tab)=='6':
        #     sql="""select home_goods,home_goods_str,home_goods_id,
        #                 shop_goods,shop_goods_str,shop_goods_id,
        #                 order_goods,order_goods_str,order_goods_id,
        #                 shop_cart_memo,menu_memo
        #             from global_config where usr_id=%s"""
        # else:
        #     sql="select vip_price,up_type,discount from member where usr_id=%s"
        # if str(self.tab)=='2':
        #     l,t= self.db.fetchall(sql,self.usr_id )
        #     if t>0:
        #         L=l
        # else:
        if sql!='':
            L = self.db.fetch(sql, self.usr_id_p)
        return L
    
    def local_add_save(self):

        dR={'code':'','MSG':'申请单 保存成功'}

        self.tab=self.GP('multab','')
        if str(self.tab)=='1':
            vip_integral=self.GP('vip_integral','')#会员购物返积分比例
            integral=self.GP('integral','')#非会员购物返积分比例
            new_score = self.GP('new_score', '')  # 新用户注册送多少积分

            # home_title=self.GP('home_title','')#店铺首页分享标题
            # home_pic=self.GP('home_pic',None)#店铺首页分享图
            # home_pic_link = self.GP('home_pic_link', '')  # 店铺首页分享图链接
            # phone = self.GP('phone', '')  # 客服电话
            # times = self.GP('times', '')  # 客服时间
            # gadds=self.GP('gadds','gadds')
            data={
                'vip_integral':vip_integral or None,
                'integral':integral or None,
                'new_score':new_score or None,
                # 'home_title':home_title,
                # 'home_pic':home_pic,
                # 'home_pic_link':home_pic_link,
                # 'gadds':gadds,
                # 'times':times,
                # 'phone':phone,
            }#score_conf
            l,t=self.db.select("select id from score_conf where usr_id=%s" ,self.usr_id_p)

            if t == 0:  # insert
                data['usr_id'] = self.usr_id_p
                data['cid']=self.usr_id
                data['ctime']=self.getToday(9)
                self.db.insert('score_conf', data)

            else:  # update

                data['uid']=self.usr_id
                data['utime']=self.getToday(9)
                self.db.update('score_conf', data, " id = %s " % l[0][0])
            self.save_score_set()

        if str(self.tab) == '2':
            lid = self.GP('lid')  # 商品id
            goods_id = self.GP('goods_id')  # 商品id
            good_name = self.GP('good_name')  # 商品名称
            score = self.GP('score', '')  # 所需积分
            amount = self.GP('amount', '')  # 限量多少件
            max_amount = self.GP('max_amount', '')  # 最大兑换数量
            #complete_id = self.GP('complete_id', '')  # 订单完成通知
            #if use_money==''
            data = {
                'goods_id': goods_id or None,
                'goods_name': good_name,
                'score': score or None,
                'amount': amount or None,
                'max_amount': max_amount or None,
                #'complete_id': complete_id,

            }  # order_set
            #l, t = self.db.select("select id from score_goods where usr_id=%s", self.usr_id)
            if lid=='':
            #if t == 0:  # insert
                data[ 'usr_id']=self.usr_id_p
                data['cid'] = self.usr_id
                data['ctime'] = self.getToday(9)
                self.db.insert('score_goods', data)


            else:  # update
                # 如果是插入 就去掉 uid，utime 的处理
                data['uid'] = self.usr_id
                data['utime'] = self.getToday(9)
                self.db.update('score_goods', data, " id = %s " % lid)


        # if str(self.tab) == '2':
        #     lid = self.REQUEST.getlist('lid')
        #     cname = self.REQUEST.getlist('cname')#商铺名称
        #     address = self.REQUEST.getlist('address')#商铺地址
        #     contact = self.REQUEST.getlist('contact')#商铺联系方式
        #     wd = self.REQUEST.getlist('wd')#商铺坐标纬度
        #     jd = self.REQUEST.getlist('jd')#商铺坐标经度
        #
        #     if len(cname) > 0:
        #         sql = "select id from shopconfig where usr_id=%s;"
        #         l, t = self.db.select(sql, self.usr_id)
        #         if t > 0:
        #             for j in l:
        #                 if str(j[0]) not in lid:
        #                     self.db.query("delete from  shopconfig where id=%s;", j[0])
        #         for i in range(len(cname)):
        #             if cname[i] != '':
        #                 if lid[i] == '':
        #                     sql = """
        #                     insert into shopconfig(usr_id,cname,address,contact,wd,jd,cid,ctime)
        #                         values(%s,%s,%s,%s,%s,%s,%s,now());
        #                     """
        #                     L = [self.usr_id, cname[i], address[i], contact[i], wd[i] or None, jd[i] or None, self.usr_id]
        #                     self.db.query(sql, L)
        #                 else:
        #                     sql = """
        #                     update shopconfig set cname=%s,address=%s,contact=%s,wd=%s,jd=%s,uid=%s,utime=now()
        #                             where id=%s
        #                     """
        #                     L = [cname[i], address[i], contact[i],wd[i] or None, jd[i] or None, self.usr_id, lid[i]]
        #                     self.db.query(sql, L)
        #     else:
        #         self.db.query("delete from  shopconfig where usr_id=%s;", self.usr_id)
        #
        #
        #
        # if str(self.tab) == '2':
        #     use_money = self.GP('use_money')  # 订单包邮金额(元)
        #     close_time = self.GP('close_time')  # 订单关闭时间(分钟)
        #     cancel_id = self.GP('cancel_id', '')  # 订单取消通知
        #     send_id = self.GP('send_id', '')  # 订单发货通知
        #     evaluate_id = self.GP('evaluate_id', '')  # 订单评价通知
        #     complete_id = self.GP('complete_id', '')  # 订单完成通知
        #     #if use_money==''
        #     data = {
        #         'use_money': use_money or None,
        #         'close_time': close_time or None,
        #         'cancel_id': cancel_id,
        #         'send_id': send_id,
        #         'evaluate_id': evaluate_id,
        #         'complete_id': complete_id,
        #
        #     }  # order_set
        #     l, t = self.db.select("select id from score_goods where usr_id=%s", self.usr_id)
        #
        #     if t == 0:  # insert
        #         data[ 'usr_id']=self.usr_id
        #         data['cid'] = self.usr_id
        #         data['ctime'] = self.getToday(9)
        #         self.db.insert('order_set', data)
        #         oid=self.db.fetchcolumn("select id from order_set where usr_id=%s", self.usr_id)
        #
        #     else:  # update
        #         # 如果是插入 就去掉 uid，utime 的处理
        #         oid=l[0][0]
        #         data['uid'] = self.usr_id
        #         data['utime'] = self.getToday(9)
        #         self.db.update('order_set', data, " id = %s " % oid)
        #     self.save_logistics_way(oid)

        # if str(self.tab) == '4':
        #
        #     appid = self.GP('appid', '')  # 小程序appid
        #     secret = self.GP('secret', '')  # 小程序secret
        #     mchid = self.GP('mchid', '')  # 微信支付商户号
        #     mchkey = self.GP('mchkey', '')  # 微信支付秘钥
        #     certificate = self.GP('certificate', '')  # 微信支付证书
        #     base_url = self.GP('base_url', '')  # 微信支付回调域名
        #
        #     data = {
        #         'appid': appid,
        #         'secret': secret,
        #         'mchid': mchid,
        #         'mchkey': mchkey,
        #         #'certificate': certificate,
        #         'base_url':base_url
        #     }  # mall
        #     l, t = self.db.select("select id from mall where usr_id=%s", self.usr_id)
        #
        #     if t == 0:  # insert
        #         # 如果是更新，就去掉cid，ctime 的处理.
        #         data['usr_id'] = self.usr_id
        #         data['cid'] = self.usr_id
        #         data['ctime'] = self.getToday(9)
        #         self.db.insert('mall', data)
        #
        #     else:  # update
        #         # 如果是插入 就去掉 uid，utime 的处理
        #
        #         data['uid'] = self.usr_id
        #         data['utime'] = self.getToday(9)
        #         self.db.update('mall', data, " id = %s " % l[0][0])
        #     self.oMALL.update(self.usr_id)
        #
        # if str(self.tab) == '5':
        #     vip_price = self.GP('vip_price', '')  # 年费会员价格
        #     up_type = self.GP('up_type', '')  # 会员升级方式
        #     discount = self.GP('discount', '')  # 会员折扣百分比
        #     up_type_str = self.GP('up_type_str', '')  # 会员升级方式
        #     # evaluate_id = self.GP('evaluate_id', '')  # 订单评价通知
        #     # complete_id = self.GP('complete_id', '')  # 订单完成通知
        #     data = {
        #         'vip_price': vip_price or None,
        #         'up_type': up_type,
        #         'discount': discount or None,
        #         'up_type_str': up_type_str,
        #         # 'evaluate_id': evaluate_id,
        #         # 'complete_id': complete_id
        #     }  # member
        #     l, t = self.db.select("select id,up_type from member where usr_id=%s", self.usr_id)
        #
        #     if t == 0:  # insert
        #         data['usr_id'] = self.usr_id
        #         data['cid'] = self.usr_id
        #         data['ctime'] = self.getToday(9)
        #         self.db.insert('member', data)
        #         oid=self.db.fetchcolumn("select id from member where usr_id=%s", self.usr_id)
        #
        #     else:  # update
        #
        #         oid=l[0][0]
        #         data['uid'] = self.usr_id
        #         data['utime'] = self.getToday(9)
        #         self.db.update('member', data, " id = %s " % oid)
        #         if str(up_type)!=str(l[0][1]):
        #             sqlu="""
        #                 select id,cname,usr_level_str  from wechat_mall_user where usr_id=%s
        #             """
        #             U,ui=self.db.select(sqlu,self.usr_id)
        #             if ui>0:
        #                 for u in U:
        #                     sqlc="""insert into wechat_user_change_log(
        #                     wechat_user_id,name,old_level,new_level,up_type_str,ctime,end_time,up_mode_str,memo,cid,usr_id)values(
        #                     %s,%s,%s,%s,'系统变更',now(),null,'手动','注:变更会员升级方式',%s,%s)
        #                     """
        #                     self.db.query(sqlc,[u[0],u[1],u[2],'无',self.usr_id,self.usr_id])
        #
        #             sqlstr="""
        #                 update wechat_mall_user set usr_level=0,usr_level_str='无',hy_flag=0,
        #                 hy_ctime=null,hy_etime=null where usr_id=%s
        #             """
        #             self.db.query(sqlstr,self.usr_id)
        #     if str(up_type)=='2':
        #         self.save_hy_up_level(oid)
        #
        # if str(self.tab) == '6':
        #     home_goods = self.GP('home_goods', '')  # 首页推荐商品设置
        #     home_goods_str = self.GP('home_goods_str', '')  # 首页推荐商品设置
        #     home_goods_id = self.GP('goods_id', '')  # 首页推荐指定商品（多）
        #     shop_goods = self.GP('shop_goods', '')  # 购物车推荐商品设置
        #     shop_goods_str = self.GP('shop_goods_str', '')  # 购物车推荐商品设置
        #     shop_goods_id = self.GP('goods_ids', '')  # 购物车推荐指定商品（多）
        #     order_goods = self.GP('order_goods', '')  # 订单页推荐商品设置
        #     order_goods_str = self.GP('order_goods_str', '')  # 订单页推荐商品设置
        #     order_goods_id = self.GP('order_goods_id', '')  # 订单页推荐指定商品（多）
        #     menu_memo = self.GP('menu_memo', '')  # 菜单页面搜索关键词设置（多）
        #     shop_cart_memo = self.GP('shop_cart_memo', '')  # 购物车页信息设置（多）
        #     data = {
        #         'home_goods': home_goods or None,
        #         'home_goods_str': home_goods_str,
        #         'home_goods_id': home_goods_id,
        #         'shop_goods': shop_goods or None,
        #         'shop_goods_str': shop_goods_str,
        #         'shop_goods_id': shop_goods_id,
        #         'order_goods':order_goods,
        #         'order_goods_str':order_goods_str,
        #         'order_goods_id':order_goods_id,
        #         'shop_cart_memo':shop_cart_memo,
        #         'menu_memo':menu_memo,
        #
        #     }  # global_config
        #     l, t = self.db.select("select id from global_config where usr_id=%s", self.usr_id)
        #
        #     if t == 0:  # insert
        #         data['usr_id'] = self.usr_id
        #         data['cid'] = self.usr_id
        #         data['ctime'] = self.getToday(9)
        #         self.db.insert('global_config', data)
        #         oid = self.db.fetchcolumn("select id from global_config where usr_id=%s", self.usr_id)
        #
        #     else:  # update
        #         oid = l[0][0]
        #         data['uid'] = self.usr_id
        #         data['utime'] = self.getToday(9)
        #         self.db.update('global_config', data, " id = %s " % oid)
        #     # self.save_global_memo(oid)
        #     # pass
        #     #home_goods,home_goods_str,home_goods_id,
        #             #     shop_goods,shop_goods_str,shop_goods_id
        #             # from global_config where usr_id=%s"""
        # if str(self.tab) == '7':
        #     pass
        #self.oSHOP.update(self.usr_id)

        dR['code'] = 0
        return dR


    def save_score_set(self):
        lid=self.REQUEST.getlist('lid')
        days = self.REQUEST.getlist('days')
        score = self.REQUEST.getlist('score')

        if len(days)>0:
            sql="select id from score_set where usr_id=%s;"
            l,t=self.db.select(sql,self.usr_id_p)
            if t>0:
                for j in l:
                    if str(j[0]) not in lid:
                        self.db.query("delete from  score_set where id=%s and usr_id=%s;",[j[0],self.usr_id_p])
            for i in range(len(days)):
                if days[i]!='':
                    if lid[i]=='':
                        sql="""
                        insert into score_set(usr_id,days,score,cid,ctime)
                            values(%s,%s,%s,%s,now());
                        """
                        L=[self.usr_id_p,days[i],score[i],self.usr_id]
                        self.db.query(sql,L)
                    else:
                        sql="""
                        update score_set set days=%s,score=%s,uid=%s,utime=now()
                                where id=%s
                        """
                        L=[days[i],score[i],self.usr_id,lid[i]]
                        self.db.query(sql, L)
        else:
            self.db.query("delete from  score_set where usr_id=%s;", self.usr_id_p)
        return

    def save_global_memo(self,oid):
        lid = self.REQUEST.getlist('lid')
        memo = self.REQUEST.getlist('memo')
        if len(memo) > 0:
            sql = "select id from global_memo where m_id=%s and usr_id=%s;"
            l, t = self.db.select(sql, [oid, self.usr_id_p])
            if t > 0:
                for j in l:
                    if str(j[0]) not in lid:
                        self.db.query("delete from  global_memo where id=%s and usr_id=%s;",[j[0],self.usr_id_p])
            for i in range(len(memo)):
                if memo[i] != '':
                    if lid[i] == '':
                        sql = """
                                insert into global_memo(m_id,usr_id,memo,cid,ctime)
                                    values(%s,%s,%s,%s,now());
                                """
                        L = [oid, self.usr_id_p, memo[i],self.usr_id]
                        self.db.query(sql, L)
                    else:
                        sql = """
                                update global_memo set memo=%s,uid=%s,utime=now()
                                        where id=%s
                                """
                        L = [memo[i], self.usr_id, lid[i]]
                        self.db.query(sql, L)
        else:
            self.db.query("delete from  global_memo where usr_id=%s;", self.usr_id_p)
        return


    def get_score_set(self):
        L=[]
        sql="""
            select id,days,score from score_set where usr_id=%s
        """
        l,n=self.db.fetchall(sql,self.usr_id_p)
        if n>0:
            L=l
        return L

    def get_score_goods(self):
        L=[]
        sql=" select id,goods_id,goods_name,score,amount,max_amount,'' as sn,status_str from score_goods where usr_id =%s "
        l,n=self.db.select(sql,self.usr_id_p)
        if n>0:
            L=l
        return L

    # def delete_data(self):
    #     pk = self.pk
    #     dR = {'R':'', 'MSG':''}
    #     self.db.query("update shopname set del_flag=1 where id= %s" % pk)
    #     return dR