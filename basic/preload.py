# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""basic/preload.py"""

###预加载数据处理
def preload_log(db,cname,errors):
    sql = "insert into preload_log(cname,errors,ctime)values(%s,%s,now())"
    db.query(sql, [cname, errors])
    return

class cSHOP:

    def __init__(self,db,md5code):
        self.db=db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):

        dT = {}
        sql = "SELECT DISTINCT usr_id from users where COALESCE(status,0)=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}
            ShopInfo={}
            sql = """select s.id,s.cname as gname,s.logo_pic_link as gpic,s.home_title as sname,s.home_pic_link as spic,
                    convert_from(decrypt(s.gadds::bytea, %s, 'aes'),'SQL_ASCII')gadds,m.txt1 as vip_type,
                    convert_from(decrypt(s.phone::bytea, %s, 'aes'),'SQL_ASCII')phone,s.times,
                    s.vip_sale,s.mini_cash as pay_min,s.arrive as pay_time,s.up_type as ctype,s.topup,
                    s.drawal,s.return_ticket as coupons,s.use_money as freepost,s.vip_price,s.discount,
                    s.home_goods as home_type,s.shop_goods as cart_type,s.order_goods as order_type,
                    s.home_goods_id,s.shop_goods_id,s.shop_cart_memo,s.menu_memo,s.order_goods_id
                        
                    from shop_set s
                    left join mtc_t m on m.type='VIPUP' and m.id=s.up_type
                    where s.usr_id =%s"""
            shopInfo= self.db.fetch(sql,[self.md5code,self.md5code,k])
            vipInfo = []
            if shopInfo:
                id = shopInfo.get('id', '')
                vname=shopInfo.get('ctype','')
                vip_price = shopInfo.get('vip_price','')
                vip_sale =shopInfo.get('discount','')
                if str(vname) == '1':
                    vipInfo.append({'vip_id': 0, 'vip_price': vip_price, 'vip_name': '会员', 'vip_sale': vip_sale})
                elif str(vname) == '2':
                    sql = """select id as vip_id,cname as vip_name,
                        up_price as vip_price,level_discount as vip_sale 
                        from hy_up_level where usr_id =%s order by up_price """
                    vipInfo, t = self.db.fetchall(sql,k)

                home_goods_id=shopInfo.pop('home_goods_id','')
                shop_goods_id=shopInfo.pop('shop_goods_id','')
                order_goods_id = shopInfo.pop('order_goods_id','')
                home_goods=shopInfo['home_type']
                shop_goods=shopInfo['cart_type']
                order_goods=shopInfo['order_type']
                shop_cart_memo=shopInfo.pop('shop_cart_memo')
                menu_memo = shopInfo.pop('menu_memo')
                shop = shop_cart_memo.split(',')
                menu = menu_memo.split(',')

                if len(shop) > 0:
                    cartText = []
                    for s in shop:
                        cartText.append({'id': id, 'name': s})
                    ShopInfo['cartText'] = cartText

                if len(menu) > 0:
                    searchTag = []
                    for m in menu:
                        searchTag.append({'id': id, 'name': m})
                    ShopInfo['searchTag'] = searchTag

                if str(home_goods) == '2' and home_goods_id!='':
                    sql = """
                        select id	--商品ID
                            ,cname	--商品名称
                            ,introduce	--商品简介
                            ,recomm as status 	--是否推荐
                            ,pic	--商品第一张图片
                            ,originalprice as original_price	--商品原价
                            ,minprice as mini_price	--商品现价
                            ,limited	--限购数量
                            ,COALESCE(stores,0) as stores	--商品库存
                            ,barcodes	--商品编码
                            ,COALESCE(orders,0) as orders	--商品销量
                            ,COALESCE(see,0) as views	--商品浏览量
                            ,COALESCE(favorite,0) as favorite	--商品收藏量
                            ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                        from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id in (%s)
                    """%(k, home_goods_id)
                    homeGoods, n = self.db.fetchall(sql)
                    ShopInfo['homeGoods'] = homeGoods
                if str(shop_goods) == '2' and shop_goods_id!='':
                    sql = """
                        select id	--商品ID
                            ,name	--商品名称
                            ,introduce	--商品简介
                            ,recomm as status 	--是否推荐
                            ,pic	--商品第一张图片
                            ,originalprice as original_price	--商品原价
                            ,minprice as mini_price	--商品现价
                            ,limited	--限购数量
                            ,COALESCE(stores,0) as stores	--商品库存
                            ,barcodes	--商品编码
                            ,COALESCE(orders,0) as orders	--商品销量
                            ,COALESCE(see,0) as views	--商品浏览量
                            ,COALESCE(favorite,0) as favorite	--商品收藏量
                            ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                        from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id in (%s)
                    """%(k, shop_goods_id)
                    cartGoods, n = self.db.fetchall(sql)
                    ShopInfo['cartGoods'] = cartGoods
                if str(order_goods) == '2' and order_goods_id!='':
                    sql = """
                        select id	--商品ID
                            ,cname	--商品名称
                            ,introduce	--商品简介
                            ,recomm as status 	--是否推荐
                            ,pic	--商品第一张图片
                            ,originalprice as original_price	--商品原价
                            ,minprice as mini_price	--商品现价
                            ,limited	--限购数量
                            ,COALESCE(stores,0) as stores	--商品库存
                            ,barcodes	--商品编码
                            ,COALESCE(orders,0) as orders	--商品销量
                            ,COALESCE(see,0) as views	--商品浏览量
                            ,COALESCE(favorite,0) as favorite	--商品收藏量
                            ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                        from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id in (%s)
                    """%(k, order_goods_id)
                    orderGoods, n = self.db.fetchall(sql)
                    ShopInfo['orderGoods'] = orderGoods
            ShopInfo['shopInfo'] = shopInfo
            ShopInfo['vipInfo'] = vipInfo
            dT[str(k)]['ShopInfo']=ShopInfo

            #以上为shopinfo接口
            #advertis_banner接口开始
            sqlb = """select id,field,cname,buseid,linkurl,picurl 
                 from advertis where coalesce(del_flag,0)=0 and coalesce(status,0)=0 and usr_id=%s  order by sort
                                """
            lB, iB = self.db.fetchall(sqlb,[k])
            advertis_banner = []
            if iB > 0:
                for bb in lB:
                    field = bb['id']
                    sql = """select id,business_id,link_url,pic_url,remark,status,title 
                            from banner where COALESCE(del_flag,0)=0 and ctype =%s  and usr_id=%s order by sort 
                            """
                    l, t = self.db.fetchall(sql, [field,k])
                    if t > 0:
                        bb['data'] = l
                    advertis_banner.append(bb)
            dT[str(k)]['advertis_banner'] = advertis_banner

            #banner_list接口开始
            sql = """select b.id,b.business_id,b.link_url,b.pic_url,b.remark,
                    b.title,b.ctype,b.sort,b.topic_id,a.field
                    from banner b
                    left join advertis  a on a.id=b.ctype
                    where COALESCE(b.del_flag,0)=0 and b.usr_id =%s and COALESCE(b.status,0)=0 order by b.sort """
            banner_list, t = self.db.fetchall(sql,k)
            dT[str(k)]['banner_list'] = banner_list
            #textarea_list
            sql = """select id,key,content as value,remark,key,
                            to_char(ctime,'YYYY-MM-DD HH24:MI')time_add,
                            to_char(utime,'YYYY-MM-DD HH24:MI')time_update 
                            from config_set  where usr_id=%s and COALESCE(del_flag,0)=0"""
            textarea_list, t = self.db.fetchall(sql,k)
            dT[str(k)]['textarea_list'] = textarea_list
            # order_delivery_list
            sql = "select id,cname as delivery_name,is_mail as delivery_free from logistics_way where usr_id=%s"
            order_delivery_list, n = self.db.fetchall(sql,k)
            dT[str(k)]['order_delivery_list'] = order_delivery_list
            #shop_category
            sql = """select c.id,c.cname,c.ctype,
                            c.ilevel,c.pid,ca.cname as pid_name,
                            c.pic_icon,c.pic_imgs,c.paixu,c.remark,
                            to_char(c.ctime,'YYYY-MM-DD HH24:MI')time_add 
                            from category c
                            left join category ca on ca.id=c.pid
                            where COALESCE(c.del_flag,0)=0 and c.usr_id=%s  
                            order by c.paixu """
            shop_category, t = self.db.fetchall(sql, k)
            dT[str(k)]['shop_category'] = shop_category
            #shopinfo_shops
            sql = " select id,cname,address,contact,jd as longitude,wd as latitude  from shopconfig where usr_id =%s"
            shopinfo_shops, t = self.db.fetchall(sql,k)
            dT[str(k)]['shopinfo_shops'] = shopinfo_shops


        self.__d = dT

    def update(self, sType):
        self.__d[str(sType)] = {}
        ShopInfo={}
        sql = """select s.id,s.cname as gname,s.logo_pic_link as gpic,s.home_title as sname,s.home_pic_link as spic,
                            convert_from(decrypt(s.gadds::bytea, %s, 'aes'),'SQL_ASCII')gadds,m.txt1 as vip_type,
                            convert_from(decrypt(s.phone::bytea, %s, 'aes'),'SQL_ASCII')phone,s.times,
                            s.vip_sale,s.mini_cash as pay_min,s.arrive as pay_time,s.up_type as ctype,s.topup,
                            s.drawal,s.return_ticket as coupons,s.use_money as freepost,s.vip_price,s.discount,
                            s.home_goods as home_type,s.shop_goods as cart_type,s.order_goods as order_type,
                            s.home_goods_id,s.shop_goods_id,s.shop_cart_memo,s.menu_memo,s.order_goods_id

                            from shop_set s
                            left join mtc_t m on m.type='VIPUP' and m.id=s.up_type
                            where s.usr_id =%s"""
        shopInfo = self.db.fetch(sql, [self.md5code,self.md5code,sType])
        vipInfo = []
        if shopInfo:
            id = shopInfo.get('id', '')
            vname = shopInfo.get('ctype', '')
            vip_price = shopInfo.get('vip_price', '')
            vip_sale = shopInfo.get('discount', '')
            if str(vname) == '1':
                vipInfo.append({'vip_id': 0, 'vip_price': vip_price, 'vip_name': '会员', 'vip_sale': vip_sale})
            elif str(vname) == '2':
                sql = """select id as vip_id,cname as vip_name,
                                up_price as vip_price,level_discount as vip_sale 
                                from hy_up_level where usr_id =%s order by up_price """
                vipInfo, t = self.db.fetchall(sql, [sType])

            home_goods_id = shopInfo.pop('home_goods_id')
            shop_goods_id = shopInfo.pop('shop_goods_id')
            order_goods_id = shopInfo.pop('order_goods_id')
            home_goods = shopInfo['home_type']
            shop_goods = shopInfo['cart_type']
            order_goods = shopInfo['order_type']
            shop_cart_memo = shopInfo.pop('shop_cart_memo')
            menu_memo = shopInfo.pop('menu_memo')
            shop = shop_cart_memo.split(',')
            menu = menu_memo.split(',')

            if len(shop) > 0:
                cartText = []
                for s in shop:
                    cartText.append({'id': id, 'name': s})
                ShopInfo['cartText'] = cartText

            if len(menu) > 0:
                searchTag = []
                for m in menu:
                    searchTag.append({'id': id, 'name': m})
                ShopInfo['searchTag'] = searchTag

            if str(home_goods) == '2' and home_goods_id != '':
                sql = """
                    select id	--商品ID
                        ,cname	--商品名称
                        ,introduce	--商品简介
                        ,recomm as status 	--是否推荐
                        ,pic	--商品第一张图片
                        ,originalprice as original_price	--商品原价
                        ,minprice as mini_price	--商品现价
                        ,limited	--限购数量
                        ,COALESCE(stores,0) as stores	--商品库存
                        ,barcodes	--商品编码
                        ,COALESCE(orders,0) as orders	--商品销量
                        ,COALESCE(see,0) as views	--商品浏览量
                        ,COALESCE(favorite,0) as favorite	--商品收藏量
                        ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                    from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id in (%s)
                """ % (sType, home_goods_id)
                homeGoods, n = self.db.fetchall(sql)
                ShopInfo['homeGoods'] = homeGoods
            if str(shop_goods) == '2' and shop_goods_id != '':
                sql = """
                    select id	--商品ID
                        ,cname	--商品名称
                        ,introduce	--商品简介
                        ,recomm as status 	--是否推荐
                        ,pic	--商品第一张图片
                        ,originalprice as original_price	--商品原价
                        ,minprice as mini_price	--商品现价
                        ,limited	--限购数量
                        ,COALESCE(stores,0) as stores	--商品库存
                        ,barcodes	--商品编码
                        ,COALESCE(orders,0) as orders	--商品销量
                        ,COALESCE(see,0) as views	--商品浏览量
                        ,COALESCE(favorite,0) as favorite	--商品收藏量
                        ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                    from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id in (%s)
                """ % (sType, shop_goods_id)
                cartGoods, n = self.db.fetchall(sql)
                ShopInfo['cartGoods'] = cartGoods
            if str(order_goods) == '2' and order_goods_id != '':
                sql = """
                    select id	--商品ID
                        ,cname	--商品名称
                        ,introduce	--商品简介
                        ,recomm as status 	--是否推荐
                        ,pic	--商品第一张图片
                        ,originalprice as original_price	--商品原价
                        ,minprice as mini_price	--商品现价
                        ,limited	--限购数量
                        ,COALESCE(stores,0) as stores	--商品库存
                        ,barcodes	--商品编码
                        ,COALESCE(orders,0) as orders	--商品销量
                        ,COALESCE(see,0) as views	--商品浏览量
                        ,COALESCE(favorite,0) as favorite	--商品收藏量
                        ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                    from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id in (%s)
                """ % (sType, order_goods_id)
                orderGoods, n = self.db.fetchall(sql)
                ShopInfo['orderGoods'] = orderGoods
        ShopInfo['shopInfo'] = shopInfo
        ShopInfo['vipInfo'] = vipInfo
        self.__d[str(sType)]['ShopInfo'] = ShopInfo

        # 以上为shopinfo接口
        # advertis_banner接口开始
        sqlb = """select id,field,cname,buseid,linkurl,picurl 
                    from advertis where coalesce(del_flag,0)=0 
                    and coalesce(status,0)=0 and usr_id=%s order by sort
                                        """
        lB, iB = self.db.fetchall(sqlb,[sType])
        advertis_banner = []
        if iB > 0:
            for bb in lB:
                field = bb['id']
                sql = """select id,business_id,link_url,pic_url,remark,status,title 
                    from banner where COALESCE(del_flag,0)=0 and ctype =%s and usr_id=%s order by sort 
                                    """
                l, t = self.db.fetchall(sql, [field,sType])
                if t > 0:
                    bb['data'] = l
                advertis_banner.append(bb)
        self.__d[str(sType)]['advertis_banner'] = advertis_banner
        # banner_list接口开始
        sql = """
                select b.id,b.business_id,b.link_url,b.pic_url,b.remark,
                    b.title,b.ctype,b.sort,b.topic_id,a.field
                    from banner b
                    left join advertis  a on a.id=b.ctype
                    where COALESCE(b.del_flag,0)=0 and b.usr_id =%s and COALESCE(b.status,0)=0 order by b.sort 
            """
        banner_list, t = self.db.fetchall(sql,sType)
        self.__d[str(sType)]['banner_list'] = banner_list
        # textarea_list
        sql = """select id,key,content as value,remark,key,
                    to_char(ctime,'YYYY-MM-DD HH24:MI')time_add,to_char(utime,'YYYY-MM-DD HH24:MI')time_update 
                    from config_set  where usr_id=%s and COALESCE(del_flag,0)=0"""
        textarea_list, t = self.db.fetchall(sql,sType)
        self.__d[str(sType)]['textarea_list'] = textarea_list
        #order_delivery_list
        sql = "select id,cname as delivery_name,is_mail as delivery_free from logistics_way where usr_id=%s"
        order_delivery_list, n = self.db.fetchall(sql,sType)
        self.__d[str(sType)]['order_delivery_list'] = order_delivery_list
        # shop_category
        sql = """select c.id,c.cname,c.ctype,
                    c.ilevel,c.pid,ca.cname as pid_name,
                    c.pic_icon,c.pic_imgs,c.paixu,c.remark,
                    to_char(c.ctime,'YYYY-MM-DD HH24:MI')time_add 
                    from category c
                    left join category ca on ca.id=c.pid
                    where COALESCE(c.del_flag,0)=0 and c.usr_id=%s  order by c.paixu """
        shop_category, t = self.db.fetchall(sql,sType)
        self.__d[str(sType)]['shop_category'] = shop_category
        # shopinfo_shops
        sql = " select id,cname,address,contact,jd as longitude,wd as latitude  from shopconfig where usr_id =%s"
        shopinfo_shops, t = self.db.fetchall(sql,sType)
        self.__d[str(sType)]['shopinfo_shops'] = shopinfo_shops

        return

    def get(self, sType, sID=''):
        if sID != '':
            return self.__d.get(str(sType), {}).get(str(sID), {})
        else:
            return self.__d.get(str(sType), {})


