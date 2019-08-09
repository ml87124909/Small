# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/I003_dl.py"""


from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cJ003_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['ID','用户名','角色']



    def mRight(self):
            
        sql = u"""
        select a.usr_id       
            ,a.login_id
           
            ,COALESCE((select array_to_string(ARRAY(SELECT unnest(array_agg(role_name))),',') from roles where role_id in( select role_id from usr_role where usr_id=a.usr_id)),null ) as usr_role
          from users a 
         
         where a.del_flag = 0  and usr_id_p=%s
        """%self.usr_id
        # if self.unit_id != 1:
        #     sql+=u" and a.h_id = %s "%self.unit_id
            
        self.qqid = self.GP('qqid','')

        self.pageNo=self.GP('pageNo','')
        if self.pageNo=='':self.pageNo='1'
        self.pageNo=int(self.pageNo)
        if self.qqid!='':
            sql+= " and a.login_id LIKE '%%%s%%' "%(self.qqid)

        sql+=" ORDER BY  a.usr_id desc"
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def getParentDept(self):
        sql = """
        select id, cname from dept where parent_id = 0 order by id asc
        """
        L,t  = self.db.fetchall(sql)
        return L

    def get_local_data(self , pk):
        if pk != '':   
            L = self.db.fetch("""select a.usr_id , a.usr_name 
            from users a where a.usr_id = '%s'""" % pk)
            L['rolelist'],t = self.db.fetchall("""
            select role_id , role_name from roles where dept_id=%s order by sort asc
            """%self.usr_id)
            userrole,t = self.db.fetchall("select role_id from usr_role where usr_id = %s" % pk)
            temp = []
            for ur in userrole:
                temp.append(ur.get('role_id'))
            L['userrole'] = temp
        else:
            L = {}
        return L

   

    def local_add_save(self):

        dR = {'R': '', 'MSG': ''}
        if self.usr_id != self.usr_id_p:
            dR['R'] = '1'
            dR['MSG'] = '非主帐号不能操作'
            return dR

        pk = self.pk

        role_id = self.REQUEST.getlist('role_id')
        self.db.query('delete from usr_role where usr_id = %s' % self.pk)

        for id in role_id:
            self.db.query("insert into usr_role (usr_id , role_id,usr_name , cid , ctime , uid, utime,access_son) values (%s , %s ,'%s', %s , '%s', %s , '%s',0)" % (
                self.pk , id,self.usr_name , self.usr_id , self.getnow, self.usr_id , self.getnow
            ))
        
        dR['pk'] = pk
        return dR
   
