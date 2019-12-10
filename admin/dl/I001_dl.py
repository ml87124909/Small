# -*- coding: utf-8 -*-

##############################################################################
#
#
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':    
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cI001_dl(cBASE_DL):
    def init_data(self):
        self.part = self.GP('part', 'Localfrm')
        self.tab = self.GP("tab", "1")

    def get_local_data(self):
        """获取 local 表单的数据
        """
        #if self.tab == '1':
        sql = """
            select 
                appid,
                secret,
                wx_status,
                wxtoken,
                wxaeskey,
                 mchid,
                mchkey,
                back_url,
                base_url,
                try_days,
                invite_days,
                vip_days,
                pay_status,
                combo_one_name,
                combo_one_price,
                combo_one_day,
                combo_one_txt,
                combo_two_name,
                combo_two_price,
                combo_two_day,
                combo_two_status,
                combo_two_txt,
                combo_thr_name,
                combo_thr_price,
                combo_thr_day,
                combo_thr_status,
                combo_thr_txt,
                /*call_url,
                re_url,
                oss_one_day,
                oss_one_size,
                oss_one_price,
                oss_two_day,
                oss_two_size,
                oss_two_price,
                oss_thr_day,
                oss_thr_size,
                oss_thr_price,
                domain_url,
                ptype,
                remark*/
                dbname,
                notices,
                memo
                
            from platform_conf where id=1
                """
        l = self.db.fetch(sql)
        return l



    
    def local_add_save(self):

        dR = {'code': '', 'MSG': '保存成功'}
        wx_status = self.GP('wx_status', '0')  # logo链接
        appid = self.GP('appid', '')  # logo链接
        secret = self.GP('secret', '')  # logo链接
        wxtoken = self.GP('wxtoken', '')  # logo链接
        wxaeskey = self.GP('wxaeskey', '')  # logo链接
        back_url = self.GP('back_url', '')  # VIP微信支付回调域名
        base_url = self.GP('base_url', '')  # 平台微信支付回调域名
        try_days = self.GP('try_days', '')  # 试用期(天)
        invite_days = self.GP('invite_days', '')  #邀请注册赠送时间
        vip_days = self.GP('vip_days', '')  #vip付费邀请人赠送时间
        pay_status=self.GP('pay_status','')
        combo_one_name = self.GP('combo_one_name', '')  #套餐1名称
        combo_one_price = self.GP('combo_one_price', '')  #套餐1价格
        combo_one_status = self.GP('combo_one_status', '')  # 套餐1是否启用
        combo_one_day = self.GP('combo_one_day', '')  # 套餐1时长（天）
        combo_two_name = self.GP('combo_two_name', '')  # 套餐2名称
        combo_two_price = self.GP('combo_two_price', '')  # 套餐2价格
        combo_two_day = self.GP('combo_two_day', '')  # 套餐2时长（天）
        combo_two_status = self.GP('combo_two_status', '')  # 套餐2是否启用
        combo_thr_name = self.GP('combo_thr_name', '')  # 套餐3名称
        combo_thr_price = self.GP('combo_thr_price', '')  # 套餐3价格
        combo_thr_day = self.GP('combo_thr_day', '')  # 套餐3时长（天）
        combo_thr_status = self.GP('combo_thr_status', '')  # 套餐3是否启用
        combo_one_txt = self.GP('combo_one_txt', '')  # 套餐1说明
        combo_two_txt = self.GP('combo_two_txt', '')  # 套餐2说明
        combo_thr_txt = self.GP('combo_thr_txt', '')  # 套餐3说明
        # call_url = self.GP('call_url', '')  # 支付回调
        # re_url = self.GP('re_url', '')  # 支付返回
        dbname = self.GP('dbname', '')  # 备份数据库名
        # oss_one_day = self.GP('oss_one_day', '')  # 存储包1天数
        # oss_one_size = self.GP('oss_one_size', '')  # 存储包1容量
        # oss_one_price = self.GP('oss_one_price', '')  # 存储包1价格
        # oss_two_day = self.GP('oss_two_day', '')  # 存储包2天数
        # oss_two_size = self.GP('oss_two_size', '')  # 存储包2容量
        # oss_two_price = self.GP('oss_two_price', '')  # 存储包2价格
        # oss_thr_day = self.GP('oss_thr_day', '')  # 存储包3天数
        # oss_thr_size = self.GP('oss_thr_size', '')  # 存储包3容量
        # oss_thr_price = self.GP('oss_thr_price', '')  # 存储包3价格
        notices = self.GP('notices', '')  # 顶部消息
        memo = self.GP('memo', '')  # 滚动消息



        mchid = self.GP('mchid', '')  # logo链接
        mchkey = self.GP('mchkey', '')  # logo链接
        #ptype = self.GP('ptype', '')
        #callback_url = self.GP('callback_url', '')  # logo链接
        #remark=self.REQUEST.get('remark','')
        # if appid not in ['wx19bdd62fb84490d4']:
        #     wx_status=0
        #cur_random_no = "%s%s" % (time.time(), random.random())
        data = {
            'pay_status':pay_status or None,
            'wx_status': wx_status or None,
            'appid': appid,
            'secret': secret,
            'wxtoken':wxtoken,
            'wxaeskey':wxaeskey,
            'mchid': mchid,
            'mchkey': mchkey,
            'back_url': back_url,
            'base_url': base_url,
            'try_days': try_days or None,
            'invite_days': invite_days or None,
            'vip_days': vip_days or None,
            'combo_one_name': combo_one_name,
            'combo_one_price': combo_one_price or None,
            'combo_one_day': combo_one_day or None,
            'combo_one_status': combo_one_status or None,
            'combo_two_name': combo_two_name,
            'combo_two_price': combo_two_price or None,
            'combo_two_day': combo_two_day or None,
            'combo_two_status': combo_two_status or None,
            'combo_thr_name': combo_thr_name,
            'combo_thr_price': combo_thr_price or None,
            'combo_thr_day': combo_thr_day or None,
            'combo_thr_status': combo_thr_status or None,
            'combo_one_txt': combo_one_txt,
            'combo_two_txt': combo_two_txt,
            'combo_thr_txt': combo_thr_txt,

            # 're_url': re_url,
            # 'call_url': call_url,
            # 'oss_one_day': oss_one_day or None,
            # 'oss_one_size': oss_one_size or None,
            # 'oss_one_price': oss_one_price or None,
            # 'oss_two_day': oss_two_day or None,
            # 'oss_two_size': oss_two_size or None,
            # 'oss_two_price': oss_two_price or None,
            # 'oss_thr_day': oss_thr_day or None,
            # 'oss_thr_size': oss_thr_size or None,
            # 'oss_thr_price': oss_thr_price or None,
            'dbname': dbname,
            'notices': notices,
            'memo': memo,


            # 'ptype': ptype or None,
            # 'remark':remark

        }  # pt_conf
        # if wx_status != 0:
        #     data['wxtoken'] = wxtoken
        #     data['wxaeskey'] = wxaeskey
        sql="select id from platform_conf where id=1"
        l,t=self.db.select(sql)
        if t==0:
            self.db.insert('platform_conf', data)
            #ptid = self.db.fetchcolumn('select id from pt_conf where random_no=%s', cur_random_no)  # 这个的格式是表名_自增字段
            self.oTOLL.update()
            dR['code'] = '0'
            return dR

        self.db.update('platform_conf', data, " id = 1 ")
        self.oTOLL.update()
        # if domain_url != '':
        #     self.oMALL.loaddata()
        dR['code'] = '0'
        dR['MSG'] = '修改成功'
        return dR
        # 更新数据缓存

    def Search_data(self):

        dR = {'code': '', 'MSG': '查询成功'}
        uid = self.GP('uid', '')
        if uid == '':
            dR['MSG'] = '查询数据用误'
            return dR

        sql = "select out_trade_no,usr_id,days,ctype from alipay_log  where id=%s"
        l, t = self.db.select(sql, [uid])
        if t == 0:
            dR['MSG'] = '查询数据不存在'
            return dR
        out_trade_no, usr_id, days, ctype = l[0]
        import datetime
        from basic.pay import WeixinPay
        app_id = self.oTOLL.get('appid')
        wechat_pay_id = self.oTOLL.get('mchid')
        wechat_pay_secret = self.oTOLL.get('mchkey')
        base_url = self.oTOLL.get('callback_url')
        notify_url = base_url + '/vipnotify'

        wxpay = WeixinPay(app_id, wechat_pay_id, wechat_pay_secret, notify_url)
        data = {
            'out_trade_no': out_trade_no,  # 商户订单号
        }
        raw = wxpay.order_query(**data)
        if raw.get('trade_state') == 'SUCCESS':
            transaction_id = raw['transaction_id']
            openid = raw['openid']
            sql = "update alipay_log set openid=%s,transaction_id=%s,pay_status=1,pay_time=now() where id=%s"
            self.db.query(sql, [openid, transaction_id, uid])

            if ctype in (1, 2, 3):
                sqlu = """select to_char(expire_time,'YYYY-MM-DD HH24:MI'),
                        to_char(now(),'YYYY-MM-DD HH24:MI'),
                        case when to_char(expire_time,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
                        then 1 else 0 end,coalesce(inviteid,1) from users  where usr_id=%s"""
                lT, iN = self.db.select(sqlu, [usr_id])
                if iN > 0:
                    time_1, time_2, flag, inviteid = lT[0]
                    if flag == 1:
                        expire_time = time_1
                    else:
                        expire_time = time_2
                    now = datetime.datetime.strptime(expire_time, "%Y-%m-%d %H:%M")
                    delta = datetime.timedelta(days=days)
                    n_days = now + delta
                    e_time = n_days.strftime('%Y-%m-%d %H:%M:%S')
                    sql = "update users set expire_time=%s,vip_flag=%s,expire_flag=0 where usr_id=%s"
                    self.db.query(sql, [e_time, ctype, usr_id])
                    sql = "update alipay_log set etime=%s where out_trade_no=%s"
                    self.db.query(sql, [e_time, out_trade_no])

                    # pay_days = self.oTOLL.get('pay_days')
                    # if inviteid != 1 and pay_days != 0:
                    #
                    #     sqlu = """select to_char(expire_time,'YYYY-MM-DD HH24:MI'),
                    #         to_char(now(),'YYYY-MM-DD HH24:MI'),
                    #         case when to_char(expire_time,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI')
                    #         then 1 else 0 end from users  where usr_id=%s"""
                    #     lT, iN = self.db.select(sqlu, [inviteid])
                    #     if iN > 0:
                    #         time1, time2, flag_ = lT[0]
                    #         if flag_ == 1:
                    #             expiretime = time1
                    #         else:
                    #             expiretime = time2
                    #         now = datetime.datetime.strptime(expiretime, "%Y-%m-%d %H:%M")
                    #         delta = datetime.timedelta(days=pay_days)
                    #         n_days = now + delta
                    #         etime = n_days.strftime('%Y-%m-%d %H:%M:%S')
                    #         sql = "update users set expire_time=%s,expire_flag=0 where usr_id=%s"
                    #         self.db.query(sql, [etime, inviteid])
                    #         isql = """insert into invite_log(ctype,return_id,usr_id,openid,return_days,return_time,ctime)
                    #                    values(2,%s,%s,%s,%s,%s,now())"""
                    #         iparm = [inviteid, usr_id, openid, pay_days, etime]
                    #         self.db.query(isql, iparm)
                    # sqlr = "select id,role_id from usr_role where usr_id=%s"
                    # lr, tr = self.db.select(sqlr, [usr_id])
                    # if tr == 1:
                    #     urid, role_id = lr[0]  # role_id 2基础，3营销
                    #     if ctype == 1 and role_id != 2:  # 基础
                    #         self.db.query("update usr_role set role_id=2 where id=%s", [urid])
                    #     elif ctype == 2 and role_id != 3:  # 营销
                    #         self.db.query("update usr_role set role_id=3 where id=%s", [urid])
                    #     elif ctype == 3:  # 未知
                    #         pass
                dR['code'] = '0'
                dR['MSG'] = '查询到已支付，已对数据进行更新。'
                return dR

            if ctype == 4:
                sqlu = "select  oss_one_size from toll_config"
            elif ctype == 5:
                sqlu = "select  oss_two_size from toll_config"
            else:
                sqlu = "select  oss_thr_size from toll_config"
            lT, iN = self.db.select(sqlu)
            if iN > 0:
                size = lT[0][0]
                now = datetime.datetime.now()
                delta = datetime.timedelta(days=days)
                n_days = now + delta
                e_time = n_days.strftime('%Y-%m-%d %H:%M:%S')
                sql = "update users set oss_time=%s,oss_flag=%s,oss_all=coalesce(oss_all,0)+%s where usr_id=%s"
                self.db.query(sql, [e_time, ctype, size, usr_id])
                sql = "update alipay_log set etime=%s,utime=now() where out_trade_no=%s"
                self.db.query(sql, [e_time, out_trade_no])

            dR['code'] = '0'
            dR['MSG'] = '查询到已支付，已对数据进行更新。'
            return dR
        dR['MSG'] = 'trade_state_desc'
        return dR