class cSHOP_T:

    def __init__(self,db,md5code):
        self.db=db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):

        dT = {}
        sql = """
            select s.usr_id,use_money,close_time,cancel_id,
                    send_id,evaluate_id,complete_id,cancel_url,send_url,evaluate_url,complete_url
                from  shop_set s 
                left join users u on u.usr_id=s.usr_id 
                where coalesce(u.expire_flag,0)=0 order by s.usr_id
        """
        lT, iN = self.db.fetchall(sql)
        for e in lT:
            k=e.pop('usr_id')
            dT[str(k)] = {}
            dT[str(k)] = e

        self.__d = dT

    def update(self,sType):
        self.__d[str(sType)] = {}
        sql = """select use_money as orderfree,close_time as orderclose,cancel_id,
                        send_id,evaluate_id,complete_id,cancel_url,send_url,evaluate_url,complete_url
                    from  shop_set where usr_id=%s"""
        l= self.db.fetch(sql,sType)
        self.__d[str(sType)]=l

        return

    def get(self, sType):
        return self.__d.get(str(sType), {})


class cUSER:

    def __init__(self,db,md5code):
        self.db=db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = """
            select w.usr_id,w.id,w.open_id from wechat_mall_user w
             left join users u on u.usr_id=w.usr_id 
            where   COALESCE(w.del_flag,0)=0 and coalesce(u.expire_flag,0)=0 order by w.usr_id 
        """
        lT, iN = self.db.fetchall(sql)
        for e in lT:
            k = e['usr_id']
            id=e['id']
            open_id = e['open_id']
            dT[str(k)] = {}
            dT[str(k)][str(id)] = {}
            dT[str(k)][str(open_id)] = {}

            sql = """
                        select id,cname as name,avatar_url as avatar,city,province,phone,
                            round(COALESCE(balance,0)::numeric,2) as money,COALESCE(score,0)score,
                            coalesce(hy_flag,0)vip_state,coalesce(usr_level,0) as vip_level,
                            usr_level_str as vip_level_name,to_char(hy_etime,'YYYY-MM-DD')vip_time,
                            to_char(up_time,'YYYY-MM-DD')up_time,status,COALESCE(del_flag,0)del_flag,
                            case when (select up_type from  shop_set where usr_id=%s limit 1)=1 then (select discount from  shop_set where usr_id=%s limit 1) 
                else ( select level_discount from hy_up_level where usr_id=%s and wechat_mall_user.usr_level=id order by level_discount limit 1) end vip_sale,
                            count_total as consume   
                        from wechat_mall_user where id=%s and COALESCE(del_flag,0)=0 
                    """
            userInfo = self.db.fetch(sql,[k,k,k,id])
            dT[str(k)][str(id)] = userInfo
            dT[str(k)][str(open_id)] = userInfo

        self.__d = dT

    def update(self, sType,id=''):

        if id!='':
            try:
                sql = """
                     select w.id,w.open_id,COALESCE(w.del_flag,0),coalesce(u.expire_flag,0) 
                     from wechat_mall_user w
             left join users u on u.usr_id=w.usr_id 
            where  w.usr_id=%s and w.id=%s
                
                """
                lT1, iN1 = self.db.select(sql, [sType,id])
                if iN1>0:
                    id, open_id,del_flag,expire_flag = lT1[0]
                    if str(expire_flag)=='1':
                        self.__d[str(sType)]={}
                        return
                    self.__d[str(sType)][str(id)] = {}
                    self.__d[str(sType)][str(open_id)] = {}
                    if str(del_flag)=='0':
                        sql = """
                                select id,cname as name,avatar_url as avatar,city,province,phone,
                                    round(COALESCE(balance,0)::numeric,2) as money,COALESCE(score,0)score,
                                    coalesce(hy_flag,0)vip_state,coalesce(usr_level,0) as vip_level,
                                    usr_level_str as vip_level_name,to_char(hy_etime,'YYYY-MM-DD')vip_time,
                                    to_char(up_time,'YYYY-MM-DD')up_time,status,COALESCE(del_flag,0)del_flag,
                                    case when (select up_type from  shop_set where usr_id=%s limit 1)=1 then (select discount from  shop_set where usr_id=%s limit 1) 
                            else ( select level_discount from hy_up_level where usr_id=%s and wechat_mall_user.usr_level=id order by level_discount limit 1) end vip_sale,
                            count_total as consume   
                                from wechat_mall_user where id=%s and COALESCE(del_flag,0)=0
                                """
                        userInfo = self.db.fetch(sql, [sType,sType,sType,id])
                        self.__d[str(sType)][str(id)] = userInfo
                        self.__d[str(sType)][str(open_id)] = userInfo

                return
            except:
                pass
        self.__d[str(sType)] = {}
        sql = """
             select w.id,w.open_id from wechat_mall_user w
             left join users u on u.usr_id=w.usr_id 
            where   COALESCE(w.del_flag,0)=0 and coalesce(u.expire_flag,0)=0 and w.usr_id=%s
        """
        lT1, iN1 = self.db.select(sql, sType)
        if iN1 > 0:
            for i in lT1:
                id,open_id = i
                sql = """
                    select id,cname as name,avatar_url as avatar,city,province,phone,
                        round(COALESCE(balance,0)::numeric,2) as money,COALESCE(score,0)score,
                        coalesce(hy_flag,0)vip_state,coalesce(usr_level,0) as vip_level,
                        usr_level_str as vip_level_name,to_char(hy_etime,'YYYY-MM-DD')vip_time,
                        to_char(up_time,'YYYY-MM-DD')up_time,status,COALESCE(del_flag,0)del_flag,
                        case when (select up_type from  shop_set where usr_id=%s limit 1)=1 then (select discount from  shop_set where usr_id=%s limit 1) 
                else ( select level_discount from hy_up_level where usr_id=%s and wechat_mall_user.usr_level=id order by level_discount limit 1) end vip_sale,
                count_total as consume     
                    from wechat_mall_user where id=%s and COALESCE(del_flag,0)=0 
                """
                userInfo = self.db.fetch(sql,[sType,sType,sType,id])
                self.__d[str(sType)][str(id)] = userInfo
                self.__d[str(sType)][str(open_id)] = userInfo

        return

    def get(self, sType, sID=''):
        if sID != '':
            return self.__d.get(str(sType), {}).get(str(sID), {})
        else:
            return self.__d.get(str(sType), {})


