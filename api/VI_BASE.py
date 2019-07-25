# -*- coding: utf-8 -*-

##############################################################################
#
#
#
#
##############################################################################
"""VI_BASE Module"""


import os, importlib, urllib, time, datetime, random, jwt, hashlib, base64, requests, oss2

from qiniu import Auth, put_stream, put_data,BucketManager

from basic.publicw import DEBUG

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatWxa
from basic.wxbase import wx_minapp_login,WXBizDataCrypt,WxPay
from werkzeug import secure_filename
import hashlib,time,json,datetime

from imp import reload


if DEBUG == '1':
    import api.VIEWS
    reload(api.VIEWS)
from api.VIEWS import cVIEWS
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

    def RQ(self, key, default=None, ctype=1):
        value = self.REQUEST.get(key, default)
        L_error = ['"', "'", '%', '#', '&', '*', '(', ')', '@', '`', '\\', ']', '=', '<', '>','?','/']
        if ctype==1 and value and isinstance(value, str):
            for c in L_error:
                if c in value:
                    value=value.replace(c,'')
        return value

    def create_token(self,usr_id,open_id,wechat_user_id):

        payloads = {


            "usr_id": usr_id,
            "open_id": open_id,
            "wechat_user_id":wechat_user_id,

        }
        encoded_jwt = jwt.encode(payloads, 'janedao', algorithm='HS256')
        token = encoded_jwt.decode('utf-8')
        return token

    def check_token(self,token):
        dR = {'MSG': '', 'code': '','open_id':'','wechat_user_id':''}

        try:
            payload = jwt.decode(token, 'janedao', algorithms=['HS256'])
        except:
            dR['code'] = 1
            dR['MSG'] = 'token无效,解密失败'
            return dR

        if not payload:
            dR['code'] = 1
            dR['MSG'] = 'token无法解密a'
            return dR

        if payload["usr_id"]!=self.subusr_id:
            dR['code'] = 1
            dR['MSG'] = 'token无法解密c'
            return dR

        dR['open_id']=payload['open_id']
        dR['wechat_user_id']=payload['wechat_user_id']

        dR['code'] = 0
        return dR

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

    def qiniu_upload_file(self, source_file, filename):

        # bucket_name 是存储空间列表名,domain_prefix是外链默认域名链接
        # 构建鉴权对象
        if self.qiniu_access_key=='':
            q = Auth(self.qiniu_access_key_all, self.qiniu_secret_key_all)
            token = q.upload_token(self.qiniu_bucket_name_all, filename)
            domain_prefix=self.qiniu_domain_all
        else:
            q = Auth(self.qiniu_access_key, self.qiniu_secret_key)
            token = q.upload_token(self.qiniu_bucket_name, filename)
            domain_prefix = self.qiniu_domain

        ret, info = put_data(token, filename, source_file)
        if info.status_code == 200:
            return domain_prefix + filename
        return None


    def ali_upload_file(self, source_file, filename):

        domain_prefix = self.qiniu_domain_all
        # endpoint = 'http://oss-cn-shenzhen.aliyuncs.com'  # 你的Bucket处于的区域
        auth = oss2.Auth(self.qiniu_access_key_all, self.qiniu_secret_key_all)
        bucket = oss2.Bucket(auth, self.endpoint, self.qiniu_bucket_name_all)
        # result = bucket.put_object(filename, source_file)  # 上传
        # if result.status == 200:
        #     return domain_prefix + filename
        new_filename = '%s/' % self.subusr_id + filename
        result = bucket.put_object(new_filename, source_file)  # 上传
        if result.status == 200:
            return domain_prefix + new_filename

        return None

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
        client = WeChatClient(appid, secret)
        wxa = WeChatWxa(client)
        return wxa

    def update_my_coupons(self):
        pass

    def print_log(self,cname,errors):
        sql="insert into print_log(cname,errors,ctime)values(%s,%s,now())"
        self.db.query(sql,[cname,errors])
        return

    def write_order_log(self,order_id,edit_name='',edit_memo='',edit_remark=''):
        sql="""insert into wechat_mall_order_log(usr_id,order_id,edit_name,edit_memo,edit_remark,cid,ctime)
            values(%s,%s,%s,%s,%s,%s,now())
        """
        self.db.query(sql,[self.subusr_id,order_id,edit_name,edit_memo,edit_remark,self.subusr_id])
        return

    def user_log(self,uid,cname,memo):
        sql="insert into user_log(usr_id,wechat_user_id,cname,memo,ctime)values(%s,%s,%s,%s,now())"
        self.db.query(sql,[self.subusr_id,uid,cname,memo])
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

    def order_refund(self,order_id,order_num,wechat_user_id):

        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]
        re_num = 'R' + danhao[2:] + romcode
        mall = self.oMALL.get(self.subusr_id)

        app_id = mall.get('appid','')
        secret = mall.get('secret','')
        wx_mch_id = mall.get('mchid','')
        wx_mch_key = mall.get('mchkey','')
        base_url = mall.get('base_url','')#'https://malishop.janedao.cn'
        api_cert_path = mall.get('cert','')
        api_key_path =mall.get('key','')

        notify_url = base_url + '/refund/%s/notify' % self.subusr_id
        wxpay = WxPay(app_id, wx_mch_id, wx_mch_key, notify_url)


        sql="select total_fee from wechat_mall_payment where order_id=%s and payment_number=%s and usr_id=%s "
        l,t=self.db.select(sql,[order_id,order_num,self.subusr_id])
        if t==0:
            return 1
        total_fee=l[0][0]
        data = {  # 退款信息
            'out_trade_no': order_num,  # 商户订单号
            'total_fee': total_fee,  # 订单金额
            'refund_fee': total_fee  # 退款金额
        }
        sql = "select out_refund_no from wechat_mall_refund where out_trade_no=%s and usr_id=%s"
        lT, iN = self.db.select(sql, [order_num, self.subusr_id])
        if iN==0:
            data['out_refund_no']=re_num  # 商户退款单号
            refund = {  # 退款信息
                'out_trade_no': order_num,  # 商户订单号
                'total_fee': total_fee,  # 订单金额
                'refund_fee': total_fee,  # 退款金额
                'out_refund_no':re_num,
                'usr_id':self.subusr_id,
                'wechat_user_id':wechat_user_id
            }

            self.db.insert('wechat_mall_refund',refund)
            data['notify_url'] = notify_url  # 商户退款回调
            raw=wxpay.refund(api_cert_path,api_key_path,**data)

            if raw['return_code'] == 'SUCCESS' and raw['result_code']  == 'SUCCESS':

                try:
                    sql="select id from wechat_mall_refund where out_trade_no=%s and out_refund_no=%s and total_fee=%s and usr_id=%s"
                    l,i=self.db.select(sql,[raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],self.subusr_id])
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

                    self.db.update("wechat_mall_refund", refund, "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" %(raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],self.subusr_id))

                    sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                values(%s,%s,%s,%s,%s,now())
                            """
                    self.db.query(sql, [self.subusr_id,'wechat_mall_refund',"out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" %(raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],self.subusr_id),
                                        '退款回调更新wechat_mall_refund表数据',self.subusr_id])
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
                    self.db.update("wechat_mall_refund", datas, "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" %(raw['out_trade_no'],raw['out_refund_no'],raw['total_fee'],self.subusr_id))
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
                                      [raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.subusr_id])
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
                                   raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.subusr_id))

                sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                            values(%s,%s,%s,%s,%s,now())
                        """
                self.db.query(sql, [self.subusr_id, 'wechat_mall_refund',
                                    "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                                        raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.subusr_id),
                                    '退款回调更新wechat_mall_refund表数据', self.subusr_id])
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
                                   raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], self.subusr_id))
                return 1
            except:
                return 1

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





