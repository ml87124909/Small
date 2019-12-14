# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/home_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import time
import random
from basic.pay import WeixinPay


class chome_dl(cBASE_DL):

    def get_wx_users(self):#用户数量
        sql="select count(id) from wechat_mall_user where usr_id=%s and coalesce(del_flag,0)=0"
        t=self.db.fetchcolumn(sql,self.usr_id_p)
        return t

    def get_goods_info(self):#商品数量
        sql="select count(id) from goods_info where usr_id=%s and coalesce(del_flag,0)=0"
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_all(self):#订单总数
        sql="select count(id) from wechat_mall_order where usr_id=%s and coalesce(del_flag,0)=0"
        t=self.db.fetchcolumn(sql,self.usr_id_p)
        return t

    def get_today_order(self):# 今日销售额
        sql="""
            select coalesce(round(sum(new_total)::numeric,2),0) from wechat_mall_order 
            where usr_id=%s and coalesce(del_flag,0)=0 
            and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')
            and status>1 and status<=10
        
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_today_views(self):# 今日浏览量
        sql="""
            select count(id) from view_history where usr_id=%s 
            and coalesce(del_flag,0)=0 and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')
        """
        t=self.db.fetchcolumn(sql,self.usr_id_p)
        return t

    def get_order_2(self):# 未发货订单
        sql="""select count(id) from wechat_mall_order 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=2
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_base_me(self):#基本信息(小程序信息等)
        sql="""
            
             select to_char(u.ctime,'YYYY-MM-DD')ctime,
                to_char(u.expire_time,'YYYY-MM-DD')expire_time,coalesce(u.with_flag,0)with_flag,
                convert_from(decrypt(m.appid::bytea, %s, 'aes'),'SQL_ASCII')appid,
                convert_from(decrypt(m.secret::bytea, %s, 'aes'),'SQL_ASCII')secret,
                
                 coalesce(u.vip_flag,0)vip_flag,
                 coalesce(u.oss_all,100) as oss_all,
                 coalesce(u.oss_flag,0)oss_flag,
                coalesce(coalesce(u.oss_all,100)-coalesce(u.oss_now,0),0) as oss_now,coalesce(qiniu_flag,0)qiniu_flag
            
            from users u
            left join mall m on m.usr_id=u.usr_id 
            where u.usr_id=%s
        """
        t=self.db.fetch(sql,[self.md5code,self.md5code,self.usr_id_p])

        return t

    def get_goods_sell(self):#出售中
        sql="""select count(id) from goods_info 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=0"""
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_sold_out(self):# 已下架
        sql = """select count(id) from goods_info 
            where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=1
            """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_score_warn(self):# 库存预警(库存小于5件)
        sql="""select count(id) from goods_info 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=0 and coalesce(stores,0)<=5
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_evaluation(self):# 商品评价
        sql="select count(id) from reputation_list where usr_id=%s and coalesce(del_flag,0)=0"
        t=self.db.fetchcolumn(sql,self.usr_id_p)
        return t

    def get_feedback(self):
        sql="select count(id) from feedback where usr_id=%s and coalesce(del_flag,0)=0"
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_drawal_audit(self): # 提现审核
        sql="select count(id) from withdraw_cash where usr_id=%s and  coalesce(status,0)=1 "
        t=self.db.fetchcolumn(sql,self.usr_id_p)
        return t

    def get_order_status_1(self):# 待付款
        sql="""select count(id) from wechat_mall_order 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=1
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_10(self):# 拼团中
        sql="""select count(id) from wechat_mall_order 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=10
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_7(self):#已完成
        sql = """select count(id) from wechat_mall_order 
                where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=7
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_4(self):# 待自提
        sql="""
            select count(id) from wechat_mall_order 
                where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=7
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_5(self):# 待收货
        sql = """
        select count(id) from wechat_mall_order 
            where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=5
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_99(self):# 退款中
        sql = """
       select count(id) from refund_money 
       where usr_id=%s and  coalesce(status,0)=99  and coalesce(del_flag,0)=0
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_89(self):# 未发货订单
        sql = """
        select count(id) from order_exchange 
        where usr_id=%s and  coalesce(status,0)=89  and coalesce(del_flag,0)=0
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_yesterday_a(self):#昨日销量
        sql = """
        select count(id)amount,coalesce(round(sum(new_total)::numeric,2),0)total 
        from wechat_mall_order  
        where to_char(ctime,'YYYY-MM-DD')=to_char('YESTERDAY'::date,'YYYY-MM-DD') and usr_id=%s
        and status>1 and status<=7
                """
        t = self.db.fetch(sql, self.usr_id_p)
        return t

    def get_this_month(self):# 本月销量
        sql = """
        select count(id)amount,coalesce(round(sum(new_total)::numeric,2),0)total 
        from wechat_mall_order  
        where to_char(ctime,'YYYY-MM')=to_char('YESTERDAY'::date,'YYYY-MM') and usr_id=%s 
        and status>1 and status<=7
                """
        t = self.db.fetch(sql, self.usr_id_p)
        return t



    def set_sync_data(self):
        dR={'code':'1','MSG':''}
        if str(self.usr_id)==1:
            dR['MSG'] = '管理员不能同步数据了'
            return dR

        if str(self.usr_id)!=str(self.usr_id_p):
            dR['MSG'] = '子帐号不能同步数据'
            return dR

        #写入小程序数据
        appid = self.GP('appid', '')  # 小程序appid
        secret = self.GP('secret', '')  # 小程序secret
        data={}
        lT,iN=self.db.select("select id from mall where appid=%s",[appid])
        if iN>0:
            dR['MSG'] = '您填写的信息已存在，无法进行导入数据操作！'
            return dR
        ll, tt = self.db.select("select usr_id from users where usr_id=%s and coalesce(with_flag ,0)=0", self.usr_id)
        if tt==0:
            dR['MSG'] = '您已同步过数据了'
            return dR

        l, t = self.db.select("select id from mall where usr_id=%s", self.usr_id)
        if t==0:
            data['usr_id'] = self.usr_id
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            self.db.insert('mall', data)
            sqlu = """
               update mall set appid=encrypt(%s,%s,'aes'),secret=encrypt(%s,%s,'aes'),
               mchid=encrypt(%s,%s,'aes'),mchkey=encrypt(%s,%s,'aes')   where usr_id=%s
               """
            Lu = [appid, self.md5code, secret, self.md5code, '', self.md5code, '', self.md5code, self.usr_id_p]
            self.db.query(sqlu, Lu)
        else:
            sqlu = """
               update mall set appid=encrypt(%s,%s,'aes'),secret=encrypt(%s,%s,'aes'),
               mchid=encrypt(%s,%s,'aes'),mchkey=encrypt(%s,%s,'aes')   where usr_id=%s
               """
            Lu = [appid, self.md5code, secret, self.md5code, '', self.md5code, '', self.md5code, self.usr_id_p]
            self.db.query(sqlu, Lu)

        syncid = 1
        #self.sync_data_1(syncid)
        #self.sync_data_2(syncid)
        #self.sync_data_3(syncid)
        #self.sync_data_4(syncid)
        #self.sync_data_5(syncid)
        self.sync_data_6(syncid)
        #self.sync_data_7(syncid)
        #self.sync_data_8(syncid)
        self.sync_data_9(syncid)
        #self.sync_data_10(syncid)
        #self.sync_data_11(syncid)

        #self.sync_data_12()

        self.oSHOP.update(self.usr_id)
        self.oSHOP_T.update(self.usr_id)
        self.oUSER.update(self.usr_id)
        self.oOPENID.update(self.usr_id)
        self.oMALL.update(self.usr_id)
        #self.oQINIU.update(self.usr_id)
        #self.oKUAIDI.update(self.usr_id)
        self.oGOODS.update(self.usr_id)
        self.oGOODS_D.update(self.usr_id)
        self.oORDER_SET.update(self.usr_id)
        self.oGOODS_N.update(self.usr_id)
        self.oGOODS_G.update(self.usr_id)
        self.oCATEGORY.update(self.usr_id)

        dR['MSG'] = '同步数据成功'
        dR['code'] = '0'
        self.db.query("update users set with_flag=1 where usr_id=%s",self.usr_id)
        return dR



    def sync_data_1(self,syncid):#A001 1

        sql="""select cname,gadds,logo_pic,logo_pic_link,home_title,home_pic,home_pic_link,phone,times
                    from  shopinfo where usr_id=%s """
        l,t=self.db.select(sql,[syncid])
        if t>0:
            cname, gadds, logo_pic, logo_pic_link, home_title, home_pic, home_pic_link, phone, times=l[0]
            data = {
                'cname': cname,
                'logo_pic_link': logo_pic_link,
                'home_title': home_title,
                'home_pic_link': home_pic_link,
                'gadds': gadds,
                'times': times,
                'phone': phone,
            }  # shopinfo

            sql = """select id from  shopinfo where usr_id=%s """
            ll, tt = self.db.select(sql,self.usr_id)
            if tt==0:
                data['usr_id'] = self.usr_id
                data['cid'] = 0
                data['ctime'] = self.getToday(9)
                self.db.insert('shopinfo', data)
            else:
                data['uid'] = self.usr_id
                data['ctime'] = self.getToday(9)
                self.db.update('shopinfo', data,'usr_id=%s'%self.usr_id)

        return


    def sync_data_2(self,syncid):#A001 2

        sql='select cname,address,contact,wd,jd from  shopconfig where usr_id=%s'
        l, t = self.db.select(sql,[syncid])
        if t > 0:
            self.db.query("delete from shopconfig where usr_id=%s and usr_id!=1" ,self.usr_id)
            for i in l:
                cname, address, contact, wd, jd=i
                sql = """
                insert into shopconfig(usr_id,cname,address,contact,wd,jd,cid,ctime)
                    values(%s,%s,%s,%s,%s,%s,0,now());
                """
                L = [self.usr_id, cname, address, contact, wd or None, jd or None]
                self.db.query(sql, L)

        return

    def sync_data_3(self,syncid):  # A001 3

        sql="""select use_money,close_time,cancel_id,send_id,evaluate_id,complete_id,take_day 
            from order_set where usr_id=%s"""
        l, t = self.db.select(sql,[syncid])
        if t > 0:
            use_money, close_time, cancel_id, send_id, evaluate_id, complete_id, take_day=l[0]
            data = {
                'use_money': use_money or None,
                'close_time': close_time or None,
                'take_day': take_day

            }  # order_set
            sql = """select id 
                        from order_set where usr_id=%s"""
            ll, tt = self.db.select(sql,self.usr_id)
            if tt==0:
                data['usr_id'] = self.usr_id
                data['cid'] = 0
                data['ctime'] = self.getToday(9)
                self.db.insert('order_set', data)
                oid = self.db.fetchcolumn("select id from order_set where usr_id=%s", self.usr_id)
            else:
                oid = self.db.fetchcolumn("select id from order_set where usr_id=%s", self.usr_id)
            sql="""
            
                select c_id,cname,status,is_mail,counts,piece,only_money,
                add_piece,add_money,is_default from logistics_way where usr_id=%s
            """
            ll,tt=self.db.select(sql,[syncid])
            if tt>0:
                self.db.query("delete from logistics_way where usr_id=%s and usr_id!=1", self.usr_id)
                for i in ll:
                    c_id, cname, status, is_mail, counts, piece, only_money,add_piece, add_money, is_default=i
                    sqli = """
                           insert into logistics_way(m_id,usr_id,c_id,cname,status,is_mail,counts,piece,only_money,
                           add_piece,add_money,is_default,ctime)
                               values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now());
                           """
                    L = [oid, self.usr_id, c_id, cname, status or None, is_mail or None, counts or None,
                         piece or None, only_money or None, add_piece or None, add_money or None, is_default or None]
                    self.db.query(sqli, L)

        return

    def sync_data_4(self,syncid):  # A001 5

        sql = "select vip_price,up_type,discount,up_type_str,vip_sale from member where usr_id=%s"
        l, t = self.db.select(sql,[syncid])
        if t > 0:
            vip_price, up_type, discount, up_type_str, vip_sale = l[0]
            data = {
                'vip_price': vip_price or None,
                'up_type': up_type,
                'discount': discount or None,
                'up_type_str': up_type_str,
                'vip_sale': vip_sale or None,

            }
            sql = "select id from member where usr_id=%s"
            lT1, iN1 = self.db.select(sql, self.usr_id)

            if iN1 == 0:
                data['usr_id'] = self.usr_id
                data['cid'] = 0
                data['ctime'] = self.getToday(9)
                self.db.insert('member', data)

            else:
                data['uid'] = 0
                data['utime'] = self.getToday(9)
                self.db.update('member', data,'usr_id=%s'%self.usr_id)
        oid = self.db.fetchcolumn("select id from member where usr_id=%s", self.usr_id)

        ll,tt=self.db.select("select cname,up_price,level_discount from hy_up_level where usr_id=%s",[syncid])
        if tt>0:
            self.db.query("delete from hy_up_level where usr_id=%s and usr_id!=1", self.usr_id)
            for i in ll:
                cname, up_price, level_discount=i
                sql = """
                    insert into hy_up_level(m_id,usr_id,cname,up_price,level_discount,ctime)
                        values(%s,%s,%s,%s,%s,now());
                    """
                L = [oid, self.usr_id, cname, up_price, level_discount]
                self.db.query(sql, L)

        return

    def sync_data_5(self,syncid):  # A001 6
        sql = """select home_goods,home_goods_str,home_goods_id,
                      shop_goods,shop_goods_str,shop_goods_id,
                      order_goods,order_goods_str,order_goods_id,
                      shop_cart_memo,menu_memo 
                  from global_config where usr_id=%s"""
        l, t = self.db.select(sql,[syncid])
        if t > 0:
            home_goods, home_goods_str, home_goods_id, shop_goods, shop_goods_str, shop_goods_id, \
            order_goods, order_goods_str, order_goods_id, shop_cart_memo, menu_memo = l[0]
            data = {
                'home_goods': home_goods or None,
                'home_goods_str': home_goods_str,
                'home_goods_id': home_goods_id,
                'shop_goods': shop_goods or None,
                'shop_goods_str': shop_goods_str,
                'shop_goods_id': shop_goods_id,
                'order_goods': order_goods,
                'order_goods_str': order_goods_str,
                'order_goods_id': order_goods_id,
                'shop_cart_memo': shop_cart_memo,
                'menu_memo': menu_memo,

            }

            sql = """select id  from global_config where usr_id=%s"""
            ll,tt = self.db.select(sql,self.usr_id)
            if tt==0:
                data['usr_id'] = self.usr_id
                data['cid'] = 0
                data['ctime'] = self.getToday(9)
                self.db.insert('global_config', data)
            else:

                data['uid'] = 0
                data['utime'] = self.getToday(9)
                self.db.update('global_config', data,'usr_id=%s'%self.usr_id)



        return

    def sync_data_6(self,syncid):  # C001
        sql="select id,ctype,field,cname,COALESCE(sort,0) from advertis where usr_id=%s and COALESCE(del_flag,0)=0"
        l,t=self.db.select(sql,[syncid])
        if t>0:
            self.db.query("delete from advertis where usr_id=%s and usr_id!=1", self.usr_id)
            self.db.query("delete from banner where usr_id=%s and usr_id!=1", self.usr_id)
            for i in l:
                aid,ctype, field, cname, sort=i
                cur_random_no = "%s%s" % (time.time(), random.random())
                sql = "insert into advertis(usr_id,ctype,field,cname,sort,ctime,random_no)values(%s,%s,%s,%s,%s,now(),%s)"
                self.db.query(sql, [self.usr_id, ctype, field, cname, sort,cur_random_no])
                pk = self.db.fetchcolumn('select id from advertis where random_no=%s', cur_random_no)


                sqll = """
                   SELECT D.business_id,D.title,D.good_name,
                        D.status,D.remark,D.link_url,D.pic_url,D.remark
                    FROM banner D
                    where  D.usr_id=%s and COALESCE(D.del_flag,0)=0 and ctype=%s
                       """
                ll,tt=self.db.select(sqll,[syncid,aid])
                if tt>0:

                    for j in ll:
                        business_id,title,good_name,status,remark,link_url,pic_url,remark=j
                        data = {'title': title,
                                'business_id': business_id or None,
                                'good_name': good_name,
                                'link_url': link_url,
                                'ctype': pk or None,
                               # 'type_str': type_str,
                                'status': status or None,
                                #'status_str': status_str,
                                'pic_url': pic_url,
                                'remark': remark,
                                }
                        data['usr_id'] = self.usr_id
                        data['cid'] = 0
                        data['ctime'] = self.getToday(9)
                        self.db.insert('banner', data)

        return

    def sync_data_7(self,syncid):  # D001

        sql = """
           select id,cname,type,pid,pic_icon,pic_imgs,paixu,remark,ilevel 
           from category where usr_id=%s and COALESCE(del_flag,0)=0
           """
        l,t = self.db.select(sql,[syncid])
        if t>0:
            self.db.query("delete from category where usr_id=%s and usr_id!=1", self.usr_id)
            for i in l:
                cpid,name, type, pid, pic_icon, pic_imgs, paixu, remark,level=i
                data = {
                    'name': name
                    , 'type': type
                    , 'pid': pid
                    , 'cp_id': cpid
                    , 'pic_icon': pic_icon
                    , 'pic_imgs': pic_imgs
                    , 'paixu': int(paixu)
                    , 'ctime': self.getToday(9)
                    , 'usr_id': self.usr_id
                    , 'level': level
                    , 'remark': remark
                }
                self.db.insert('category', data)
            sql = """
               select id,cp_id 
               from category where usr_id=%s and COALESCE(del_flag,0)=0 and ilevel=1
               """
            ll, tt = self.db.select(sql,self.usr_id)
            for j in ll:
                did, cp_id=j
                self.db.query("update category set pid=%s  where usr_id=%s and pid=%s ",[did,self.usr_id,cp_id])

        return

    def sync_data_8(self,syncid):  # D002
        sql = """
            select id,cname,ctype,cicon,sort from spec  where  usr_id=%s and COALESCE(del_flag,0)=0
                """
        l,t=self.db.select(sql)
        if t>0:
            self.db.query("delete from spec where usr_id=%s and usr_id!=1", self.usr_id)
            for i in l:
                cp_id,cname, ctype, cicon, sort=i
                sql = "insert into spec(usr_id,ctype,cicon,cname,sort,ctime,cp_id)values(%s,%s,%s,%s,%s,now(),%s)"
                self.db.query(sql, [self.usr_id, ctype, cicon, cname, sort or None, cp_id])

            sql="""
            select spec_id,ctype_c,cicon_c,cname_c,sort_c from spec_child where usr_id=%s
            """
            ll,tt=self.db.select(sql,[syncid])
            if tt>0:
                self.db.query("delete from spec_child where usr_id=%s and usr_id!=1", self.usr_id)
                for j in ll:
                    spec_id, ctype_c, cicon_c, cname_c, sort_c=j
                    sql = """insert into spec_child(usr_id,spec_id,ctype_c,cicon_c,cname_c,sort_c,ctime,cp_id)
                    values(%s,%s,%s,%s,%s,%s,now(),%s)"""
                    self.db.query(sql, [self.usr_id, spec_id, ctype_c, cicon_c, cname_c, sort_c or None, spec_id])
            sql = """
                select id,cp_id from spec where usr_id=%s
                """
            lT, iN = self.db.select(sql,self.usr_id)
            if iN>0:
                for m in lT:
                    did, cp_id=m
                    sql="update spec_child set spec_id=%s  where usr_id=%s and cp_id=%s "
                    self.db.query(sql, [did, self.usr_id, cp_id])


        return


    def sync_data_9(self,syncid):  # D003
        sql="""
             SELECT  D.id,D.cname,D.introduce,D.recomm,D.status,D.category_ids,
                D.category_ids_str,D.video,D.contents,D.originalprice,D.minprice,D.stores,D.barcodes,D.logisticsid,
                D.limited,D.discount,D.share_type_str,D.share_type,D.share_time_str,D.share_time,
                D.share_title,D.share_imgs,D.share_return,D.return_ticket,D.return_ticket_str,D.paixu,D.weight,D.pic
            FROM goods_info D
           where  usr_id=%s and COALESCE(D.del_flag,0)=0
       
        """
        l,t=self.db.select(sql,[syncid])
        if t>0:
            self.db.query("delete from goods_info where usr_id=%s and usr_id!=1", self.usr_id)
            for i in l:
                cpid, name, introduce, recomm,status,category_ids,\
                category_ids_str, video, content, originalprice, minprice, stores, barcodes, logisticsid,\
                limited, discount, share_type_str, share_type, share_time_str, share_time,\
                share_title, share_imgs, share_return, return_ticket, return_ticket_str, paixu, weight,pic=i
                data = {
                    'cname': name,
                    'introduce': introduce,
                    #'recommstr': recommstr,
                    'recomm': recomm or None,
                    #'statusstr': statusstr,
                    'status': status  or None,

                    'video': video,
                    'contents': content,
                    'originalprice': originalprice  or None,
                    'minprice': minprice  or None,
                    'stores': stores  or None,
                    'limited': limited  or None,
                    'discount': discount  or None,
                    'share_type': share_type  or None,
                    'share_type_str': share_type_str,
                    'share_title': share_title,
                    'share_imgs': share_imgs,
                    'copy_id':cpid,
                    'paixu': paixu or None,
                    'weight': weight or None,
                    'barcodes': barcodes,
                    'pic':pic
                }

                if str(share_type) != '0':
                    data['share_time_str'] = share_time_str
                    data['share_time'] = share_time  or None
                    if str(share_type) == '3':
                        data['share_return'] = None
                        data['return_ticket'] = return_ticket  or None
                        data['return_ticket_str'] = return_ticket_str
                    else:
                        data['share_return'] = share_return  or None
                        data['return_ticket'] = None
                        data['return_ticket_str'] = return_ticket_str
                else:
                    data['share_time_str'] = ''
                    data['share_time'] = None
                    data['share_return'] = None
                    data['return_ticket'] = None


                data['usr_id'] = self.usr_id
                data['cid'] = 0
                data['ctime'] = self.getToday(9)
                self.db.insert('goods_info', data)
            sqll=" SELECT id,copy_id from goods_info where usr_id = %s "
            ll,tt=self.db.select(sqll,self.usr_id)
            if tt>0:
                self.db.query("delete from goods_pics where usr_id=%s and usr_id!=1", self.usr_id)
                for j in ll:
                    did, copy_id=j

                    sqlp="select pic from goods_pics where  usr_id=%s and goods_id=%s"
                    lT,iN=self.db.select(sqlp,[syncid,copy_id])
                    if iN>0:
                        for n in lT:
                            pic=n[0]
                            sql = "insert into goods_pics(usr_id,goods_id,pic,ctime)values(%s,%s,%s,now())"
                            LL=[self.usr_id, did, pic]
                            self.db.query(sql,LL)
                    # sqli="""
                    #     select  dis_id,dis_name,dis_level_discount  from alone_discount where usr_id=%s and goods_id=%s
                    # """
                    # lT1,iN1=self.db.select(sqli,[syncid,copy_id])
                    # if iN1>0:
                    #     self.db.query("delete from alone_discount where usr_id=%s and usr_id!=1", self.usr_id)
                    #     for m in lT1:
                    #         dis_id, dis_name, dis_level_discount=m
                    #         sql = """ insert into alone_discount(usr_id,goods_id,dis_id,dis_name,
                    #                 dis_level_discount,ctime)values (%s,%s,%s,%s,%s,now())
                    #                     """
                    #         LLL=[self.usr_id, did, dis_id, dis_name, dis_level_discount]
                    #         self.db.query(sql,LLL)


        return

    def sync_data_10(self,syncid):  # E001
        sql = """
            select
                cname
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
            where usr_id =%s and COALESCE(del_flag,0)=0
            """

        l,t = self.db.select(sql,[syncid])
        if t>0:
            self.db.query("delete from coupons where usr_id=%s", self.usr_id)
            for i in l:
                cname, remark,total,amount,type_id,type_str,type_ext,apply_id,apply_str,apply_ext_num,\
                apply_ext_money,apply_goods,apply_goods_str,apply_goods_id,use_time,use_time_str,\
                datestart,dateend,validday,icons,pics,isshow=i

                data = {
                    'cname': cname,
                    'remark': remark,
                    'total': total,
                    'amount': amount,
                    'type_id': type_id,
                    'type_str': type_str,
                    'type_ext': type_ext or None,
                    'apply_id': apply_id,
                    'apply_str': apply_str,
                    'apply_ext_num': apply_ext_num or None,
                    'apply_ext_money': apply_ext_money or None,
                    'apply_goods': apply_goods,
                    'apply_goods_str': apply_goods_str,
                    'apply_goods_id': apply_goods_id or None,
                    'use_time': use_time,
                    'use_time_str': use_time_str,
                    'datestart': datestart or None,
                    'dateend': dateend,
                    'validday': validday or None,
                    'icons': icons,
                    'pics': pics,
                    'usr_id': self.usr_id,
                    'isshow': isshow or None

                }

                data['cid'] = 0
                data['ctime'] = self.getToday(9)
                data['remain_total'] = 0
                self.db.insert('coupons', data)

        return

    def sync_data_11(self,syncid):  # E002


        sql="""
            select vip_integral,integral,new_score from  score_conf where usr_id=%s
        """
        l,t=self.db.select(sql,[syncid])
        if t>0:
            self.db.query("delete from score_conf where usr_id=%s and usr_id!=1", self.usr_id)
            vip_integral, integral, new_score=l[0]

            data = {
                'vip_integral': vip_integral or None,
                'integral': integral or None,
                'new_score': new_score or None,

            }  # score_conf
            data['usr_id'] = self.usr_id
            data['cid'] = 0
            data['ctime'] = self.getToday(9)
            self.db.insert('score_conf', data)

        sql="""
            select days,score from score_set where usr_id=%s
        """
        l,t=self.db.select(sql,[syncid])

        if t>0:
            self.db.query("delete from score_set where usr_id=%s and usr_id!=1", self.usr_id)
            for i in l:
                days, score=i

                sql = """
                insert into score_set(usr_id,days,score,cid,ctime)
                    values(%s,%s,%s,%s,now());
                """
                L = [self.usr_id, days, score, self.usr_id]
                self.db.query(sql, L)


        return

    def sync_data_12(self):  # G001

        sql="""
        select max_cash,mini_cash,arrive,topup,topup_str,drawal,drawal_str 
        from topup_set where usr_id = 1
        """
        l,t=self.db.select(sql)
        if t>0:

            max_cash, mini_cash, arrive, topup, topup_str, drawal, drawal_str=l[0]
            data = {
                'arrive': arrive or None,
                'mini_cash': mini_cash,
                'topup': topup or None,
                'topup_str': topup_str,
                'drawal': drawal or None,
                'drawal_str': drawal_str
            }
            sql = """
                    select id  from topup_set where usr_id = %s
                    """
            ll, tt = self.db.select(sql,self.usr_id)
            if tt==0:
                data['usr_id'] = self.usr_id
                data['cid'] = 0
                data['ctime'] = self.getToday(9)
                self.db.insert('topup_set', data)
            else:
                data['uid'] = 0
                data['utime'] = self.getToday(9)
                self.db.update('topup_set', data,'usr_id=%s'%self.usr_id)

        sql="""
            select add_money,giving from gifts where usr_id=1
        """
        l,t=self.db.select(sql)
        if t>0:
            self.db.query("delete from gifts where usr_id=%s and usr_id!=1", self.usr_id)
            for i in l:
                add_money, giving=i
                sql = """
                   insert into gifts(usr_id,add_money,giving,cid,ctime)
                       values(%s,%s,%s,%s,now());
                   """
                L = [self.usr_id, add_money or None, giving or None, self.usr_id]
                self.db.query(sql, L)

        return

    def cache_data(self):
        dR={'code':'1','MSG':''}
        id = self.GP('id', '')  # 用户id
        go= self.GP('go', '')  # 取那个缓存
        if self.usr_id!=1:
            dR['data'] = '请不要乱搞！'
            return dR
        try:
            id =int(id)
        except:
            dR['data'] = '请不要乱搞！'
            return dR

        if go == 'oSHOP':
            dR['data'] = self.oSHOP.get(id)
            return dR
        elif go == 'oUSER':
            dR['data'] = self.oUSER.get(id)
            return dR
        elif go == 'oMALL':
            dR['data'] = self.oMALL.get(id)
            return dR
        elif go == 'oQINIU':
            dR['data'] = self.oQINIU.get(id)
            return dR
        # elif go == 'oKUAIDI':
        #     dR['data'] = self.oKUAIDI.get(id)
        #     return dR
        elif go == 'oGOODS':
            dR['data'] = self.oGOODS.get(id)
            return dR
        elif go == 'oGOODS_D':
            dR['data'] = self.oGOODS_D.get(id)
            return dR
        elif go == 'oORDER_SET':
            dR['data'] = self.oORDER_SET.get(id)
            return dR
        elif go == 'oGOODS_N':
            dR['data'] = self.oGOODS_N.get(id)
            return dR
        elif go == 'oGOODS_G':
            dR['data'] = self.oGOODS_G.get(id)
            return dR
        elif go == 'oOPENID':
            dR['data'] = self.oOPENID.get(id)
            return dR
        elif go == 'oSHOP_T':
            dR['data'] = self.oSHOP_T.get(id)
            return dR
        elif go == 'oGOODS_PT':
            dR['data'] = self.oGOODS_PT.get(id)
            return dR
        elif go == 'oCATEGORY':
            dR['data'] = self.oCATEGORY.get(id)
            return dR
        elif go == 'oGOODS_SELL':
            dR['data'] = self.oGOODS_SELL.get(id)
            return dR
        elif go == 'oTOLL':
            dR['data'] = self.oTOLL.get()
            return dR
        elif go == 'oGOODS_DPT':
            dR['data'] = self.oGOODS_DPT.get(id)
            return dR
        elif go == 'oPT_GOODS':
            dR['data'] = self.oPT_GOODS.get(id)
            return dR
        else:
            dR['data'] = '请不要乱搞！'
            return dR

    def vip_db_data(self):
        dR = {'code': '1'}
        sql = """
              select 
            combo_one_name,
            combo_one_price,
            combo_one_day,
            combo_two_name,
            combo_two_price,
            combo_two_day,
            coalesce(combo_two_status,0),
            combo_thr_name,
            combo_thr_price,
            combo_thr_day,
            coalesce(combo_thr_status,0),
            combo_one_txt,
            combo_two_txt,
            combo_thr_txt
        from toll_config 
        
        """
        l, t = self.db.select(sql)
        if t == 0:
            return dR
        one_name, one_price, one_day, two_name, two_price, two_day, two_status, thr_name, thr_price, thr_day, thr_status, one_txt, two_txt, thr_txt = \
        l[0]
        if one_name == '':
            return dR
        data = [{
            'name': one_name,
            'price': one_price,
            'day': one_day,
            'txt': one_txt,
            'id': 1

        }]
        if two_status == 1:
            data.append({
                'name': two_name,
                'price': two_price,
                'day': two_day,
                'txt': two_txt,
                'id': 2
            })
        if thr_status == 1:
            data.append({
                'name': thr_name,
                'price': thr_price,
                'day': thr_day,
                'txt': thr_txt,
                'id': 3
            })

        dR['code'] = '0'
        dR['data'] = data
        return dR

    def buy_vip_data(self):
        dR = {'code': '1', 'MSG': ''}
        vip_flag = self.GP('vip_flag', '')  #
        try:
            if vip_flag == '2':
                sql = "select  combo_two_name,combo_two_price,combo_two_day from toll_config where coalesce(combo_two_status,0)=1"
                l, t = self.db.select(sql)
                if t == 0:
                    dR['MSG'] = '您所要购买的套餐不存在,请重新选择购买'
                    return dR
                dR['code'] = '0'
            elif vip_flag == '3':
                sql = "select  combo_thr_name,combo_thr_price,combo_thr_day from toll_config where coalesce(combo_thr_status,0)=1"
                l, t = self.db.select(sql)
                if t == 0:
                    dR['MSG'] = '您所要购买的套餐不存在,请重新选择购买'
                    return dR
                dR['code'] = '0'
            else:
                sql = "select  combo_one_name,combo_one_price,combo_one_day from toll_config "
                l, t = self.db.select(sql)
                dR['code'] = '0'
            name, price, day = l[0]
            # 如果你是 Python 3的用户，使用默认的字符串即可

            data = {
                'ctype': vip_flag,
                'cname': name,
                'price': price,
                'days': day,
            }

            sql = """select ctype from pingtai_paylog 
                where coalesce(pay_status,0)=1 and usr_id=%s and ctype in (1,2,3) order by id desc limit 1;"""
            lT1, iN1 = self.db.select(sql, [self.usr_id])
            if iN1 > 0:
                ctype=lT1[0][0]
                if str(vip_flag) !=str(ctype):
                    dR['MSG'] = '您上一次购买的套餐与现在有冲突，请联系管理员'
                    return dR
                    # sqlr = "select role_id from usr_role where usr_id=%s"
                    # lr, tr = self.db.select(sqlr, [self.usr_id])
                    # if tr == 1:
                    #     role_id = lr[0][0]  # role_id 2基础，3营销
                    #     if str(vip_flag) == '1' and role_id != 2:  # 基础
                    #         self.db.query("update usr_role set role_id=2 where id=%s", [urid])
                    #     elif str(vip_flag) == '2' and role_id != 3:  # 营销
                    #         self.db.query("update usr_role set role_id=3 where id=%s", [urid])
                    #     elif str(vip_flag) == 3:  # 未知
                    #         pass


            sql = "select id,out_trade_no from pingtai_paylog where coalesce(pay_status,0)=0 and usr_id=%s and ctype=%s"
            lT, iN = self.db.select(sql, [self.usr_id,vip_flag])
            if iN == 0:
                timeStamp = time.time()
                timeArray = time.localtime(timeStamp)
                danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
                romcode = str(time.time()).split('.')[-1]  # [3:]
                out_trade_no = 'V' + danhao[2:] + romcode
                data['usr_id'] = self.usr_id
                data['out_trade_no'] = out_trade_no
                data['ctime'] = self.getToday(9)
                self.db.insert('pingtai_paylog', data)
            else:
                data['utime'] = self.getToday(9)
                id, out_trade_no = lT[0]

                self.db.update('pingtai_paylog', data, 'id=%s' % id)

            app_id = self.oTOLL['wx_appid']

            wechat_pay_id = self.oTOLL['mchid']
            wechat_pay_secret = self.oTOLL['mchkey']
            base_url = self.oTOLL['callback_url']

            notify_url = base_url + '/vipnotify'

            data = {
                'appid': app_id,
                'mch_id': wechat_pay_id,
                'body': '简道商城平台-%s' % name,  # 商品描述
                'out_trade_no': out_trade_no,  # 商户订单号
                'total_fee': int(float(price) * 100),
                'notify_url': notify_url,
                'trade_type': 'NATIVE',
                'timeStamp': str(int(time.time())),
                'product_id': vip_flag
            }

            wxpay = WeixinPay(app_id, wechat_pay_id, wechat_pay_secret, notify_url)
            raw = wxpay.unified_order(**data)
            if raw.get('return_code') == 'SUCCESS':
                dR['code'] = '0'
                dR['code_url'] = raw['code_url']
                return dR

            dR['MSG'] = raw
            return dR

        except Exception as e:
            dR = {'code': '1', 'MSG': '%s' % e}
            return dR



    def vip_oss_data(self):
        dR = {'code': '1'}
        sql = """
              select 
                oss_one_day,
                oss_one_size,
                oss_one_price,
                oss_two_day,
                oss_two_size,
                oss_two_price,
                oss_thr_day,
                oss_thr_size,
                oss_thr_price
        from toll_config 

        """
        l, t = self.db.select(sql)
        if t == 0:
            return dR
        oss_one_day, oss_one_size, oss_one_price, oss_two_day, oss_two_size, oss_two_price, oss_thr_day, oss_thr_size, oss_thr_price = \
        l[0]

        data = [{
            'name': oss_one_size,
            'price': oss_one_price,
            'day': oss_one_day,
            'id': 4
        },
            {
                'name': oss_two_size,
                'price': oss_two_price,
                'day': oss_two_day,
                'id': 5
            },
            {
                'name': oss_thr_size,
                'price': oss_thr_price,
                'day': oss_thr_day,
                'id': 6
            }
        ]

        dR['code'] = '0'
        dR['data'] = data
        return dR

    def buy_oss_data(self):
        dR = {'code': '1', 'MSG': ''}
        oss_flag = self.GP('oss_flag', '')  #
        try:
            if self.usr_id_p != self.usr_id:
                dR['MSG'] = '子帐号不需要购买存储包'
                return dR
            sql = "select usr_id from users where coalesce(qiniu_flag,0)=1 and usr_id=%s"
            lT, iN = self.db.select(sql, [self.usr_id])
            if iN > 0:
                dR['MSG'] = '您是使用自己的自定义存储，不需要购买!'
                return dR
            if oss_flag == '4':
                sql = "select  oss_one_size,oss_one_price,oss_one_day from toll_config"
                l, t = self.db.select(sql)
                if t == 0:
                    dR['MSG'] = '您所要购买的套餐不存在,请重新选择购买'
                    return dR
                dR['code'] = '0'
            elif oss_flag == '5':
                sql = "select  oss_two_size,oss_two_price,oss_two_day from toll_config"
                l, t = self.db.select(sql)
                if t == 0:
                    dR['MSG'] = '您所要购买的套餐不存在,请重新选择购买'
                    return dR
                dR['code'] = '0'
            else:
                sql = "select  oss_thr_size,oss_thr_price,oss_thr_day from toll_config "
                l, t = self.db.select(sql)
                if t == 0:
                    dR['MSG'] = '您所要购买的套餐不存在,请重新选择购买'
                    return dR
                dR['code'] = '0'
            name, price, day = l[0]
            # 如果你是 Python 3的用户，使用默认的字符串即可
            cname='OSS存储%sM'%name
            data = {
                'ctype': oss_flag,
                'cname': cname,
                'price': price,
                'days': day,
            }
            sql = "select id,out_trade_no from pingtai_paylog where coalesce(pay_status,0)=0 and usr_id=%s and ctype=%s"
            lT, iN = self.db.select(sql, [self.usr_id,oss_flag])

            if iN == 0:
                timeStamp = time.time()
                timeArray = time.localtime(timeStamp)
                danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
                romcode = str(time.time()).split('.')[-1]  # [3:]
                out_trade_no = 'O' + danhao[2:] + romcode
                data['usr_id'] = self.usr_id
                data['out_trade_no'] = out_trade_no
                data['ctime'] = self.getToday(9)
                self.db.insert('pingtai_paylog', data)
            else:
                data['utime'] = self.getToday(9)
                id, out_trade_no = lT[0]

                self.db.update('pingtai_paylog', data, 'id=%s' % id)

            app_id = self.oTOLL['wx_appid']

            wechat_pay_id = self.oTOLL['mchid']
            wechat_pay_secret = self.oTOLL['mchkey']
            base_url = self.oTOLL['callback_url']

            notify_url = base_url + '/vipnotify'

            data = {
                'appid': app_id,
                'mch_id': wechat_pay_id,
                'body': '简道商城平台-%s' % cname,  # 商品描述
                'out_trade_no': out_trade_no,  # 商户订单号
                'total_fee': int(float(price) * 100),
                'notify_url': notify_url,
                'trade_type': 'NATIVE',
                'timeStamp': str(int(time.time())),
                'product_id': oss_flag
            }

            wxpay = WeixinPay(app_id, wechat_pay_id, wechat_pay_secret, notify_url)
            raw = wxpay.unified_order(**data)
            if raw.get('return_code') == 'SUCCESS':
                dR['code'] = '0'
                dR['code_url'] = raw['code_url']
                return dR


            dR['MSG'] = raw
            return dR

        except Exception as e:
            dR = {'code': '1', 'MSG': '%s' % e}
            return dR