class cUSERS:

    def __init__(self,db,md5code):
        self.db=db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = """SELECT usr_id,mini_openid from users 
            where status=1 and COALESCE(del_flag,0)=0 and coalesce(expire_flag,0)=0"""
        lT, iN = self.db.select(sql)
        for e in lT:
            k,v = e
            dT[str(k)] = v
            dT[str(v)] = k
        self.__d = dT

    def update(self, sType,openid):
        self.__d[str(sType)] = openid
        self.__d[str(openid)] = sType
        return

    def get(self, sType):
        return self.__d.get(str(sType),'')


class cOPENID:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = """ select w.id,w.open_id from wechat_mall_user w
             left join users u on u.usr_id=w.usr_id 
            where   COALESCE(w.del_flag,0)=0 and coalesce(u.expire_flag,0)=0
             """
        lT, iN = self.db.select(sql)
        for e in lT:
            id, open_id = e
            dT[str(id)] = open_id

        self.__d = dT

    def update(self, sType):

        self.__d[str(sType)] = {}
        sql = """select COALESCE(w.open_id,'') from wechat_mall_user w
             left join users u on u.usr_id=w.usr_id 
            where   COALESCE(w.del_flag,0)=0 and coalesce(u.expire_flag,0)=0 and w.id=%s"""
        open_id = self.db.fetchcolumn(sql, [sType])
        self.__d[str(sType)]=open_id

        return

    def get(self, sType):
        return self.__d.get(str(sType), '')


class cMALL:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = """
                select m.usr_id,convert_from(decrypt(appid::bytea, %s, 'aes'),'SQL_ASCII')appid,
                    convert_from(decrypt(secret::bytea, %s, 'aes'),'SQL_ASCII')secret,
                    convert_from(decrypt(mchid::bytea, %s, 'aes'),'SQL_ASCII') as mchid
                    ,convert_from(decrypt(mchkey::bytea, %s, 'aes'),'SQL_ASCII')mchkey,
                    certpem as cert,keypem as key  from mall m
             left join users u on u.usr_id=m.usr_id 
            where   coalesce(u.expire_flag,0)=0 order by m.usr_id 

                    """
        parm = [self.md5code, self.md5code, self.md5code, self.md5code]
        lT, iN = self.db.fetchall(sql,parm)
        for e in lT:
            k = e.pop('usr_id')
            dT[str(k)]= e

        self.__d = dT

    def update(self, sType):
        self.__d[str(sType)] = {}
        sql = """
                select convert_from(decrypt(appid::bytea, %s, 'aes'),'SQL_ASCII')appid,
                    convert_from(decrypt(secret::bytea, %s, 'aes'),'SQL_ASCII')secret,
                    convert_from(decrypt(mchid::bytea, %s, 'aes'),'SQL_ASCII') as mchid
                    ,convert_from(decrypt(mchkey::bytea, %s, 'aes'),'SQL_ASCII')mchkey,
                    certpem as cert,keypem as key  from mall m
             left join users u on u.usr_id=m.usr_id 
            where   coalesce(u.expire_flag,0)=0 and u.usr_id=%s
                
            """
        parm = [self.md5code, self.md5code, self.md5code, self.md5code, sType]
        self.__d[str(sType)] = self.db.fetch(sql,parm)

        return

    def get(self, sType):
        return self.__d.get(str(sType), {})


class cQINIU:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = """
            select q.usr_id,
            convert_from(decrypt(q.access_key::bytea, %s, 'aes'),'SQL_ASCII') as access_key,
            convert_from(decrypt(q.secret_key::bytea, %s, 'aes'),'SQL_ASCII') as secret_key,
            convert_from(decrypt(q.cname::bytea, %s, 'aes'),'SQL_ASCII') as cname,
            convert_from(decrypt(q.domain_url::bytea, %s, 'aes'),'SQL_ASCII') as domain_url,
            endpoint,COALESCE(ctype,0)ctype 
                    from qiniu  q
             left join users u on u.usr_id=q.usr_id 
            where   coalesce(u.expire_flag,0)=0 order by q.usr_id 
        
        """
        lT, iN = self.db.fetchall(sql,[self.md5code,self.md5code,self.md5code,self.md5code])
        for e in lT:
            k = e.pop('usr_id')
            dT[str(k)]= e

        self.__d = dT

    def update(self, sType):
        self.__d[str(sType)] = {}
        sql = """ select  convert_from(decrypt(q.access_key::bytea, %s, 'aes'),'SQL_ASCII') as access_key,
            convert_from(decrypt(q.secret_key::bytea, %s, 'aes'),'SQL_ASCII') as secret_key,
            convert_from(decrypt(q.cname::bytea, %s, 'aes'),'SQL_ASCII') as cname,
            convert_from(decrypt(q.domain_url::bytea, %s, 'aes'),'SQL_ASCII') as domain_url,
            endpoint,COALESCE(ctype,0)ctype 
                    from qiniu  q
             left join users u on u.usr_id=q.usr_id 
            where   coalesce(u.expire_flag,0)=0  and q.usr_id=%s"""
        self.__d[str(sType)] = self.db.fetch(sql,[self.md5code,self.md5code,self.md5code,self.md5code,sType])

        return

    def get(self, sType):
        return self.__d.get(str(sType), {})


