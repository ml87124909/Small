# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""manage/vi/login.py"""

from imp import reload
from basic.publicw import DEBUG,user_menu
if DEBUG == '1':
    import manage.vi.VI_BASE
    reload(manage.vi.VI_BASE)
from manage.vi.VI_BASE             import cVI_BASE
import time, random, datetime
from flask import make_response,redirect

class clogin(cVI_BASE):

    def setClassName(self):
        self.dl_name = ''

    def goPartList(self):

        return self.runApp('login.html')
    
    def goPartDologin(self):
        dR={'code':'1','MSG':''}
        login_id = self.dl.GP('inputname','')
        password = self.dl.GP('inputPassword','')
        try:
            login_ip = self.objHandle.headers["X-Real-IP"]
        except:
            login_ip = self.objHandle.remote_addr

        if login_id =='' or password=='':
            dR['MSG']='用户名或密码不能为空'
            return self.jsons(dR)

        lT = self.dl.login(login_id,password)

        if lT:
            usr_id=lT[0][0]
            login_lock=lT[0][3]
            if str(login_lock) == '1':
                dR['MSG'] = '您的帐号已被锁定，请联系管理员!'
                return self.jsons(dR)

            result = self.dl.cookie.isetcookie("__session" , usr_id)
            
            self.dl.checkuser(usr_id)
            menu1,menu2,menu3 = self.dl.getSysMenu(usr_id)
            if usr_id in user_menu:
                user_menu[usr_id] = {
                    'menu1':menu1,'menu2':menu2,'menu3':menu3
                }
            else:
                user_menu.update( {usr_id:{
                    'menu1':menu1,'menu2':menu2,'menu3':menu3
                }} )

            sql="UPDATE users SET  last_login=%s,last_ip=%s WHERE usr_id=%s"
            self.dl.db.query(sql,[self.dl.getToday(7),login_ip,usr_id])

            self.login_log(login_status='成功', usr_id=usr_id, login_id=login_id, login_type='PC',login_ip=login_ip)
            dR['MSG'] = '登录成功！'
            dR['code']='0'
        else:

            self.login_log(login_status= '失败', usr_id='0', login_id=login_id, login_type='PC',login_ip=login_ip)
            dR['MSG'] = '用户名或密码错误！'
        return self.jsons(dR)


    # 登录时插入数据库表login_log的函数
    def login_log(self, login_status='', usr_id='0', login_id='', login_type='PC',login_ip=''):

        HTTP_USER_AGENT = self.objHandle.environ['HTTP_USER_AGENT']

        login_id = login_id.replace("'", "")
        if len(login_id) > 18: login_id = 'XXXXXX'
        sql = """insert into login_log(login_id,usr_id,login_ip,http_user_agent,login_type,login_status,ctime,status)
               values(%s,%s,%s,%s,%s,%s,now(),0)
            """
        self.dl.db.query(sql,[login_id, usr_id, login_ip, HTTP_USER_AGENT, login_type, login_status])
        if login_status == '失败':  # 登录失败失败超过5次，锁住账号
            sql = """select COUNT(*) from login_log 
                    where login_id=%s and status=0 
                    and to_char(ctime,'YYYY-MM-DD HH:24-MI')>to_char(now(),'YYYY-MM-DD') and login_status='失败'
            """
            lT, iN = self.dl.db.select(sql,login_id)
            if lT[0][0] >= 5:
                sql = "update users set login_lock=1,login_lock_time=now() where login_id=%s"
                self.dl.db.query(sql,login_id)
                sql2 = "update login_log set status=1 where login_id=%s"
                self.dl.db.query(sql2,login_id)


    def goPartLogout(self):
        self.dl.cookie.clearcookie('__session')
        response = make_response(redirect("manage?viewid=login"))
        self.dl.cookie.responeCookie(response)
        return response

    def goPartRegister(self):

        aaa = self.dl.get_QR_code_url('register_code')
        self.assign('aaa', aaa)
        return self.runApp('register.html')

    def goPartReg_Save(self):
        dR={'code':'1','MSG':''}
        qrcode = self.dl.GP('qrcode', '')
        inviteid = self.dl.GP('inviteid', '')

        if qrcode=='':
            dR['MSG']='微信验证码有误!'
            return self.jsons(dR)

        sql = """
            select id,openid from wx_msg
            where coalesce(state,0)=0 and  passwd=%s
            and to_char(end_time,'YYYY-MM-DD HH24:MI') >to_char(now(),'YYYY-MM-DD HH24:MI')
            order by id desc limit 1;
                                        """
        lT, iN = self.dl.db.select(sql, [qrcode])
        if iN==0:
            dR['MSG'] = '微信验证码有误!'
            return self.jsons(dR)

        sid, openid = lT[0]
        self.dl.db.query("update wx_msg set state=1,utime=now() where id=%s", sid)
        sql = "select usr_id from users where wx_openid=%s"
        l, t = self.dl.db.select(sql, [openid])
        if t>0:
            dR['MSG'] = '您已注册，请到登录页面扫码登录!'
            return self.jsons(dR)
        invite_id=1
        e_time=''
        try:
            inviteid = int(inviteid)
            invite_days = int(self.dl.oTOLL.get('invite_days', 0))
            sqli = """select to_char(expire_time,'YYYY-MM-DD HH24:MI'),
                    to_char(now(),'YYYY-MM-DD HH24:MI'),
                    case when to_char(expire_time,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
                    then 1 else 0 end 
                    from users where  usr_id=%s"""
            lT1, iN1 = self.dl.db.select(sqli, [inviteid])
            if iN1 > 0:
                time_1, time_2, flag = lT1[0]
                if flag == 1:
                    expiretime = time_1
                else:
                    expiretime = time_2
                now = datetime.datetime.strptime(expiretime, "%Y-%m-%d %H:%M")
                delta = datetime.timedelta(days=invite_days)
                n_days = now + delta
                e_time = n_days.strftime('%Y-%m-%d %H:%M:%S')
                invite_id=inviteid

        except:
            invite_days=0
            inviteid=None

        try:
            try_out = int(self.dl.oTOLL.get('try_out'))
        except:
            try_out = 30
        try_all=invite_days+try_out
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=try_all)
        n_days = now + delta
        expire_time = n_days.strftime('%Y-%m-%d %H:%M:%S')
        random_no="%s%s" % (time.time(), random.random())
        sql = """insert into users(login_id,status,ctime,expire_time,inviteid,random_no,wx_openid)
                values(encrypt(%s,%s,'aes'),1,now(),%s,%s,%s,%s)"""
        parm = ['',self.dl.md5code,expire_time,inviteid or None,random_no,openid]
        self.dl.db.query(sql,parm)

        ll,tt=self.dl.db.select('select usr_id from users where random_no=%s',random_no)
        if tt==0:
            dR['MSG'] = '注册失败了，请重新注册!'
            return self.jsons(dR)
        usr_id=ll[0][0]
        sqlu= """
                update users set dept_id=%s where usr_id=%s;
                insert into usr_role (usr_id ,role_id,usr_name ,dept_id,cid ,ctime) 
                values (%s,2 ,%s,%s,0 ,now())"""
        parmu=[usr_id,usr_id,usr_id,openid,usr_id]
        self.dl.db.query(sqlu,parmu)
        if invite_id!=1 and e_time!='':
            sql = "update users set expire_time=%s,expire_flag=0 where usr_id=%s"
            self.dl.db.query(sql, [e_time, invite_id])
            isql="""insert into invite_log(ctype,return_id,usr_id,openid,return_days,return_time,ctime)
                        values(1,%s,%s,%s,%s,%s,now())"""
            iparm=[invite_id,usr_id,openid,invite_days,e_time]
            self.dl.db.query(isql,iparm)
        dR = {'code': '0', 'MSG': '注册成功,请返回登录页面进行登录'}
        return self.jsons(dR)


    def goPartQrlogin(self):
        dR = {'code': '0', 'MSG': '登录成功,跳转到首页'}
        qrcode = self.dl.GP('qrcode', '')

        if qrcode == '':
            dR = {'code': '1', 'MSG': '微信验证码不能为空'}
            return self.jsons(dR)

        try:
            login_ip = self.objHandle.headers["X-Real-IP"]
        except:
            login_ip = self.objHandle.remote_addr
        sql = """
            select id,openid from wx_msg
            where coalesce(state,0)=0 and  passwd=%s
            and to_char(end_time,'YYYY-MM-DD HH24:MI') >to_char(now(),'YYYY-MM-DD HH24:MI')
            order by id desc limit 1;
                                """
        lT, iN = self.dl.db.select(sql, [qrcode])
        if iN == 0:
            dR = {'code': '1', 'MSG': '微信验证码有误或超时'}
            return self.jsons(dR)
        sid, openid = lT[0]
        self.dl.db.query("update wx_msg set state=1,utime=now() where id=%s", sid)
        sql = """select usr_id,convert_from(decrypt(login_id::bytea,%s, 'aes'),'SQL_ASCII') 
            from users where wx_openid=%s"""
        l, t = self.dl.db.select(sql, [self.dl.md5code,openid])
        if t==0:#不存在需要注册
            dR = {'code': '1', 'MSG': '您还没有注册，请注册后再登录'}
            return self.jsons(dR)


        #已注册直接跳转
        usr_id,login_id = l[0]
        result = self.dl.cookie.isetcookie("__session", usr_id)

        self.dl.checkuser(usr_id)
        self.dl.oUSERS_OSS.update(usr_id)
        menu1, menu2, menu3 = self.dl.getSysMenu(usr_id)
        if usr_id in user_menu:
            user_menu[usr_id] = {
                'menu1': menu1, 'menu2': menu2, 'menu3': menu3
            }
        else:
            user_menu.update({usr_id: {
                'menu1': menu1, 'menu2': menu2, 'menu3': menu3
            }})

        sql = "UPDATE users SET  last_login=%s,last_ip=%s WHERE usr_id=%s"
        self.dl.db.query(sql, [self.dl.getToday(7), login_ip, usr_id])

        login_status = '成功'
        self.login_log(login_status=login_status, usr_id=usr_id, login_id=login_id, login_type='PC',
                       login_ip=login_ip)
        return self.jsons(dR)

    def goPartAccount(self):
        return self.runApp('login_manage.html')


