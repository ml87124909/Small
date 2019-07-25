# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################

from imp import reload
from basic.publicw import DEBUG
if DEBUG=='1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL
from qiniu import Auth, put_stream, put_data,BucketManager,build_batch_stat
import time

class cZ003(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'Z003_dl'


    def goPartList(self):
        #self.assign('top_btns',self.top_btns())
        self.assign('NL',self.dl.GNL)
        self.navTitle = ''
        self.getBreadcrumb() #获取面包屑
        PL,L = self.dl.mRight()
        M = []
        if len(L)>0:
            for i in L:
                i['pic']=self.dl.qiniu_domain+i['key']
                i['put_time'] = i['putTime']
                if i['putTime']!='':
                    timeStamp=i['putTime']
                    timeArray=time.localtime(int(str(timeStamp)[:10]))
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    i['put_time']=otherStyleTime
                M.append(i)
            self.assign('dataList',M)
            self.getPagination(PL)
        s = self.runApp('Z003_list.html')
        return s
    
    def initPagiUrl(self):
        lb_code = self.REQUEST.get('lb_code','')
        brand_id = self.REQUEST.get('brand_id','')
        status = self.REQUEST.get('status','')
        ctype = self.REQUEST.get('ctype','')
        qqid = self.REQUEST.get('qqid','')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        if lb_code:
            url += "&lb_code=%s" % lb_code
        if brand_id:
            url += "&brand_id=%s" % brand_id
        if status:
            url += "&status=%s" % status
        if ctype:
            url += "&ctype=%s" % ctype
        return url
    
    def goPartLocalfrm(self):
        pass

    def goPartaudit(self):
        dR ={'code':'','MSG':''}
        ait=self.dl.GP('ait','')
        if ait=='':
            dR['MSG']='数据有误!'
            return self.jsons(dR)

        q = Auth(self.dl.qiniu_access_key, self.dl.qiniu_secret_key)
        bucket_name = self.dl.qiniu_bucket_name

        bucket = BucketManager(q)
        ret, info = bucket.stat(bucket_name, ait)
        if ret == None:
            dR['code'] = '1'
            dR['MSG'] = '数据有误！'
            return dR
        ret_d, info_d = bucket.delete(bucket_name, ait)
        dR['MSG'] = '删除成功！'
        self.dl.db.query("update images set del_flag=1 where usr_id=%s and cname=%s",[self.dl.usr_id,ait])
        return self.jsons(dR)


    
    
    
        
 