class cGOODS:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}
            sql = u"""
            select id	--商品ID
                ,cname	--商品名称
                ,introduce	--商品简介
                ,recomm as status 	--是否推荐
                ,pic	--商品第一张图片
                ,originalprice as original_price	--商品原价
                ,minprice as mini_price	--商品现价
                ,round(CAST(case when (select up_type from  shop_set where usr_id=%s limit 1)=1 then (select discount from  shop_set where usr_id=%s limit 1)* minprice/100
                else ( select level_discount from hy_up_level where usr_id=%s order by level_discount limit 1)* minprice/100 end as numeric),2) vip_price 
                ,limited	--限购数量
                ,COALESCE(stores,0) as stores	--商品库存
                ,barcodes	--商品编码
                ,weight
                ,COALESCE(orders,0) as orders	--商品销量
                --,COALESCE(views,0) as views	--商品浏览量
                --,COALESCE(favorite,0) as favorite	--商品收藏量
                ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                ,discount
                ,category_ids
                --,content
                ,COALESCE(pt_status,0) as pt_status
            from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0
                    """
            lT1, iN1 = self.db.fetchall(sql,[k,k,k,k])

            dT[str(k)] = lT1

        self.__d = dT

    def update(self, sType,id=0):

        self.__d[str(sType)] = {}
        sql = u"""
        select id	--商品ID
            ,cname	--商品名称
            ,introduce	--商品简介
            ,recomm as status 	--是否推荐
            ,pic	--商品第一张图片
            ,originalprice as original_price	--商品原价
            ,minprice as mini_price	--商品现价
            ,round(CAST(case when (select up_type from  shop_set where usr_id=%s limit 1)=1 then (select discount from  shop_set where usr_id=%s limit 1)* minprice/100
            else ( select level_discount from hy_up_level where usr_id=%s order by level_discount limit 1)* minprice/100 end as numeric),2) vip_price 
            ,limited	--限购数量
            ,COALESCE(stores,0) as stores	--商品库存
            ,barcodes	--商品编码
            ,weight
            ,COALESCE(orders,0) as orders	--商品销量
           -- ,COALESCE(views,0) as views	--商品浏览量
            --,COALESCE(favorite,0) as favorite	--商品收藏量
            ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
            ,discount
            ,category_ids
            --,content
            ,COALESCE(pt_status,0) as pt_status
        from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 
                """
        lT1, iN1 = self.db.fetchall(sql, [sType,sType,sType,sType])
        self.__d[str(sType)] = lT1
        return


    def updateo(self, sType,id):
        self.update(str(sType))
        return

    def updates(self, sType,id,num):
        self.update(str(sType))
        return

    def updatef(self, sType,id,num):
        self.update(str(sType))
        return

    def updatev(self, sType,id):
        self.update(str(sType))
        return

    def get(self, sType):
        return self.__d.get(str(sType),{})


class cGOODS_SELL:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}
            sql = u"""
             SELECT
                D.id,
                D.cname,
                D.category_ids,
                D.pic,
                D.status,
              
                D.recomm,
                D.stores,
                D.originalprice ,
                D.minprice
    
            FROM goods_info D
            where COALESCE(D.del_flag,0)=0 and  D.usr_id=%s
            order by D.recomm desc,D.id
                    """
            lT1, iN1 = self.db.fetchall(sql,k)
            dT[str(k)] = lT1
        self.__d = dT

    def update(self, sType):

        self.__d[str(sType)] = {}
        sql = u"""
         SELECT
                D.id,
                D.cname,
                D.category_ids,
                D.pic,
                D.status,
               
                D.recomm,
                D.stores,
                D.originalprice ,
                D.minprice
                
            FROM goods_info D
            where COALESCE(D.del_flag,0)=0 and  D.usr_id=%s 
            order by D.recomm desc,D.id
                """
        lT1, iN1 = self.db.fetchall(sql, sType)

        self.__d[str(sType)] = lT1

        return

    def get(self, sType):
        return self.__d.get(str(sType),[])


