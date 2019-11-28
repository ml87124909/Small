# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/C001_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cC001_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['','分类排序','分类名称','分类类型','分类图标','分类海报']


    def mRight(self):
            
        sql = u"""
             select 
                id
                ,paixu
                ,cname
                ,ctype
                ,pic_icon
                ,pic_imgs
                ,pid
                ,ilevel
                
            from category
           
            where COALESCE(del_flag,0)=0 and usr_id=%s
            
        """
        parm=[self.usr_id_p]
        self.qqid = self.GP('qqid','')
        if self.qqid!='':
            sql+= "and cname LIKE %s "
            parm.append('%%%s%%'%self.qqid)

        pageNo=self.GP('pageNo','')
        if pageNo=='':
            pageNo='1'
        pageNo=int(pageNo)

        sql+="order by ilevel,paixu "

        l,t=self.db.select(sql,parm)
        if t==0:
            return [0,0,0,0],[]
        List=[]
        L1,L2=[],[]
        for i in l:
            if i[7]==1:
                L1.append(i)
            else:
                i[2]='╚═══'+i[2]
                L2.append(i)
        for j in L1:
            List.append(j)
            for m in L2:
                if j[0]==m[6]:
                    List.append(m)
        m=len(List)
        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(List, m, pageNo=pageNo,
                                                                                select_size=10)
        #L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,pageNo,L=parm)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]

        return PL,L

    def get_local_data(self):
        """获取 local 表单的数据
        """
        L = {}

        if self.pk != '':
            sql = """
                select id,cname,ctype,pid,pic_icon,pic_imgs,paixu,remark,status from category where usr_id=%s and id=%s
                """
            L = self.db.fetch(sql,[self.usr_id_p,self.pk] )

        return L
    
    def local_add_save(self):

        #这些是操作权限

        pk = self.pk
        dR={'code':'','MSG':'处理失败'}

        
        #获取表单参数
        cname=self.GP('cname','')#名称
        ctype=self.GP('ctype','')#类型
        pid=self.GP('pid','') #上级分类
        pic_icon=self.GP('pic_icon','')#图标
        pic_imgs = self.GP('pic_imgs', '')#海报
        paixu=self.GP('paixu',0)#排序
        status = self.GP('status', '')  # 状态
        remark = self.GP('remark', '')  #备注

        level=1
        if int(pid)!=0:
            level=2


        
        data = {
                'cname':cname
                ,'ctype':ctype
                ,'pid':pid
                ,'pic_icon':pic_icon
                ,'pic_imgs':pic_imgs
                ,'paixu':int(paixu)
                ,'cid': self.usr_id
                ,'ctime': self.getToday(9)
                ,'uid': self.usr_id
                ,'utime': self.getToday(9)
                ,'usr_id':self.usr_id_p
                ,'ilevel':level
                ,'remark':remark
                ,'status':status
        }

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data.pop('cid')
            data.pop('ctime')
            self.db.update('category' , data , " id = %s " % pk)
            self.use_log('修改商品分类%s' % pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data.pop('uid')
            data.pop('utime')
            self.db.insert('category' , data)
            self.use_log('增加商品分类')
        self.oSHOP.update(self.usr_id_p)
        self.oGOODS_D.update(self.usr_id_p)
        self.oGOODS.update(self.usr_id_p)
        self.oGOODS_N.update(self.usr_id_p)
        self.oCATEGORY.update(self.usr_id_p)
        dR['pk'] = pk
        dR['code'] = '0'
        dR['MSG'] = '处理成功'
        return dR

    def getfllist(self):
        L=[[0,'顶级分类']]
        sql="""select id,cname from category 
                where usr_id=%s and COALESCE(del_flag,0)=0 and ilevel=1 """
        parm=[self.usr_id_p]
        if self.pk!='':
            sql+="and id!=%s"
            parm.append(self.pk)
        sql+="order by paixu "

        l,t=self.db.select(sql,parm)
        if t>0:
            for r in l:
                L.append(r)
        return L

    def delete_data(self):
        pk = self.pk
        dR = {'code':'', 'MSG':''}
        l,t=self.db.select("select ilevel from category  where id= %s and usr_id=%s" ,[pk,self.usr_id_p])
        if t==0:
            dR['MSG']='数据不存在'
            return dR
        level=l[0][0]
        if str(level)=='1':
            self.db.query("update category set del_flag=1 where pid=%s and usr_id=%s", [pk, self.usr_id_p])
        elif str(level)=='2':
            self.db.query("update category set del_flag=1 where pid=%s and usr_id=%s", [pk, self.usr_id_p])
        self.db.query("update category set del_flag=1 where id=%s and usr_id=%s" ,[pk,self.usr_id_p])
        self.oGOODS_D.update(self.usr_id_p)
        self.oSHOP.update(self.usr_id_p)
        self.oCATEGORY.update(self.usr_id_p)
        self.use_log('删除商品分类%s' % pk)
        dR['MSG'] = '删除成功'
        dR['code'] = '0'
        return dR

    def setfllist(self):
        L=[[0,'请选择分类']]
        sql="select id,cname from category where usr_id=%s and COALESCE(del_flag,0)=0 and ilevel=1"
        l,t=self.db.select(sql,self.usr_id_p)
        if t>0:
            for r in l:
                L.append(r)
        return L