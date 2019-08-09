# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/J002_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cJ002_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['角色ID','角色名']



    def mRight(self):
            
        sql = u"""
        select r.role_id                                   -- 0 角色id 
              ,r.role_name                                 -- 1 角色名
             
        from roles r 
      
       
        where r.dept_id=%s
          
        """%self.usr_id
        self.qqid = self.GP('qqid','')

        self.pageNo=self.GP('pageNo','')
        if self.pageNo=='':self.pageNo='1'
        self.pageNo=int(self.pageNo)
        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+= self.QNL + " LIKE '%%%s%%' "%(self.qqid)
        #ORDER BY
        sql+=" ORDER BY r.role_id DESC"

        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
        select COALESCE (role_name,'') as role_name
              ,COALESCE (sort,null)      as sort
              ,COALESCE (dept_id,null)   as dept_id
              ,COALESCE (memo,'')      as memo
          from roles
         where role_id = %s
        """
        if pk != '':
            L = self.db.fetch( sql,pk )
        return L

    def get_My_Roles(self,pk):
        L=[]
        if pk=='':
            sql="select role_id from usr_role where usr_id=%s"
            l,t=self.db.select(sql,self.usr_id)
            if t>0:
                for i in l:
                    roleId=i[0]
                    j=self.getMenuRoleList(roleId)
                    L=L+j
        else:
            L=self.getMenuRoleList(pk)
        return L


    def getMenuRoleList(self,roleId=0):
        L = []
        sql = """
        select * from  p_getmenurightlist_s(%s);
        """ % roleId
        lT,iN = self.db.fetchall(sql)
        for e in lT:
            if e not in L:
                L.append(e)
        return L

    def local_add_save(self):
        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        dR = {'R': '', 'MSG': ''}
        if self.usr_id!=self.usr_id_p:
            dR['R'] = '1'
            dR['MSG'] = '非主帐号不能操作'
            return dR

        #这些是操作权限
        seeList = self.REQUEST.getlist('see')
        addList = self.REQUEST.getlist('add')
        delList = self.REQUEST.getlist('del')
        updList = self.REQUEST.getlist('upd')


        if seeList not in ['',None,0] and type(seeList)==list:
            seeStr = ','.join(seeList)
        else:
            seeStr = seeList
        
        if addList not in ['',None,0] and type(addList)==list:
            addStr = ','.join(addList)
        else:
            addStr = addList
            
        if delList not in ['',None,0] and type(delList)==list:
            delStr = ','.join(delList)
        else:
            delStr = delList
            
        if updList not in ['',None,0] and type(updList)==list:
            updStr = ','.join(updList)
        else:
            updStr = updList
        
        pk = self.pk
        dR={'R':'','MSG':''}


        from random import Random
        import time
        
        ranCode = str(Random(time.time()).random())[2:]
        
        #获取表单参数
        roleName = self.REQUEST.get('roleName','')  #角色名
        sort     = self.REQUEST.get('sort','')      #排序号

        

        
        if roleName == '':
            dR['R'] = '1'
            dR['MSG'] = '请输入角色名字'
        
        data = {
                'role_name' : roleName , 
                'sort'      : sort ,
                'cid'       : self.usr_id,
                'ctime'     : self.getToday(6),
                'uid'       : self.usr_id,
                'utime'     : self.getToday(6),
                'random'    : ranCode
        }

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            
            data.pop('cid')
            data.pop('ctime')
            data.pop('random')

            self.db.update('roles' , data , " role_id = %s " % pk)
            
        else:  #insert 
            
            #如果是插入 就去掉 uid，utime 的处理
            data['dept_id'] =self.usr_id_p
            data.pop('uid')
            data.pop('utime')
            
            self.db.insert('roles' , data)
            
        #保存权限列表修改情况
        if pk not in ['',None,'Null']:
            roleId = pk
        else:
            sql = """ select role_id from roles where random='%s' """%ranCode

            lT,iN=self.db.select(sql)

            if iN > 0:
                roleId = lT[0][0]
            else:
                roleId = 0

        rs = self.saveRoleMenuList(roleId,seeStr,addStr,delStr,updStr)
        
        if rs == 'error':
            dR['R'] = '1'
            dR['MSG'] = '角色权限列表保存失败'
        
        return dR

    def saveRoleMenuList(self,roleId,seeStr,addStr,delStr,updStr):
        
        """保存权限列表
        """
        if seeStr == '':
            seeStr = '0'
        if addStr == '':
            addStr = '0'
        if delStr == '':
            delStr = '0'
        if updStr == '':
            updStr = '0'
        result = 'error' #返回标志
        
        if roleId not in [0,'','Null',None] :
            sql = "select * from  p_save_roleMenu(%s, '%s','%s','%s','%s',%s)" % (roleId, seeStr, addStr, delStr, updStr, self.usr_id)
            self.db.query(sql)
            
            result = 'ok' #执行没问题就算成功了
        
        return result
        
    def delete_data(self):
        
        """删除数据
        """
        dR = {'R': '', 'MSG': ''}
        if self.usr_id != self.usr_id_p:
            dR['R'] = '1'
            dR['MSG'] = '非主帐号不能删除'
            return dR
        pk = self.pk
        u = self.db.fetch("select 1 from roles where dept_id=%s and role_id= %s" ,[self.usr_id_p,pk])
        dR={'R':'','MSG':''}
        if not u:
            dR={'R':'1','MSG':'数据不存在'}
        else:
            self.db.query("delete from roles where role_id= %s" % pk)
            self.db.query("delete from role_menu where role_id = %s "%pk)
            self.db.query("delete from usr_role where role_id = %s "%pk)
        return dR


