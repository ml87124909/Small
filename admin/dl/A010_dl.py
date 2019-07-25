# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################

from imp import reload
from basic.publicw import DEBUG


if DEBUG == '1':    
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import hashlib , os , time , random

class cA010_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['','手机号码','昵称','类型','收支','变动积分','剩余积分','交易时间','备注']


    #在子类中重新定义         
    def myInit(self):
        self.src = 'A010'
        pass

    def mRight(self):
            
        sql = """
             select i.id
                ,COALESCE(w.phone,'')
                ,w.name
                ,i.type
                ,i.in_out
                ,i.amount
                ,i.now_amount
                ,i.ctime
                ,''
            from  integral_log i
            left join wechat_mall_user w on w.id=i.wechat_user_id 
            where i.usr_id=%s
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
            select c.id
                    
                    
                  
                  
            from menu_func c
            
            where  c.id=%s
           
        """ % pk
        if pk != '':
            L = self.db.fetch( sql )
        else:
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            danhao = time.strftime("%Y%m%d%H%M%S", timeArray)

            L['danhao']='cgdd'+danhao
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

        
        #获取表单参数
        danhao=self.GP('danhao')#单号
        sp_name=self.GP('sp_name')#商品名
        sp_bh=self.GP('sp_bh')#商品编号
        sp_type=self.GP('sp_type')#商品类型
        candi=self.GP('candi')#产地
        num=self.GP('num')#数量
        dw=self.GP('dw')#单位
        gys_id = self.GP('gys_id')  # 供应商ID
        money=self.GP('money')#进货价格
        in_date=self.GP('in_date')#进货时间
        beizhu=self.GP('beizhu')#备注



        
        # if danhao == '':
        #     dR['R'] = '1'
        #     dR['MSG'] = '请输入角色名字'
        
        data = {
                'danhao':danhao
                ,'sp_name':sp_name
                ,'sp_bh':sp_bh
                ,'sp_type':sp_type
                ,'candi':candi
                ,'num':num
                ,'dw':dw
                ,'gys_id':gys_id
                ,'money':money
                ,'in_date':in_date
                ,'beizhu':beizhu,
                'cid': self.usr_id,
                'ctime': self.getToday(6),
                'uid': self.usr_id,
                'utime': self.getToday(6)
        }


        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data.pop('cid')
            data.pop('ctime')
            #data.pop('random')

            self.db.update('cggl_cg' , data , " id = %s " % pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data.pop('uid')
            data.pop('utime')
            
            self.db.insert('cggl_cg' , data)
            pk = self.db.insertid('cggl_cg_id')#这个的格式是表名_自增字段
            dR['isadd'] = 1
        #self.listdata_save(pk,danhao)
        dR['pk'] = pk
        
        return dR
