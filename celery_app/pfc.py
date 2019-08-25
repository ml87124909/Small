# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""celery_app/pfc.py"""

from flask import Flask,json
#from flask_mail import Mail,Message
from celery import Celery
from celery_app import c
import time

app=Flask(__name__)


import requests,json,os,random,traceback,oss2
from imp import reload
import datetime
from basic  import publicw as public

db,ATTACH_ROOT,getToday=public.db,public.ATTACH_ROOT,public.getToday
oUSER,oPT_GOODS,oMALL=public.oUSER,public.oPT_GOODS,public.oMALL
from qiniu import Auth, put_stream, put_data,put_file,BucketManager
from basic.wxbase import wx_minapp_login,WXBizDataCrypt,WxPay
# app.config['MAIL_SERVER'] = ''
# app.config['MAIL_PORT'] = 994
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_DEBUG'] = True
# app.config['MAIL_DEFAULT_SENDER'] = ''
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ""

#mails=Mail(app)

@c.task
def money_pay():
    try:
        sql = """
        select id,coalesce(couponid,0) from offline_pay 
        where coalesce(status,0)=0 
        and to_char(data_close,'YYYY-MM-DD HH24:MI')<to_char(now(),'YYYY-MM-DD HH24:MI')
        """
        lT, iN = db.select(sql)
        if iN == 0:
            return
        for i in lT:
            id,couponid=i
            db.query("update offline_pay set status=3 where id=%s",[id])
            sql = """
            update  my_coupons set state=0,state_str='未使用',utime=now() where id=%s
            """
            db.query(sql, [couponid])
    except Exception as e:
        print_log('处理超时未买单故障', '%s' % e)
        return

@c.task
def Did_not_pay():#####处理超时未交费

    try:
        sql = """
        select usr_id,to_char(expire_time,'YYYY-MM-DD') from users 
                where coalesce(expire_flag,0)=0 and to_char(expire_time,'YYYY-MM-DD')<to_char(now(),'YYYY-MM-DD') 
                and coalesce(vip_flag,0)!=7"""
        lT, iN = db.select(sql)
        if iN == 0:
            return
        for i in lT:
            usr_id,expire_time=i
            db.query("update users set expire_flag=1 where usr_id=%s",[usr_id])
            sql="insert into users_expire_log(usr_id,expire_time,ctime)values(%s,%s,now())"
            db.query(sql,[usr_id,expire_time])
    except Exception as e:
        print_log('处理超时未交费故障', '%s' % e)
        return


@c.task
def Did_not_oss():  #####处理存储包过期

    try:
        sql = """select a.id,a.usr_id,a.cname from alipay_log a
		left join users u on u .usr_id=a.usr_id
        where to_char(a.etime,'YYYY-MM-DD')<to_char(now(),'YYYY-MM-DD') 
        and a.ctype in (4,5,6) and coalesce(a.oss_flag,0)=0 and coalesce(u.oss_flag,0)!=7
        """
        lT, iN = db.select(sql)
        if iN == 0:
            return
        for i in lT:
            id, usr_id, cname = i
            db.query("update users set oss_all=oss_all-%s where usr_id=%s", [int(cname), usr_id])
            db.query("update alipay_log set oss_flag=1 where id=%s", [id])
            sql = "insert into users_oss_log(usr_id,size,ctime)values(%s,%s,now())"
            db.query(sql, [usr_id, int(cname)])
    except Exception as e:
        print_log('处理存储包过期', '%s' % e)
        return



def write_order_log(subusr_id,order_id,edit_name='',edit_memo='',edit_remark=''):
    sql="""insert into wechat_mall_order_log(usr_id,order_id,edit_name,edit_memo,edit_remark,cid,ctime)
        values(%s,%s,%s,%s,%s,0,now())
    """
    db.query(sql,[subusr_id,order_id,edit_name,edit_memo,edit_remark])
    return

@c.task
def update_order():#关闭订单
    sql = """select id,usr_id  from wechat_mall_order 
            where coalesce(status,0)=1 
            and to_char(data_close,'YYYY-MM-DD HH24:MI')<to_char(now(),'YYYY-MM-DD HH24:MI')
                   """
    k, r = db.select(sql)

    if r >0:
        for i in k:
            gid=i[0]
            usr_id = i[1]
            db.query("update wechat_mall_order set status=-1,status_str='已取消' where id=%s", gid)
            write_order_log(usr_id,gid,"status=-1,status_str=已取消",'取消订单','系统定时检测超时未支付')
        sqlu = "insert into update_order(remark,ctime)values('定时处理关闭订单完成',now())"
        db.query(sqlu)
        return
    sqlu = "insert into update_order(remark,ctime)values('定时处理关闭订单没有订单要关闭',now())"
    db.query(sqlu)
    return



def user_log(subusr_id,uid,cname,memo):
    sql="insert into user_log(usr_id,wechat_user_id,cname,memo,ctime)values(%s,%s,%s,%s,now())"
    db.query(sql,[subusr_id,uid,cname,memo])
    return

def print_log(cname,errors):
    sql = "insert into celery_log(cname,errors,ctime)values(%s,%s,now())"
    db.query(sql,[cname,errors])
    return


def Pingtuan_close(ptkid,subusr_id):  # 超时关团 11 拼团失败
    print_log('超时关团退款', 'ptkid:%s' % ptkid)
    try:
        sql = "select order_id,ptid,wechat_user_id from open_pt_detail where usr_id=%s and status=1 and opid=%s"
        l, t = db.select(sql, [subusr_id, ptkid])
        if t == 0:
            return
        for i in l:
            orderid, ptid, wechat_user_id = i
            db.query("update open_pt set status=3 where id=%s and usr_id=%s", [ptkid, subusr_id])
            db.query("update open_pt_detail set status=3 where opid=%s and usr_id=%s", [ptkid, subusr_id])

            sqld = """
                                   update wechat_mall_order set 
                                   status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                                    update wechat_mall_order_detail set 
                                   status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                                   """
            db.query(sqld, [subusr_id, orderid, subusr_id, orderid])
            write_order_log(subusr_id, orderid, '拼团失败', '更新订单状态为拼团失败', '订单id:%s' % orderid)



    except:
        print_log('超时关团退款失败ptkid:%s'% ptkid, '%s' % str(traceback.format_exc()))

    return


