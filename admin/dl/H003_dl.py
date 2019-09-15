# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/H003_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import time
class cH003_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['用户ID','登录帐号','注册时间','到期时间','最后登录时间','最后登录IP']


    def mRight(self):


        sql = """
            select usr_id 
                ,convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII')
                ,to_char(ctime,'YYYY-MM-DD HH24:MI')
                ,to_char(expire_time,'YYYY-MM-DD HH24:MI')
                ,last_login 
                ,last_ip 
             from users u
        """
        parm=[self.md5code]
        self.qqid = self.GP('qqid','')

        if self.qqid!='':
            sql+= " where u.login_id LIKE %s "
            parm.append('%%%s%%' % (self.qqid))

        #ORDER BY
        sql+=" ORDER BY u.usr_id DESC"

        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo,L=parm)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        L = {}
        sql = """
            select 
                usr_id
                 ,convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII') as login_id --登录名
                  ,status
                    ,to_char(expire_time,'YYYY-MM-DD HH24:MI')expire_time
                    ,qiniu_flag
                    ,vip_flag
                    ,oss_flag
            from users 
            where usr_id = %s
        """
        if pk != '':
            L = self.db.fetch( sql ,[self.md5code,pk])
        return L

    
    def local_add_save(self):

        pk = self.pk
        dR={'code':'0','MSG':'保存成功'}
        login_id = self.GP('login_id', '')  # 状态
        status  = self.GP('status','')  #状态
        respw =self.GP('respw','')#恢复密码
        expire_time =self.GP('expire_time','')#到期时间
        qiniu_flag = self.GP('qiniu_flag', '')  # 用户自定义标识
        vip_flag = self.GP('vip_flag', '')  # 系统版本
        oss_flag = self.GP('oss_flag', '')  # OSS版本

        sql="select usr_id from users where convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII')=%s"
        parm=[self.md5code,login_id]
        if pk != '':
            sql = "select usr_id from users where convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII')=%s and usr_id!=%s"
            parm = [self.md5code, login_id,pk]
        l,t=self.db.select(sql,parm)

        if t>0:
            dR = {'code': '1', 'MSG': '登录名有重复!'}
            return dR
        if pk=='':
            random_no='%s'%time.time()
            data={'random_no':random_no,'cid':self.usr_id,'ctime':self.getToday(9)}
            self.db.insert('users',data)
            pk = self.db.fetchcolumn('select usr_id from users where random_no=%s', random_no)
            sql = """
                update users set passwd = crypt('Aa123456', gen_salt('md5')),
                login_id=encrypt(%s,%s,'aes'),uid=%s,utime=now() where usr_id = %s
                 """
            self.db.query(sql, [login_id,self.md5code,self.usr_id, pk])
        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            if str(respw)=='1':
                sql="""
                    update users set passwd = crypt('Aa123456', gen_salt('md5')),uid=%s,utime=now() where usr_id = %s
                """
                self.db.query(sql, [self.usr_id, pk])
            sql = """
                update users set login_id=encrypt(%s,%s,'aes'),status=%s,uid=%s,utime=now() where usr_id =%s
            """
            self.db.query(sql, [login_id or None, self.md5code,status, self.usr_id, pk])

            # sql = """
            #     update users set expire_time=%s,status=%s,uid=%s,utime=now()
            #     --,qiniu_flag=%s,vip_flag=%s,oss_flag=%s
            #     where usr_id = %s
            # """
            # self.db.query(sql, [expire_time or None, status, self.usr_id, qiniu_flag or None, vip_flag or None, oss_flag or None, pk])
            # sql="""select coalesce(expire_flag,0) from users
            #         where to_char(expire_time,'YYYY-MM-DD')>to_char(now(),'YYYY-MM-DD') and usr_id = %s  and status=1
            #         """
            # l,t=self.db.select(sql,[pk])
            # if t>0 or vip_flag=='7':
            #     if str(l[0][0])=='1':
            #         sql = """update users set expire_flag=0 where usr_id = %s """
            #         self.db.query(sql,[pk])
            #         # 进行缓存更新
            #
            #         self.oSHOP.update(pk)
            #         self.oSHOP_T.update(pk)
            #         self.oUSER.update(pk)
            #         self.oGOODS.update(pk)
            #         self.oGOODS_SELL.update(pk)
            #         self.oGOODS_D.update(pk)
            #         self.oGOODS_N.update(pk)
            #         self.oGOODS_G.update(pk)
            #         self.oCATEGORY.update(pk)
            #         self.oGOODS_PT.update(pk)
            #         self.oGOODS_DPT.update(pk)
            #         self.oPT_GOODS.update(pk)

            dR['pk'] = pk

        return dR


    
        
    def delete_data(self):
        
        """删除数据
        """
        
        pk = self.pk
        u = self.db.fetch("select 1 from users where usr_id= %s" % pk)
        dR={'code':'0','MSG':'删除成功'}
        if not u:
            dR={'code':'1','MSG':'数据不存在'}
        else:
            self.db.query("update  users set del_flag=1 where usr_id= %s" % pk)

        return dR
    def get_status(self):
        sql="select id,txt1 from mtc_t where type='YESNO'"
        l,t=self.db.select(sql)
        return l

    def get_toll(self):
        sql = "select combo_one_name,combo_two_name,combo_thr_name,oss_one_size,oss_two_size,oss_thr_size from toll_config"
        l, t = self.db.select(sql)
        combo_one_name, combo_two_name, combo_thr_name, oss_one_size, oss_two_size, oss_thr_size = l[0]
        L1 = [['1', combo_one_name], ['2', combo_two_name], ['3', combo_thr_name]]
        L2 = [['4', oss_one_size], ['5', oss_two_size], ['6', oss_thr_size]]
        return L1, L2
