# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
"""sell/VI_BASE.py"""

import os,time,hashlib,base64,requests
from basic.publicw import DEBUG
from imp import reload

if DEBUG=='1':
    import sell.VIEWS
    reload(sell.VIEWS)
from sell.VIEWS            import cVIEWS

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatWxa
import json
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
class cVI_BASE(cVIEWS):


    def qiniu_Upload(self):

        file = self.objHandle.files['audio']  # request的files属性为请求中文件的数据<input 里的name="file">
        url = ''
        if file.filename.find('.') > 0:
            file_ext = file.filename.rsplit('.', 1)[1].strip().lower()

            timeStamp = time.time()
            md5name = hashlib.md5()
            md5name.update(str(timeStamp).encode('utf-8'))
            filename = md5name.hexdigest() + '.' + file_ext
            file.save(os.path.join(self.ATTACH_ROOT, filename))
            #url="static/data/%s"%filename
            url =filename
            #file = file.read()
            #url = self.qiniu_upload_file(file, filename)
        return url

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['bmp', 'png', 'jpg', 'jpeg', 'gif']



    def list_for_grid(self, List,iTotal_length, pageNo=1, select_size=10):

        if iTotal_length % select_size == 0:
            iTotal_Page = iTotal_length // select_size
        else:
            iTotal_Page = iTotal_length // select_size + 1

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
        mall=self.oMALL.get(self.usr_id_p)
        if mall=={}:
            return 0

        appid=mall['appid']
        secret =mall['secret']
        client = WeChatClient(appid, secret)
        wxa = WeChatWxa(client)
        return wxa

    def print_log(self,cname,errors):
        sql="insert into print_log(cname,errors,ctime)values(%s,%s,now())"
        self.db.query(sql,[cname,errors])
        return

    def write_order_log(self,order_id,edit_name='',edit_memo='',edit_remark=''):
        sql="""insert into wechat_mall_order_log(usr_id,order_id,edit_name,edit_memo,edit_remark,cid,ctime)
            values(%s,%s,%s,%s,%s,%s,now())
        """
        self.db.query(sql,[self.usr_id_p,order_id,edit_name,edit_memo,edit_remark,self.usr_id])
        return

    def user_log(self,uid,cname,memo):
        sql="insert into user_log(usr_id,wechat_user_id,cname,memo,ctime)values(%s,%s,%s,%s,now())"
        self.db.query(sql,[self.usr_id_p,uid,cname,memo])
        return

    def encrypt(self,d1,apikey):
        m = hashlib.md5()
        m.update((d1 + apikey).encode("utf8"))
        encodestr = m.hexdigest()
        requestdata = base64.b64encode(encodestr.encode(encoding='utf-8'))
        return requestdata

    def sendpost(self, post_data):
        """发送post请求"""
        url = 'http://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx'

        header = {
            "Accept": "application/x-www-form-urlencoded;charset=utf-8",
            "Accept-Encoding": "utf-8"
        }
        req = requests.post(url, post_data, headers=header)
        sort_data = json.loads(req.text)
        return sort_data


    def Save_pic_table(self, f_ext, f_size, filename, url,ctype,timestamp,ctype_str='',other_id=0):

        f_year = self.getToday(6)[:4]
        sql = """insert into images_api(usr_id,ctype,ctype_str,other_id,f_year,f_ext,f_size,cname,pic,cid,ctime,timestamp)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s)"""
        L = [self.usr_id_p,ctype or None, ctype_str,other_id or None,f_year, f_ext, f_size, filename, url, self.usr_id,timestamp]
        self.db.query(sql, L)


    # 登录时插入数据库表login_log的函数
    def login_log(self, login_status='', usr_id='0', login_id='', login_type='PC', login_ip=''):

        HTTP_USER_AGENT = self.objHandle.environ['HTTP_USER_AGENT']
        login_id = login_id.replace("'", "")
        sql = """insert into login_log(login_id,usr_id,login_ip,http_user_agent,login_type,login_status,ctime,status)
               values(%s,%s,%s,%s,%s,%s,now(),0)
            """
        self.db.query(sql, [login_id, usr_id, login_ip, HTTP_USER_AGENT, login_type, login_status])
        if login_status == '失败':  # 登录失败失败超过5次，锁住账号
            sql = """select COUNT(*) from login_log 
                    where login_id=%s and status=0 
                    and to_char(ctime,'YYYY-MM-DD HH:24-MI')>to_char(now(),'YYYY-MM-DD') and login_status='失败'
            """
            lT, iN = self.db.select(sql, login_id)
            if lT[0][0] >= 5:
                sql = "update users set login_lock=1,login_lock_time=now() where login_id=%s"
                self.db.query(sql, login_id)
                sql2 = "update login_log set status=1 where login_id=%s"
                self.db.query(sql2, login_id)

    def goPartGologin(self):
        login_id = self.GP('inputname', '')
        password = self.GP('inputPassword', '')
        code = self.REQUEST.get('code', '')
        if code == '' or code == 'None' or code == 'undefined':
            return self.jsons({'code': 300, 'data': {'msg': self.error_code[300].format('code')}})
        if login_id == '' or login_id == 'None' or login_id == 'undefined':
            return self.jsons({'code': 300, 'data': {'msg': self.error_code[300].format('inputname')}})
        if password == '' or password == 'None' or password == 'undefined':
            return self.jsons({'code': 300, 'data': {'msg': self.error_code[300].format('inputPassword')}})

        if self.app_id=='' or  self.secret=='':
            return self.jsons({'code': 404, 'msg': '请联系管理员到后台填写商家小程序设置'})

        session_info = self.wx_login(code)
        if session_info.get('errcode'):
            return self.jsons(
                {'code': 602, 'msg': '微信用户信息解密错误请检查appid和secret信息', 'data': session_info.get('errmsg')})
        open_id = session_info['openid']

        try:
            login_ip = self.objHandle.headers["X-Real-IP"]
        except:
            login_ip = self.objHandle.remote_addr
        lT = self.login(login_id, password)

        if lT:
            usr_id = lT[0][0]
            self.oUSERS.update(usr_id,open_id)
            self.oUSERS.update(open_id,usr_id)
            sql = """UPDATE users SET openid=%s,cookid=newid(),last_login=%s,last_ip=%s,use_count=use_count+1 WHERE usr_id=%s"""
            self.db.query(sql, [open_id,self.getToday(7), login_ip, usr_id])

            code = 0
            token = self.create_token(usr_id)
            self.login_log(login_status='成功', usr_id=usr_id, login_id=login_id, login_type='商家小程序',
                           login_ip=login_ip)

        else:
            self.login_log(login_status='失败', usr_id='0', login_id=login_id, login_type='商家小程序', login_ip=login_ip)
            code, token = 1, '000'

        return self.jsons({'code': code, 'malitoken': token})

    def goPartlogin(self):  #登录
        code = self.REQUEST.get('code', '')
        if code == '' or code == 'None' or code == 'undefined':
            return self.jsons({'code': 300, 'data': {'msg': self.error_code[300].format('code')}})

        if self.app_id=='' or  self.secret=='':
            return self.jsons({'code': 404, 'msg': '请联系管理员到后台填写商家小程序设置'})

        session_info = self.wx_login(code)
        if session_info.get('errcode'):
            return self.jsons(
                {'code': 602, 'msg': '微信用户信息解密错误请检查appid和secret信息', 'data': session_info.get('errmsg')})
        open_id = session_info['openid']
        try:
            login_ip = self.objHandle.headers["X-Real-IP"]
        except:
            login_ip = self.objHandle.remote_addr

        usr_id = self.oUSERS.get(open_id)
        if usr_id == '':
            return self.jsons({'code': 10000, 'msg': self.error_code[10000]})
        sql = """SELECT usr_id FROM users
                           WHERE  status=1 and COALESCE(del_flag,0) = 0 and COALESCE(expire_flag,0) = 0
                        """
        lT, iN = self.db.select(sql, [usr_id])
        if iN==0:
            return self.jsons({'code': 1, 'msg': '已过体验期，请付费使用！'})
        self.login_log(login_status='成功', usr_id=usr_id, login_id=open_id, login_type='商家小程序',
                       login_ip=login_ip)
        token = self.create_token(usr_id)
        return self.jsons({'code': 0, 'data': {'malitoken': token},'msg':self.error_code[0]})

    def wx_login(self,code):
        session_info = self.api.get_session_info(code=code)
        return session_info

    def order_shipment_send(self, wechat_user_id, form_id, order_num, shipment='', shipmentcode='',orderid=''):  # 订单发货通知模板消息
        # 订单号  发货时间，快递公司，物流单号
        wxa = self.get_wecthpy()
        if wxa == 0:
            return 1
        opid = self.oOPENID.get(int(wechat_user_id))

        if opid == '':
            return 1
        shop = self.oSHOP_T.get(self.usr_id_p)

        if shop == {}:
            return 1
        url = None
        tid = shop.get('send_id', '')  # 'M1VCMVmg6_Rz5ZCxBZpZGYsojOIfOxJt80Lo83OSzW8'
        if tid == '':
            return 1
        send_url = shop.get('send_url', '')
        if send_url != '':
            url = send_url.format(orderid=orderid)
        data = {"keyword1": {
            "value": "%s" % order_num
        }, "keyword2": {
            "value": "%s" % self.getToday(9)
        },
            "keyword3": {
                "value": "%s" % shipment
            },
            "keyword4": {
                "value": "%s" % shipmentcode
            }
        }
        a = wxa.send_template_message(opid, tid, data, form_id, page=url)
        return a

    def get_vip_type(self, wechat_user_id):

        l, t = self.db.select("select up_type,discount from member where usr_id=%s", self.usr_id_p)
        if t == 0:
            return 0, '0', '无', 1

        ctype, sale = l[0]

        sql = """
            select coalesce(hy_flag,0),coalesce(usr_level,0),
            case when to_char(hy_ctime,'YYYY-MM-DD HH24:MI')<to_char(now(),'YYYY-MM-DD HH24:MI') and to_char(hy_etime,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') then 1 else 0 end
            from wechat_mall_user where id=%s
        """
        l, t = self.db.select(sql, wechat_user_id)
        if t == 0:
            raise 0
        hy_flag, usr_level, hyt, = l[0]
        if str(ctype) == '1' and str(hy_flag) == '1':

            return 1, '0', '会员', sale / 100

        elif str(ctype) == '2' and str(usr_level) != '0':
            sql = "select id,cname,level_discount from hy_up_level where usr_id=%s and id=%s"
            lT, iN = self.db.select(sql, [self.usr_id_p, usr_level])
            if iN > 0:
                vip_level, vip_level_name, vip_sale = lT[0]
                return 1, vip_level, vip_level_name, vip_sale / 100
        return 0, '0', '无', 1  # vip_state, vip_level, vip_level_name, vip_sale