class cGOODS_D:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}
            sql="select id from goods_info where usr_id=%s"
            lT1,iN1=self.db.select(sql,k)
            if iN1>0:
                for j in lT1:
                    id=j[0]
                    dT[str(k)][str(id)]={}
                    sql = """
                    select id	--商品ID
                        ,barcodes as barcode	--商品编码
                        ,cname	--商品名称
                        ,introduce	--商品简介
                        ,pic	--商品第一张图片
                        ,video
                        ,status
                        ,COALESCE(minprice,0) as mini_price	--商品现价
                        ,COALESCE(originalprice,0) as original_price	--商品原价
                        ,round(CAST(case when (select up_type from  shop_set where usr_id=%s limit 1)=1 then (select discount from  shop_set where usr_id=%s limit 1)* minprice/100
                        else ( select level_discount from hy_up_level where usr_id=%s order by level_discount limit 1)* minprice/100 end as numeric),2) vip_price
                        ,COALESCE(stores,0)stores	--商品库存
                        ,COALESCE(weight,0)weight
                        ,COALESCE(favorite,0)as favorite	--商品收藏量
                        ,COALESCE(see,0) as views	--商品浏览量
                        ,COALESCE(orders,0) as orders	--商品销量
                        ,discount as vip_open --是否开启会员折扣
                        ,limited as max_number	--限购数量
                        ,contents   --商品详情
                        ,to_char(ctime,'YYYY-MM-DD HH24:MI') as date_add	--商品添加时间
        
                        ,share_imgs    --商品分享海报
                        ,share_title   --商品分享标题
                        ,share_type    --商品分享返现类型
                        ,share_type_str    --商品分享返现类型
                        ,share_time    --商品分享返现时效
                        ,share_return   --商品分享返现数值
                        ,return_ticket  --商品分享返的优惠券id
                    from goods_info  
                    where usr_id=%s and COALESCE(del_flag,0)=0  and id=%s
                    """
                    parm = [k, k, k, k,id]
                    i = self.db.fetch(sql, parm)
                    if i!={}:
                        sql = "select id,goods_id,pic from goods_pics where goods_id=%s"
                        pics, n = self.db.fetchall(sql, id)  # pics商品图片列表
                        mini_price=i.get('mini_price','')
                        ticket_id=i.get('return_ticket','')
                        share_type=i.get('share_type', '')
                        share_time = i.get('share_time', '')
                        share_number=0
                        if str(share_type)=='1' or str(share_type)=='2':
                            share_number=i['share_return']
                        elif str(share_type)=='3' and ticket_id!='':
                            sql="select apply_id,apply_ext_num from coupons where usr_id=%s and id=%s"
                            ll,tt=self.db.select(sql,[k,ticket_id])
                            if tt>0:
                                apply_id, apply_ext_num=ll[0]
                                if str(apply_id)=='0':
                                    share_number=apply_ext_num
                                else:
                                    share_number = round(float(apply_ext_num)/100,2)
                        shareInfo = {'share_imgs': i.get('share_imgs', ''), 'share_title': i.get('share_title', ''),
                                     'share_type': share_type, 'share_type_str': i.get('share_type_str', ''),
                                     'share_time': share_time, 'share_number': share_number,
                                     #'share_coupons': ''
                                     }  # 商品分享数据

                        i.pop('share_imgs')
                        i.pop('share_title')
                        i.pop('share_type')
                        i.pop('share_type_str')
                        i.pop('share_time')
                        i.pop('share_return')
                        #i.pop('return_ticket')
                        datas = {'basicInfo': i, 'pics': pics, 'shareInfo': shareInfo}
                        vipInfo = []
                        if str(i.get('vip_open', '')) == '1':  # 开启就用
                            sql = """
                                select id,COALESCE(vip_price,0),discount,up_type 
                                from shop_set where usr_id=%s
                            """
                            L, t = self.db.select(sql,k)
                            if t > 0:
                                vip_id, vip_price, vip_sale, vtype = L[0]
                                if str(vtype) == '1':  # 付费升级
                                    Di = {'vip_id': 0, 'vip_price': vip_price, 'vip_name': '会员', 'vip_sale': vip_sale}
                                    vipInfo.append(Di)
                                elif str(vtype) == '2':  # 购物升级
                                    sqlv = """
                                    select id as vip_id,up_price as vip_price,
                                    cname as vip_name,COALESCE(level_discount,0) vip_sale 
                                    from hy_up_level where usr_id=%s order by up_price"""
                                    vipInfo, t = self.db.fetchall(sqlv, k)
                        if len(vipInfo) > 0:
                            for f in vipInfo:
                                vip_sale=f['vip_sale']
                                if vip_sale!='':
                                    f['vip_price']=round(float(mini_price)*float(vip_sale)/100,2)
                            datas['vipInfo'] = vipInfo
                        sqls = "select sc_id from spec_child_price where usr_id=%s and goods_id=%s"
                        sp_p = []
                        sp_c = []
                        ll, t = self.db.select(sqls, [k, id])
                        for i in ll:
                            I = i[0].split(',')
                            for j in I:
                                A = j.split(':')
                                if A[0] not in sp_p:
                                    sp_p.append(A[0])
                                if A[1] not in sp_c:
                                    sp_c.append(A[1])

                        specInfo = []
                        if len(sp_p) > 0:
                            SP_P = ','.join(sp_p)
                            SP_C = ','.join(sp_c)
                            sqlp = """
                                    select id as spec_id,cname as spec_name,ctype as spec_type,
                                    cicon as spec_icons,sort as spec_paixu,
                                    to_char(ctime,'YYYY-MM-DD HH24:MI')spec_time
                                    from spec where id in (%s) and usr_id=%s and  coalesce(del_flag,0)=0 order by sort
                            """ % (SP_P,k)
                            specInfo, t = self.db.fetchall(sqlp)
                            if t > 0:
                                for A in specInfo:
                                    sqlsc = """
                                        select id as chil_id,cname_c as chil_name,
                                            ctype_c as chil_type,cicon_c as chil_icons,
                                            sort_c as chil_paixu,
                                            to_char(ctime,'YYYY-MM-DD HH24:MI') as chil_time
                                        from spec_child
                                        where id in  (%s) and spec_id=%s
                                    """ % (SP_C, A.get('spec_id'))
                                    A['spec_childs'], t = self.db.fetchall(sqlsc)
                        if len(specInfo) > 0:
                            datas['specInfo'] = specInfo

                        dT[str(k)][str(id)]=datas

        self.__d = dT

    def update(self, sType,id=''):
        if id=='':
            self.__d[str(sType)] = {}
            sql = "select id from goods_info where usr_id=%s and COALESCE(del_flag,0)=0 "
            lT1, iN1 = self.db.select(sql, sType)
            if iN1 > 0:
                for j in lT1:
                    did = j[0]
                    self.__d[str(sType)][str(did)]={}
                    sql = """
                    select id	--商品ID
                        ,barcodes as barcode	--商品编码
                        ,cname	--商品名称
                        ,introduce	--商品简介
                        ,pic	--商品第一张图片
                        ,video
                        ,status
                        ,COALESCE(minprice,0) as mini_price	--商品现价
                        ,COALESCE(originalprice,0) as original_price	--商品原价
                        ,round(CAST(case when (select up_type from  shop_set where usr_id=%s limit 1)=1 then (select discount from  shop_set where usr_id=%s limit 1)* minprice/100
                        else ( select level_discount from hy_up_level where usr_id=%s order by level_discount limit 1)* minprice/100 end as numeric),2) vip_price
                        ,COALESCE(stores,0)stores	--商品库存
                        ,COALESCE(weight,0)weight
                        ,COALESCE(favorite,0)as favorite	--商品收藏量
                        ,COALESCE(see,0) as views	--商品浏览量
                        ,COALESCE(orders,0) as orders	--商品销量
                        ,discount as vip_open --是否开启会员折扣
                        ,limited as max_number	--限购数量
                        ,contents   --商品详情
                        ,to_char(ctime,'YYYY-MM-DD HH24:MI') as date_add	--商品添加时间

                        ,share_imgs    --商品分享海报
                        ,share_title   --商品分享标题
                        ,share_type    --商品分享返现类型
                        ,share_type_str    --商品分享返现类型
                        ,share_time    --商品分享返现时效
                        ,share_return   --商品分享返现数值
                        ,return_ticket  --商品分享返的优惠券id
                    from goods_info  
                    where usr_id=%s and COALESCE(del_flag,0)=0  and id=%s
                    """
                    parm = [sType, sType,sType,sType, did]
                    i = self.db.fetch(sql, parm)
                    if i != {}:
                        sql = "select id,goods_id,pic from goods_pics where goods_id=%s"
                        pics, n = self.db.fetchall(sql, did)  # pics商品图片列表
                        mini_price = i.get('mini_price', '')
                        ticket_id = i.get('return_ticket', '')
                        share_type = i.get('share_type', '')
                        share_time = i.get('share_time', '')
                        share_number = 0
                        if str(share_type) == '1' or str(share_type) == '2':
                            share_number = i['share_return']
                        elif str(share_type) == '3' and ticket_id != '':
                            sql = "select apply_id,apply_ext_num from coupons where usr_id=%s and id=%s"
                            ll, tt = self.db.select(sql, [sType, ticket_id])
                            if tt > 0:
                                apply_id, apply_ext_num = ll[0]
                                if str(apply_id) == '0':
                                    share_number = apply_ext_num
                                else:
                                    share_number = round(float(apply_ext_num) / 100, 2)

                        shareInfo = {'share_imgs': i.get('share_imgs', ''), 'share_title': i.get('share_title', ''),
                                     'share_type': share_type,
                                     'share_type_str': i.get('share_type_str', ''),
                                     'share_time': share_time, 'share_number': share_number,
                                     #'share_coupons': ''
                                     }  # 商品分享数据

                        i.pop('share_imgs')
                        i.pop('share_title')
                        i.pop('share_type')
                        i.pop('share_type_str')
                        i.pop('share_time')
                        i.pop('share_return')
                        #i.pop('return_ticket')
                        datas = {'basicInfo': i, 'pics': pics, 'shareInfo': shareInfo}
                        vipInfo = []
                        if str(i.get('vip_open', '')) == '1':  # 开启就用
                            sql = """
                                select id,COALESCE(vip_price,0),discount,up_type 
                                from shop_set where usr_id=%s 
                            """
                            L, t = self.db.select(sql, sType)
                            if t > 0:
                                vip_id, vip_price, vip_sale, vtype = L[0]
                                if str(vtype) == '1':  # 付费升级
                                    Di = {'vip_id': 0, 'vip_price': vip_price, 'vip_name': '会员',
                                          'vip_sale': vip_sale}
                                    vipInfo.append(Di)
                                elif str(vtype) == '2':  # 购物升级
                                    sqlv = """
                                    select id as vip_id,up_price as vip_price,
                                    cname as vip_name,COALESCE(level_discount,0)vip_sale 
                                    from hy_up_level where usr_id=%s order by up_price"""
                                    vipInfo, t = self.db.fetchall(sqlv, sType)
                        if len(vipInfo) > 0:
                            for f in vipInfo:
                                vip_sale=f['vip_sale']
                                if vip_sale != '':
                                    f['vip_price']=round(float(mini_price)*float(vip_sale)/100,2)
                            datas['vipInfo'] = vipInfo
                        sqls = "select sc_id from spec_child_price where usr_id=%s and goods_id=%s"
                        sp_p = []
                        sp_c = []
                        ll, t = self.db.select(sqls, [sType, did])
                        for i in ll:
                            I = i[0].split(',')
                            for j in I:
                                A = j.split(':')
                                if A[0] not in sp_p:
                                    sp_p.append(A[0])
                                if A[1] not in sp_c:
                                    sp_c.append(A[1])

                        specInfo = []
                        if len(sp_p) > 0:
                            SP_P = ','.join(sp_p)
                            SP_C = ','.join(sp_c)
                            sqlp = """
                                    select id as spec_id,cname as spec_name,ctype as spec_type,
                                    cicon as spec_icons,sort as spec_paixu,
                                    to_char(ctime,'YYYY-MM-DD HH24:MI')spec_time
                                    from spec where id in (%s) and usr_id=%s and coalesce(del_flag,0)=0 order by sort
                            """ % (SP_P, sType)
                            specInfo, t = self.db.fetchall(sqlp)
                            if t > 0:
                                for A in specInfo:
                                    sqlsc = """
                                        select id as chil_id,cname_c as chil_name,
                                            ctype_c as chil_type,cicon_c as chil_icons,
                                            sort_c as chil_paixu,
                                            to_char(ctime,'YYYY-MM-DD HH24:MI') as chil_time
                                        from spec_child
                                        where id in  (%s) and spec_id=%s
                                    """ % (SP_C, A.get('spec_id'))
                                    A['spec_childs'], t = self.db.fetchall(sqlsc)
                        if len(specInfo) > 0:
                            datas['specInfo'] = specInfo

                        self.__d[str(sType)][str(did)] = datas

            return
        self.__d[str(sType)][str(id)] = {}
        sql = """
        select id	--商品ID
            ,barcodes as barcode	--商品编码
            ,cname	--商品名称
            ,introduce	--商品简介
            ,pic	--商品第一张图片
            ,video
            ,status
            ,COALESCE(minprice,0)mini_price	--商品现价
            ,COALESCE(originalprice,0)original_price	--商品原价
            ,round(CAST(case when (select up_type from  shop_set where usr_id=%s limit 1)=1 then (select discount from  shop_set where usr_id=%s limit 1)* minprice/100
            else ( select level_discount from hy_up_level where usr_id=%s order by level_discount limit 1)* minprice/100 end as numeric),2) vip_price
            ,COALESCE(stores,0)stores	--商品库存
            ,COALESCE(weight,0)weight
            ,COALESCE(favorite,0)as favorite	--商品收藏量
            ,COALESCE(see,0) as views	--商品浏览量
            ,COALESCE(orders,0) as orders	--商品销量
            ,discount as vip_open --是否开启会员折扣
            ,limited as max_number	--限购数量
            ,contents   --商品详情
            ,to_char(ctime,'YYYY-MM-DD HH24:MI') as date_add	--商品添加时间

            ,share_imgs    --商品分享海报
            ,share_title   --商品分享标题
            ,share_type    --商品分享返现类型
            ,share_type_str    --商品分享返现类型
            ,share_time    --商品分享返现时效
            ,share_return   --商品分享返现数值
            ,return_ticket  --商品分享返的优惠券id
        from goods_info  
        where usr_id=%s and COALESCE(del_flag,0)=0  and id=%s
        """
        parm = [sType,sType,sType, sType, id]
        i = self.db.fetch(sql, parm)

        sql = "select id,goods_id,pic from goods_pics where goods_id=%s"
        pics, n = self.db.fetchall(sql, id)  # pics商品图片列表
        mini_price = i.get('mini_price', '')
        ticket_id = i.get('return_ticket', '')
        share_type = i.get('share_type', '')
        share_time = i.get('share_time', '')
        share_number = 0
        if str(share_type) == '1' or str(share_type) == '2':
            share_number = i['share_return']
        elif str(share_type) == '3' and ticket_id != '':
            sql = "select apply_id,apply_ext_num from coupons where usr_id=%s and id=%s"
            ll, tt = self.db.select(sql, [sType, ticket_id])
            if tt > 0:
                apply_id, apply_ext_num = ll[0]
                if str(apply_id) == '0':
                    share_number = apply_ext_num
                else:
                    share_number = round(float(apply_ext_num) / 100, 2)
        shareInfo = {'share_imgs': i.get('share_imgs', ''), 'share_title': i.get('share_title', ''),
                     'share_type': share_type, 'share_type_str': i.get('share_type_str', ''),
                     'share_time': share_time, 'share_number': share_number,
                     #'share_coupons': ''
                     }  # 商品分享数据
        i.pop('share_imgs')
        i.pop('share_title')
        i.pop('share_type')
        i.pop('share_type_str')
        i.pop('share_time')
        i.pop('share_return')
        #i.pop('return_ticket')
        datas = {'basicInfo': i, 'pics': pics, 'shareInfo': shareInfo}
        vipInfo = []
        if str(i.get('vip_open', '')) == '1':  # 开启就用
            sql = """
                select id,COALESCE(vip_price,0),discount,up_type 
                from shop_set where usr_id=%s
            """
            L, t = self.db.select(sql,sType)
            if t > 0:
                vip_id, vip_price, vip_sale, vtype = L[0]
                if str(vtype) == '1':  # 付费升级
                    Di = {'vip_id': 0, 'vip_price': vip_price, 'vip_name': '会员', 'vip_sale': vip_sale}
                    vipInfo.append(Di)
                elif str(vtype) == '2':  # 购物升级
                    sqlv = """
                        select id as vip_id,up_price as vip_price,
                        cname as vip_name,COALESCE(level_discount,0)vip_sale 
                        from hy_up_level where usr_id=%s order by up_price"""
                    vipInfo, t = self.db.fetchall(sqlv, sType)
        if len(vipInfo) > 0:
            for f in vipInfo:
                vip_sale = f['vip_sale']
                if vip_sale != '':
                    f['vip_price'] = round(float(mini_price) *float(vip_sale)/100, 2)
            datas['vipInfo'] = vipInfo
        sqls = "select sc_id from spec_child_price where usr_id=%s and goods_id=%s"
        sp_p = []
        sp_c = []
        ll, t = self.db.select(sqls, [sType, id])
        for i in ll:
            I = i[0].split(',')
            for j in I:
                A = j.split(':')
                if A[0] not in sp_p:
                    sp_p.append(A[0])
                if A[1] not in sp_c:
                    sp_c.append(A[1])

        specInfo = []
        if len(sp_p) > 0:
            SP_P = ','.join(sp_p)
            SP_C = ','.join(sp_c)
            sqlp = """
                    select id as spec_id,cname as spec_name,ctype as spec_type,
                    cicon as spec_icons,sort as spec_paixu,
                    to_char(ctime,'YYYY-MM-DD HH24:MI')spec_time
                    from spec where id in (%s) and usr_id=%s and coalesce(del_flag,0)=0 order by sort
            """ % (SP_P,sType)
            specInfo, t = self.db.fetchall(sqlp)
            if t > 0:
                for A in specInfo:
                    sqlsc = """
                        select id as chil_id,cname_c as chil_name,
                            ctype_c as chil_type,cicon_c as chil_icons,
                            sort_c as chil_paixu,
                            to_char(ctime,'YYYY-MM-DD HH24:MI') as chil_time
                        from spec_child
                        where id in  (%s) and spec_id=%s
                    """ % (SP_C, A.get('spec_id'))
                    A['spec_childs'], t = self.db.fetchall(sqlsc)
        if len(specInfo) > 0:
            datas['specInfo'] = specInfo

        self.__d[str(sType)][str(id)] = datas

        return

    def updatev(self, sType,id):
        views=self.__d[str(sType)][str(id)]['basicInfo'].get('views','')
        self.__d[str(sType)][str(id)]['basicInfo']['views']=int(views)+1

        return

    def updatef(self, sType,id,num):
        views=self.__d[str(sType)][str(id)]['basicInfo'].get('favorite','')
        self.__d[str(sType)][str(id)]['basicInfo']['favorite']=int(views)+num

        return

    def updateo(self, sType,id):
        views=self.__d[str(sType)][str(id)]['basicInfo'].get('orders','')
        self.__d[str(sType)][str(id)]['basicInfo']['orders']=int(views)+1

        return

    def updates(self, sType,id,num):
        views=self.__d[str(sType)][str(id)]['basicInfo'].get('stores','')
        self.__d[str(sType)][str(id)]['basicInfo']['stores']=int(views)-num

        return



    def get(self, sType, sID):

        return self.__d.get(str(sType), {}).get(str(sID), {})


