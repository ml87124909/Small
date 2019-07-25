# -*- coding: utf-8 -*-

##############################################################################
#
#
#
##############################################################################


from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import hashlib , os , time , random

class cK003_dl(cBASE_DL):
    def init_data(self):
        self.usr_dept_id=self.dActiveUser['usr_dept'][0]
        #以字典形式创建列表上要显示的字段 
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['',      "u.usr_id",             '',''],#0
            ['标题',      "u.usr_name",           '',''],#1
            ['类型', "u.usr_name", '', ''],  # 2
            ['是否展示',      "u.login_id",      '',''],#3
            ['发布时间',      "r.role_name",'',''],#4
            ['内容',        "d.cname",     '',''],#5
            #['添加时间',      "u1.usr_name",'',''],#6
            #['更新时间',    "u.ctime",               '',''],#7
            #['添加时间',  "u2.usr_name",'',''],#8
            #['修改时间',"u.utime",               '',''],#9
            #['进货时间',      "u.last_login",'',''],#10
            #['备注',    "u.last_ip",               '','']#11
            
        ]
        #self.GNL=[] #列表上出现的
        #self.SNL=[]     #排序
        #self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0,1,2,3,4,5])


    #在子类中重新定义         
    def myInit(self):
        self.src = 'K003'
        pass

    def mRight(self):
            
        sql = u"""
            select id
                ,fenlei
                ,title
                ,tags
                ,keywords
                ,descript
                ,income
                ,author
                ,case when isshow=0 then '是' else '否' end 
                ,ctime
                ,content
            from cms_doc 
            where COALESCE(del_flag,0)=2 and  usr_id=%s
        """%self.usr_id
        # self.qqid = self.GP('qqid','')
        # self.orderby = self.GP('orderby','')
        # self.orderbydir = self.GP('orderbydir','')
        # self.pageNo=self.GP('pageNo','')
        # if self.pageNo=='':self.pageNo='1'
        # self.pageNo=int(self.pageNo)
        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+= self.QNL + " LIKE '%%%s%%' "%(self.qqid)
        # #ORDER BY
        # if self.orderby!='':
        #     sql+=' ORDER BY %s %s' % (self.orderby,self.orderbydir)
        # else:
        #     sql+=" ORDER BY r.role_id DESC"
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
            select id
                ,fenlei
                ,title
                ,tags
                ,keywords
                ,descript
                ,income
                ,author
                ,isshow
                ,status
                ,sort
                ,pic
                ,content
            from cms_doc  
            where  id=%s
        """ % pk
        if pk != '':
            L = self.db.fetch( sql )
        # else:
        #     timeStamp = time.time()
        #     timeArray = time.localtime(timeStamp)
        #     danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        #
        #     #L['danhao']='cgdd'+danhao
        #     L['danhao'] = ''
        return L
    
    def local_add_save(self):
        

        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        
        #这些是操作权限
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}  
        pk = self.pk
        #dR={'R':'','MSG':'','isadd':''}
        dR={'R':'','MSG':''}
        save_flag = self.REQUEST.get("save_flag").strip()
        save_flag2 = self.cookie.getcookie("__flag")
        
        
        #获取表单参数
        fenlei=self.GP('fenlei')#分类
        title=self.GP('title')#类型
        tags=self.GP('tags')#是否展示
        keywords=self.GP('keywords')#内容
        descript = self.GP('descript')  # 标题
        income = self.GP('income')  # 类型
        author = self.GP('author')  # 是否展示
        isshow = self.GP('isshow')  # 内容
        status = self.GP('status')  # 内容
        sort=self.GP('sort')
        container = self.GP('container')  # 内容



        # if not (save_flag == save_flag2):
        #     #为FALSE时,当前请求为重刷新
        #     return dR
        
        # if danhao == '':
        #     dR['R'] = '1'
        #     dR['MSG'] = '请输入角色名字'
        
        data = {
                'fenlei':fenlei
                ,'title':title
                ,'tags':tags
                ,'keywords':keywords
                ,'descript': descript
                , 'income': income
                , 'author': author
                , 'isshow': isshow
                ,'status':status
                ,'content':container
                ,'sort':sort
                ,'cid': self.usr_id
                ,'ctime': self.getToday(9)
                ,'uid': self.usr_id
                ,'utime': self.getToday(9)
                ,'usr_id':self.usr_id

        }
        for k in list(data):
            if data[k] == '':
                data.pop(k)

        from werkzeug import secure_filename
        try:
            file = self.objHandle.files['pic']
            if file:
                filename = secure_filename(file.filename)
                data['pic'] = filename  ##封面展示图片
                file.save(os.path.join(public.ATTACH_ROOT, filename))
        except:
            pass

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data.pop('cid')
            data.pop('ctime')
            #data.pop('random')

            self.db.update('cms_doc' , data , " id = %s " % pk)

        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data.pop('uid')
            data.pop('utime')

            self.db.insert('cms_doc' , data)
            pk = self.db.insertid('cms_doc_id')#这个的格式是表名_自增字段
            #dR['isadd'] = 1
        #self.listdata_save(pk,danhao)
        dR['pk'] = pk
        
        return dR

    def getfllist(self):
        L=[]
        sql="select id,name from cms_fl"
        l,t=self.db.select(sql)
        if t>0:
            L=l

        return L

    # def delete_data(self):
    #     pk = self.pk
    #     dR = {'R':'', 'MSG':''}
    #     self.db.query("update cms_doc set del_flag=1 where id= %s" % pk)
    #     return dR
