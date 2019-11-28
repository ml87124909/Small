# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/H004_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cH004_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['ID','用户名','角色']


    def mRight(self):
            
        sql = u"""
        select a.usr_id       
            , convert_from(decrypt(a.login_id::bytea, %s, 'aes'),'SQL_ASCII')
           
            ,COALESCE((select array_to_string(ARRAY(SELECT unnest(array_agg(role_name))),',') from roles where role_id in( select role_id from usr_role where usr_id=a.usr_id)),null ) as usr_role
          from users a 
         
         where COALESCE(a.del_flag,0) = 0  
        """
        parm=[self.md5code]
            
        self.qqid = self.GP('qqid','')

        self.pageNo=self.GP('pageNo','')
        if self.pageNo=='':self.pageNo='1'
        self.pageNo=int(self.pageNo)
        if self.qqid!='':
            sql+= " and a.login_id LIKE %s "
            parm.append('%%%s%%'%(self.qqid))


        #ORDER BY 

        sql+=" ORDER BY  a.usr_id desc"
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo,L=parm)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        if pk != '':   
            L = self.db.fetch("""select a.usr_id ,  convert_from(decrypt(a.login_id::bytea,%s, 'aes'),'SQL_ASCII') as login_id 
            from users a where a.usr_id = %s""", [self.md5code,pk])
            L['rolelist'],t = self.db.fetchall("""
            select role_id , role_name from roles order by sort asc
            """)
            userrole,t = self.db.fetchall("select role_id from usr_role where usr_id = %s" % pk)
            temp = []
            for ur in userrole:
                temp.append(ur.get('role_id'))
            L['userrole'] = temp
        else:
            L = {}
        return L

   

    def local_add_save(self):
        pk = self.pk
        dR={'code':'0','MSG':'保存成功'}
        try:
            role_id = self.REQUEST.getlist('role_id')
            self.db.query('delete from usr_role where usr_id = %s' % self.pk)

            for id in role_id:
                sql="""
                insert into usr_role (usr_id , role_id,usr_name , cid , ctime , access_son)
                values (%s , %s ,%s, %s , now(), 0)
                """
                self.db.query(sql,[self.pk ,id,self.usr_name , self.usr_id])

            dR['pk'] = pk
        except:
            dR['code'] = '1'
            dR['MSG'] = '保存失败'
        return dR
   
