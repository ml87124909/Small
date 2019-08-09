# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/H006_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cH006_dl(cBASE_DL):
    def init_data(self):

        self.FDT = [
            ['ID', "u.usr_id", '', ''],  # 0
            ['login_id', "u.login_id", '', ''],  # 1
            ['姓名', "u.usr_name", '', ''],  # 2
            ['电话', "u.mobile", '', ''],  # 3
            ['被锁时间', "u.login_lock_time", '', ''],  # 4
            ['状态', "u.login_lock", '', ''],  # 5

        ]

        self.GNL = self.parse_GNL([0, 1, 4])


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


   
