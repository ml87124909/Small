# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/H001_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cH001_dl(cBASE_DL):


    def getInfo(self):
        sql="""
        select  convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII') as login_id 
        from users where usr_id = %s
        """
        info  =  self.db.fetch(sql ,[self.md5code,self.usr_id])
        return info

    def local_add_save(self):
        dR={'code':'','MSG':'保存成功'}
        login_id = self.GP('login_id','')
        password = self.GP('password','')
        password2 = self.GP('password2','')

        if login_id=='':
            dR['code'] = '1'
            dR['MSG'] = '登录名不能为空!'
            return dR

        sql="""
         select usr_id from users 
         where  convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII')=%s and usr_id!=%s
        """
        l,t=self.db.select(sql,[self.md5code,login_id,self.usr_id])
        if t>0:
            dR['code'] = '1'
            dR['MSG'] = '当前登录名已存在'
            return dR

        if password != '' :
            if password2 != password:
                dR['code'] = '1'
                dR['MSG'] = '确认密码必须和新密码相同'
                return dR
            sql = "select usr_id from users where usr_id = %s;"
            l, t = self.db.select(sql, [self.usr_id])
            if t> 0:
                sql = "update users set login_id=encrypt(%s,%s,'aes'),passwd= crypt(%s, gen_salt('md5')) where usr_id=%s"
                parm = [login_id, self.md5code, password, self.usr_id]
                self.db.query(sql, parm)
                self.use_log('修改个人帐号%s' % self.usr_id)
                return dR


        sql = "update users set login_id=encrypt(%s,%s,'aes')  where usr_id=%s"
        parm = [login_id, self.md5code, self.usr_id]
        self.db.query(sql, parm)
        self.use_log('修改个人帐号%s' % self.usr_id)
        dR['MSG'] = '登录名保存成功'
        return dR