class cGOODS_PT:

    def __init__(self, db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}
            sql = """select goods_id from pt_conf where usr_id=%s and COALESCE(del_flag,0)=0
                        and COALESCE(status,0)=0
                        """
            lT1, iN1 = self.db.select(sql, k)
            if iN1 > 0:
                for j in lT1:
                    id = j[0]
                    dT[str(k)][str(id)] = {}
                    sqlpt = """
                            select p.id,g.pt_price as price,pt_num as number,
                            ok_num as success,to_char(date_add,'YYYY-MM-DD HH24:MI')date_start,
                            to_char(date_end,'YYYY-MM-DD HH24:MI')date_end,kt_type as ptkstat,
                            add_type as ptcstat,
                            case when to_char(date_end,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
                            then 0 else 2 end status
                            from pt_conf p
                            left join goods_info g on g.id=p.goods_id and g.usr_id=p.usr_id
                            where p.usr_id=%s and goods_id=%s
                            """
                    pingtuanInfo = self.db.fetch(sqlpt, [k, id])
                    dT[str(k)][str(id)] = pingtuanInfo

        self.__d = dT

    def update(self, sType, id=''):
        if id == '':
            self.__d[str(sType)] = {}
            sql = """select goods_id from pt_conf where usr_id=%s and COALESCE(del_flag,0)=0
                    and COALESCE(status,0)=0
                    """
            lT1, iN1 = self.db.select(sql, sType)
            if iN1 > 0:
                for j in lT1:
                    did = j[0]
                    self.__d[str(sType)][str(did)] = {}
                    sqlpt = """
                            select p.id,g.pt_price as price,pt_num as number,
                            ok_num as success,to_char(date_add,'YYYY-MM-DD HH24:MI')date_start,
                            to_char(date_end,'YYYY-MM-DD HH24:MI')date_end,kt_type as ptkstat,
                            add_type as ptcstat,
                            case when to_char(date_end,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
                            then 0 else 2 end status
                            from pt_conf p
                            left join goods_info g on g.id=p.goods_id and g.usr_id=p.usr_id
                            where p.usr_id=%s and goods_id=%s
                            """
                    pingtuanInfo = self.db.fetch(sqlpt, [sType, did])
                    self.__d[str(sType)][str(did)] = pingtuanInfo

            return
        try:
            self.__d[str(sType)][str(id)] = {}
        except:
            return
        sqlpt = """
                select p.id,g.pt_price as price,pt_num as number,
                    ok_num as success,to_char(date_add,'YYYY-MM-DD HH24:MI')date_start,
                    to_char(date_end,'YYYY-MM-DD HH24:MI')date_end,kt_type as ptkstat,
                    add_type as ptcstat,
                    case when to_char(date_end,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
                            then 0 else 2 end status
                    from pt_conf p
                    left join goods_info g on g.id=p.goods_id and g.usr_id=p.usr_id
                    where p.usr_id=%s and goods_id=%s
                """
        pingtuanInfo = self.db.fetch(sqlpt, [sType, id])
        self.__d[str(sType)][str(id)] = pingtuanInfo
        return

    def get(self, sType, sID):
        return self.__d.get(str(sType), {}).get(str(sID), {})


