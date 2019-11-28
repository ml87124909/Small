# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" manage/dl/E004_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import manage.dl.BASE_DL
    reload(manage.dl.BASE_DL)
from manage.dl.BASE_DL  import cBASE_DL

from basic.wxbase import WxPay
import  os

class cE004_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['','','','','','','','','','']
        self.FDT = [
            ['', '', ''],  # 0
            ['售后单号', '4rem', ''],  # 1
            ['售后类型', '10rem', ''],  # 2
            ['申请用户', '10rem', ''],  # 3
            ['申请原因', '10rem', ''],  # 4
            ['售后截图', '10rem', ''],  # 5
            ['售后商品', '6rem', ''],  # 6
            ['申请退款金额', '10rem', ''],  # 7
            ['订单合订金额', '10rem', ''],  # 8
            ['状态', '10rem', ''],  # 9


        ]
        # self.GNL=[] #列表上出现的
        self.GNL = self.parse_GNL([0, 1, 2, 3, 4, 5, 6, 7,8,9])



    def mRight(self):
            

        sql="""
            select id,e_num,ctype_str,w_name,reason,
                (select array_agg(pic) from images_api 
                where  images_api.timestamp=order_exchange.timestamp and images_api.other_id=order_exchange.order_id
                and order_exchange.usr_id=images_api.usr_id and ctype=1),
                (select  array_agg(row_to_json(row(good_id,good_name,pic,spec))) 
                from order_exchange_detail where order_exchange.id=order_exchange_detail.e_id),
                r_money,order_money,status_str,ctype,order_id,status
            from order_exchange
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

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
            select id
                ,fenlei
                ,title
                ,tags
                ,keywords
                ,descript
                ,income
                ,author
                ,isshow
                ,status
                ,sort
                ,pic
                ,content
            from cms_doc  
            where  id=%s and usr_id=%s
        """
        if pk != '':
            L = self.db.fetch( sql,[ pk,self.usr_id_p] )

        return L
    
    def local_add_save(self):
        

        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        
        #这些是操作权限
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}  
        pk = self.pk
        #dR={'R':'','MSG':'','isadd':''}
        dR={'R':'','MSG':''}
        save_flag = self.REQUEST.get("save_flag").strip()
        save_flag2 = self.cookie.getcookie("__flag")
        
        
        #获取表单参数
        fenlei=self.GP('fenlei')#分类
        title=self.GP('title')#类型
        tags=self.GP('tags')#是否展示
        keywords=self.GP('keywords')#内容
        descript = self.GP('descript')  # 标题
        income = self.GP('income')  # 类型
        author = self.GP('author')  # 是否展示
        isshow = self.GP('isshow')  # 内容
        status = self.GP('status')  # 内容
        sort=self.GP('sort')
        container = self.GP('container')  # 内容



        # if not (save_flag == save_flag2):
        #     #为FALSE时,当前请求为重刷新
        #     return dR
        
        # if danhao == '':
        #     dR['R'] = '1'
        #     dR['MSG'] = '请输入角色名字'
        
        data = {
                'fenlei':fenlei
                ,'title':title
                ,'tags':tags
                ,'keywords':keywords
                ,'descript': descript
                , 'income': income
                , 'author': author
                , 'isshow': isshow
                ,'status':status
                ,'content':container
                ,'sort':sort
                ,'cid': self.usr_id
                ,'ctime': self.getToday(9)
                ,'uid': self.usr_id
                ,'utime': self.getToday(9)
                ,'usr_id':self.usr_id_p

        }
        for k in list(data):
            if data[k] == '':
                data.pop(k)

        from werkzeug import secure_filename
        try:
            file = self.objHandle.files['pic']
            if file:
                filename = secure_filename(file.filename)
                data['pic'] = filename  ##封面展示图片
                file.save(os.path.join(public.ATTACH_ROOT, filename))
        except:
            pass

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data.pop('cid')
            data.pop('ctime')
            #data.pop('random')

            self.db.update('cms_doc' , data , " id = %s " % pk)

        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data.pop('uid')
            data.pop('utime')

            self.db.insert('cms_doc' , data)
            pk = self.db.insertid('cms_doc_id')#这个的格式是表名_自增字段
            #dR['isadd'] = 1
        #self.listdata_save(pk,danhao)
        dR['pk'] = pk
        
        return dR

    def getfllist(self):
        L=[]
        sql="select id,name from cms_fl"
        l,t=self.db.select(sql)
        if t>0:
            L=l

        return L

    # def delete_data(self):
    #     pk = self.pk
    #     dR = {'R':'', 'MSG':''}
    #     self.db.query("update cms_doc set del_flag=1 where id= %s" % pk)
    #     return dR

    def get_order_reply_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        sid = self.GP('sid', '')
        t_money= self.GP('t_money', '')
        if id == '' or sid=='' or t_money=='':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select order_id,order_num,e_num,order_money,r_money from order_exchange where id=%s and status=89"
        l,t=self.db.select(sql,id)
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR
        order_id, order_num, e_num, order_money, r_money = l[0]
        if float(t_money)>r_money:
            dR['code'] = '1'
            dR['MSG'] = '退款金额大于申请金额！'
            return dR

        mall = self.oMALL.get(self.usr_id_p)
        if mall == {}:
            dR['code'] = '1'
            dR['MSG'] = '请到店铺设置填写小程序设置'
            return dR


        sql="select balance,wechat_user_id from wechat_mall_order where usr_id=%s and id=%s"
        ll,tt=self.db.select(sql,[self.usr_id_p,order_id])
        if tt==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR

        balance,wechat_user_id=ll[0]
        if balance>0 or str(sid)=='2':
            sql="update order_exchange set status=88,status_str='售后成功',refund_type=%s where id=%s"
            self.db.query(sql,[sid,id])
            sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
            self.db.query(sql, [float(t_money), wechat_user_id])
            sql = """insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,remark,
                            cid,ctime)values(%s,%s,3,'消费',%s,4,'退回','退款',%s,now())"""
            self.db.query(sql, [self.usr_id_p, wechat_user_id, float(t_money), self.usr_id])
            self.oUSER.update(self.usr_id_p, wechat_user_id)
            dR['code'] = '0'
            dR['MSG'] = '退款操作完成!'
            return dR

        else:
            sql = "update order_exchange set status=88,status_str='售后成功',refund_type=%s where id=%s"
            self.db.query(sql, [sid, id])
            a = self.order_refund(order_id, order_num, e_num, wechat_user_id)
            if a == 1:
                dR['code'] = '1'
                dR['MSG'] = '退款操作失败!'
                return dR
            sql = """insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,remark,
                                       cid,ctime)values(%s,%s,3,'消费',%s,4,'退回','退款',%s,now())"""
            self.db.query(sql, [self.usr_id_p, wechat_user_id, float(t_money), self.usr_id])
            self.oUSER.update(self.usr_id_p, wechat_user_id)
            dR['code'] = '0'
            dR['MSG'] = '退款操作完成!'
            return dR


        # sql = "update wechat_mall_order_detail set status=98,status_str='退款成功' where usr_id=%s  and order_id=%s"
        # self.db.query(sql, [self.usr_id, order_id])
        # self.write_order_log(id, 'status,status_str', 'status=98,status_str=退款成功', '后台同意退款,更新订单表,订单明细表状态')
        # if str(sid)=='2':
        #     sql="update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
        #     self.db.query(sql,[new_total,wechat_user_id])
        # else:
        #     if balance==new_total:
        #         sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
        #         self.db.query(sql, [new_total, wechat_user_id])
        #     else:
        #         sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
        #         self.db.query(sql, [balance, wechat_user_id])
        #         a=self.order_refund(order_id, order_num, r_num,wechat_user_id)
        #         if a==1:
        #             dR['code'] = '1'
        #             dR['MSG'] = '退款操作失败!'
        #             return dR
        # self.oUSER.update(self.usr_id,wechat_user_id)
        # dR['code'] = '0'
        # dR['MSG'] = '退款操作完成!'
        # return dR

    def order_refund(self,order_id,order_num,re_num,wechat_user_id):


        mall = self.oMALL.get(self.usr_id_p)

        app_id = mall.get('appid','')
        secret = mall.get('secret','')
        wx_mch_id = mall.get('mchid','')
        wx_mch_key = mall.get('mchkey','')
        base_url = mall.get('base_url','')#'https://malishop.janedao.cn'
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
        sql="select order_id,order_num,e_num from order_exchange where id=%s and status=89"
        l,t=self.db.select(sql,id)
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR


        sql="select o_gid from order_exchange_detail where usr_id=%s and e_id=%s and status=89"
        ll,tt=self.db.select(sql,[self.usr_id_p,id])
        if tt==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR


        sql="""update order_exchange set status=87,status_str='售后失败',not_memo=%s,uid=%s,utime=now() 
                where id=%s and status=89"""
        self.db.query(sql,[sid,self.usr_id,id])
        sql = """update order_exchange_detail set status=87,status_str='售后失败',not_memo=%s,uid=%s,utime=now() 
                        where e_id=%s and status=89"""
        self.db.query(sql, [sid, self.usr_id, id])


        for i in ll:
            gid=i[0]
            sql = "update wechat_mall_order_detail set status=87,status_str='售后失败',uid=%s,utime=now() where usr_id=%s  and id=%s"
            self.db.query(sql, [self.usr_id,self.usr_id_p, gid])
            self.write_order_log(gid, '明细id,status,status_str', 'id=%s,status=87,status_str=售后失败'%gid, '后台驳回售后,更新订单明细表状态')

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
        sql="select not_memo from order_exchange where id=%s and status=87"
        l,t=self.db.select(sql,id)
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR


        dR['code'] = '0'
        dR['memo'] =l[0][0]

        return dR

    def get_order_ok_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')

        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select order_id from order_exchange where usr_id=%s and id=%s and status=89"
        l,t=self.db.select(sql,[self.usr_id_p,id])
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR

        order_id=l[0][0]
        sql="select o_gid from order_exchange_detail where usr_id=%s and  e_id=%s"
        ll,tt=self.db.select(sql,[self.usr_id_p,id])
        if tt==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单没有申请商品'
            return dR
        self.db.query("update order_exchange set status=86,status_str='售后待补充信息' where id=%s",id)
        for i in ll:
            did=i[0]
            self.db.query("update wechat_mall_order_detail set status=86,status_str='售后待补充信息' where id=%s", did)
        dR['code'] = '0'
        dR['MSG'] = '同意成功!'
        return dR

    def get_order_ig_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')

        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select kuaname,kd_number from order_exchange where usr_id=%s and id=%s and status=85"
        l,t=self.db.select(sql,[self.usr_id_p,id])
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR

        kuaname, kd_number=l[0]

        dR['code'] = '0'
        dR['kuaname'] = kuaname
        dR['kd_number'] = kd_number
        return dR

    def get_order_ig_save_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')

        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select id from order_exchange where usr_id=%s and id=%s and status=85"
        l,t=self.db.select(sql,[self.usr_id_p,id])
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR

        sql="update order_exchange set status=88,status_str='售后成功' where id=%s"
        self.db.query(sql,id)

        dR['code'] = '0'
        dR['MSG'] = '退货信息处理成功!'
        return dR

    def get_retweet_ig_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        sid = self.GP('sid', '')
        if id == '' or sid=='':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select order_id,order_num,e_num from order_exchange where id=%s and status=85"
        l,t=self.db.select(sql,id)
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR

        sql="select o_gid from order_exchange_detail where usr_id=%s and e_id=%s"
        ll,tt=self.db.select(sql,[self.usr_id_p,id])
        if tt==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR

        sql="""update order_exchange set status=86,status_str='售后待补充信息',not_memo=%s,uid=%s,utime=now() 
                where id=%s and status=85"""
        self.db.query(sql,[sid,self.usr_id,id])

        for i in ll:
            gid=i[0]
            sql = "update wechat_mall_order_detail set status=86,status_str='售后待补充信息',uid=%s,utime=now() where usr_id=%s  and id=%s"
            self.db.query(sql, [self.usr_id,self.usr_id_p, gid])
            self.write_order_log(gid, '明细id,status,status_str', 'id=%s,status=86,status_str=售后待补充信息'%gid, '后台驳回售后,更新订单明细表状态')

        dR['code'] = '0'
        dR['MSG'] = '驳回原因提交成功!'
        return dR

    def get_order_ig_r_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')

        if id == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql="select kuaname,kd_number,r_money from order_exchange where usr_id=%s and id=%s and status=85"
        l,t=self.db.select(sql,[self.usr_id_p,id])
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR

        kuaname, kd_number,r_money=l[0]

        dR['code'] = '0'
        dR['kuaname'] = kuaname
        dR['kd_number'] = kd_number
        dR['r_money'] = r_money
        return dR

    def get_order_ig_reply_data(self):
        dR = {'code': '', 'MSG': ''}
        id = self.GP('id', '')
        sid = self.GP('sid', '')
        t_money = self.GP('t_money', '')
        if id == '' or sid == '' or t_money == '':
            dR['code'] = '1'
            dR['MSG'] = '参数有误！'
            return dR
        sql = "select order_id,order_num,e_num,order_money,r_money from order_exchange where id=%s and status=85"
        l, t = self.db.select(sql, id)
        if t == 0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR
        order_id, order_num, e_num, order_money, r_money = l[0]

        if float(t_money)>r_money:
            dR['code'] = '1'
            dR['MSG'] = '退款金额大于申请金额！'
            return dR

        mall = self.oMALL.get(self.usr_id_p)
        if mall == {}:
            dR['code'] = '1'
            dR['MSG'] = '请到店铺设置填写小程序设置'
            return dR

        sql = "select balance,wechat_user_id from wechat_mall_order where usr_id=%s and id=%s"
        ll, tt = self.db.select(sql, [self.usr_id_p, order_id])
        if tt == 0:
            dR['code'] = '1'
            dR['MSG'] = '售后单状态不正常'
            return dR

        balance, wechat_user_id = ll[0]
        if balance > 0 or str(sid) == '2':
            sql = "update order_exchange set status=88,status_str='售后成功',refund_type=%s where id=%s"
            self.db.query(sql, [sid, id])
            sql = "update wechat_mall_user set balance=coalesce(balance,0)+%s where id=%s"
            self.db.query(sql, [float(t_money), wechat_user_id])
            sql = """insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,remark,
                                    cid,ctime)values(%s,%s,3,'消费',%s,4,'退回','退款',%s,now())"""
            self.db.query(sql, [self.usr_id_p, wechat_user_id, float(t_money), self.usr_id])
            self.oUSER.update(self.usr_id_p, wechat_user_id)
            dR['code'] = '0'
            dR['MSG'] = '退款操作完成!'
            return dR

        else:
            sql = "update order_exchange set status=88,status_str='售后成功',refund_type=%s where id=%s"
            self.db.query(sql, [sid, id])
            a = self.order_refund(order_id, order_num, e_num, wechat_user_id)
            if a == 1:
                dR['code'] = '1'
                dR['MSG'] = '退款操作失败!'
                return dR
            sql = """insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,remark,
                                               cid,ctime)values(%s,%s,3,'消费',%s,4,'退回','退款',%s,now())"""
            self.db.query(sql, [self.usr_id_p, wechat_user_id, float(t_money), self.usr_id])
            self.oUSER.update(self.usr_id, wechat_user_id)
            dR['code'] = '0'
            dR['MSG'] = '退款操作完成!'
            return dR

