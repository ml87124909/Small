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

class cA009_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['','类型','满足条件','赠送积分','添加时间','修改时间']


    #在子类中重新定义         
    def myInit(self):
        self.src = 'A009'
        pass

    def mRight(self):
            
        sql = u"""
            select s.id
                ,m.txt1
                ,s.confine
                ,s.score
                ,to_char(s.ctime,'YYYY-MM-DD HH24:MI')
                ,to_char(s.utime,'YYYY-MM-DD HH24:MI')
            from score_send s
            left join mtc_t m on m.id=s.code and m.type='ZFZSGZ'
            where  COALESCE(s.del_flag,0)!=1  and s.usr_id=%s
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
                ,code
                ,confine
                ,score
            
            from score_send 
            
            where  id=%s
           
        """ % pk
        if pk != '':
            L = self.db.fetch( sql )

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
        code=self.GP('code')#类型
        confine=self.GP('confine')# 满足条件:
        score=self.GP('score')# 赠送积分:

        #
        # sp_type=self.GP('sp_type')#商品类型
        # candi=self.GP('candi')#产地
        # num=self.GP('num')#数量
        # dw=self.GP('dw')#单位
        # gys_id = self.GP('gys_id')  # 供应商ID
        # money=self.GP('money')#进货价格
        # in_date=self.GP('in_date')#进货时间
        # beizhu=self.GP('beizhu')#备注



        # if danhao == '':
        #     dR['R'] = '1'
        #     dR['MSG'] = '请输入角色名字'
        
        data = {
                'code':code
                ,'confine':confine
                ,'score':score
                ,'usr_id':self.usr_id
                ,'del_flag':0
                ,'cid': self.usr_id
                ,'ctime': self.getToday(9)
                ,'uid': self.usr_id
                ,'utime': self.getToday(9)
        }



        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data.pop('cid')
            data.pop('ctime')
            #data.pop('random')

            self.db.update('score_send' , data , " id = %s " % pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data.pop('uid')
            data.pop('utime')
            
            self.db.insert('score_send' , data)
            pk = self.db.insertid('score_send_id')#这个的格式是表名_自增字段
            dR['isadd'] = 1
        #self.listdata_save(pk,danhao)
        dR['pk'] = pk
        
        return dR

    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update score_send set del_flag=1 where id= %s" % pk)
        return dR


