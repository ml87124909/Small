# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""api/home.py"""


from imp import reload
from config import DEBUG

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import hashlib,time,json,datetime,os,random,requests,traceback
from .pay import WeixinPay
from .helper import md5_constructor as md5
from .wxpay import WxPay, get_nonce_str, dict_to_xml, xml_to_dict
from werkzeug import secure_filename
if DEBUG == '1':
    import single.sapi.BASE_LOC
    reload(single.sapi.BASE_LOC)
from single.sapi.BASE_LOC import cBASE_LOC



class chome(cBASE_LOC):


    def goPartorder_create(self):
        """
        :return:
        参数名称	参数说明
        yunfei_price	订单运费金额
        goods_price	商品总价合计
        goods_number	商品数量
        vip_state	是否是会员
        vip_price	商品会员价总价合计
        vip_level	会员等级ID
        vip_level_name	会员等级名称
        """
        token = self.REQUEST.get('token','')
        name = self.RQ('name', '')
        phone = self.RQ('phone', '')
        goodsJsonStr = self.REQUEST.get('goodsJsonStr', '')
        kuaid = self.RQ('kuaid','')
        province =self.RQ('province','')
        city = self.RQ('city', '')
        district = self.RQ('district', '')
        address = self.RQ('address', '')
        code = self.RQ('code', '')
        coupon_id = self.RQ('coupon_id', '')
        remark = self.RQ('remark', '')
        calculate = self.RQ('calculate', '')
        balance = self.RQ('balance', '')
        mendian_id = self.RQ('mendian_id', '')
        ctype = self.RQ('ctype', '')#订单类型
        formId = self.RQ('formId', '')  # 用于推送模版消息用的formId
        ptkid = self.RQ('ptkid', '')  # 开团ID
        ptype = self.RQ('ptype', '')  # 拼团类型

        if token=='' or token=='None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if goodsJsonStr=='' or goodsJsonStr=='None' or goodsJsonStr == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goodsJsonStr')})

        if name=='' or name=='None' or name == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('name')})

        if phone=='' or phone=='None' or phone == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('phone')})


        if kuaid == '' or kuaid == 'None' or kuaid == 'undefined':
            kuaid =''

        if province == '' or province == 'None' or province == 'undefined':
            province=''

        if city == '' or city == 'None' or  city == 'undefined':
            city=''

        if district=='' or district=='None' or district == 'undefined':
            district=''

        if address == '' or address == 'None' or address== 'undefined':
            address=''

        if code == '' or code == 'None' or code == 'undefined':
            code=''

        if coupon_id == '' or coupon_id == 'None' or coupon_id== 'undefined' or coupon_id== 'null':
            coupon_id=''

        if remark == '' or remark == 'None' or remark == 'undefined':
            remark=''

        if balance == '' or balance == 'None' or balance == 'undefined' or balance== 'null':
            balance=0

        if mendian_id == '' or mendian_id == 'None' or mendian_id == 'undefined' or mendian_id== 'null':
            mendian_id=''

        if ctype == '' or ctype == 'None' or ctype == 'undefined' or ctype== 'null':
            ctype=''

        if formId == 'None' or formId == 'undefined' or formId== 'null':
            formId=''

        if ptkid == 'None' or ptkid == 'undefined' or ptkid == 'null':
            ptkid = ''

        if ptype == 'None' or ptype == 'undefined' or ptype == 'null':
            ptype =''

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        USER=self.oUSER.get(self.subusr_id, wechat_user_id)

        if USER=={}:
            return self.jsons({'code': 10000, 'msg': self.error_code[10000]})

        if str(ctype) == '2':
            if str(ptype) == '0':#开团

                sqlt = "select COALESCE(kt_type,0)  from  pt_conf where usr_id=%s and id=%s"
                lk, kt = self.db.select(sqlt, [self.subusr_id, ptkid])
                if kt == 0:
                    return self.jsons({'code': 301, 'msg': '拼团ID不正确'})

                sqlo = """select id  from  wechat_mall_order 
                            where usr_id=%s and wechat_user_id=%s and ptid=%s and COALESCE(status,0)=10"""
                llT, iiN = self.db.select(sqlo, [self.subusr_id, wechat_user_id, ptkid])
                if iiN > 0:
                    return self.jsons({'code': 307, 'msg': '已有未完成的拼团'})

                kt_type=lk[0][0]
                sqlk="select id  from  open_pt_detail where wechat_user_id=%s"
                kl,tk=self.db.select(sqlk,wechat_user_id)
                if tk>0 and str(kt_type)=='1':
                    return self.jsons({'code': 304, 'msg': '仅限新用户开团'})
                elif tk==0 and str(kt_type)=='2':
                    return self.jsons({'code': 305, 'msg': '仅限老用户开团'})

            else:#参团
                sqlo = """select COALESCE(status,0) from wechat_mall_order 
                    where usr_id=%s and wechat_user_id=%s and ptkid=%s and COALESCE(status,0) in (10,1) """
                llT,iiN=self.db.select(sqlo,[self.subusr_id,wechat_user_id,ptkid])
                if iiN>0:
                    return self.jsons({'code': 307, 'msg': '已有未完成的拼团1'})

                sqlt="select COALESCE(add_type,0),ptid,COALESCE(status,0)  from  open_pt where usr_id=%s and id=%s"
                lk,kt=self.db.select(sqlt,[self.subusr_id,ptkid])
                if kt==0:
                    return self.jsons({'code': 301, 'msg': '拼团ID不正确'})
                add_type,ptid,status=lk[0]
                if str(status)!='1':
                    return self.jsons({'code': 303, 'msg': '拼团已经结束'})

                sqlp="""select id  from  open_pt_detail 
                        where usr_id=%s and wechat_user_id=%s and ptid=%s and COALESCE(status,0)=1"""
                lp,tp=self.db.select(sqlp,[self.subusr_id,wechat_user_id,ptid])
                if tp>0:
                    return self.jsons({'code': 307, 'msg': '已有未完成的拼团2'})

                sqlkk="select id  from  open_pt_detail where usr_id=%s and wechat_user_id=%s"
                kl,tk=self.db.select(sqlkk,[self.subusr_id,wechat_user_id])
                if tk>0 and str(add_type)=='1':
                    return self.jsons({'code': 304, 'msg': '仅限新用户参团'})
                elif tk==0 and str(add_type)=='2':
                    return self.jsons({'code': 305, 'msg': '仅限老用户参团'})

        #查看店铺设置
        # uptype = ''
        # vip_state, vip_level, vip_level_name, vip_sale = 0,'0','无',1
        # l,t=self.db.select("select up_type,discount from member where usr_id=%s",self.subusr_id)
        # if t>=0:
        #     uptype=l[0]
        #     uptype.append(wechat_user_id)
        # if uptype!='':
        #     vip_state, vip_level, vip_level_name, vip_sale=self.get_vip_type(uptype)
        #print('vip_sale',vip_sale)
        # 处理商品json数据
        try:
            goods_json = json.loads(goodsJsonStr)
        except Exception as e:
            return self.jsons({'code': -1,'data':e, 'msg': '提交的商品数据转换有误'})

        vip_list, coupon, goods_price, logistics_price, total, goods_list, dR = self._handle_goods_json(goods_json,coupon_id,kuaid,wechat_user_id,ctype)

        if dR==1:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        elif dR==2:
            return self.jsons({'code': 700, 'msg': '订单中存在已下架的商品，请重新下单。'})
        elif dR==3:
            return self.jsons({'code': 700, 'msg': '订单中存在库存不足商品，请重新下单！'})
        elif dR==4:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('后台没有设置运费模板')})
        elif dR==5:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format(goods_json)})
        elif dR==6:
            return self.jsons({'code': 701, 'msg': self.error_code[701]})
        elif dR==7:
            return self.jsons({'code': 700, 'msg': '订单中存在商品超过限购买量!'})

        coupon_name, coupon_price = coupon
        vip_total, vip_price, vip_state, vip_level, vip_level_name, vip_sale = vip_list

        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode=str(time.time()).split('.')[-1]#[3:]
        if str(ctype)=='1':
            ctype_str = '购买会员'
            order_num = 'H' + danhao[2:] + romcode
        elif str(ctype) == '2':
            if ptkid == '' or ptype == '':
                return self.jsons({'code': 300, 'msg': self.error_code[300].format('ptkid or ptype')})
            ctype_str = '拼团订单'
            order_num = 'P' + danhao[2:] + romcode
        elif str(ctype) == '3':
            ctype_str = '砍价订单'
            order_num = 'K' + danhao[2:] + romcode
        else:
            ctype_str='普通订单'
            order_num='B'+danhao[2:]+romcode

        number_goods=sum(map(lambda r: r['amount'], goods_list))
        goods_ids=list(set(map(lambda r: r['goods_id'], goods_list)))
        new_total = total
        if vip_total > 0:
            new_total = vip_total
        if not calculate:
            new_money = round(new_total-float(balance), 2)
        else:
            new_money = round(new_total, 2)

        vip_small=round(goods_price - vip_price,2)
        datas = {'yunfei_price': logistics_price, 'goods_number': number_goods, 'goods_price': round(goods_price,2),
                 'total': total, 'vip_total': vip_total,'money':new_money
            , 'vip_state': vip_state, 'vip_price': vip_price, 'vip_level': vip_level, 'vip_sale': vip_sale
            , 'vip_level_name': vip_level_name,'vip_small':vip_small
                 }

        order_dict = {
            'wechat_user_id': wechat_user_id,
            #'cname':name,
            #'phone':phone,
            #'address':address,
            'code':code,
            'remark':remark,
            'number_goods': number_goods,
            'goods_price': goods_price,
            'logistics_price': logistics_price,
            'vip_sale':vip_sale,
            'vip_price':vip_price,
            'vip_total':vip_total,
            'vip_small':vip_small,
            'total': total,
            'new_total': new_total,
            'province': province,
            'city': city,
            'district': district,
            'cid':wechat_user_id,
            'order_num ':order_num,
            'status':'1',
            'status_str': '待支付',
            'usr_id':self.subusr_id,
            'ctype':ctype or None,
            'ctype_str': ctype_str,
            'balance':balance
        }

        if coupon_id!='' and coupon_id!='null' and coupon_price>0:
            order_dict['couponid']= coupon_id
            order_dict['coupon_price']= coupon_price
            order_dict['coupon_name'] = coupon_name
        if kuaid != '' and kuaid != 'null':
            kuaid_str=''
            if kuaid=='0':
                kuaid_str='快递配送'
            if kuaid == '1':
                kuaid_str = '上门自提'
                order_dict['mendian_id']=mendian_id
                upperCase = [
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I','J', 'K','L', 'M', 'N','O',
                    'P', 'Q', 'R', 'S', 'T', 'U', 'V','W', 'X', 'Y', 'Z',
                ]
                romcode = str(time.time()).split('.')[-1]
                nums = romcode[-6:]
                Dstr=random.sample(upperCase, 2)
                D_c = ''.join(Dstr)
                str_c=D_c+nums
                pick_number = str_c  # 上门自提提取码
                order_dict['pick_number'] = pick_number

            if kuaid == '2':
                kuaid_str = '无需配送'
            order_dict['kuaid'] = kuaid
            order_dict['kuaid_str'] = kuaid_str

        if str(ctype) == '2':
            order_dict['pt_type'] = ptype
            if ptype == '0':
                order_dict['ptid'] = ptkid
            else:
                order_dict['ptkid'] = ptkid

        if not calculate:
            if new_money<0:
                return self.jsons({'code': 405, 'msg': self.error_code[405]})
            if str(USER.get('status', '')) == '1':
                return self.jsons({'code': 701, 'msg': self.error_code[701]})

            now = datetime.datetime.now()
            ctime=now.strftime('%Y-%m-%d %H:%M:%S')
            order_dict['ctime'] = ctime
            sql="select COALESCE(close_time,0),COALESCE(close_time_pk,0) from shop_set where usr_id=%s"
            l,t=self.db.select(sql,self.subusr_id)
            if t>0:
                close_time,close_time_pk=l[0]
                if str(ctype) in ('2','3'):
                    new_close_time=close_time_pk
                else:
                    new_close_time=close_time
                delta = datetime.timedelta(minutes=int(new_close_time))
                n_days = now + delta
                data_close = n_days.strftime('%Y-%m-%d %H:%M:%S')
                order_dict['data_close'] = data_close

            self.db.insert('wechat_mall_order',order_dict)

            order_id = self.db.fetchcolumn("select id from wechat_mall_order where order_num='%s'" % order_num)
            # 'cname':name,
            # 'phone':phone,
            # 'address':address,
            # sql = """update feedback  set cname=encrypt(%s,%s,'aes'),phone=encrypt(%s,%s,'aes'),
            #         address=encrypt(%s,%s,'aes')  where  and id =%s"""
            sql = """update wechat_mall_order  set cname=encrypt(%s,%s,'aes'),phone=encrypt(%s,%s,'aes'),
                                address=encrypt(%s,%s,'aes')  where id =%s"""
            parm=[name, self.md5code,phone, self.md5code,address, self.md5code, order_id]
            self.db.query(sql,parm )

            self.write_order_log(order_id,'创建订单',edit_remark='订单号:%s'%order_num)
            if formId!='':
                fidd={'formid':formId,'usr_id':self.subusr_id,'order_id':order_id,
                      'wechat_user_id':wechat_user_id,'ctime':self.getToday(9)}
                self.db.insert('wechat_formid',fidd)
            #更新优惠券状态
            if  order_dict.get('coupon_price','')!='':
                sql="""
                update  my_coupons set state=1,state_str='已使用' where id=%s and wechat_user_id=%s and usr_id=%s
                """
                self.db.query(sql,[coupon_id,wechat_user_id,self.subusr_id])
                self.write_order_log(order_id, '更新优惠券状态', '使用优惠券id:%s,优惠券名称:%s,优惠券价格:%s'%(coupon_id,coupon_name,coupon_price), '订单号:%s'%order_num)

            for good in goods_list:
                goodsid=good['goods_id']
                amountc=good['amount']
                scname=good['property_str']
                good_dict = {
                    'order_id':order_id,
                    'order_num ': order_num,
                    'good_id':goodsid,#good['goods_id'],
                    'good_name':good['name'],
                    'price':good['price'],
                    'pic':good['pic'],
                    'amount':good['amount'],
                    'property_str':good['property_str'],
                    'total':good['total'],
                    'cid':wechat_user_id,
                    'ctime':self.getToday(9),
                    'usr_id':self.subusr_id,
                    'status':1,
                    'status_str': '待支付',
                    'inviter_user':good['inviter_user'],
                }

                self.db.insert('wechat_mall_order_detail', good_dict)
                #更新单个库存
                sql="""update spec_child_price set store_c=store_c-%s 
                        where usr_id=%s and sc_name=%s and goods_id=%s"""
                self.db.query(sql,[amountc,self.subusr_id,scname,goodsid])
                try:
                    self.oGOODS_D.updateo(self.subusr_id, goodsid)
                    self.oGOODS.updateo(self.subusr_id, goodsid)
                    self.oGOODS_N.update(self.subusr_id, goodsid)
                    self.oGOODS_SELL.update(self.subusr_id)
                except Exception as e:
                    self.print_log('创建订单更新商品数据报错1','%s'%e)
                self.db.query("update goods_info set orders=COALESCE(orders,0)+%s where id=%s", [amountc, goodsid])



            goods_ids_str=[]
            for ds in goods_ids:
                goods_ids_str.append(str(ds))
            ids_str=','.join(goods_ids_str)
            self.write_order_log(order_id, '写入订单商品数据','商品id:%s,' % ids_str,'订单号:%s' % order_num)

            datas['order_number']=order_num

            if float(balance)>0:#使用余额支付：

                #检查用户帐户余额
                sql="select balance from wechat_mall_user where usr_id=%s and id=%s"
                yue=self.db.fetchcolumn(sql,[self.subusr_id,wechat_user_id])
                if yue>=float(balance):#足够支付
                    #修改用户余额，写入冻结金额
                    sqly="update wechat_mall_user set balance=balance-%s where usr_id=%s and id=%s"
                    self.db.query(sqly,[balance,self.subusr_id,wechat_user_id])
                    self.write_order_log(order_id, '采用用户余额支付', '需要支付的金额为:%s,用户当前余额为:%s' %(balance,yue),
                                         '订单号:%s' % order_num)
                    sql = """
                    insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                    values(%s,%s,3,'消费',%s,3,'抵扣',%s,'提交订单抵扣',%s,now())
                            """
                    self.db.query(sql, [self.subusr_id, wechat_user_id, balance, order_num, self.subusr_id])
                    if new_total == float(balance):#使用余额支付全部
                        # 修改订单状态
                        sqlo="""
                            update wechat_mall_order set pay_status=2,pay_status_str='余额支付',pay_ctime=now()
                                ,status=2,status_str='待发货' where usr_id=%s and id=%s and wechat_user_id=%s
                        """
                        self.db.query(sqlo,[self.subusr_id,order_id,wechat_user_id])
                        #修改订单商品明细表状态

                        sqld = """
                        update wechat_mall_order_detail set status=2,status_str='待发货' where usr_id=%s and order_id=%s 
                                """
                        self.db.query(sqld, [self.subusr_id, order_id])
                        self.write_order_log(order_id, '采用用户余额全支付', '更新订单状态为待发货,支付方式为余额支付,支付时间',
                                         '订单号:%s' % order_num)

                        if kuaid == '1':#自提单
                            # 修改订单状态
                            sqlo = """
                                update wechat_mall_order set pay_status=2,pay_status_str='余额支付',pay_ctime=now()
                                    ,status=4,status_str='待自提' where usr_id=%s and id=%s and wechat_user_id=%s
                                """
                            self.db.query(sqlo, [self.subusr_id, order_id, wechat_user_id])
                            # 修改订单商品明细表状态
                            sqld = """
                                update wechat_mall_order_detail set status=4,status_str='待自提' where usr_id=%s and order_id=%s 
                                        """
                            self.db.query(sqld, [self.subusr_id, order_id])
                            self.write_order_log(order_id, '采用用户余额全支付自提单', '更新订单状态为待自提',
                                                 '订单号:%s' % order_num)
                        if kuaid == '2':#无须配送
                            # 修改订单状态
                            sqlo = """
                                update wechat_mall_order set pay_status=2,pay_status_str='余额支付',pay_ctime=now()
                                    ,status=6,status_str='待评价' where usr_id=%s and id=%s and wechat_user_id=%s
                                """
                            self.db.query(sqlo, [self.subusr_id, order_id, wechat_user_id])
                            # 修改订单商品明细表状态
                            sqld = """
                                update wechat_mall_order_detail set status=6,status_str='待评价' where usr_id=%s and order_id=%s 
                                        """
                            self.db.query(sqld, [self.subusr_id, order_id])
                            self.write_order_log(order_id, '采用用户余额全支付非快递配送', '更新订单状态为待评价',
                                                 '订单号:%s' % order_num)
                        #更新商品库存
                        sql="select good_id,amount,inviter_user,good_name,cid from wechat_mall_order_detail  where usr_id=%s and order_id=%s "
                        lll,t=self.db.select(sql,[self.subusr_id, order_id])
                        for ii in lll:
                            good_id, amountm,user,good_name,cid=ii
                            try:
                                self.oGOODS_D.updates(self.subusr_id,good_id,amountm)
                                self.oGOODS.updates(self.subusr_id, good_id, amountm)
                                self.oGOODS_N.update(self.subusr_id, good_id)
                            except Exception as e:
                                self.print_log('创建订单更新商品数据报错2', '%s' % e)
                            if str(user)!='0' and str(user)!=str(cid):#下单返现
                                good_D = self.oGOODS_D.get(self.subusr_id, int(good_id))
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
                                            self.db.query(sql, [float(share_number), self.subusr_id, user])
                                            sqlg = "insert into user_log(usr_id,wechat_user_id,cname,memo,ctime)values(%s,%s,'balance',%s,now())"
                                            self.db.query(sqlg, [self.subusr_id, user, '%s下单返现给%s' % (cid, user)])
                                            sql = """
                                            insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,
                                            typeid,typeid_str,remark,goods_id,goods_name,cid,ctime)
                                            values(%s,%s,2,'返现',%s,1,'分享返现','单次分享返现返',%s,%s,%s,now())
                                            """
                                            parm = [self.subusr_id, user, float(share_number), good_id, gname,cid]
                                            self.db.query(sql, parm)
                                            sql = """
                                                insert into profit_record(usr_id,wechat_user_id,ctype,ctype_str,
                                                share_type,
                                                share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                                values(%s,%s,0,'现金收益',3,'好友下单返现',%s,%s,%s,%s,now())
                                                """
                                            parm = [self.subusr_id, user, float(share_number), good_id, gname,cid]
                                            self.db.query(sql, parm)

                                        elif str(share_type) == '2' and share_number != '':  # 返积分

                                            sql = """
                                            update wechat_mall_user set score=coalesce(score,0)+%s 
                                            where usr_id=%s and id=%s 
                                                    """
                                            self.db.query(sql, [float(share_number), self.subusr_id, user])
                                            sqlg = "insert into user_log(usr_id,wechat_user_id,cname,memo,ctime)values(%s,%s,'score',%s,now())"
                                            self.db.query(sqlg, [self.subusr_id, user, '%s下单返积分给%s' % (cid, user)])
                                            sql = """
                                                    insert into integral_log(usr_id,wechat_user_id,type,typestr,in_out,
                                                    inoutstr,amount,cid,ctime)values(%s,%s,7,'分享返',0,'收入',%s,%s,now())
                                                    """
                                            parm = [self.subusr_id, good_id, float(share_number), cid]
                                            self.db.query(sql, parm)
                                            sql = """insert into profit_record(usr_id,wechat_user_id,ctype,
                                            ctype_str,share_type,
                                                share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                                values(%s,%s,1,'积分收益',4,'好友下单返积分',%s,%s,%s,%s,now())
                                                            """
                                            parm = [self.subusr_id, user, float(share_number), good_id, gname,cid]
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
                                            parm = [self.subusr_id, ticket_id]
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
                                                        'usr_id': self.subusr_id,
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
                                                        'cid': self.subusr_id,
                                                        'ctime': self.getToday(9),
                                                        'good_id': good_id,
                                                        're_status': 1

                                                    }

                                                    self.db.insert('my_coupons', data)
                                                    sql="""update coupons set remain_total=COALESCE(remain_total,0)+1 
                                                    where id=%s"""
                                                    self.db.query(sql,ticket_id)
                                                    sql = """insert into profit_record(usr_id,wechat_user_id,ctype,
                                                    ctype_str,share_type,
                                                    share_type_str,change_money,goods_id,goods_name,cid,ctime,ticket_id)
                                                    values(%s,%s,2,'优惠券收益',5,'好友下单返优惠券',%s,%s,%s,%s,now(),%s)
                                                        """
                                                    parm = [self.subusr_id, user, change_money, good_id, gname, cid,ticket_id]
                                                    self.db.query(sql, parm)
                                        self.oUSER.update(self.subusr_id, user)
                        self.oUSER.update(self.subusr_id, wechat_user_id)

                else:
                    sqlo = """
                        update wechat_mall_order set balance=0 where usr_id=%s and id=%s and wechat_user_id=%s
                         """
                    self.db.query(sqlo, [self.subusr_id, order_id, wechat_user_id])


                self.oUSER.update(self.subusr_id,wechat_user_id)
            #self.oORDER_D.update(self.subusr_id,wechat_user_id,order_id)


        return self.jsons({'code': 0,'data':datas, 'msg':'success'})

    def _handle_goods_json(self, goods_json, couponid, kuaid, wechat_user_id, ctype):
        """
        :return:goods_price, logistics_price, total, goods_list,dR (dR是返回标识)
        """
        goods_price,amounts, logistics_price,dR = 0.0, 0,0.0,0
        goods_list = []
        good_ids=[]
        for each_goods in goods_json:
            if each_goods['goods_id']=='undefined':
                return 0,0,0, 0, 0, 0,5
            good_id=each_goods['goods_id']#商品id
            if str(ctype) == '1':  # 购买会员订单

                vip_list = [0.0, 0.0, 0, '0', '无', 1]
                coupon_price=0.0
                coupon_name=''
                coupon = [coupon_name, coupon_price]
                sql = "select up_type,vip_price from shop_set where usr_id=%s"
                up, vp = self.db.select(sql, self.subusr_id)
                if vp == 0:
                    dR=2
                    total = goods_price + logistics_price - coupon_price
                    return vip_list, coupon, goods_price, logistics_price, total, goods_list, dR

                up_type, vip_price=up[0]
                if str(up_type)=='2':
                    dR = 6
                    total = goods_price + logistics_price - coupon_price
                    return vip_list, coupon, goods_price, logistics_price, total, goods_list, dR

                goods_price+=vip_price
                total = goods_price + logistics_price - coupon_price

                return vip_list,coupon,goods_price, logistics_price, total, goods_list,dR


            good_ids.append(int(good_id))
            sql="select status,COALESCE(limited,0) from goods_info where id=%s"
            l,t=self.db.select(sql,good_id)
            if t ==0:
                dR=1
                return 0,0,0, 0, 0, 0, dR
            if str(l[0][0])=='1':
                dR = 2
                return 0,0,0, 0, 0, 0, dR
            sqlg = "select cname,pic,minprice,originalprice,COALESCE(stores,0)stores,COALESCE(weight,0)weight,pt_price from goods_info where id=%s"
            good_dict=self.db.fetch(sqlg,good_id)
            amount = int(each_goods['buy_number'])  # 购买数量
            limited=int(l[0][1])
            if limited>0:
                if amount>limited:
                    return 0, 0, 0, 0, 0, 0, 7

            amounts+=amount
            property_child_ids = each_goods.get('goods_childs','')#商品规格
            try:
                inviter_user=int(each_goods['inviter_user'])
            except:
                inviter_user=0
            # userid=0
            # if inviter_user!=0:
            #     userid=self.oUSER.get(self.subusr_id,inviter_user)

            each_goods_price, each_goods_total, property_str,dr = self._count_goods_price(
                good_dict, amount, property_child_ids, good_id, ctype
            )

            if dr == 2:
                return 0, 0, 0, 0, 0, 0, dr
            if dr==3:
                return 0, 0, 0, 0, 0, 0, dr

            goods_list.append({
                'goods_id': good_id,
                'name': good_dict['cname'],
                'pic': good_dict['pic'],
                'property_str': property_str,
                'price': each_goods_price,
                'amount': amount,
                'total': each_goods_total,
                'original_price':good_dict['originalprice'],
                'weight':good_dict['weight'],
                'inviter_user':inviter_user
            })

            goods_price += float(each_goods_total)
        each_logistics_price, rd = self._count_logistics_price(goods_list, amounts, kuaid,goods_price)
        if rd == 4:
            return 0, 0, 0, 0, 0, 0, rd
        logistics_price += each_logistics_price
        vip_state, vip_level, vip_level_name, vip_sale = self.get_vip_type(wechat_user_id)

        coupon_price = 0
        coupon_name=''

        if couponid != '' and couponid!='null':
            sqlc="""select cname,apply_ext_money,apply_ext_num,to_char(datestart,'YYYY-MM-DD'),to_char(date_end,'YYYY-MM-DD'),
                    COALESCE(apply_id,0),goods_id , COALESCE(use_time,0),validday,
                    date_part('day', to_char(now(),'YYYY-MM-DD')::timestamp - to_char(ctime,'YYYY-MM-DD')::timestamp)
                from my_coupons where id=%s and wechat_user_id=%s and usr_id=%s"""
            l,t=self.db.select(sqlc,[couponid,wechat_user_id,self.subusr_id])
            #l, t = self.db.select(sqlc, [couponid, 1,1])
            if t>0:

                coupon_name,apply_ext_money, apply_ext_num, datestart,dateend,apply_id, apply_goods_id, use_time, validday,yday=l[0]
                if goods_price>=float(apply_ext_money):

                    if self.getToday(6)<= dateend:

                        if str(apply_id)=='0':#满减

                            if (str(use_time)=='0' and self.getToday(6)>= datestart) or (str(use_time)=='1' and int(validday)>int(yday)):
                                if apply_goods_id=='' or apply_goods_id=='0':
                                    coupon_price += apply_ext_num
                                else:
                                    apply_goods=[]
                                    apply_goods_id=apply_goods_id.split(',')
                                    for i in apply_goods_id:
                                        apply_goods.append(int(i))
                                    if list(set(good_ids).intersection(set(apply_goods)))!=[]:
                                        coupon_price += apply_ext_num

                            # elif str(use_time)=='1' and int(validday)>int(yday):
                            #     if apply_goods_id=='':
                            #         coupon_price += apply_ext_num
                            #     else:
                            #         apply_goods=[]
                            #         apply_goods_id=apply_goods_id.split(',')
                            #         for i in apply_goods_id:
                            #             apply_goods.append(int(i))
                            #         if list(set(good_ids).intersection(set(apply_goods)))!=[]:
                            #             coupon_price += apply_ext_num
                        else:#折扣

                            if (str(use_time) == '0' and self.getToday(6) >= datestart) or (str(use_time) == '1' and int(validday) > int(yday)):
                                if apply_goods_id=='':
                                    coupon_price += round(goods_price*(1-apply_ext_num/100),2)
                                else:
                                    apply_goods=[]
                                    apply_goods_id=apply_goods_id.split(',')
                                    for i in apply_goods_id:
                                        apply_goods.append(int(i))
                                    if list(set(good_ids).intersection(set(apply_goods)))!=[]:
                                        coupon_price += round(goods_price*(1-apply_ext_num/100),2)

                            # elif str(use_time) == '1' and int(validday) > int(yday):
                            #     pass
        #print(coupon_price,'coupon_price')
        vip_price=0
        vip_total=0
        total = round(goods_price + logistics_price - coupon_price, 2)
        if vip_state==1:
            #vip_p=goods_price*vip_sale - coupon_price
            #vip_price='%.2f' %a#round(total*vip_sale,2)
            vip_price =round((goods_price- coupon_price)*vip_sale,2)
            #vip_total = round((goods_price - coupon_price) * vip_sale + logistics_price, 2)
            vip_total = round(vip_price + logistics_price, 2)

        coupon=[coupon_name,coupon_price]
        #[vip_state, vip_level, vip_level_name, vip_sale]
        vip_list = [vip_total,vip_price,vip_state, vip_level, vip_level_name, vip_sale]
        return vip_list,coupon,goods_price, logistics_price, total, goods_list,dR

    def _count_goods_price(self, goods, amount, property_child_ids, good_id, ctype):
        """
        计算商品价格
        :param goods: model('wechat_mall.goods')
        :param amount: int
        :param property_child_ids: string
        :return: price, total, property_str, dR(返回标识)
        """
        property_str,dR = '',0

        if property_child_ids!='' and property_child_ids!='null':

            sql="""
            select sc_name,newprice,store_c,ptprice from spec_child_price 
            where usr_id=%s and goods_id=%s and sc_id=%s
            """
            l,t=self.db.select(sql,[self.subusr_id,good_id,property_child_ids[:-1]])
            if t==0:
                return 0,0,'',2
            property_str, miprice, store, ptprice = l[0]
            if str(ctype) == '2':
                price = ptprice
            else:
                price = miprice
            total = price * amount
            stores = store - amount
            if stores < 0:
                dR=3

            if stores == 0:
                # todo 发送库存空邮件
                pass

        else:
            if str(ctype) == '2':
                price = goods['pt_price']
            else:
                price = goods['minprice']
            total = price * amount
            stores = goods['stores'] - amount
            if stores < 0:
                dR=3


            if stores == 0:
                # todo 发送库存空邮件
                pass


        return price, total, property_str,dR

    def _count_logistics_price(self, goods, amount, kuaid,goods_price):
        """
        计算物流费用
        :param goods: model('wechat_mall.goods')
        :param amount: int
        :param transport_type: string
        :return: price,dR(返回标识)
        """
        k_price,dR=0.0,0
        if str(kuaid)!='' and kuaid!='null':
            sql = 'select use_money from shop_set where usr_id=%s'
            by=self.db.fetchcolumn(sql,self.subusr_id)
            if by!=0 and by!='':
                if goods_price>by:
                    return k_price,dR

            sql="""
            select is_mail,counts,piece,only_money,add_piece,add_money 
            from logistics_way where status=1 and c_id=%s and usr_id=%s
            """
            l,t=self.db.select(sql,[kuaid,self.subusr_id])

            if t==0:
                return 0, 4
            is_mail,counts, piece, only_money, add_piece, add_money=l[0]
            if str(is_mail)=='1':
                return k_price, dR
            if str(counts)=='0':#按件
                a=amount-piece

                if a>0:
                    b=a//add_piece
                    k_price=only_money+add_money*b

                    return k_price, dR

                return only_money,dR
            else:#按重量
                weights=0
                for d in goods:
                    weights+=d['weight']*d['amount']
                a=weights-piece
                if a>0:
                    b=a//add_piece
                    if a%add_piece>0:
                        b+=1
                    k_price=only_money+add_money*b

                    return k_price, dR

                return only_money, dR

        return k_price, dR

    def get_vip_type(self,wechat_user_id):

        l,t=self.db.select("select up_type,discount from shop_set where usr_id=%s",self.subusr_id)
        if t==0:
            return 0,'0','无',1

        ctype,sale=l[0]

        sql="""
            select coalesce(hy_flag,0),coalesce(usr_level,0),
            case when to_char(hy_ctime,'YYYY-MM-DD HH24:MI')<to_char(now(),'YYYY-MM-DD HH24:MI') and to_char(hy_etime,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') then 1 else 0 end
            from wechat_mall_user where id=%s
        """
        l,t=self.db.select(sql,wechat_user_id)
        if t==0:
            raise 0
        hy_flag,usr_level,hyt,=l[0]
        if str(ctype)=='1' and str(hy_flag)=='1':

           return 1,'0','会员',sale/100

        elif str(ctype)=='2' and str(usr_level)!='0':
            sql="select id,cname,level_discount from hy_up_level where usr_id=%s and id=%s"
            lT,iN=self.db.select(sql,[self.subusr_id,usr_level])
            if iN>0:
                vip_level,vip_level_name,vip_sale=lT[0]
                return 1,vip_level,vip_level_name,vip_sale/100
        return 0,'0','无',1#vip_state, vip_level, vip_level_name, vip_sale


    def goPartorder_paypal(self):

        token = self.REQUEST.get('token', '')
        number=self.RQ('number','')

        if token == '' or token == 'None'  or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if number == '' or number == 'None'  or number == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('number')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})

        wechat_user_id = dR['wechat_user_id']
        sql="""select w.id,w.balance,w.cname as receiver,w.status,
                    case when w.status in (1,10,15) then (w.new_total-w.balance) else 0 end money,
                    to_char(w.data_close,'YYYY-MM-DD HH24:MI')data_close,
                    u.cname as userNmae,u.avatar_url as userAvatar,w.status_str as state
                from wechat_mall_order w
                left join wechat_mall_user u on u.id=w.wechat_user_id
                where w.usr_id=%s and w.order_num=%s"""
        l,t=self.db.fetchall(sql,[self.subusr_id,number])
        if t==0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        for i in l:
            data_close=i.get('data_close','')
            status=i.get('status', '')
            receiver=i.get('receiver','')
            money=i.get('money', '')
            balance=i.get('balance','')
            id = i.get('id', '')
            if money>0:
                i['money'] =  round(money, 2)
            if data_close!='' and self.getToday(8)>data_close and str(status)=='1':
                self.db.query("update wechat_mall_order set status=-1,status_str='已取消' where order_num=%s ",number)
                self.db.query("update wechat_mall_order_detail set status=-1,status_str='已取消' where order_num=%s", number)
                i['state'] = '已取消'
                #self.oORDER_D.update(self.subusr_id, wechat_user_id, id)
                if balance>0:
                    sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                    self.db.query(sql, [balance, self.subusr_id, wechat_user_id])
                    self.oUSER.update(self.subusr_id, wechat_user_id)

            if receiver!='':
                if len(receiver)==2:
                    receiver=receiver[0]+'*'
                    i['receiver']=receiver
                elif len(receiver)==3:
                    receiver = receiver[0] + '*'+receiver[2]
                    i['receiver'] = receiver
                elif len(receiver) == 4:
                    receiver = receiver[0] + '*'+'*' + receiver[3]
                    i['receiver'] = receiver
                elif len(receiver) == 5:
                    receiver = receiver[0] + '*' + '*'+ '*' + receiver[4]
                    i['receiver'] = receiver
                elif len(receiver) == 6:
                    receiver = receiver[0] + '*'+'*' + '*'+ '*' + receiver[5]
                    i['receiver'] = receiver
                else:
                    pass

            sql="""select good_id as id,good_name as name,property_str as spec,pic,amount as number,
            COALESCE(price,0.0) as mini_price,COALESCE(original_price,0.0)original_price  
            from wechat_mall_order_detail where usr_id =%s and order_num=%s """
            lT,iN=self.db.fetchall(sql,[self.subusr_id,number])
            if iN>0:
                i['orderGoods']=lT

        return self.jsons({'code': 0,'data':l[0], 'msg': self.error_code['ok']})

    def goPartorder_list(self):

        token = self.REQUEST.get('token', '')
        status=self.REQUEST.get('status','')
        ctype = self.RQ('ctype', '')
        page = self.RQ('page','')
        pageSize=self.RQ('pageSize','')


        if token == '' or token == 'None'  or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if status == '' or status == 'None' or status == 'undefined' or status == 'null':
            status = '0'
        if ctype == '' or ctype == 'None' or ctype == 'undefined' or ctype == 'null':
            ctype = ''
        if page == '' or page == 'None' or page == 'undefined' or page == 'null':
            page = 1
        page=int(page)
        if pageSize == '' or pageSize == 'None' or pageSize == 'undefined' or pageSize == 'null':
            pageSize = 100
        pageSize=int(pageSize)

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})

        wechat_user_id = dR['wechat_user_id']

        sql="""select id,order_num as number,COALESCE(status,0)status,status_str as sname,ctype,
                to_char(ctime,'YYYY-MM-DD HH24:MI')data_add,COALESCE(new_total,0.0) as real_money
                ,to_char(data_close,'YYYY-MM-DD HH24:MI')data_close,pick_number,
                    case when COALESCE(check_id,0)=0 then '未核验' else '已核验' end pick_status,kuaid,
                    to_char(shipper_time,'YYYY-MM-DD HH24:MI')shipper_time,ptkid
                from wechat_mall_order 
                where usr_id=%s and wechat_user_id=%s and COALESCE(del_flag,0)=0 and COALESCE(ctype,0)!=6 """
        parm=[self.subusr_id,wechat_user_id]
        if ctype!='':
            sql+=" and ctype=%s "
            parm.append(ctype)
        if status!='0':
            sql+=" and status in (%s) "%status

        sql+=" order by id desc "

        l,n =self.db.fetchall(sql,parm)

        if n==0:
            return self.jsons({'code': 404, 'msg':self.error_code[404]})
        for i in l:
            kuaid=i.get('kuaid','')
            if str(kuaid)==0:
                i.pop('pick_number')
                i.pop('pick_status')
            i.pop('kuaid')
            data_close = i.get('data_close', '')
            shipper_time = i.get('shipper_time', '')
            id = i.get('id')
            status = i.get('status', '')
            if data_close!='' and self.getToday(8)>data_close and str(status)=='1':
                self.db.query("update wechat_mall_order set status=-1,status_str='已取消' where id=%s",id)
                self.db.query("update wechat_mall_order_detail set status=-1,status_str='已取消' where order_id=%s",id)
                i['status']=-1
                i['sname'] = '已取消'
                #self.oORDER_D.update(self.subusr_id,wechat_user_id,id)
            if str(status) == '5' and shipper_time!='':
                ORDER=self.oORDER_SET.get(self.subusr_id)

                if ORDER=={}:
                    pass
                else:
                    take_day=ORDER.get('take_day')
                    now = datetime.datetime.strptime(shipper_time, "%Y-%m-%d %H:%M")
                    delta = datetime.timedelta(days=int(take_day))
                    n_days = now + delta
                    etime = n_days.strftime('%Y-%m-%d %H:%M:%S')
                    if self.getToday(9)>etime:
                        self.db.query("update wechat_mall_order set status=6,status_str='待评价' where id=%s",
                                      id)
                        self.db.query(
                            "update wechat_mall_order_detail set status=6,status_str='待评价' where order_id=%s",
                            id)
                        i['status'] = 6
                        i['sname'] = '待评价'
                        #self.oORDER_D.update(self.subusr_id, wechat_user_id, id)
            elif str(status) in ('99','98','97','89','88','87'):
                sql="""select to_char(ctime,'YYYY-MM-DD HH24:MI')date,r_money as money,
                        case when refund_type=1 then '原路退回' else '退回余额' end as mode,not_memo as reason 
                        from refund_money where order_id=%s and usr_id=%s
                        """
                lT2,iN2=self.db.fetchall(sql,[id,self.subusr_id])
                if iN2>0:
                    i['service'] = lT2

            sql="""select good_id as id,good_name as name,property_str as spec,pic,amount as number,
            COALESCE(price,0.0) as mini_price,COALESCE(original_price,0.0)original_price  
            from wechat_mall_order_detail where usr_id =%s and order_id=%s """
            lT,iN=self.db.fetchall(sql,[self.subusr_id,id])
            if iN>0:
                i['order_goods']=lT
        List,iTotal_length,iTotal_Page, pageNo, select_size=self.list_for_grid(l, n, pageNo=page, select_size=pageSize)
        return self.jsons({'code': 0,'data':List, 'msg': self.error_code['ok']})

    def goPartget_wechat_paypal(self):
        token = self.REQUEST.get('token', '')
        money=self.REQUEST.get('money','')
        remark=self.REQUEST.get('remark','')
        payName=self.REQUEST.get('payName','')#: "在线支付",
        nextAction=self.REQUEST.get('nextAction','')


        if token=='' or token =='None'  or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if money=='' or money =='None'  or money == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('money')})
        if remark=='' or remark =='None'  or remark == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('remark')})
        if payName=='' or payName =='None'  or payName == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('payName')})
        if nextAction=='' or nextAction =='None'  or nextAction == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('nextAction')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        open_id = dR['open_id']

        try:
            nextaction = json.loads(nextAction)
            gid=int(nextaction['id'])
            ctype = int(nextaction['ctype'])
            payType = int(nextaction['ptype'])
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('nextAction')})

        mall = self.oMALL.get(self.subusr_id)

        if mall == {}:
            return self.jsons({'code': 404, 'msg': '请到店铺设置填写小程序设置'})
        app_id = mall['appid']
        secret = mall['secret']
        wechat_pay_id=mall['mchid']
        wechat_pay_secret=mall['mchkey']
        base_url = mall['base_url']
        if base_url=='':
            return self.jsons({'code': 404, 'msg': '请到店铺设置填写小程序设置的支付回调域名'})

        if ctype==6:
            if payType != 0:#微信全额支付
                return self.jsons({'code': 405, 'msg': self.error_code[405]})
            sql = """select order_num,truemoney 
                  from offline_pay where usr_id=%s  and id=%s and  coalesce(status,0)=0
                                """
            k, r = self.db.select(sql, [self.subusr_id, gid])
            if r == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            order_num, new_total = k[0]

            ############
            if float(money) != float(new_total):
                return self.jsons({'code': 405, 'msg': self.error_code[405]})

            payment = {
                'order_id': int(gid),
                'wechat_user_id': wechat_user_id,
                'price': float(money),
                'usr_id': self.subusr_id,
                'cid': wechat_user_id,
                'ctime': self.getToday(9),
                'payment_number': order_num,
                'status': 0,
                'status_str': '待支付',
                'ctype': ctype,
                'order_num': order_num
            }
            sql = """select coalesce(status,0) from  wechat_mall_payment where order_id=%s and payment_number=%s"""
            A, a = self.db.select(sql, [gid, order_num])
            if a > 0:
                if str(A[0][0]) == '1':
                    return self.jsons({'code': 10, 'msg': '已支付'})
                self.db.update('wechat_mall_payment', payment, 'order_id=%s' % gid)
            else:
                self.db.insert('wechat_mall_payment', payment)

            notify_url = base_url + '/pay/%s/notify' % self.subusr_id

            data = {
                'appid': app_id,
                'mch_id': wechat_pay_id,
                'nonce_str': get_nonce_str(),
                'body': order_num,  # 商品描述
                'out_trade_no': order_num,  # 商户订单号
                'total_fee': int(float(money) * 100),
                'notify_url': notify_url,
                'trade_type': 'JSAPI',
                'openid': open_id,
                'timeStamp': str(int(time.time())),

            }

            wxpay = WxPay(wechat_pay_secret, **data)
            pay_info, dR, prepay_id = wxpay.get_pay_info()

            if dR == 0:
                sql = "update wechat_mall_payment set prepay_id=%s where payment_number=%s"
                self.db.query(sql, [prepay_id, order_num])
                sql = """update wechat_mall_payment set timestamp_=%s,noncestr=%s,
                            package=%s,paysign=%s,total_fee=%s where payment_number=%s"""
                self.db.query(sql,
                              [pay_info['timeStamp'], pay_info['nonceStr'], pay_info['package'], pay_info['paySign'],
                               int(float(money) * 100), order_num])
                return self.jsons({'code': 0, 'data': pay_info, 'msg': self.error_code['ok']})
            elif dR == 2:
                sql = "select id from mall where appid=%s and mchid=%s and usr_id = %s"
                l, t = self.db.select(sql, [pay_info['appid'], pay_info['mch_id'], self.subusr_id])
                sql = "select id from offline_pay where order_num=%s and usr_id=%s"
                m, n = self.db.select(sql, [order_num, self.subusr_id])

                if pay_info.get('err_code') == 'ORDERPAID':  # 订单已支付
                    if t > 0 and n > 0:
                        try:
                            sql = """update offline_pay set 
                                status=1,uid=0,utime=now(),paytime=now() where usr_id=%s and order_num=%s"""
                            self.db.query(sql, [self.subusr_id, order_num])
                            sql = """update wechat_mall_payment set 
                                status=1,status_str='成功',uid=0,utime=now() where usr_id=%s and payment_number=%s"""
                            self.db.query(sql, [self.subusr_id, order_num])
                            return self.jsons({'code': 110, 'msg': pay_info.get('err_code_des')})
                        except:
                            pass
                return self.jsons({'code': 10, 'msg': pay_info.get('err_code_des')})
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        elif ctype==5:#充值
            if payType != 0:#微信全额支付
                return self.jsons({'code': 405, 'msg': self.error_code[405]})
            sql="select order_no,add_money from top_up where status=1 and usr_id=%s  and id=%s"
            k, r = self.db.select(sql, [self.subusr_id, gid])
            if r == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            order_num, add_money = k[0]

            if float(money) != add_money:
                return self.jsons({'code': 405, 'msg': self.error_code[405]})

            payment = {
                'order_id': int(gid),
                'wechat_user_id': wechat_user_id,
                'price': float(money),
                'usr_id': self.subusr_id,
                'cid': wechat_user_id,
                'ctime': self.getToday(9),
                'payment_number': order_num,
                'status': 0,
                'status_str': '待支付',
                'ctype': ctype,
                'order_num': order_num
            }
            sql = "select coalesce(status,0) from  wechat_mall_payment where order_id=%s and payment_number=%s"
            A, a = self.db.select(sql, [gid, order_num])
            if a > 0:
                if str(A[0][0]) == '1':
                    return self.jsons({'code': 10, 'msg': '已支付'})
                self.db.update('wechat_mall_payment', payment, 'order_id=%s' % gid)
            else:
                self.db.insert('wechat_mall_payment', payment)

            notify_url = base_url + '/pay/%s/notify' % self.subusr_id

            data = {
                'appid': app_id,
                'mch_id': wechat_pay_id,
                'nonce_str': get_nonce_str(),
                'body': order_num,  # 商品描述
                'out_trade_no': order_num,  # 商户订单号
                'total_fee': int(float(money) * 100),
                'notify_url': notify_url,
                'trade_type': 'JSAPI',
                'openid': open_id,
                'timeStamp': str(int(time.time())),

            }

            wxpay = WxPay(wechat_pay_secret, **data)
            pay_info, dR, prepay_id = wxpay.get_pay_info()
            if dR == 0:
                sql = "update wechat_mall_payment set prepay_id=%s where payment_number=%s"
                self.db.query(sql, [prepay_id, order_num])
                sql = """update wechat_mall_payment set timestamp_=%s,noncestr=%s,
                        package=%s,paysign=%s,total_fee=%s where payment_number=%s"""
                self.db.query(sql,
                              [pay_info['timeStamp'], pay_info['nonceStr'], pay_info['package'], pay_info['paySign'],
                               int(float(money) * 100), order_num])
                return self.jsons({'code': 0, 'data': pay_info, 'msg': self.error_code['ok']})
            elif dR == 2:
                sql = "select id from mall where appid=%s and mchid=%s and usr_id = %s"
                l, t = self.db.select(sql, [pay_info['appid'], pay_info['mch_id'], self.subusr_id])
                sql = "select id from top_up where order_no=%s and usr_id=%s"
                m, n = self.db.select(sql, [order_num, self.subusr_id])

                if pay_info.get('err_code') == 'ORDERPAID':  # 订单已支付
                    if t > 0 and n > 0:
                        try:
                            sql = "update top_up set status=5,status_str='已完成',uid=0,utime=now() where status=1 and order_no=%s"
                            self.db.query(sql, order_num)
                            sql = "update wechat_mall_payment set status=1,status_str='支付成功',uid=0,utime=now() where coalesce(status,0)=0 and payment_number=%s"
                            self.db.query(sql, order_num)
                            return self.jsons({'code': 110, 'msg': pay_info.get('err_code_des')})
                        except:
                            pass
                return self.jsons({'code': 10, 'msg': pay_info.get('err_code_des')})
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        elif ctype == 1:  # 会员
            if payType != 0:#微信支付
                return self.jsons({'code': 405, 'msg': self.error_code[405]})

            sql="select order_no,real_money from vip_member where status=1 and usr_id=%s  and id=%s"
            k, r = self.db.select(sql, [self.subusr_id, gid])
            if r == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            order_num, add_money = k[0]

            if float(money) != add_money:
                return self.jsons({'code': 405, 'msg': self.error_code[405]})

            payment = {
                'order_id': int(gid),
                'wechat_user_id': wechat_user_id,
                'price': float(money),
                'usr_id': self.subusr_id,
                'cid': wechat_user_id,
                'ctime': self.getToday(9),
                'payment_number': order_num,
                'status': 0,
                'status_str': '待支付',
                'ctype': ctype,
                'order_num': order_num
            }
            sql = "select coalesce(status,0) from  wechat_mall_payment where order_id=%s and payment_number=%s"
            A, a = self.db.select(sql, [gid, order_num])
            if a > 0:
                if str(A[0][0]) == '1':
                    return self.jsons({'code': 10, 'msg': '已支付'})
                self.db.update('wechat_mall_payment', payment, 'order_id=%s' % gid)
            else:
                self.db.insert('wechat_mall_payment', payment)

            notify_url = base_url + '/pay/%s/notify' % self.subusr_id

            data = {
                'appid': app_id,
                'mch_id': wechat_pay_id,
                'nonce_str': get_nonce_str(),
                'body': order_num,  # 商品描述
                'out_trade_no': order_num,  # 商户订单号
                'total_fee': int(float(money) * 100),
                'notify_url': notify_url,
                'trade_type': 'JSAPI',
                'openid': open_id,
                'timeStamp': str(int(time.time())),

            }

            wxpay = WxPay(wechat_pay_secret, **data)
            pay_info, dR, prepay_id = wxpay.get_pay_info()
            if dR == 0:
                sql = "update wechat_mall_payment set prepay_id=%s where payment_number=%s"
                self.db.query(sql, [prepay_id, order_num])
                sql = """update wechat_mall_payment set timestamp_=%s,noncestr=%s,
                        package=%s,paysign=%s,total_fee=%s where payment_number=%s"""
                self.db.query(sql,
                              [pay_info['timeStamp'], pay_info['nonceStr'], pay_info['package'], pay_info['paySign'],
                               int(float(money) * 100), order_num])
                return self.jsons({'code': 0, 'data': pay_info, 'msg': self.error_code['ok']})
            elif dR == 2:
                sql = "select id from mall where appid=%s and mchid=%s and usr_id = %s"
                l, t = self.db.select(sql, [pay_info['appid'], pay_info['mch_id'], self.subusr_id])
                sql = "select id from vip_member where order_no=%s and usr_id=%s"
                m, n = self.db.select(sql, [order_num, self.subusr_id])

                if pay_info.get('err_code') == 'ORDERPAID':  # 订单已支付
                    if t > 0 and n > 0:
                        try:
                            sql = """update vip_member set 
                                status=5,status_str='已完成',uid=0,utime=now() where status=1 and order_no=%s"""
                            self.db.query(sql, order_num)
                            sql = """update wechat_mall_payment set 
                            status=1,status_str='支付成功',uid=0,utime=now() 
                            where coalesce(status,0)=0 and payment_number=%s"""
                            self.db.query(sql, order_num)
                            return self.jsons({'code': 110, 'msg': pay_info.get('err_code_des')})
                        except:
                            pass
                return self.jsons({'code': 10, 'msg': pay_info.get('err_code_des')})
            return self.jsons({'code': 404, 'msg':self.error_code[404]})

        else:
            sql = """select order_num,to_char(data_close,'YYYY-MM-DD HH24:MI'),status,
                    new_total,kuaid,ptkid,ptid,pt_type,phone,coalesce(price_status,0),price_num
                    from wechat_mall_order where usr_id=%s  and id=%s and ctype=%s and coalesce(status,0)=1
                       
                    """
            k, r = self.db.select(sql, [self.subusr_id, gid, ctype])
            if r == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            order_num, data_close, status, new_total, kuaid, ptkid, ptid, pt_type, phone, price_status, price_num = k[0]
            if data_close != '' and self.getToday(8) > data_close and str(status) == '1':
                self.db.query("update wechat_mall_order set status=-1,status_str='已取消' where id=%s", gid)
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            # total=new_total- balance
            # if float(money)!=total:
            #     return self.jsons({'code': 405, 'msg': self.error_code[405]})
            ############
            if float(money) != new_total:
                return self.jsons({'code': 405, 'msg': self.error_code[405]})

            sql = "select balance from wechat_mall_user where usr_id=%s and id=%s"
            lL, tI = self.db.select(sql, [self.subusr_id, wechat_user_id])
            if tI == 0:
                return self.jsons({'code': 10000, 'msg': self.error_code[10000]})
            balance = lL[0][0]
            if payType == 1:  # 1:余额全额支付
                if balance < float(money):
                    return self.jsons({'code': 405, 'msg': self.error_code[405]})

                # 修改用户余额，写入冻结金额
                sqly = "update wechat_mall_user set balance=balance-%s where usr_id=%s and id=%s"
                self.db.query(sqly, [float(money), self.subusr_id, wechat_user_id])
                self.write_order_log(gid, '采用用户余额支付', '需要支付的金额为:%s,用户当前余额为:%s' % (money, balance),
                                     '订单号:%s' % order_num)
                sql = """
                insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                values(%s,%s,3,'消费',%s,3,'抵扣',%s,'提交订单抵扣',%s,now())
                        """
                self.db.query(sql, [self.subusr_id, wechat_user_id, float(money), order_num, self.subusr_id])
                # 修改订单状态
                sqlo = """
                    update wechat_mall_order set pay_status=2,pay_status_str='余额支付',pay_ctime=now(),balance=%s
                                 where usr_id=%s and id=%s and wechat_user_id=%s
                        """
                self.db.query(sqlo, [float(money), self.subusr_id, gid, wechat_user_id])

                if str(kuaid) == '0' and str(ctype) == '0':  # 自提单
                    # 修改订单状态
                    sqlo = """
                        update wechat_mall_order set status=2,status_str='待发货' 
                        where usr_id=%s and id=%s and wechat_user_id=%s
                    """
                    self.db.query(sqlo, [self.subusr_id, gid, wechat_user_id])
                    # 修改订单商品明细表状态

                    sqld = """
                    update wechat_mall_order_detail set status=2,status_str='待发货' where usr_id=%s and order_id=%s 
                            """
                    self.db.query(sqld, [self.subusr_id, gid])
                    self.write_order_log(gid, '采用用户余额全支付', '更新订单状态为待发货,支付方式为余额支付,支付时间',
                                         '订单号:%s' % order_num)

                elif str(kuaid) == '1' and str(ctype) == '0':  # 自提单
                    # 修改订单状态
                    sqlo = """
                        update wechat_mall_order set status=4,status_str='待自提' 
                        where usr_id=%s and id=%s and wechat_user_id=%s
                        """
                    self.db.query(sqlo, [self.subusr_id, gid, wechat_user_id])
                    # 修改订单商品明细表状态
                    sqld = """
                        update wechat_mall_order_detail set status=4,status_str='待自提' where usr_id=%s and order_id=%s 
                                """
                    self.db.query(sqld, [self.subusr_id, gid])
                    self.write_order_log(gid, '采用用户余额全支付自提单', '更新订单状态为待自提',
                                         '订单号:%s' % order_num)
                elif str(kuaid) == '2' and str(ctype) == '0':  # 无须配送
                    # 修改订单状态
                    sqlo = """
                        update wechat_mall_order set status=6,status_str='待评价' 
                        where usr_id=%s and id=%s and wechat_user_id=%s
                        """
                    self.db.query(sqlo, [self.subusr_id, gid, wechat_user_id])
                    # 修改订单商品明细表状态
                    sqld = """
                        update wechat_mall_order_detail set status=6,status_str='待评价' where usr_id=%s and order_id=%s 
                                """
                    self.db.query(sqld, [self.subusr_id, gid])
                    self.write_order_log(gid, '采用用户余额全支付非快递配送', '更新订单状态为待评价',
                                         '订单号:%s' % order_num)
                # 更新商品库存
                sql = "select good_id,amount,inviter_user,good_name,cid from wechat_mall_order_detail  where usr_id=%s and order_id=%s "
                lll, t = self.db.select(sql, [self.subusr_id, gid])
                for ii in lll:
                    good_id, amountm, user, good_name, cid = ii
                    try:
                        self.oGOODS_D.updates(self.subusr_id, good_id, amountm)
                        self.oGOODS.updates(self.subusr_id, good_id, amountm)
                        self.oGOODS_N.update(self.subusr_id, good_id)
                    except Exception as e:
                        self.print_log('创建订单更新商品数据报错2', '%s' % e)
                    if str(user) != '0' and str(user) != str(cid):  # 下单返现
                        good_D = self.oGOODS_D.get(self.subusr_id, int(good_id))
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
                                    self.db.query(sql, [float(share_number), self.subusr_id, user])
                                    sql = """
                                    insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,
                                    typeid,typeid_str,remark,goods_id,goods_name,cid,ctime)
                                    values(%s,%s,2,'返现',%s,1,'分享返现','单次分享返现返',%s,%s,%s,now())
                                    """
                                    parm = [self.subusr_id, user, float(share_number), good_id, gname, cid]
                                    self.db.query(sql, parm)
                                    sql = """
                                        insert into profit_record(usr_id,wechat_user_id,ctype,ctype_str,
                                        share_type,
                                        share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                        values(%s,%s,0,'现金收益',3,'好友下单返现',%s,%s,%s,%s,now())
                                        """
                                    parm = [self.subusr_id, user, float(share_number), good_id, gname, cid]
                                    self.db.query(sql, parm)

                                elif str(share_type) == '2' and share_number != '':  # 返积分

                                    sql = """
                                    update wechat_mall_user set score=coalesce(score,0)+%s 
                                    where usr_id=%s and id=%s 
                                            """
                                    self.db.query(sql, [float(share_number), self.subusr_id, user])
                                    sql = """
                                            insert into integral_log(usr_id,wechat_user_id,type,typestr,in_out,
                                            inoutstr,amount,cid,ctime)values(%s,%s,7,'分享返',0,'收入',%s,%s,now())
                                            """
                                    parm = [self.subusr_id, good_id, float(share_number), cid]
                                    self.db.query(sql, parm)
                                    sql = """insert into profit_record(usr_id,wechat_user_id,ctype,
                                    ctype_str,share_type,
                                        share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                        values(%s,%s,1,'积分收益',4,'好友下单返积分',%s,%s,%s,%s,now())
                                                    """
                                    parm = [self.subusr_id, user, float(share_number), good_id, gname, cid]
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
                                    parm = [self.subusr_id, ticket_id]
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
                                                'usr_id': self.subusr_id,
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
                                                'cid': self.subusr_id,
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
                                            parm = [self.subusr_id, user, change_money, good_id, gname, cid, ticket_id]
                                            self.db.query(sql, parm)

                if ctype == 2:  # 支付处理拼团数据

                    if str(pt_type) == '0':  # 开团
                        self.Pingtuan_add(wechat_user_id, ptid, gid, phone)

                    elif str(pt_type) == '1':  # 参团
                        self.Pingtuan_join(wechat_user_id, ptkid, gid, phone)

                self.oUSER.update(self.subusr_id, wechat_user_id)
                return self.jsons({'code': 1, 'msg': '不需要再进行支付'})

            elif payType == 2:  # 微信 + 余额支付
                if balance >= float(money):
                    return self.jsons({'code': 405, 'msg': self.error_code[405]})
                money = float(money) - balance
                # 修改用户余额，写入冻结金额
                sqly = "update wechat_mall_user set balance=balance-%s where usr_id=%s and id=%s"
                self.db.query(sqly, [balance, self.subusr_id, wechat_user_id])
                self.write_order_log(gid, '采用用户余额支付', '需要支付的金额为:%s,用户当前余额为:%s' % (money, balance),
                                     '订单号:%s' % order_num)
                sql = """
                    insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                    values(%s,%s,3,'消费',%s,3,'抵扣',%s,'提交订单抵扣',%s,now())
                    """
                self.db.query(sql, [self.subusr_id, wechat_user_id, balance, order_num, self.subusr_id])
            ############
            payment_number = order_num
            if str(price_status) == '1':
                payment_number = price_num

            payment = {
                'order_id': int(gid),
                'wechat_user_id': wechat_user_id,
                'price': float(money),
                'usr_id': self.subusr_id,
                'cid': wechat_user_id,
                'ctime': self.getToday(9),
                'payment_number': payment_number,
                'order_num': order_num,
                'status': 0,
                'status_str': '待支付',
                'ctype': ctype
            }
            sql = "select coalesce(status,0) from  wechat_mall_payment where order_id=%s and order_num=%s"
            A, a = self.db.select(sql, [gid, order_num])
            if a > 0:
                if str(A[0][0]) == '1':
                    self.jsons({'code': 10, 'msg': '已支付'})
                self.db.update('wechat_mall_payment', payment, 'order_id=%s' % gid)
            else:
                self.db.insert('wechat_mall_payment', payment)

            notify_url = base_url + '/pay/%s/notify' % self.subusr_id

            data = {
                'appid': app_id,
                'mch_id': wechat_pay_id,
                'nonce_str': get_nonce_str(),
                'body': order_num,  # 商品描述
                'out_trade_no': payment_number,  # 商户订单号
                'total_fee': int(float(money) * 100),
                'notify_url': notify_url,
                'trade_type': 'JSAPI',
                'openid': open_id,
                'timeStamp': str(int(time.time())),

            }

            wxpay = WxPay(wechat_pay_secret, **data)
            pay_info, dR, prepay_id = wxpay.get_pay_info()

            if dR == 0:
                sql = "update wechat_mall_payment set prepay_id=%s where payment_number=%s"
                self.db.query(sql, [prepay_id, payment_number])
                sql = """update wechat_mall_payment set timestamp_=%s,noncestr=%s,
                package=%s,paysign=%s,total_fee=%s where payment_number=%s"""
                self.db.query(sql,
                              [pay_info['timeStamp'], pay_info['nonceStr'], pay_info['package'], pay_info['paySign'],
                               int(float(money) * 100), payment_number])
                return self.jsons({'code': 0, 'data': pay_info, 'msg': self.error_code['ok']})
            elif dR == 2:
                sql = "select id from mall where appid=%s and mchid=%s and usr_id = %s"
                l, t = self.db.select(sql, [pay_info['appid'], pay_info['mch_id'], self.subusr_id])
                sql = "select id from wechat_mall_order where order_num=%s and usr_id=%s"
                m, n = self.db.select(sql, [order_num, self.subusr_id])

                if pay_info.get('err_code') == 'ORDERPAID':  # 订单已支付
                    if t > 0 and n > 0:
                        try:
                            sql = """update wechat_mall_order set 
                            status=2,status_str='待发货',uid=0,utime=now(),pay_ctime=now(),pay_status=%s 
                            where usr_id=%s and order_num=%s"""
                            self.db.query(sql, [payType, self.subusr_id, order_num])
                            sql = "update wechat_mall_payment set status=1,status_str='支付成功',uid=0,utime=now() where usr_id=%s and payment_number=%s"
                            self.db.query(sql, [self.subusr_id, payment_number])
                            if ctype == 2:  # 支付处理拼团数据
                                if str(pt_type) == '0':  # 开团
                                    self.Pingtuan_add(wechat_user_id, ptid, gid, phone)
                                elif str(pt_type) == '1':  # 参团
                                    self.Pingtuan_join(wechat_user_id, ptkid, gid, phone)

                            return self.jsons({'code': 110, 'msg': pay_info.get('err_code_des')})
                        except:
                            pass
                return self.jsons({'code': 10, 'msg': pay_info.get('err_code_des')})
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

    def goPartTopic_category(self):  # 文章分类接口

        type = self.RQ('type', '')

        if type == '' or type == 'None' or type == 'undefined' or type == 'null':
            type = ''

        sql = """
            select id,cname as name,ctype as type,pic,to_char(ctime,'YYYY-MM-DD HH24:MI')date 
            from  cms_fl where usr_id=%s   and coalesce(del_flag,0)=0  order by sort,id desc
                """
        parm = [self.subusr_id]
        if type != '':
            sql += "ctype=%s"
            parm.append(type)
        l, n = self.db.fetchall(sql, parm)
        if n == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartTopic_list(self):  # 文章列表接口
        id = self.RQ('id', '')
        type = self.RQ('type', '')
        page = self.RQ('page', '')
        size = self.RQ('size', '')

        if type == 'None' or type == 'undefined' or type == 'null':
            type = ''
        if id == 'None' or id == 'undefined' or id == 'null':
            id = ''

        if page == '' or page == 'None' or page == 'undefined' or page == 'null':
            page = 1
        if size == '' or size == 'None' or size == 'undefined' or size == 'null':
            size = 10

        page = int(page)
        size = int(size)

        sql = """
            select id,title,ctype as type,to_char(ctime,'YYYY-MM-DD HH24:MI')date,pic,sketch,coalesce(recom,0)recom
            ,coalesce(see,0) as views,coalesce(likes,0)likes,coalesce(favorite,0)favorite 
            from cms_doc where usr_id=%s   and coalesce(del_flag,0)=0  
                """
        parm = [self.subusr_id]
        if id != '':
            sql+= """
                 and class_id=%s
                            """
            parm.append(id)
        sql+=" order by sort,id desc"
        if type != '':
            sql = """
                select cd.id,cd.title,cd.ctype as type,to_char(cd.ctime,'YYYY-MM-DD HH24:MI')date,cd.pic,sketch,coalesce(recom,0)recom
            ,coalesce(see,0) as views,coalesce(likes,0)likes,coalesce(favorite,0)favorite  
                from cms_doc cd
                left join cms_fl cm on cm.id=cd.class_id and cd.usr_id=cm.usr_id
                where cd.usr_id=%s   and coalesce(cd.del_flag,0)=0 and cm.ctype=%s  order by cd.sort,cd.id desc
                            """
            parm = [self.subusr_id, type]

        l, n = self.db.fetchall(sql, parm)
        if n == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(l, n, pageNo=page, select_size=size)
        return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

    def goPartTopic_content(self):  # 文章详情接口

        id = self.RQ('id', '')
        token = self.REQUEST.get('token', '')

        if id == '' or id == 'None' or id == 'undefined' or id == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if token == 'None' or token == 'undefined' or token == 'null':
            token =''

        sql = """
             select id,title,ctype as type,keywords as keyword,pic,sketch,class_id,
             contents as content,to_char(ctime,'YYYY-MM-DD HH24:MI')date,coalesce(recom,0)recom
            ,coalesce(views,0) as views,coalesce(likes,0)likes,coalesce(favorite,0)favorite,goods
           
            from cms_doc where usr_id=%s   and coalesce(del_flag,0)=0  and  id=%s
                
                """
        parm = [self.subusr_id, id]

        l = self.db.fetch(sql, parm)
        if len(l) == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        sql = "update cms_doc set views=coalesce(views,0)+1 where id=%s"
        self.db.query(sql, [id])
        if token!='':
            dR = self.check_token(token)
            if dR['code'] == 0:
                wechat_user_id = dR['wechat_user_id']

                l['favstart'] = 0
                l['likestart'] = 0
                sql = """
                select id from cms_favorite 
                where usr_id=%s and wechat_user_id=%s and doc_id=%s and coalesce(del_flag,0)=0
                            """
                parm = [self.subusr_id, wechat_user_id, id]

                lT, t = self.db.select(sql, parm)
                if t > 0:
                    l['favstart'] = 1

                sql = """
                       select id from cms_likes 
                        where usr_id=%s and wechat_user_id=%s and doc_id=%s and coalesce(del_flag,0)=0
                                """
                parm = [self.subusr_id, wechat_user_id, id]
                lT1, t = self.db.select(sql, parm)
                if t > 0:
                    l['likestart'] = 1
        goods = l.get('goods', '')
        if goods != '':
            sql = """
                select id	--商品ID
                    ,name	--商品名称
                    ,introduce	--商品简介
                    ,pic	--商品第一张图片
                    ,originalprice as original_price	--商品原价
                    ,minprice as mini_price	--商品现价
                from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and id in (%s)
            """ % (self.subusr_id, goods)
            L, t = self.db.fetchall(sql)
            if t > 0:
                l['goodslist'] = L

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartTopic_favorite_add(self):  # 新增收藏文章接口

        id = self.RQ('id', '')
        token = self.REQUEST.get('token', '')

        if id == '' or id == 'None' or id == 'undefined' or id == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
             select id from cms_favorite where usr_id=%s and wechat_user_id=%s and doc_id=%s and coalesce(del_flag,0)=0
                """
        parm = [self.subusr_id, wechat_user_id, id]

        l, t = self.db.select(sql, parm)
        if t > 0:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})

        sql = "Insert into cms_favorite(usr_id,wechat_user_id,doc_id,cid,ctime)values(%s,%s,%s,%s,now())"
        self.db.query(sql, [self.subusr_id, wechat_user_id, id, wechat_user_id])
        sql = "update cms_doc set favorite=coalesce(favorite,0)+1 where id=%s"
        self.db.query(sql, [id])
        return self.jsons({'code': 0, 'msg': '收藏成功'})

    def goPartTopic_favorite_del(self):  # 取消收藏文章接口

        id = self.RQ('id', '')
        token = self.REQUEST.get('token', '')

        if id == '' or id == 'None' or id == 'undefined' or id == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
             select id from cms_favorite where usr_id=%s and wechat_user_id=%s and doc_id=%s and coalesce(del_flag,0)=0
                """
        parm = [self.subusr_id, wechat_user_id, id]

        l, t = self.db.select(sql, parm)
        if t == 0:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})
        cid = l[0][0]
        sql = "update cms_favorite set del_flag=1 where id=%s"
        self.db.query(sql, [cid])
        sql = "update cms_doc set favorite=coalesce(favorite,0)-1 where id=%s"
        self.db.query(sql, [id])
        return self.jsons({'code': 0, 'msg': '取消收藏成功'})

    def goPartTopic_favorite_list(self):  # 我的文章收藏列表接口

        page = self.RQ('page', '')
        size = self.RQ('size', '')
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if page == '' or page == 'None' or page == 'undefined' or page == 'null':
            page = 1
        if size == '' or size == 'None' or size == 'undefined' or size == 'null':
            size = 10

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
             select c.id,c.title,c.ctype as type,coalesce(c.recom,0)recom,coalesce(c."views",0) as views,
                coalesce(c.likes,0)likes,coalesce(c.favorite,0)favorite,c.pic,c.sketch,
                to_char(c.ctime,'YYYY-MM-DD HH24:MI')date 
            from cms_favorite f 
            left join cms_doc c on c.usr_id=f.usr_id and c.id=f.doc_id
            where f.usr_id=%s and f.wechat_user_id=%s and coalesce(f.del_flag,0)=0
                """
        parm = [self.subusr_id, wechat_user_id]

        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(l, t, pageNo=int(page),
                                                                                select_size=int(size))

        return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

    def goPartTopic_likes_add(self):  # 新增文章点赞接口

        id = self.RQ('id', '')
        token = self.REQUEST.get('token', '')

        if id == '' or id == 'None' or id == 'undefined' or id == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
             select id from cms_likes where usr_id=%s and wechat_user_id=%s and doc_id=%s and coalesce(del_flag,0)=0
                """
        parm = [self.subusr_id, wechat_user_id, id]

        l, t = self.db.select(sql, parm)
        if t > 0:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})

        sql = "Insert into cms_likes(usr_id,wechat_user_id,doc_id,cid,ctime)values(%s,%s,%s,%s,now())"
        self.db.query(sql, [self.subusr_id, wechat_user_id, id, wechat_user_id])
        sql = "update cms_doc set likes=coalesce(likes,0)+1 where id=%s"
        self.db.query(sql, [id])

        return self.jsons({'code': 0, 'msg': '点赞成功'})

    def goPartTopic_likes_del(self):  # 取消文章点赞接口

        id = self.RQ('id', '')
        token = self.REQUEST.get('token', '')

        if id == '' or id == 'None' or id == 'undefined' or id == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
             select id from cms_likes where usr_id=%s and wechat_user_id=%s and doc_id=%s and coalesce(del_flag,0)=0
                """
        parm = [self.subusr_id, wechat_user_id, id]

        l, t = self.db.select(sql, parm)
        if t == 0:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})
        cid = l[0][0]
        sql = "update cms_likes set del_flag=1 where id=%s"
        self.db.query(sql, [cid])
        sql = "update cms_doc set likes=coalesce(likes,0)-1 where id=%s"
        self.db.query(sql, [id])
        return self.jsons({'code': 0, 'msg': '取消收藏成功'})

    def goPartTopic_likes_list(self):  # 我的文章点赞列表接口

        page = self.RQ('page', '')
        size = self.RQ('size', '')
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if page == '' or page == 'None' or page == 'undefined' or page == 'null':
            page = 1
        if size == '' or size == 'None' or size == 'undefined' or size == 'null':
            size = 10

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
             select c.id,c.title,c.ctype as type,coalesce(c.recom,0)recom,coalesce(c."views",0) as views,
                coalesce(c.likes,0)likes,coalesce(c.favorite,0)favorite,c.pic,c.sketch,
                to_char(c.ctime,'YYYY-MM-DD HH24:MI')date 
            from cms_likes f 
            left join cms_doc c on c.usr_id=f.usr_id and c.id=f.doc_id
            where f.usr_id=%s and f.wechat_user_id=%s and coalesce(f.del_flag,0)=0
                """
        parm = [self.subusr_id, wechat_user_id]

        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(l, t, pageNo=int(page),
                                                                                select_size=int(size))

        return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

    def goPartCheck_money_pay(self):  # 自助买单接口

        money = self.RQ('money', '')
        token = self.REQUEST.get('token', '')
        coupon = self.RQ('coupon', '')

        if money == '' or money == 'None' or money == 'undefined' or money == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('money')})
        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if coupon == 'None' or coupon == 'undefined' or coupon == 'null':
            coupon = ''

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        USER = self.oUSER.get(self.subusr_id, wechat_user_id)

        if USER == {}:
            return self.jsons({'code': 10000, 'msg': self.error_code[10000]})

        if str(USER.get('status', '')) == '1':
            return self.jsons({'code': 701, 'msg': self.error_code[701]})
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
            'usr_id': self.subusr_id,
            'order_num ': order_num,
            'wname': wname,
            'avatar': avatar,
            'total': float(money),
            'ctype': 1
        }

        # score
        # null, --获得积分数量


        now = datetime.datetime.now()
        ctime = now.strftime('%Y-%m-%d %H:%M:%S')
        order_dict['ctime'] = ctime
        sql = "select COALESCE(close_time,0),COALESCE(close_time_pk,0) from shop_set where usr_id=%s"
        l, t = self.db.select(sql, self.subusr_id)
        if t > 0:
            close_time, close_time_pk = l[0]
            new_close_time = close_time
            delta = datetime.timedelta(minutes=int(new_close_time))
            n_days = now + delta
            data_close = n_days.strftime('%Y-%m-%d %H:%M:%S')
            order_dict['data_close'] = data_close
        #优惠券处理
        if coupon!='':
            l=self.check_my_coupons(coupon,wechat_user_id)
            if l==[]:
                return self.jsons({'code': 406, 'msg': '优惠券有误'})
            coupon_id,coupon_name,apply_ext_num, apply_ext_money, apply_id=l

            order_dict['couponid'] = coupon_id
            order_dict['couponname'] = coupon_name
            if float(money) < float(apply_ext_money):
                return self.jsons({'code':405, 'msg': self.error_code[405]})
            if str(apply_id)=='0':#满减
                coupon_price=float(apply_ext_num)
                order_dict['counpon'] = coupon_price
                money=round(float(money)-float(apply_ext_num),2)
            elif str(apply_id)=='1':#折扣
                coupon_price=round(float(money)*(1-float(apply_ext_num)/100),2)
                order_dict['counpon'] = coupon_price
                money=round(float(money)*float(apply_ext_num)/100,2)

        ##确定会员折扣
        vip_state, vip_level, vip_level_name, vip_sale=self.get_vip_type(wechat_user_id)
        new_total=round(float(money) * float(vip_sale),2)
        vipsale = round(float(money) - float(new_total), 2)
        #生成订单写入数据库返回
        order_dict['vipsale'] = vipsale
        order_dict['truemoney'] = new_total

        self.db.insert('offline_pay', order_dict)
        order_id = self.db.fetchcolumn("select id from offline_pay where order_num='%s'" % order_num)
        self.write_order_log(order_id, '创建订单', edit_remark='订单号:%s' % order_num)
        if order_dict.get('counpon', '') != '':
            sql = """
                    update  my_coupons set state=1,state_str='已使用' where id=%s and wechat_user_id=%s and usr_id=%s
                    """
            self.db.query(sql, [coupon_id, wechat_user_id, self.subusr_id])
            self.write_order_log(order_id, '更新优惠券状态',
                                 '使用优惠券id:%s,优惠券名称:%s,优惠券价格:%s' % (coupon_id, coupon_name, coupon_price),
                                 '订单号:%s' % order_num)

        return self.jsons({'code': 0,'data':{'id':order_id,'order_number':order_num,'money':new_total}, 'msg': self.error_code['ok']})

    def goPartUser_paypal_code(self):  # 用户付款码接口
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        nums,romcode = str(time.time()).split('.')
        upperCase = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',  'J', 'K', 'L', 'M', 'N',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        ]

        Dstr = random.sample(upperCase, 6)
        D_c = ''.join(Dstr)
        paykey = nums + D_c  # + danhao + romcode
        sql="select id from self_paykey where usr_id=%s and wechat_user_id=%s"
        l,t=self.db.select(sql,[self.subusr_id,wechat_user_id])
        if t==0:
            sql="insert into self_paykey(usr_id,wechat_user_id,paykey,ctime)values(%s,%s,%s,now())"
            self.db.query(sql,[self.subusr_id,wechat_user_id,paykey])
            return self.jsons({'code': 0, 'data': {'paykey': paykey}, 'msg': self.error_code['ok']})
        sid=l[0][0]
        sql="update self_paykey set paykey=%s,ctime=now() where id=%s"
        self.db.query(sql,[paykey,sid])
        return self.jsons({'code': 0,'data':{'paykey':paykey},'msg': self.error_code['ok']})

    def goPartUser_paypal_info(self):  # 买单状态接口
        token = self.REQUEST.get('token', '')
        orderid = self.RQ('orderid', '')
        paykey = self.RQ('paykey', '')

        if token == '' or token == 'None' or token == 'undefined' or token == 'null':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if orderid == 'None' or orderid == 'undefined' or orderid == 'null':
            orderid = ''
        if paykey == 'None' or paykey == 'undefined' or paykey == 'null':
            paykey = ''

        if paykey == '' and orderid == '':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('paykey or orderid')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
            select coalesce(status,0) as state,coalesce(total,0) as money,coalesce(counpon,0) as counpon,
            coalesce(vipsale,0) as vipsale,truemoney,coalesce(score,0) as score,
            to_char(paytime,'YYYY-MM-DD HH24:MI') as paytime 
            from offline_pay where usr_id=%s and wechat_user_id=%s
        """
        parm = [self.subusr_id, wechat_user_id]
        if orderid != '':
            sql += ' and id=%s'
            parm.append(orderid)
        if paykey != '':
            sql += ' and paykey=%s'
            parm.append(paykey)
        l = self.db.fetch(sql, parm)
        if len(l) == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartgoods_random(self):  # 随机推荐商品接口
        """
        参数名称	参数说明	是否必填
        page	获取第几页数据，不传该参数默认第一页	否
        page_size	每页获取多少条数据，不传该参数默认为100	否
        category_id	获取指定分类下的商品	否
        barcode	商品条码	否
        status	是否推荐，0为不推荐，1为推荐	否
        search_key	搜索关键词，会匹配商品标题+商品简介+商品详情	否
        paixu	排序规则：priceUp 商品升序，priceDown 商品倒序，ordersUp 销量升序，ordersDown 销量降序，addedUp 发布时间升序，addedDown 发布时间倒序

        """
        number = self.RQ('number', '1')
        price = self.REQUEST.get('price', '')
        if price == 'None' or price == 'undefined' or price == 'null':
            price = ''

        try:
            ran = int(number)
        except:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})

        l = self.oGOODS.get(self.subusr_id)
        t = len(l)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        if price != '':
            List = []
            pL = price.split(',')
            try:
                m, n = int(pL[0]), int(pL[1])
            except:
                return self.jsons({'code': 405, 'msg': self.error_code[405]})

            for i in l:
                mini_price = i.get('mini_price')
                if m < mini_price and n > mini_price:
                    List.append(i)
            tt=len(List)
            if tt == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            if t>ran:
                L = random.sample(List, ran)
            else:
                L=List

            lT, DL, totalPrice = [],{}, 0.0

            for k in L:
                lD={}
                lD['buy_number'] = 1
                lD['active'] = 'true'
                goods_id = k.get('id')
                goods_name = k.get('name')
                goods_pic = k.get('pic')
                goods_price = k.get('mini_price')
                goods_weight = k.get('weight')
                lD['goods_id'] = goods_id
                lD['goods_name'] = goods_name
                lD['goods_pic'] = goods_pic
                lD['goods_price'] = goods_price
                lD['goods_weight'] = goods_weight
                totalPrice += float(goods_price)
                # goods_childs,goods_label
                sqls = "select sc_id from spec_child_price where usr_id=%s and goods_id=%s"
                ll, tl = self.db.select(sqls, [self.subusr_id, goods_id])
                if tl > 0:
                    il = random.sample(ll, 1)
                    goods_childs = il[0][0]
                    lD['goods_childs'] = goods_childs + ','
                    goods_label = ''
                    gl = goods_childs.split(',')
                    ia = 0
                    for g in gl:
                        A = g.split(':')
                        sqlp = """
                            select cname
                            from spec where id =%s and usr_id=%s 
                                    """
                        specInfo, It = self.db.select(sqlp, [A[0], self.subusr_id])
                        if ia == 0:
                            goods_label += specInfo[0][0]
                        else:
                            goods_label += ',' + specInfo[0][0]
                        sqlsc = """
                                            select cname_c
                                            from spec_child
                                            where id=%s and usr_id=%s 
                                        """
                        spec_childs, ct = self.db.select(sqlsc, [A[1],self.subusr_id])

                        goods_label += ':' + spec_childs[0][0]
                        ia += 1

                    lD['goods_label'] = goods_label

                lT.append(lD)
            DL['totalPrice'] = totalPrice
            DL['list'] = lT
            return self.jsons({'code': 0, 'data': DL, 'msg': self.error_code['ok']})
        if t > ran:
            L = random.sample(l, ran)
        else:
            L = l
        lT,DL,totalPrice=[],{},0.0

        for k in L:
            lD={}
            lD['buy_number']=1
            lD['active'] = 'true'
            goods_id = k.get('id')
            goods_name=k.get('name')
            goods_pic=k.get('pic')
            goods_price=k.get('mini_price')
            goods_weight=k.get('weight')
            lD['goods_id']=goods_id
            lD['goods_name'] = goods_name
            lD['goods_pic'] = goods_pic
            lD['goods_price'] = goods_price
            lD['goods_weight'] = goods_weight
            totalPrice+=float(goods_price)
            #goods_childs,goods_label

            sqls = "select sc_id from spec_child_price where usr_id=%s and goods_id=%s"
            ll, tl = self.db.select(sqls, [self.subusr_id, goods_id])
            if tl>0:
                il = random.sample(ll, 1)
                goods_childs=il[0][0]
                lD['goods_childs'] = goods_childs + ','

                goods_label=''
                gl=goods_childs.split(',')
                ia=0
                for g in gl:
                    A = g.split(':')
                    sqlp = """
                            select cname
                            from spec where id =%s and usr_id=%s and  coalesce(del_flag,0)=0 order by sort
                    """
                    specInfo, It = self.db.select(sqlp, [A[0], self.subusr_id])
                    if ia==0:
                        goods_label += specInfo[0][0]
                    else:
                        goods_label +=','+ specInfo[0][0]
                    sqlsc = """
                            select cname_c
                            from spec_child
                            where id=%s and usr_id=%s
                        """
                    spec_childs, ct = self.db.select(sqlsc,[A[1], self.subusr_id])
                    goods_label +=':'+ spec_childs[0][0]
                    ia+=1

                lD['goods_label'] = goods_label
            lT.append(lD)
        DL['totalPrice']=totalPrice
        DL['list'] = lT

        return self.jsons({'code': 0, 'data': DL, 'msg': self.error_code['ok']})
