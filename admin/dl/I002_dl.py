# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/I002_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cI002_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['公告标题','公告类型','发布时间','发布人']


    def mRight(self):
            
        sql = u"""
            select s.id,s.title,s.ctype,s.ctime,u.login_id
            from sys_news s
             left join users u on u.usr_id=s.cid 
            where COALESCE(s.del_flag,0)=0
        """
        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L

    def get_local_data(self ):
        """获取 local 表单的数据
        """
        L={}
        sql = """
            select title,ctype,contents
            from sys_news 
           
            where COALESCE(del_flag,0)=0 and id=%s

        """
        if self.pk!='':
            L = self.db.fetch( sql,self.pk )

        return L

    def local_add_save(self):

        dR={'R':'','MSG':'申请单 保存成功','B':'1'}
        #获取表单参数
        title=self.GP('title','')#标题
        ctype=self.GP('ctype','')#类型
        contents = self.REQUEST.get('text_contents', '')  # 内容
        data = {
                'title':title
                ,'ctype':ctype
                , 'contents': contents
             }

        if self.pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data['uid']=self.usr_id
            data['utime']=self.getToday(6)
            self.db.update('sys_news' , data , " id = %s " % self.pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(6)
            self.db.insert('sys_news' , data)

        return dR

    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update sys_news set del_flag=1,utime=now() where id= %s " ,[pk])

        return dR
