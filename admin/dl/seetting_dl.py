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


import hashlib , os , time , random,datetime,traceback

class cseetting_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['', '积分规则设置', '积分商品设置']  # 列表表头

    #在子类中重新定义         
    def myInit(self):
        self.src = 'seetting'
        self.part = self.GP('part', 'Localfrm')
        self.tab = self.GP("tab", "1")

    def get_local_data(self):
        """获取 local 表单的数据
        """


        sql = """
            select token,name,key,secret from ims_wechats where usr_id=%s
            """
        l = self.db.fetch(sql,[self.usr_id_p])
        return l


    
    def local_add_save(self):

        dR = {'code': '', 'MSG': '保存成功'}

        #token,name,key,secret
        token = self.GP('token', '')  #token
        name  = self.GP('name', '')  #name
        key = self.GP('key', '')  # appid
        secret = self.GP('secret', '')  # secret

        data = {
            'token': token,
            'name': name,
            'key':key,
            'secret': secret,
        }  # pt_conf
        sql="select weid from ims_wechats where usr_id=%s"
        l,t=self.db.select(sql,[self.usr_id_p])
        if t==0:
            self.db.insert('ims_wechats', data)
            #self.oTOLL.update()
            dR['code'] = '0'
            return dR

        id=l[0][0]
        self.db.update('ims_wechats', data, " weid = %s " % (id))
        #self.oTOLL.update()

        dR['code'] = '0'
        dR['MSG'] = '修改成功'
        return dR
        # 更新数据缓存






