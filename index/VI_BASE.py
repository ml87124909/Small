# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
"""index/VI_BASE.py"""

#import os, importlib, urllib, time, datetime, random, jwt, hashlib, base64, requests, oss2

#from qiniu import Auth, put_stream, put_data,BucketManager

from basic.publicw import cVIEW_wx
from flask import session
#from wechatpy import WeChatClient
#from wechatpy.client.api import WeChatWxa
#from basic.wxbase import wx_minapp_login,WXBizDataCrypt,WxPay
from werkzeug import secure_filename
import hashlib,time,json,datetime
# {
#     -1: u'服务器内部错误',
#     0: u'接口调用成功',
#     403: u'禁止访问',
#     405: u'错误的请求类型',
#     501: u'数据库错误',
#     502: u'并发异常，请重试',
#     600: u'缺少参数',
#     601: u'无权操作:缺少 token',
#     602: u'签名错误',
#     700: u'暂无数据',
#     701: u'该功能暂未开通',
#     702: u'资源余额不足',
#     901: u'登录超时',
#     300: u'缺少{}参数',
#     400: u'域名错误',
#     401: u'该域名已删除',
#     402: u'该域名已禁用',
#     404: u'暂无数据',
#     10000: u'微信用户未注册',
#     'ok':'success'
# }
class cVI_BASE(cVIEW_wx):

    def getmtcdata(self,type,df='',title='请选择'):
        if title!='':L=[['',title,'']]
        else:L=[]
        if type!='':
            sql="select id,txt1 from mtc_t where type='%s' order by sort"%type
            lT,iN=self.db.select(sql)
            if iN>0:
                for e in list(lT):
                    id,txt=e
                    b = ''
                    if str(df) == str(id):
                        b = ' selected="selected"'
                    L.append([id,txt,b])
        return L

    def get_province(self,df=''):
        sql = """
        SELECT code , cname from province
        """
        L,iTotal_length=self.db.select(sql)
        option = [['','请选择','']]
        for r in L:
            b = ''
            if r[0] == df : b = ' selected="selected"'
            d = [r[0],'%s'%r[1],b]
            option.append(d)
        return option

    def get_city(self,province,df=''):
        option = [['','请选择','']]
        if not province: return option
        sql = """
        SELECT code , cname from city where parent_code = '%s'
        """ % province
        L,iTotal_length=self.db.select(sql)

        for r in L:
            b = ''
            if r[0] == df : b = ' selected="selected"'
            d = [r[0],'%s'%r[1],b]
            option.append(d)
        return option

    def get_area(self,city,df=''):
        option = [['','请选择','']]
        if not city: return option
        sql = """
        SELECT code , cname from area where parent_code = '%s'
        """ % city
        L,iTotal_length=self.db.select(sql)
        for r in L:
            b = ''
            if r[0] == df : b = ' selected="selected"'
            d = [r[0],'%s'%r[1],b]
            option.append(d)
        return option

    def get_session(self, key, default=None):
        return session.get(key, default)

    def set_session(self, key, value):
        session[key] = value


    def Get_New_Code(self,cdtype,length,type = 0):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]
        code = cdtype + danhao[2:] + romcode
        return code


    def checkshopbox(self,pid,gamount):
        #gamount 传入购买总量 包括购物车量
        L = {'error':0,'msg':'操作成功'}

        sql_vip = """ select top 1 1 from wechat_mall_user where usr_id = %s and coalesce(vip,0) != 0 """%self.usr_id
        vt,vN = self.db.select(sql_vip)
        if vN >0:
            pass
        else:
            L['error'] = 3
            L['msg'] = '会员卡正在绑定，请稍后...'
            return L

        if pid not in ['',0]:
            sql_amount = """ select xg_amount xg_amount,hd.cname,coalesce(gs.amount,0) as sy_amount from goodsale gs LEFT JOIN hd_item_info hd
                                    ON gs.item_id = hd.item_id where gs.id = %s limit 1"""%pid
            L = self.db.fetch(sql_amount)

            #by Mast 20171106
            if int(L.get('sy_amount','0'))<int(gamount):
                L['error'] = 5#库存不足
                L['msg'] = str(L.get('cname','') or '')+'库存不足'
                return L

            xg_amount = L.get('xg_amount',None)
            xg = xg_amount
            if xg_amount not in [None,'']:

                #购物车数量
                sql = """ select coalesce(sum(coalesce(amount,0)),0) amount from shopbox where cid = %s and goodsid = %s """%(self.usr_id,pid)

                L1 = self.db.fetch(sql)

                #订单数量
                sql_order = """ select coalesce(sum(coalesce(amount,0)),0) amount from orderdetail od 
                    inner join orders o on o.code = od.code where od.cid = %s and od.goodsid = %s
                                and o.cstatus != 3
                            """%(self.usr_id,pid)
                L2 = self.db.fetch(sql_order)
                if float(gamount)+float(L2.get('amount',0)) >float(xg_amount):
                    if L1.get('amount',0) > 0:
                        L['error'] = 2#存在购物车中
                        L['msg'] = str(L.get('cname','') or '')+'购物车已限量'
                    else:
                        L['error'] = 4#存在订单中
                        L['msg'] = str(L.get('cname','') or '')+'订单已限量'
                else:
                    pass
            else:
                xg = 1
                sql = """ select top 1 1 from shopbox where cid = %s and goodsid = %s"""%(self.usr_id,pid)
                lt,iN = self.db.select(sql)
                if iN >0:
                    L['error'] = 2#存在购物车
                    L['msg'] = str(L.get('cname','') or '')+'购物车已限量'
                else:
                    pass
                sql_order = """ select top 1 1 from orderdetail od inner join orders o on o.code = od.code where od.cid = %s and od.goodsid = %s
                                and o.cstatus != 3
                            """%(self.usr_id,pid)
                lt1,iN1 = self.db.select(sql_order)
                if iN1 >0:
                    L['error'] = 4#存在订单
                    L['msg'] = str(L.get('cname','') or '')+'订单已限量'
                else:
                    pass
        else:
            L['error'] = 1
            L['msg'] = '操作异常'
        return L

    def checkorders(self,pid,gmamount):#验证订单数量
        L = {'error':0,'msg':''}
        plid = pid.split(',')
        if pid !='':
            for e in plid:
                sql_amount = """ select top 1 gs.xg_amount,hd.cname from goodsale gs LEFT JOIN hd_item_info hd
                                    ON gs.item_id = hd.item_id where gs.id = %s """%e
                LL = self.db.fetch(sql_amount)
                xg_amount = LL.get('xg_amount',None)
                gmamount1 = gmamount.get(e,1)
                if xg_amount not in [None,'']:
                    sql = """ select coalesce(sum(coalesce(od.amount,0)),0) amount from orderdetail od 
                    inner join orders o on o.code = od.code where od.cid = %s and od.goodsid = %s
                                and o.cstatus != 3
                            """%(self.usr_id,e)
                    L1 = self.db.fetch(sql)
                    if float(L1.get('amount',0)) > float(xg_amount) - float(gmamount1):
                        if L1.get('amount',0) > 0:
                            L['error'] = 2#存在订单中
                            L['msg'] = str(L.get('cname','') or '')+'订单已限量'
                    else:
                        pass
                else:
                    sql = """ select top 1 1 from orderdetail od 
                    inner join orders o on o.code = od.code where od.cid = %s and od.goodsid = %s
                                and o.cstatus != 3
                            """%(self.usr_id,e)
                    lt,iN = self.db.select(sql)
                    if iN >0:
                        L['error'] = 2#存在订单中
                        L['msg'] = str(L.get('cname','') or '')+'订单已限量'
                        break
                    else:
                        pass
        else:
            L['error'] = 1
            L['msg'] = '操作异常'
        return L

    def checkjforders(self,pid):#验证积分订单是否可以继续可以下单
        #pid 积分兑换发布明细ID error:0 可兑换 1积分不足 2处理异常 3限量提示 5总限量 4活动结束
        L = {'error':0,'msg':''}

        if pid !='':
            try:
                sql_amount = """ select top 1 j.v_code,jf.xg_amount,jf.samount,j.alltimes,
                coalesce(j.cstatus,0) cstatus,coalesce(jf.jf_price,0) jf_price
                            from jfsale_detail jf inner join jfsales j
                            ON jf.v_code = j.v_code where jf.id = %s """%pid
                LL = self.db.fetch(sql_amount)
                xg_amount = LL.get('xg_amount',0)
                alltimes = LL.get('alltimes',0)
                cstatus = LL.get('cstatus',0)
                v_code = LL.get('v_code','')
                jf_price = LL.get('jf_price',0)
                samount = LL.get('samount',0)
                if samount == 0:
                    L['error'] = 4
                    L['msg'] = '此商品兑换活动结束'
                    return L
                if cstatus != 1 or v_code == '':#关闭了活动
                    L['error'] = 4 #此商品兑换活动结束
                    L['msg'] = '此商品兑换活动结束'
                    return L
                if alltimes != 0:#设置总限制
                    #总限制 把未结算的也算进来
                    sqlall = """
                        SELECT coalesce(sum(coalesce(nd.amount,0)),0) amount,
                        coalesce(sum(case when coalesce(cstatus,0)=0 then 1 else 0 end),0) uamount  FROM
                        neworders_detail nd
                        INNER JOIN neworders n ON nd.code = n.code
                        INNER JOIN jfsale_detail AS jd ON jd.id = nd.m_id
                        WHERE jd.v_code = '%s' AND n.otype = 1 AND coalesce(n.cstatus,0) IN (0,1,2)
                        and n.cid = %s
                    """%(v_code,self.usr_id)
                    Lall = self.db.fetch(sqlall)
                    if Lall.get('amount',0) >=alltimes:
                        L['error'] = 5 #总限量
                        L['msg'] = '本次活动限兑'+str(alltimes)+'次'
                        if Lall.get('uamount',0) !=0:
                            L['msg'] += ',您还有未结算单据'
                        return L

                if xg_amount !=0:#设置单个限制
                    #单个限制 把未结算的也算进来
                    sqlall = """
                        SELECT coalesce(sum(coalesce(nd.amount,0)),0) amount,
                        coalesce(sum(case when isnull(cstatus,0)=0 then 1 else 0 end),0) uamount  FROM
                        neworders_detail nd
                        INNER JOIN neworders n ON nd.code = n.code
                        WHERE nd.m_id = %s AND n.otype = 1 AND coalesce(n.cstatus,0) IN (0,1,2)
                        and n.cid = %s
                    """%(pid,self.usr_id)
                    Lx = self.db.fetch(sqlall)
                    if Lx.get('amount',0) >=xg_amount:
                        L['error'] = 3 #总限量
                        L['msg'] = '本次活动限兑'+str(xg_amount)+'次'
                        if Lx.get('uamount',0) !=0:
                            L['msg'] += ',您还有未结算单据'
                        return L

                if jf_price != 0:#有积分的活动
                    sql_vip = """
                        SELECT coalesce(jfnum,0) jfnum FROM hd_vip_info hvi
                        INNER JOIN users us ON hvi.vipcode = us.vip
                        WHERE us.usr_id = %s
                    """%(self.usr_id)
                    L1 = self.db.fetch(sql_vip) #VIP积分
                    sql_dvip = """
                        SELECT coalesce(SUM(coalesce(nd.jfprice,0)),0) jfprice FROM
                        neworders_detail nd
                        INNER JOIN neworders n ON nd.code = n.code
                        WHERE n.cid =%s AND coalesce(cstatus,0) IN (0,1)
                    """%self.usr_id
                    L2 = self.db.fetch(sql_dvip) #VIP 冻结积分
                    if float(L1.get('jfnum',0)) < (float(jf_price)+float(L2.get('jfprice',0))):
                        L['error'] = 1 #积分不足
                        L['msg'] = '积分不足'
                        if L2.get('jf_price',0) >0:
                            L['msg'] += ',您还有未结算单据'
                        return L
            except Exception as ex:
                L['error'] = 2
                L['msg'] = '操作异常' #str(ex)
        else:
            L['error'] = 2
            L['msg'] = '操作异常'
        return L

    def gettclist(self,pk):
        L=[]
        if pk!='':
            sql ="""
                SELECT  h.item_id,
                h.tm,
                h.cname,
                coalesce(mt.txt1,'') dw,
                hd.amount,
                hd.bj,   -- 零售价
                hd.vip_bj,
                h.pic
            FROM hd_item_db hd
            inner join hd_item_info h ON hd.item_id = h.item_id
            LEFT JOIN mtc_t AS mt ON mt.type = 'DW' AND mt.id = h.unit
            WHERE  hd.sitem_id = %s
            """%pk
            L,t = self.db.fetchall(sql)
        return L

    def get_order_status(self,pk):
        #删除 未支付，未完成订单,用户自主取消
        R = 0 #不可删除
        sql = """
            select top 1 1 from orders where code = '%s' and zfstatus = 0 and cstatus in (0,1) and cid=%s
        """%(pk,self.usr_id)
        L,iN = self.db.select(sql)
        if iN>0:
            R = 1
        return R

    def get_neworder_status(self,pk):
        #删除 未支付，未完成订单,用户自主取消
        R = 0 #不可删除
        sql = """
            select top 1 1 from neworders where code = '%s' and zfstatus = 0 and cstatus in (0,1) and cid=%s
        """%(pk,self.usr_id)
        L,iN = self.db.select(sql)
        if iN>0:
            R = 1
        return R

    def list_for_grid(self, List,iTotal_length, pageNo=1, select_size=10):

        if iTotal_length % select_size == 0:
            iTotal_Page = iTotal_length / select_size
        else:
            iTotal_Page = iTotal_length / select_size + 1

        start, end = (int(pageNo) - 1) * select_size, pageNo * select_size
        if end >= iTotal_length: end = iTotal_length
        if iTotal_length == 0 or start > iTotal_length or start < 0:
            return [], iTotal_length, iTotal_Page, pageNo, select_size
        return List[start:end], iTotal_length, iTotal_Page, pageNo, select_size

    def get_wecthpy(self):

        # sql = "select appid,secret from mall where usr_id=%s"
        # l, t = self.db.select(sql, self.subusr_id)
        # appid, secret = l[0]
        # if t == 0:
        #     return 0
        mall=self.oMALL.get(self.subusr_id)
        if mall=={}:
            return 0

        appid=mall['appid']
        secret =mall['secret']
        # client = WeChatClient(appid, secret)
        # wxa = WeChatWxa(client)
        # return wxa

    def update_my_coupons(self):
        pass

    def print_log(self,cname,errors):
        sql="insert into print_log(cname,errors,ctime)values(%s,%s,now())"
        self.db.query(sql,[cname,errors])
        return



    def Save_pic_table(self, f_ext, f_size, filename, url, ctype, timestamp, ctype_str='', other_id=0, goodsid=0):

        f_year = self.getToday(6)[:4]
        sql = """insert into images_api(usr_id,ctype,ctype_str,other_id,f_year,f_ext,f_size,cname,pic,cid,ctime,timestamp,goodsid)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,%s)"""
        L = [self.subusr_id, ctype or None, ctype_str, other_id or None, f_year, f_ext, f_size, filename, url,
             self.subusr_id, timestamp, goodsid or None]
        self.db.query(sql, L)

    def order_complete_send(self, wechat_user_id, form_id, order_num, orderid=''):  # 订单完成通知模板消息
        # 订单编号，提示
        wxa = self.get_wecthpy()
        if wxa == 0:
            return 1
        opid = self.oOPENID.get(int(wechat_user_id))
        if opid == '':
            return 1
        shop = self.oSHOP_T.get(self.subusr_id)
        if shop == {}:
            return 1
        url = None
        tid = shop.get('complete_id','')  # 'M1VCMVmg6_Rz5ZCxBZpZGYsojOIfOxJt80Lo83OSzW8'
        if tid == '':
            return 1
        complete_url = shop.get('complete_url', '')
        if complete_url != '':
            url = complete_url.format(orderid=orderid)
        data = {"keyword1": {
            "value": "%s" % order_num
        }, "keyword2": {
            "value": "您的订单已完成,感谢您的支持,欢迎再次光临。"
        }
        }
        try:
            a = wxa.send_template_message(opid, tid, data, form_id, page=url)
        except Exception as e:
            self.print_log('订单完成:%s' % tid, '%s' % e)
            a = 1

        return a

    def order_evaluation_send(self, wechat_user_id, form_id, order_num, orderid=''):  #订单评价通知模板消息
        #订单编号，提示
        wxa = self.get_wecthpy()
        if wxa == 0:
            return 1
        opid = self.oOPENID.get(int(wechat_user_id))
        if opid == '':
            return 1
        shop = self.oSHOP_T.get(self.subusr_id)
        if shop == {}:
            return 1
        url = None
        tid = shop.get('evaluate_id','')  # 'M1VCMVmg6_Rz5ZCxBZpZGYsojOIfOxJt80Lo83OSzW8'
        if tid == '':
            return 1
        evaluate_url = shop.get('evaluate_url', '')
        if evaluate_url != '':
            url = evaluate_url.format(orderid=orderid)
        data = {"keyword1": {
            "value": "%s" % order_num
        }, "keyword2": {
            "value": "期待您的评价，帮助我们提升服务品质。"
        }
        }
        try:
            a = wxa.send_template_message(opid, tid, data, form_id, page=url)
        except Exception as e:
            self.print_log('订单评价:%s' % tid, '%s' % e)
            a = 1

        return a

    def order_cancel_send(self, wechat_user_id, form_id, order_num, total='', ctime='', orderid=''):  # 订单取消通知模板消息
        #订单金额，取消原因，下单时间，订单编号，提示
        wxa=self.get_wecthpy()
        if wxa==0:
            return 1
        opid = self.oOPENID.get(int(wechat_user_id))

        if opid == '':
            return 1
        shop = self.oSHOP_T.get(self.subusr_id)

        if shop == {}:
            return 1
        url = None
        tid = shop.get('cancel_id','')#'M1VCMVmg6_Rz5ZCxBZpZGYsojOIfOxJt80Lo83OSzW8'

        if tid=='':
            return 1

        cancel_url = shop.get('cancel_url', '')
        if cancel_url != '':
            url = cancel_url.format(orderid=orderid)

        data = {"keyword1": {
            "value": "%s" % total
        }, "keyword2": {
            "value": "用户自己取消"
        }, "keyword3": {
            "value": "%s" % ctime
        }, "keyword4": {
            "value": "%s" % order_num
        }, "keyword5": {
            "value": "您的订单已取消，欢迎再次光临。"
        }
        }

        try:
            a = wxa.send_template_message(opid, tid, data, form_id, page=url)
        except Exception as e:
            self.print_log('订单取消:%s' % tid, '%s' % e)
            a = 1
        return a





