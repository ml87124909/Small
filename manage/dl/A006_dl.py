# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/A006_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cA006_dl(cBASE_DL):
    def init_data(self):
        #[列头,宽,对齐]
        self.FDT = [
            ['', '', ''],  # 0
            ['用户编号', '4rem', ''],  # 1
            ['手机号码', '10rem', ''],  # 2
            ['昵称', '10rem', ''],  # 3
            ['省份', '10rem', ''],  # 4
            ['城市', '10rem', ''],  # 5
            ['头像', '6rem', ''],  # 6
            ['注册时间', '7rem', ''],  # 7
            ['注册IP', '10rem', ''],  # 8
            ['最后登录时间', '7rem', ''],  # 9
            ['最后登录IP', '10rem', ''],  # 10
            ['状态', '5rem', ''],  # 11
            ['会员级别', '4rem', ''],  # 12
            ['会员开始时间', '6rem', ''],  # 13
            ['会员到期时间', '6rem', ''],  # 14
            ['余额', "5rem", '', ''],  # 15

        ]
        # self.GNL=[] #列表上出现的
        self.GNL = self.parse_GNL([1,  3, 4, 5, 6, 7,  9,  11, 12, 13, 14, 15])


    def mRight(self):
            
        sql = u"""
            select id
                --,phone
                ,cname
                ,province
                ,city
                ,avatar_url
                ,to_char(ctime,'YYYY-MM-DD')ctime
                --,register_ip
                ,to_char(utime,'YYYY-MM-DD')utime
               -- ,last_login_ip
                ,COALESCE(status_str,'正常')
                ,usr_level_str
                ,to_char(hy_ctime,'YYYY-MM-DD')hy_ctime --会员开始时间
                ,to_char(hy_etime,'YYYY-MM-DD')hy_etime     --会员到期时间
                ,coalesce(balance,0)
            from wechat_mall_user 
            where usr_id=%s and COALESCE(del_flag,0)=0
        """
        parm = [self.usr_id_p]
        self.qqid = self.GP('qqid','')


        if self.qqid!='':
            sql += "  and cname LIKE %s "
            parm.append('%%%s%%' % (self.qqid))
        # #ORDER BY
        sql+=" ORDER BY id "
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo,L=parm)
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
                ,COALESCE(status_str,'正常')status_str
                ,COALESCE(usr_level ,0)as usr_level
                ,usr_level_str 
                ,COALESCE(hy_flag,0)hy_flag   --会员状态0否1是
                ,to_char(hy_ctime,'YYYY-MM-DD')hy_ctime --会员开始时间
                ,to_char(hy_etime,'YYYY-MM-DD')hy_etime     --会员到期时间
                ,COALESCE(usr_flag,0) as usr_flag
                ,usr_flag_str
                ,hy_flag
                ,hy_flag_str
                ,count_total
            from wechat_mall_user 
            where usr_id=%s and COALESCE(del_flag,0)=0 and id=%s
           
        """
        if self.pk != '':
            L = self.db.fetch( sql,[self.usr_id_p,self.pk] )

        return L
    
    def local_add_save(self):

        pk = self.pk
        dR={'code':'0','MSG':'修改成功'}

        #获取表单参数
        phone=self.GP('phone','')#电话号码
        status=self.GP('status','')#状态
        status_str = self.GP('status_str', '')  # 状态
        usr_level=self.GP('usr_level','')#会员级别
        usr_level_str = self.GP('usr_level_str', '')  # 会员级别
        hy_ctime=self.GP('hy_ctime','')#会员开始时间
        hy_etime=self.GP('hy_etime','')#会员到期时间
        usr_flag=self.GP('usr_flag','')#会员标签
        usr_flag_str = self.GP('usr_flag_str','')  # 会员标签
        hy_flag_str = self.GP('hy_flag_str','')  # 是否会员
        hy_flag = self.GP('hy_flag','')  # 是否会员

        data = {
                'phone':phone
                ,'status':status
                ,'usr_level':usr_level or None
                ,'hy_ctime':hy_ctime or None
                ,'hy_etime':hy_etime or None
                ,'usr_flag':usr_flag or None
                ,'status_str':status_str
                ,'usr_level_str':usr_level_str
                ,'usr_flag_str':usr_flag_str
                ,'usr_id': self.usr_id
                ,'hy_flag':hy_flag or None
                ,'hy_flag_str':hy_flag_str
        }


        if pk == '':
            dR ['MSG']='数据有误!'
            return dR

        #如果是更新，就去掉cid，ctime 的处理.
        l,t=self.db.select("select usr_level,usr_level_str,hy_flag,hy_flag_str,cname from wechat_mall_user where id=%s",pk)
        ousr_level,ousr_level_str, ohy_flag,ohy_flag_str,cname=l[0]
        data['uid'] = self.usr_id
        data['utime'] = self.getToday(9)
        self.db.update('wechat_mall_user', data, " id = %s " % pk)
        if usr_level!='':

            if str(usr_level)!=str(ousr_level):
                sqlc = """insert into wechat_user_change_log(
                wechat_user_id,name,old_level,new_level,up_type_str,ctime,end_time,up_mode_str,
                memo,cid,usr_id)values(
                %s,%s,%s,%s,'购物升级',now(),null,'手动','注:后台变更会员级别操作',%s,%s);
                """
                self.db.query(sqlc, [pk, cname,ousr_level_str, usr_level_str, self.usr_id, self.usr_id_p])
        if not hy_flag:
            if usr_level == '':
                sqlu = "update wechat_mall_user set hy_flag=null,hy_flag_str='' where id=%s;"
                self.db.query(sqlu, pk)
            else:
                sqlu = "update wechat_mall_user set hy_flag=1,hy_flag_str='是' where id=%s;"
                self.db.query(sqlu, pk)

        if hy_flag!='':
            if str(hy_flag) != str(ohy_flag):
                sqlc = """insert into wechat_user_change_log(
                wechat_user_id,name,old_level,new_level,up_type_str,ctime,end_time,up_mode_str,
                memo,cid,usr_id)values(
                %s,%s,%s,%s,'付费升级',now(),%s,'手动','注:后台变更是否会员操作',%s,%s)
                """
                self.db.query(sqlc, [pk, cname,ohy_flag_str, hy_flag_str or None,hy_etime or None, self.usr_id, self.usr_id_p])
        self.oUSER.update(self.usr_id_p, pk)
        self.use_log('修改用户信息')
        dR['pk'] = pk

        return dR


    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update wechat_mall_user set del_flag=1 where id= %s and usr_id=%s" ,[pk,self.usr_id_p])
        self.oUSER.update(self.usr_id_p,pk)
        self.use_log('删除用户%s'%pk)
        return dR


    def get_usr_tag(self):
        L=[]
        sql="select id,ctitle from user_tag where COALESCE(del_flag,0)=0 and usr_id=%s"
        l,t=self.db.select(sql,self.usr_id_p)
        if t>0:
            L=l
        return L

    def get_up_type(self):
        t = self.db.fetchcolumn("select up_type from shop_set where usr_id=%s", self.usr_id_p)
        return t

    def get_t_send_data(self):
        id=self.GP('id','')
        dR = {'R': '', 'MSG': ''}
        wxa=self.get_wecthpy()
        if wxa==0:
            dR['MSG']='请到店铺设置里配置小程序设置'
            return dR
        user=self.oUSER.get(self.usr_id_p,int(id))

        if user=={}:
            dR['MSG'] = '用户信息有误，请联系后台维护员'
            return dR
        sql="select open_id from wechat_mall_user where usr_id=%s and id=%s"
        opid=self.db.fetchcolumn(sql,[self.usr_id_p,id])
        tid='FebTBZG020ZIgIRhrUyRBD9fq7vZkcyBreg6AFyAGOM'
        data={"keyword1": {
          "value": "339208499"
            },"emphasis_keyword":"keyword1.DATA"}
        form_id='wx05123240364158123efaa6533193940789'

        a=wxa.send_template_message(opid,tid,data,form_id)
        if a.get('errcode','')==0:
            dR['MSG'] = '推送成功'
        return dR

    def addm_data(self):
        id=self.GP('id','')#用户id
        balance = self.GP('balance','')
        dR = {'code': '', 'MSG': '处理成功'}
        sql="update wechat_mall_user set balance=COALESCE(balance,0)+%s where id= %s and usr_id=%s"
        self.db.query(sql, [balance,id, self.usr_id_p])
        self.use_log('修改用户余额balance:%s,id:%s'%(balance,id))
        self.oUSER.update(self.usr_id_p, id)
        return dR
