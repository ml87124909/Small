# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/E003_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

from basic.wxbase import WxPay
import  os

class cE003_dl(cBASE_DL):
    def init_data(self):

        self.FDT = [
            ['', '', ''],  # 0
            ['退款单号', '4rem', ''],  # 1
            ['申请用户', '10rem', ''],  # 2
            ['申请原因', '10rem', ''],  # 3
            ['退款截图', '10rem', ''],  # 4
            ['申请退款金额', '10rem', ''],  # 5
            ['订单合订金额', '6rem', ''],  # 6
            ['状态', '10rem', ''],  # 7


        ]
        # self.GNL=[] #列表上出现的
        self.GNL = self.parse_GNL([0,1, 2, 3, 4, 5, 6, 7])



    def mRight(self):
            

        sql="""
            select id,r_num,w_name,reason,
                (select array_agg(pic) from images_api 
                where images_api.timestamp=refund_money.timestamp and images_api.other_id=refund_money.order_id
                and refund_money.usr_id=images_api.usr_id and ctype=0),
                r_money,order_money,status_str,order_id,status
            from refund_money
            where COALESCE(del_flag,0)=0 and  usr_id=%s order by ctime desc
        """%self.usr_id_p
        self.pageNo = self.GP('pageNo', '')
        if self.pageNo == '':
            self.pageNo = '1'
        self.pageNo = int(self.pageNo)


        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo)
        #L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(lT, iN, self.pageNo)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L


    def get_order_reply_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        sid = self.GP('sid', '')
        if id == '' or sid=='':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select order_id,order_num,r_num from refund_money where id=%s and status=99"
        l,t=self.db.select(sql,id)
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '退款单状态不正常'
            return dR
        mall = self.oMALL.get(self.usr_id_p)
        if mall == {}:
            dR['code'] = '1'
            dR['MSG'] = '请到店铺设置填写小程序设置'
            return dR
        order_id, order_num, r_num=l[0]
        sql="select balance,new_total,wechat_user_id from wechat_mall_order where usr_id=%s and id=%s and status=99"
        ll,tt=self.db.select(sql,[self.usr_id_p,order_id])
        if tt==0:
            dR['code'] = '1'
            dR['MSG'] = '退款单状态不正常'
            return dR
        balance, new_total,wechat_user_id=ll[0]

        sql="update refund_money set status=98,status_str='退款成功',refund_type=%s where id=%s and status=99"
        self.db.query(sql,[sid,id])
        sql = "update wechat_mall_order set status=98,status_str='退款成功' where usr_id=%s and id=%s"
        self.db.query(sql, [self.usr_id_p, order_id])
        sql = "update wechat_mall_order_detail set status=98,status_str='退款成功' where usr_id=%s  and order_id=%s"
        self.db.query(sql, [self.usr_id_p, order_id])
        self.write_order_log(id, 'status,status_str', 'status=98,status_str=退款成功', '后台同意退款,更新订单表,订单明细表状态')
        if str(sid)=='2':
            sql="update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
            self.db.query(sql,[new_total,wechat_user_id])
        else:
            if balance==new_total:
                sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
                self.db.query(sql, [new_total, wechat_user_id])
            else:
                sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
                self.db.query(sql, [balance, wechat_user_id])
                a=self.order_refund(order_id, order_num, r_num,wechat_user_id)
                if a==1:
                    dR['code'] = '1'
                    dR['MSG'] = '退款操作失败!'
                    return dR
        sql="""insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,remark,
                cid,ctime)values(%s,%s,3,'消费',%s,4,'退回','退款',%s,now())"""
        self.db.query(sql,[self.usr_id_p,wechat_user_id,new_total,self.usr_id])
        self.oUSER.update(self.usr_id_p,wechat_user_id)
        dR['code'] = '0'
        dR['MSG'] = '退款操作完成!'
        return dR

    def order_refund(self,order_id,order_num,re_num,wechat_user_id):


        mall = self.oMALL.get(self.usr_id_p)

        app_id = mall.get('appid','')
        secret = mall.get('secret','')
        wx_mch_id = mall.get('mchid','')
        wx_mch_key = mall.get('mchkey','')
        base_url = self.base_url#'https://malishop.janedao.cn'
        api_cert_path = mall.get('cert','')
        api_key_path =mall.get('key','')

        notify_url = base_url + '/refund/%s/notify' % self.usr_id_p
        wxpay = WxPay(app_id, wx_mch_id, wx_mch_key, notify_url)


        sql="select total_fee from wechat_mall_payment where order_id=%s and payment_number=%s and usr_id=%s "
        l,t=self.db.select(sql,[order_id,order_num,self.usr_id_p])
        if t==0:
            return 1
        total_fee=l[0][0]
        data = {  # 退款信息
            'out_trade_no': order_num,  # 商户订单号
            'total_fee': total_fee,  # 订单金额
            'refund_fee': total_fee  # 退款金额
        }
        sql = "select out_refund_no from wechat_mall_refund where out_trade_no=%s and usr_id=%s"
        lT, iN = self.db.select(sql, [order_num, self.usr_id_p])
        if iN==0:
            data['out_refund_no']=re_num  # 商户退款单号
            refund = {  # 退款信息
            'out_trade_no': order_num,  # 商户订单号
            'total_fee': total_fee,  # 订单金额
            'refund_fee': total_fee,  # 退款金额
            'out_refund_no':re_num,
            'usr_id':self.usr_id_p,
            'wechat_user_id':wechat_user_id
            }

            self.db.insert('wechat_mall_refund',refund)
            data['notify_url'] = notify_url  # 商户退款回调
            raw=wxpay.refund(api_cert_path,api_key_path,**data)

            if raw['return_code'] == 'SUCCESS' and raw['result_code']  == 'SUCCESS':

                try:
                    sql="select id from wechat_mall_refund where out_trade_no=%s and out_refund_no=%s and total_fee=%s and usr_id=%s"
                    l,i=self.db.select(sql,[raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],self.usr_id_p])
                    if i == 0:
                        return 1

                    refund = {
                        'refund_id': raw['refund_id']
                        , 'result_code': raw['result_code']
                        , 'return_msg': raw['return_msg']
                        ,'status':1
                        ,'status_str': '成功'
                        ,'utime': self.getToday(9)
                    }

                    self.db.update("wechat_mall_refund", refund, "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" %(raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],self.usr_id_p))

                    sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                values(%s,%s,%s,%s,%s,now())
                            """
                    self.db.query(sql, [self.usr_id_p, 'wechat_mall_refund',
                                        "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                                        raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.usr_id_p),
                                   '退款回调更新wechat_mall_refund表数据', self.usr_id])
                    return 0
                except:
                    return 1

            else:
                try:
                    datas = {
                        'status_str': '失败',
                        'result_code': raw['result_code'],
                        'utime':self.getToday(9)
                    }
                    self.db.update("wechat_mall_refund", datas, "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" %(raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],self.usr_id_p))
                    return 1
                except:
                    return 1
        out_refund_no=lT[0][0]
        data['out_refund_no'] = out_refund_no  # 商户退款单号
        raw = wxpay.refund(api_cert_path, api_key_path, **data)
        if raw['return_code'] == 'SUCCESS' and raw['result_code'] == 'SUCCESS':
            try:
                sql = "select id from wechat_mall_refund where out_trade_no=%s and out_refund_no=%s and total_fee=%s and usr_id=%s"
                l, i = self.db.select(sql,
                                      [raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.usr_id_p])
                if i == 0:
                    return 1

                refund = {
                    'refund_id': raw['refund_id']
                    , 'result_code': raw['result_code']
                    , 'return_msg': raw['return_msg']
                    , 'status': 1
                    , 'status_str': '成功'
                    , 'utime': self.getToday(9)
                }

                self.db.update("wechat_mall_refund", refund,
                               "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                               raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.usr_id_p))

                sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                            values(%s,%s,%s,%s,%s,now())
                        """
                self.db.query(sql, [self.usr_id_p, 'wechat_mall_refund',
                                    "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                                    raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.usr_id_p),
                                    '退款回调更新wechat_mall_refund表数据', self.usr_id])
                return 0
            except:
                return 1

        else:
            try:
                datas = {
                    'status_str': '失败',
                    'result_code': raw['result_code'],
                    'utime': self.getToday(9)
                }
                self.db.update("wechat_mall_refund", datas,
                               "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                               raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.usr_id_p))
                return 1
            except:
                return 1

    def get_retweet_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        sid = self.GP('sid', '')
        if id == '' or sid=='':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select order_id,order_num,r_num from refund_money where id=%s and status=99"
        l,t=self.db.select(sql,id)
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '退款单状态不正常'
            return dR

        order_id, order_num, r_num=l[0]
        sql="select balance,new_total,wechat_user_id from wechat_mall_order where usr_id=%s and id=%s and status=99"
        ll,tt=self.db.select(sql,[self.usr_id_p,order_id])
        if tt==0:
            dR['code'] = '1'
            dR['MSG'] = '退款单状态不正常'
            return dR


        sql="update refund_money set status=97,status_str='退款失败',not_memo=%s,uid=%s,utime=now() where id=%s and status=99"
        self.db.query(sql,[sid,self.usr_id,id])
        sql = "update wechat_mall_order set status=97,status_str='退款失败',uid=%s,utime=now() where usr_id=%s and id=%s"
        self.db.query(sql, [self.usr_id, self.usr_id_p,order_id])
        sql = "update wechat_mall_order_detail set status=97,status_str='退款失败',uid=%s,utime=now() where usr_id=%s  and order_id=%s"
        self.db.query(sql, [self.usr_id,self.usr_id_p, order_id])
        self.write_order_log(id, 'status,status_str', 'status=97,status_str=退款失败', '后台驳回退款,更新订单表,订单明细表状态')

        dR['code'] = '0'
        dR['MSG'] = '驳回原因提交成功!'
        return dR

    def get_retweetv_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')

        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select not_memo from refund_money where id=%s and status=97"
        l,t=self.db.select(sql,id)
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '退款单状态不正常'
            return dR

        memo=l[0][0]
        dR['code'] = '0'
        dR['memo'] =memo

        return dR


