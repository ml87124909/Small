# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""wxpay/WxPay.py"""
import hashlib
import datetime
import time
import traceback
import random
from lxml import etree
from basic.publicw import db,oUSER,oGOODS_D,oGOODS_N,oPT_GOODS,oMALL
#db,subid,xml_data,
class cmPay:

    def __init__(self, request):

        self.objHandle = request
        self.subid=1
        self.db = db
        self.oUSER=oUSER
        self.oGOODS_D=oGOODS_D
        self.oGOODS_N=oGOODS_N
        self.oPT_GOODS=oPT_GOODS
        self.oMALL=oMALL


    def Webpage(self):

        try:
            data = self.to_dict(self.objHandle.data)
            # print_log(db, '微信支付回调', '6666666666')
            if not self.check(data):
                self.print_log('微信支付签名验证失败', '%s' % data)
                return self.reply("签名验证失败", False)

            sql = "select usr_id from users where usr_id=%s "
            l, t = self.db.select(sql, self.subid)
            if t == 0:
                self.print_log('微信支付商家用户不存在', '%s'% data)
                return self.reply("数据不存在", False)

            if data['return_code'] == 'SUCCESS' and data['result_code'] == 'SUCCESS':
                out_trade_no = data['out_trade_no']
                me = int(data['total_fee']) / 100
                self.print_log( 'wechat_mall_payment测试:','%s,%s,%s' % (out_trade_no, data['total_fee'], self.subid))
                sql = """select id,order_num,ctype from wechat_mall_payment 
                        where payment_number=%s and coalesce(status,0)=0 and total_fee=%s and usr_id=%s
                        """
                l, t = self.db.select(sql, [out_trade_no, data['total_fee'], self.subid])
                # print_log(db, 'wechat_mall_payment测试:%s' % i,'%s,%s,%s' % (out_trade_no, data['total_fee'], subid))
                if t == 0:
                    self.print_log('微信支付数据不存在', '%s' % data)
                    return self.reply("数据不存在", False)

                id, order_num, ctype = l[0]
                if str(ctype) == '6':
                    sql = "select wechat_user_id from offline_pay where order_num=%s and usr_id=%s "
                    k, r = self.db.select(sql, [out_trade_no, self.subid])
                    if r == 0:
                        self.print_log('微信支付数据不存在', '%s' % data)
                        return self.reply("数据不存在", False)
                    try:
                        uid = k[0][0]
                    except:
                        uid = 0
                    payment = {
                        'openid': data.get('openid')  # = fields.Char('openid')
                        , 'result_code': data['result_code']  # = fields.Char('业务结果')
                        , 'transaction_id': data['transaction_id']  # = fields.Char('微信订单号')
                        , 'bank_type': data['bank_type']  # = fields.Char('付款银行')
                        , 'fee_type': data['fee_type']  # = fields.Char('货币种类')
                        , 'total_fee': data['total_fee']  # = fields.Integer('订单金额(分)')
                        , 'cash_fee': data['cash_fee']  # = fields.Integer('现金支付金额')
                        , 'status': 1
                        , 'status_str': '成功'
                        , 'uid': uid
                        , 'utime': self.getToday(9)
                        , 'renoncestr': data['nonce_str']
                        , 'time_end': data['time_end']
                        #, 'sign': data['sign']

                    }

                    self.db.update("wechat_mall_payment", payment,
                              "payment_number='%s' and usr_id=%s" % (out_trade_no, self.subid))

                    score = 0
                    # 赠送积分
                    sql = "select COALESCE(integral,0),COALESCE(vip_integral,0) from shop_set where usr_id=%s"
                    l, t = self.db.select(sql, [self.subid])
                    if t > 0:
                        integral, vip_integral = l[0]
                        User = self.oUSER.get(self.subid, uid)
                        vip_level = User.get('vip_level', '0')
                        if str(vip_level) == '0':
                            score = float(me) * integral
                        else:
                            score = float(me) * vip_integral

                        sql = "update wechat_mall_user set score=COALESCE(score,0)+%s where usr_id=%s and id=%s"
                        self.db.query(sql, [score, self.subid, uid])
                        self.user_log(uid, '扫码支付回调增加积分', 'score:%s' % score)

                    sql = """update offline_pay set 
                        status=1,utime=now(),paytime=now(),score=%s where usr_id=%s and order_num=%s"""
                    self.db.query(sql, [score, self.subid, out_trade_no])

                elif str(ctype) == '5':
                    sql = "select id,wechat_user_id from top_up where order_no=%s and usr_id=%s "
                    k, r = self.db.select(sql, [out_trade_no, self.subid])
                    if r == 0:
                        self.print_log('微信支付数据不存在', '%s' % data)
                        return self.reply("数据不存在", False)
                    try:
                        uid = k[0][1]
                    except:
                        uid = 0
                    payment = {
                        'openid': data.get('openid')  # = fields.Char('openid')
                        , 'result_code': data['result_code']  # = fields.Char('业务结果')
                        , 'transaction_id': data['transaction_id']  # = fields.Char('微信订单号')
                        , 'bank_type': data['bank_type']  # = fields.Char('付款银行')
                        , 'fee_type': data['fee_type']  # = fields.Char('货币种类')
                        , 'total_fee': data['total_fee']  # = fields.Integer('订单金额(分)')
                        , 'cash_fee': data['cash_fee']  # = fields.Integer('现金支付金额')
                        , 'status_str': '成功'
                        , 'status': 1
                        , 'uid': uid
                        , 'utime': self.getToday(9)
                        , 'renoncestr': data['nonce_str']
                        , 'time_end': data['time_end']
                        #, 'sign': data['sign']

                    }

                    self.db.update("wechat_mall_payment", payment,
                              "payment_number='%s' and usr_id=%s" % (out_trade_no, self.subid))

                    sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                            values(%s,%s,%s,%s,%s,now())
                                                        """
                    self.db.query(sql, [self.subid, 'wechat_mall_payment', 'payment_number:%s' % out_trade_no,
                                   '支付回调更新wechat_mall_payment表数据', self.subid])

                    sqld = "update top_up set status=7,status_str='已完成',uid=0,utime=now() where order_no=%s"
                    self.db.query(sqld, out_trade_no)
                    real_money = float(me)
                    give = 0
                    sql = "select giving from  gifts where add_money<=%s and usr_id=%s order by add_money desc limit 1 "
                    lT, iN = self.db.select(sql, [me, self.subid])
                    if iN > 0:
                        give = lT[0][0]
                        real_money += float(give)

                    cash_dict = {
                        'wechat_user_id': uid,
                        'cid': uid,
                        'ctime': self.getToday(9),
                        'usr_id': self.subid,
                        'real_money': real_money,  # 实际到帐
                        'cnumber': data['out_trade_no'],
                        'status': '5',
                        'status_str': '已完成',
                        'change_money': me,  # 充值
                        'ctype': '1',
                        'ctype_str': '充值',
                        'pay_ctime': self.getToday(9),
                        'give': give

                    }
                    self.db.insert('cash_log', cash_dict)
                    sql = "update wechat_mall_user set balance =coalesce(balance,0)+%s where id=%s"
                    self.db.query(sql, [real_money, uid])
                    self.oUSER.update(self.subid, uid)


                elif str(ctype) == '1':
                    sql = "select id,wechat_user_id from vip_member where order_no=%s and usr_id=%s "
                    lT, iN = self.db.select(sql, [out_trade_no, self.subid])
                    if iN == 0:
                        self.print_log('微信支付数据不存在', '%s' % data)
                        return self.reply("数据不存在", False)
                    try:
                        uid = lT[0][1]
                    except:
                        uid = 0
                    payment = {
                        'openid': data.get('openid')  # = fields.Char('openid')
                        , 'result_code': data['result_code']  # = fields.Char('业务结果')
                        , 'transaction_id': data['transaction_id']  # = fields.Char('微信订单号')
                        , 'bank_type': data['bank_type']  # = fields.Char('付款银行')
                        , 'fee_type': data['fee_type']  # = fields.Char('货币种类')
                        , 'total_fee': data['total_fee']  # = fields.Integer('订单金额(分)')
                        , 'cash_fee': data['cash_fee']  # = fields.Integer('现金支付金额')
                        , 'status': 1
                        , 'status_str': '成功'
                        , 'uid': uid
                        , 'utime': self.getToday(9)
                        , 'renoncestr': data['nonce_str']
                        , 'time_end': data['time_end']
                        #, 'sign': data['sign']

                    }

                    self.db.update("wechat_mall_payment", payment,
                              "payment_number='%s' and usr_id=%s" % (out_trade_no, self.subid))

                    sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                                values(%s,%s,%s,%s,%s,now())
                                                            """
                    self.db.query(sql, [self.subid, 'wechat_mall_payment', 'payment_number:%s' % out_trade_no,
                                   '支付回调更新wechat_mall_payment表数据', self.subid])

                    sqld = "update vip_member set status=7,status_str='已完成',uid=0,utime=now() where order_no=%s"
                    self.db.query(sqld, out_trade_no)
                    sql = " select hy_flag,to_char(hy_etime,'YYYY-MM-DD HH24:MI') from wechat_mall_user where id=%s"
                    ll, tt = db.select(sql, uid)
                    hy_flag, hyetime = ll[0]
                    if str(hy_flag) == '1':
                        now = datetime.datetime.strptime(hyetime, "%Y-%m-%d %H:%M")
                        delta = datetime.timedelta(days=365)
                        n_days = now + delta
                        hy_etime = n_days.strftime('%Y-%m-%d %H:%M:%S')

                        sqlh = "update wechat_mall_user set hy_etime=%s where usr_id =%s and id=%s"
                        self.db.query(sqlh, [hy_etime, self.subid, uid])
                        sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                                values(%s,%s,%s,%s,%s,now())
                                                            """
                        self.db.query(sql, [self.subid, 'wechat_mall_user', "id:%s,hy_flag=1" % uid,
                                       '会员服务支付回调更新wechat_mall_user表数据', self.subid])

                        self.oUSER.update(self.subid, uid)
                        return self.reply("OK", True)

                    now = datetime.datetime.now()
                    delta = datetime.timedelta(days=365)
                    n_days = now + delta
                    hy_etime = n_days.strftime('%Y-%m-%d %H:%M:%S')
                    sqlh = "update wechat_mall_user set hy_flag=1,hy_ctime=now(),hy_etime=%s where usr_id =%s and id=%s"
                    self.db.query(sqlh, [hy_etime, self.subid, uid])
                    sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                        values(%s,%s,%s,%s,%s,now())
                    """
                    self.db.query(sql, [self.subid, 'wechat_mall_user', "id:%s,hy_flag=1" % uid,
                                   '会员服务支付回调更新wechat_mall_user表数据', self.subid])

                    self.oUSER.update(self.subid, uid)

                else:
                    mn = "select id,wechat_user_id from wechat_mall_order where  order_num=%s and usr_id=%s"
                    m, n = self.db.select(mn, [order_num, self.subid])
                    if n == 0:
                        self.print_log('微信支付数据不存在', '%s' % data)
                        return self.reply("数据不存在", False)
                    try:
                        uid = m[0][1]
                    except:
                        uid = 0
                    payment = {
                        'openid': data.get('openid')  # = fields.Char('openid')
                        , 'result_code': data['result_code']  # = fields.Char('业务结果')

                        , 'transaction_id': data['transaction_id']  # = fields.Char('微信订单号')
                        , 'bank_type': data['bank_type']  # = fields.Char('付款银行')
                        , 'fee_type': data['fee_type']  # = fields.Char('货币种类')
                        , 'total_fee': data['total_fee']  # = fields.Integer('订单金额(分)')
                        , 'cash_fee': data['cash_fee']  # = fields.Integer('现金支付金额')
                        , 'status': 1
                        , 'status_str': '成功'
                        , 'uid': uid
                        , 'utime': self.getToday(9)
                        , 'renoncestr': data['nonce_str']
                        , 'time_end': data['time_end']
                        #, 'sign': data['sign']

                    }

                    self.db.update("wechat_mall_payment", payment,
                              "payment_number='%s' and usr_id=%s" % (out_trade_no, self.subid))

                    sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                values(%s,%s,%s,%s,%s,now())
                            """
                    self.db.query(sql, [self.subid, 'wechat_mall_payment', 'payment_number:%s' % out_trade_no,
                                   '支付回调更新wechat_mall_payment表数据', self.subid])

                    sqlo = "update wechat_mall_order set status=2,status_str='待发货',pay_ctime=now(),uid=0,utime=now() where order_num=%s"
                    self.db.query(sqlo, order_num)
                    sqld = "update wechat_mall_order_detail set status=2,status_str='待发货',uid=0,utime=now() where order_num=%s"
                    self.db.query(sqld, order_num)
                    sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                        values(%s,%s,%s,%s,%s,now())
                                                    """
                    self.db.query(sql,
                             [self.subid, 'wechat_mall_order',
                              "order_num:%s,status=2,status_str='待发货'" % order_num,
                              '支付回调更新wechat_mall_order表数据', self.subid])
                    sqlt = """select id,wechat_user_id,ctype,kuaid,balance,ptkid,ptid,pt_type,phone 
                        from wechat_mall_order where order_num=%s and usr_id=%s """
                    ll, tt = self.db.select(sqlt, [order_num, self.subid])
                    if tt > 0:
                        order_id, wechat_user_id, ctype, kuaid, balance, ptkid, ptid, pt_type, phone = \
                        ll[0]
                        if float(balance) > 0:
                            pay_status = 3
                            pay_status_str = '组合支付'
                        else:
                            pay_status = 1
                            pay_status_str = '微信支付'
                        sqlo = """update wechat_mall_order set pay_status=%s,pay_status_str=%s,pay_ctime=now(),
                                uid=0,utime=now() where order_num=%s"""
                        self.db.query(sqlo, [pay_status, pay_status_str, order_num])
                        sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                                                    values(%s,%s,%s,%s,%s,now())
                                                                                """
                        self.db.query(sql, [self.subid, 'wechat_mall_order',
                                       "order_num:%s,pay_status=%s,pay_status_str=%s" % (
                                           order_num, pay_status, pay_status_str),
                                       '支付回调更新wechat_mall_order表数据', self.subid])

                        if str(kuaid) == '1' and str(ctype) != '1':  # 上门自提
                            sqlo = """update wechat_mall_order set status=4,status_str='待自提',
                                    uid=0,utime=now() where order_num=%s"""
                            self.db.query(sqlo, order_num)
                            sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                        values(%s,%s,%s,%s,%s,now())
                                    """
                            self.db.query(sql, [self.subid, 'wechat_mall_order',
                                           "order_num:%s,status=4,status_str='待自提'" % order_num,
                                           '支付回调更新wechat_mall_order表数据', self.subid])
                        elif str(kuaid) == '2' and str(ctype) != '1':  # 无需配送
                            sqlo = """update wechat_mall_order set status=6,status_str='待评价',
                                        uid=0,utime=now() where order_num=%s"""
                            self.db.query(sqlo, order_num)
                            sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                            values(%s,%s,%s,%s,%s,now())
                                        """
                            self.db.query(sql, [self.subid, 'wechat_mall_order',
                                           "order_num:%s,status=6,status_str='待评价'" % order_num,
                                           '支付回调更新wechat_mall_order表数据', self.subid])

                        sql = """select good_id,amount,inviter_user,good_name,cid from wechat_mall_order_detail 
                                where usr_id=%s and order_num=%s """
                        lll, t = self.db.select(sql, [self.subid, order_num])
                        for ii in lll:
                            good_id, amountm, user, good_name, cid = ii
                            self.oGOODS_D.updates(self.subid, good_id, amountm)
                            self.oGOODS_N.update(self.subid, good_id)
                            if str(user) != '0' and str(user) != str(cid):  # 下单返现
                                good_D = oGOODS_D.get(self.subid, int(good_id))
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
                                            self.db.query(sql, [float(share_number), self.subid, user])
                                            sqlg = """insert into user_log(usr_id,wechat_user_id,cname,memo,ctime)
                                                    values(%s,%s,'balance',%s,now())"""
                                            self.db.query(sqlg, [self.subid, user, '%s下单返现给%s' % (cid, user)])
                                            sql = """
                                            insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,
                                            typeid,typeid_str,remark,goods_id,goods_name,cid,ctime)
                                            values(%s,%s,2,'返现',%s,1,'分享返现','单次分享返现返',%s,%s,%s,now())
                                            """
                                            parm = [self.subid, user, float(share_number), good_id, gname,
                                                    cid]
                                            self.db.query(sql, parm)
                                            sql = """
                                                insert into profit_record(usr_id,wechat_user_id,ctype,ctype_str,
                                                share_type,
                                                share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                                values(%s,%s,0,'现金收益',3,'好友下单返现',%s,%s,%s,%s,now())
                                                """
                                            parm = [self.subid, user, float(share_number), good_id, gname,
                                                    cid]
                                            self.db.query(sql, parm)

                                        elif str(share_type) == '2' and share_number != '':  # 返积分
                                            sql = """
                                            update wechat_mall_user set score=coalesce(score,0)+%s 
                                            where usr_id=%s and id=%s 
                                                    """
                                            self.db.query(sql, [float(share_number), self.subid, user])
                                            sqlg = """insert into user_log(usr_id,wechat_user_id,cname,memo,ctime)
                                                    values(%s,%s,'score',%s,now())"""
                                            self.db.query(sqlg, [self.subid, user, '%s下单返积分给%s' % (cid, user)])
                                            sql = """
                                                insert into integral_log(usr_id,wechat_user_id,type,typestr,in_out,
                                                inoutstr,amount,cid,ctime)values(%s,%s,7,'分享返',0,'收入',%s,%s,now())
                                                    """
                                            parm = [self.subid, good_id, float(share_number), cid]
                                            self.db.query(sql, parm)
                                            sql = """insert into profit_record(usr_id,wechat_user_id,ctype,
                                            ctype_str,share_type,
                                                share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                                values(%s,%s,1,'积分收益',4,'好友下单返积分',%s,%s,%s,%s,now())
                                                            """
                                            parm = [self.subid, user, float(share_number), good_id, gname,
                                                    cid]
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
                                            parm = [self.subid, ticket_id]
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
                                                        'usr_id': self.subid,
                                                        'wechat_user_id': user,
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
                                                        'cid': self.subid,
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
                                                    parm = [self.subid, user, change_money, good_id, gname,
                                                            cid,
                                                            ticket_id]
                                                    self.db.query(sql, parm)
                                        self.oUSER.update(self.subid, user)
                        if str(ctype) == '2':  # 支付更新团的状态gid
                            if str(pt_type) == '0':  # 开团
                                self.Pingtuan_add(wechat_user_id, ptid, order_id,phone)
                            if str(pt_type) == '1':  # 参团
                                self.Pingtuan_join(wechat_user_id, ptkid, order_id,phone)
                    self.oUSER.update(self.subid, uid)

            else:
                datas = {
                    'status_str': '失败',
                    'result_code': data['result_code'],
                    'err_code': data['err_code'],
                    'err_code_des': data['err_code_des'],
                    'uid': 0,
                    'utime': self.getToday(9)
                }
                self.db.update("wechat_mall_payment", datas, "payment_number='%s'" % data['out_trade_no'])
            return self.reply("OK", True)
        except Exception as e:
            self.print_log('平台vip支付回调错误','%s'%e)


    def to_dict(self, content):
        raw = {}
        root = etree.fromstring(content,parser=etree.XMLParser(resolve_entities=False))
        for child in root:
            raw[child.tag] = child.text
        return raw

    def to_xml(self, raw):
        s = ""
        for k, v in raw.items():
            s += "<{0}>{1}</{0}>".format(k, v)
        s = "<xml>{0}</xml>".format(s)
        return s.encode("utf-8")

    def sign(self, raw):
        mall=self.oMALL.get(self.subid)
        wechat_pay_secret = mall.get('mchkey')
        raw = [(k, str(raw[k]) if isinstance(raw[k], int) else raw[k])
               for k in sorted(raw.keys())]
        s = "&".join("=".join(kv) for kv in raw if kv[1])
        s += "&key={0}".format(wechat_pay_secret)
        return hashlib.md5(s.encode("utf-8")).hexdigest().upper()

    def check(self, data):
        sign = data.pop("sign")
        return sign == self.sign(data)

    def reply(self, msg, ok=True):
        code = "SUCCESS" if ok else "FAIL"
        return self.to_xml(dict(return_code=code, return_msg=msg))

    def print_log(self,cname, errors):
        sql = "insert into print_log(cname,errors,ctime)values(%s,%s,now())"
        self.db.query(sql, [cname, errors])
        return

    def getToday(self,format=3):
        """返回今天的日期字串"""
        # format=1	yyyymmdd
        # format=2	hh:mm
        # format=3	yyyy/mm/dd
        # format=4	yyyy/mm/dd  hh:mm
        # format=5	yymmdd
        t = time.time()
        date_ary = time.localtime(t)
        if format == 1:
            x = time.strftime("%Y%m%d", date_ary)
        elif format == 2:
            x = time.strftime("%H:%M", date_ary)
        elif format == 3:
            x = time.strftime("%Y/%m/%d", date_ary)
        elif format == 4:
            x = time.strftime("%Y/%m/%d %H:%M", date_ary)
        elif format == 5:
            x = time.strftime("%y%m%d", date_ary)
        elif format == 6:
            x = time.strftime("%Y-%m-%d", date_ary)
        elif format == 7:
            x = time.strftime("%Y/%m/%d %H:%M:%S", date_ary)
        elif format == 8:
            x = time.strftime("%Y-%m-%d %H:%M", date_ary)
        elif format == 9:
            x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
        elif format == 10:
            x = time.strftime("%Y年%m月%d日 %H:%M", date_ary)
        else:
            x = time.strftime("%Y-%m-%d", date_ary)
        return x


    def Pingtuan_add_close(self,order_id):  # 开团数据处理失败进行拼团失败处理

        lT, iN = self.db.select("select id from open_pt where usr_id=%s and  order_id=%s", [self.subid, order_id])
        if iN > 0:
            return

        sqlw = """select id from wechat_mall_order 
                            where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                            """
        lT, iN = self.db.select(sqlw, [self.subid, order_id])
        if iN == 0:
            return

        sqld = """
                update wechat_mall_order set 
                status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                 update wechat_mall_order_detail set 
                status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                """
        self.db.query(sqld, [self.subid, order_id, self.subid, order_id])
        sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                values(%s,%s,%s,%s,%s,now())
                                            """
        self.db.query(sql, [self.subid, 'wechat_mall_order_detail,wechat_mall_order', '开团失败,订单id:%s' % order_id,
                       '更新订单状态为开团失败', self.subid])

        return

    def Pingtuan_add(self, wechat_user_id, ptid, order_id,phone):
        sqlw = """select id from wechat_mall_order 
                    where ctype=2  and usr_id=%s and wechat_user_id=%s and id=%s and coalesce(pay_status,0)!=0
                    """
        lT, iN = self.db.select(sqlw, [self.subid, wechat_user_id, order_id])
        if iN == 0:
            return

        try:
            cur_random_no = "%s%s" % (time.time(), random.random())
            oUSER = self.oUSER.get(self.subid, wechat_user_id)
            name = oUSER['name']
            avatar = oUSER['avatar']
            # self.print_log('subusr_id:%s,ptid:%s'%(self.subusr_id, ptid),'%s'%self.oPT_GOODS.get(self.subusr_id))
            oPT_GOODS = self.oPT_GOODS.get(self.subid, ptid)
            number = oPT_GOODS['cnumber']
            gid = oPT_GOODS['gid']
            gname = oPT_GOODS['gname']
            gintr = oPT_GOODS['gintr']
            gpic = oPT_GOODS['gpic']
            gcontent = oPT_GOODS['gcontent']
            ptprice = oPT_GOODS['pt_price']
            mnprice = oPT_GOODS['mini_price']
            stores = oPT_GOODS['stores']
            ok_type = oPT_GOODS['ok_type']
            add_type = oPT_GOODS['add_type']
            tk_type = oPT_GOODS['tk_type']
            kt_type = oPT_GOODS['kt_type']
            timeout_h = oPT_GOODS['timeout_h']

            cnow = datetime.datetime.now()
            # ctime = now.strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(hours=int(timeout_h))
            n_days = cnow + delta
            date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

            data = {
                'usr_id': self.subid,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'order_id': order_id,
                'name': name,
                'avatar': avatar,
                'number': number,
                'short': number - 1,
                'phone': phone,
                'status': 1,
                'ok_type': ok_type,
                'add_type': add_type,
                'tk_type': tk_type,
                'kt_type': kt_type,
                'date_end': date_end,
                'gid': gid,
                'gname': gname,
                'gintr': gintr,
                'gpic': gpic,
                'gcontent': gcontent,
                'ptprice': ptprice,
                'mnprice': mnprice,
                'stores': stores,
                'random_no': cur_random_no,
                'cid': wechat_user_id,
                'ctime': self.getToday(9)

            }
            self.db.insert('open_pt', data)
            opid = self.db.fetchcolumn("select id from open_pt where random_no=%s", cur_random_no)
            sqlo = """
                    update wechat_mall_order set ptkid=%s,status=10,status_str='拼团中' where usr_id=%s and id=%s 
                            """
            self.db.query(sqlo, [opid, self.subid, order_id])
            sqld = """
                    update wechat_mall_order_detail set 
                    status=10,status_str='拼团中' where usr_id=%s and order_id=%s; 
                    """
            self.db.query(sqld, [self.subid, order_id])
            datad = {
                'usr_id': self.subid,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'opid': opid,
                'order_id': order_id,
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
            sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                values(%s,%s,%s,%s,%s,now())
                                            """
            self.db.query(sql, [self.subid, 'wechat_mall_order_detail,wechat_mall_order', '开团成功,订单id:%s' % order_id,
                           '更新订单状态为开团成功', self.subid])
            return
        except:
            self.print_log( 'subusr_id:%s,ptid:%s' % (self.subid, ptid), '%s' % self.oPT_GOODS.get(self.subid))
            self.print_log( '拼团失败', '%s' % str(traceback.format_exc()))
            self.Pingtuan_add_close(order_id)
            return

    def Pingtuan_join_close(self, order_id):  # 参团数据处理失败进行拼团失败处理
        sql="select id from open_pt_detail where usr_id=%s and  order_id=%s"
        lT, iN = self.db.select(sql, [self.subid, order_id])
        if iN > 0:
            return

        sqlw = """select id from wechat_mall_order 
                    where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                    """
        lT, iN = self.db.select(sqlw, [self.subid, order_id])
        if iN == 0:
            return

        sqld = """
                update wechat_mall_order set 
                status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                 update wechat_mall_order_detail set 
                status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                """
        self.db.query(sqld, [self.subid, order_id, self.subid, order_id])
        sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                values(%s,%s,%s,%s,%s,now())
                                            """
        self.db.query(sql, [self.subid, 'wechat_mall_order_detail,wechat_mall_order', '拼团失败,订单id:%s' % order_id,
                       '更新订单状态为参团失败', self.subid])
        return

    def Pingtuan_join(self, wechat_user_id, ptkid, order_id, phone):
        sqlw = """select id from wechat_mall_order 
                                    where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                                    """
        lT, iN = self.db.select(sqlw, [self.subid, order_id])
        if iN == 0:
            return
        try:
            sql = "select ptid,number,short from open_pt where usr_id=%s and id=%s and coalesce(status,0)=1"
            l, t = self.db.select(sql, [self.subid, ptkid])
            if t == 0:
                sqld = """
                    update wechat_mall_order set 
                    status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                     update wechat_mall_order_detail set 
                    status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                        """
                self.db.query(sqld, [self.subid, order_id, self.subid, order_id])
                sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                values(%s,%s,%s,%s,%s,now())
                                            """
                self.db.query(sql, [self.subid, 'wechat_mall_order_detail,wechat_mall_order', '拼团失败,订单id:%s'% order_id,
                               '更新订单状态为拼团失败', self.subid])
                return
            ptid, number, short = l[0]

            oUSER = self.oUSER.get(self.subid, wechat_user_id)
            name = oUSER['name']
            avatar = oUSER['avatar']

            # self.print_log('number:%s'%number,'short:%s'%short)
            oPT_GOODS = self.oPT_GOODS.get(self.subid, ptid)
            timeout_h = oPT_GOODS['timeout_h']
            cnow = datetime.datetime.now()
            # ctime = now.strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(hours=int(timeout_h))
            n_days = cnow + delta
            date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

            datad = {
                'usr_id': self.subid,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'opid': ptkid,
                'order_id': order_id,
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
            self.db.query("update open_pt set short=short-1 where id=%s and usr_id=%s", [ptkid, self.subid])

            sqlo = """
                update wechat_mall_order set ptid=%s,status=10,status_str='拼团中' where usr_id=%s and id=%s 
                    """
            self.db.query(sqlo, [ptid, self.subid, order_id])

            sqld = """
                    update wechat_mall_order_detail set 
                    status=10,status_str='拼团中' where usr_id=%s and order_id=%s; 
                    """
            self.db.query(sqld, [self.subid, order_id])

            if int(short) == 1:
                self.db.query("update open_pt set status=2 where id=%s and usr_id=%s", [ptkid, self.subid])
                self.db.query("update open_pt_detail set status=2 where opid=%s and usr_id=%s", [ptkid, self.subid])
                ############处理订单状态
                sqlp = """select id,kuaid from wechat_mall_order 
                        where usr_id=%s and ptkid=%s and ctype=2 and status=10"""
                l, t = self.db.select(sqlp, [self.subid, ptkid])
                if t > 0:
                    for i in l:
                        orderdid, kuaid = i
                        if str(kuaid) == '0':  # 快递单
                            sqld = """
                                update wechat_mall_order set 
                                status=2,status_str='待发货' where usr_id=%s and id=%s;
                                 update wechat_mall_order_detail set 
                                status=2,status_str='待发货' where usr_id=%s and order_id=%s; 
                                """
                            self.db.query(sqld, [self.subid, orderdid, self.subid, orderdid])

                            sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                        values(%s,%s,%s,%s,%s,now())
                                            """
                            self.db.query(sql, [self.subid, 'wechat_mall_order_detail,wechat_mall_order',
                                           '拼团成功,订单id:%s' % order_id,
                                           '更新订单状态为待发货', self.subid])


                        elif str(kuaid) == '1':  # 自提单
                            sqld = """
                                update wechat_mall_order set 
                                    status=4,status_str='待自提' where usr_id=%s and id=%s; 
                                update wechat_mall_order_detail set 
                                    status=4,status_str='待自提' where usr_id=%s and order_id=%s; 
                                        """
                            self.db.query(sqld, [self.subid, orderdid, self.subid, orderdid])

                            sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                values(%s,%s,%s,%s,%s,now())
                                            """
                            self.db.query(sql, [self.subid, 'wechat_mall_order_detail,wechat_mall_order',
                                           '拼团成功,订单id:%s' % order_id,
                                           '更新订单状态为待自提', self.subid])


                        elif str(kuaid) == '2':  # 无须配送
                            sqld = """
                            update wechat_mall_order set 
                                status=6,status_str='待评价' where usr_id=%s and id=%s;
                            update wechat_mall_order_detail set 
                                status=6,status_str='待评价' where usr_id=%s and order_id=%s; 
                                        """
                            self.db.query(sqld, [self.subid, orderdid, self.subid, orderdid])
                            sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                                values(%s,%s,%s,%s,%s,now())
                                            """
                            self.db.query(sql, [self.subid, 'wechat_mall_order_detail,wechat_mall_order',
                                           '拼团成功,订单id:%s' % order_id,
                                           '更新订单状态为待评价', self.subid])

            return
        except:
            self.print_log('参团失败', '%s' % str(traceback.format_exc()))
            self.Pingtuan_join_close(order_id)
            return

    def user_log(self, uid, cname, memo):
        sql = "insert into user_log(usr_id,wechat_user_id,cname,memo,ctime)values(%s,%s,%s,%s,now())"
        self.db.query(sql, [self.subid, uid, cname, memo])
        return






















