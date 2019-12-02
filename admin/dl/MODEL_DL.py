# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/dl/MODEL_DL.py"""
#
# from imp import reload
# from basic.publicw import DEBUG
# if DEBUG == '1':
#     import admin.dl.DL_BASE
#     reload(admin.dl.DL_BASE)
from admin.dl.DL_BASE  import cDL_BASE

import os

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatWxa

class cMODEL_DL(cDL_BASE):

    def myaddslashes(self, s):

        if not s:
            return s
        d = {'"': '\\"', "'": "\\'", "\0": "\\\0", "\\": "\\\\"}
        return ''.join(d.get(c, c) for c in s)

    # 代替了self.REQUEST.get()
    # key为参数名， default为默认值，type为是否需要过滤字符
    def GPRQ(self, key, default=None, ctype=1):
        value = self.REQUEST.get(key, default)
        if ctype == 1 and value and isinstance(value, str):
            self.myaddslashes(value.strip())
        return value


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

    def make_sub_path(self, sPATH):
        """检查os的最后一级子目录，如果不存在，生成之"""
        if os.path.exists(sPATH) == 0:
            os.makedirs(sPATH)
        return 0

    def pic_list(self):
        L=[]
        sql="select id,id from images where usr_id =%s"
        l,t=self.db.select(sql,self.usr_id_p)
        if t>0:
            L=l
        return L

    def pic_dict(self):
        D={}
        sql="select id,pic from images where usr_id =%s"
        l,t=self.db.select(sql,self.usr_id_p)
        if t>0:
            for i in l:
                D[i[0]]=i[1]
        return D




    def list_for_grid_self(self, List,iTotal_length, pageNo=1, select_size=10):

        if iTotal_length % select_size == 0:
            iTotal_Page = iTotal_length // select_size
        else:
            iTotal_Page = iTotal_length // select_size + 1

        start, end = (int(pageNo) - 1) * select_size, pageNo * select_size
        if end >= iTotal_length: end = iTotal_length
        if iTotal_length == 0 or start > iTotal_length or start < 0:
            return [], iTotal_length, iTotal_Page, pageNo, select_size
        return List, iTotal_length, iTotal_Page, pageNo, select_size

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

    def get_wecthpy(self):#微信小程序调用
        mall=self.oMALL.get(self.usr_id_p)

        if mall=={}:
            return 0

        appid=mall['appid']
        secret =mall['secret']
        client = WeChatClient(appid, secret)
        wxa = WeChatWxa(client)
        return wxa


    def use_log(self,memo):
        sql="insert into use_log(usr_id,viewid,memo,ctime)values(%s,%s,%s,now())"
        self.db.query(sql,[self.usr_id,self.viewid,memo])
        return

    def get_QR_code_url(self,vtype):
        if self.qr_ticket!='':
            return self.qr_ticket

        pdata = {'viewid': 'wxcode', 'part': 'Get_ticket',
                 'vtype': vtype
                 }

        r = self._http.post('https://wxcode.yjyzj.cn/wxcode', data=pdata)
        res = r.json()
        if res.get('code', '') == '0':
            url = res.get('url', '')
            self.qr_ticket = url
            return url

        return ''






