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

class cseetting_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['', '积分规则设置', '积分商品设置']  # 列表表头

    #在子类中重新定义         
    def myInit(self):

        self.part = self.GP('part', 'Localfrm')
        self.tab = self.GP("tab", "1")

    def get_local_data(self):
        """获取 local 表单的数据
        """


        sql = """
            select convert_from(decrypt(token::bytea, %s, 'aes'),'SQL_ASCII') as token,
                name,convert_from(decrypt(key::bytea, %s, 'aes'),'SQL_ASCII') as key,
                convert_from(decrypt(secret::bytea, %s, 'aes'),'SQL_ASCII') as secret,
                 convert_from(decrypt(hash::bytea, %s, 'aes'),'SQL_ASCII') as hashkey 
                from ims_wechats where usr_id=%s
            """
        l = self.db.fetch(sql,[self.md5code,self.md5code,self.md5code,self.md5code,self.usr_id])
        return l


    
    def local_add_save(self):

        dR = {'code': '', 'MSG': '保存成功'}

        #token,name,key,secret
        token = self.GP('token', '')  #token
        name  = self.GP('name', '')  #name
        key = self.GP('key', '')  # appid
        secret = self.GP('secret', '')  # secret
        hashkey = self.GP('hashkey', '')  # secret

        sql = """
                       update ims_wechats set name=%s,
                       token=encrypt(%s,%s,'aes'),key=encrypt(%s,%s,'aes'),
                       secret=encrypt(%s,%s,'aes'), 
                       hash=encrypt(%s,%s,'aes')
                       where usr_id=%s;
                       """
        Lu = [name, token,self.md5code, key, self.md5code,secret, self.md5code,hashkey, self.md5code,self.usr_id]
        self.db.query(sql, Lu)


        # data = {
        #     'token': ,
        #     'name': name,
        #     'key':key,
        #     'secret': secret,
        # }
        # sql="select weid from ims_wechats where usr_id=%s"
        # l,t=self.db.select(sql,[self.usr_id])
        # if t==0:
        #     data['usr_id']=self.usr_id
        #     self.db.insert('ims_wechats', data)
        #     #self.oTOLL.update()
        #     dR['code'] = '0'
        #     return dR
        #
        # id=l[0][0]
        # self.db.update('ims_wechats', data, " weid = %s " % (id))
        self.oTOLL.update()

        dR['code'] = '0'
        dR['MSG'] = '修改成功'
        return dR
        # 更新数据缓存






