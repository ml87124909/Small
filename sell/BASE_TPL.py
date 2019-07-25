# -*- coding: utf-8 -*-
##############################################################################
#
#
#
##############################################################################
from imp import reload
from config import DEBUG
if DEBUG=='1':
    import sell.VI_BASE
    reload(sell.VI_BASE)
from sell.VI_BASE             import cVI_BASE
from basic.wxbase import wx_minapp_login,WXBizDataCrypt,WxPay
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib,time,json,datetime,requests


class cBASE_TPL(cVI_BASE):

    def goPartbegin(self):
        return self.jsons({'code':0,'data':u'你很调皮哦','msg':self.error_code[0]})

    def get_wx_users(self):  # 用户数量
        sql = "select count(id) from wechat_mall_user where usr_id=%s and coalesce(del_flag,0)=0"
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def user_today(self):  # 今日用户数量--
        sql = """select count(id) from wechat_mall_user 
                    where usr_id=%s and coalesce(del_flag,0)=0 
                    and to_char(now(),'YYYY-MM-DD')=to_char(ctime,'YYYY-MM-DD') 
            """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_goods_info(self):  # 商品数量
        sql = "select count(id) from goods_info where usr_id=%s and coalesce(del_flag,0)=0"
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def goods_today(self):  # 今日销量最高的商品名字--
        good_name = ''
        sql = """
            select count(amount)all_amount,good_name 
            from wechat_mall_order_detail 
            where usr_id=%s and to_char(now(),'YYYY-MM-DD')=to_char(ctime,'YYYY-MM-DD') 
             and coalesce(del_flag,0)=0
            group by good_id,good_name 
            order by all_amount desc limit 1;

        """
        l, t = self.db.select(sql, self.usr_id_p)
        if t > 0:
            good_name = l[0][1]
        return good_name

    def get_order_all(self):  # 订单总数
        sql = "select count(id) from wechat_mall_order where usr_id=%s and coalesce(del_flag,0)=0"
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def orders_today(self):  # 今日订单总数----
        sql = """select count(id) from wechat_mall_order 
        where usr_id=%s and coalesce(del_flag,0)=0 
        and to_char(now(),'YYYY-MM-DD')=to_char(ctime,'YYYY-MM-DD') 
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_today_order(self):  # 今日销售额
        sql = """
            select coalesce(round(sum(new_total)::numeric,2),0) from wechat_mall_order 
            where usr_id=%s and coalesce(del_flag,0)=0 
            and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')
            and status>1 and status<=7

        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def orders_all(self):  # 销售总额（总付款金额）--
        sql = """
                    select coalesce(round(sum(new_total)::numeric,2),0) from wechat_mall_order 
                    where usr_id=%s and coalesce(del_flag,0)=0 
                    and status>1 and status<=7
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_today_views(self):  # 今日浏览量
        sql = """
            select count(id) from view_history where usr_id=%s 
            and coalesce(del_flag,0)=0 and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_2(self):  # 未发货订单
        sql = """select count(id) from wechat_mall_order 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=2
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_base_me(self):  # 基本信息(小程序信息等)
        sql = """
            select to_char(u.ctime,'YYYY-MM-DD HH24:MI')ctime,
            to_char(u.expire_time,'YYYY-MM-DD HH24:MI')expire_time,
            m.appid,m.secret , coalesce(with_flag,0)with_flag
            from users u
            left join mall m on m.usr_id=u.usr_id 
            where u.usr_id=%s
        """
        t = self.db.fetch(sql, self.usr_id_p)
        return t

    def get_goods_sell(self):  # 出售中
        sql = """select count(id) from goods_info 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=0"""
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_sold_out(self):  # 已下架
        sql = """select count(id) from goods_info 
            where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=1
            """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_score_warn(self):  # 库存预警(库存小于5件)
        sql = """select count(id) from goods_info 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=0 and coalesce(stores,0)<=5
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_evaluation(self):  # 商品评价
        sql = "select count(id) from reputation_list where usr_id=%s and coalesce(del_flag,0)=0"
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_feedback(self):
        sql = "select count(id) from feedback where usr_id=%s and coalesce(del_flag,0)=0"
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_drawal_audit(self):  # 提现审核
        sql = "select count(id) from withdraw_cash where usr_id=%s and  coalesce(status,0)=1 "
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_1(self):  # 待付款
        sql = """select count(id) from wechat_mall_order 
        where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=1
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_7(self):  # 已完成
        sql = """select count(id) from wechat_mall_order 
                where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=7
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_4(self):  # 待自提
        sql = """
            select count(id) from wechat_mall_order 
                where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=7
        """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_5(self):  # 待收货
        sql = """
        select count(id) from wechat_mall_order 
            where usr_id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=5
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_99(self):  # 退款中
        sql = """
       select count(id) from refund_money 
       where usr_id=%s and  coalesce(status,0)=99  and coalesce(del_flag,0)=0
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_order_status_89(self):  # 未发货订单
        sql = """
        select count(id) from order_exchange 
        where usr_id=%s and  coalesce(status,0)=89  and coalesce(del_flag,0)=0
                """
        t = self.db.fetchcolumn(sql, self.usr_id_p)
        return t

    def get_yesterday_a(self):  # 昨日销量
        sql = """
        select count(id)amount,coalesce(round(sum(new_total)::numeric,2),0)total 
        from wechat_mall_order  
        where to_char(ctime,'YYYY-MM-DD')=to_char('YESTERDAY'::date,'YYYY-MM-DD') and usr_id=%s
        and status>1 and status<=7
                """
        t = self.db.fetch(sql, self.usr_id_p)
        return t

    def get_this_month(self):  # 本月销量
        sql = """
        select count(id)amount,coalesce(round(sum(new_total)::numeric,2),0)total 
        from wechat_mall_order  
        where to_char(ctime,'YYYY-MM')=to_char('YESTERDAY'::date,'YYYY-MM') and usr_id=%s 
        and status>1 and status<=7
                """
        t = self.db.fetch(sql, self.usr_id_p)
        return t

    def sale_goods(self):#销量排行 10个
        sql="""
            select good_id
            from wechat_mall_order_detail 
            where usr_id=%s  and coalesce(del_flag,0)=0  and status>1 and status<=7
            group by good_id
            order by sum(amount) desc limit 10;
        
        """
        l,t=self.db.select(sql,self.usr_id_p)
        if t==0:
            return {}
        L=[]
        for i in l:
            L.append(str(i[0]))
        good_ids=','.join(L)
        sql="""
             SELECT
                id,
                name,
                pic,
                coalesce(orders,0)orders,
                coalesce(stores,0)stores,
                minprice as mini_price
            FROM goods_info
            where usr_id=%s  and coalesce(del_flag,0)=0  and id in (%s) order by orders desc
        """%(self.usr_id_p,good_ids)
        D,i=self.db.fetchall(sql)
        return D


    def money_goods(self):#支付金额排行  10个
        sql = """
                   select good_id
                    from wechat_mall_order_detail 
                    where usr_id=%s 
                     and coalesce(del_flag,0)=0 and status>1 and status<=7
                    group by good_id
                    order by sum(amount*price) desc limit 10;
                """
        l, t = self.db.select(sql, self.usr_id_p)
        if t == 0:
            return {}
        L = []
        for i in l:
            L.append(str(i[0]))
        good_ids = ','.join(L)
        sql = """
             SELECT
                id,
                name,
                pic,
                coalesce(orders,0)orders,
                coalesce(stores,0)stores,
                minprice as mini_price

            FROM goods_info
            where usr_id=%s  and coalesce(del_flag,0)=0  and id in (%s) order by orders
                """ % (self.usr_id_p, good_ids)
        D, i = self.db.fetchall(sql)
        return D

    def trend_today(self):#销售趋势今日
        sql="""
        SELECT '今日付款金额' as name,substring(ac.dates from 11 for 11) as time,COALESCE(b.number,0) as value FROM (
            SELECT  to_char(
                to_char(now(), 'yyyy-MM-DD')::timestamp + (s.A || ' hour')::interval, 
                'yyyy-MM-DD HH24') AS dates 
        FROM 
            generate_series (0, 23) AS s (A)  --表示时间  
            ) AS ac  LEFT JOIN (SELECT sum(new_total) AS NUMBER, to_char(ctime, 'yyyy-MM-DD HH24') AS initme 
            FROM  wechat_mall_order where status>1 and status<=7 and usr_id=%s GROUP BY  initme
            ) b ON ac.dates = b.initme 
        """
        l,t=self.db.fetchall(sql,self.usr_id_p)

        sql="""
             SELECT '昨日付款金额' as name,substring(ac.dates from 11 for 11) as time,COALESCE(b.number,0) as value FROM (
            SELECT  to_char(
                (date_trunc('day',now()) -interval '1d')::timestamp + (s.A || ' hour')::interval, 
                'yyyy-MM-DD HH24') AS dates 
        FROM 
            generate_series (0, 23) AS s (A)  --表示时间  
            ) AS ac  LEFT JOIN (SELECT sum(new_total) AS NUMBER, to_char(ctime, 'yyyy-MM-DD HH24') AS initme 
            FROM  wechat_mall_order where status>1 and status<=7 and usr_id=%s GROUP BY  initme
            ) b ON ac.dates = b.initme 
        """
        ll,tt=self.db.fetchall(sql,self.usr_id_p)
        L = l+ll#[{'name':'今日付款金额','data':l},{'name':'昨日付款金额','data':ll}]
        return L

    def trend_month(self):#销售趋势本月
        sql = """
        SELECT '支付金额' as name,substring(ac.dates from 9 for 9) as time ,COALESCE(b.number,0) as value  FROM  ( 
            SELECT to_char( to_date(to_char(now(),'YYYY-MM'), 'yyyy-MM-dd') + s. A,'yyyy-MM-dd') AS dates  FROM 
            generate_series (0, 30) AS s (A)  --表示时间 
            ) AS ac  LEFT JOIN (SELECT sum(new_total) AS NUMBER, to_char(ctime, 'yyyy-MM-dd') AS initme 
            FROM  wechat_mall_order where status>1 and status<=7 and usr_id=%s  GROUP BY  initme
            ) b ON ac.dates = b.initme
        """
        l, t = self.db.fetchall(sql, self.usr_id_p)

        sql = """
                SELECT '退款金额' as name,substring(ac.dates from 9 for 9) as time ,COALESCE(b.number,0) as value  FROM  ( 
                    SELECT to_char( to_date(to_char(now(),'YYYY-MM'), 'yyyy-MM-dd') + s. A,'yyyy-MM-dd') AS dates  FROM 
                    generate_series (0, 30) AS s (A)  --表示时间 
                    ) AS ac  LEFT JOIN (SELECT sum(new_total) AS NUMBER, to_char(ctime, 'yyyy-MM-dd') AS initme 
                    FROM  wechat_mall_order where status>97 and status<=100 and usr_id=%s  GROUP BY  initme
                    ) b ON ac.dates = b.initme
                """
        ll,tt = self.db.fetchall(sql, self.usr_id_p)

        L = l+ll#[{'name': '支付金额', 'data': l}, {'name': '退款金额', 'data': ll}]
        return L

    def trend_all(self):#销售趋势合计
        sql = """
            SELECT '成交金额' as name,substring(ac.dates from 6 for 7) as time,COALESCE(b.number,0) as value  FROM  ( 
             SELECT to_char(now()::timestamp + (s.A || ' month')::interval,'yyyy-MM') AS dates 
                FROM generate_series (0, 11) AS s (A)  --表示时间 
            ) AS ac  LEFT JOIN (SELECT sum(new_total) AS NUMBER, to_char(ctime, 'yyyy-MM') AS initme 
            FROM  wechat_mall_order where status>1 and status<=7 and usr_id=%s  GROUP BY  initme
            ) b ON ac.dates = b.initme
                """
        l, t = self.db.fetchall(sql, self.usr_id_p)

        sql = """
                    SELECT '退款金额' as name,substring(ac.dates from 6 for 7) as time,COALESCE(b.number,0) as value  FROM  ( 
                     SELECT to_char(now()::timestamp + (s.A || ' month')::interval,'yyyy-MM') AS dates 
                        FROM generate_series (0, 11) AS s (A)  --表示时间 
                    ) AS ac  LEFT JOIN (SELECT sum(new_total) AS NUMBER, to_char(ctime, 'yyyy-MM') AS initme 
                    FROM  wechat_mall_order where status>97 and status<=100 and usr_id=%s  GROUP BY  initme
                    ) b ON ac.dates = b.initme
                        """
        ll, tt = self.db.fetchall(sql, self.usr_id_p)

        L = l+ll#[{'name': '成交金额', 'data': l}, {'name': '退款金额', 'data': ll}]
        return L

    def sales_today(self):#销售概况今日
        L = []
        sqla="""select coalesce(sum(new_total),0) from wechat_mall_order 
                where status=1 and usr_id=%s and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')"""
        la,ta=self.db.select(sqla,self.usr_id_p)
        pa=la[0][0]
        if pa>0:
            L.append({'name': '待支付', 'percent': pa, 'a': '1'})
        sqlb = """select coalesce(sum(new_total),0) from wechat_mall_order 
        where status>1 and status<=7 and usr_id=%s and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')"""
        lb,tb = self.db.select(sqlb, self.usr_id_p)
        pb=lb[0][0]
        if pb>0:
            L.append({'name': '已支付', 'percent': pb, 'a': '1'})
        sqlc = """select coalesce(sum(new_total),0) from wechat_mall_order 
        where status=-1 and usr_id=%s and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')"""
        lc,tc = self.db.select(sqlc, self.usr_id_p)
        pc=lc[0][0]
        if pc>0:
            L.append({'name': '已取消', 'percent': pc, 'a': '1'})
        sqld = """select coalesce(sum(new_total),0) from wechat_mall_order 
        where status=98 and usr_id=%s and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')"""
        ld,td = self.db.select(sqld, self.usr_id_p)
        pd=ld[0][0]
        if pd>0:
            L.append({'name': '已退款', 'percent': pd, 'a': '1'})


        return L

    def sales_month(self):#销售概况本月
        L = []
        sqla = """select coalesce(sum(new_total),0) from wechat_mall_order 
            where status>1 and status<=7 and usr_id=%s
            and to_char(ctime,'YYYY-MM')=to_char(now(),'YYYY-MM')
            """
        la,ta = self.db.select(sqla, self.usr_id_p)
        pa=la[0][0]
        if pa>0:
            L.append({'name': '成交金额', 'percent': pa, 'a': '1'})
        sqlb = """select coalesce(sum(new_total),0) from wechat_mall_order 
            where status=98 and usr_id=%s and to_char(ctime,'YYYY-MM')=to_char(now(),'YYYY-MM')"""
        lb,tb = self.db.select(sqlb, self.usr_id_p)
        pb=lb[0][0]
        if pb>0:
            L.append({'name': '退款金额', 'percent': pb, 'a': '1'})
        sqlc = """select coalesce(sum(new_total),0) from wechat_mall_order 
        where status=-1 and usr_id=%s and to_char(ctime,'YYYY-MM')=to_char(now(),'YYYY-MM')"""
        lc,tc = self.db.select(sqlc, self.usr_id_p)
        pc=lc[0][0]
        if pc>0:
            L.append({'name': '取消金额', 'percent': pc, 'a': '1'})

        return L

    def sales_all(self):#销售概况合计
        L = []
        sqla = """select coalesce(sum(new_total),0) from wechat_mall_order 
            where status>1 and status<=7 and usr_id=%s
            and to_char(ctime,'YYYY')=to_char(now(),'YYYY')
            """
        la,ta = self.db.select(sqla, self.usr_id_p)
        pa=la[0][0]
        if pa>0:
            L.append({'name': '成交金额', 'percent': pa, 'a': '1'})
        sqlb = """select coalesce(sum(new_total),0) from wechat_mall_order 
            where status=98 and usr_id=%s
            and to_char(ctime,'YYYY')=to_char(now(),'YYYY')
            """
        lb,tb = self.db.select(sqlb, self.usr_id_p)
        pb=lb[0][0]
        if pb>0:
            L.append({'name': '退款金额', 'percent': pb, 'a': '1'})

        return L

    def keyword(self):#搜索关键字排行（前10）
        sql="select cname as name,num as number from search_key where usr_id=%s order by num desc limit 10;"
        l,t=self.db.fetchall(sql,self.usr_id_p)
        return l

    def goodsView(self):##商品浏览排行（前20）
        sql="""
            select id,name,pic,minprice as price,coalesce(stores,0)stores,coalesce("views",0) as views,
            (coalesce("views",0)*coalesce(orders,0)/100)sales 
            from goods_info where usr_id=%s order by "views" desc limit 20;
        """
        l, t = self.db.fetchall(sql, self.usr_id_p)
        return l







