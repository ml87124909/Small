# -*- coding: utf-8 -*-

##############################################################################
#
#
#
##############################################################################
from imp import reload
from basic.publicw import DEBUG


if DEBUG == '1':    
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import hashlib , os , time , random

class cH006_dl(cBASE_DL):
    def init_data(self):
        #self.usr_dept_id = self.dActiveUser['usr_dept'][0]
        # 以字典形式创建列表上要显示的字段
        # 以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        # [列表名,查询用别名,表格宽度,对齐]
        self.FDT = [
            ['ID', "u.usr_id", '', ''],  # 0
            ['login_id', "u.login_id", '', ''],  # 1
            ['姓名', "u.usr_name", '', ''],  # 2
            ['电话', "u.mobile", '', ''],  # 3
            ['被锁时间', "u.login_lock_time", '', ''],  # 4
            ['状态', "u.login_lock", '', ''],  # 5

        ]
        # self.GNL=[] #列表上出现的
        # self.SNL=[]     #排序
        # self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0, 1, 4])


    #在子类中重新定义         
    def myInit(self):
        self.src = 'H006'
        pass

    def mRight(self):

        sql = """
            select usr_id,login_id,to_char(login_lock_time,'YYYY-MM-DD HH:24-MI') 
            from users
            where  COALESCE(login_lock,0)=1 
                     
                """
        parm=[]
        self.qqid = self.GP('qqid', '')

        self.pageNo = self.GP('pageNo', '')
        if self.pageNo == '': self.pageNo = '1'
        self.pageNo = int(self.pageNo)
        if self.qqid != '':
            sql += "where login_id LIKE %s "
            parm.append('%%%s%%'%self.qqid)
        # ORDER BY

        sql += " ORDER BY usr_id DESC"

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo,L=parm)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L


   