class cGOODS_DPT:

    def __init__(self, db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}
            sql = """select g.id 
                        ,g.cname	--商品名称
                        ,g.introduce	--商品简介
                        ,g.pic	--商品第一张图片
                        ,g.minprice as mini_price	--商品现价
                        ,g.originalprice as original_price	--商品原价
                        ,g.pt_price
                        ,p.pt_num as ptuan_success
                        ,p.ok_num as ptuan_number
                        ,p.id as ptuan_id
                        ,p.kt_type as ptuan_ktype
                        ,p.add_type as ptuan_ctype
                    from pt_conf p
                    left join goods_info g on p.usr_id=g.usr_id and p.goods_id=g.id
                    where p.usr_id=%s and COALESCE(g.del_flag,0)=0 and COALESCE(p.del_flag,0)=0
                        and COALESCE(g.status,0)=0  and COALESCE(g.pt_status,0)=1 """
            lT1, iN1 = self.db.fetchall(sql, k)
            if iN1 > 0:
                for j in lT1:
                    id = j['id']
                    dT[str(k)][str(id)] = j

        self.__d = dT

    def update(self, sType, id=''):
        if str(id) == '':
            self.__d[str(sType)] = {}
            sql = """select g.id 
                    ,g.cname	--商品名称
                    ,g.introduce	--商品简介
                    ,g.pic	--商品第一张图片
                    ,g.minprice as mini_price	--商品现价
                    ,g.originalprice as original_price	--商品原价
                    ,g.pt_price
                    ,p.pt_num as ptuan_success
                    ,p.ok_num as ptuan_number
                    ,p.id as ptuan_id
                    ,p.kt_type as ptuan_ktype
                    ,p.add_type as ptuan_ctype
                from pt_conf p
                left join goods_info g on p.usr_id=g.usr_id and p.goods_id=g.id
                where p.usr_id=%s and COALESCE(g.del_flag,0)=0 and COALESCE(p.del_flag,0)=0
                    and COALESCE(g.status,0)=0  and COALESCE(g.pt_status,0)=1 """
            lT1, iN1 = self.db.fetchall(sql, sType)
            if iN1 > 0:
                for j in lT1:
                    id = j['id']
                    self.__d[str(sType)][str(id)] = j

            return
        try:
            self.__d[str(sType)][str(id)] = {}
        except:
            return
        #self.__d[str(sType)][str(id)] = {}
        sql = """select g.id 
                ,g.cname	--商品名称
                ,g.introduce	--商品简介
                ,g.pic	--商品第一张图片
                ,g.minprice as mini_price	--商品现价
                ,g.originalprice as original_price	--商品原价
                ,g.pt_price
                ,p.pt_num as ptuan_success
                ,p.ok_num as ptuan_number
                ,p.id as ptuan_id
                ,p.kt_type as ptuan_ktype
                ,p.add_type as ptuan_ctype
            from pt_conf p
            left join goods_info g on p.usr_id=g.usr_id and p.goods_id=g.id
            where p.usr_id=%s and COALESCE(g.del_flag,0)=0 and COALESCE(p.del_flag,0)=0
                and COALESCE(g.status,0)=0  and COALESCE(g.pt_status,0)=1 
                and p.goods_id=%s"""
        datas = self.db.fetch(sql, [sType, id])
        self.__d[str(sType)][str(id)] = datas

        return



    def get(self, sType, sID=''):
        if sID != '':
            return self.__d.get(str(sType), {}).get(str(sID), {})
        else:
            return self.__d.get(str(sType), {})


class cPT_GOODS:

    def __init__(self, db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}
            sql = """select p.id
                        ,p.goods_id as gid
                        ,g.cname	as gname 
                        ,g.introduce as gintr
                        ,g.pic as gpic
                        ,g.minprice as mini_price	--商品现价
                        ,g.contents as gcontent
                        ,g.pt_price
                        ,timeout_h 
                        ,p.pt_num as cnumber
                        ,p.ok_num as stores
                        ,ok_type
                        ,add_type
                        ,tk_type
                        ,kt_type
                    from pt_conf p
                    left join goods_info g on p.usr_id=g.usr_id and p.goods_id=g.id
                    where p.usr_id=%s and COALESCE(g.del_flag,0)=0 and COALESCE(p.del_flag,0)=0
                        and COALESCE(g.status,0)=0  and COALESCE(g.pt_status,0)=1 """
            lT1, iN1 = self.db.fetchall(sql, k)
            if iN1 > 0:
                for j in lT1:
                    id = j['id']
                    dT[str(k)][str(id)] = j

        self.__d = dT

    def update(self, sType, id=''):
        if str(id) == '':
            self.__d[str(sType)] = {}
            sql = """select p.id
                        ,p.goods_id as gid
                        ,g.cname	as gname 
                        ,g.introduce as gintr
                        ,g.pic as gpic
                        ,g.minprice as mini_price	--商品现价
                        ,g.contents as gcontent
                        ,g.pt_price
                        ,timeout_h 
                         ,p.pt_num as cnumber
                        ,p.ok_num as stores
                        ,ok_type
                        ,add_type
                        ,tk_type
                        ,kt_type
                from pt_conf p
                left join goods_info g on p.usr_id=g.usr_id and p.goods_id=g.id
                where p.usr_id=%s and COALESCE(g.del_flag,0)=0 and COALESCE(p.del_flag,0)=0
                    and COALESCE(g.status,0)=0  and COALESCE(g.pt_status,0)=1 """
            lT1, iN1 = self.db.fetchall(sql, sType)
            if iN1 > 0:
                for j in lT1:
                    did = j['id']
                    self.__d[str(sType)][str(did)] = j

            return

        self.__d[str(sType)][str(id)] = {}
        sql = """select p.id
                        ,p.goods_id as gid
                        ,g.cname	as gname 
                        ,g.introduce as gintr
                        ,g.pic as gpic
                        ,g.minprice as mini_price	--商品现价
                        ,g.contents as gcontent
                        ,g.pt_price
                        ,timeout_h 
                        ,p.pt_num as cnumber
                        ,p.ok_num as stores
                        ,ok_type
                        ,add_type
                        ,tk_type
                        ,kt_type
            from pt_conf p
            left join goods_info g on p.usr_id=g.usr_id and p.goods_id=g.id
            where p.usr_id=%s and COALESCE(g.del_flag,0)=0 and COALESCE(p.del_flag,0)=0
                and COALESCE(g.status,0)=0  and COALESCE(g.pt_status,0)=1 
                and p.id=%s"""
        datas = self.db.fetch(sql, [sType, id])
        self.__d[str(sType)][str(id)] = datas

        return


    def get(self, sType, sID=''):
        if sID != '':
            return self.__d.get(str(sType), {}).get(str(sID), {})
        else:
            return self.__d.get(str(sType), {})


class cORDER_SET:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = """
            select s.usr_id,use_money ,close_time,cancel_id,
                        send_id,evaluate_id ,complete_id,
                        take_day
                    from  shop_set s
             left join users u on u.usr_id=s.usr_id 
            where   coalesce(u.expire_flag,0)=0 order by s.usr_id
        """
        lT, iN = self.db.fetchall(sql)
        for e in lT:
            k = e.pop('usr_id')
            dT[str(k)] = e

        self.__d = dT

    def update(self, sType):
        self.__d[str(sType)] = {}
        sql = """select use_money ,close_time,cancel_id,
                        send_id,evaluate_id ,complete_id,
                        take_day
                    from  shop_set s
             left join users u on u.usr_id=s.usr_id 
            where   coalesce(u.expire_flag,0)=0 and s.usr_id=%s"""

        self.__d[str(sType)] = self.db.fetch(sql,[sType])

        return

    def get(self, sType):
        return self.__d.get(str(sType), {})


class cGOODS_N:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}
            sql = u"""
            select id	--商品ID
                ,cname	--商品名称
                ,introduce	--商品简介
                ,pic	--商品第一张图片
                ,originalprice as original_price	--商品原价
                ,minprice as mini_price	--商品现价
                ,COALESCE(stores,0) as stores	--商品库存
                ,COALESCE(orders,0) as orders	--商品销量
                ,to_char(ctime,'YYYY-MM-DD')date_add	--商品添加时间
            from goods_info  
            where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 
                    """
            lT2, iN2 = self.db.fetchall(sql,k)
            if iN2>0:
                for i in lT2:
                    id=i.get('id')
                    dT[str(k)][str(id)]=i

        self.__d = dT

    def update(self, sType,id=''):
        if id!='':
            self.__d[str(sType)][str(id)] = {}
            sql = u"""
                        select id	--商品ID
                            ,cname	--商品名称
                            ,introduce	--商品简介
                            ,pic	--商品第一张图片
                            ,originalprice as original_price	--商品原价
                            ,minprice as mini_price	--商品现价
                            ,COALESCE(stores,0) as stores	--商品库存
                            ,COALESCE(orders,0) as orders	--商品销量
                            ,to_char(ctime,'YYYY-MM-DD')date_add	--商品添加时间
                        from goods_info  
                        where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id=%s
                                """
            dT2 = self.db.fetch(sql,[sType,id])
            self.__d[str(sType)][str(id)]=dT2

            return

        self.__d[str(sType)]= {}
        sql = u"""
                select id	--商品ID
                    ,cname	--商品名称
                    ,introduce	--商品简介
                    ,pic	--商品第一张图片
                    ,originalprice as original_price	--商品原价
                    ,minprice as mini_price	--商品现价
                    ,COALESCE(stores,0) as stores	--商品库存
                    ,COALESCE(orders,0) as orders	--商品销量
                    ,to_char(ctime,'YYYY-MM-DD')date_add	--商品添加时间
                from goods_info  
                where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 
                        """
        l,t = self.db.fetchall(sql, sType)
        for i in l:
            id=i.get('id')
            self.__d[str(sType)][str(id)] = i

        return

    def get(self, sType):
        return self.__d.get(str(sType),{})


