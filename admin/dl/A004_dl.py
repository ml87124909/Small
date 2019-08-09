# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/A004_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cA004_dl(cBASE_DL):
    def init_data(self):

        #以字典形式创建列表上要显示的字段 
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['',      "u.usr_id",             '',''],#0
            ['分类ID',      "u.usr_name",           '',''],#1
            ['分类名称', "u.usr_name", '', ''],  # 2
            ['分类类型',      "u.login_id",      '',''],#3
            ['分类海报',      "r.role_name",'',''],#4
            ['分类排序',        "d.cname",     '',''],#5
            ['添加时间',      "u1.usr_name",'',''],#6
            ['修改时间',    "u.ctime",               '',''],#7
            ['分类级别',  "u2.usr_name",'',''],#8
            ['上级分类',"u.utime",               '',''],#9

            
        ]

        self.GNL = self.parse_GNL([0,1,2,3,4,6])


    def mRight(self):
            
        sql = u"""
            select id
                ,cname
                ,ctype
                ,pic
                ,to_char(ctime,'YYYY-MM-DD HH24:MI')ctime
               
            from cms_fl 
            where COALESCE(del_flag,0)=0 and usr_id=%s
        """%self.usr_id_p

        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {}

        if pk != '':
            sql = """
                 select id
                    ,cname
                    ,ctype
                    ,pic
                    ,sort
                    ,status
                from cms_fl 
                where COALESCE(del_flag,0)=0 and usr_id=%s and id=%s
                    """
            L = self.db.fetch( sql,[self.usr_id_p,pk] )

        return L
    
    def local_add_save(self):

        pk = self.pk
        dR={'code':'','MSG':'保存成功'}

        #获取表单参数
        cname=self.GP('cname','')#名称
        ctype=self.GP('ctype','')#类型
        pic=self.GP('pic','') #海报
        sort=self.GP('sort','')#排序
        status = self.GP('status','')  # 排序

        data = {
                'cname':cname
                ,'ctype':ctype
                ,'pic':pic
                , 'sort': sort or None
                ,'status':status
        }
        try:
            if pk != '':  #update
                #如果是更新，就去掉cid，ctime 的处理.
                data['uid']=self.usr_id
                data['utime']=self.getToday(9)
                self.db.update('cms_fl' , data , "usr_id=%s and  id = %s " % (self.usr_id_p,pk))
                self.use_log('修改文章分类')
            else:  #insert
                #如果是插入 就去掉 uid，utime 的处理
                data['usr_id']=self.usr_id_p
                data['cid']=self.usr_id
                data['ctime']=self.getToday(9)
                self.db.insert('cms_fl' , data)
                self.use_log('增加文章分类')
            dR['pk'] = pk
            dR['code'] = '0'

        except:
            dR['code'] = '1'
            dR['MSG'] = '保存失败'
        return dR

    def delete_data(self):
        pk = self.pk
        dR = {'code':'', 'MSG':'保存成功'}
        try:
            self.db.query("update cms_fl set del_flag=1 where usr_id=%s and id= %s", [self.usr_id_p,pk])
            self.use_log('删除文章分类')
            dR['code'] = '0'
        except:
            dR['code'] = '1'
            dR['MSG'] = '保存失败'
        return dR
