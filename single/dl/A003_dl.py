# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/A003_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cA003_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['','编号','KEY','值','备注','添加时间','更新时间']

    def mRight(self):
            
        sql = u"""
            select id,key,content,remark,ctime,utime from config_set  where COALESCE(del_flag,0)=0 and usr_id= %s
        """
        parm=[self.usr_id_p]
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo,L=parm)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self):
        L = {}
        sql = """
            select id,type,type_str,key,content,remark,ctime,utime from config_set  where id= %s
        """
        if self.pk != '':
            L = self.db.fetch( sql,[self.pk] )

        return L
    
    def local_add_save(self):
        pk = self.pk
        dR = {'code': '', 'MSG': '保存成功'}
        #获取表单参数
        type=self.GP('type','')#类型
        type_str = self.GP('type_str','')  # 类型
        key=self.GP('key','')#编码
        content=self.GP('content','')#参数值
        remark=self.GP('remark','')#备注
        
        data = {
                'type':type
                ,'type_str':type_str
                ,'key':key
                ,'content':content
                ,'remark':remark
        }
        try:
            if pk != '':  #update
                data['uid']=self.usr_id
                data['utime']= self.getToday(9)
                self.db.update('config_set' , data , " id = %s " % pk)
                self.use_log('修改文字广告')

            else:  #insert
                #如果是插入 就去掉 uid，utime 的处理
                data['cid']= self.usr_id_p
                data['ctime']= self.getToday(9)
                data[ 'usr_id']=self.usr_id
                self.db.insert('config_set' , data)
                self.use_log('增加文字广告')
            self.oSHOP.update(self.usr_id_p)
            dR['pk'] = pk
            dR['code']=0
        except:
            dR['code'] = '1'
            dR['MSG'] = '保存失败'
        return dR

    def delete_data(self):
        pk = self.pk
        dR = {'code':'', 'MSG':''}
        self.db.query("update config_set set del_flag=1 where id= %s and usr_id=%s" ,[pk,self.usr_id_p])
        self.use_log('删除文字广告')
        self.oSHOP.update(self.usr_id_p)
        dR['code']='0'
        dR['MSG'] = '删除成功'
        return dR


