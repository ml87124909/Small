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
import time,hashlib,os
from qiniu import Auth, put_stream, put_data,BucketManager

class cF009_dl(cBASE_DL):
    
    def init_data(self):
        self.GNL = ['', '编号','图片名', '图片预览', '大小(KB)','上传时间']
        self.src = 'F009'

    def mRight(self):

        sql = """
            SELECT
                id,
                cname,
                pic,
                f_size,
                to_char(ctime,'YYYY-MM-DD HH24:MI')
            FROM images 
           where usr_id=%s and COALESCE(del_flag,0)=0
        """%self.usr_id_p
        sql += " ORDER BY id DESC"

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L

        
    def delete_qiniu_pic_data(self):
        pk = self.GP('id','')
        dR = {'code':'', 'MSG':''}

        sql="select cname,pic from images where id =%s"
        l,n =self.db.select(sql,pk)
        if n ==0:
            dR['code'] = '1'
            dR['MSG'] = '删除图片失败，请刷新页面重试'
            return dR
        filename,file_link=l[0]

        q = Auth(self.qiniu_access_key, self.qiniu_secret_key)
        bucket_name = self.qiniu_bucket_name

        bucket = BucketManager(q)
        ret, info = bucket.stat(bucket_name, filename)
        if ret == None:
            self.db.query("update images set del_flag=1  where id= %s", pk)
            dR['MSG'] = '七牛没有这张图片，在数据库删除记录成功！'
            dR['code'] = '0'
            return dR

        ret_d, info_d = bucket.delete(bucket_name, filename)
        if ret_d == {}:
            self.db.query("update images set del_flag=1  where id= %s",pk)
            dR['MSG'] = '删除图片成功！'
        return dR



