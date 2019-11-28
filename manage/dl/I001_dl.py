# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/I001_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import time
import random
class cI001_dl(cBASE_DL):
    def init_data(self):
        self.GNL = []  # 列表表头
    #在子类中重新定义         
    def myInit(self):

        self.part = self.GP('part', 'Localfrm')
        self.tab = self.GP("tab", "1")

    def get_local_data(self):
        """获取 local 表单的数据
        """
        if self.tab == '1':
            sql = """
                select 
	            convert_from(decrypt(wx_appid::bytea, %s, 'aes'),'SQL_ASCII') as wx_appid,
	            convert_from(decrypt(wx_secret::bytea, %s, 'aes'),'SQL_ASCII') as wx_secret,
	            convert_from(decrypt(wx_token::bytea, %s, 'aes'),'SQL_ASCII') as wx_token,
	            convert_from(decrypt(wx_aeskey::bytea, %s, 'aes'),'SQL_ASCII') as wx_aeskey,
	            convert_from(decrypt(mchid::bytea, %s, 'aes'),'SQL_ASCII') as mchid,
	            convert_from(decrypt(mchkey::bytea, %s, 'aes'),'SQL_ASCII') as mchkey,
	            callback_url,
	            applet_url,
	            convert_from(decrypt(sms_appid::bytea, %s, 'aes'),'SQL_ASCII') as sms_appid,
	            convert_from(decrypt(sms_appkey::bytea, %s, 'aes'),'SQL_ASCII') as sms_appkey,
	            convert_from(decrypt(sms_appcode::bytea, %s, 'aes'),'SQL_ASCII') as sms_appcode,
                try_out,
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
                oss_one_day,
                oss_one_size,
                oss_one_price,
                oss_two_day,
                oss_two_size,
                oss_two_price,
                oss_thr_day,
                oss_thr_size,
                oss_thr_price,
                invite_days,
	            pay_days,
                convert_from(decrypt(dbname::bytea, %s, 'aes'),'SQL_ASCII') as dbname,
                notices,
                memo,
                convert_from(decrypt(help_appid::bytea, %s, 'aes'),'SQL_ASCII') as help_appid,
	            convert_from(decrypt(help_secret::bytea, %s, 'aes'),'SQL_ASCII') as help_secret
            from toll_config where id=1
                """
            parm=[self.md5code,self.md5code,self.md5code,self.md5code,self.md5code,self.md5code,self.md5code,
                  self.md5code,self.md5code,self.md5code,self.md5code,self.md5code]
            l = self.db.fetch(sql,parm)
            return l
        else:
            sql = u"""
            select 
                a.id,
                a.usr_id,
                a.out_trade_no,
                a.ctype,
                a.price,
                to_char(a.pay_time,'YYYY-MM-DD HH24:MI'),
                a.cname,
                coalesce(to_char(a.utime,'YYYY-MM-DD HH24:MI'),to_char(a.ctime,'YYYY-MM-DD HH24:MI')),
                to_char(a.etime,'YYYY-MM-DD HH24:MI'),
                coalesce(pay_status,0) 
                from   pingtai_paylog a 
                order by a.id desc limit 100;
                    """
            L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo)
            PL = [pageNo, iTotal_Page, iTotal_length, select_size]
            return PL, L


    
    def local_add_save(self):

        dR = {'code': '', 'MSG': '保存成功'}

        mchid = self.GP('mchid', '')  # 微信公众号id
        mchkey = self.GP('mchkey', '')  # 微信公众号
        wx_token = self.GP('wx_token', '')  # 微信公众号id
        wx_aeskey = self.GP('wx_aeskey', '')  # 微信公众号
        wx_appid = self.GP('wx_appid', '')  # 微信公众号id
        wx_secret = self.GP('wx_secret', '')  # 微信公众号

        callback_url = self.GP('callback_url', '')  # 微信支付回调域名
        applet_url=self.GP('applet_url','')
        sms_appid = self.GP('sms_appid', '')  # 短信AppSecret
        sms_appkey = self.GP('sms_appkey', '')  # 短信AppSecret
        sms_appcode = self.GP('sms_appcode', '')  # 短信AppCode
        try_out = self.GP('try_out', '')  # 试用期(天)
        combo_one_name = self.GP('combo_one_name', '')  #套餐1名称
        combo_one_price = self.GP('combo_one_price', '')  #套餐1价格
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

        oss_one_day = self.GP('oss_one_day', '')  # 七牛access_key
        oss_one_size = self.GP('oss_one_size', '')  # 七牛secret_key
        oss_one_price = self.GP('oss_one_price', '')  # 七牛bucket
        oss_two_day = self.GP('oss_two_day', '')  # 七牛qiniu_domain
        oss_two_size = self.GP('oss_two_size', '')  # 七牛access_key
        oss_two_price = self.GP('oss_two_price', '')  # 七牛secret_key
        oss_thr_day = self.GP('oss_thr_day', '')  # 七牛bucket
        oss_thr_size = self.GP('oss_thr_size', '')  # 七牛qiniu_domain
        oss_thr_price = self.GP('oss_thr_price', '')  # 七牛access_key


        invite_days = self.GP('invite_days', '')  # 邀请码增加天数
        pay_days = self.GP('pay_days', '')  # 付费增加天数
        dbname = self.GP('dbname', '')  # 备份数据库名
        notices = self.GP('notices', '')  # 顶部消息
        memo = self.GP('memo', '')  # 滚动消息
        help_appid = self.GP('help_appid', '')  # 商家助手appid
        help_secret = self.GP('help_secret', '')  # 商家助手


        cur_random_no = "%s%s" % (time.time(), random.random())
        data = {

           # 'wx_appid': wx_appid,
           # 'wx_secret':wx_secret,
            #'mchid':mchid,
            #'mckey':mchkey,
            'callback_url': callback_url,
            'applet_url':applet_url,
            # 'sms_appid': sms_appid,
            # 'sms_appkey':sms_appkey,
            # 'sms_appcode': sms_appcode,
            'try_out': try_out or None,
            'combo_one_name': combo_one_name,
            'combo_one_price': combo_one_price or None,
            'combo_one_day': combo_one_day or None,
            'combo_two_name': combo_two_name,
            'combo_two_price': combo_two_price or None,
            'combo_two_day': combo_two_day or None,
            'combo_two_status': combo_two_status or None,
            'combo_thr_name': combo_thr_name,
            'combo_thr_price': combo_thr_price or None,
            'combo_thr_day': combo_thr_day or None,
            'combo_thr_status': combo_thr_status or None,
            'oss_one_day': oss_one_day or None,
            'oss_one_size': oss_one_size or None,
            'oss_one_price': oss_one_price or None,
            'oss_two_day': oss_two_day or None,
            'oss_two_size': oss_two_size or None,
            'oss_two_price': oss_two_price or None,
            'oss_thr_day': oss_thr_day or None,
            'oss_thr_size': oss_thr_size or None,
            'oss_thr_price': oss_thr_price or None,

            'invite_days':invite_days or None,
            'pay_days': pay_days or None,
            'utime': self.getToday(9),
            'combo_one_txt': combo_one_txt,
            'combo_two_txt': combo_two_txt,
            'combo_thr_txt': combo_thr_txt,
            #'dbname': dbname,
            'notices': notices,
            'memo': memo,
            # 'help_appid': help_appid,
            # 'help_secret': help_secret,
        }  # pt_conf
        sql="select id from toll_config"
        l,t=self.db.select(sql)
        if t==0:
            data['random_no']= cur_random_no
            self.db.insert('toll_config', data)
            tid = self.db.fetchcolumn('select id from toll_config where random_no=%s', cur_random_no)
            sqlu = """
               update toll_config set wx_appid=encrypt(%s,%s,'aes'),wx_secret=encrypt(%s,%s,'aes'),
               wx_token=encrypt(%s,%s,'aes'),wx_aeskey=encrypt(%s,%s,'aes'),
               mchid=encrypt(%s,%s,'aes'),mchkey=encrypt(%s,%s,'aes'),dbname=encrypt(%s,%s,'aes'),
               help_appid=encrypt(%s,%s,'aes'),help_secret=encrypt(%s,%s,'aes'),
               sms_appid=encrypt(%s,%s,'aes'),sms_appkey=encrypt(%s,%s,'aes'),
               sms_appcode=encrypt(%s,%s,'aes') where id=%s;
               """
            Lu = [wx_appid, self.md5code,wx_secret, self.md5code,
                  wx_token, self.md5code, wx_aeskey, self.md5code,
                  mchid, self.md5code,mchkey, self.md5code,dbname, self.md5code,
                  help_appid, self.md5code,help_secret, self.md5code,
                  sms_appid, self.md5code, sms_appkey, self.md5code,
                  sms_appcode, self.md5code, tid]
            self.db.query(sqlu, Lu)
            self.oTOLL.update()
            dR['code'] = '0'
            return dR

        id=l[0][0]
        self.db.update('toll_config', data, "id=%s" %id)
        sqlu = """
               update toll_config set wx_appid=encrypt(%s,%s,'aes'),wx_secret=encrypt(%s,%s,'aes'),
               wx_token=encrypt(%s,%s,'aes'),wx_aeskey=encrypt(%s,%s,'aes'),
               mchid=encrypt(%s,%s,'aes'),mchkey=encrypt(%s,%s,'aes'),dbname=encrypt(%s,%s,'aes'),
               help_appid=encrypt(%s,%s,'aes'),help_secret=encrypt(%s,%s,'aes'),
               sms_appid=encrypt(%s,%s,'aes'),sms_appkey=encrypt(%s,%s,'aes'),
               sms_appcode=encrypt(%s,%s,'aes') where id=%s;
                       """
        Lu = [wx_appid, self.md5code, wx_secret, self.md5code,
              wx_token, self.md5code, wx_aeskey, self.md5code,
              mchid, self.md5code, mchkey, self.md5code, dbname, self.md5code,
              help_appid, self.md5code, help_secret, self.md5code,
              sms_appid, self.md5code, sms_appkey, self.md5code,
              sms_appcode, self.md5code,id]
        self.db.query(sqlu, Lu)
        self.oTOLL.update()
        # if domain_url != '':
        #     self.oMALL.loaddata()
        dR['code'] = '0'
        dR['MSG'] = '修改成功'
        return dR
        # 更新数据缓存


    def Search_data(self):

        dR={'code':'','MSG':'查询成功'}
        uid=self.GP('uid','')
        if uid=='':
            dR['MSG']='查询数据用误'
            return dR

        sql="select out_trade_no,usr_id,days,ctype from pingtai_paylog  where id=%s"
        l,t=self.db.select(sql,[uid])
        if t==0:
            dR['MSG'] = '查询数据不存在'
            return dR
        out_trade_no, usr_id,days,ctype=l[0]
        import datetime
        from basic.pay import WeixinPay
        app_id = self.oTOLL['wx_appid']
        wechat_pay_id = self.oTOLL['mchid']
        wechat_pay_secret = self.oTOLL['mchkey']
        base_url = self.oTOLL['callback_url']
        notify_url = base_url + '/vipnotify'

        wxpay = WeixinPay(app_id, wechat_pay_id, wechat_pay_secret, notify_url)
        data = {
            'out_trade_no': out_trade_no,  # 商户订单号
        }
        raw = wxpay.order_query(**data)
        if raw.get('trade_state') == 'SUCCESS':
            transaction_id = raw['transaction_id']
            openid = raw['openid']
            sql = "update pingtai_paylog set openid=%s,transaction_id=%s,pay_status=1,pay_time=now() where id=%s"
            self.db.query(sql, [openid, transaction_id, uid])

            if ctype in (1, 2, 3):
                sqlu = """select to_char(expire_time,'YYYY-MM-DD HH24:MI'),
                        to_char(now(),'YYYY-MM-DD HH24:MI'),
                        case when to_char(expire_time,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
                        then 1 else 0 end,coalesce(inviteid,1) from users  where usr_id=%s"""
                lT, iN = self.db.select(sqlu, [usr_id])
                if iN > 0:
                    time_1, time_2, flag,inviteid = lT[0]
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
                    sql = "update pingtai_paylog set etime=%s where out_trade_no=%s"
                    self.db.query(sql, [e_time, out_trade_no])

                    pay_days = self.oTOLL.get('pay_days')
                    if inviteid != 1 and pay_days != 0:

                        sqlu = """select to_char(expire_time,'YYYY-MM-DD HH24:MI'),
                            to_char(now(),'YYYY-MM-DD HH24:MI'),
                            case when to_char(expire_time,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
                            then 1 else 0 end from users  where usr_id=%s"""
                        lT, iN = self.db.select(sqlu, [inviteid])
                        if iN > 0:
                            time1, time2, flag_ = lT[0]
                            if flag_ == 1:
                                expiretime = time1
                            else:
                                expiretime = time2
                            now = datetime.datetime.strptime(expiretime, "%Y-%m-%d %H:%M")
                            delta = datetime.timedelta(days=pay_days)
                            n_days = now + delta
                            etime = n_days.strftime('%Y-%m-%d %H:%M:%S')
                            sql = "update users set expire_time=%s,expire_flag=0 where usr_id=%s"
                            self.db.query(sql, [etime, inviteid])
                            isql = """insert into invite_log(ctype,return_id,usr_id,openid,return_days,return_time,ctime)
                                       values(2,%s,%s,%s,%s,%s,now())"""
                            iparm = [inviteid, usr_id, openid, pay_days, etime]
                            self.db.query(isql, iparm)
                    sqlr = "select id,role_id from usr_role where usr_id=%s"
                    lr, tr = self.db.select(sqlr, [usr_id])
                    if tr == 1:
                        urid, role_id = lr[0]  # role_id 2基础，3营销
                        if ctype == 1 and role_id != 2:  # 基础
                            self.db.query("update usr_role set role_id=2 where id=%s", [urid])
                        elif ctype == 2 and role_id != 3:  # 营销
                            self.db.query("update usr_role set role_id=3 where id=%s", [urid])
                        elif ctype == 3:  # 未知
                            pass

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
                sql = "update pingtai_paylog set etime=%s,utime=now() where out_trade_no=%s"
                self.db.query(sql, [e_time, out_trade_no])

            dR['code'] = '0'
            dR['MSG'] = '查询到已支付，已对数据进行更新。'
            return dR
        dR['MSG'] ='trade_state_desc'
        return dR






