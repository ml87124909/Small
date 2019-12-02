# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/C002_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cC002_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['','规格名称','规格类型','规格图标','规格排序','添加时间','子属性管理']

    #在子类中重新定义         
    def myInit(self):
        self.src = 'C002'
        pass

    def mRight(self):
            
        sql = u"""
            select id,cname,ctype,cicon,sort,ctime,''
            from spec 
            where COALESCE(del_flag,0)=0 and usr_id=%s 
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
        sql+=" ORDER BY sort "
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self):
        """获取 local 表单的数据
        """
        L = {}

        if self.pk != '':
            sql = """
            select cname,ctype,cicon,sort   from spec  where  id=%s and usr_id=%s
             """
            L = self.db.fetch( sql,[self.pk,self.usr_id_p] )

        return L

    def get_sec_data(self):
        L = []

        if self.pk != '':
            sql = """
                select id,cname_c,ctype_c,cicon_c,sort_c  
                from spec_child 
                where  spec_id=%s and COALESCE(del_flag,0)=0 and usr_id=%s
                """
            l,t= self.db.select(sql,[self.pk,self.usr_id_p])
            if t>0:
                L=l

        return L


    def save_type(self):#保存规格

        ctype = self.GP("ctype", '')
        url = self.GPRQ("url", '')
        # url = ''
        # if self.objHandle.files:
        #     cicon = self.objHandle.files['cicon']
        #     from PIL import Image
        #     im = Image.open(cicon)
        #     width, height = im.size
        #     print('1111111111')
        #     resizedIm=cicon
        #     if width > 100:
        #
        #         resizedIm = im.resize((100, 100))
        #         print(resizedIm)
        #         #print(resizedIm.show())
        #
        #         #resizedIm.save(jpg)
        #         print('000000000')
        #     url = self.to_qiniu_Upload(cicon)
        #     #print(cicon)

        cname = self.GP("cname", '')
        sort = self.GP("sort", '')
        id = self.GP("id", '')
        dR = {'code': '', 'MSG': ''}

        if id=='0':
            sql = """
                        select id
                        from spec
                        where COALESCE(del_flag,0)=0 and usr_id=%s and cname=%s
                    """
            l, t = self.db.select(sql, [self.usr_id_p, cname])
            if t > 0:
                dR['code'] = '1'
                dR['MSG'] = '规格名称有重复'
                return dR

            sql = "insert into spec(usr_id,ctype,cicon,cname,sort,cid,ctime)values(%s,%s,%s,%s,%s,%s,now())"
            try:
                dR['MSG'] = '增加规格成功'
                self.db.query(sql, [self.usr_id_p, ctype, url, cname, sort or None, self.usr_id])
                self.oGOODS_D.update(self.usr_id_p)
                self.oGOODS.update(self.usr_id_p)
                self.oGOODS_N.update(self.usr_id_p)
                self.use_log('增加商品规格')
                dR['code'] = '0'
                return dR
            except:
                dR['code'] = '1'
                dR['MSG'] = '增加规格失败'
                return dR
        else:
            sql = """
                select id
                from spec
                where id!=%s and COALESCE(del_flag,0)=0 and usr_id=%s and cname=%s
                                """
            l, t = self.db.select(sql, [id,self.usr_id_p, cname])
            if t > 0:
                dR['code'] = '1'
                dR['MSG'] = '规格名称有重复'
                return dR
            try:

                sql = "update spec set ctype=%s,cicon=%s,cname=%s,sort=%s,uid=%s,utime=now() where id=%s "
                self.db.query(sql, [ctype, url, cname, sort or None, self.usr_id, id])
                dR['MSG'] = '修改规格成功'
                self.oGOODS_D.update(self.usr_id_p)
                self.oGOODS.update(self.usr_id_p)
                self.oGOODS_N.update(self.usr_id_p)
                self.use_log('修改商品规格%s' %id)
                dR['code'] = '0'
                return dR
            except:
                dR['MSG'] = '修改规格失败'
                dR['code'] = '1'
                return dR

    def save_ctype(self):#保存规格子属性
        ctype = self.GP("ctype", '')
        url = self.GPRQ("url", '')
        cname = self.GP("cname", '')
        sort = self.GP("sort", '')
        id = self.GP("id", '')
        pk = self.GP("pk", '')
        dR = {'code': '', 'MSG': ''}

        if id=='0':
            # sql = """
            #     select id from spec_child
            #     where usr_id=%s and COALESCE(del_flag,0)=0 and  cname_c=%s and spec_id=%s
            #         """
            # l, t = self.db.select(sql, [self.usr_id_p, cname, pk])
            # if t > 0:
            #     dR['code'] = '1'
            #     dR['MSG'] = '子规格名称有重复'
            #     return dR
            sql = "insert into spec_child(usr_id,spec_id,ctype_c,cicon_c,cname_c,sort_c,cid,ctime)values(%s,%s,%s,%s,%s,%s,%s,now())"
            try:
                dR['MSG'] = '增加规格子属性成功'
                self.db.query(sql, [self.usr_id_p,pk, ctype, url, cname, sort or None, self.usr_id])
                self.oGOODS_D.update(self.usr_id_p)
                self.oGOODS.update(self.usr_id_p)
                self.oGOODS_N.update(self.usr_id_p)
                self.use_log('增加商品规格子属性')
                dR['code'] = '0'
                return dR
            except:
                dR['MSG'] = '增加规格子属性失败'
                dR['code'] = '1'
                return dR
        else:
            try:
                dR['MSG'] = '修改规格子属性成功'

                sql = """update spec_child set ctype_c=%s,cicon_c=%s,
                    cname_c=%s,sort_c=%s,uid=%s,utime=now() where id=%s """
                self.db.query(sql, [ctype, url, cname, sort or None, self.usr_id, id])
                self.oGOODS_D.update(self.usr_id_p)
                self.oGOODS.update(self.usr_id_p)
                self.oGOODS_N.update(self.usr_id_p)
                self.use_log('修改商品规格子属性%s' % id)
                dR['code'] = '0'
                return dR
            except:
                dR['MSG'] = '修改规格子属性失败'
                dR['code'] = '1'
                return dR

    def ajax_delete_data(self):
        pk = self.pk
        dR = {'code':'', 'MSG':''}
        self.db.query("update spec set del_flag=1,utime=now() where id= %s and usr_id=%s", [pk,self.usr_id_p])
        self.oGOODS_D.update(self.usr_id_p)
        self.oGOODS.update(self.usr_id_p)
        self.oGOODS_N.update(self.usr_id_p)
        self.use_log('删除商品规格%s' % pk)
        dR['MSG'] = '删除成功！'
        return dR


    def ajax_up_data(self):
        id = self.GP('id','')
        dR = {'code': '', 'MSG': ''}
        data=self.db.fetch("select id,ctype_c,cicon_c,cname_c,sort_c from  spec_child where id= %s" ,id)
        if data:
            dR['data'] = data
            dR['code'] = 0
        return dR

    def ajax_update_data(self):
        id = self.GP('pk','')
        dR = {'code': '', 'MSG': ''}
        data=self.db.fetch("select id,ctype,cicon,cname,sort from  spec where id= %s" ,id)
        if data:
            dR['data'] = data
            dR['code'] = 0
        return dR

    def ajax_del_data(self):
        pk = self.pk
        dR = {'code':'', 'MSG':''}
        self.db.query("update spec_child set del_flag=1,utime=now() where id= %s and usr_id=%s" ,[pk,self.usr_id_p])
        self.oGOODS_D.update(self.usr_id_p)
        self.oGOODS.update(self.usr_id_p)
        self.oGOODS_N.update(self.usr_id_p)
        self.use_log('删除商品子规格%s' % pk)
        dR['MSG'] = '删除成功！'
        return dR


