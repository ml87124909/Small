# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cfans_dl(cBASE_DL):

    def init_data(self):

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

        self.GNL = self.parse_GNL([0,1,2,3,4,5,6])


    def mRight(self,weid):
        
        sql = """
        SELECT id , from_user , realname , nickname , nickname2 , avatar , gender
        ,nationality , resideprovince , residecity , residedist ,''-- dateadd(s,createtime + 8 * 3600,'1970-01-01 00:00:00')
          FROM ims_fans a
           WHERE weid = %s
        """
        parm=[weid]
        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+= " and a.nickname LIKE '%%%s%%' "%(self.qqid)
        #ORDER BY 

        sql+=" ORDER BY a.id desc"
        #self.log(sql)
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo,L=parm)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L