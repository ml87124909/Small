# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
import random
import time
import datetime
from basic.publicw import db,oTOLL,md5code
from wechatpy.utils import check_signature
from wechatpy import parse_message, create_reply

class cweixin:

    def __init__(self, request):

        self.objHandle = request
        if request.method == 'POST':
            self.REQUEST = request.form
        else:
            self.REQUEST = request.args
        self.RQ = request.values
        self.db = db
        self.oTOLL=oTOLL.get()
        self.md5code=md5code
        # *****************************************************************

    def Webpage(self):

        self.TOKEN = self.oTOLL.get('wx_token','')
        self.AES_KEY = self.oTOLL.get('wx_aeskey', '')
        self.APPID = self.oTOLL.get('wx_appid', '')

        signature = self.objHandle.args.get('signature', '')
        timestamp = self.objHandle.args.get('timestamp', '')
        nonce = self.objHandle.args.get('nonce', '')
        encrypt_type = self.objHandle.args.get('encrypt_type', 'raw')
        msg_signature = self.objHandle.args.get('msg_signature', '')
        open_id = self.objHandle.args.get('openid', '')

        try:
            check_signature(self.TOKEN, signature, timestamp, nonce)
        except Exception as e:
            self.wx_log('验证失败:%s'%open_id, '%s' % e)
            if encrypt_type == 'raw':
                msg = parse_message(self.objHandle.data)
                reply=create_reply('该公众号服务器故障，请休息一会再试', msg)
                return reply.render()
            return ''

        if self.objHandle.method == 'GET':
            echo_str = self.objHandle.args.get('echostr', '')
            return echo_str
        #self.wx_log('恭恭敬敬恭恭敬敬', 'aaaaaaaaaaaaaaaa')
        # POST request
        if encrypt_type == 'raw':
            # plaintext mode
            msg = parse_message(self.objHandle.data)
            if msg.type == 'text':
                reply = create_reply(msg.content, msg)
            elif msg.type == 'event':
                if msg.event =='scan' or msg.event=='subscribe_scan':
                    if msg.scene_id == 'login_code' or msg.scene_id == 'register_code':
                        MSG = self.wx_code_msg(open_id)
                        reply = create_reply(MSG, msg)
                    else:
                        reply = create_reply('未知事件', msg)
                else:
                    reply = create_reply('login_code666666', msg)
            else:
                reply = create_reply('Sorry, can not handle this for now', msg)
            return reply.render()
        else:

            # encryption mode
            from wechatpy.crypto import WeChatCrypto
            crypto = WeChatCrypto(self.TOKEN, self.AES_KEY, self.APPID)
            try:
                msg = crypto.decrypt_message(
                    self.objHandle.data,
                    msg_signature,
                    timestamp,
                    nonce
                )
            except Exception as e:
                self.wx_log('消息解密失败:%s' % open_id, '%s' % e)
            else:
                msg = parse_message(msg)
                if msg.type == 'text':
                    reply = create_reply(msg.content, msg)
                elif msg.type == 'event':
                    if msg.event == 'scan' or msg.event == 'subscribe_scan':
                        if msg.scene_id == 'login_code' or msg.scene_id == 'register_code':
                            MSG = self.wx_code_msg(open_id)
                            reply = create_reply(MSG, msg)
                        else:
                            reply = create_reply('未知事件', msg)
                    else:
                        reply = create_reply('login_code666666', msg)
                else:
                    reply = create_reply('Sorry, can not handle this for now11111111', msg)
                return crypto.encrypt_message(reply.render(), nonce, timestamp)


    def wx_code_msg(self,openid):


        sql = "select usr_id from users where wx_openid=%s"
        l, t = self.db.select(sql, [openid])
        if t==0:
            try:
                try_out = int(self.oTOLL.get('try_out'))
            except:
                try_out = 30

            now = datetime.datetime.now()
            delta = datetime.timedelta(days=try_out)
            n_days = now + delta
            expire_time = n_days.strftime('%Y-%m-%d %H:%M:%S')
            random_no = "%s%s" % (time.time(), random.random())
            sql = """insert into users(login_id,status,ctime,expire_time,random_no,wx_openid)
                    values(encrypt(%s,%s,'aes'),1,now(),%s,%s,%s)"""
            parm = ['', self.md5code, expire_time,random_no, openid]
            self.db.query(sql, parm)

            ll, tt = self.db.select('select usr_id from users where random_no=%s', random_no)
            if tt == 0:
                return '数据有误，请联系管理员'
            usr_id = ll[0][0]
            sqlu = """
                update users set dept_id=%s where usr_id=%s;
                insert into usr_role (usr_id ,role_id,usr_name ,dept_id,cid ,ctime) 
                values (%s,2 ,%s,%s,0 ,now())"""
            parmu = [usr_id, usr_id, usr_id, openid, usr_id]
            self.db.query(sqlu, parmu)


        sql = """
            select id from wx_msg 
            where coalesce(state,0)=0  and openid=%s
            and to_char(end_time,'YYYY-MM-DD HH24:MI') >to_char(now(),'YYYY-MM-DD HH24:MI')
        """
        l, t = self.db.select(sql, [openid])
        if t > 0:
            return '您上一次的验证码还在有效期内!'

        passwd = ' '.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)).replace(" ", "")
        sql = """
                insert into wx_msg (openid,passwd,state,ctime,end_time)
                values(%s,%s,0,now(),now() + interval '10 minute')
                """
        self.db.query(sql, [openid, passwd])

        return '您的验证码是%s ，10分钟内有效!' % passwd

    def wx_log(self,openid, errors):
        sql = "insert into wxerror(openid,errcontent,ctime)values(%s,%s,now())"
        self.db.query(sql, [openid, errors])
        return




















