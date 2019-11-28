# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/J001_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cJ001_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['用户ID','用户名','登录帐号','创建时间','最后修改时间','最后登录时间','最后登录IP']


    def mRight(self):


        sql = """
            select usr_id  --0
                
                ,login_id  --2
                ,to_char(ctime,'YYYY-MM-DD')  --6+2
                ,to_char(utime,'YYYY-MM-DD')  --8+2
                ,last_login --9+2
                ,last_ip --10+2
             from users u
             where usr_id_p=%s
        """%self.usr_id
        

        self.qqid = self.GP('qqid','')

        self.pageNo=self.GP('pageNo','')
        if self.pageNo=='':self.pageNo='1'
        self.pageNo=int(self.pageNo)

        sql+=" ORDER BY usr_id DESC"

        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {'dept_id':2}
        sql = """
            select u.login_id --登录名
                   ,u.usr_name --用户名
                   ,u.status
                   ,u.mobile --手机
            from users u
            where u.usr_id = %s and u.usr_id_p=%s
        """
        if pk != '':
            L = self.db.fetch( sql,[pk,self.usr_id_p] )

        return L

    
    def local_add_save(self):
        

        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        
        #这些是操作权限
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}  
        pk = self.pk

        dR={'R':'','MSG':''}
        if self.usr_id!=self.usr_id_p:
            dR['R'] = '1'
            dR['MSG'] = '非主帐号不能操作'
            return dR
        
        #获取表单参数
        usr_name = self.REQUEST.get('usr_name','')  #用户名
        mobile   = self.REQUEST.get('mobile','')    #手机
        status  = self.REQUEST.get('status','')  #状态
        respw =self.REQUEST.get('respw','')#恢复密码
        login_id_p=self.dActiveUser.get('login_id')
        login_id=login_id_p+'_'+usr_name
        if pk == '':
            sql="SELECT count(login_id) FROM users WHERE login_id='%s'"%(login_id)
            lT,iN=self.db.select(sql)
            if lT[0][0]>0:
                dR={'R':'1','MSG':'登录名已存在，保存失败!'}
                return dR
        
        if login_id == '':
            dR['R'] = '1'
            dR['MSG'] = '请输入登录名'
            return dR


        if pk != '':  #update

            #如果是更新，就去掉cid，ctime 的处理.
            if str(respw)=='1':
                sql="""
                    update users set password = crypt('Aa123456', gen_salt('md5')),uid=%s,utime=now() where usr_id = %s
                """%(self.usr_id,pk)
                self.db.query(sql)
            sql = """
                update users set mobile='%s',status=%s,uid=%s,utime=now() where usr_id = %s
            """ % (mobile,status,self.usr_id,pk)

            self.db.query(sql)

            dR['pk'] = pk

            
        else:  #insert 
            
            #如果是插入 就去掉 uid，utime 的处理
            sql="""insert into users(login_id, password, usr_name, status, usr_type, dept_id, del_flag, isadmin, is_dept_admin, sort,cid,ctime,mobile,usr_id_p)
            values('%s', crypt('Aa123456', gen_salt('md5')), '%s', %s, 1, 2, 0, 0, 0, 0,%s,now(),'%s',%s);
            """%(login_id,usr_name,status,self.usr_id,mobile,self.usr_id)
            self.db.query(sql)

        return dR


    
        
    def delete_data(self):
        
        """删除数据
        """
        dR = {'R': '', 'MSG': ''}
        if self.usr_id != self.usr_id_p:
            dR['R'] = '1'
            dR['MSG'] = '非主帐号不能删除'
            return dR
        pk = self.pk
        u = self.db.fetch("select 1 from users where usr_id= %s" % pk)

        if not u:
            dR={'R':'1','MSG':'数据不存在'}
        else:
            self.db.query("update  users set del_flag=1 where usr_id= %s" % pk)
            #self.db.query("delete from user_book where uid= %s" % pk)
            #self.db.query("delete from user_info where uid= %s" % pk)
            #self.db.query("update users set usr_id2=0 ,login_id=''   where  usr_id2= %s" % pk)
        return dR
    def get_status(self):
        sql="select id,txt1 from mtc_t where type='YESNO'"
        l,t=self.db.select(sql)
        return l