class cGOODS_G:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = []

            sql1="""
                select to_char(ctime,'YYYY-MM-DD')date
                from goods_info where usr_id=%s group by date order by date desc
            """
            lT1,iN1=self.db.select(sql1,k)
            if iN1>0:
                dT[str(k)]=lT1

        self.__d = dT

    def update(self, sType):
        self.__d[str(sType)] = []
        sql1 = """
            select to_char(ctime,'YYYY-MM-DD')date
            from goods_info where usr_id=%s group by date order by date desc
                    """
        lT1, iN1 = self.db.select(sql1,sType)
        if iN1 > 0:
            self.__d[str(sType)]=lT1

        return


    def get(self, sType):
        return self.__d.get(str(sType),[])


class cGOODS_H:

    def __init__(self,db):
        self.db = db
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = []
            sql = u"""
                select g.id	--商品ID
                    ,g.cname	--商品名称
                    ,g.introduce	--商品简介
                    ,g.pic	--商品第一张图片
                    ,g.originalprice as original_price	--商品原价
                    ,g.minprice as mini_price	--商品现价
                   
                    ,COALESCE(g.stores,0) as stores	--商品库存
                    ,COALESCE(g.orders,0) as orders	--商品销量
                    ,g.barcodes	--商品编码
                    ,g.weight
                    ,to_char(g.ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                   
                from hot_sell h 
                left join goods_info g on g.id=h.gid
                where COALESCE(h.del_flag,0)=0 and COALESCE(g.del_flag,0)=0 and g.status=0  and h.usr_id=%s 
                order by h.sort
                    """
            lT1, iN1 = self.db.fetchall(sql,[k])
            dT[str(k)]=lT1
        self.__d = dT

    def update(self,sType):
        self.__d[str(sType)]=[]

        sql = u"""
        select g.id	--商品ID
                ,g.cname	--商品名称
                ,g.introduce	--商品简介
                ,g.pic	--商品第一张图片
                ,g.originalprice as original_price	--商品原价
                ,g.minprice as mini_price	--商品现价
                
                ,COALESCE(g.stores,0) as stores	--商品库存
                ,COALESCE(g.orders,0) as orders	--商品销量
                ,g.barcodes	--商品编码
                ,g.weight
                ,to_char(g.ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
               
            from hot_sell h 
            left join goods_info g on g.id=h.gid
            where COALESCE(h.del_flag,0)=0 and COALESCE(g.del_flag,0)=0 and g.status=0  and h.usr_id=%s
            order by h.sort
                """
        lT1, iN1 = self.db.fetchall(sql,[sType])
        self.__d = lT1
        return

    def get(self, sType=''):
        if sType != '':
            return self.__d.get(str(sType), {})
        else:
            return self.__d


class cCATEGORY:

    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):
        dT = {}
        sql = "SELECT DISTINCT usr_id from users where status=1 and coalesce(expire_flag,0)=0"
        lT, iN = self.db.select(sql)
        for e in lT:
            k = e[0]
            dT[str(k)] = {}

            sql1="""
                select c.id,c.cname,c.ctype,c.pid,ca.cname as pid_name,
                    c.pic_icon,c.pic_imgs,c.remark,
                    c.paixu,to_char(c.ctime,'YYYY-MM-DD HH24:MI')time_add 
                from category c 
                left join category ca on ca.id=c.pid
                where COALESCE(c.del_flag,0)=0 and c.usr_id=%s order by c.paixu
            """
            lT1,iN=self.db.fetchall(sql1,k)
            if iN>0:
                dT[str(k)]=lT1

        self.__d = dT

    def update(self, sType):
        self.__d[str(sType)] = {}
        sql1 = """
         select c.id,c.cname,c.ctype,c.pid,ca.cname as pid_name,
                    c.pic_icon,c.pic_imgs,c.remark,
                    c.paixu,to_char(c.ctime,'YYYY-MM-DD HH24:MI')time_add 
                from category c 
                left join category ca on ca.id=c.pid
               
             left join users u on u.usr_id=c.usr_id 
            where   coalesce(u.expire_flag,0)=0  and COALESCE(c.del_flag,0)=0 and c.usr_id=%s order by c.paixu
            
                    """
        lT1,iN = self.db.fetchall(sql1,[sType])
        if iN>0:
            self.__d[str(sType)]=lT1

        return


    def get(self, sType):
        return self.__d.get(str(sType),[])


class cUSERS_OSS:

    def __init__(self, db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):

        sql = """select usr_id,coalesce(oss_all,100),coalesce(oss_now,0)oss_now,
        coalesce(qiniu_flag,0)qiniu_flag,coalesce(oss_flag,0)oss_flag,coalesce(expire_flag,0)expire_flag
                from users where coalesce(del_flag,0)=0 and coalesce(status,0)=1
            """
        l, t = self.db.fetchall(sql)
        for i in l:
            usr_id= i.pop('usr_id')
            self.__d[str(usr_id)] = i

    def update(self, sType):
        self.__d[str(sType)] = {}
        sqlu = "update users set oss_now=(select sum(f_size::float) from images where  usr_id=%s)/1024 where usr_id=%s"
        self.db.query(sqlu, [sType, sType])
        sql = """select coalesce(oss_all,100)oss_all,coalesce(oss_now,0)oss_now,
                    coalesce(qiniu_flag,0)qiniu_flag,coalesce(oss_flag,0)oss_flag, 
                    coalesce(expire_flag,0)expire_flag
                    from users where coalesce(del_flag,0)=0 and coalesce(status,0)=1 and usr_id=%s
                    """
        l = self.db.fetch(sql, [sType])
        self.__d[str(sType)] = l
    def updates(self, sType,id):
        views = self.__d[str(sType)].get('oss_now', 0)
        self.__d[str(sType)]['oss_now'] = float(views) + float(id)
        return
    def get(self, sType=''):
        if sType == '':
            return self.__d
        return self.__d.get(str(sType), {})


class cTOLL:
    """功能：将goods_info表装进内存中，提供上新接口调用。当该表修改时调用oGOODS_G.update()
       用法：get(self,sType)
    """
    def __init__(self,db,md5code):
        self.db = db
        self.md5code=md5code
        self.__d = {}
        self.loaddata()

    def loaddata(self):

        sql = """select 
                appid,
                secret,
                coalesce(wx_status,0)wx_status,
                wxtoken,
                wxaeskey,
                mchid,
                mchkey,
                back_url,
                base_url,
                coalesce(try_days,0)try_days,
                coalesce(invite_days,0)invite_days,
                coalesce(vip_days,0)vip_days,
                coalesce(pay_status,0)pay_status,
                combo_one_name,
                combo_one_price,
                combo_one_day,
                combo_one_txt,
                combo_two_name,
                combo_two_price,
                combo_two_day,
                combo_two_status,
                combo_two_txt,
                combo_thr_name,
                combo_thr_price,
                combo_thr_day,
                combo_thr_status,
                combo_thr_txt,
                /*call_url,
                re_url,
                oss_one_day,
                oss_one_size,
                oss_one_price,
                oss_two_day,
                oss_two_size,
                oss_two_price,
                oss_thr_day,
                oss_thr_size,
                oss_thr_price,
                domain_url,
                ptype,
                remark*/
                dbname,
                notices,
                memo
                
            from platform_conf where id=1
            """
        self.__d = self.db.fetch(sql)

    def update(self):
        self.__d={}
        sql = """select 
                appid,
                secret,
                coalesce(wx_status,0)wx_status,
                wxtoken,
                wxaeskey,
                mchid,
                mchkey,
                back_url,
                base_url,
                coalesce(try_days,0)try_days,
                coalesce(invite_days,0)invite_days,
                coalesce(vip_days,0)vip_days,
                coalesce(pay_status,0)pay_status,
                combo_one_name,
                combo_one_price,
                combo_one_day,
                combo_one_txt,
                combo_two_name,
                combo_two_price,
                combo_two_day,
                combo_two_status,
                combo_two_txt,
                combo_thr_name,
                combo_thr_price,
                combo_thr_day,
                combo_thr_status,
                combo_thr_txt,
                /*call_url,
                re_url,
                oss_one_day,
                oss_one_size,
                oss_one_price,
                oss_two_day,
                oss_two_size,
                oss_two_price,
                oss_thr_day,
                oss_thr_size,
                oss_thr_price,
                domain_url,
                ptype,
                remark*/
                dbname,
                notices,
                memo
                
            from platform_conf where id=1
                    """
        self.__d = self.db.fetch(sql)

        return

    def get(self, sType=''):
        if sType == '':
            return self.__d
        return self.__d.get(str(sType), '')
#########预加载数据结束









