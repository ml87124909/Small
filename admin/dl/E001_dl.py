# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/E001_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import time , random,datetime,traceback

 
class cE001_dl(cBASE_DL):
    
    def init_data(self):

        # [列头,宽,对齐]
        self.FDT = [
            ['', '', ''],  # 0
            ['商品', '3', ''],  # 1
            ['单价(元)/数量', '1', ''],  # 2
            ['小计', '1', ''],  # 3
            ['发货', '1', ''],  #4
            ['买家/收货人', '2', ''],  # 5
            ['配送方式', '1', ''],  #6
            ['实付金额(元)', '1', ''],  # 7
            ['订单状态', '1', ''],  # 8
            ['发货状态', '1', ''],  # 9
            ['单价(元)/数量', '2', ''],  # 10
            ['退款状态', '1', ''],  # 11
            ['优惠(元)', '1', ''],  # 12


        ]
        # self.GNL=[] #列表上出现的
        self.GNL = self.parse_GNL([0,1, 2, 3, 4, 5, 6, 7,8])
        self.GNL2 = self.parse_GNL([0, 1, 10,3, 9, 11, 12])


        

        self.multab = self.GP("multab", "1")
        self.tab = self.GP("tab", self.multab)


    def mRight(self):
            
        sql = """
            SELECT
                D.id,
                convert_from(decrypt(D.cname::bytea, %s, 'aes'),'SQL_ASCII')cname,
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
                convert_from(decrypt(D.phone::bytea, %s, 'aes'),'SQL_ASCII')phone,
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
             left join wechat_mall_user w on w.id=D.wechat_user_id and w.usr_id=D.usr_id
           where COALESCE(D.del_flag,0)=0 and  COALESCE(D.ctype,0)!=6 and  D.usr_id=%s
        """
        parm=[self.md5code,self.md5code,self.usr_id_p]
        ctype=self.GP('ctype','')

        ctype_d = {'0': 'order_num', '1': 'cname', '2': 'phone', '3': '', '4': 'cname'}
        cnames = ctype_d.get(ctype, '0')

        if self.qqid!='':
            if ctype == '4':
                sql += "and w.%s" % cnames + "  like %s"
            else:
                sql += "and D.%s" % cnames + "  like %s"
            parm.append('%%%s%%'%self.qqid)
        status_s = self.GP('status', '')
        if status_s != '':
            sql += " and D.status=%s"
            parm.append(status_s)
        sdate=self.GP('sdate','')
        if sdate!='':
            sql+=" and to_char(D.ctime,'YYYY-MM-DD')>=%s"
            parm.append(sdate)
        edate = self.GP('edate', '')
        if edate!='':
            sql+=" and to_char(D.ctime,'YYYY-MM-DD')<=%s"
            parm.append(edate)
        if str(self.tab)=='2':
            sql += " and D.status=1 "
        elif str(self.tab) == '3':
            sql += " and D.status=2 "
        elif str(self.tab) == '4':
            sql += " and D.status=3 "
        elif str(self.tab) == '5':
            sql += " and D.status=5 "
        elif str(self.tab) == '6':
            sql += " and D.status=4 "
        elif str(self.tab) == '7':
            sql += " and D.status=7 "
        elif str(self.tab) == '8':
            sql += " and D.status=-1 "
        sql += " ORDER BY D.id DESC"

        lT,iN=self.db.fetchall(sql,parm)
        for j in lT:
            data_close=j.get('data_close','')
            status=j.get('status','')
            order_num=j.get('order_num','')
            # id = j.get('id', '')
            # wechat_user_id = j.get('wechat_user_id', '')
            shipper_time = j.get('shipper_time', '')
            if data_close !='' and self.getToday(8)> data_close and str(status)=='1':
                self.db.query("update wechat_mall_order set status=-1,status_str='已取消' where order_num=%s",order_num)
                self.db.query("update wechat_mall_order_detail set status=-1,status_str='已取消' where order_num=%s", order_num)
                j['status']=-1
                j['sname'] = '已取消'
                #self.oORDER_D.update(self.usr_id, wechat_user_id, id)
            if str(status) == '5' and shipper_time!='':
                ORDER=self.oORDER_SET.get(self.usr_id_p)
                if ORDER=={}:
                    pass
                else:
                    take_day=ORDER.get('take_day')
                    now = datetime.datetime.strptime(shipper_time, "%Y-%m-%d %H:%M")
                    delta = datetime.timedelta(days=int(take_day))
                    n_days = now + delta
                    etime = n_days.strftime('%Y-%m-%d %H:%M:%S')
                    if self.getToday(9)>etime:
                        self.db.query("update wechat_mall_order set status=6,status_str='待评价' where order_num=%s",
                                      order_num)
                        self.db.query(
                            "update wechat_mall_order_detail set status=6,status_str='待评价' where order_num=%s",
                            order_num)
                        j['status'] = 6
                        j['sname'] = '待评价'
                        #self.oORDER_D.update(self.usr_id, wechat_user_id, id)

            sqld = """select id,good_name,price,amount,total,status,shipper_id,tracking_number,
                        pic,property_str,shipper_str
                            from wechat_mall_order_detail 
                            where order_num=%s
                                """
            l,t=self.db.fetchall(sqld,order_num)
            if t>0:
                j['detail']=l
                j['qd']=t
        self.pageNo = self.GP('pageNo', '')
        if self.pageNo == '':
            self.pageNo = '1'
        self.pageNo = int(self.pageNo)
        # if self.qqid != '' and len(self.QNL) > 0:
        #     sql += self.QNL + "AND LIKE '%%%s%%' " % (self.qqid)
        # ORDER BY 
        # if self.orderby != '':
        #     sql += ' ORDER BY %s %s' % (self.orderby, self.orderbydir)
        # else:

        #print(sql)

        #L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo)
        L, iTotal_length, iTotal_Page, pageNo, select_size=self.list_for_grid(lT,iN,self.pageNo)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L
    
    def get_local_data(self):
        #这里请获取表单所有内容。包括gw_doc表的title

        L = {}
        sql="""
             SELECT
                D.id
                ,convert_from(decrypt(D.cname::bytea, %s, 'aes'),'SQL_ASCII')cname
                ,convert_from(decrypt(D.phone::bytea, %s, 'aes'),'SQL_ASCII')phone
                ,D.order_num
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
                ,convert_from(decrypt(D.address::bytea, %s, 'aes'),'SQL_ASCII')address
                ,D.remark
                ,D.memo
                ,D.pay_status
                ,D.pay_status_str
                ,to_char(D.pay_ctime,'YYYY-MM-DD HH24:MI')pay_ctime
                ,w.cname as wcname
                ,s.cname as dname,s.address as md_address,s.contact
            FROM wechat_mall_order D
           left join wechat_mall_user w on w.id=d.wechat_user_id and w.usr_id=D.usr_id
           left join shopconfig s on s.usr_id=D.usr_id and s.id=D.mendian_id
           where D.id=%s and COALESCE(D.del_flag,0)=0 and D.usr_id=%s
        """
        if self.pk != '':
            L = self.db.fetch(sql,[self.pk,self.usr_id_p])
            sqld="""select id,good_name,price,amount,total,status,shipper_id,tracking_number,
                    pic,property_str,shipper_str
                from wechat_mall_order_detail 
                where order_id=%s
                    """
            l, t = self.db.fetchall(sqld,self.pk)
            if t > 0:
                L['detail'] = l
                L['qd'] = t

        return L

    def local_add_save(self):
        
        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        pk 已经传进来  是 gw_doc 的 ID 请勿弄错
        """

        # 这些是表单值
        dR = {'R':'', 'MSG':'提交成功'}
        
        #请先查询自己的表是否有数据。 例如gw_doc有ID为1的数据。 table1的gw_id没有ID为1的数据。需要增加
        #假如字表的名字是 gw_test

        coupon_price = self.GP('coupon_price','')
        status =self.GP('status','')
        tracking_number = self.GP('tracking_number', '')
        total=self.GP('total','')


        data={

            'tracking_number':tracking_number,
            'status': status,
        }
        if coupon_price!='':
            data['coupon_price']=coupon_price
            data['total'] = total

        # if self.pk != '':  # update
        #     data['uid']=self.usr_id
        #     data['utime'] = self.getToday(9)
        #     self.db.update('wechat_mall_order' , data , " id = %s " % self.pk)
            
        return dR
        
    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update wechat_mall_order set del_flag=1 where id= %s and usr_id=%s" , [pk,self.usr_id_p])
        return dR

    def good_list(self):
        sql="select id,name from goods_category where usr_id =%s"
        l,t=self.db.select(sql,self.usr_id_p)
        return l

    def order_status_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        if id=='':
            dR['code']='1'
            dR['MSG'] = '参数有误！'
            return dR

        sql="select new_total from wechat_mall_order where COALESCE(status,0)=1 and id=%s and usr_id=%s"
        l,t=self.db.select(sql,[id,self.usr_id_p])

        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        dR['code'] = '0'
        dR['data'] = l[0][0]
        return dR


    def edit_price_data(self):
        dR = {'code': '', 'MSG': ''}
        id=self.GP('id','')
        total=self.GP('total','')
        new_total = self.GP('new_total', '')

        if id =='' or total=='' or new_total=='':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR

        sql = "select wechat_user_id,order_num from wechat_mall_order where COALESCE(status,0)=1 and id=%s and usr_id=%s"

        l, t = self.db.select(sql, [id,self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        wechat_user_id, order_num = l[0]
        romcode = str(time.time()).split('.')[-1]  # [3:]
        price_num = order_num + '_' + romcode
        try:
            sql = """update wechat_mall_order set 
                        new_total=%s,price_status=1,price_time=now(),utime=now(),price_num=%s 
                        where COALESCE(status,0)=1 and id=%s and usr_id=%s"""
            self.db.query(sql, [new_total, price_num, id, self.usr_id_p])

            self.write_order_log(id, 'new_total', '原来价格:%s,现在价格:%s' % (total, new_total), '修改价格')
            #self.oORDER_D.update(self.usr_id, wechat_user_id, id)
        except:
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR

        dR['code'] = '0'
        dR['MSG'] = '数据修改成功！'
        return dR

    def Pay_order_pay_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        if id =='':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql = """select new_total,wechat_user_id,status,status_str,kuaid,order_num,ctype,ptid,ptkid,
                COALESCE(pt_type,0),COALESCE(pay_status,0),phone 
                from wechat_mall_order where COALESCE(status,0)=1 and id=%s and usr_id=%s"""
        l, t = self.db.select(sql, [id,self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        total,uid,status, status_str, kuaid,order_num,ctype,ptid,ptkid,pt_type,pay_status,phone=l[0]

        sql="select COALESCE(balance,0.0) from wechat_mall_user where COALESCE(del_flag,0)=0 and usr_id=%s and id=%s"
        lT, iN = self.db.select(sql, [self.usr_id_p,uid])
        if iN == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        balance=lT[0][0]
        if total>balance:
            dR['code'] = '1'
            dR['MSG'] = '用户余额不足！'
            return dR
        sql = "update wechat_mall_user set balance=balance-%s where COALESCE(del_flag,0)=0 and usr_id=%s and id=%s"
        self.db.query(sql, [total, self.usr_id_p, uid])
        sql="""
            insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
            values(%s,%s,3,'消费',%s,3,'抵扣',%s,'后台余额支付',%s,now())
        """
        self.db.query(sql,[self.usr_id_p,uid,total,order_num,self.usr_id])

        self.pay_time(4, '后台余额', id)

        if str(ctype) == '2':

            dR['code'] = '1'
            dR['MSG'] = '拼团后台未处理!'
            return dR

        try:
            if str(ctype)=='0':
                if str(kuaid) == '0':
                    sql = "update wechat_mall_order set status=2,status_str='待发货'  where  id=%s and usr_id=%s "
                    self.db.query(sql, [id, self.usr_id_p])
                    self.write_order_log(id, 'wechat_mall_user:balance,wechat_mall_order:status和status_str',
                                         '用户余额:%s,价格:%s' % (balance, total), '用户余额支付')
                    self.pay_order_detail_data(id, 2, '待发货')

                    self.update_pay_member(id)
                    self.user_log(self.usr_id, 'balance', '余额支付订单，balance:%s，订单id:%s' % (balance, id))
                    self.oUSER.update(self.usr_id_p, uid)
                    # self.oORDER_D.update(self.usr_id, uid, id)
                    dR['code'] = '0'
                    dR['MSG'] = '余额支付成功!'
                    return dR


                elif str(kuaid) == '2':

                    sql = "update wechat_mall_order set status=6,status_str='待评价'  where  id=%s and usr_id=%s "
                    self.db.query(sql, [id, self.usr_id_p])
                    self.write_order_log(id, 'wechat_mall_user:balance,wechat_mall_order:status和status_str',
                                         '用户余额:%s,价格:%s' % (balance, total), '用户余额支付,无需配送待评价')
                    self.pay_order_detail_data(id, 6, '待评价')

                    self.update_pay_member(id)
                    self.user_log(self.usr_id, 'balance', '余额支付订单，balance:%s，订单id:%s' % (balance, id))
                    self.oUSER.update(self.usr_id_p, uid)
                    # self.oORDER_D.update(self.usr_id, uid, id)
                    dR['code'] = '0'
                    dR['MSG'] = '余额支付成功!'
                    return dR
                else:

                    sql = "update wechat_mall_order set status=4,status_str='待自提'  where  id=%s and usr_id=%s "
                    self.db.query(sql, [id, self.usr_id_p])
                    self.write_order_log(id, 'wechat_mall_user:balance,wechat_mall_order:status和status_str',
                                         '用户余额:%s,价格:%s' % (balance, total), '用户余额支付,自提单待自提')
                    self.pay_order_detail_data(id, 4, '待自提')

                    self.update_pay_member(id)
                    self.user_log(self.usr_id, 'balance', '余额支付订单，balance:%s，订单id:%s' % (balance, id))
                    self.oUSER.update(self.usr_id_p, uid)
                    # self.oORDER_D.update(self.usr_id, uid, id)
                    dR['code'] = '0'
                    dR['MSG'] = '余额支付成功!'
                    return dR
            elif str(ctype)=='2':
                if str(pt_type) == '0':#开团
                    self.Pingtuan_add(uid,ptid,id,phone)
                elif str(pt_type) == '1':#参团
                    self.Pingtuan_join(uid,ptkid,id,phone)

                dR['code'] = '0'
                dR['MSG'] = '余额支付成功!'
                return dR
        except:
            dR['code'] = '1'
            dR['MSG'] = '更新订单数据及状态故障！'
            return dR

    def pay_order_status_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR

        sql = """select status,status_str,kuaid,wechat_user_id,ctype,ptid,ptkid,
                COALESCE(pt_type,0),phone  
            from wechat_mall_order where COALESCE(status,0)=1 and id=%s and usr_id=%s
            """
        l, t = self.db.select(sql, [id, self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        status, status_str, kuaid, wechat_user_id, ctype, ptid, ptkid, pt_type, phone = l[0]

        self.pay_time(5, '后台修改(线下支付)', id)
        self.update_pay_member(id)

        if str(ctype)=='0':
            try:
                if str(kuaid)=='0':

                    sql = "update wechat_mall_order set status=2,status_str='待发货'  where  id=%s and usr_id=%s "
                    self.db.query(sql, [id, self.usr_id_p])

                    self.write_order_log(id, 'wechat_mall_order:status和status_str',
                                         '订单状态:status:%s,status_str:%s' % (status,status_str), '修改为支付')
                    self.pay_order_detail_data(id, 2, '待发货')
                    dR['code'] = '0'
                    dR['MSG'] = '修改订单状态为待发货(已付款)成功!'
                    #self.oORDER_D.update(self.usr_id, wechat_user_id, id)
                    self.profit_record(wechat_user_id,id)
                    return dR

                elif str(kuaid)=='2':

                    sql = "update wechat_mall_order set status=6,status_str='待评价'  where  id=%s and usr_id=%s "
                    self.db.query(sql, [id, self.usr_id_p])
                    self.write_order_log(id, 'wechat_mall_order:status和status_str',
                                         '订单状态:status:%s,status_str:%s,kuaid:%s' % (status, status_str, kuaid), '修改支付,无需配送待评价货')
                    self.pay_order_detail_data(id, 6, '待评价')
                    dR['code'] = '0'
                    dR['MSG'] = '修改订单状态为待发货(已付款)成功!'
                    #self.oORDER_D.update(self.usr_id, wechat_user_id, id)
                    self.profit_record(wechat_user_id, id)
                    return dR

                else:

                    sql = "update wechat_mall_order set status=4,status_str='待自提'  where  id=%s and usr_id=%s "
                    self.db.query(sql, [id, self.usr_id_p])
                    self.write_order_log(id, 'wechat_mall_order:status和status_str',
                                         '订单状态:status:%s,status_str:%s,kuaid:%s' % (status, status_str,kuaid), '修改支付,自提单待自提')
                    self.pay_order_detail_data(id,4, '待自提')
                    dR['code'] = '0'
                    dR['MSG'] = '修改订单状态为待发货(已付款)成功!'
                    #self.oORDER_D.update(self.usr_id, wechat_user_id, id)
                    self.profit_record(wechat_user_id, id)
                    return dR

            except:
                dR['code'] = '1'
                dR['MSG'] = '更新订单数据及状态故障！'
                return dR
        elif str(ctype)=='2':
            try:
                if str(pt_type) == '0':  # 开团
                    self.Pingtuan_add(wechat_user_id, ptid, id, phone)
                elif str(pt_type) == '1':  # 参团
                    self.Pingtuan_join(wechat_user_id, ptkid, id, phone)
                dR['code'] = '0'
                dR['MSG'] = '修改订单状态,拼团处理完成!'
                return dR

            except:
                dR['code'] = '1'
                dR['MSG'] = '更新订单数据及状态故障！'
                return dR
        else:
            dR['code'] = '1'
            dR['MSG'] = '订单类型不对！'
            return dR


    def close_order_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR

        sql = """select COALESCE(new_total,0),status,status_str,coalesce(balance,0),wechat_user_id,order_num,coalesce(c_type,0),
                ctype,ptid,ptkid,COALESCE(pt_type,0),COALESCE(pay_status,0),to_char(ctime,'YYYY-MM-DD HH24:MI') 
                from wechat_mall_order where id=%s and usr_id=%s"""
        l, t = self.db.select(sql, [id, self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        new_total, status, status_str, balance, wechat_user_id, order_num, c_type, ctype, ptid, ptkid, pt_type, pay_status, ctime = \
        l[0]
        if status != 1 and status != 2 and status != 4:  # 待付款or待发货
            dR['code'] = '1'
            dR['MSG'] = '订单当前状态是:%s,不允许关闭'%status_str
            return dR

        if str(status) =='1':
            sql = "update wechat_mall_order set status=-1,status_str='已取消'  where  id=%s and usr_id=%s "
            self.db.query(sql, [id, self.usr_id_p])

            self.write_order_log(id, 'wechat_mall_order:status和status_str',
                                 '订单状态:status:%s,status_str:%s' % (status, status_str), '关闭订单')
            self.pay_order_detail_data(id, -1, '已取消')

        elif str(status) in ('2', '4'):  #待发货or待自提
            if str(ctype)=='0':
                if str(pay_status)=='1':#微信支付
                    try:
                        self.order_refund(self.usr_id_p, id, order_num, wechat_user_id)
                    except:
                        dR['code'] = '1'
                        dR['MSG'] = '订单微信退款失败!'
                        return dR
                elif str(pay_status)=='3':#组合支付
                    try:
                        self.order_refund(self.usr_id_p, id, order_num, wechat_user_id)
                    except:
                        dR['code'] = '1'
                        dR['MSG'] = '订单微信退款失败!'
                        return dR

                    if float(balance) > 0:
                        sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                        self.db.query(sql, [balance, self.usr_id_p, wechat_user_id])
                        self.user_log(self.usr_id, 'balance', '取消订单，balance:%s' % balance)
                        sql = """
                        insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                        values(%s,%s,3,'消费',%s,4,'退回',%s,'余额退回',%s,now())
                                """
                        self.db.query(sql, [self.usr_id_p, wechat_user_id, balance, order_num, self.usr_id])
                        self.oUSER.update(self.usr_id_p, wechat_user_id)
                else:  # 2余额支付4后台余额5后台修改
                    if new_total>0:
                        sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                        self.db.query(sql, [new_total, self.usr_id_p, wechat_user_id])
                        self.user_log(self.usr_id, 'balance', '取消订单，balance:%s' % new_total)
                        sql = """
                            insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                            values(%s,%s,3,'消费',%s,4,'退回',%s,'余额退回',%s,now())
                                    """
                        self.db.query(sql, [self.usr_id_p, wechat_user_id, new_total, order_num, self.usr_id])
                        self.oUSER.update(self.usr_id_p, wechat_user_id)
                    sql = "update wechat_mall_order set status=-1,status_str='已取消'  where  id=%s and usr_id=%s "
                    self.db.query(sql, [id, self.usr_id_p])

                    self.write_order_log(id, 'wechat_mall_order:status和status_str',
                                         '订单状态:status:%s,status_str:%s' % (status, status_str), '关闭订单')
                    self.pay_order_detail_data(id, -1, '已取消')

            elif str(ctype)=='2':
                try:
                    if str(pt_type) == '0':  # 开团
                        try:
                            self.Pingtuan_close(ptid, ptkid)
                        except:
                            dR['code'] = '1'
                            dR['MSG'] = '拼团订取消失败!'

                            return dR
                    else:#参团
                        dR['code'] = '1'
                        dR['MSG'] = '更新订单数据失败,拼团订单请关闭开团单!'

                        return dR

                except:
                    dR['code'] = '1'
                    dR['MSG'] = '更新订单数据及状态故障！'
                    return dR
            else:
                dR['code'] = '1'
                dR['MSG'] = '订单类型不允许关闭'
                return dR

        else:
            dR['code'] = '1'
            dR['MSG'] = '订单当前状态是:%s,不允许关闭'%status_str
            return dR



        try:
            if str(c_type) == '0':  # 推送取消订单消息
                sql = "select formid from wechat_formid where order_id=%s and coalesce(status,0)=0"
                lT1, iN1 = self.db.select(sql, id)
                if iN1 > 0:
                    prepay_id = lT1[0][0]
                    a = self.order_cancel_send(wechat_user_id, prepay_id, order_num, total=new_total, ctime=ctime,
                                               orderid=id)
                    if str(a.get('errcode', '')) == '0':
                        self.db.query("update wechat_mall_order set c_type=1 where id=%s ", id)
                        self.db.query("update wechat_formid set status=1,status_str='已使用' where order_id=%s ", id)
                    if str(a)=='1':
                        dR['code'] = '1'
                        dR['MSG'] = '更新订单状态成功，推送消息失败!'
                        return dR
        except:
            dR['code'] = '0'
            dR['MSG'] = '更新订单状态成功，推送消息失败!'
            return dR
        dR['code'] = '0'
        dR['MSG'] = '关闭订单成功!'
        return dR

    def order_shipments_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        sid = self.GP('sid', '')
        number = self.GP('number', '')

        if id == '' or sid == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR

        sql = "select wechat_user_id,order_num,coalesce(s_type,0) from wechat_mall_order where COALESCE(status,0) in (2,3) and id=%s and usr_id=%s"
        l, t = self.db.select(sql, [id, self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        wechat_user_id,order_num,s_type=l[0]
        if sid == '0':
            shipper_code = '0'
            shipper_str = '商家配送'
        else:
            sql = "select txt1,txt2 from mtc_t where type='KD' and id=%s"
            ll, tt = self.db.select(sql, sid)
            shipper_code, SH = ll[0]
            shipper_str = SH.replace('快递code:', '')
        try:
            sql = """update wechat_mall_order set shipper_id=%s,tracking_number=%s,status=5,status_str='待收货', 
                shipper_str=%s,shipper_code=%s where id=%s and usr_id=%s"""
            self.db.query(sql, [sid, number,shipper_str,shipper_code,id, self.usr_id_p])
            self.write_order_log(id, 'tracking_number', '快递公司:%s,单号:%s' % (sid, number), '发货')
            self.order_shipments_detail_data(id, sid, number, shipper_str)

        except:
            dR['code'] = '1'
            dR['MSG'] = '更新订单及发货状态故障！'
            return dR

        try:
            if str(s_type)=='0':#推送发货消息
                sql = "select prepay_id from wechat_mall_payment where COALESCE(status,0)=1 and order_id=%s"
                lT1,iN1=self.db.select(sql,id)
                if iN1>0:
                    prepay_id=lT1[0][0]
                    a = self.order_shipment_send(wechat_user_id, prepay_id, order_num, shipment=shipper_str,
                                                 shipmentcode=number, orderid=id)

                    if a == 1:
                        dR['code'] = '1'
                        dR['MSG'] = '推送消息失败!'
                        return dR
                    if a.get('errcode', '') == 0:
                        self.db.query("update wechat_mall_order set s_type=1 where id=%s ", id)
        except:
            dR['code'] = '0'
            dR['MSG'] = '更新订单状态成功，推送消息失败!'
            return dR
        #self.oORDER_D.update(self.usr_id, wechat_user_id, id)
        dR['code'] = '0'
        dR['MSG'] = '发货成功！'
        return dR

    def pay_order_detail_data(self,id,status,status_str):
        #后台手工处理支付后更新订单商品明细表数据
        sql="update wechat_mall_order_detail set status=%s,status_str=%s where order_id=%s and usr_id=%s"
        self.db.query(sql,[status,status_str,id,self.usr_id_p])

        return

    def order_shipments_detail_data(self,id,sid,number,shipper_str):

        #全部发货
        sql = """update wechat_mall_order_detail set shipper_id=%s,tracking_number=%s,shipper_time=now(),
                shipper_str=%s where order_id=%s and usr_id=%s and status=2"""
        self.db.query(sql, [sid, number, shipper_str,id, self.usr_id_p])
        sql = "update wechat_mall_order_detail set status=5,status_str='待收货' where order_id=%s and usr_id=%s and status=2"
        self.db.query(sql, [id, self.usr_id_p])

    def order_shipment_detail(self):
        #单个发货
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        sid = self.GP('sid', '')
        number = self.GP('number', '')

        if id == '' or sid == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        if sid == '0':
            shipper_str = '商家配送'
        else:
            sql = "select txt2 from mtc_t where type='KD' and id=%s"
            SH = self.db.fetchcolumn(sql, sid)
            shipper_str = SH.replace('快递code:', '')

        sql = "select order_id,order_num from wechat_mall_order_detail where COALESCE(status,0)=2 and id=%s and usr_id=%s"
        l, t = self.db.select(sql, [id, self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        order_id, order_num=l[0]
        ll,tt=self.db.select("select wechat_user_id,coalesce(s_type,0) from wechat_mall_order where id=%s  ",order_id)
        wechat_user_id,s_type=ll[0]
        try:

            sql = """update wechat_mall_order_detail set shipper_id=%s,tracking_number=%s,status=5,
                    status_str='待收货',shipper_str=%s,shipper_time=now() where id=%s and usr_id=%s"""
            self.db.query(sql, [sid, number,shipper_str, id, self.usr_id_p])
            sql = "update wechat_mall_order set status=3,status_str='部分发货' where id=%s and usr_id=%s"
            self.db.query(sql, [order_id, self.usr_id_p])
            self.write_order_log(id, 'tracking_number', '快递公司:%s,单号:%s' % (sid, number), '发货')
            sql="select id from wechat_mall_order_detail where order_id=%s and order_num=%s and status=2 and usr_id=%s"
            lT,iN=self.db.select(sql,[ order_id, order_num,self.usr_id_p])

            if iN==0:
                sql = "update wechat_mall_order set status=5,status_str='待收货' where id=%s and order_num=%s and usr_id=%s"
                self.db.query(sql, [order_id, order_num, self.usr_id_p])
                # sql = "update wechat_mall_order set status=5,status_str='待收货' where id=%s and usr_id=%s"
                # self.db.query(sql, [id, self.usr_id])
                self.write_order_log(id, 'wechat_mall_order', '单个发货并全部已发货,更新状态为待收货', '发货更新状态')

        except:
            dR['code'] = '1'
            dR['MSG'] = '更新订单状态故障！'
            return dR

        try:
            if str(s_type)=='0':#推送发货消息
                sql = "select prepay_id from wechat_mall_payment where COALESCE(status,0)=1 and order_id=%s"
                lT1, iN1 = self.db.select(sql, order_id)
                if iN1>0:
                    prepay_id=lT1[0][0]
                    a = self.order_shipment_send(wechat_user_id, prepay_id, order_num, shipment=shipper_str,
                                                 shipmentcode=number, orderid=order_id)

                    if a == 1:
                        dR['code'] = '1'
                        dR['MSG'] = '发货成功推送消息失败!'
                        return dR
                    if a.get('errcode', '') == 0:
                        self.db.query("update wechat_mall_order set s_type=1 where id=%s ", order_id)
        except:
            dR['code'] = '0'
            dR['MSG'] = '更新订单状态成功，推送消息失败!'
            return dR
        #self.oORDER_D.update(self.usr_id, wechat_user_id, id)

        dR['code'] = '0'
        dR['MSG'] = '发货成功！'
        return dR

    def pay_time(self,pay_status,pay_status_str,id):
        sql="update wechat_mall_order set pay_status=%s,pay_status_str=%s,pay_ctime=now() where id=%s and usr_id=%s "
        self.db.query(sql,[pay_status,pay_status_str,id,self.usr_id_p])
        return

    def update_pay_member(self,id):
        l,t=self.db.select("select ctype,order_num from wechat_mall_order where usr_id=%s and  id=%s",[self.usr_id_p,id])
        ctype, order_num=l[0]
        if str(ctype)=='1':
            # 修改订单状态
            sqlh = """
                update wechat_mall_order set status=5,status_str='已完成' where usr_id=%s and id=%s 
                    """
            self.db.query(sqlh, [self.usr_id_p, id])
            self.write_order_log(id, '购买会员', '后台处理付款,更新订单状态为已完成', '订单号:%s' % order_num)

    def order_after_data(self):#核销
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR

        sql = "select wechat_user_id from wechat_mall_order where COALESCE(status,0)=4 and id=%s and usr_id=%s"
        l, t = self.db.select(sql, [id, self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR
        wechat_user_id=l[0][0]
        try:
            sql = """update wechat_mall_order set check_id=1,status=6,status_str='待评价',
                    uid=%s,utime=now() where id=%s and usr_id=%s"""
            self.db.query(sql, [ self.usr_id,id,self.usr_id_p])
            sql = "update wechat_mall_order_detail set status=6,status_str='待评价' where order_id=%s and usr_id=%s"
            self.db.query(sql, [id, self.usr_id_p])
            self.write_order_log(id, 'pick_number', '后台核销订单状态改为待评价', '后台核销')
            #self.oORDER_D.update(self.usr_id, wechat_user_id, id)
        except:
            dR['code'] = '1'
            dR['MSG'] = '更新订单状态故障！'
            return dR
        dR['code'] = '0'
        dR['MSG'] = '核销成功！'
        return dR

    def profit_record(self,wid,id):#self.profit_record(wechat_user_id,id)#处理返现
        # 更新商品库存
        sql = """select good_id,amount,inviter_user,good_name,cid from wechat_mall_order_detail  
            where usr_id=%s and order_id=%s """
        lll, t = self.db.select(sql, [self.usr_id_p, id])
        for ii in lll:
            good_id, amountm, user, good_name, cid = ii
            self.oGOODS_D.updates(self.usr_id_p, good_id, amountm)
            self.oGOODS_N.update(self.usr_id_p, good_id)
            if str(user) != '0' and str(user) != str(cid):  # 下单返现
                good_D = self.oGOODS_D.get(self.usr_id_p, int(good_id))
                if good_D != {}:
                    shareInfo = good_D['shareInfo']
                    basicInfo = good_D['basicInfo']
                    share_type = shareInfo['share_type']
                    share_time = shareInfo['share_time']
                    share_number = shareInfo['share_number']

                    gname = basicInfo['name']
                    ticket_id = basicInfo['return_ticket']
                    if str(share_type) != '0' and str(share_time) == '2':  # 返现
                        if str(share_type) == '1' and share_number != '':  # 返现金
                            sql = """
                                update wechat_mall_user set balance=coalesce(balance,0)+%s 
                                where usr_id=%s and id=%s 
                                """
                            self.db.query(sql, [float(share_number), self.usr_id_p, cid])
                            sql = """
                                insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,
                                typeid,typeid_str,remark,goods_id,goods_name,cid,ctime)
                                values(%s,%s,2,'返现',%s,1,'分享返现','单次分享返现返',%s,%s,%s,now())
                                """
                            parm = [self.usr_id_p, user, float(share_number), good_id, gname, cid]
                            self.db.query(sql, parm)
                            sql = """
                                    insert into profit_record(usr_id,wechat_user_id,ctype,ctype_str,
                                    share_type,
                                    share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                    values(%s,%s,0,'现金收益',3,'好友下单返现',%s,%s,%s,%s,now())
                                    """
                            parm = [self.usr_id_p, user, float(share_number), good_id, gname, cid]
                            self.db.query(sql, parm)

                        elif str(share_type) == '2' and share_number != '':  # 返积分

                            sql = """
                                    update wechat_mall_user set score=coalesce(score,0)+%s 
                                    where usr_id=%s and id=%s 
                                            """
                            self.db.query(sql, [float(share_number), self.usr_id_p, cid])
                            sql = """
                                insert into integral_log(usr_id,wechat_user_id,type,typestr,in_out,
                                inoutstr,amount,cid,ctime)values(%s,%s,7,'分享返',0,'收入',%s,%s,now())
                                """
                            parm = [self.usr_id_p, good_id, float(share_number), cid]
                            self.db.query(sql, parm)
                            sql = """insert into profit_record(usr_id,wechat_user_id,ctype,
                                ctype_str,share_type,
                                    share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                    values(%s,%s,1,'积分收益',4,'好友下单返积分',%s,%s,%s,%s,now())
                                                """
                            parm = [self.usr_id_p, user, float(share_number), good_id, gname, cid]
                            self.db.query(sql, parm)

                        elif str(share_type) == '3' and ticket_id != '':  # 返优惠券

                            sql = """
                                select to_char(now(),'YYYY-MM-DD'),
                                    amount,to_char(dateend,'YYYY-MM-DD'),COALESCE(total,0),
                                    cname,remark,type_id,type_str,
                                case when type_id=1 then COALESCE(type_ext,'0') else '0' end type_ext,
                                    apply_id,apply_str,apply_ext_num,apply_ext_money,apply_goods_id,
                                    use_time,use_time_str,datestart,validday,icons,pics,remain_total
                                from coupons 
                                where usr_id=%s and COALESCE(del_flag,0)=0 and id=%s
                                                """
                            parm = [self.usr_id_p, ticket_id]
                            l, n = self.db.select(sql, parm)
                            if n > 0:
                                now_, max_num, dateend, total, cname, remark, type_id, type_str, type_ext = \
                                    l[0][0:9]
                                apply_id, apply_str, apply_ext_num, apply_ext_money, apply_goods_id, use_time, use_time_str = \
                                    l[0][9:16]
                                datestart, validday, icons, pics, remain_total = l[0][16:]
                                if now_ < dateend and int(remain_total) != int(total):

                                    if str(apply_id) == '1':
                                        change_money = float(apply_ext_num) / 100
                                    else:
                                        change_money = apply_ext_num

                                    data = {
                                        'usr_id': self.usr_id_p,
                                        'wechat_user_id': cid,
                                        'm_id': ticket_id,
                                        'cname': cname,
                                        'type_id': type_id,
                                        'type_str': type_str,
                                        'type_ext': type_ext,
                                        'remark': remark,
                                        'icons': icons,
                                        'pics': pics,
                                        'goods_id': apply_goods_id,
                                        'datestart': datestart or None,
                                        'date_end': dateend or None,
                                        'apply_id': apply_id or None,
                                        'apply_str': apply_str,
                                        'apply_ext_num': apply_ext_num or None,
                                        'apply_ext_money': apply_ext_money or None,
                                        'use_time': use_time or None,
                                        'use_time_str': use_time_str,
                                        'validday': validday or None,
                                        'cid': self.usr_id,
                                        'ctime': self.getToday(9),
                                        'good_id': good_id,
                                        're_status': 1

                                    }

                                    self.db.insert('my_coupons', data)
                                    sql = """update coupons set remain_total=COALESCE(remain_total,0)+1 
                                                            where id=%s"""
                                    self.db.query(sql, ticket_id)
                                    sql = """insert into profit_record(usr_id,wechat_user_id,ctype,
                                            ctype_str,share_type,
                                            share_type_str,change_money,goods_id,goods_name,cid,ctime,ticket_id)
                                            values(%s,%s,2,'优惠券收益',5,'好友下单返优惠券',%s,%s,%s,%s,now(),%s)
                                                """
                                    parm = [self.usr_id_p, user, change_money, good_id, gname, cid, ticket_id]
                                    self.db.query(sql, parm)
        self.oUSER.update(self.usr_id_p, wid)

    def Pingtuan_add(self, wechat_user_id,ptid, order_id,phone):
        sqlw = """select id from wechat_mall_order 
                where ctype=2  and usr_id=%s and wechat_user_id=%s and id=%s and coalesce(pay_status,0)!=0
                """
        lT,iN=self.db.select(sqlw,[self.usr_id_p,wechat_user_id,order_id])
        if iN==0:
            return

        try:
            cur_random_no = "%s%s" % (time.time(), random.random())
            oUSER = self.oUSER.get(self.usr_id_p, wechat_user_id)
            name = oUSER['name']
            avatar = oUSER['avatar']
            #self.print_log('subusr_id:%s,ptid:%s'%(self.subusr_id, ptid),'%s'%self.oPT_GOODS.get(self.subusr_id))
            oPT_GOODS = self.oPT_GOODS.get(self.usr_id_p, ptid)
            number = oPT_GOODS['cnumber']
            gid = oPT_GOODS['gid']
            gname = oPT_GOODS['gname']
            gintr = oPT_GOODS['gintr']
            gpic = oPT_GOODS['gpic']
            gcontent = oPT_GOODS['gcontent']
            ptprice =oPT_GOODS['pt_price']
            mnprice = oPT_GOODS['mini_price']
            stores = oPT_GOODS['stores']
            ok_type=oPT_GOODS['ok_type']
            add_type=oPT_GOODS['add_type']
            tk_type=oPT_GOODS['tk_type']
            kt_type = oPT_GOODS['kt_type']
            timeout_h = oPT_GOODS['timeout_h']

            cnow = datetime.datetime.now()
            #ctime = now.strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(hours=int(timeout_h))
            n_days = cnow + delta
            date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

            data = {
                'usr_id': self.usr_id_p,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'order_id': order_id,
                'name': name,
                'avatar': avatar,
                'number': number,
                'short': number - 1,
                'phone': phone,
                'status': 1,
                'ok_type':ok_type,
                'add_type':add_type,
                'tk_type':tk_type,
                'kt_type':kt_type,
                'date_end': date_end,
                'gid': gid,
                'gname': gname,
                'gintr': gintr,
                'gpic': gpic,
                'gcontent': gcontent,
                'ptprice':ptprice,
                'mnprice':mnprice,
                'stores':stores,
                'random_no': cur_random_no,
                'cid': wechat_user_id,
                'ctime': self.getToday(9)

            }
            self.db.insert('open_pt', data)
            opid = self.db.fetchcolumn("select id from open_pt where random_no=%s", cur_random_no)
            sqlo="""
                update wechat_mall_order set ptkid=%s,status=10,status_str='拼团中' where usr_id=%s and id=%s 
                        """
            self.db.query(sqlo,[opid,self.usr_id_p,order_id])
            sqld= """
                update wechat_mall_order_detail set 
                status=10,status_str='拼团中' where usr_id=%s and order_id=%s; 
                """
            self.db.query(sqld,[self.usr_id_p, order_id])
            datad = {
                'usr_id': self.usr_id_p,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'opid': opid,
                'order_id':order_id,
                'name': name,
                'avatar': avatar,
                'phone': phone,
                'title': 1,
                'status': 1,
                'date_end': date_end,
                'cid': wechat_user_id,
                'ctime': self.getToday(9)
            }
            self.db.insert('open_pt_detail', datad)
            return
        except:
            self.print_log('subusr_id:%s,ptid:%s' % (self.usr_id_p, ptid), '%s' % self.oPT_GOODS.get(self.usr_id_p))
            self.print_log('拼团失败', '%s' % str(traceback.format_exc()))
            self.Pingtuan_add_close(order_id)
            return

    def Pingtuan_add_close(self, order_id):#开团数据处理失败进行拼团失败处理

        lT,iN = self.db.select("select id from open_pt where usr_id=%s and  order_id=%s", [self.usr_id_p,order_id])
        if iN>0:
            return

        sqlw = """select id from wechat_mall_order 
                        where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                        """
        lT, iN = self.db.select(sqlw, [self.usr_id_p, order_id])
        if iN == 0:
            return

        sqld = """
            update wechat_mall_order set 
            status=11,status_str='拼团失败' where usr_id=%s and id=%s;
             update wechat_mall_order_detail set 
            status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
            """
        self.db.query(sqld, [self.usr_id_p, order_id, self.usr_id_p, order_id])
        self.write_order_log(order_id, '开团失败', '更新订单状态为拼团失败',
                             '订单id:%s' % order_id)
        return

    def Pingtuan_join(self, wechat_user_id, ptkid,order_id,phone):
        #self.print_log('order_id:%s'%order_id,'ptkid:%s'%ptkid)
        sqlw = """select id from wechat_mall_order 
                                where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                                """
        lT, iN = self.db.select(sqlw, [self.usr_id_p, order_id])
        if iN == 0:
            return
        try:
            sql="select ptid,number,short from open_pt where usr_id=%s and id=%s and coalesce(status,0)=1"
            l,t=self.db.select(sql,[self.usr_id_p,ptkid])
            if t==0:
                sqld = """
                    update wechat_mall_order set 
                    status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                     update wechat_mall_order_detail set 
                    status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                    """
                self.db.query(sqld, [self.usr_id_p, order_id,self.usr_id_p, order_id])
                self.write_order_log(order_id, '拼团成功', '更新订单状态为待发货',
                                     '订单id:%s'%order_id)
                return
            ptid, number, short = l[0]

            oUSER = self.oUSER.get(self.usr_id_p, wechat_user_id)
            name = oUSER['name']
            avatar = oUSER['avatar']

            #self.print_log('number:%s'%number,'short:%s'%short)
            oPT_GOODS = self.oPT_GOODS.get(self.usr_id_p, ptid)
            timeout_h = oPT_GOODS['timeout_h']
            cnow = datetime.datetime.now()
            # ctime = now.strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(hours=int(timeout_h))
            n_days = cnow + delta
            date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

            datad = {
                'usr_id': self.usr_id_p,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'opid': ptkid,
                'order_id':order_id,
                'name': name,
                'avatar': avatar,
                'phone': phone,
                'title': 2,
                'status': 1,
                'date_end': date_end,
                'cid': wechat_user_id,
                'ctime': self.getToday(9)
            }
            self.db.insert('open_pt_detail', datad)
            self.db.query("update open_pt set short=short-1 where id=%s and usr_id=%s",[ptkid,self.usr_id_p])

            sqlo="""
                update wechat_mall_order set ptid=%s,status=10,status_str='拼团中' where usr_id=%s and id=%s 
                """
            self.db.query(sqlo,[ptid,self.usr_id_p,order_id])

            sqld= """
                update wechat_mall_order_detail set 
                status=10,status_str='拼团中' where usr_id=%s and order_id=%s; 
                """
            self.db.query(sqld,[self.usr_id_p, order_id])

            if int(short)==1:
                self.db.query("update open_pt set status=2 where id=%s and usr_id=%s", [ptkid,self.usr_id_p])
                self.db.query("update open_pt_detail set status=2 where opid=%s and usr_id=%s", [ptkid,self.usr_id_p])
                ############处理订单状态
                sqlp = "select id,kuaid from wechat_mall_order where usr_id=%s and ptkid=%s and ctype=2 and status=10"
                l, t = self.db.select(sqlp, [self.usr_id_p, ptkid])
                if t>0:
                    for i in l:
                        orderdid,kuaid = i
                        if str(kuaid) == '0':#快递单
                            sqld = """
                                update wechat_mall_order set 
                                status=2,status_str='待发货' where usr_id=%s and id=%s;
                                 update wechat_mall_order_detail set 
                                status=2,status_str='待发货' where usr_id=%s and order_id=%s; 
                                """
                            self.db.query(sqld, [self.usr_id_p, orderdid,self.usr_id_p, orderdid])
                            self.write_order_log(orderdid, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s'%orderdid)


                        elif str(kuaid) == '1':#自提单
                            sqld = """
                                    update wechat_mall_order set 
                                        status=4,status_str='待自提' where usr_id=%s and id=%s; 
                                    update wechat_mall_order_detail set 
                                        status=4,status_str='待自提' where usr_id=%s and order_id=%s; 
                                    """
                            self.db.query(sqld, [self.usr_id_p, orderdid,self.usr_id_p, orderdid])
                            self.write_order_log(order_id, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s'%orderdid)

                        elif str(kuaid) == '2':#无须配送
                            sqld = """
                                    update wechat_mall_order set 
                                        status=6,status_str='待评价' where usr_id=%s and id=%s;
                                    update wechat_mall_order_detail set 
                                        status=6,status_str='待评价' where usr_id=%s and order_id=%s; 
                                    """
                            self.db.query(sqld, [self.usr_id_p, orderdid,self.usr_id_p, orderdid])
                            self.write_order_log(order_id, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s'%orderdid)

            return
        except:
            self.print_log('参团失败', '%s' % str(traceback.format_exc()))
            self.Pingtuan_join_close(order_id)
            return

    def Pingtuan_join_close(self, order_id):#参团数据处理失败进行拼团失败处理

        lT,iN = self.db.select("select id from open_pt_detail where usr_id=%s and  order_id=%s", [self.usr_id_p,order_id])
        if iN>0:
            return

        sqlw = """select id from wechat_mall_order 
                        where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                        """
        lT, iN = self.db.select(sqlw, [self.usr_id_p, order_id])
        if iN == 0:
            return

        sqld = """
            update wechat_mall_order set 
            status=11,status_str='拼团失败' where usr_id=%s and id=%s;
             update wechat_mall_order_detail set 
            status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
            """
        self.db.query(sqld, [self.usr_id_p, order_id, self.usr_id_p, order_id])
        self.write_order_log(order_id, '参团失败', '更新订单状态为拼团失败',
                             '订单id:%s' % order_id)
        return

    def Pingtuan_close(self, ptid, ptkid):  # 拼团订单取消处理
        sql = "select id from open_pt where usr_id=%s and id=%s and ptid=%s"
        lT, iN = self.db.select(sql, [self.usr_id_p, ptkid, ptid])
        if iN == 0:
            return
        sqlo = "update open_pt set status=3 where usr_id=%s and id=%s and ptid=%s "
        self.db.query(sqlo, [self.usr_id_p, ptkid, ptid])

        sqlw = """select id from wechat_mall_order 
                        where ctype=2  and usr_id=%s and ptid=%s and ptkid=%s
                        """
        lT1, iN1 = self.db.select(sqlw, [self.usr_id_p, ptid, ptkid])
        if iN1 == 0:
            return
        for i in lT1:
            order_id = i[0]
            sqld = """
                update wechat_mall_order set 
                status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                 update wechat_mall_order_detail set 
                status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                """
            self.db.query(sqld, [self.usr_id_p, order_id, self.usr_id_p, order_id])
            self.write_order_log(order_id, '参团失败', '更新订单状态为拼团失败',
                                 '订单id:%s' % order_id)
        return

    def editmemo_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        memo = self.GP('memo', '')
        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR

        sql = """select id   from wechat_mall_order where id=%s and usr_id=%s
            """
        l, t = self.db.select(sql, [id, self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '数据不存在！'
            return dR

        try:
            sql = "update wechat_mall_order set memo=%s where id=%s and usr_id=%s"
            self.db.query(sql, [memo, id, self.usr_id_p])
            dR['code'] = '0'
            dR['MSG'] = '修改卖家备注成功!'
            return dR

        except:
            dR['code'] = '1'
            dR['MSG'] = '修改卖家备注失败！'
            return dR

    def export_excel_data(self):

        sql = """
           select u.cname as wname,w.cname,w.phone,w.province,w.city,w.district,w.address,w.code,w.logistics_price,
           pay_status_str,w.order_num,
        (select array_to_json(array_agg(row_to_json(t)))
            from (
              select good_name from wechat_mall_order_detail d where d.order_id=w.id    ) t)goodname
        from wechat_mall_order w 
        left join wechat_mall_user u on u.usr_id=w.usr_id and  w.wechat_user_id =u.id
        where  w.status in (2,3) and w.usr_id=%s
                """

        parm = [self.usr_id_p]
        l, t = self.db.select(sql, parm)
        return l

    def allexcel_data(self):

        sql = """
           select u.cname as wname,w.cname,w.phone,w.province,w.city,w.district,w.address,w.code,w.logistics_price,
           pay_status_str,w.order_num,w.status_str,
           (select array_to_json(array_agg(row_to_json(t)))
            from (
              select good_name,property_str from wechat_mall_order_detail d where d.order_id=w.id    ) t)goodname
        from wechat_mall_order w 
        left join wechat_mall_user u on u.usr_id=w.usr_id and  w.wechat_user_id =u.id
        where   w.usr_id=%s
                """
        if str(self.tab) == '2':
            sql += " and w.status=1 "
        elif str(self.tab) == '3':
            sql += " and w.status=2 "
        elif str(self.tab) == '4':
            sql += " and w.status=3 "
        elif str(self.tab) == '5':
            sql += " and w.status=5 "
        elif str(self.tab) == '6':
            sql += " and w.status=4 "
        elif str(self.tab) == '7':
            sql += " and w.status=7 "
        elif str(self.tab) == '8':
            sql += " and w.status=-1 "
        # print(self.tab)
        sql += " order by w.id desc limit 5000; "
        parm = [self.usr_id_p]
        l, t = self.db.select(sql, parm)
        return l

    def excel_import(self):
        from random import Random
        import os
        import time
        # from flask import request

        random_code = str(Random(time.time()).random())[2:]
        dR = {'code': '', 'MSG': ''}

        F1 = self.objHandle.files.get('excel', '')

        fc = F1.read()
        TEMP_PATH = self.PEM_ROOTR
        self.make_sub_path(TEMP_PATH)
        file = os.path.join(TEMP_PATH, '%s.xls' % random_code)
        #self.file = file
        f = open(file, 'wb')
        f.write(fc)
        f.flush()
        f.close()

        import xlrd

        try:
            data = xlrd.open_workbook(file)
        except:
            dR['code'] = '1'
            dR['MSG'] = "无法识别的EXCEL文件，请上传正确的EXCEL文件！"
            return dR

        sh = data.sheet_by_index(0)
        nrows = sh.nrows
        ncols = sh.ncols
        L = []
        if nrows == 2:
            dR['code'] = '1'
            dR['MSG'] = '缺少表头或内容,请遵循模板样式，第一、二行为表头，第三行开始为导入内容'
            return dR

        for n in range(nrows)[2:]:
            if n > 0:
                L1 = []
                for m in range(ncols)[:3]:
                    s = sh.cell_value(rowx=n, colx=m)
                    #ss = sh.cell(rowx=n, colx=m)
                    # print s
                    # if (ss.ctype == 3):
                    #    date_value = xlrd.xldate_as_tuple(s,data.datemode)
                    #    s = date(*date_value[:3]).strftime('%Y-%m-%d')

                    try:
                        s = str(s).replace('"', "").replace("'", "")
                    except:
                        pass

                    L1.append(s)
                L.append(L1)

        MSG = []
        if len(L) == 0:
            MSG.append("没有数据")

        sql = ''
        for R in L:

            order_num, shipperid, tracking_number = R  # 订单号,快递公司id,快递单号
            sqlc = "select id from wechat_mall_order where status=2 and order_num=%s and usr_id=%s"
            l, t = self.db.select(sqlc, [order_num, self.usr_id_p])
            if t > 0:

                order_id = l[0][0]
                shipper_str = '商家配送'
                shipper_code = '0'
                shipper_id = str(shipperid).split('.')[0]
                if int(shipper_id) != 0:
                    sqlt = "select txt1,txt2 from mtc_t where type='KD' and id=%s"
                    ll, tt = self.db.select(sqlt, [int(shipper_id)])
                    shipper_code, SH = ll[0]
                    shipper_str = SH.replace('快递code:', '')
                sql += """
                        update wechat_mall_order set shipper_id=%s,tracking_number='%s',status=5,status_str='待收货', 
                        shipper_time=now(),shipper_str='%s',shipper_code='%s' where id=%s and usr_id=%s and status=2;
                        update wechat_mall_order_detail set shipper_id=%s,tracking_number='%s',shipper_time=now(),
                            shipper_str='%s',status=5,status_str='待收货' where order_id=%s and usr_id=%s and status=2;
                            """ % (
                    int(shipper_id), tracking_number, shipper_str, shipper_code, order_id, self.usr_id_p,
                    int(shipper_id),
                    tracking_number, shipper_str, order_id, self.usr_id_p)

        if sql != '':
            self.db.query(sql)

        j = 1
        if len(MSG) >= 20:
            for m in MSG:
                if j <= 20:
                    dR['MSG'] += str(m) + '<br/>'
                    j += 1
                else:
                    dR['MSG'] += '...'
        else:
            for m in MSG:
                dR['MSG'] += str(m) + '<br/>'
        os.remove(file)
        if dR['MSG'] == '':
            dR['MSG'] = '处理成功!'
        return dR

    def order_refund_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR

        sql = """select COALESCE(balance,0),new_total,wechat_user_id,
                coalesce(pay_status,0),order_num,coalesce(ctype,0),coalesce(pt_type,0),
                 coalesce(ptid,0),coalesce(ptkid,0)
            from wechat_mall_order 
            where COALESCE(status,0) in (2,4) and id=%s and usr_id=%s"""
        l, t = self.db.select(sql, [id, self.usr_id_p])
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '退款单状态不正常'
            return dR
        balance, new_total, wechat_user_id, pay_status, order_num, ctype, pt_type, ptid, ptkid = l[0]
        sql = "update wechat_mall_order set status=98,status_str='退款成功' where usr_id=%s and id=%s"
        self.db.query(sql, [self.usr_id_p, id])
        sql = "update wechat_mall_order_detail set status=98,status_str='退款成功' where usr_id=%s  and order_id=%s"
        self.db.query(sql, [self.usr_id_p, id])
        self.write_order_log(id, 'status,status_str', 'status=98,status_str=退款成功', '未发货或未自提，后台操作退款,更新订单表,订单明细表状态')
        if str(ctype) == '0':
            if str(pay_status) == '1':  # 微信支付
                try:
                    self.order_refund(self.usr_id_p, id, order_num, wechat_user_id)
                except:
                    dR['code'] = '1'
                    dR['MSG'] = '订单微信退款失败!'
                    return dR
            elif str(pay_status) == '3':  # 组合支付
                try:
                    self.order_refund(self.usr_id_p, id, order_num, wechat_user_id)
                except:
                    dR['code'] = '1'
                    dR['MSG'] = '订单微信退款失败!'
                    return dR

                if float(balance) > 0:
                    sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where usr_id=%s and id=%s"
                    self.db.query(sql, [balance, self.usr_id_p, wechat_user_id])
                    self.user_log(self.usr_id, 'balance', '取消订单，balance:%s' % balance)
                    sql = """
                    insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                    values(%s,%s,3,'消费',%s,4,'退回',%s,'余额退回',%s,now())
                            """
                    self.db.query(sql, [self.usr_id_p, wechat_user_id, balance, order_num, self.usr_id])
                    self.oUSER.update(self.usr_id_p, wechat_user_id)
            else:  # 2余额支付4后台余额5后台修改
                sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                self.db.query(sql, [new_total, self.usr_id_p, wechat_user_id])
                self.user_log(self.usr_id, 'balance', '取消订单，balance:%s' % new_total)
                sql = """
                    insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                    values(%s,%s,3,'消费',%s,4,'退回',%s,'余额退回',%s,now())
                            """
                self.db.query(sql, [self.usr_id_p, wechat_user_id, new_total, order_num, self.usr_id])
                self.oUSER.update(self.usr_id_p, wechat_user_id)


        elif str(ctype) == '2':
            try:
                if str(pt_type) == '0':  # 开团
                    try:
                        self.Pingtuan_close(ptid, ptkid)
                    except:
                        dR['code'] = '1'
                        dR['MSG'] = '拼团订取消失败!'
                        return dR
                else:  # 参团
                    dR['code'] = '1'
                    dR['MSG'] = '更新订单数据失败,拼团订单请关闭开团单!'

                    return dR

            except:
                dR['code'] = '1'
                dR['MSG'] = '更新订单数据及状态故障！'
                return dR
        else:
            dR['code'] = '1'
            dR['MSG'] = '订单类型不允许关闭'
            return dR

        if str(pay_status) == '1':  # 微信支付
            pass
        elif str(pay_status) == '2':  # 抵扣支付
            if balance == new_total:
                sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
                self.db.query(sql, [new_total, wechat_user_id])
            else:
                dR['code'] = '1'
                dR['MSG'] = '抵扣支付数据异常，请联系平台管理'
                return dR
        elif str(pay_status) == '3':  # 组合支付

            sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
            self.db.query(sql, [new_total, wechat_user_id])
            a = self.order_refund(id, order_num,
                                  wechat_user_id)  # order_refund(self, subusr_id, order_id, order_num, wechat_user_id):
            if a == 1:
                dR['code'] = '1'
                dR['MSG'] = '退款操作失败!'
                return dR

        elif str(pay_status) == '4':  # 后台支付
            sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
            self.db.query(sql, [new_total, wechat_user_id])

        sql = """insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,remark,
                        cid,ctime)values(%s,%s,3,'消费',%s,4,'退回','退款',%s,now())"""
        self.db.query(sql, [self.usr_id_p, wechat_user_id, new_total, self.usr_id])
        self.oUSER.update(self.usr_id_p, wechat_user_id)
        dR['code'] = '0'
        dR['MSG'] = '退款操作完成!'
        return dR
