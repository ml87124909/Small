# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/A005_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cA005_dl(cBASE_DL):
    def init_data(self):

        #以字典形式创建列表上要显示的字段 
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['文章ID',      "u.usr_id",             '',''],#0
            ['文章分类',      "u.usr_name",           '',''],#1
            ['文章标题', "u.usr_name", '', ''],  # 2
            ['文章类型',      "u.login_id",      '',''],#3
            ['文章海报',      "r.role_name",'',''],#4
            ['创建时间',        "d.cname",     '',''],#5

            
        ]

        self.GNL = self.parse_GNL([0,1,2,3,4,5])


    def mRight(self):
            
        sql = u"""
            select cd.id
                ,cf.cname
                ,cd.title
                ,cd.ctype 
                ,cd.pic
                ,to_char(cd.ctime,'YYYY-MM-DD HH24:MI')ctime
             
            from cms_doc cd
            left join cms_fl cf on cf.id=cd.class_id and cf.usr_id=cd.usr_id
            where COALESCE(cd.del_flag,0)=0 and cd.usr_id=%s
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
                ,class_id
                ,title
                ,keywords
                ,ctype
                ,sort
                ,pic
                ,contents
                ,sketch
                ,recom
                ,goods
                ,status
            from cms_doc  
            where  id=%s and usr_id=%s and COALESCE(del_flag,0)=0 
        """
            L = self.db.fetch( sql,[pk,self.usr_id_p] )

        return L
    
    def local_add_save(self):
        pk = self.pk
        dR={'code':'1','MSG':'处理失败'}

        #获取表单参数
        class_id=self.GP('class_id','')#分类
        title=self.GP('title','')#名称
        keywords=self.GP('keywords','')#关键字
        ctype = self.GP('ctype','')  # 标题
        sort=self.GP('sort','')
        status = self.GP('status', '')
        sketch=self.GP('sketch','')
        contents = self.REQUEST.get('text_contents', '')  # 详情介绍
        pic = self.GP('pic', '')#封面图片
        recom=self.GP('recom','')
        goods = self.GP('goods_id', '')
        
        data = {
                'class_id': class_id or None
                ,'title':title
                ,'keywords':keywords
                ,'pic': pic
                ,'contents':contents
                , 'sort': sort or None
                ,'ctype':ctype
                ,'sketch':sketch
                ,'recom':recom
                , 'goods': goods
                ,'status':status
        }


        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data['uid']=self.usr_id
            data['utime']=self.getToday(9)
            self.db.update('cms_doc' , data , " id = %s and usr_id=%s" % (pk,self.usr_id_p))
            self.use_log('修改文章')
            dR['code']='0'
            dR['MSG'] = '修改成功'

        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data['usr_id'] = self.usr_id_p
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            self.db.insert('cms_doc' , data)
            self.use_log('增加文章')
            dR['code'] = '0'
            dR['MSG'] = '增加成功'
        dR['pk'] = pk
        
        return dR

    def getfllist(self):
        L=[['','请新建文章分类']]
        sql="select id,cname from cms_fl where COALESCE(del_flag,0)=0 and COALESCE(status,0)=0 and usr_id=%s"
        l,t=self.db.select(sql,self.usr_id_p)
        if t>0:
            L=l
        return L

    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update cms_doc set del_flag=1 where id= %s and usr_id=%s" , [pk,self.usr_id_p])
        self.use_log('删除文章')
        return dR
