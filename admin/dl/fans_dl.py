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


class cfans_dl(cBASE_DL):
    def init_data(self):
        #self.usr_dept_id=self.dActiveUser['usr_dept'][0]
        #以字典形式创建列表上要显示的字段 
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['粉丝ID',      "a.id",             '',''],#0
            ['OpenID',      "a.from_user",           '',''],#1
            ['昵称',      "a.nickname",      '',''],#2
            ['头像',      "a.avatar",'',''],#3
            ['性别',        "a.gender",     '',''],#4
            ['地区',      "resideprovince",'',''],#5
            ['创建时间',    "a.createtime",               '',''],#6
            ['最后修改人',  "ISNULL(u2.usr_name,'')",'',''],#7
            ['最后修改时间',"a.utime",               '','']#8
        ]
        #self.GNL=[] #列表上出现的
        #self.SNL=[]     #排序
        #self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0,1,2,3,4,5,6])


    #在子类中重新定义         
    def myInit(self):
        self.src = 'fans'
        pass

    def mRight(self):
        
        sql = u"""
        SELECT id , from_user , realname , nickname , nickname2 , avatar , gender
        ,nationality , resideprovince , residecity , residedist ,''-- dateadd(s,createtime + 8 * 3600,'1970-01-01 00:00:00')
          FROM ims_fans a
           WHERE weid = '%s'
        """ % self.weid
        
        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+= " and a.nickname LIKE '%%%s%%' "%(self.qqid)
        #ORDER BY 

        sql+=" ORDER BY a.id desc"
        #self.log(sql)
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L