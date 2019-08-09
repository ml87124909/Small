# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/H002_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cH002_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['角色ID','角色名','所属用户ID','创建ID',
                    '创建时间','最后修改ID','最后修改时间']

    def mRight(self):
            
        sql = u"""
        select r.role_id                                   -- 0 角色id 
              ,r.role_name                                 -- 1 角色名
              ,r.dept_id
              ,r.cid               -- 5 创建人
              ,to_char(r.ctime,'YYYY-MM-DD')     -- 6 创建时间
              ,r.uid                -- 7 最后修改人
              ,to_char(r.utime,'YYYY-MM-DD')  -- 8 最后修改时间
        from roles r 
        where coalesce(del_flag,0)=0
        """
        self.qqid = self.GP('qqid','')

        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+= self.QNL + "role_name  LIKE '%%%s%%' "%(self.qqid)
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
        select COALESCE (role_name,'') as role_name from roles where role_id = %s
        """
        if pk != '':
            L = self.db.fetch( sql,[pk] )
        return L

    def getMenuRoleList(self,roleId=0):
        
        """获取权限列表，默认显示全部菜单的权限情况，如果有 roleid 就显示对应这个roleId的情况
        """
        
        L = []
        
        sql = """
        select * from  p_getMenuRightList(%s);
        """ % roleId
        lT,iN = self.db.fetchall(sql)
        L = []
        for e in lT:
            if e not in L:
                L.append(e)
        return L

    def local_add_save(self):
        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
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
        dR={'code':'0','MSG':'角色权限列表保存成功'}
        from random import Random
        import time
        
        ranCode = str(Random(time.time()).random())[2:]
        #获取表单参数
        roleName = self.REQUEST.get('roleName','')  #角色名
        
        if roleName == '':
            dR['code'] = '1'
            dR['MSG'] = '请输入角色名字'
        
        data = {'role_name':roleName}

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            
            data['uid']=self.usr_id
            data['utime']=self.getToday(6)
            self.db.update('roles' , data , " role_id = %s " % pk)

        else:  #insert 
            
            #如果是插入 就去掉 uid，utime 的处理
            data['dept_id'] = self.dept_id
            data['random_no'] = ranCode
            data['cid']=self.usr_id
            data['ctime']=self.getToday(6)
            
            self.db.insert('roles' , data)

        #保存权限列表修改情况
        if pk not in ['',None,'Null']:
            roleId = pk
        else:
            sql = """ select role_id from roles where random_no=%s """
            lT,iN=self.db.select(sql,[ranCode])
            if iN > 0:
                roleId = lT[0][0]
            else:
                roleId = 0

        rs = self.saveRoleMenuList(roleId,seeStr,addStr,delStr,updStr)
        
        if rs == 'error':
            dR['code'] = '1'
            dR['MSG'] = '角色权限列表保存失败'
        dR['pk'] = pk
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
        pk = self.pk
        l,t = self.db.select("select 1 from roles where role_id= %s" , [pk])

        if t==0:
            dR={'code':'1','MSG':'数据不存在'}
        else:
            self.db.query("update roles set del_flag=1 where role_id= %s" ,[pk])
            self.db.query("delete from role_menu where role_id = %s ",[pk])
            self.db.query("delete from usr_role where role_id = %s ",[pk])
            dR = {'code': '0', 'MSG': '删除成功'}
        return dR


