# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
from imp import reload
from config import DEBUG
if DEBUG=='1':
    import sell.BASE_TPL
    reload(sell.BASE_TPL)
from sell.BASE_TPL            import cBASE_TPL
import time,datetime

class chome(cBASE_TPL):


    def goParthome_list(self):#首页统计数据
        data={
            'user_amount': self.get_wx_users()  # 用户数量
            , 'user_today': self.user_today()  # 今日用户数量---
            , 'goods_amount': self.get_goods_info()  # 商品数量
            , 'goods_today': self.goods_today()  # 今日销量最高的商品名字----
            , 'orders_amount': self.get_order_all()  # 订单总数
            , 'orders_today': self.orders_today()  # 今日订单总数---
            , 'today_order': self.get_today_order()  # 今日销售额
            , 'orders_all': self.orders_all()  # 销售总额（总付款金额）---
            , 'today_views': self.get_today_views()  # 今日浏览量
            , 'orders_status_2': self.get_order_2()  # 未发货订单
            , 'base_me': self.get_base_me()  # 基本信息(小程序信息等)
            , 'goods_sell': self.get_goods_sell()  # 出售中
            , 'sold_out': self.get_sold_out()  # 已下架
            , 'score_warn': self.get_score_warn()  # 库存预警(库存小于5件)
            , 'evaluation': self.get_evaluation()  # 商品评价
            , 'feedback': self.get_feedback()  # 用户反馈
            , 'drawal_audit': self.get_drawal_audit()  # 提现审核
            , 'order_status_1': self.get_order_status_1()  # 待付款
            , 'order_status_7': self.get_order_status_7()  # 已完成
            , 'order_status_4': self.get_order_status_4()  # 待自提
            , 'order_status_5': self.get_order_status_5()  # 待收货
            , 'order_status_99': self.get_order_status_99()  # 退款中
            , 'order_status_89': self.get_order_status_89()  # 未发货订单
            , 'yesterday_a': self.get_yesterday_a()  # 昨日销量
            , 'this_month': self.get_this_month()  # 本月销量

        }
        return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})


    def goPartSales_Reports(self):#销售报表

        datas={
            'order_goods':{
                'sale_goods':self.sale_goods(),#销量排行
                'money_goods':self.money_goods(),#支付金额排行
            },#oeder_goods
            'order_trend':{
                'trend_today':self.trend_today(),#今日
                'trend_month':self.trend_month(),#本月
                'trend_all':self.trend_all()#合计
            },#销售趋势
            'order_sales':{
                'sales_today':self.sales_today(),  # 今日
                'sales_month': self.sales_month(),  # 本月
                'sales_all': self.sales_all()  # 合计
            }#销售概况
        }
        return self.jsons({'code':0,'data':datas,'msg':self.error_code['ok']})

    def goPartTrend_Reports(self):#运营报表

        datas={
            'keyword':self.keyword(),#搜索关键字排行（前10）
            'goodsView':self.goodsView()#商品浏览排行（前20）
        }
        return self.jsons({'code':0,'data':datas,'msg':self.error_code['ok']})


    def goPartOrder_list(self):#获取订单列表接口
        page = self.GP('page', '')
        pageSize = self.GP('pageSize', '')
        if page=='':
            page=1
        else:
            page=int(page)
        if pageSize=='':
            page_size=10
        else:
            page_size=int(pageSize)

        sql = """
                    SELECT
                        D.id,
                        D.cname,
                        D.order_num ,
                        D.number_goods ,
                        D.status,
                        D.status_str,
                        COALESCE(D.goods_price,0.0)goods_price,
                        COALESCE(D.logistics_price,0.0)logistics_price ,
                        COALESCE(D.coupon_price,0.0)coupon_price,
                        COALESCE(D.new_total,0.0)total ,
                        to_char(D.ctime,'YYYY-MM-DD HH24:MI')ctime,
                        COALESCE(D.check_id,0)check_id,
                        D.kuaid,
                        D.kuaid_str,
                        D.phone,
                        D.shipper_id,
                        D.tracking_number,
                        D.pay_status_str,
                        to_char(D.pay_ctime,'YYYY-MM-DD HH24:MI')pay_ctime,
                        (select count(w.id) from wechat_mall_order_detail w where w.order_id=D.id and w.status=2)ns,
                        to_char(data_close,'YYYY-MM-DD HH24:MI')data_close,
                        s.cname as dname,
                        to_char(D.shipper_time,'YYYY-MM-DD HH24:MI')shipper_time,wechat_user_id
                    FROM wechat_mall_order D
                    left join shopconfig s on s.usr_id=D.usr_id and s.id=D.mendian_id
                   where COALESCE(D.del_flag,0)=0 and  D.usr_id=%s
                """
        parm = [self.usr_id_p]
        ctype = self.GP('type', '')
        phone = self.GP('phone', '')
        if ctype!='':
            if ',' in ctype:
                andwhere = 'and D.status in (%s)'%ctype
            else:
                andwhere = ' and D.status =%s '
                parm.append(ctype)
            sql+=andwhere
        if phone!='':
            sql+=" and D.phone=%s"
            parm.append(phone)
        sql += " ORDER BY D.id DESC"

        lT, iN = self.db.fetchall(sql, parm)
        for j in lT:
            data_close = j.get('data_close', '')
            status = j.get('status', '')
            order_num = j.get('order_num', '')
            # id = j.get('id', '')
            # wechat_user_id = j.get('wechat_user_id', '')
            shipper_time = j.get('shipper_time', '')
            if data_close != '' and self.getToday(8) > data_close and str(status) == '1':
                self.db.query("update wechat_mall_order set status=-1,status_str='已取消' where order_num=%s", order_num)
                self.db.query("update wechat_mall_order_detail set status=-1,status_str='已取消' where order_num=%s",
                              order_num)
                j['status'] = -1
                j['sname'] = '已取消'
                # self.oORDER_D.update(self.usr_id, wechat_user_id, id)
            if str(status) == '5' and shipper_time != '':
                ORDER = self.oORDER_SET.get(self.usr_id_p)
                if ORDER == {}:
                    pass
                else:
                    take_day = ORDER.get('take_day')
                    now = datetime.datetime.strptime(shipper_time, "%Y-%m-%d %H:%M")
                    delta = datetime.timedelta(days=int(take_day))
                    n_days = now + delta
                    etime = n_days.strftime('%Y-%m-%d %H:%M:%S')
                    if self.getToday(9) > etime:
                        self.db.query("update wechat_mall_order set status=6,status_str='待评价' where order_num=%s",
                                      order_num)
                        self.db.query(
                            "update wechat_mall_order_detail set status=6,status_str='待评价' where order_num=%s",
                            order_num)
                        j['status'] = 6
                        j['sname'] = '待评价'
                        # self.oORDER_D.update(self.usr_id, wechat_user_id, id)

            sqld = """select id,good_name,price,amount,total,status,shipper_id,tracking_number,
                                pic,property_str,shipper_str
                                    from wechat_mall_order_detail 
                                    where order_num=%s
                                        """
            l, t = self.db.fetchall(sqld, order_num)
            if t > 0:
                j['detail'] = l
                j['qd'] = t

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(lT, iN,pageNo=page,
                                                                                select_size=page_size)

        datas={'result':L,'totalRow':iTotal_length,'totalPage':iTotal_Page}
        return self.jsons({'code':0,'data':datas,'msg':self.error_code['ok']})


    def goPartOrder_details(self):#查看订单详情接口
        id = self.GP('id', '')
        code = self.GP('code', '')
        if id =='' and code=='':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id or code')})
        sql = """
             SELECT
                D.id
                ,D.cname
                ,D.phone
                ,D.order_num
                ,D.status
                ,D.status_str
                ,D.ctype_str
                ,COALESCE(D.goods_price,0.0)goods_price
                ,COALESCE(D.logistics_price,0.0)logistics_price 
                ,COALESCE(D.coupon_price,0.0)coupon_price
                ,COALESCE(D.total,0.0)total
                ,D.tracking_number
                ,to_char(D.ctime,'YYYY-MM-DD HH24:MI')ctime
                ,D.kuaid
                ,D.kuaid_str
                ,COALESCE(D.shipper_id,0)shipper_id
                ,D.tracking_number
                ,D.province
                ,D.city
                ,D.district
                ,D.address
                ,D.remark
                ,D.pay_status
                ,D.pay_status_str
                ,to_char(D.pay_ctime,'YYYY-MM-DD HH24:MI')pay_ctime
                ,w.cname as wcname
                ,s.cname as dname,s.address as md_address,s.contact
                ,u.usr_name
                ,case when check_id=1 then to_char(check_time,'YYYY-MM-DD HH24:MI') else '' end check_time

            FROM wechat_mall_order D
            left join users u on u.usr_id=D.check_uid
           left join wechat_mall_user w on w.id=d.wechat_user_id and w.usr_id=D.usr_id
           left join shopconfig s on s.usr_id=D.usr_id and s.id=D.mendian_id
           where COALESCE(D.del_flag,0)=0 and D.usr_id=%s
        """
        parm=[self.usr_id_p]
        if id!='':
            sql+=" and D.id=%s"
            parm.append(id)
        if code!='':
            sql+=" and D.pick_number=%s"
            parm.append(code)


        L = self.db.fetch(sql,parm)
        if L=={}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        order_id=L.get('id','')
        if order_id!='':
            sqld = """select id,good_name,price,amount,total,status,shipper_id,tracking_number,
                            pic,property_str,shipper_str
                        from wechat_mall_order_detail 
                        where order_id=%s
                    """
            l, t = self.db.fetchall(sqld,order_id)
            if t > 0:
                L['detail'] = l
                L['qd'] = t

        return self.jsons({'code':0,'data':L,'msg':self.error_code['ok']})


    def goPartOrder_check(self):#核销自提订单接口
        id = self.GP('id', '')
        code = self.GP('code', '')

        if id=='' or id=='None' or id=='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if code=='' or code=='None' or code=='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('code')})

        sql="""select COALESCE(check_id,0) from wechat_mall_order 
        where pick_number=%s and id=%s and usr_id=%s and status=4"""
        l,t=self.db.select(sql,[code,id,self.usr_id_p])
        if t==0:
            return self.jsons({'code': 301,  'msg': 'code或id不正确'})
        check_id=l[0][0]
        if str(check_id)!='0':
            return self.jsons({'code': 302, 'msg': '该订单已经核销'})
        sql="""update wechat_mall_order set check_id=1,check_uid=%s,check_time=now(),status=6,status_str='待评价' 
            where usr_id=%s and id=%s
            """
        self.db.query(sql,[self.usr_id,self.usr_id_p,id])
        sql = """update wechat_mall_order_detail set status=6,status_str='待评价' 
                    where usr_id=%s and order_id=%s
                    """
        self.db.query(sql, [self.usr_id_p, id])
        return self.jsons({'code':0,'msg':'核销成功'})

    def goPartOrder_check_list(self):#查看已经核销的自提订单接口
        page = self.GP('page', '')
        pageSize = self.GP('pageSize', '')
        if page=='':
            page=1
        else:
            page=int(page)
        if pageSize=='':
            page_size=10
        else:
            page_size=int(pageSize)
        sql = """
            SELECT
                D.id,
                D.cname,
                D.order_num ,
                D.number_goods ,
                D.status,
                D.status_str,
                COALESCE(D.goods_price,0.0)goods_price,
                COALESCE(D.logistics_price,0.0)logistics_price ,
                COALESCE(D.coupon_price,0.0)coupon_price,
                COALESCE(D.new_total,0.0)total ,
                to_char(D.ctime,'YYYY-MM-DD HH24:MI')ctime,
                COALESCE(D.check_id,0)check_id,
                D.kuaid,
                D.kuaid_str,
                D.phone,
                D.shipper_id,
                D.tracking_number,
                D.pay_status_str,
                to_char(D.pay_ctime,'YYYY-MM-DD HH24:MI')pay_ctime,
                (select count(w.id) from wechat_mall_order_detail w where w.order_id=D.id and w.status=2)ns,
                to_char(data_close,'YYYY-MM-DD HH24:MI')data_close,
                s.cname as dname,
                to_char(D.shipper_time,'YYYY-MM-DD HH24:MI')shipper_time,
                wechat_user_id,
                u.usr_name
                ,case when check_id=1 then to_char(check_time,'YYYY-MM-DD HH24:MI') else '' end check_time
            FROM wechat_mall_order D
            left join users u on u.usr_id=D.check_uid
            left join shopconfig s on s.usr_id=D.usr_id and s.id=D.mendian_id
           where COALESCE(D.del_flag,0)=0 and  D.usr_id=%s and check_id=1
            """
        parm = [self.usr_id_p]
        id = self.GP('id', '')
        phone = self.GP('phone', '')
        if id!='':
            sql+= ' and D.id =%s '
            parm.append(id)

        if phone!='':
            sql+=" and D.phone=%s"
            parm.append(phone)
        sql += " ORDER BY D.id DESC"

        lT, iN = self.db.fetchall(sql, parm)
        for j in lT:
            data_close = j.get('data_close', '')
            status = j.get('status', '')
            order_num = j.get('order_num', '')
            # id = j.get('id', '')
            # wechat_user_id = j.get('wechat_user_id', '')
            shipper_time = j.get('shipper_time', '')
            if data_close != '' and self.getToday(8) > data_close and str(status) == '1':
                self.db.query("update wechat_mall_order set status=-1,status_str='已取消' where order_num=%s", order_num)
                self.db.query("update wechat_mall_order_detail set status=-1,status_str='已取消' where order_num=%s",
                              order_num)
                j['status'] = -1
                j['sname'] = '已取消'
                # self.oORDER_D.update(self.usr_id, wechat_user_id, id)
            if str(status) == '5' and shipper_time != '':
                ORDER = self.oORDER_SET.get(self.usr_id_p)
                if ORDER == {}:
                    pass
                else:
                    take_day = ORDER.get('take_day')
                    now = datetime.datetime.strptime(shipper_time, "%Y-%m-%d %H:%M")
                    delta = datetime.timedelta(days=int(take_day))
                    n_days = now + delta
                    etime = n_days.strftime('%Y-%m-%d %H:%M:%S')
                    if self.getToday(9) > etime:
                        self.db.query("update wechat_mall_order set status=6,status_str='待评价' where order_num=%s",
                                      order_num)
                        self.db.query(
                            "update wechat_mall_order_detail set status=6,status_str='待评价' where order_num=%s",
                            order_num)
                        j['status'] = 6
                        j['sname'] = '待评价'
                        # self.oORDER_D.update(self.usr_id, wechat_user_id, id)

            sqld = """select id,good_name,price,amount,total,status,shipper_id,tracking_number,
                                pic,property_str,shipper_str
                                    from wechat_mall_order_detail 
                                    where order_num=%s
                                        """
            l, t = self.db.fetchall(sqld, order_num)
            if t > 0:
                j['detail'] = l
                j['qd'] = t

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(lT, iN, pageNo=page,
                                                                                select_size=page_size)

        datas={'result':L,'totalRow':iTotal_length,'totalPage':iTotal_Page}
        return self.jsons({'code':0,'data':datas,'msg':self.error_code['ok']})


    def goPartGoods_list(self):#获取商品列表接口
        ctype = self.GP('type', '')
        page = self.GP('page', '')
        pageSize = self.GP('pageSize', '')
        if page=='':
            page=1
        else:
            page=int(page)
        if pageSize=='':
            page_size=10
        else:
            page_size=int(pageSize)
        l = self.oGOODS_SELL.get(self.usr_id_p)
        if str(ctype)=='1':
            M=[]
            for i in l:
                status=i.get('status')
                if str(status)=='0':
                    M.append(i)
            t = len(M)
        elif str(ctype) == '2':
            M = []
            for i in l:
                status = i.get('stores')
                if str(status) == '0':
                    M.append(i)
            t = len(M)
        elif str(ctype) == '3':
            M = []
            for i in l:
                status = i.get('status')
                if str(status) == '1':
                    M.append(i)
            t = len(M)
        else:
            M=l
            t = len(l)
        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(M, t, pageNo=page,
                                                                                select_size=page_size)
        datas = {'result': L, 'totalRow': iTotal_length, 'totalPage': iTotal_Page}

        return self.jsons({'code':0,'data':datas,'msg':self.error_code['ok']})


    def goPartGoods_fast_edit(self):#快速修改商品接口
        id = self.GP('id', '')
        ctype = self.GP('type', '')
        data = self.GP('data', '')

        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if ctype == '' or ctype == 'None' or ctype == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('type')})
        if data == '' or data == 'None' or data == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('data')})

        sql="select status,recomm from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and id=%s"
        l,t=self.db.select(sql,[self.usr_id_p,id])
        if t==0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        status, recomm=l[0]
        if ctype=='1':
            if (str(status)=='0' and str(data)=='true') or (str(status)=='1' and str(data)=='false'):
                return self.jsons({'code': 301, 'msg': '参数不正确'})
            if str(data)=='false':
                statuss=1
                statusstr = '下架'
            else:
                statuss = 0
                statusstr = '上架'
            sql = "update goods_info set status=%s,statusstr=%s,utime=now() where usr_id=%s and  id=%s"
            self.db.query(sql, [statuss,statusstr,self.usr_id_p, id])
        elif ctype=='2':
            if (str(recomm)=='0' and str(data)=='false') or (str(recomm)=='1' and str(data)=='true'):
                return self.jsons({'code': 301, 'msg': '参数不正确'})
            if str(data)=='false':
                recomms=0
                recommsstr = '不推荐'
            else:
                recomms = 1
                recommsstr = '推荐'

            sql = "update goods_info set recomm=%s,recommstr=%s,uid=%s,utime=now() where usr_id=%s and  id=%s"
            self.db.query(sql, [recomms,recommsstr,self.usr_id,self.usr_id_p, id])
        elif ctype=='3':
            sql="update goods_info set del_flag=1,utime=now() where usr_id=%s and  id=%s"
            self.db.query(sql,[self.usr_id_p,id])
        self.oGOODS.update(self.usr_id_p,id)
        self.oGOODS_SELL.update(self.usr_id_p)
        self.oGOODS_D.update(self.usr_id_p,id)
        self.oGOODS_N.update(self.usr_id_p,id)
        return self.jsons({'code': 0, 'msg': self.error_code['ok']})



    def goPartGoods_edit(self):#获取/修改/添加 商品数据接口

        datas={
            'keyword':{#搜索关键字排行（前10）
                'name':'',#关键字名称
                'number':'',#关键字搜索次数
            },
            'goodsView':{#商品浏览排行（前20）
                'trend_today':self.trend_today(),#今日
                'trend_month':self.trend_month(),#本月
                'trend_all':self.trend_all()#合计
            }

        }
        return self.jsons({'code':0,'data':datas,'msg':self.error_code['ok']})


    def goPartLogistics_all(self):#全部发货接口
        id = self.GP('id', '')
        kuaid = self.GP('kuaid', '')
        kuanum = self.GP('kuanum', '')
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if kuaid == '' or kuaid == 'None' or kuaid == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('kuaid')})
        # if kuanum == '' or kuanum == 'None' or kuanum == 'undefined':
        #     return self.jsons({'code': 300, 'msg': self.error_code[300].format('kuanum')})

        sql = """select status,coalesce(s_type,0),wechat_user_id,order_num  
        from wechat_mall_order where usr_id=%s and id=%s"""
        l,t=self.db.select(sql,[self.usr_id_p,id])
        if t==0:
            return self.jsons({'code':404, 'msg': self.error_code[404]})
        status, s_type, wechat_user_id, order_num = l[0]
        if str(status)!='2':
            return self.jsons({'code': 301, 'msg': '订单ID状态不正确'})
        l,t=self.db.select("select id,txt2 from mtc_t where type='KD' and txt1=%s" ,kuaid)
        if t==0:
            return self.jsons({'code': 304, 'msg': '您发货的物流公司目前不支持'})
        kid,kai=l[0]
        shipper_str=kai.replace('快递code:','')
        sql="""
            update  wechat_mall_order set 
            shipper_id=%s,tracking_number=%s,shipper_str=%s,shipper_time=now(),shipper_code=%s,
            status=5,status_str='待收货'
            where id=%s and usr_id=%s
        """
        self.db.query(sql,[kid,kuanum,shipper_str,kuaid,id,self.usr_id_p])

        sql = """
                    update  wechat_mall_order_detail set 
                    shipper_id=%s,tracking_number=%s,shipper_str=%s,shipper_time=now(),shipper_code=%s,
                    status=5,status_str='待收货'
                    where order_id=%s and usr_id=%s
                """
        self.db.query(sql, [kid, kuanum, shipper_str, kuaid, id, self.usr_id_p])
        a='shipper_id=%s,tracking_number=%s,shipper_str=%s,shipper_code=%s'%(kid, kuanum, shipper_str, kuaid)
        self.write_order_log(id,'小程序发货',a,'uid=%s'%self.usr_id)
        try:
            if str(s_type) == '0':  # 推送发货消息
                sql = "select prepay_id from wechat_mall_payment where COALESCE(status,0)=1 and order_id=%s"
                lT1, iN1 = self.db.select(sql, id)
                if iN1 > 0:
                    prepay_id = lT1[0][0]
                    a = self.order_shipment_send(wechat_user_id, prepay_id, order_num, shipment=shipper_str,
                                                 shipmentcode=kuanum,orderid=id)
                    if a.get('errcode', '') == 0:
                        self.db.query("update wechat_mall_order set s_type=1 where id=%s ", id)

        except Exception as e:
            self.print_log('推送发货出错','%s'%e)

        return self.jsons({'code':0,'msg':self.error_code['ok']})


    def goPartNotice_list(self):#公告列表接口
        ctype = self.GP('type', '')
        sql="""
            select s.id,s.title,s.ctype as type,to_char(s.ctime,'YYYY-MM-DD HH24:MI') as time,u.usr_name as user
            from sys_news s
             left join users u on u.usr_id=s.cid 
            where COALESCE(s.del_flag,0)=0
        """
        parm=[]
        if ctype!='':
            sql+=" and s.ctype=%s "
            parm.append(ctype)
        sql+="order by s.id desc"
        l,t=self.db.fetchall(sql,parm)
        if t==0:
            return self.jsons({'code':404, 'msg': self.error_code[404]})

        return self.jsons({'code':0,'msg':self.error_code['ok'],'data':l})


    def goPartNotice_details(self):#公告详情接口
        id = self.GP('id', '')
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        sql="""
            select s.id,s.title,s.ctype as type,to_char(s.ctime,'YYYY-MM-DD HH24:MI') as time
            ,u.usr_name as user,s.contents as content
            from sys_news s
             left join users u on u.usr_id=s.cid 
            where COALESCE(s.del_flag,0)=0 and id=%s
        """
        parm=[id]
        l,t=self.db.fetchall(sql,parm)
        if t==0:
            return self.jsons({'code':404, 'msg': self.error_code[404]})

        return self.jsons({'code':0,'msg':self.error_code['ok'],'data':l[0]})

    def goPartPaypal_qrcode(self):#扫码收款接口
        paypalkey = self.GP('paypalkey', '')
        money = self.GP('money', '')
        if paypalkey == '' or paypalkey == 'None' or paypalkey == 'undefined' or paypalkey=='null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('paypalkey')})
        if money == '' or money == 'None' or money == 'undefined' or money=='null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('money')})
        # self.usr_id = int(dR['usr_id'])
        # self.usr_id_p = self.get_usr_id_p(self.usr_id)
        sql="""
          select id,wechat_user_id,extract(epoch FROM (now() - ctime)) from self_paykey where usr_id=%s and paykey=%s
        """
        parm=[self.usr_id_p,paypalkey]
        l,t=self.db.select(sql,parm)
        if t==0:
            return self.jsons({'code': 2, 'msg': '付款码无效'})
            #return self.jsons({'code':404, 'msg': self.error_code[404]})

        sid,wechat_user_id,SECOND=l[0]
        if SECOND>=30:
            return self.jsons({'code': 2, 'msg': '付款码无效'})
        self.db.query("update self_paykey set paykey='' where id=%s", [sid])
        USER = self.oUSER.get(self.usr_id_p, wechat_user_id)

        if USER == {}:
            return self.jsons({'code': 10000, 'msg': self.error_code[10000]})

        if str(USER.get('status', '')) == '1':
            return self.jsons({'code': 701, 'msg': self.error_code[701]})


        sql="select round(COALESCE(balance,0)::numeric,2),cname from wechat_mall_user where usr_id=%s and id=%s"
        l,t=self.db.select(sql,[self.usr_id_p,wechat_user_id])
        if t==0:
            return self.jsons({'code':405, 'msg': self.error_code[405]})
        balance,cname=l[0]
        wname = USER.get('name', '')
        avatar = USER.get('avatar', '')
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]

        order_num = 'C' + danhao[2:] + romcode
        order_dict = {
            'wechat_user_id': wechat_user_id,
            'cid': wechat_user_id,
            'usr_id': self.usr_id_p,
            'order_num ': order_num,
            'wname': wname,
            'avatar': avatar,
            'total': float(money),
            'paykey': paypalkey,
            'ctype': 2
        }
        ##确定会员折扣
        vip_state, vip_level, vip_level_name, vip_sale = self.get_vip_type(wechat_user_id)
        new_total = round(float(money) * float(vip_sale), 2)

        if float(new_total) > balance:
            return self.jsons({'code': 1, 'msg': '余额不足'})
        vipsale = round(float(money) - float(new_total), 2)
        # 生成订单写入数据库返回
        order_dict['vipsale'] = vipsale
        order_dict['truemoney'] = new_total

        score = 0
        # 赠送积分
        sql = "select COALESCE(integral,0),COALESCE(vip_integral,0) from score_conf where usr_id=%s"
        l, t = self.db.select(sql, [self.usr_id_p])
        if t > 0:
            integral, vip_integral = l[0]
            User = self.oUSER.get(self.usr_id_p, wechat_user_id)
            vip_level = User.get('vip_level', '0')
            if str(vip_level) == '0':
                score = float(money) * integral
            else:
                score = float(money) * vip_integral

            sql = "update wechat_mall_user set balance=balance-%s,score=COALESCE(score,0)+%s where usr_id=%s and id=%s"
            self.db.query(sql, [new_total, score, self.usr_id_p, wechat_user_id])
            self.user_log(wechat_user_id, '扫码支付', 'balance:%s,money:%s,score:%s' % (balance, new_total, score))
        else:
            sql = "update wechat_mall_user set balance=balance-%s where usr_id=%s and id=%s"
            self.db.query(sql, [new_total, self.usr_id_p, wechat_user_id])
            self.user_log(wechat_user_id, '扫码支付', 'balance:%s,money:%s' % (balance, new_total))
        order_dict['score'] = score
        order_dict['truemoney'] = new_total
        order_dict['paytime'] = self.getToday(9)
        order_dict['ctime'] = self.getToday(9)
        order_dict['status'] = 1
        self.db.insert('offline_pay', order_dict)


        self.oUSER.update(self.usr_id_p,wechat_user_id)
        # try:
        #     from apps import user_socket_dict
        #     WS = user_socket_dict.get(wechat_user_id,'')
        #
        #     if WS!='':
        #         self.print_log('扫码ws','ws不为空')
        #         WS.send(paypalkey)
        # except Exception as e:
        #     self.print_log('扫码发送WEBSOCKET故障:','%s'%e)
        return self.jsons({'code':0,'msg':self.error_code['ok'],'data':{'uid':wechat_user_id,'paykey':paypalkey}})

    def goPartPaypal_qrcode_list(self):#扫码收款记录接口

        sql="""
            select id,wname as user,round(COALESCE(truemoney,0)::numeric,2) as money,
            to_char(ctime,'YYYY-MM-DD HH24:MI')as time
            from offline_pay
            where usr_id=%s and ctype=2 order by ctime desc
        """
        parm=[self.usr_id_p]
        l,t=self.db.fetchall(sql,parm)
        if t==0:
            return self.jsons({'code':404, 'msg': self.error_code[404]})
        return self.jsons({'code':0,'msg':self.error_code['ok'],'data':l})




















