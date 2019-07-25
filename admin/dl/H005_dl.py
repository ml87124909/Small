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

class cH005_dl(cBASE_DL):
    def init_data(self):
        #self.usr_dept_id = self.dActiveUser['usr_dept'][0]
        # 以字典形式创建列表上要显示的字段
        # 以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        # [列表名,查询用别名,表格宽度,对齐]
        self.FDT = [
            ['用户ID', "u.usr_id", '', ''],  # 0
            ['登录IP', "u.login_ip", '', ''],  # 1
            ['登录ID', "u.login_id", '', ''],  # 2
            ['HTTP_USER_AGENT', "u.HTTP_USER_AGENT", '40%', ''],  # 3
            ['登录类型', "u.login_type", '', ''],  # 4
            ['状态', "u.login_status", '', ''],  # 5
            ['登录时间', "u.ctime", '', ''],  # 6
            ['姓名', "u.usr_name", '', ''],  # 7

        ]
        # self.GNL=[] #列表上出现的
        # self.SNL=[]     #排序
        # self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0, 2,  1, 3, 4, 5, 6])


    #在子类中重新定义         
    def myInit(self):
        self.src = 'H005'
        pass

    def mRight(self):

        sql = """
                    select u.usr_id  --0
                        ,u.login_id
                      
                        ,u.login_ip
                        ,u.HTTP_USER_AGENT
                        ,u.login_type
                        ,u.login_status
                        ,to_char(u.ctime,'YYYY-MM-DD')

                     from login_log u
                     left join users us on u.login_id = us.login_id
                     
                """
        parm=[]
        self.qqid = self.GP('qqid', '')

        self.pageNo = self.GP('pageNo', '')
        if self.pageNo == '': self.pageNo = '1'
        self.pageNo = int(self.pageNo)
        if self.qqid != '':
            sql += "where u.login_id LIKE %s "
            parm.append('%%%s%%'%self.qqid)
        # ORDER BY

        sql += " ORDER BY u.id DESC limit 100;"

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo,L=parm)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L


   
