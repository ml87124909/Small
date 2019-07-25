# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
import hashlib
import datetime
from lxml import etree
from basic.publicw import db,oTOLL

class cVipPay:

    def __init__(self, request):

        self.objHandle = request
        self.db = db
        self.oTOLL = oTOLL.get()

    def Webpage(self):
        try:
            data = self.to_dict(self.objHandle.data)
            self.print_log('222222222222222222222', '%s' % data)
            if not self.check(data):
                #self.print_log('222222222222222222222', '%s' % data)
                return self.reply("签名验证失败", False)
            # 处理业务逻辑
            out_trade_no = data['out_trade_no']
            transaction_id = data['transaction_id']
            openid = data['openid']
            sql = """select id,usr_id,days,ctype from pingtai_paylog 
                where out_trade_no=%s and coalesce(pay_status,0)=0"""
            l, t = self.db.select(sql, [out_trade_no])
            if t == 0:
                #self.print_log('222222222222222222222', '数据不存在')
                return self.reply("数据不存在", False)
            pid,usr_id, days, ctype = l[0]

            sql = "update pingtai_paylog set openid=%s,transaction_id=%s,pay_status=1,pay_time=now() where id=%s"
            self.db.query(sql, [openid,transaction_id, pid])

            if ctype in (1, 2, 3):#基础，营销，未知
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
                    if inviteid!=1 and pay_days!=0:

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
                    sqlr="select id,role_id from usr_role where usr_id=%s"
                    lr,tr=self.db.select(sqlr,[usr_id])
                    if tr==1:
                        urid,role_id=lr[0]#role_id 2基础，3营销
                        if ctype==1 and role_id!=2:#基础
                            self.db.query("update usr_role set role_id=2 where id=%s",[urid])
                        elif ctype==2 and role_id!=3:#营销
                            self.db.query("update usr_role set role_id=3 where id=%s",[urid])
                        elif ctype == 3:#未知
                            pass


                return self.reply("OK", True)
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
                sql = "update users set oss_time=%s,oss_flag=%s,oss_all=coalesce(oss_all,100)+%s where usr_id=%s"
                self.db.query(sql, [e_time, ctype, size, usr_id])
                sql = "update pingtai_paylog set etime=%s,utime=now() where out_trade_no=%s"
                self.db.query(sql, [e_time, out_trade_no])
            return self.reply("OK", True)
            #
            #
            # sqlu = """select to_char(expire_time,'YYYY-MM-DD HH24:MI'),
            #                     to_char(now(),'YYYY-MM-DD HH24:MI'),
            #                     case when to_char(expire_time,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI')
            #                     then 1 else 0 end from users  where usr_id=%s"""
            # lT, iN = self.db.select(sqlu, [usr_id])
            # if iN > 0:
            #     time_1, time_2, flag = lT[0]
            #     if flag == 1:
            #         expire_time = time_1
            #     else:
            #         expire_time = time_2
            #     now = datetime.datetime.strptime(expire_time, "%Y-%m-%d %H:%M")
            #     delta = datetime.timedelta(days=days)
            #     n_days = now + delta
            #     e_time = n_days.strftime('%Y-%m-%d %H:%M:%S')
            #     sql = "update users set expire_time=%s,vip_flag=%s,expire_flag=0 where usr_id=%s"
            #     self.db.query(sql, [e_time, ctype, usr_id])
            #
            #     sql = "update pingtai_paylog set etime=%s where id=%s"
            #     self.db.query(sql, [e_time, pid])
            #
            #return self.reply("OK", True)
        except Exception as e:
            self.print_log('平台vip支付回调错误','%s'%e)

    def dict_to_xml(self,dict_data):
        '''
        dict to xml
        :param dict_data:
        :return:
        '''
        xml = ["<xml>"]
        for k, v in dict_data.items():
            xml.append("<{0}>{1}</{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(self,xml_data):
        '''
        xml to dict
        :param xml_data:
        :return:
        '''
        xml_dict = {}
        root = ET.fromstring(xml_data)
        for child in root:
            xml_dict[child.tag] = child.text
        return xml_dict


    def to_dict(self, content):
        raw = {}
        root = etree.fromstring(content,parser=etree.XMLParser(resolve_entities=False))
        for child in root:
            raw[child.tag] = child.text
        return raw

    def to_xml(self, raw):
        s = ""
        for k, v in raw.items():
            s += "<{0}>{1}</{0}>".format(k, v)
        s = "<xml>{0}</xml>".format(s)
        return s.encode("utf-8")

    def sign(self, raw):
        wechat_pay_secret = self.oTOLL['mchkey']
        raw = [(k, str(raw[k]) if isinstance(raw[k], int) else raw[k])
               for k in sorted(raw.keys())]
        s = "&".join("=".join(kv) for kv in raw if kv[1])
        s += "&key={0}".format(wechat_pay_secret)
        return hashlib.md5(s.encode("utf-8")).hexdigest().upper()

    def check(self, data):
        sign = data.pop("sign")
        return sign == self.sign(data)

    def reply(self, msg, ok=True):
        code = "SUCCESS" if ok else "FAIL"
        return self.to_xml(dict(return_code=code, return_msg=msg))

    def print_log(self,cname, errors):
        sql = "insert into print_log(cname,errors,ctime)values(%s,%s,now())"
        self.db.query(sql, [cname, errors])
        return




















