# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/C004_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import hashlib , os , time , random,json,itertools

 
class cC004_dl(cBASE_DL):
    
    def init_data(self):

        self.GNL = ['商品ID', '标题', '分类','首图', '上架状态','推荐状态',
                    '库存','原价','现价','销量']

        
        self.src = 'C004'


    def mRight(self):
        self.sorting = self.GP('sorting', '')
        sql = """
            SELECT
                D.id,
                D.cname,
                D.category_ids_str,
                D.pic,
                D.status,
                D.recomm,
              
                D.stores,
                D.originalprice ,
                D.minprice,
                D.orders 
                

                --to_char(D.ctime,'YYYY-MM-DD HH:MM'),
                --to_char(D.utime,'YYYY-MM-DD HH:MM')
            FROM goods_info D

           -- left join category g on g.id=D.categoryid and D.usr_id=g.usr_id
           where COALESCE(D.del_flag,0)=0 and  D.usr_id=%s
        """
        parm=[self.usr_id_p]
        if self.qqid != '':
            sql += " AND D.cname  LIKE %s "
            parm.append('%%%s%%'% (self.qqid))

        sort_ = 'asc'
        if self.sorting == '2':
            sort_ = 'desc'
        sql += " ORDER BY D.paixu %s,D.id %s " % (sort_, sort_)
        #print(sql)
        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo,L=parm)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return  PL, L
    
    def get_local_data(self):
        #这里请获取表单所有内容。包括gw_doc表的title

        L = {}
        sql="""
             SELECT
                D.id,
                D.cname,
                D.introduce,
                D.recomm,
                D.status,
                D.category_ids,
                D.category_ids_str,
                D.video,
                D.contents,
                D.originalprice,
                D.minprice,
                D.stores,
                D.barcodes,
                D.logisticsid,
                D.limited,
                D.discount,
                D.share_type_str,
                D.share_type,
                D.share_time_str,
                D.share_time,
                D.share_title,
                D.share_imgs,
                D.share_return,
                D.return_ticket,
                D.return_ticket_str,
                D.paixu,
                D.weight,
                D.pt_status,
                D.pt_price,
                D.orders
            FROM goods_info D
           where D.id=%s and  COALESCE(D.del_flag,0)=0 and usr_id=%s
        """
        if self.pk != '':
            L = self.db.fetch(sql,[self.pk,self.usr_id_p])

        return L

    def get_pics_data(self):
        L = []
        sql = """
               select pic from goods_pics where goods_id=%s
                """
        if self.pk != '':
            l,t= self.db.select(sql,self.pk)
            if t>0:
                for i in l:
                    L.append(i[0])

        return L
    def local_add_save(self):

        # 这些是表单值
        dR = {'code':'0', 'MSG':'保存成功'}

        pk=self.pk
        cname=self.GP('cname','')#商品标题
        introduce = self.GPRQ('introduce','')#商品简介
        recomm = self.GP('recomm', '')#是否推荐
        status = self.GP('status', '')#上架状态
        paixu = self.GP('paixu', '')  # 排序
        category_ids=self.GP('category_ids','')#商品分类
        #category_ids_str =self.GP('category_ids_str','')#商品分类
        video = self.GP('video', '')#视频链接
        content = self.REQUEST.get('text_contents','')#详情介绍
        originalprice = self.GP('originalprice', '')#商品原价
        minprice = self.GP('minprice', '')  # 现价
        stores = self.GP('stores', '')#库存
        barcodes = self.GP('barcodes', '')  # 编 码
        weight = self.GP('weight', '')  # 重量
        #logisticsid=self.GP('logisticsid','')#配送方式
        limited = self.GP('limited', '')  # 限购数量
        discount=self.GP('discount','')#是否单独会员折扣
        share_type=self.GP('share_type','')#分享返现方式
        #share_type_str=self.GP('share_type_str','')#分享返现方式
        #share_time_str=self.GP('share_time_str','')#分享返现时效
        share_time=self.GP('share_time','')#分享返现时效
        share_title=self.GP('share_title','')#分享标题
        share_imgs=self.GP('share_imgs','')#分享海报
        cur_random_no = "%s%s" % (time.time(), random.random())
        share_return = self.GP('share_return', '')  # 分享返回现金或积分
        return_ticket = self.GP('return_ticket', '')  # 分享返的优惠券id
        return_ticket_str= self.GP('return_ticket_str', '')  # 分享返的优惠券名称
        pt_status = self.GP('pt_status', '')  # 拼团状态
        #pt_statusstr = self.GP('pt_statusstr', '')  # 拼团状态
        pt_price = self.GP('pt_price', '')  # 拼团价
        orders = self.GP('orders', '')  # 销量
        hy_price = self.GP('hy_price', '')  # 会员价
        big_price = self.GP('big_price', '')  # 大客户价
        pf_price = self.GP('pf_price', '')  # 批发价
        ls_price = self.GP('ls_price', '')  # 连锁价
        dl_price = self.GP('dl_price', '')  # 代理价



        data = {
            'cname': cname,
            'introduce': introduce,
            'recomm': recomm or None,
            'status': status or None,
            'category_ids': category_ids,
            #'category_ids_str':category_ids_str,
            'video': video,
            'contents': content,
            'originalprice': originalprice or None,
            'minprice': minprice or None,
            'stores': stores or None,
            #'logisticsid': logisticsid,
            'limited': limited or None,
            'discount': discount or None,
            'share_type': share_type or None,
            #'share_type_str': share_type_str,
            'share_title': share_title,
            'share_imgs': share_imgs,
            'random_no':cur_random_no,
            'paixu':paixu or None,
            'weight':weight or None,
            'barcodes': barcodes,
            'pt_status': pt_status or None,
            #'pt_statusstr': pt_statusstr,
            'pt_price': pt_price or None,
            'orders':orders or None,
            'hy_price':hy_price or None,
            'big_price':big_price or None,
            'pf_price':pf_price or None,
            'ls_price':ls_price or None,
            'dl_price':dl_price or None
        }

        if str(share_type)!='0':
            #data['share_time_str']=share_time_str
            data['share_time']=share_time
            if str(share_type)=='3':
                data['share_return'] = None
                data['return_ticket'] = return_ticket
                data['return_ticket_str'] = return_ticket_str
            else:
                data['share_return'] = share_return
                data['return_ticket'] = None
                data['return_ticket_str'] = return_ticket_str
        else:
            #data['share_time_str'] = ''
            data['share_time'] = None
            data['share_return'] = None
            data['return_ticket'] = None
        try:
            if pk != '':#update
                data['uid']=self.usr_id
                data['utime'] = self.getToday(9)
                self.db.update('goods_info' , data , " id = %s " %pk)
                self.use_log('修改商品档案%s' % pk)
            else:#insert
                data['usr_id']= self.usr_id_p
                data['cid'] = self.usr_id
                data['ctime'] = self.getToday(9)
                self.db.insert('goods_info' , data)
                pk = self.db.fetchcolumn('select id from goods_info where random_no=%s' ,cur_random_no)  # 这个的格式是表名_自增字段
                self.oGOODS_G.update(self.usr_id_p)
                self.use_log('增加商品档案%s' % pk)
            dR['pk'] = pk
            self.save_pics(pk)
            self.save_Spec(pk)

            self.oGOODS_D.update(self.usr_id_p,pk)
            self.oGOODS.update(self.usr_id_p,pk)
            self.oGOODS_N.update(self.usr_id_p,pk)
            self.oGOODS_SELL.update(self.usr_id_p)
            self.oGOODS_PT.update(self.usr_id_p,pk)
            sqlp = "select id from pt_conf where usr_id=%s and goods_id=%s"
            lT, iN = self.db.select(sqlp, [self.usr_id_p, pk])
            if iN > 0:
                ptid = lT[0][0]
                self.oPT_GOODS.update(self.usr_id_p, ptid)
        except Exception as e:
            dR = {'code':'1', 'MSG':'保存失败%s'%e}
        return dR

    def category_list(self):
        sql = u"""
                 select 
                    id
                    ,cname
                    ,pid
                    ,ilevel
                from category
                where COALESCE(del_flag,0)=0 and usr_id=%s
                """
        sql += "order by ilevel,paixu "
        parm = [self.usr_id_p]

        l,t=self.db.select(sql,parm)
        if t==0:
            return []

        List = []
        L1, L2 = [], []
        for i in l:
            if i[3]==1:
                L1.append(i)
            else:
                L2.append(i)
        k=0
        for j in L1:
            List.append({'id':j[0], "icon": "talent-icon-folder", "text": j[1]})
            for m in L2:
                if j[0]==m[2]:
                    if 'nodes' in List[k].keys():
                        List[k]['nodes']+=[{'id':m[0], "icon": "talent-icon-folder", "text": m[1]}]
                    else:
                        List[k]['nodes'] = [{'id': m[0], "icon": "talent-icon-folder", "text": m[1]}]
            k+=1

        return List

    def category_list_pk(self,pk):
        sql = u"""
                 select 
                    id
                    ,cname
                    ,pid
                    ,ilevel
                from category
                where COALESCE(del_flag,0)=0 and usr_id=%s
                """
        sql += "order by ilevel,paixu "
        l, t = self.db.select(sql, self.usr_id_p)
        if t == 0:
            return []
        List = []
        L1, L2 = [], []
        for i in l:
            if i[3] == 1:
                L1.append(i)
            else:
                L2.append(i)

        cids=self.db.fetchcolumn("select category_ids from goods_info where  id=%s",pk)

        if cids=='':
            cids=0
        else:
            cids = cids[:-1]

        sql = """
            select id,pid from category where COALESCE(del_flag,0)=0 and usr_id=%s and id in (%s)
        """ % (self.usr_id_p, cids)

        l,t=self.db.select(sql)
        P,I=[],[]
        for m in l:
            I.append(m[0])
            P.append(m[1])
        k = 0
        for j in L1:
            if j[0] in I :
                List.append({'id': j[0], "icon": "talent-icon-folder", "text": j[1],"state":{"checked":'true','expanded':'true'}})
            elif j[0] in P :
                List.append({'id': j[0], "icon": "talent-icon-folder", "text": j[1],"state":{"selected":'true','expanded':'true'}})
            else:
                List.append({'id': j[0], "icon": "talent-icon-folder", "text": j[1]})
            for m in L2:
                if j[0] == m[2]:
                    if 'nodes' in List[k].keys():
                        if m[0] in I:
                            List[k]['nodes'] += [{'id': m[0], "icon": "talent-icon-folder", "text": m[1],"state":{"checked":'true'}}]
                        else:
                            List[k]['nodes'] += [{'id': m[0], "icon": "talent-icon-folder", "text": m[1]}]
                    else:
                        if m[0] in I:
                            List[k]['nodes'] = [{'id': m[0], "icon": "talent-icon-folder", "text": m[1],"state":{"checked":'true'}}]
                        else:
                            List[k]['nodes'] = [{'id': m[0], "icon": "talent-icon-folder", "text": m[1]}]
            k += 1

        return List

    def spec_list(self):
        sql = "select id,cname from spec where usr_id =%s and COALESCE(del_flag,0)=0 order by sort"
        l, t = self.db.select(sql,self.usr_id_p)
        L=[]
        if t>0:
            #L.append(['','请选择规格'])
            for i in l:
                L.append(i)
        return L

    def spec_child_list(self):
        sql = "select id,spec_id,cname_c from spec_child where usr_id =%s and COALESCE(del_flag,0)=0 order by sort_c"
        l, t = self.db.select(sql,self.usr_id_p)
        L=[]
        if t>0:
            for i in l:
                L.append(i)
        return L

    def local_ajax_getSpec(self):
        id = self.REQUEST.get('id', '')
        pid = self.GP('pid', '')

        dR={'code':'','MSG':'数据为空'}

        id_dict=json.loads(id)
        print(id_dict)
        L=[]
        for k in id_dict:
            L.append(id_dict[k])
        List=[]

        l_t=len(L)

        if l_t==0:
            pass
        elif l_t==1:
            M=[]
            List=L[0]
            id=','.join(List)
            sql = """select id,cname_c,spec_id,cicon_c from spec_child 
                    where usr_id =%s and COALESCE(del_flag,0)=0 and id in (%s)""" %(self.usr_id_p,id)
            l, t = self.db.select(sql)
            if t>0:
                for i in l:
                    a=str(i[2]) + ':' + str(i[0])
                    c=''
                    d=''
                    e=''
                    f=''
                    g=''
                    h=i[3]
                    k=''
                    c1=''
                    c2 = ''
                    c3 = ''
                    c4 = ''
                    c5 = ''
                    if pid!='':
                        sql = """select id,oldprice,newprice,ptprice,hyprice,bigprice,
                        pfprice,lsprice,dlprice,store_c,barcode 
                        from spec_child_price where goods_id=%s AND sc_id=%s and usr_id=%s"""
                        l,t=self.db.select(sql,[pid,a,self.usr_id_p])
                        if t>0:
                            c,d,e,k,f,g,c1,c2,c3,c4,c5=l[0]
                    b=i[1]
                    M.append([c,a,b,d,e,k,f,g,h,c1,c2,c3,c4,c5])
            dR['code']='0'
            dR['data'] = M
            return dR

        elif l_t==2:
            M=[]
            for x in itertools.product(L[0], L[1]):
                List.append(x)
            for i in List:

                sql = """select sc.id,sc.cname_c,sc.spec_id,sc.cicon_c 
                        from spec_child sc
                        left join spec s on s.id=sc.spec_id
                        where sc.usr_id =%s and COALESCE(sc.del_flag,0)=0 and sc.id in %s
                        order by s.sort
                
                """ % (self.usr_id_p, i)
                l, t = self.db.select(sql)
                if t==2:
                    a=str(l[0][2])+':'+str(l[0][0])+','+str(l[1][2])+':'+str(l[1][0])
                    b=l[0][1]+'--'+l[1][1]
                    c = ''
                    d = ''
                    e = ''
                    f = ''
                    g = ''
                    h = ''
                    k=''
                    c1 = ''
                    c2 = ''
                    c3 = ''
                    c4 = ''
                    c5 = ''
                    if l[0][3]!='':
                        h = l[0][3]

                    if h!='':
                        if l[1][3]!='':
                            h+=','+l[1][3]
                    else:
                        h = l[1][3]
                    if pid != '':
                        sql = """ select id,oldprice,newprice,ptprice,hyprice,bigprice,
                                    pfprice,lsprice,dlprice,store_c,barcode 
                                    from spec_child_price where goods_id=%s AND sc_id=%s and usr_id=%s
                                """
                        l, t = self.db.select(sql, [pid, a, self.usr_id_p])
                        if t > 0:
                            c, d, e,k, f, g,c1,c2,c3,c4,c5 = l[0]

                    M.append([c, a, b, d, e,k, f, g,h,c1,c2,c3,c4,c5])

            dR['code'] = '0'
            dR['data'] = M
            return dR

        elif l_t==3:
            M=[]
            for x in itertools.product(L[0], L[1],L[2]):
                List.append(x)

            for i in List:

                sql = """select sc.id,sc.cname_c,sc.spec_id,sc.cicon_c 
                        from spec_child sc
                        left join spec s on s.id=sc.spec_id
                        where sc.usr_id =%s and COALESCE(sc.del_flag,0)=0 and sc.id in %s
                        order by s.sort

                """ % (self.usr_id_p, i)
                l, t = self.db.select(sql)

                if t==3:
                    a = str(l[0][2]) + ':' + str(l[0][0]) + ',' + str(l[1][2]) + ':' + str(l[1][0])+ ',' + str(l[2][2]) + ':' + str(l[2][0])
                    b=l[0][1]+'--'+l[1][1]+'--'+l[2][1]
                    c = ''
                    d = 0
                    e = 0
                    f = ''
                    g = ''
                    h=''
                    k=''
                    c1 = ''
                    c2 = ''
                    c3 = ''
                    c4 = ''
                    c5 = ''
                    if l[0][3] != '':
                        h = l[0][3]

                    if h != '':
                        if l[1][3] != '':
                            h += ',' + l[1][3]
                    else:
                        h = l[1][3]
                    if h != '':
                        if l[2][3] != '':
                            h += ',' + l[2][3]
                    else:
                        h = l[2][3]

                    if pid != '':
                        sql = """ select id,oldprice,newprice,ptprice,hyprice,bigprice,
                                pfprice,lsprice,dlprice,store_c,barcode 
                                from spec_child_price where goods_id=%s AND sc_id=%s and usr_id=%s"""
                        l, t = self.db.select(sql, [pid, a, self.usr_id_p])
                        if t > 0:
                            c, d, e,k, f, g,c1,c2,c3,c4,c5 = l[0]
                    M.append([c, a, b, d, e,k, f, g,h,c1,c2,c3,c4,c5])

            dR['code'] = '0'
            dR['data'] = M
            return dR

        elif l_t==4:
            M=[]
            for x in itertools.product(L[0], L[1],L[2],L[3]):
                List.append(x)
            for i in List:
                sql = """select sc.id,sc.cname_c,sc.spec_id,sc.cicon_c 
                            from spec_child sc
                            left join spec s on s.id=sc.spec_id
                            where sc.usr_id =%s and COALESCE(sc.del_flag,0)=0 and sc.id in %s
                            order by s.sort

                    """ % (self.usr_id_p, i)
                l, t = self.db.select(sql)
                if t==4:
                    a = str(l[0][2]) + ':' + str(l[0][0]) + ',' + str(l[1][2]) + ':' + str(l[1][0]) + ',' + str(
                        l[2][2]) + ':' + str(l[2][0])+ ',' + str(
                        l[3][2]) + ':' + str(l[3][0])
                    b=l[0][1]+'--'+l[1][1]+'--'+l[2][1]+'--'+l[3][1]
                    c = ''
                    d = 0
                    e = 0
                    f = ''
                    g = ''
                    h = ''
                    k=''
                    c1 = ''
                    c2 = ''
                    c3 = ''
                    c4 = ''
                    c5 = ''
                    if l[0][3] != '':
                        h = l[0][3]

                    if h != '':
                        if l[1][3] != '':
                            h += ',' + l[1][3]
                    else:
                        h = l[1][3]
                    if h != '':
                        if l[2][3] != '':
                            h += ',' + l[2][3]
                    else:
                        h = l[2][3]
                    if h != '':
                        if l[3][3] != '':
                            h += ',' + l[3][3]
                    else:
                        h = l[3][3]

                    if pid != '':
                        sql = """select id,oldprice,newprice,ptprice,hyprice,bigprice,
                                pfprice,lsprice,dlprice,store_c,barcode 
                                from spec_child_price where goods_id=%s AND sc_id=%s and usr_id=%s"""
                        l, t = self.db.select(sql, [pid, a, self.usr_id_p])
                        if t > 0:
                            c, d, e,k, f, g,c1,c2,c3,c4,c5 = l[0]
                    M.append([c, a, b, d, e,k, f, g,h,c1,c2,c3,c4,c5])
            dR['code'] = '0'
            dR['data'] = M
            return dR
        elif l_t==5:
            M=[]
            for x in itertools.product(L[0], L[1],L[2],L[3],L[4]):
                List.append(x)
            for i in List:
                sql = """select sc.id,sc.cname_c,sc.spec_id,sc.cicon_c 
                            from spec_child sc
                            left join spec s on s.id=sc.spec_id
                            where sc.usr_id =%s and COALESCE(sc.del_flag,0)=0 and sc.id in %s
                            order by s.sort

                    """ % (self.usr_id_p, i)
                l, t = self.db.select(sql)
                if t==5:
                    a = str(l[0][2]) + ':' + str(l[0][0]) + ',' + str(l[1][2]) + ':' + str(l[1][0]) + ',' + str(
                        l[2][2]) + ':' + str(l[2][0]) + ',' + str(
                        l[3][2]) + ':' + str(l[3][0])+ ',' + str(
                        l[4][2]) + ':' + str(l[4][0])
                    b=l[0][1]+'--'+l[1][1]+'--'+l[2][1]+'--'+l[3][1]+'--'+l[4][1]
                    c = ''
                    d = 0
                    e = 0
                    f = ''
                    g = ''
                    h=''
                    k=''
                    c1 = ''
                    c2 = ''
                    c3 = ''
                    c4 = ''
                    c5 = ''
                    if l[0][3] != '':
                        h = l[0][3]

                    if h != '':
                        if l[1][3] != '':
                            h += ',' + l[1][3]
                    else:
                        h = l[1][3]
                    if h != '':
                        if l[2][3] != '':
                            h += ',' + l[2][3]
                    else:
                        h = l[2][3]
                    if h != '':
                        if l[3][3] != '':
                            h += ',' + l[3][3]
                    else:
                        h = l[3][3]
                    if h != '':
                        if l[4][3] != '':
                            h += ',' + l[4][3]
                    else:
                        h = l[4][3]

                    if pid != '':
                        sql = """ select id,oldprice,newprice,ptprice,hyprice,bigprice,
                                pfprice,lsprice,dlprice,store_c,barcode 
                                from spec_child_price where goods_id=%s AND sc_id=%s and usr_id=%s
                                """
                        l, t = self.db.select(sql, [pid, a, self.usr_id_p])
                        if t > 0:
                            c, d, e,k , f, g,c1,c2,c3,c4,c5= l[0]
                    M.append([c, a, b, d,e,k,  f, g,h,c1,c2,c3,c4,c5])
            dR['code'] = '0'
            dR['data'] = M
            return dR


        return dR

    def save_pics(self,pk):

        try:
            sqldel = "delete from goods_pics where goods_id=%s and usr_id=%s;"
            self.db.query(sqldel,[pk,self.usr_id_p])
            sqlu = "update goods_info set pic='' where id=%s and usr_id=%s"
            self.db.query(sqlu,[pk,self.usr_id_p])

            files = self.REQUEST.getlist('pics')
            if files:

                sql=""
                i=0
                for file in files:
                    if i==0:
                        sqlu="update goods_info set pic=%s where id=%s and usr_id=%s"
                        self.db.query(sqlu,[file,pk,self.usr_id_p])

                    if sql == '':
                        sql+="insert into goods_pics(usr_id,goods_id,pic,cid,ctime)values(%s,%s,'%s',%s,now())"%(self.usr_id_p,pk,file,self.usr_id)
                    else:
                        sql += ",(%s,%s,'%s',%s,now())" % (self.usr_id_p,pk,file,self.usr_id)
                    i+=1
                if sql!='':
                    self.db.query(sql)
        except:
            pass

    def save_Spec(self,pk):
        lid = self.REQUEST.getlist('lid')  # 规格
        sc_id = self.REQUEST.getlist('sc_id')  #  规格
        sc_name = self.REQUEST.getlist('sc_name')  # 名称
        oldprice = self.REQUEST.getlist('oldprice')  # 原价
        newprice =  self.REQUEST.getlist('newprice')  # 现价
        ptprice = self.REQUEST.getlist('ptprice')  # 拼团价
        hyprice = self.REQUEST.getlist('hyprice')  # 会员价
        bigprice = self.REQUEST.getlist('bigprice')  # 大客户价
        pfprice = self.REQUEST.getlist('pfprice')  # 批发价
        lsprice = self.REQUEST.getlist('lsprice')  # 链锁价
        dlprice = self.REQUEST.getlist('dlprice')  # 代理价
        store_c = self.REQUEST.getlist('store_c')  # 库存
        barcode = self.REQUEST.getlist('barcode')  # 编码
        sc_icon = self.REQUEST.getlist('sc_icon')  # 图标

        if len(sc_name)>0:
            sql="select id from spec_child_price where  goods_id=%s and usr_id=%s;"
            l,t=self.db.select(sql,[pk,self.usr_id_p])
            if t>0:
                for j in l:
                    id_d=j[0]
                    if str(id_d) not in lid:
                        self.db.query("delete from  spec_child_price where id=%s and usr_id=%s;",[id_d,self.usr_id_p])
            for i in range(len(sc_name)):
                if sc_name[i]!='':
                    if lid[i]=='':
                        sql = """ insert into spec_child_price(usr_id,goods_id,sc_name,oldprice,newprice,ptprice,
                            hyprice,bigprice,pfprice,lsprice,dlprice,store_c,sc_id,barcode,sc_icon,cid,ctime)
                            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
                                               """
                        L =[self.usr_id_p, pk, sc_name[i], oldprice[i] or None, newprice[i] or None,ptprice[i] or None,
                             hyprice[i] or None,bigprice[i] or None,pfprice[i] or None,lsprice[i] or None,
                            dlprice[i] or None, store_c[i] or None, sc_id[i], barcode[i], sc_icon[i],

                        self.usr_id]
                        self.db.query(sql,L)
                    else:
                        sql="""
                        update spec_child_price set oldprice=%s,newprice=%s,ptprice=%s,hyprice=%s,bigprice=%s,
                        pfprice=%s,lsprice=%s,dlprice=%s,store_c=%s,barcode=%s,sc_icon=%s,uid=%s,utime=now()
                                where usr_id=%s and id=%s
                        """
                        L = [oldprice[i] or None, newprice[i] or None, ptprice[i] or None,hyprice[i] or None,
                             bigprice[i] or None,pfprice[i] or None,lsprice[i] or None,dlprice[i] or None,
                             store_c[i] or None,barcode[i], sc_icon[i], self.usr_id, self.usr_id_p, lid[i]]
                        self.db.query(sql, L)
        else:
            self.db.query("delete from  spec_child_price where usr_id=%s and goods_id=%s;", [self.usr_id_p,pk])




    def delete_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update goods_info set del_flag=1,utime=now() where id= %s and usr_id=%s" ,[pk,self.usr_id_p])
        self.oGOODS_D.update(self.usr_id_p)
        self.oGOODS.update(self.usr_id_p)
        self.oGOODS_N.update(self.usr_id_p)
        return dR

    def get_spec_data(self,pk):
        L, L_p, L_c, L_str = [], [], [], ''

        if pk!='':
            sql="select sc_id from spec_child_price where goods_id=%s and usr_id=%s"
            l,t=self.db.select(sql,[pk,self.usr_id_p])

            if t>0:
                for i in l:
                    I = i[0].split(',')
                    for j in I:
                        k = j.split(':')[-1]
                        L.append(k)
            if len(L)>0:
                L_str=','.join(set(L))
                sql = "select spec_id,id,cname_c,cicon_c from spec_child where id in (%s)" % L_str
                # print(sql)
                ll, n = self.db.select(sql)
                if n >0:
                    for k in ll:
                        if k[0] not in L_p:
                            L_p.append(k[0])
                        L_c.append(k)
        return L_p,L_c


    def spec_child_price(self,pk):
        L=[]
        if pk!='':
            sql = """select id,sc_id,sc_name,oldprice,newprice,ptprice,hyprice,bigprice,
            pfprice,lsprice,dlprice,store_c,barcode,sc_icon 
            from spec_child_price where goods_id=%s and usr_id=%s order by id"""
            l,t=self.db.select(sql,[pk,self.usr_id_p])
            if t>0:
                L=l
        return L

    def pics_list(self,pk):
        L=[]
        if pk!='':
            sql="select pic from goods_pics where usr_id =%s and goods_id=%s"
            l,t=self.db.select(sql,[self.usr_id_p,pk])
            if t>0:
                for i in l:
                    L.append(i[0])
        return L

    def Discount_list(self,pk):
        L = []
        if pk != '':
            sql = "select dis_id,dis_name,dis_level_discount from alone_discount where usr_id =%s and goods_id=%s"
            l, t = self.db.select(sql, [self.usr_id_p, pk])
            if t > 0:
                L=l
        return L

    def get_spec_child_data(self):
        dR = {'data': []}
        pk = self.pk
        spec_child_v = self.GP('spec_child_v', '')
        sql = "select id,cname_c from spec_child where COALESCE(del_flag,0)=0 and spec_id=%s and usr_id=%s"
        if spec_child_v != '':
            sql += ' and id not in (%s)' % spec_child_v
        l, t = self.db.fetchall(sql, [pk, self.usr_id_p])
        if t == 0:
            return dR
        dR['data'] = l
        return dR

    def set_spec_child_data(self):
        # spec_cid = self.REQUEST.getlist('spec_cid')
        # if spec_cid == []:
        #     return 0, []
        # spec_cids = ",".join(spec_cid)
        sid = self.GP('sid')
        spec_cids = self.GP('spec_cids', '')
        if spec_cids == '':
            return 0, []
        sql = """select id,cname_c,cicon_c from spec_child where COALESCE(del_flag,0)=0 
            and id in (%s) and usr_id=%s order by sort_c,id""" % (spec_cids, self.usr_id_p)
        l, t = self.db.select(sql)
        return sid, l

    def add_spec_child_data(self):
        sid = self.GP('sid')
        spec_p = self.GP('spec_p', '')
        new_name = self.GP('new_name', '')
        url = self.GP('url', '')
        sql = "select id from spec_child where usr_id=%s and spec_id=%s and cname_c=%s and COALESCE(del_flag,0)=0"
        l, t = self.db.select(sql, [self.usr_id_p, spec_p, new_name])
        if t > 0:
            dR = {'code': '1', 'MSG': '名称有重复'}
            return dR
        sql = "insert into spec_child(usr_id,spec_id,cname_c,cicon_c,cid,ctime)values(%s,%s,%s,%s,%s,now())"
        self.db.query(sql, [self.usr_id_p, spec_p, new_name, url, self.usr_id])
        dR = {'code': '0', 'id': sid}
        return dR

    def get_spec_class_data(self):
        spa = self.GP('spa', '')
        spcv = self.GP('spcv', '')

        sql = """select id,cname from spec where COALESCE(del_flag,0)=0 
         and usr_id=%s """
        if spcv != 'undefined' and spcv != '':
            sql += " and id not in (%s)" % spcv
        sql += "order by sort"
        l, t = self.db.select(sql, [self.usr_id_p])
        return l, spa

    def save_add_spec_data(self):
        sid = self.GP('sid')
        new_name = self.GP('new_name', '')
        sql = "select id from spec where usr_id=%s and  cname=%s and COALESCE(del_flag,0)=0"
        l, t = self.db.select(sql, [self.usr_id_p, new_name])
        if t > 0:
            dR = {'code': '1', 'MSG': '名称有重复'}
            return dR
        sql = "insert into spec(usr_id,cname)values(%s,%s)"
        self.db.query(sql, [self.usr_id_p, new_name])
        sql = "select id,cname from spec where usr_id=%s and  cname=%s and COALESCE(del_flag,0)=0"
        l = self.db.fetch(sql, [self.usr_id_p, new_name])
        dR = {'code': '0', 'data': l, 'sid': l['id'], 'cname': l['cname']}
        return dR

    def get_spec_class_re_data(self):
        spcvv = self.GP('spcvv', '')
        L = []
        D = {}

        sql = """select spec_id,id,cname_c,cicon_c from spec_child where COALESCE(del_flag,0)=0 
         and usr_id=%s """
        if spcvv != 'undefined' and spcvv != '':
            sql += " and id in (%s)" % spcvv

        l, t = self.db.select(sql, [self.usr_id_p])
        for i in l:
            if i[0] not in L:
                L.append(i[0])
            if str(i[0]) not in D:
                D[str(i[0])] = str(i[1])
            else:
                D[str(i[0])] = str(D[str(i[0])]) + ',' + str(i[1])

        sql = "select id,cname from spec where COALESCE(del_flag,0)=0 and usr_id=%s order by sort"
        S, t = self.db.select(sql, [self.usr_id_p])
        return l, L, S, D

    def local_ajax_getSpecChild(self):

        keywords = self.GP('keyword', '')
        tree_pk = self.GP('tree_pk', '')
        tree_id = self.GP('tree_id', '')
        rL = []
        sql = """
        select id,cname_c,ctype_c,cicon_c from spec_child 
        where usr_id=%s and spec_id=%s and COALESCE(del_flag,0)=0 
        """
        parm = [self.usr_id_p, tree_pk]
        if tree_id != '':  # name
            sql += "and  id not in (%s) " % tree_id

        if keywords != '':  # name
            sql += "and  cname_c like %s "
            parm.append('%%%s%%' % keywords)

        sql += """ order by id desc """
        lT, iN = self.db.fetchall(sql, parm)
        if iN > 0:
            rL = [lT, iN]

        return rL

    def local_ajax_getSpec_c(self):
        tree_pk = self.GP('tree_pk', '0')
        L = []
        sql = """
            select 
                id,0,cname,0 
                from spec 
                where  COALESCE(del_flag,0)=0 and id=%s

        """

        lT, iN = self.db.select(sql, [int(tree_pk)])
        if iN > 0:
            L = lT
        return L
