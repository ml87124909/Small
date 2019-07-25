# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) janedao
# Author：hyj
# Start  Date:  2019
##############################################################################
"""BIZ_BASE Module"""


import time,hashlib,os,oss2
from imp import reload
from basic.publicw import DEBUG, CLIENT_NAME, ATTACH_ROOT, PEM_ROOTR
if DEBUG=='1':
    import admin.dl.MODEL_DL
    reload(admin.dl.MODEL_DL)
from admin.dl.MODEL_DL             import cMODEL_DL
from werkzeug import secure_filename
from qiniu import Auth, put_stream, put_data,BucketManager
from basic.wxbase import wx_minapp_login, WXBizDataCrypt, WxPay
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatWxa

#from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
#from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient



#需要填写你的 Access Key 和 Secret Key
#access_key = app.config['QINIU_ACCESS_KEY']
#secret_key = app.config['QINIU_SECRET_KEY']
#构建鉴权对象
#q = Auth(access_key, secret_key)
#要上传的空间
#bucket_name = app.config['QINIU_BUCKET_NAME']
#domain_prefix = app.config['QINIU_DOMAIN']

class cBASE_DL(cMODEL_DL):

    def qiniu_Upload(self):#保存到七牛
        if self.oss_now > self.oss_all and self.qiniu_flag == 0 and self.oss_flag != 7:
            return '您的容量已超'
        file = self.objHandle.files['file']  # request的files属性为请求中文件的数据<input 里的name="file">
        url = ''
        if file and self.allowed_file(file.filename):
            # if file.filename.find('.') > 0:
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[-1].lower()
            timeStamp = time.time()
            md5name = hashlib.md5()
            md5name.update(str(timeStamp).encode('utf-8'))
            filename = md5name.hexdigest() + '.' + file_ext
            file_content = file.read()
            file_size = float(len(file_content)) / 1024
            if self.qiniu_ctype_all==0:
                url = self.qiniu_upload_file(file_content, filename)
            else:
                url = self.ali_upload_file(file_content, filename)
            self.Save_pic_table(file_ext, file_size, filename, url)

        return url

    def Pem_upload(self):#PEM证书保存到本地

        file = self.objHandle.files['file']  # request的files属性为请求中文件的数据<input 里的name="file">
        url = ''
        if file and self.PEM_allowed_file(file.filename):
            # if file.filename.find('.') > 0:
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[-1].lower()
            timeStamp = time.time()
            md5name = hashlib.md5()
            md5name.update(str(timeStamp).encode('utf-8'))
            filename = md5name.hexdigest() + '.' + file_ext
            paths = os.path.join(PEM_ROOTR, '%s' % self.usr_id_p)
            self.make_sub_path(paths)
            file.save(os.path.join(paths, filename))
            url = '/var/data_h/%s/%s/' % (CLIENT_NAME,self.usr_id_p) + filename

        return url

    def qiniu_upload_file(self,source_file, filename):

        # 构建鉴权对象
        q = Auth(self.qiniu_access_key_all, self.qiniu_secret_key_all)
        token = q.upload_token(self.qiniu_bucket_name_all, filename)
        domain_prefix=self.qiniu_domain_all

        ret, info = put_data(token, filename, source_file)
        if info.status_code == 200:
            return domain_prefix + filename
        return None

    def ali_upload_file(self,source_file, filename):

        domain_prefix = self.qiniu_domain_all
        #endpoint = 'http://oss-cn-shenzhen.aliyuncs.com'  # 你的Bucket处于的区域
        auth = oss2.Auth(self.qiniu_access_key_all, self.qiniu_secret_key_all)
        bucket = oss2.Bucket(auth, self.endpoint, self.qiniu_bucket_name_all)
        # result = bucket.put_object(filename, source_file)  # 上传
        # if result.status == 200:
        #     return domain_prefix + filename
        new_filename='%s/'%self.usr_id_p+filename
        result = bucket.put_object(new_filename, source_file)  # 上传
        if result.status == 200:
            return domain_prefix + new_filename

        return None

    def PEM_allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ['pem']

    def allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ['bmp', 'png', 'jpg', 'jpeg', 'gif']

    def Upload(self):#保存到本地硬盘

        file = self.objHandle.files['file']  # request的files属性为请求中文件的数据<input 里的name="file">
        url = ''
        if file and self.allowed_file(file.filename):
        #if file.filename.find('.') > 0:
            filename = secure_filename(file.filename)
            file_ext=filename.rsplit('.', 1)[-1].lower()
            timeStamp = time.time()
            md5name = hashlib.md5()
            md5name.update(str(timeStamp).encode('utf-8'))
            filename = md5name.hexdigest() + '.' + file_ext
            file_content = file.read()
            file_size = float(len(file_content)) / 1024
            paths = os.path.join(ATTACH_ROOT,'%s'%self.usr_id_p)
            self.make_sub_path(paths)
            PATH = os.path.join(paths, filename)
            f = open(PATH, 'wb')
            f.write(file_content)
            f.flush()
            f.close()

            url = 'static/data/%s/'%self.usr_id_p + filename
            self.Save_pic_table(file_ext, file_size, filename, url)
            # file = file.read()
            # url = self.qiniu_upload_file(file, filename)#七牛存储保存图片
        return url

    def to_qiniu_Upload(self,file):#保存到七牛

        #file = self.objHandle.files['file']  # request的files属性为请求中文件的数据<input 里的name="file">
        url = ''
        if file and self.allowed_file(file.filename):
            # if file.filename.find('.') > 0:
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[-1].lower()
            timeStamp = time.time()
            md5name = hashlib.md5()
            md5name.update(str(timeStamp).encode('utf-8'))
            filename = md5name.hexdigest() + '.' + file_ext
            file_content = file.read()
            file_size = float(len(file_content)) / 1024
            url = self.qiniu_upload_file(file_content, filename)
            self.Save_pic_table(file_ext, file_size, filename, url)

        return url

    def Save_pic_table(self, f_ext, f_size, filename, url):

        f_year = self.getToday(6)[:4]
        sql = """insert into images(usr_id,f_year,f_ext,f_size,cname,pic,cid,ctime)
                        values(%s,%s,%s,%s,%s,%s,%s,now())"""
        L = [self.usr_id_p, f_year, f_ext, f_size, filename, url, self.usr_id]
        self.db.query(sql, L)

        if ('http://' in url or 'https://' in url) and self.qiniu_flag==0:
            nums=(float(f_size) / 1024)
            self.oUSERS_OSS.updates(self.usr_id_p,nums)
            try:
                sqlu = "update users set oss_now=coalesce(oss_now,0)+(%s/1024),utime=now(),uid=%s where usr_id=%s"
                self.db.query(sqlu, [f_size, self.usr_id, self.usr_id_p])
            except Exception as e:
                self.print_log('处理oss_now出错', '%s' % e)
        return

    def save_type(self):#保存广告类型
        type = self.GP("type", '')
        field = self.GP("field", '')
        cname = self.GP("cname", '')
        sort = self.GP("sort", '')
        id = self.GP("id", '')
        dR = {'code': '', 'MSG': ''}
        if id=='0':
            sql = "insert into advertis(usr_id,type,field,cname,sort,cid,ctime)values(%s,%s,%s,%s,%s,%s,now())"
            try:
                dR['MSG'] = '增加类型成功'
                self.db.query(sql, [self.usr_id_p, type, field, cname, sort, self.usr_id])
                self.oSHOP.update(self.usr_id_p)
                self.oGOODS_D.update(self.usr_id_p)
                self.oGOODS.update(self.usr_id_p)
                self.oGOODS_N.update(self.usr_id_p)
                return dR
            except:
                dR['MSG'] = '增加类型失败'
                return dR
        else:
            sql="update advertis set type=%s,field=%s,cname=%s,sort=%s,uid=%s,utime=now() where id=%s "
            try:
                dR['MSG'] = '修改类型成功'
                self.db.query(sql, [type, field, cname, sort, self.usr_id,id])
                self.oSHOP.update(self.usr_id_p)
                self.oGOODS_D.update(self.usr_id_p)
                self.oGOODS.update(self.usr_id_p)
                self.oGOODS_N.update(self.usr_id_p)
                return dR
            except:
                dR['MSG'] = '增加类型失败'
                return dR


    def sendMselectData(self, ListData, hid_cols=0):
        # 发送mselect列表数据
        # 这里重写是因为要处理那个显示和实际的列不一样
        # hid_cols 隐藏后面多少列
        res = {'list': [], 'value': []}
        if len(ListData) > 0:
            if hid_cols != 0:  # 不为零说明需要隐藏后面的N 列
                tmp_list = []
                for r in ListData:
                    row_tmp = eval('r[:-%s]' % hid_cols)  # 例子 row_tmp = r[:-2]
                    tmp_list.append(row_tmp)
                res['list'] = tmp_list
            else:
                res['list'] = ListData  # 显示用的结果集
            tmp = []
            for row in ListData:
                try:
                    t = '###'.join(row)  # 要保证row 里面全部都是字符串类型的，要不然会报错，当然下面我处理了
                except TypeError:
                    row_tmp = []
                    for r in row:
                        row_tmp.append(str(r))
                    t = '###'.join(row_tmp)
                tmp.append(t)
            res['value'] = tmp  # 选择用的结果集
        return res

    def sendLayerData(self, ListData, hid_cols=0):
        # 发送mselect列表数据
        # 这里重写是因为要处理那个显示和实际的列不一样
        # hid_cols 隐藏后面多少列
        exec('from %s.source.json                  import write,read ' % CLIENT_NAME)
        result = ''
        res = {'list': [], 'value': []}
        if len(ListData) > 0:

            if hid_cols != 0:  # 不为零说明需要隐藏后面的N 列
                tmp_list = []
                for r in ListData:
                    row_tmp = eval('r[:-%s]' % hid_cols)  # 例子 row_tmp = r[:-2]
                    tmp_list.append(row_tmp)
                res['list'] = tmp_list
            else:
                res['list'] = ListData  # 显示用的结果集
            tmp = []
            for row in ListData:
                try:
                    t = '###'.join(row)  # 要保证row 里面全部都是字符串类型的，要不然会报错，当然下面我处理了
                except TypeError:
                    row_tmp = []
                    for r in row:
                        row_tmp.append(str(r))
                    t = '###'.join(row_tmp)
                tmp.append(t)
            res['value'] = tmp  # 选择用的结果集
        # result = write(res)
        return res


    def delete_local_pic_data(self):
        pk = self.GP('id','')
        dR = {'code':'', 'MSG':''}
        sql="select cname from images where id =%s"
        l,n =self.db.select(sql,pk)
        if n ==0:
            dR['code'] = '1'
            dR['MSG'] = '删除图片失败！'
            return dR
        filename=l[0][0]
        paths = os.path.join(ATTACH_ROOT, '%s' % self.usr_id_p)

        img_path = os.path.join(paths, filename)

        if os.path.isfile(img_path):
            os.remove(img_path)
        if os.path.isfile(img_path):
            dR['code'] = '1'
            dR['MSG'] = '删除图片失败！'
            return dR
        self.db.query("delete from  images  where id= %s" % pk)
        dR['MSG'] = '删除图片成功！'
        return dR

    def delete_qiniu_pic_data(self):
        pk = self.GP('id','')
        dR = {'code':'', 'MSG':''}
        sql="select cname from images where id =%s"
        l,n =self.db.select(sql,pk)
        if n ==0:
            dR['code'] = '1'
            dR['MSG'] = '删除图片失败！'
            return dR
        filename=l[0][0]
        paths = os.path.join(ATTACH_ROOT, '%s' % self.usr_id_p)

        img_path = os.path.join(paths, filename)

        if os.path.isfile(img_path):
            os.remove(img_path)
        if os.path.isfile(img_path):
            dR['code'] = '1'
            dR['MSG'] = '删除图片失败！'
            return dR
        self.db.query("update  images set del_flag=1,utime=now()  where id= %s" , pk)
        dR['MSG'] = '删除图片成功！'
        return dR

    def get_hy_up_level(self):#会员级别
        L = []
        sql = """
                    select id,cname,up_price,level_discount from hy_up_level where usr_id=%s  order by up_price 
                """
        l, n = self.db.fetchall(sql, self.usr_id_p)
        if n > 0:
            L = l
        return L

    def del_qiniu_pic(self):
        path_url = self.GP('path_url','')
        dR = {'code':'', 'MSG':''}
        sql = "select id,cname from images where pic =%s and COALESCE(del_flag,0)=0"
        l, n = self.db.select(sql, path_url)
        if n == 0:
            dR['code'] = '1'
            dR['MSG'] = '删除图片失败！'
            return dR
        aid,cname=l[0]

        q = Auth(self.qiniu_access_key, self.qiniu_secret_key)
        bucket_name = self.qiniu_bucket_name

        bucket = BucketManager(q)
        ret, info = bucket.stat(bucket_name, cname)
        if ret == None:
            q = Auth(self.qiniu_access_key_all, self.qiniu_secret_key_all)
            bucket_name = self.qiniu_bucket_name_all
            bucket = BucketManager(q)
            ret, info = bucket.stat(bucket_name, cname)
            if ret == None:
                dR['code'] = '1'
                dR['MSG'] = '数据有误！'
                return dR
        ret_d, info_d = bucket.delete(bucket_name, cname)

        self.db.query("update images set del_flag=1  where id= %s", aid)
        dR['MSG'] = '删除图片成功！'
        dR['code'] = '0'
        return dR

    def local_ajax_goods(self):
        kw = self.GP('keyword', '')
        sql = u"""
                select id,name from goods_info 
                where COALESCE(del_flag,0)=0 and status=0 and usr_id=%s
                    """
        L=[self.usr_id_p]
        if kw != '':
            sql += "and name LIKE %s"
            L.append('%%%s%%'%kw)
        sql += " ORDER BY id"
        lT, iN = self.db.select(sql,L)

        return self.sendMselectData(lT)

    def local_ajax_pt_goods(self):
        kw = self.GP('keyword', '')
        sql = u"""
                select id,name from goods_info 
                where COALESCE(del_flag,0)=0 and status=0 and usr_id=%s and COALESCE(pt_status,0)=1
                and id not in (select goods_id from pt_conf where usr_id=%s and COALESCE(del_flag,0)=0)
                    """
        L = [self.usr_id_p, self.usr_id_p]
        if kw != '':
            sql += "and name LIKE %s"
            L.append('%%%s%%' % kw)
        sql += " ORDER BY id"
        lT, iN = self.db.select(sql, L)

        return self.sendMselectData(lT)


    def local_ajax_getTree(self):
        L=[]
        sql = """
            select 
                id,pid,name,level 
                from category 
                where usr_id=%s and  COALESCE(del_flag,0)=0 or id=1
                order by level,paixu,id
        """
        lT, iN = self.db.select(sql,self.usr_id_p)
        if iN>0:
            L = lT
        return L

    def local_ajax_getGoods(self):

        keywords = self.GP('keyword', '')
        tree_pk = self.GP('tree_pk', '')
        rL = []
        sql = """
        select id,name,originalprice,minprice,stores,limited 
            from goods_info 
            where usr_id=%s and  COALESCE(del_flag,0)=0  and status=0
        """
        parm=[self.usr_id_p]
        if keywords!='':#name
            sql+="and  name like %s "
            parm.append('%%%s%%'%keywords)
        if tree_pk != '' and tree_pk != '1':#category_ids
            sql += "and  category_ids like %s "
            parm.append('%%%s%%' % tree_pk)
        sql += """  order by paixu """
        lT, iN = self.db.fetchall(sql,parm)
        if iN > 0:
            rL = [lT, iN]

        return rL

    def local_ajax_ticket(self):
        kw = self.GP('keyword', '')
        sql = """
                select id,cname,type_str,apply_str,remark from coupons where COALESCE(del_flag,0)=0 and usr_id=%s
            """
        L=[self.usr_id_p]
        if kw != '':
            sql += " and cname LIKE %s"
            L.append('%%%s%%'%kw)
        sql += " ORDER BY id"
        lT, iN = self.db.select(sql,L)

        return self.sendMselectData(lT)

    def local_ajax_hot_goods(self):
        kw = self.GP('keyword', '')
        sql = u"""
                select id,cname from goods_info 
                where COALESCE(del_flag,0)=0 and status=0 
                and id not in (select gid from hot_sell where coalesce(del_flag,0)=0)
                    """
        L = []
        if kw != '':
            sql += " and cname LIKE %s"
            L.append('%%%s%%' % kw)
        sql += " ORDER BY id"
        lT, iN = self.db.select(sql, L)

        return self.sendMselectData(lT)

    def order_cancel_send(self, wechat_user_id, form_id, order_num, total='', ctime='', orderid=''):  # 订单取消通知模板消息
        # 订单金额，取消原因，下单时间，订单编号，提示
        wxa=self.get_wecthpy()
        if wxa==0:
            return 1
        opid = self.oOPENID.get(int(wechat_user_id))

        if opid == '':
            return 1
        shop = self.oSHOP_T.get(self.usr_id_p)

        if shop == {}:
            return 1
        url = None
        tid = shop.get('cancel_id', '')  #'M1VCMVmg6_Rz5ZCxBZpZGYsojOIfOxJt80Lo83OSzW8'
        if tid=='':
            return 1
        cancel_url = shop.get('cancel_url', '')
        if cancel_url != '':
            url = cancel_url.format(orderid=orderid)

        data = {"keyword1": {
            "value": "%s" % total
        }, "keyword2": {
            "value": "商家取消"
        }, "keyword3": {
            "value": "%s" % ctime
        }, "keyword4": {
            "value": "%s" % order_num
        }, "keyword5": {
            "value": "您的订单已取消，欢迎再次光临"
        }
        }
        try:
            a = wxa.send_template_message(opid, tid, data, form_id, page=url)
        except Exception as e:
            self.print_log('订单取消:%s' % tid, '%s' % e)
            a = 1
        return a


    def order_shipment_send(self, wechat_user_id, form_id, order_num, shipment='', shipmentcode='',
                            orderid=''):  # 订单发货通知模板消息
        #订单号  发货时间，快递公司，物流单号
        wxa=self.get_wecthpy()
        if wxa==0:
            return 1
        opid=self.oOPENID.get(int(wechat_user_id))

        if opid=='':
            return 1
        shop=self.oSHOP_T.get(self.usr_id_p)

        if shop=={}:
            return 1
        url = None
        tid = shop.get('send_id', '')  #'M1VCMVmg6_Rz5ZCxBZpZGYsojOIfOxJt80Lo83OSzW8'
        if tid=='':
            return 1
        send_url = shop.get('send_url', '')
        if send_url != '':
            url = send_url.format(orderid=orderid)
        data={"keyword1": {
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
        try:
            a = wxa.send_template_message(opid, tid, data, form_id, page=url)
        except Exception as e:
            self.print_log('推送发货消息失败:%s' % tid, '%s' % e)
            a=1
        return a

    def order_refund(self, subusr_id, order_id, order_num, wechat_user_id):

        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]
        re_num = 'R' + danhao[2:] + romcode
        mall = self.oMALL.get(subusr_id)

        app_id = mall.get('appid', '')
        secret = mall.get('secret', '')
        wx_mch_id = mall.get('mchid', '')
        wx_mch_key = mall.get('mchkey', '')
        base_url = mall.get('base_url', '')  # 'https://malishop.janedao.cn'
        api_cert_path = mall.get('cert', '')
        api_key_path = mall.get('key', '')

        notify_url = base_url + '/refund/%s/notify' % subusr_id
        wxpay = WxPay(app_id, wx_mch_id, wx_mch_key, notify_url)

        sql = "select total_fee from wechat_mall_payment where order_id=%s and payment_number=%s and usr_id=%s "
        l, t = self.db.select(sql, [order_id, order_num, subusr_id])
        if t == 0:
            return 1
        total_fee = l[0][0]
        data = {  # 退款信息
            'out_trade_no': order_num,  # 商户订单号
            'total_fee': total_fee,  # 订单金额
            'refund_fee': total_fee  # 退款金额
        }
        sql = "select out_refund_no from wechat_mall_refund where out_trade_no=%s and usr_id=%s"
        lT, iN = self.db.select(sql, [order_num, subusr_id])
        if iN == 0:
            data['out_refund_no'] = re_num  # 商户退款单号
            refund = {  # 退款信息
                'out_trade_no': order_num,  # 商户订单号
                'total_fee': total_fee,  # 订单金额
                'refund_fee': total_fee,  # 退款金额
                'out_refund_no': re_num,
                'usr_id': subusr_id,
                'wechat_user_id': wechat_user_id
            }

            self.db.insert('wechat_mall_refund', refund)
            data['notify_url'] = notify_url  # 商户退款回调
            raw = wxpay.refund(api_cert_path, api_key_path, **data)

            if raw['return_code'] == 'SUCCESS' and raw['result_code'] == 'SUCCESS':

                try:
                    sql = """select id from wechat_mall_refund 
                        where out_trade_no=%s and out_refund_no=%s and total_fee=%s and usr_id=%s"""
                    l, i = self.db.select(sql, [raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id])
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
                                   raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id))

                    sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                                values(%s,%s,%s,%s,%s,now())
                            """
                    self.db.query(sql, [subusr_id, 'wechat_mall_refund',
                                        "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                                        raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id),
                                        '退款回调更新wechat_mall_refund表数据', subusr_id])
                    sql = "update wechat_mall_order set status=-1,status_str='已取消'  where  id=%s and usr_id=%s "
                    self.db.query(sql, [order_id, subusr_id])
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
                                   raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id))
                    return 1
                except:
                    return 1
        out_refund_no = lT[0][0]
        data['out_refund_no'] = out_refund_no  # 商户退款单号
        raw = wxpay.refund(api_cert_path, api_key_path, **data)
        if raw['return_code'] == 'SUCCESS' and raw['result_code'] == 'SUCCESS':
            try:
                sql = "select id from wechat_mall_refund where out_trade_no=%s and out_refund_no=%s and total_fee=%s and usr_id=%s"
                l, i = self.db.select(sql,
                                      [raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id])
                if i == 0:
                    return 1

                sql = "update wechat_mall_order set status=-1,status_str='已取消'  where  id=%s and usr_id=%s "
                self.db.query(sql, [order_id, subusr_id])

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
                                   raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id))

                sql = """insert into wechat_mall_order_log(usr_id,edit_name,edit_memo,edit_remark,cid,ctime)
                            values(%s,%s,%s,%s,%s,now())
                        """
                self.db.query(sql, [subusr_id, 'wechat_mall_refund',
                                    "out_trade_no='%s' and out_refund_no='%s' and total_fee=%s and usr_id=%s" % (
                                        raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id),
                                    '退款回调更新wechat_mall_refund表数据', subusr_id])
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
                                   raw['out_trade_no'], raw['out_refund_no'], raw['total_fee'], subusr_id))
                return 1
            except:
                return 1



