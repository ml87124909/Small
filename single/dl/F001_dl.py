# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/F001_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import time

class cF001_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['','用户昵称','优惠券ID','优惠券名字','优惠券类型','优惠券金额',
                    '起用金额','优惠券状态','优惠券领取时间','优惠券到期时间']


    def mRight(self):
            
        sql = u"""
            select m.id,wu.cname,m.m_id,m.cname,m.type_str,
                    m.apply_ext_num,m.apply_ext_money,
                    
                    case when to_char(now(),'YYYY-MM-DD')<to_char(date_end,'YYYY-MM-DD') and COALESCE(state,0)=0 then '可使用' 
            when COALESCE(state,0)=1 then '已使用'
          when to_char(now(),'YYYY-MM-DD')>to_char(date_end,'YYYY-MM-DD') or COALESCE(state,0)=2 then '已过期'
           when COALESCE(state,0)=3 then '已失效' end ,
                            to_char(m.ctime,'YYYY-MM-DD HH24:MI'),m.date_end ,
                            case when to_char(now(),'YYYY-MM-DD')<to_char(date_end,'YYYY-MM-DD') and COALESCE(state,0)=0 then 0
                    when COALESCE(state,0)=1 then 1
          when to_char(now(),'YYYY-MM-DD')>to_char(date_end,'YYYY-MM-DD') or COALESCE(state,0)=2 then 2
           when COALESCE(state,0)=3 then 3 end 
            from my_coupons m
            left join wechat_mall_user  wu on wu.id=m.wechat_user_id
            where m.usr_id=%s 
        """%self.usr_id_p

        sql+=" ORDER BY m.id DESC"
        
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

            #L['danhao']='cgdd'+danhao
            L['danhao'] = ''
        return L
    
    # def local_add_save(self):
    #
    #
    #     """
    #     <p>这里是local 表单 ，add 模式下的保存处理</p>
    #     """
    #
    #     #这些是操作权限
    #     dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}
    #     pk = self.pk
    #     #dR={'R':'','MSG':'','isadd':''}
    #     dR={'R':'','MSG':''}
    #     save_flag = self.REQUEST.get("save_flag").strip()
    #     save_flag2 = self.cookie.getcookie("__flag")
    #
    #
    #     #获取表单参数
    #     danhao=self.GP('danhao')#单号
    #     sp_name=self.GP('sp_name')#商品名
    #     sp_bh=self.GP('sp_bh')#商品编号
    #     sp_type=self.GP('sp_type')#商品类型
    #     candi=self.GP('candi')#产地
    #     num=self.GP('num')#数量
    #     dw=self.GP('dw')#单位
    #     gys_id = self.GP('gys_id')  # 供应商ID
    #     money=self.GP('money')#进货价格
    #     in_date=self.GP('in_date')#进货时间
    #     beizhu=self.GP('beizhu')#备注
    #
    #
    #
    #     if not (save_flag == save_flag2):
    #         #为FALSE时,当前请求为重刷新
    #         return dR
    #
    #     # if danhao == '':
    #     #     dR['R'] = '1'
    #     #     dR['MSG'] = '请输入角色名字'
    #
    #     data = {
    #             'danhao':danhao
    #             ,'sp_name':sp_name
    #             ,'sp_bh':sp_bh
    #             ,'sp_type':sp_type
    #             ,'candi':candi
    #             ,'num':num
    #             ,'dw':dw
    #             ,'gys_id':gys_id
    #             ,'money':money
    #             ,'in_date':in_date
    #             ,'beizhu':beizhu,
    #             'cid': self.usr_id,
    #             'ctime': self.getToday(6),
    #             'uid': self.usr_id,
    #             'utime': self.getToday(6)
    #     }
    #
    #
    #     if pk != '':  #update
    #         #如果是更新，就去掉cid，ctime 的处理.
    #         data.pop('cid')
    #         data.pop('ctime')
    #         #data.pop('random')
    #
    #         self.db.update('cggl_cg' , data , " id = %s " % pk)
    #
    #     else:  #insert
    #         #如果是插入 就去掉 uid，utime 的处理
    #         data.pop('uid')
    #         data.pop('utime')
    #
    #         self.db.insert('cggl_cg' , data)
    #         pk = self.db.insertid('cggl_cg_id')#这个的格式是表名_自增字段
    #         dR['isadd'] = 1
    #     #self.listdata_save(pk,danhao)
    #     dR['pk'] = pk
    #
    #     return dR
    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update wechat_mall_address set del_flag=1 where id= %s" % pk)
        return dR

    def Up_status_data(self):
        dR = {'code': '', 'MSG': ''}
        id=self.GP('cid','')
        sql="select id from my_coupons where id=%s and usr_id=%s and COALESCE(state,0)=0"
        l,t=self.db.select(sql,[id,self.usr_id_p])
        if t==0:
            dR['MSG']='数据不存在，请确认'
            return dR
        sql="update my_coupons set state=3,state_str='失效' where id=%s "
        self.db.query(sql,id)
        dR['MSG'] = '失效成功'
        return dR
