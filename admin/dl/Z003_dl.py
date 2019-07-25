# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import hashlib , os , time , random
from qiniu import Auth, put_stream, put_data,BucketManager

class cZ003_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['', '编号', '图片名称', '图片预览', '大小(KB)','存储类型', '上传时间']


    #在子类中重新定义         
    def myInit(self):
        self.src = 'Z003'
        pass

    def mRight(self):

        if self.qiniu_access_key == '' or self.qiniu_secret_key == '' or self.qiniu_bucket_name == '':
            return [], []

        q = Auth(self.qiniu_access_key, self.qiniu_secret_key)
        bucket_name = self.qiniu_bucket_name
        bucket = BucketManager(q)
        # 前缀
        prefix = None
        # 列举条目
        limit = 10000
        # 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
        delimiter = None
        # 标记
        marker = None
        ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)

        iTotal_length=len(ret.get('items'))
        if  iTotal_length== 0:
            return [],[]
        List = ret.get('items')

        pageNo=self.GP('pageNo','')
        if pageNo=='':
            pageNo='1'
        pageNo=int(pageNo)

        L, iTotal_length, iTotal_Page, pageNo, select_size=self.list_for_grid( List, iTotal_length, pageNo=pageNo, select_size=10)
        #L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L



    def getfllist(self):
        L=[]
        sql="select id,name from cms_fl"
        l,t=self.db.select(sql)
        if t>0:
            L=l

        return L

    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update post_future set del_flag=1 where id= %s" % pk)
        return dR

    def audit(self):
        id = self.GP('id','')
        ait = self.GP('ait', '')
        dR = {'code': 0, 'MSG': ''}
        if id == '' or ait == '':
            dR['code']=1
            dR['MSG']='参数有误，请重新审核！'
            return dR

        try:
            self.db.query("update post_future set audit_flag=%s,audit_time =now() where id = %s",[ait,id])
        except:
            dR['code'] = 1
            dR['MSG'] = '审核失败，请重新审核！'
            return dR


        dR['MSG'] = '审核提交成功！'
        return dR

    def all_audit(self):
        pk = self.GP('pk','')
        del_id = self.REQUEST.getlist('del_id')
        dR = {'code': 0, 'MSG': ''}

        for id in del_id:
            try:
                self.db.query("update post_future set audit_flag=%s,audit_time =now() where id = %s",[pk,id])
            except:
                dR['code'] = 1
                dR['MSG'] = '审核失败，请重新审核！'
                return dR


        dR['MSG'] = '审核提交成功！'
        return dR



