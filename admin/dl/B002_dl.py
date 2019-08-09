# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/B002_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cB002_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['','标签名称','总用户','可推送','推送模板消息']


    def mRight(self):
            
        sql = u"""
            select w.id,m.txt1,'',''
              
            from wechat_mall_user w
           left join mtc_t m on m.id=w.usr_level and m.type='TAG'
            where w.usr_id=%s and COALESCE(w.del_flag,0)=0
        """%self.usr_id_p

        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self ):
        """获取 local 表单的数据
        """
        L = {}
        # sql = """
        #    select usr_id
        #         ,s_keywords
        #         ,num_time
        #         ,s_keywords
        #         ,money
        #         ,amount
        #         ,b_keywords
        #
        #     from shop_set
        #
        #     where usr_id=%s
        #
        # """ % self.usr_id
        #
        # L = self.db.fetch( sql )

        return L

    def local_add_save(self):
        

        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        
        #这些是操作权限
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}
        return dR
        #dR={'R':'','MSG':'','isadd':''}
        dR={'R':'','MSG':''}
        save_flag = self.REQUEST.get("save_flag").strip()
        save_flag2 = self.cookie.getcookie("__flag")
        
        
        #获取表单参数
        s_keywords=self.GP('s_keywords','')#小程序appid
        num_time=self.GP('num_time','')#小程序secret
        money=self.GP('money','')#小程序对应的token
        amount=self.GP('amount','')#微信支付商户号
        b_keywords=self.GP('b_keywords','')#微信支付商户秘钥

        
        data = {
                's_keywords':s_keywords
                ,'num_time':num_time
                ,'money':money
                ,'amount':amount
                ,'b_keywords':b_keywords
                ,'usr_id':self.usr_id

        }


        pk=''
        sql="select id from shop_set where usr_id=%s"%self.usr_id_p
        l,t=self.db.select(sql)
        if t>0:
            pk=l[0][0]

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data['cid']=self.usr_id
            data['ctime']=self.getToday(6)
            #data.pop('random')

            self.db.update('shop_set' , data , " id = %s " % pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data['uid'] = self.usr_id
            data['utime'] = self.getToday(6)
            
            self.db.insert('shop_set' , data)
            #pk = ''#self.db.insertid('mall_id')#这个的格式是表名_自增字段
            dR['isadd'] = 1
        #self.listdata_save(pk,danhao)
        #dR['pk'] = pk
        
        return dR

    # def save_tag(self):
    #     ctitle = self.GP("ctitle",'')
    #     status = self.GP("status",'')
    #     dR={'code':'','MSG':''}
    #     sql="insert into user_tag(usr_id,ctitle,status,cid,ctime)values(%s,%s,%s,%s,now())"
    #     try:
    #         dR['MSG']='增加标签成功'
    #         self.db.query(sql,[self.usr_id_p,ctitle,status,self.usr_id])
    #         return dR
    #     except:
    #         dR['MSG'] = '增加标签失败'
    #         return dR
    #
    # def ajax_delete_data(self):
    #     pk = self.pk
    #     dR = {'R':'', 'MSG':''}
    #     try:
    #         self.db.query("update user_tag set del_flag=1 where id= %s and usr_id=%s" ,[pk,self.usr_id_p])
    #         dR['MSG'] = '删除成功'
    #     except:
    #         dR['MSG']='删除失败'
    #     return dR
