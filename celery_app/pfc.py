# -*- coding: utf-8 -*-

##############################################################################
#
#
##############################################################################


from flask import Flask,json
#from flask_mail import Mail,Message
from celery import Celery
from celery_app import c
import time

app=Flask(__name__)


import requests,json,os,random,traceback,oss2
from imp import reload
import datetime
import basic
reload(basic)
from basic import public
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





if __name__ == '__main__':

    app.run()



