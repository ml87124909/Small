# -*- coding: utf-8 -*-

##############################################################################
#
#
#
##############################################################################
from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':    
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cH001_dl(cBASE_DL):
    #在子类中重新定义         
    def myInit(self):
        self.src = 'H001'
        pass

    def getInfo(self):
        sql="""
        select  convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII') as login_id 
        from users where usr_id = %s
        """
        info  =  self.db.fetch(sql ,[self.md5code,self.usr_id])
        return info

    def local_add_save(self):
        dR={'code':'','MSG':'保存成功'}
        login_id = self.GP('login_id','')
        oldpassword = self.GP('oldpassword','')
        password = self.GP('password','')
        password2 = self.GP('password2','')

        if login_id=='':
            dR['code'] = '1'
            dR['MSG'] = '登录名不能为空!'
            return dR

        sql="""
         select usr_id from users 
         where  convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII')=%s and usr_id!=%s
        """
        l,t=self.db.select(sql,[self.md5code,login_id,self.usr_id])
        if t>0:
            dR['code'] = '1'
            dR['MSG'] = '当前登录名已存在'
            return dR

        if password != '' :
            if password2 != password:
                dR['code'] = '1'
                dR['MSG'] = '确认密码必须和新密码相同'
                return dR
            sql = "select usr_id from users where usr_id = %s and coalesce(passwd,'') = %s;"
            l, t = self.db.select(sql, [self.usr_id, oldpassword])
            if t> 0:
                sql = "update users set login_id=encrypt(%s,%s,'aes'),password= crypt(%s, gen_salt('md5')) where usr_id=%s"
                parm = [login_id, self.md5code, password, self.usr_id]
                self.db.query(sql, parm)
                self.use_log('修改个人帐号%s' % self.usr_id)
                return dR

            sql="select usr_id from users where usr_id = %s and passwd = crypt(%s, password);"
            l,t=self.db.select(sql,[self.usr_id,oldpassword])
            if t==0:
                dR['code'] = '1'
                dR['MSG'] = '您的旧密码输入错误'
                return dR

            sql = "update users set login_id=encrypt(%s,%s,'aes'),password= crypt(%s, gen_salt('md5')) where usr_id=%s"
            parm=[login_id,self.md5code,password, self.usr_id]
            self.db.query(sql,parm)
            self.use_log('修改个人帐号%s' % self.usr_id)
            return dR

        sql = "update users set login_id=encrypt(%s,%s,'aes')  where usr_id=%s"
        parm = [login_id, self.md5code, self.usr_id]
        self.db.query(sql, parm)
        self.use_log('修改个人帐号%s' % self.usr_id)
        dR['MSG'] = '登录名保存成功'
        return dR

    def get_local_data(self):
        """获取 local 表单的数据
        """

        sql = u"""
        select 
            a.id,
            a.out_trade_no,
            a.ctype,
            a.price,
            to_char(a.pay_time,'YYYY-MM-DD HH24:MI'),
            a.cname,
            coalesce(to_char(a.utime,'YYYY-MM-DD HH24:MI'),to_char(a.ctime,'YYYY-MM-DD HH24:MI')),
            to_char(a.etime,'YYYY-MM-DD HH24:MI'),
            coalesce(pay_status,0)
            from   pingtai_paylog a 
            where a.usr_id=%s
            order by a.id desc limit 100;
                """%self.usr_id
        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L

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

