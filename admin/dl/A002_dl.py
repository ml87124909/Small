# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/A002_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cA002_dl(cBASE_DL):
    
    def init_data(self):
        self.GNL = ['ID','编号', '类型标记', '业务编号','名称',
                    'Banner图片','链接地址','状态','添加时间','修改时间	']

    def mRight(self):
            
        sql = """
            SELECT
                id
                ,field
                ,cname
            FROM advertis 
           where COALESCE(del_flag,0)=0 and ctype=1 and usr_id=%s
        """
        parm=[self.usr_id_p]
        #
        # if self.qqid != '':
        #     sql += "AND cname LIKE '%%%s%%' " % (self.qqid)
        # ORDER BY
        sql += " ORDER BY sort "

        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo,L=parm)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L
    
    def get_local_data(self):
        #这里请获取表单所有内容。包括gw_doc表的title

        L = {'ctype':self.GP('ctype','')}

        sql="""
             SELECT
                D.id,
                D.ctype,
                D.business_id,
                D.title,
                D.good_name,
                D.status,
                D.remark,
                D.link_url,
                D.pic_url,
                D.remark,
                D.sort
            FROM banner D
            where  D.id = %s
        """
        if self.pk != '':
            L = self.db.fetch(sql,[self.pk])

        return L

    def local_add_save(self):

        dR = {'code':'', 'MSG':'保存成功'}

        title = self.GP('title','')#类型标记:
        business_id =self.GP('business_id','')# 跳转商品id:
        good_name = self.GP('good_name', '')  # 商品名称
        link_url = self.GP('link_url', '')  # 链接地址
        ctype = self.GP('ctype', '')  # 类型
        status = self.GP('status', '')  # 状态
        pic_url = self.GP('pic_url', '')  # 图片链接
        remark = self.REQUEST.get('remark', '')  # 备注
        sort = self.GP('sort', '')  # 备注


        data={
            'title':title,
            'business_id':business_id or None,
              'good_name':good_name,
              'link_url':link_url,
              'ctype':ctype or None,
              'status':status or None,
              'pic_url':pic_url,
              'remark':remark,
              'sort':sort or None
              }
        pk=''

        if self.pk != '':  # update

            data['uid']=self.usr_id
            data['utime'] = self.getToday(9)
            self.db.update('banner' , data , " id = %s " % self.pk)
            pk=self.pk
            self.use_log('修改图片广告%s' % pk)

        else:  # insert
            data['usr_id'] = self.usr_id_p
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            self.db.insert('banner' , data)
            self.use_log('增加图片广告')
        self.oSHOP.update(self.usr_id_p)

        dR['code'] = '0'
        dR['pk'] = pk

        return dR
        
    def delete_data(self):
        pk = self.pk
        dR = {'code':'', 'MSG':''}
        self.db.query("update banner set del_flag=1 where id= %s" ,[pk])
        self.oSHOP.update(self.usr_id_p)
        self.use_log('删除图片广告%s'%pk)
        dR['code'] = '1'
        dR['MSG'] = '删除成功'
        return dR

    def local_ajax_jftype(self):
        kw = self.GP('keyword', '')
        sql = u"""
                select id,cname from goods_info where COALESCE(del_flag,0)=0 and usr_id=%s
                    """
        L=[self.usr_id_p]
        if kw != '':
            sql += " and cname LIKE %s"
            L.append('%%%s%%'%kw)
        sql += " ORDER BY id"
        lT, iN = self.db.select(sql,L)

        return self.sendMselectData(lT)

    def pic_type(self):
        L=[]
        sql="select id,cname from advertis where coalesce(del_flag,0)=0 and ctype=1 and usr_id=%s"
        l,n=self.db.select(sql,[self.usr_id_p])
        if n>0:
            L=l
        return L

    def banner_data(self):
        L=[]
        sql="select id,title,pic_url,ctype from banner where coalesce(del_flag,0)=0 and usr_id=%s order by id desc"
        l,n=self.db.fetchall(sql,[self.usr_id_p])
        if n>0:
            L=l
        return L

    def ajax_update(self):
        pk = self.pk
        dR = {'code': '', 'MSG': ''}
        data=self.db.fetch("select picurl,linkurl,buseid,field,cname,sort,status from  advertis where ctype=1 and id= %s" ,pk)
        if data:
            dR['data'] = data
            dR['code'] = '0'
        return dR


    def ajax_delete_data(self):
        pk = self.pk
        dR = {'code':'', 'MSG':''}
        self.db.query("update advertis set del_flag=1 where id= %s ", [pk])
        self.db.query("update banner set del_flag=1 where type= %s ", [pk])
        self.oSHOP.update(self.usr_id_p)
        self.use_log('删除图片广告分类%s' % pk)
        dR['code'] = '0'
        dR['MSG']='删除成功！'
        return dR

    def ajax_del_data(self):
        pk = self.pk
        dR = {'code': '', 'MSG': ''}
        self.db.query("update banner set del_flag=1 where id= %s" ,[pk])
        self.oSHOP.update(self.usr_id_p)
        self.use_log('删除图片广告%s' % pk)
        dR['code'] = '0'
        dR['MSG'] = '删除成功！'
        return dR

    def save_type(self):#增加广告类型

        field = self.GP("field", '')
        cname = self.GP("cname", '')
        sort = self.GP("sort", '')
        status = self.GP("status", '')
        buseid = self.GP("buseid", '')
        url = self.REQUEST.get("url", '')
        linkurl = self.GP("linkurl", '')

        dR = {'code': '', 'MSG': ''}

        sql = """insert into advertis(usr_id,ctype,field,cname,sort,cid,ctime,buseid,linkurl,picurl,status)
                    values(%s,1,%s,%s,%s,%s,now(),%s,%s,%s,%s)
                    """
        try:
            dR['MSG'] = '增加类型成功'
            self.db.query(sql, [self.usr_id_p,field, cname, sort or None, self.usr_id,buseid or None,linkurl,url,status])
            self.oSHOP.update(self.usr_id_p)
            self.use_log('增加图片广告分类')
            dR['code'] = '0'
        except:
            dR['code'] = '1'
            #print(str(traceback.format_exc()))
            dR['MSG'] = '增加类型失败'
        return dR

    def save_type_data(self): # 修改广告类型
        dR = {'code': '', 'MSG': ''}
        id = self.GP("id", '')
        field = self.GP("field", '')
        cname = self.GP("cname", '')
        sort = self.GP("sort", '')
        status = self.GP("status", '')
        buseid = self.GP("buseid", '')
        url = self.REQUEST.get("url", '')
        linkurl = self.GPRQ("linkurl", '')
        if id=='':
            dR['code'] = '1'
            dR['MSG'] = '没有id参数'
            return dR


        sql="""update advertis set buseid=%s,picurl=%s,linkurl=%s,field=%s,
            cname=%s,sort=%s,uid=%s,utime=now(),status=%s where id=%s """
        try:
            dR['MSG'] = '修改类型成功'
            self.db.query(sql, [buseid or None,url,linkurl,field, cname, sort or None, self.usr_id,status,id])
            self.oSHOP.update(self.usr_id_p)
            self.use_log('修改图片广告分类%s' % id)
            dR['code'] = '0'
            return dR
        except:
            dR['code'] = '1'
            dR['MSG'] = '增加类型失败'
            return dR