def Pingtuan_ok_join(ptkid,subusr_id):  # 促团
    print_log('促团','ptkid:%s'%ptkid)
    try:
        sql = "select wechat_user_id,cname,avatar from virtual_conf where usr_id=%s order by id desc"
        lT, iN = db.select(sql, [subusr_id])
        if iN == 0:
            Pingtuan_close(ptkid, subusr_id)
            return

        sql = "select ptid,order_id,number,short from open_pt where usr_id=%s and id=%s and status=1"
        l, t = db.select(sql, [subusr_id, ptkid])
        if t == 0:
            Pingtuan_close(ptkid, subusr_id)
            return
        ptid, orderid, number, short = l[0]
        print_log('促团11111:short:%s' % short, 'ptkid:%s' % ptkid)
        while short > 0:
            print_log('促团222222222:short', 'ptkid:%s' % ptkid)
            ws = random.randint(0, iN - 1)
            wechat_user_id, cname, avatar = lT[ws]
            # self.print_log('number:%s'%number,'short:%s'%short)
            PT_GOODS = oPT_GOODS.get(subusr_id, ptid)
            timeout_h = PT_GOODS['timeout_h']
            cnow = datetime.datetime.now()
            # ctime = now.strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(hours=int(timeout_h))
            n_days = cnow + delta
            date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

            datad = {
                'usr_id': subusr_id,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'opid': ptkid,
                'name': cname,
                'avatar': avatar,
                'title': 2,
                'status': 1,
                'date_end': date_end,
                'cid': wechat_user_id,
                'ctime': getToday(9)
            }
            db.insert('open_pt_detail', datad)
            db.query("update open_pt set short=short-1 where id=%s and usr_id=%s", [ptkid, subusr_id])
            if int(short) == 1:
                db.query("update open_pt set status=2 where id=%s and usr_id=%s", [ptkid, subusr_id])
                db.query("update open_pt_detail set status=2 where opid=%s and usr_id=%s", [ptkid, subusr_id])
                ############处理订单状态
                sqlp = "select id,kuaid from wechat_mall_order where usr_id=%s and ptkid=%s and ctype=2"
                l, t = db.select(sqlp, [subusr_id, ptkid])
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
                            db.query(sqld, [subusr_id, orderdid, subusr_id, orderdid])
                            write_order_log(subusr_id,orderdid, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)


                        elif str(kuaid) == '1':  # 自提单
                            sqld = """
                                update wechat_mall_order set 
                                    status=4,status_str='待自提' where usr_id=%s and id=%s; 
                                update wechat_mall_order_detail set 
                                    status=4,status_str='待自提' where usr_id=%s and order_id=%s; 
                                """
                            db.query(sqld, [subusr_id, orderdid, subusr_id, orderdid])
                            write_order_log(subusr_id,orderdid, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)

                        elif str(kuaid) == '2':  # 无须配送
                            sqld = """
                                    update wechat_mall_order set 
                                        status=6,status_str='待评价' where usr_id=%s and id=%s;
                                    update wechat_mall_order_detail set 
                                        status=6,status_str='待评价' where usr_id=%s and order_id=%s; 
                                    """
                            db.query(sqld, [subusr_id, orderdid, subusr_id, orderdid])
                            write_order_log(subusr_id,orderdid, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)

            short = short - 1
    except:
        print_log('促团失败ptkid:%s'% ptkid, '%s' % str(traceback.format_exc()))

    return


@c.task
def update_pt():

    sqlk = """
            select id,coalesce(ok_type,0)ok_type,usr_id from open_pt 
                        where coalesce(del_flag,0)=0 and coalesce(status,0)=1
                    and to_char(date_end,'YYYY-MM-DD HH24:MI')<to_char(now(),'YYYY-MM-DD HH24:MI')
            """
    lT, iN = db.select(sqlk)
    if iN > 0:
        for i in lT:
            kid, ok_type, subusr_id = i
            try:
                if str(ok_type) == '1':  # 促团
                    Pingtuan_ok_join(kid,subusr_id)
                else:  # 关闭
                    Pingtuan_close(kid,subusr_id)
            except:
                sqlu = "insert into update_pt(remark,ctime)values('出错了%s',now())" % kid
                db.query(sqlu)

    sqlu = "insert into update_pt(remark,ctime)values('定时处理关闭超时未成团的订单',now())"
    db.query(sqlu)


@c.task
def update_refund():  # 拼团退款
    sqlu = "insert into update_refund(remark,ctime)values('start',now())"
    db.query(sqlu)
    sql = """select w.id,w.wechat_user_id,w.usr_id,coalesce(w.pay_status,0),w.new_total,w.order_num,w.balance,
                coalesce(w.ptkid,0),coalesce(w.ptid,0),coalesce(w.pt_type,0)  
                from wechat_mall_order w
                where coalesce(w.status,0)=11 and coalesce(w.pt_kt,0)=0
                """

    lT, iN = db.select(sql)

    if iN > 0:

        for i in lT:
            try:
                orderid,wechat_user_id,subusr_id,pay_status,new_total,order_num,balance,ptkid,ptid,pt_type = i

                if str(pt_type) == '0':
                    sqlo = "select tk_type from open_pt where ptid=%s"
                    l, t = db.select(sqlo, ptid)
                    if t == 0:
                        sqlp = "select tk_type from pt_conf where id=%s"
                        l, t = db.select(sqlp, ptid)
                else:
                    sqlo = "select tk_type from open_pt where id=%s"
                    l, t = db.select(sqlo, ptkid)

                tk_type=l[0][0]

                if str(tk_type) == '2':  # 退回余额
                    sqlc = "select id from cash_log where typeid=4 and cnumber=%s"
                    l,t=db.select(sqlc,order_num)
                    if t==0:
                        sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                        db.query(sql, [new_total, subusr_id, wechat_user_id])
                        user_log(subusr_id, wechat_user_id, 'balance:%s' % new_total, '拼团失败订单余额变化')
                        sql = """
                           insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                           values(%s,%s,3,'消费',%s,4,'退回',%s,'拼团失败订单退款',%s,now())
                                               """
                        db.query(sql, [subusr_id, wechat_user_id, -new_total, order_num, subusr_id])
                        print_log('orderid:%s'%orderid,'退款1')

                elif str(tk_type) == '1':  # 原路退回
                    sqlu = "insert into update_refund(remark,ctime)values('start55555555',now())"
                    db.query(sqlu)
                    if str(pay_status) == '1':  # 微信
                        order_refund(subusr_id, orderid, order_num, wechat_user_id)
                        print_log('orderid:%s' % orderid, '退款2')
                    elif str(pay_status) in ('2', '4', '5'):  # 余额
                        sqlc = "select id from cash_log where typeid=4 and cnumber=%s"
                        l, t = db.select(sqlc, order_num)
                        if t == 0:
                            sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                            db.query(sql, [new_total, subusr_id, wechat_user_id])
                            user_log(subusr_id, wechat_user_id, 'balance:%s' % new_total, '拼团失败订单余额变化')
                            sql = """
                               insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                               values(%s,%s,3,'消费',%s,4,'退回',%s,'拼团失败订单退款',%s,now())
                                                   """
                            db.query(sql, [subusr_id, wechat_user_id, -new_total, order_num, subusr_id])
                            print_log('orderid:%s' % orderid, '退款3')
                    elif str(pay_status) == '3':  # 微信+余额
                        order_refund(subusr_id, orderid, order_num, wechat_user_id)
                        sqlc = "select id from cash_log where typeid=4 and cnumber=%s"
                        l, t = db.select(sqlc, order_num)
                        if t == 0:
                            sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                            db.query(sql, [balance, subusr_id, wechat_user_id])
                            user_log(subusr_id, wechat_user_id, 'balance:%s' % new_total, '拼团失败订单余额变化')
                            sql = """
                                   insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                                   values(%s,%s,3,'消费',%s,4,'退回',%s,'拼团失败订单退款',%s,now())
                                                                       """
                            db.query(sql, [subusr_id, wechat_user_id, -balance, order_num, subusr_id])

                        print_log('orderid:%s' % orderid, '退款4')
                    sqlu = "insert into update_refund(remark,ctime)values('start666666',now())"
                    db.query(sqlu)
                db.query("update wechat_mall_order set pt_kt=1 where id=%s;", orderid)
                oUSER.update(subusr_id, wechat_user_id)

            except:
                sqlu = """insert into update_refund(remark,ctime)values('定时处理拼团失败订单退款:%s',now())
                        """%str(traceback.format_exc())
                db.query(sqlu)
                pass
        sqlu = "insert into update_refund(remark,ctime)values('定时处理关闭订单完成',now())"
        db.query(sqlu)
        return
    sqlu = "insert into update_refund(remark,ctime)values('定时处理关闭没有数据要处理',now())"
    db.query(sqlu)

    return


