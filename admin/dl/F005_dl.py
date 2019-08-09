# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/F005_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cF005_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['','用户ID','用户名字','之前级别','目前级别','升级方式',
                    '升级时间','到期时间','操作方式']


    def mRight(self):
            
        sql = u"""
            select id
               ,wechat_user_id
               ,name
                ,old_level
                ,new_level
                ,up_type_str
                ,ctime
                ,end_time
                ,up_mode_str
                
        
            from wechat_user_change_log 
            where usr_id=%s 
        """%self.usr_id_p
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
        sql+=" ORDER BY id"
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
            select id
                ,phone
                ,cname
                ,province
                ,city
                ,avatar_url
                ,ctime
                ,register_ip
                ,utime
                ,last_login_ip
                ,COALESCE(status ,0) as status   --允许下单0正常1禁用 
                ,status_str
                ,COALESCE(usr_level ,0)as usr_level
                ,usr_level_str 
                ,COALESCE(hy_flag,0)hy_flag   --会员状态0否1是
                ,hy_ctime --会员开始时间
                ,hy_etime     --会员到期时间
                ,COALESCE(usr_flag,0) as usr_flag
                ,usr_flag_str
            from wechat_mall_user 
            where usr_id=%s and COALESCE(del_flag,0)=0 and id=%s
           
        """
        if self.pk != '':
            L = self.db.fetch(sql, [self.usr_id_p, self.pk])

        return L
    
    def local_add_save(self):

        pk = self.pk
        dR={'R':'','MSG':''}

        #获取表单参数
        phone=self.GP('phone','')#电话号码
        status=self.GP('status','')#状态
        status_str = self.GP('status_str', '')  # 状态
        usr_level=self.GP('usr_level','')#会员级别
        usr_level_str = self.GP('usr_level_str', '')  # 会员级别
        hy_ctime=self.GP('hy_ctime','')#会员开始时间
        hy_etime=self.GP('hy_etime','')#会员到期时间
        usr_flag=self.GP('usr_flag','')#会员标签
        usr_flag_str = self.GP('usr_flag_str')  # 会员标签
        hy_flag=0
        if usr_level!='':
            hy_flag = 1

        data = {
                'phone':phone
                ,'status':status
                ,'usr_level':usr_level or None
                ,'hy_ctime':hy_ctime
                ,'hy_etime':hy_etime
                ,'usr_flag':usr_flag or None
                ,'status_str':status_str
                ,'usr_level_str':usr_level_str
                ,'usr_flag_str':usr_flag_str
            , 'usr_id': self.usr_id_p
                ,'hy_flag':hy_flag

        }


        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data['uid']=self.usr_id
            data['utime']=self.getToday(9)

            self.db.update('wechat_mall_user' , data , " id = %s " % pk)

        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data['cid']=self.usr_id
            data['ctime']=self.getToday(9)


        dR['pk'] = pk

        return dR
    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update wechat_mall_user set del_flag=1 where id= %s" % pk)
        return dR


    def get_usr_tag(self):
        L=[]
        sql="select id,ctitle from user_tag where COALESCE(del_flag,0)=0 and usr_id=%s"
        l, t = self.db.select(sql, self.usr_id_p)
        if t>0:
            L=l
        return L
