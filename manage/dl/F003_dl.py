# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/F003_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class cF003_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['时间','金额','方式','用户ID','用户名']


    def mRight(self):
            
        sql = u"""
            select to_char(c.ctime,'YYYY-MM-DD HH24:MI'),c.change_money,c.ctype_str,c.wechat_user_id,u.cname 
                    from cash_log c
                    left join  wechat_mall_user u on u.id=c.wechat_user_id and u.usr_id =c.usr_id 
                    where c.usr_id=%s and  c.ctype=2 order by  c.ctime desc
        """%self.usr_id_p

        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self ):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
            select 
                
                synurl
            from users  where usr_id=%s

        """

        L = self.db.fetch( sql , self.usr_id)

        return L

    def local_add_save(self):
        

        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        
        #这些是操作权限
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}  

        #获取表单参数
        synurl=self.GP('synurl','')#小程序appid
        data = {
                'synurl':synurl
                ,'syn_flag':1
             }

        data['uid']=self.usr_id
        data['utime']=self.getToday(6)
        self.db.update('users' , data , " usr_id = %s " % self.usr_id)
        dR['pk'] = self.usr_id
        
        return dR

    def sync_data(self):
        dR = {'MSG': '','code':''}
        id = self.GP('id','')
        if id=='':
            dR['code']=1
            dR['MSG']='参数有误'
            return dR
        sql="select synurl,COALESCE(syn_flag,0) from users where usr_id=%s"
        l,t=self.db.select(sql,id)
        if t==0:
            dR['code'] = 1
            dR['MSG'] = '用户数据问题，请联系管理员'
            return dR
        if str(l[0][1])=='0':
            dR['code'] = 1
            dR['MSG'] = '请填写API工厂同步设置'
            return dR
        if str(l[0][1])=='2':
            dR['code'] = 1
            dR['MSG'] = '您已同步过数据，请联系管理员'
            return dR

        synurl=l[0][0].replace(' ','')
        import urllib, json
        #banner数据
        banner_url=synurl+'/banner/list'
        banner_req = urllib.request.Request(banner_url)
        banner = urllib.request.urlopen(banner_req).read()
        banner_dict=json.loads(banner.decode('utf-8'))
        MSG=''
        try:
            banner_data=banner_dict.get('data', '')
            if banner_data!='':
                for d in banner_data:
                    id=d['id']
                    b_data={}
                    b_data['businessid'] = d['businessId']
                    b_data['title'] = d['title']
                    b_data['linkurl'] = d['linkUrl']
                    b_data['status'] = d['status']
                    b_data['paixu'] = d['paixu']
                    b_data['remark'] = d['remark']
                    b_data['pic'] = d['picUrl']
                    b_data['type'] = d['type']
                    b_data['ctime']=d['dateAdd']
                    #b_data['utime']=d['dateUpdate']
                    b_data['m_id'] = id
                    b_data['usr_id'] = self.usr_id

                    for k in list(b_data):
                        if b_data[k] == '':
                            b_data.pop(k)
                    sql="select id from banner where m_id=%s and usr_id=%s "
                    l,t=self.db.select(sql,[id,self.usr_id])
                    if t>0:
                        b_data['del_flag'] = 0
                        b_data['syn_utime'] = self.getToday(9)
                        self.db.update('banner', b_data, " m_id = %s and usr_id=%s" %(id,self.usr_id))
                    else:
                        b_data['syn_ctime'] = self.getToday(9)
                        self.db.insert('banner', b_data)
        except Exception as e:
            #print('banner数据写入故障',e)
            dR['code'] = 1
            MSG+= 'banner数据写入故障'


        #分类数据
        category_url = synurl + '/shop/goods/category/all'
        category_req = urllib.request.Request(category_url)
        category = urllib.request.urlopen(category_req).read()
        category_dict = json.loads(category.decode('utf-8'))

        try:
            category_data = category_dict.get('data', '')
            if category_data != '':
                for c in category_data:
                    id = c['id']
                    if c['isUse']==True:
                        isUse=0
                    else:
                        isUse = 1

                    c_data = {}
                    c_data['name'] = c['name']
                    c_data['type'] = c['type']
                    c_data['pid'] = c['pid']
                    c_data['key'] = c['key']
                    c_data['icon'] = c['icon']
                    c_data['isuse'] = isUse
                    c_data['paixu'] = c['paixu']
                    c_data['level'] = c['level']
                    c_data['ctime'] = c['dateAdd']
                    #c_data['utime'] = d['dateUpdate']
                    c_data['m_id'] = id
                    c_data['usr_id'] = self.usr_id

                    for k in list(c_data):
                        if c_data[k] == '':
                            c_data.pop(k)

                    sql = "select id from goods_category where m_id=%s and usr_id=%s "
                    l, t = self.db.select(sql, [id, self.usr_id])
                    if t > 0:
                        c_data['del_flag']=0
                        c_data['syn_utime'] = self.getToday(9)
                        self.db.update('goods_category', c_data, " m_id = %s and usr_id=%s" % (id, self.usr_id))
                    else:
                        c_data['syn_ctime'] = self.getToday(9)
                        self.db.insert('goods_category', c_data)

                    #########更改分类适应当前数据库数据
                    sqls="select m_id,id from goods_category where COALESCE(m_id,0)!=0 and pid=0 and level=1 order by id"
                    ls, ts = self.db.select(sqls)
                    if ts>0:
                        for s in ls:
                            sqlu="update goods_category set pid=%s where pid=%s"
                            self.db.query(sqlu,[s[1],s[0]])


        except Exception as e:
            #print('商品分类数据写入故障',e)
            dR['code'] = 1
            MSG+= '  商品分类数据写入故障'


        # #商品数据
        goods_url=synurl+'/shop/goods/list'
        goods_req = urllib.request.Request(goods_url)
        goods = urllib.request.urlopen(goods_req).read()
        goods_dict = json.loads(goods.decode('utf-8'))

        try:
            goods_data = goods_dict.get('data', '')
            if goods_data != '':
                for g in goods_data:
                    id = g['id']
                    content_url = synurl + '/shop/goods/detail?id='+str(id)
                    content_req = urllib.request.Request(content_url)
                    content = urllib.request.urlopen(content_req).read()
                    content_dict = json.loads(content.decode('utf-8'))
                    content_data=content_dict.get('data')
                    content = content_data.get('content')
                    pics=content_data.get('pics')

                    if g['pingtuan'] == True:
                        pt = 0
                    else:
                        pt = 1

                    g_data = {}
                    g_data['barcode'] = g['barCode']
                    g_data['categoryid'] = g['categoryId']
                    g_data['characteristic'] = g['characteristic']
                    g_data['commission'] = g['commission']
                    g_data['commissiontype'] = g['commissionType']
                    g_data['datestart'] = g['dateStart']
                    #g_data['dateend'] = g['paixu']
                    g_data['logisticsid'] = g['logisticsId']
                    g_data['minprice'] = g['minPrice']
                    g_data['name'] = g['name']
                    g_data['numberfav'] = g['numberFav']
                    g_data['numbergoodreputation'] = g['numberGoodReputation']
                    g_data['numberorders'] = g['numberOrders']
                    g_data['paixu'] = g['paixu']
                    g_data['originalprice'] = g['originalPrice']
                    g_data['pic'] = g['pic']
                    g_data['recommendstatus'] = g['recommendStatus']
                    g_data['recommendstatusstr'] = g['recommendStatusStr']
                    g_data['shopid'] = g['shopId']
                    g_data['status'] = g['status']
                    g_data['statusstr'] = g['statusStr']
                    g_data['stores'] = g['stores']
                    g_data['videoid'] = g['videoId']
                    g_data['views'] = g['views']
                    g_data['weight'] = g['weight']
                    g_data['ptprice'] = g['pingtuanPrice']
                    g_data['pt'] = pt
                    g_data['content'] = content
                    g_data['ctime'] = g['dateAdd']
                    g_data['utime'] = g['dateUpdate']
                    g_data['m_id'] = id
                    g_data['usr_id'] = self.usr_id

                    for k in list(g_data):
                        if g_data[k] == '':
                            g_data.pop(k)

                    sql = "select id from goods_info where m_id=%s and usr_id=%s "
                    l, t = self.db.select(sql, [id, self.usr_id])
                    if t > 0:
                        g_data['del_flag'] = 0
                        g_data['syn_utime'] = self.getToday(9)
                        self.db.update('goods_info', g_data, " m_id = %s and usr_id=%s" % (id, self.usr_id))
                    else:
                        g_data['syn_ctime'] = self.getToday(9)
                        self.db.insert('goods_info', g_data)

                    if len(pics)>0:
                        if t==0:
                            sql = "select id from goods_info where m_id=%s and usr_id=%s "
                            l, t = self.db.select(sql, [id, self.usr_id])
                        try:
                            for p in pics:
                                goods_id = l[0][0]
                                p_data={}
                                p_data['goods_id'] = goods_id
                                p_data['m_id'] = p['id']
                                p_data['goodsid_mid']=p['goodsId']
                                p_data['pic'] = p['pic']
                                p_data['usr_id'] = self.usr_id

                                for k in list(p_data):
                                    if p_data[k] == '':
                                        p_data.pop(k)
                                sql = "select id from goods_pics where m_id=%s and usr_id=%s and goodsid_mid=%s"
                                ll, tt = self.db.select(sql,[id, self.usr_id,p['goodsId']])
                                if tt > 0:
                                    p_data['syn_utime'] = self.getToday(9)
                                    self.db.update('goods_pics', p_data," m_id = %s and usr_id=%s and goodsid_mid=%s" % (id, self.usr_id,p['goodsId']))
                                else:
                                    p_data['syn_ctime'] = self.getToday(9)
                                    self.db.insert('goods_pics', p_data)
                        except Exception as e:
                            #print('商品图片数据写入故障',e)
                            dR['code'] = 1
                            MSG += '  商品图片数据写入故障'

        except Exception as e:
            #print('商品数据写入故障',e)
            dR['code'] = 1
            MSG+= '  商品数据写入故障'

        if str(dR['code']) == '1':
            dR['MSG'] = MSG
            return dR

        dR['code'] = 0
        dR['MSG'] = '同步数据完成'
        sql = "update users set syn_flag=2 where usr_id=%s"%self.usr_id
        self.db.query(sql)
        return dR