def order_refund(subusr_id,order_id,order_num,wechat_user_id):

    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
    romcode = str(time.time()).split('.')[-1]  # [3:]
    re_num = 'R' + danhao[2:] + romcode
    mall = oMALL.get(subusr_id)

    app_id = mall.get('appid','')
    secret = mall.get('secret','')
    wx_mch_id = mall.get('mchid','')
    wx_mch_key = mall.get('mchkey','')
    base_url = mall.get('base_url','')#'https://malishop.janedao.cn'
    api_cert_path = mall.get('cert','')
    api_key_path =mall.get('key','')

    notify_url = base_url + '/refund/%s/notify' % subusr_id
    wxpay = WxPay(app_id, wx_mch_id, wx_mch_key, notify_url)


    sql="select total_fee from wechat_mall_payment where order_id=%s and payment_number=%s and usr_id=%s "
    l,t=db.select(sql,[order_id,order_num,subusr_id])
    if t==0:
        return 1
    total_fee=l[0][0]
    data = {  # 退款信息
        'out_trade_no': order_num,  # 商户订单号
        'total_fee': total_fee,  # 订单金额
        'refund_fee': total_fee  # 退款金额
    }
    sql = "select out_refund_no from wechat_mall_refund where out_trade_no=%s and usr_id=%s"
    lT, iN = db.select(sql, [order_num, subusr_id])
    if iN==0:
        data['out_refund_no']=re_num  # 商户退款单号
        refund = {  # 退款信息
            'out_trade_no': order_num,  # 商户订单号
            'total_fee': total_fee,  # 订单金额
            'refund_fee': total_fee,  # 退款金额
            'out_refund_no':re_num,
            'usr_id':subusr_id,
            'wechat_user_id':wechat_user_id
        }

        db.insert('wechat_mall_refund',refund)
        data['notify_url'] = notify_url  # 商户退款回调
        raw=wxpay.refund(api_cert_path,api_key_path,**data)

        if raw['return_code'] == 'SUCCESS' and raw['result_code']  == 'SUCCESS':

            try:
                sql="""select id from wechat_mall_refund 
                    where out_trade_no=%s and out_refund_no=%s and total_fee=%s and usr_id=%s"""
                l,i=db.select(sql,[raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],subusr_id])
                if i == 0:
                    return 1

                refund = {
                    'refund_id': raw['refund_id']
                    , 'result_code': raw['result_code']
                    , 'return_msg': raw['return_msg']
                    ,'status':1
                    ,'status_str': '成功'
                    ,'utime': getToday(9)
                }

                db.update("wechat_mall_refund", refund, "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" %(raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],subusr_id))

                sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                            values(%s,%s,%s,%s,%s,now())
                        """
                db.query(sql, [subusr_id,'wechat_mall_refund',"out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" %(raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],subusr_id),
                                    '退款回调更新wechat_mall_refund表数据',subusr_id])
                return 0
            except:
                return 1

        else:
            try:
                datas = {
                    'status_str': '失败',
                    'result_code': raw['result_code'],
                    'utime':getToday(9)
                }
                db.update("wechat_mall_refund", datas, "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" %(raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],subusr_id))
                return 1
            except:
                return 1
    out_refund_no=lT[0][0]
    data['out_refund_no'] = out_refund_no  # 商户退款单号
    raw = wxpay.refund(api_cert_path, api_key_path, **data)
    if raw['return_code'] == 'SUCCESS' and raw['result_code'] == 'SUCCESS':
        try:
            sql = "select id from wechat_mall_refund where out_trade_no=%s and out_refund_no=%s and total_fee=%s and usr_id=%s"
            l, i = db.select(sql,
                                  [raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id])
            if i == 0:
                return 1

            refund = {
                'refund_id': raw['refund_id']
                , 'result_code': raw['result_code']
                , 'return_msg': raw['return_msg']
                , 'status': 1
                , 'status_str': '成功'
                , 'utime': getToday(9)
            }

            db.update("wechat_mall_refund", refund,
                           "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                               raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id))

            sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                        values(%s,%s,%s,%s,%s,now())
                    """
            db.query(sql, [subusr_id, 'wechat_mall_refund',
                                "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                                    raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id),
                                '退款回调更新wechat_mall_refund表数据', subusr_id])
            return 0
        except:
            return 1

    else:
        try:
            datas = {
                'status_str': '失败',
                'result_code': raw['result_code'],
                'utime': getToday(9)
            }
            db.update("wechat_mall_refund", datas,
                           "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                               raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id))
            return 1
        except:
            return 1






#
# @c.task
# def send_mail():
#
#     sql="""select p.id,p.email,to_char(p.ctime,'YYYY-MM-DD HH:MM')ctime,p.content,p.mp3,COALESCE(p.tomp3,0)
#             from post_future p
#             where COALESCE(p.del_flag,0)=0 and COALESCE(p.status,0)!=1 and to_time<now() """
#     l,t=db.select(sql)
#     if t>0:
#         with app.app_context():
#             with mails.connect() as conn:
#                 for i in l:
#                     id,email,ctime,content,audio,flag=i[0],i[1],i[2],i[3],i[4],i[5]
#                     path = os.path.join(ATTACH_ROOT, audio)
#
#                     html = u'''
#                         <style type="text/css">
#                         /*** BMEMBF Start ***/
#                         @media only screen and (max-width: 480px){table.blk, table.tblText, .bmeHolder, .bmeHolder1, table.bmeMainColumn{width:100% !important;} }
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable td.tblCell{padding:0px 20px 20px 20px !important;} }
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable.bmeCaptionTableMobileTop td.tblCell{padding:20px 20px 0 20px !important;} }
#                         @media only screen and (max-width: 480px){table.bmeCaptionTable td.tblCell{padding:10px !important;} }
#                         @media only screen and (max-width: 480px){table.tblGtr{ padding-bottom:20px !important;} }
#                         @media only screen and (max-width: 480px){td.blk_container, .blk_parent, .bmeLeftColumn, .bmeRightColumn, .bmeColumn1, .bmeColumn2, .bmeColumn3, .bmeBody{display:table !important;max-width:600px !important;width:100% !important;} }
#                         @media only screen and (max-width: 480px){table.container-table, .bmeheadertext, .container-table { width: 95% !important; } }
#                         @media only screen and (max-width: 480px){.mobile-footer, .mobile-footer a{ font-size: 13px !important; line-height: 18px !important; } .mobile-footer{ text-align: center !important; } table.share-tbl { padding-bottom: 15px; width: 100% !important; } table.share-tbl td { display: block !important; text-align: center !important; width: 100% !important; } }
#                         @media only screen and (max-width: 480px){td.bmeShareTD, td.bmeSocialTD{width: 100% !important; } }
#                         @media only screen and (max-width: 480px){td.tdBoxedTextBorder{width: auto !important;}}
#                         @media only screen and (max-width: 480px){table.blk, table[name=tblText], .bmeHolder, .bmeHolder1, table[name=bmeMainColumn]{width:100% !important;} }
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable td[name=tblCell]{padding:0px 20px 20px 20px !important;} }
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable.bmeCaptionTableMobileTop td[name=tblCell]{padding:20px 20px 0 20px !important;} }
#                         @media only screen and (max-width: 480px){table.bmeCaptionTable td[name=tblCell]{padding:10px !important;} }
#                         @media only screen and (max-width: 480px){table[name=tblGtr]{ padding-bottom:20px !important;} }
#                         @media only screen and (max-width: 480px){td.blk_container, .blk_parent, [name=bmeLeftColumn], [name=bmeRightColumn], [name=bmeColumn1], [name=bmeColumn2], [name=bmeColumn3], [name=bmeBody]{display:table !important;max-width:600px !important;width:100% !important;} }
#                         @media only screen and (max-width: 480px){table[class=container-table], .bmeheadertext, .container-table { width: 95% !important; } }
#                         @media only screen and (max-width: 480px){.mobile-footer, .mobile-footer a{ font-size: 13px !important; line-height: 18px !important; } .mobile-footer{ text-align: center !important; } table[class="share-tbl"] { padding-bottom: 15px; width: 100% !important; } table[class="share-tbl"] td { display: block !important; text-align: center !important; width: 100% !important; } }
#                         @media only screen and (max-width: 480px){td[name=bmeShareTD], td[name=bmeSocialTD]{width: 100% !important; } }
#                         @media only screen and (max-width: 480px){td[name=tdBoxedTextBorder]{width: auto !important;}}
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeImageTable{height: auto !important; width:100% !important; padding:20px !important;clear:both; float:left !important; border-collapse: separate;} }
#                         @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable{height: auto !important; width:100% !important; padding:10px !important;clear:both;} }
#                         @media only screen and (max-width: 480px){.bmeMblInline table.bmeCaptionTable{width:100% !important; clear:both;} }
#                         @media only screen and (max-width: 480px){table.bmeImageTable{height: auto !important; width:100% !important; padding:10px !important;clear:both; } }
#                         @media only screen and (max-width: 480px){table.bmeCaptionTable{width:100% !important;  clear:both;} }
#                         @media only screen and (max-width: 480px){table.bmeImageContainer{width:100% !important; clear:both; float:left !important;} }
#                         @media only screen and (max-width: 480px){table.bmeImageTable td{padding:0px !important; height: auto; } }
#                         @media only screen and (max-width: 480px){img.mobile-img-large{width:100% !important; height:auto !important;} }
#                         @media only screen and (max-width: 480px){img.bmeRSSImage{max-width:320px; height:auto !important;}}
#                         @media only screen and (min-width: 640px){img.bmeRSSImage{max-width:600px !important; height:auto !important;} }
#                         @media only screen and (max-width: 480px){.trMargin img{height:10px;} }
#                         @media only screen and (max-width: 480px){div.bmefooter, div.bmeheader{ display:block !important;} }
#                         @media only screen and (max-width: 480px){.tdPart{ width:100% !important; clear:both; float:left !important; } }
#                         @media only screen and (max-width: 480px){table.blk_parent1, table.tblPart {width: 100% !important; } }
#                         @media only screen and (max-width: 480px){.tblLine{min-width: 100% !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblCenter img { margin: 0 auto; } }
#                         @media only screen and (max-width: 480px){.bmeMblCenter, .bmeMblCenter div, .bmeMblCenter span  { text-align: center !important; text-align: -webkit-center !important; } }
#                         @media only screen and (max-width: 480px){.bmeNoBr br, .bmeImageGutterRow, .bmeMblStackCenter .bmeShareItem .tdMblHide { display: none !important; } }
#                         @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable, .bmeMblInline table.bmeCaptionTable, td.bmeMblInline { clear: none !important; width:50% !important; } }
#                         @media only screen and (max-width: 480px){.bmeMblInlineHide, .bmeShareItem .trMargin { display: none !important; } }
#                         @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable img, .bmeMblShareCenter.tblContainer.mblSocialContain, .bmeMblFollowCenter.tblContainer.mblSocialContain{width: 100% !important; } }
#                         @media only screen and (max-width: 480px){.bmeMblStack> .bmeShareItem{width: 100% !important; clear: both !important;} }
#                         @media only screen and (max-width: 480px){.bmeShareItem{padding-top: 10px !important;} }
#                         @media only screen and (max-width: 480px){.tdPart.bmeMblStackCenter, .bmeMblStackCenter .bmeFollowItemIcon {padding:0px !important; text-align: center !important;} }
#                         @media only screen and (max-width: 480px){.bmeMblStackCenter> .bmeShareItem{width: 100% !important;} }
#                         @media only screen and (max-width: 480px){ td.bmeMblCenter {border: 0 none transparent !important;}}
#                         @media only screen and (max-width: 480px){.bmeLinkTable.tdPart td{padding-left:0px !important; padding-right:0px !important; border:0px none transparent !important;padding-bottom:15px !important;height: auto !important;}}
#                         @media only screen and (max-width: 480px){.tdMblHide{width:10px !important;} }
#                         @media only screen and (max-width: 480px){.bmeShareItemBtn{display:table !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblStack td {text-align: left !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblStack .bmeFollowItem{clear:both !important; padding-top: 10px !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblStackCenter .bmeFollowItemText{padding-left: 5px !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblStackCenter .bmeFollowItem{clear:both !important;align-self:center; float:none !important; padding-top:10px;margin: 0 auto;}}
#                         @media only screen and (max-width: 480px){
#                         .tdPart> table{width:100% !important;}
#                         }
#                         @media only screen and (max-width: 480px){.tdPart>table.bmeLinkContainer{ width:auto !important; }}
#                         @media only screen and (max-width: 480px){.tdPart.mblStackCenter>table.bmeLinkContainer{ width:100% !important;}}
#                         .blk_parent:first-child, .blk_parent{float:left;}
#                         .blk_parent:last-child{float:right;}
#                         /*** BMEMBF END ***/
#
#                         table[name="bmeMainBody"], body {background-color:#000000;}
#                          td[name="bmePreHeader"] {background-color:#000000;}
#                          td[name="bmeHeader"] {background:#ffffff;}
#                          td[name="bmeBody"], table[name="bmeBody"] {background-color:#ffffff;}
#                          td[name="bmePreFooter"] {background-color:#ffffff;}
#                          td[name="bmeFooter"] {background-color:#e6e6e8;}
#                          td[name="tblCell"], .blk {font-family:initial;font-weight:normal;font-size:initial;}
#                          table[name="blk_blank"] td[name="tblCell"] {font-family:Arial, Helvetica, sans-serif;font-size:14px;}
#                          [name=bmeMainContentParent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;border-collapse:separate;border-spacing:0px;overflow:hidden;}
#                          [name=bmeMainColumnParent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;overflow:visible;}
#                          [name=bmeMainColumn] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;border-collapse:separate;border-spacing:0px;}
#                          [name=bmeMainContent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;overflow:visible;border-collapse:separate;border-spacing:0px;}
#
#                         </style>
#                         <style type="text/css">
#                         body{margin:0;padding:0;}
#                         .blk_img_dd_wrap{background: #f5f5f7;padding: 40px 0;}
#                         .blk_img_drop{border: 2px dashed #e6e6e8;border-radius: 0px;color: #9ca8af;margin: 0 auto;overflow: hidden;padding: 10px;position: relative;max-width: 210px;}
#                         .blk_img_drop_icon{background: url('/images/icn/img-block-dd.png') no-repeat top;display: inline-block;float: left;height: 65px;margin-right: 10px;width: 65px;}
#                         .blk_img_txt_wrap { float: left; max-width: 135px; }
#                         .blk_img_drop_txt{font-size: 22px;font-weight: bold;line-height: 26px;margin: 5px 0; }
#                         .blk_img_drop_link{font-size: 13px;margin: 0;}
#                         .blk_img_drop_link a{color: #16a7e0;cursor: pointer;font-weight: 600;margin-left: 5px;text-decoration: underline;text-transform: lowercase;}
#                         .blk_img_drop_link a:hover{color: #72c2a1;}
#                         .blk_img_drop_txt.no-dd {display: none;}
#                         .blk_img_drop_link.no-dd span{display: none;}
#                         .blk_img_drop_link.no-dd a{ font-size: 14px; display: inline-block; margin-left: 0; padding: 0;}
#                         .ie8 .blk_img_drop_link.no-dd a { padding-top: 20px; }
#                         .blk_vid_dd_wrap{ background: #f5f5f7; padding: 40px 0; }
#                         .blk_vid_dd{ border: 2px solid #e6e6e8; border-radius: 6px; display: inline-block; padding: 10px 12px; }
#                         .blk_vid_txt{ color: #16a7e0; cursor: pointer; font-size: 20px; font-weight: 600; line-height: 40px; text-decoration: underline; }
#                         .blk_vid_txt:before{ background: url('/images/icn/editor-video-play.png') no-repeat center; border: 4px solid #9ca8af; border-radius: 8px; content: ''; display: inline-block; float: left; height: 39px; width: 39px; margin-right: 10px; }
#                         @media screen { @media (min-width: 0px) {
#                         .blk_img_drop_icon{
#                         background-image: url('/images/icn/img-block-dd.svg');
#                         background-size: 65px 65px;
#                         }
#                         }
#                         }
#                         </style>
#
#                         <table width="100%" cellspacing="0" cellpadding="0" border="0" name="bmeMainBody" style="text-align: center; background-color: rgb(0, 0, 0);" bgcolor="#000000"><tbody><tr><td width="100%" valign="top" align="center">
#                         <table cellspacing="0" cellpadding="0" border="0" name="bmeMainColumnParentTable" style="text-align: center;"><tbody><tr><td name="bmeMainColumnParent" style="border: 0px none transparent; border-radius: 0px; border-collapse: separate; overflow: visible;">
#                         <table name="bmeMainColumn" class="bmeHolder bmeMainColumn" style="max-width: 600px; overflow: visible; border-radius: 0px; border-collapse: separate; border-spacing: 0px;" cellspacing="0" cellpadding="0" border="0" align="center">    <tbody><tr><td width="100%" class="blk_container bmeHolder" name="bmePreHeader" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(0, 0, 0);" bgcolor="#000000"><div id="dv_8" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_divider" style="background-color: rgb(0, 0, 0);"><tbody><tr><td class="tblCellMain" style="padding: 10px 20px;">
#                         <table class="tblLine" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top-width: 0px; border-top-style: none; min-width: 1px;"><tbody><tr><td><span></span></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div><div id="dv_1" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_text"><tbody><tr><td>
#                         <table cellpadding="0" cellspacing="0" border="0" width="100%" class="bmeContainerRow"><tbody><tr><td class="tdPart" valign="top" align="center">
#                         <table cellspacing="0" cellpadding="0" border="0" width="600" name="tblText" class="tblText" style="float:left; background-color:transparent;" align="left"><tbody><tr><td valign="top" align="left" name="tblCell" class="tblCell" style="padding: 0px; text-align: left;"><div style="text-align: center;"><font color="#ffffff" face="Arial, Helvetica, sans-serif"><span style="font-size: 20px;">'''
#                     html += u'一封来自' + str(ctime[:4]) + u'年的信件'
#                     html += u'''</span></font></div></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div></td></tr> <tr><td width="100%" class="bmeHolder" valign="top" align="center" name="bmeMainContentParent" style="border: 0px none transparent; border-radius: 0px; border-collapse: separate; border-spacing: 0px; overflow: hidden;">
#                         <table name="bmeMainContent" style="border-radius: 0px; border-collapse: separate; border-spacing: 0px; border: 0px none transparent; overflow: visible;" width="100%" cellspacing="0" cellpadding="0" border="0" align="center"> <tbody><tr><td width="100%" class="blk_container bmeHolder" name="bmeHeader" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#                         <div id="dv_3" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_divider" style="background-color: rgb(0, 0, 0);"><tbody><tr><td class="tblCellMain" style="padding: 10px 20px;">
#                         <table class="tblLine" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top-width: 0px; border-top-style: none; min-width: 1px;"><tbody><tr><td><span></span></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div></td></tr> <tr><td width="100%" class="blk_container bmeHolder bmeBody" name="bmeBody" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#
#
#                         <div id="dv_11" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_boxtext"><tbody><tr><td align="center" name="bmeBoxContainer" style="padding-left:10px; padding-right:10px; padding-top:5px; padding-bottom:5px;">
#                         <table cellspacing="0" cellpadding="0" width="100%" name="tblText" class="tblText" border="0"><tbody><tr><td valign="top" align="left" style="padding: 20px; font-family:Arial, Helvetica, sans-serif; font-weight: normal; font-size: 14px; color: #383838;background-color:rgba(0, 0, 0, 0); border-collapse: collapse;" name="tblCell" class="tblCell"><div style=""><span style=""><br></span></div><div style=""><span style="">'''
#
#                     html += content
#
#                     html += u'''</span></div></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div><div id="dv_2" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_text"><tbody><tr><td>
#                         <table cellpadding="0" cellspacing="0" border="0" width="100%" class="bmeContainerRow"><tbody><tr><td class="tdPart" valign="top" align="center">
#                         <table cellspacing="0" cellpadding="0" border="0" width="600" name="tblText" class="tblText" style="float:left; background-color:transparent;" align="left"><tbody><tr><td valign="top" align="left" name="tblCell" class="tblCell" style="padding: 5px 20px; text-align: left;"><div style=""><div style="color: rgb(56, 56, 56); font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 400; text-align: right;"><span style=""><br></span></div><div style="color: rgb(56, 56, 56); font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 400; text-align: right;"><span style="">'''
#                     html += ctime
#
#                     html += u'''</span></div><span style=""><div style="text-align: right;"><span style="background-color: transparent;">'''
#                     html+=u'从未来邮局寄出'
#                     html+=u'''</span></div><div style="text-align: right;"><span style="background-color: transparent;"><br></span></div></span></div></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div></td></tr>
#                          </tbody>
#                         </table> </td></tr>  <tr><td width="100%" class="blk_container bmeHolder" name="bmeFooter" valign="top" align="center" style="color: rgb(102, 102, 102); border: 0px none transparent; background-color: rgb(230, 230, 232);" bgcolor="#e6e6e8"><div id="dv_10" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_footer" style="background-color: rgb(0, 0, 0);"><tbody><tr><td name="tblCell" class="tblCell" style="padding:5px;" valign="top" align="left">
#                         <table cellpadding="0" cellspacing="0" border="0" width="100%"><tbody><tr><td name="bmeBadgeText" style="text-align:center; word-break: break-word;" align="center"><span id="spnFooterText" style=" font-family: Arial, Helvetica, sans-serif; font-weight: normal; font-size: 11px ; ">
#                         <br><font color="#ffffff">'''
#                     if int(flag) == 1 and os.path.isfile(path):
#                         html+=u'附件包含录音文件，您可以下载到本地播放'
#                     html+=u'''</font></span><font color="#ffffff">
#                         <br></font><br></td></tr></tbody>
#                         </table>    </td></tr></tbody></table></div></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table>
#                         '''
#                     sender=("未来邮局", "weilai@eoen.org")
#                     subject = u'一封来自' + str(ctime[:4]) + u'年的信件'  # 邮件主题
#                     msg = Message(recipients=[email],
#                                   html=html,sender=sender,
#                                   subject=subject)
#
#                     if int(flag) == 1 and os.path.isfile(path):
#                         with app.open_resource(path) as fp:
#                             msg.attach(audio, "audio/mp3", fp.read())
#                     conn.send(msg)
#                     db.query("update post_future set status=1 where id=%s", id)
#
#
# def mail_proj(id,email,ctime,content):
#     apiUser='weilai'#API_USER
#     apiKey='JlAG4Q5G4kNLGpQC'#API_KEY
#     _from='weilai@eoen.org'#发件人地址
#     to=email#收件人地址
#     subject='一封来自'+str(ctime[:4])+'年的信件'#邮件主题
#     #html#邮件内容 (text/html)
#
#     html="""
#     <!DOCTYPE html>
#     <html>
#     <head>
#     <meta content="width=device-width, initial-scale=1.0" name="viewport">
#     <style type="text/css">
#     /*** BMEMBF Start ***/
#     [name=bmeMainBody]{min-height:1000px;}
#     @media only screen and (max-width: 480px){table.blk, table.tblText, .bmeHolder, .bmeHolder1, table.bmeMainColumn{width:100% !important;} }
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable td.tblCell{padding:0px 20px 20px 20px !important;} }
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable.bmeCaptionTableMobileTop td.tblCell{padding:20px 20px 0 20px !important;} }
#     @media only screen and (max-width: 480px){table.bmeCaptionTable td.tblCell{padding:10px !important;} }
#     @media only screen and (max-width: 480px){table.tblGtr{ padding-bottom:20px !important;} }
#     @media only screen and (max-width: 480px){td.blk_container, .blk_parent, .bmeLeftColumn, .bmeRightColumn, .bmeColumn1, .bmeColumn2, .bmeColumn3, .bmeBody{display:table !important;max-width:600px !important;width:100% !important;} }
#     @media only screen and (max-width: 480px){table.container-table, .bmeheadertext, .container-table { width: 95% !important; } }
#     @media only screen and (max-width: 480px){.mobile-footer, .mobile-footer a{ font-size: 13px !important; line-height: 18px !important; } .mobile-footer{ text-align: center !important; } table.share-tbl { padding-bottom: 15px; width: 100% !important; } table.share-tbl td { display: block !important; text-align: center !important; width: 100% !important; } }
#     @media only screen and (max-width: 480px){td.bmeShareTD, td.bmeSocialTD{width: 100% !important; } }
#     @media only screen and (max-width: 480px){td.tdBoxedTextBorder{width: auto !important;}}
#     @media only screen and (max-width: 480px){table.blk, table[name=tblText], .bmeHolder, .bmeHolder1, table[name=bmeMainColumn]{width:100% !important;} }
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable td[name=tblCell]{padding:0px 20px 20px 20px !important;} }
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable.bmeCaptionTableMobileTop td[name=tblCell]{padding:20px 20px 0 20px !important;} }
#     @media only screen and (max-width: 480px){table.bmeCaptionTable td[name=tblCell]{padding:10px !important;} }
#     @media only screen and (max-width: 480px){table[name=tblGtr]{ padding-bottom:20px !important;} }
#     @media only screen and (max-width: 480px){td.blk_container, .blk_parent, [name=bmeLeftColumn], [name=bmeRightColumn], [name=bmeColumn1], [name=bmeColumn2], [name=bmeColumn3], [name=bmeBody]{display:table !important;max-width:600px !important;width:100% !important;} }
#     @media only screen and (max-width: 480px){table[class=container-table], .bmeheadertext, .container-table { width: 95% !important; } }
#     @media only screen and (max-width: 480px){.mobile-footer, .mobile-footer a{ font-size: 13px !important; line-height: 18px !important; } .mobile-footer{ text-align: center !important; } table[class="share-tbl"] { padding-bottom: 15px; width: 100% !important; } table[class="share-tbl"] td { display: block !important; text-align: center !important; width: 100% !important; } }
#     @media only screen and (max-width: 480px){td[name=bmeShareTD], td[name=bmeSocialTD]{width: 100% !important; } }
#     @media only screen and (max-width: 480px){td[name=tdBoxedTextBorder]{width: auto !important;}}
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeImageTable{height: auto !important; width:100% !important; padding:20px !important;clear:both; float:left !important; border-collapse: separate;} }
#     @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable{height: auto !important; width:100% !important; padding:10px !important;clear:both;} }
#     @media only screen and (max-width: 480px){.bmeMblInline table.bmeCaptionTable{width:100% !important; clear:both;} }
#     @media only screen and (max-width: 480px){table.bmeImageTable{height: auto !important; width:100% !important; padding:10px !important;clear:both; } }
#     @media only screen and (max-width: 480px){table.bmeCaptionTable{width:100% !important;  clear:both;} }
#     @media only screen and (max-width: 480px){table.bmeImageContainer{width:100% !important; clear:both; float:left !important;} }
#     @media only screen and (max-width: 480px){table.bmeImageTable td{padding:0px !important; height: auto; } }
#     @media only screen and (max-width: 480px){img.mobile-img-large{width:100% !important; height:auto !important;} }
#     @media only screen and (max-width: 480px){img.bmeRSSImage{max-width:320px; height:auto !important;}}
#     @media only screen and (min-width: 640px){img.bmeRSSImage{max-width:600px !important; height:auto !important;} }
#     @media only screen and (max-width: 480px){.trMargin img{height:10px;} }
#     @media only screen and (max-width: 480px){div.bmefooter, div.bmeheader{ display:block !important;} }
#     @media only screen and (max-width: 480px){.tdPart{ width:100% !important; clear:both; float:left !important; } }
#     @media only screen and (max-width: 480px){table.blk_parent1, table.tblPart {width: 100% !important; } }
#     @media only screen and (max-width: 480px){.tblLine{min-width: 100% !important;}}
#     @media only screen and (max-width: 480px){.bmeMblCenter img { margin: 0 auto; } }
#     @media only screen and (max-width: 480px){.bmeMblCenter, .bmeMblCenter div, .bmeMblCenter span  { text-align: center !important; text-align: -webkit-center !important; } }
#     @media only screen and (max-width: 480px){.bmeNoBr br, .bmeImageGutterRow, .bmeMblStackCenter .bmeShareItem .tdMblHide { display: none !important; } }
#     @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable, .bmeMblInline table.bmeCaptionTable, td.bmeMblInline { clear: none !important; width:50% !important; } }
#     @media only screen and (max-width: 480px){.bmeMblInlineHide, .bmeShareItem .trMargin { display: none !important; } }
#     @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable img, .bmeMblShareCenter.tblContainer.mblSocialContain, .bmeMblFollowCenter.tblContainer.mblSocialContain{width: 100% !important; } }
#     @media only screen and (max-width: 480px){.bmeMblStack> .bmeShareItem{width: 100% !important; clear: both !important;} }
#     @media only screen and (max-width: 480px){.bmeShareItem{padding-top: 10px !important;} }
#     @media only screen and (max-width: 480px){.tdPart.bmeMblStackCenter, .bmeMblStackCenter .bmeFollowItemIcon {padding:0px !important; text-align: center !important;} }
#     @media only screen and (max-width: 480px){.bmeMblStackCenter> .bmeShareItem{width: 100% !important;} }
#     @media only screen and (max-width: 480px){ td.bmeMblCenter {border: 0 none transparent !important;}}
#     @media only screen and (max-width: 480px){.bmeLinkTable.tdPart td{padding-left:0px !important; padding-right:0px !important; border:0px none transparent !important;padding-bottom:15px !important;height: auto !important;}}
#     @media only screen and (max-width: 480px){.tdMblHide{width:10px !important;} }
#     @media only screen and (max-width: 480px){.bmeShareItemBtn{display:table !important;}}
#     @media only screen and (max-width: 480px){.bmeMblStack td {text-align: left !important;}}
#     @media only screen and (max-width: 480px){.bmeMblStack .bmeFollowItem{clear:both !important; padding-top: 10px !important;}}
#     @media only screen and (max-width: 480px){.bmeMblStackCenter .bmeFollowItemText{padding-left: 5px !important;}}
#     @media only screen and (max-width: 480px){.bmeMblStackCenter .bmeFollowItem{clear:both !important;align-self:center; float:none !important; padding-top:10px;margin: 0 auto;}}
#     @media only screen and (max-width: 480px){
#     .tdPart> table{width:100% !important;}
#     }
#     @media only screen and (max-width: 480px){.tdPart>table.bmeLinkContainer{ width:auto !important; }}
#     @media only screen and (max-width: 480px){.tdPart.mblStackCenter>table.bmeLinkContainer{ width:100% !important;}}
#     .blk_parent:first-child, .blk_parent{float:left;}
#     .blk_parent:last-child{float:right;}
#     /*** BMEMBF END ***/
#
#     table[name="bmeMainBody"], body {background-color:#000000;}
#      td[name="bmePreHeader"] {background-color:#000000;}
#      td[name="bmeHeader"] {background:#ffffff;}
#      td[name="bmeBody"], table[name="bmeBody"] {background-color:#ffffff;}
#      td[name="bmePreFooter"] {background-color:#ffffff;}
#      td[name="bmeFooter"] {background-color:#e6e6e8;}
#      td[name="tblCell"], .blk {font-family:initial;font-weight:normal;font-size:initial;}
#      table[name="blk_blank"] td[name="tblCell"] {font-family:Arial, Helvetica, sans-serif;font-size:14px;}
#      [name=bmeMainContentParent] {border-color:transparent;border-width:0px;border-style:none;border-radius:5px;border-collapse:separate;border-spacing:0px;overflow:hidden;}
#      [name=bmeMainColumnParent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;overflow:visible;}
#      [name=bmeMainColumn] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;border-collapse:separate;border-spacing:0px;}
#      [name=bmeMainContent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;overflow:visible;border-collapse:separate;border-spacing:0px;}
#
#     </style>
#     <!--[if gte mso 9]>
#     <xml>
#     <o:OfficeDocumentSettings>
#     <o:AllowPNG/>
#     <o:PixelsPerInch>96</o:PixelsPerInch>
#     </o:OfficeDocumentSettings>
#     </xml>
#     <![endif]-->
#
#     </head>
#     <body marginheight=0 marginwidth=0 topmargin=0 leftmargin=0 style="height: 100% !important; margin: 0; padding: 0; width: 100% !important;min-width: 100%;">
#     <style type="text/css">
#     body{height:100%;margin:0;padding:0;}
#     .blk_img_dd_wrap{background: #f5f5f7;padding: 40px 0;}
#     .blk_img_drop{border: 2px dashed #e6e6e8;border-radius: 6px;color: #9ca8af;margin: 0 auto;overflow: hidden;padding: 10px;position: relative;max-width: 210px;}
#     .blk_img_drop_icon{background: url('/images/icn/img-block-dd.png') no-repeat top;display: inline-block;float: left;height: 65px;margin-right: 10px;width: 65px;}
#     .blk_img_txt_wrap { float: left; max-width: 135px; }
#     .blk_img_drop_txt{font-size: 22px;font-weight: bold;line-height: 26px;margin: 5px 0; }
#     .blk_img_drop_link{font-size: 13px;margin: 0;}
#     .blk_img_drop_link a{color: #16a7e0;cursor: pointer;font-weight: 600;margin-left: 5px;text-decoration: underline;text-transform: lowercase;}
#     .blk_img_drop_link a:hover{color: #72c2a1;}
#     .blk_img_drop_txt.no-dd {display: none;}
#     .blk_img_drop_link.no-dd span{display: none;}
#     .blk_img_drop_link.no-dd a{ font-size: 14px; display: inline-block; margin-left: 0; padding: 0;}
#     .ie8 .blk_img_drop_link.no-dd a { padding-top: 20px; }
#     .blk_vid_dd_wrap{ background: #f5f5f7; padding: 40px 0; }
#     .blk_vid_dd{ border: 2px solid #e6e6e8; border-radius: 6px; display: inline-block; padding: 10px 12px; }
#     .blk_vid_txt{ color: #16a7e0; cursor: pointer; font-size: 20px; font-weight: 600; line-height: 40px; text-decoration: underline; }
#     .blk_vid_txt:before{ background: url('/images/icn/editor-video-play.png') no-repeat center; border: 4px solid #9ca8af; border-radius: 8px; content: ''; display: inline-block; float: left; height: 39px; width: 39px; margin-right: 10px; }
#     @media screen { @media (min-width: 0px) {
#     .blk_img_drop_icon{
#     background-image: url('/images/icn/img-block-dd.svg');
#     background-size: 65px 65px;
#     }
#     }
#     }
#     </style>
#
#
#     <table width="100%" cellspacing="0" cellpadding="0" border="0" name="bmeMainBody" style="background-color: rgb(0, 0, 0);" bgcolor="#000000"><tbody><tr><td width="100%" valign="top" align="center">
#     <table cellspacing="0" cellpadding="0" border="0" name="bmeMainColumnParentTable"><tbody><tr><td name="bmeMainColumnParent" style="border: 0px none transparent; border-radius: 0px; border-collapse: separate; overflow: visible;">
#     <table name="bmeMainColumn" class="bmeHolder bmeMainColumn" style="max-width: 600px; overflow: visible; border-radius: 0px; border-collapse: separate; border-spacing: 0px;" cellspacing="0" cellpadding="0" border="0" align="center">    <tbody><tr><td width="100%" class="blk_container bmeHolder" name="bmePreHeader" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(0, 0, 0);" bgcolor="#000000"><div id="dv_8" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_divider" style="background-color: rgb(0, 0, 0);"><tbody><tr><td class="tblCellMain" style="padding: 10px 20px;">
#     <table class="tblLine" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top-width: 0px; border-top-style: none; min-width: 1px;"><tbody><tr><td><span></span></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div><div id="dv_1" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_text"><tbody><tr><td>
#     <table cellpadding="0" cellspacing="0" border="0" width="100%" class="bmeContainerRow"><tbody><tr><td class="tdPart" valign="top" align="center">
#     <table cellspacing="0" cellpadding="0" border="0" width="600" name="tblText" class="tblText" style="float:left; background-color:transparent;" align="left"><tbody><tr><td valign="top" align="left" name="tblCell" class="tblCell" style="padding: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 400; color: rgb(56, 56, 56); text-align: left;"><div style="line-height: 200%; text-align: center;"><span style="color: #ffffff; font-size: 20px; line-height: 200%; font-family: '微軟正黑體', 'Microsoft JhengHei', STXihei, '华文细黑', sans-serif;">一封来自
#     """
#     html+=str(ctime[:4])
#
#     html+="""年的信件</span></div></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div></td></tr> <tr><td width="100%" class="bmeHolder" valign="top" align="center" name="bmeMainContentParent" style="border: 0px none transparent; border-radius: 5px; border-collapse: separate; border-spacing: 0px; overflow: hidden;">
#     <table name="bmeMainContent" style="border-radius: 0px; border-collapse: separate; border-spacing: 0px; border: 0px none transparent; overflow: visible;" width="100%" cellspacing="0" cellpadding="0" border="0" align="center"> <tbody><tr><td width="100%" class="blk_container bmeHolder" name="bmeHeader" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#     <div id="dv_3" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_divider" style="background-color: rgb(0, 0, 0);"><tbody><tr><td class="tblCellMain" style="padding: 10px 20px;">
#     <table class="tblLine" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top-width: 0px; border-top-style: none; min-width: 1px;"><tbody><tr><td><span></span></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div></td></tr> <tr><td width="100%" class="blk_container bmeHolder bmeBody" name="bmeBody" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#
#
#     <div id="dv_11" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_boxtext"><tbody><tr><td align="center" name="bmeBoxContainer" style="padding-left:10px; padding-right:10px; padding-top:5px; padding-bottom:5px;">
#     <table cellspacing="0" cellpadding="0" width="100%" name="tblText" class="tblText" border="0"><tbody><tr><td valign="top" align="left" style="padding: 20px; font-family:Arial, Helvetica, sans-serif; font-weight: normal; font-size: 14px; color: #383838;background-color:rgba(0, 0, 0, 0); border-collapse: collapse;" name="tblCell" class="tblCell"><div style="line-height: 200%;"><span style="font-size: 14px; font-family: '微軟正黑體', 'Microsoft JhengHei', STXihei, '华文细黑', sans-serif; color: #191919; line-height: 200%;">
#     """""
#     html+=content
#     html+="""</span></div></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div><div id="dv_2" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_text"><tbody><tr><td>
#     <table cellpadding="0" cellspacing="0" border="0" width="100%" class="bmeContainerRow"><tbody><tr><td class="tdPart" valign="top" align="center">
#     <table cellspacing="0" cellpadding="0" border="0" width="600" name="tblText" class="tblText" style="float:left; background-color:transparent;" align="left"><tbody><tr><td valign="top" align="left" name="tblCell" class="tblCell" style="padding: 5px 20px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 400; color: rgb(56, 56, 56); text-align: left;"><div style="line-height: 200%; text-align: right;"><span style="font-family: '微軟正黑體', 'Microsoft JhengHei', STXihei, '华文细黑', sans-serif; font-size: 16px;">
#     """
#     html+=str(ctime)
#     html+="""
#     <br>从未来邮局寄出</span><br><br></div></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div></td></tr> <tr><td width="100%" class="blk_container bmeHolder" name="bmePreFooter" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#
#     </td></tr> </tbody>
#     </table> </td></tr>  <tr><td width="100%" class="blk_container bmeHolder" name="bmeFooter" valign="top" align="center" style="color: rgb(102, 102, 102); border: 0px none transparent; background-color: rgb(230, 230, 232);" bgcolor="#e6e6e8"><div id="dv_10" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_footer" style="background-color: rgb(0, 0, 0);"><tbody><tr><td name="tblCell" class="tblCell" style="padding:5px;" valign="top" align="left">
#     <table cellpadding="0" cellspacing="0" border="0" width="100%"><tbody><tr><td name="bmeBadgeText" style="text-align:center; word-break: break-word;" align="center"><span id="spnFooterText" style="font-family: Arial, Helvetica, sans-serif; font-weight: normal; font-size: 11px; line-height: 140%; color: rgb(255, 255, 255);">
#     <br>&#27492;&#23553;&#20449;&#20214;&#26159;&#24744;&#20197;&#21069;&#23492;&#20986;&#30340;&#26410;&#26469;&#20449;&#20214;&#65292;&#24744;&#29616;&#22312;&#26159;&#21542;&#36824;&#35760;&#24471;&#65311;</span>
#     <br></td></tr></tbody>
#     </table>
#     <!-- /Test Path -->
#     </body>
#     </html>
#     """
#
#     url='https://sendcloud.sohu.com/apiv2/mail/send'
#     data={
#         'apiUser':apiUser,
#         'apiKey':apiKey,
#         'from':_from,
#         'to':to,
#         'subject':subject,
#         'html':html
#     }
#     re=requests.post(url,data=data)
#     dictinfo = json.loads(re.text)
#     status=1
#     if dictinfo.get('statusCode') != 200:
#         status=2
#     db.query("update post_future set status=%s where id=%s",[status,id])
#










if __name__ == '__main__':

    app.run()



