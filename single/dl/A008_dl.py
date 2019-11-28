# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/B004_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cA008_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['','编号','昵称','是否默认','地址详情',
                    '联系人姓名','手机号码','添加时间','更新时间']


    def mRight(self):
            
        sql = u"""
            select w.id
                ,wu.cname
                 ,case when w.is_default=1 then '是' else '否' end
                ,convert_from(decrypt(w.address::bytea, %s, 'aes'),'SQL_ASCII')
                ,w.cname
                ,convert_from(decrypt(w.phone::bytea, %s, 'aes'),'SQL_ASCII')
                ,w.ctime 
                ,w.utime
            from wechat_address w
            left join wechat_mall_user  wu on wu.id=w.wechat_user_id
            where  COALESCE(w.del_flag,0)=0 and w.usr_id =%s
        """
        parm=[self.md5code,self.md5code,self.usr_id_p]
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
        sql+=" ORDER BY w.id DESC"
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo,L=parm)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {}
        sql = u"""
                    select w.id
                        ,wu.cname
                        ,case when w.is_default=1 then '是' else '否' end is_default
                        ,w.address
                        ,w.cname
                        ,w.phone
                        ,w.ctime 
                        ,w.utime
                    from wechat_address w
                    left join wechat_mall_user  wu on wu.id=w.wechat_user_id
                    where  COALESCE(w.del_flag,0)=0 and w.usr_id =%s and w.id=%s
                """
        if pk != '':
            L = self.db.fetch( sql,[self.usr_id_p,pk] )

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

        self.db.query("update wechat_address set del_flag=1,del_time=now() where id= %s" % pk)
        self.use_log('删除用户地址%s' % pk)
        return dR
