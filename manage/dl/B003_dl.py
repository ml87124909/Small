# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/B003_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cB003_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['','模板名称','模板ID','最近推送人']


    def mRight(self):
        wxa=self.get_wecthpy()
        if wxa==0:
            return [0,0,0,0],[]
        pageNo=self.GP('pageNo','')
        if pageNo=='':
            pageNo='1'
        pageNo=int(pageNo)
        offset=pageNo*10-10

        select_size=10
        List=wxa.list_templates(offset=offset, count=10)
        all_c=len(List)

        if all_c==0:
            return [0, 0, 0, 0], []
        L, iTotal_length, iTotal_Page, pageNo, select_size=self.list_for_grid_self(List,all_c,pageNo,select_size)
        
        #L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]

        return PL,L

    def get_local_data(self ):
        wxa = self.get_wecthpy()
        if wxa == 0:
            return [0, 0, 0, 0], []
        pageNo = self.GP('pageNo', '')
        if pageNo == '':
            pageNo = '1'
        pageNo = int(pageNo)
        offset = pageNo * 10 - 10

        select_size = 10
        A = wxa.list_library_templates(offset=offset, count=10)
        List=A.get('list','')
        all_c = A.get('total_count','')

        if List == '' and all_c == '':
            return [0, 0, 0, 0], []
        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid_self(List, all_c, pageNo, select_size)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L


    def local_add_save(self):
        

        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        
        #这些是操作权限
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}  

        #dR={'R':'','MSG':'','isadd':''}
        dR={'R':'','MSG':''}

        
        
        #获取表单参数
        appid=self.GP('appid')#小程序appid
        secret=self.GP('secret')#小程序secret
        wxtoken=self.GP('wxtoken')#小程序对应的token
        mchid=self.GP('mchid')#微信支付商户号
        mchkey=self.GP('mchkey')#微信支付商户秘钥


        data = {
                'appid':appid
                ,'secret':secret
                ,'wxtoken':wxtoken
                ,'mchid':mchid
                ,'mchkey':mchkey
                ,'usr_id':self.usr_id

        }


        pk=''
        sql="select id from mall where usr_id=%s"%self.usr_id_p
        l,t=self.db.select(sql)
        if t>0:
            pk=l[0][0]

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data['cid']=self.usr_id
            data['ctime']=self.getToday(6)
            #data.pop('random')

            self.db.update('mall' , data , " id = %s " % pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data['uid'] = self.usr_id
            data['utime'] = self.getToday(6)
            
            self.db.insert('mall' , data)

        #self.listdata_save(pk,danhao)
        dR['pk'] = pk
        
        return dR

    def save_temp(self):
        tid = self.GP("tid",'')
        ttitle = self.GP("ttitle",'')
        link = self.GP("link", '')
        keywords = self.GP("keywords", '')
        dR={'code':'','MSG':''}
        sql="insert into templates(usr_id,ttitle,tid,link,keywords,cid,ctime)values(%s,%s,%s,%s,%s,%s,now())"
        try:
            dR['MSG']='增加模板成功'
            self.db.query(sql,[self.usr_id_p,ttitle,tid,link,keywords,self.usr_id])
            return dR
        except:
            dR['MSG'] = '增加模板失败'
            return dR

    def ajax_delete_data(self):

        dR = {'code':'', 'MSG':'删除失败!'}
        if self.pk != '':
            wxa = self.get_wecthpy()
            if wxa==0:
                return dR
            wxa.del_template(self.pk)
            dR['MSG'] = '删除成功！'

        return dR
