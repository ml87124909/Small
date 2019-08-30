# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""api/BASE_TPL.py"""
"""
检查token，注册，登录，参数设置接口,Banner,商品分类,地址相关接口，收藏相关接口


"""

from imp import reload
from config import DEBUG,CLIENT_NAME
if DEBUG=='1':
    import api.VI_BASE
    reload(api.VI_BASE)
from api.VI_BASE             import cVI_BASE
from basic.wxbase import wx_minapp_login,WXBizDataCrypt,WxPay
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib,time,json,datetime,requests
from werkzeug import secure_filename

class cBASE_TPL(cVI_BASE):

    def goPartbegin(self):
        return self.jsons({'code':0,'data':u'你很调皮哦','msg':self.error_code[0]})

    def goPartchecktoken(self): #检查token
        token = self.REQUEST.get('token','')
        if token == '' or token == 'None' or token=='undefined':
            return self.jsons(({'code': 300, 'msg': self.error_code[300].format('token')}))

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})

        # sql=" select token from wechat_mall_access_token where token='%s' and usr_id=%s"%(token,self.subusr_id)
        # l,t=self.db.select(sql)
        # if t==0:
        #     return self.jsons({'code': 901, 'msg': self.error_code[901]})

        return self.jsons({'code': 0, 'msg': 'success'})

    def goPartregister(self): #注册
        code = self.REQUEST.get('code','')
        encrypted_data = self.REQUEST.get('encryptedData','')
        rawData = self.REQUEST.get('rawData','')
        iv = self.REQUEST.get('iv','')
        signature = self.REQUEST.get('signature','')

        if not code or code == '' or code == 'None' or code=='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('code')})

        if not encrypted_data or encrypted_data =='' or encrypted_data =='None'  or encrypted_data =='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('encryptedData')})

        if not iv or iv=='' or iv=='None' or iv=='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('iv')})

        if not rawData or rawData=='' or rawData=='None' or rawData=='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('rawData')})

        if not signature or signature=='' or signature=='None' or signature=='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('signature')})

        # sql = "select appid,secret  from mall where usr_id=%s"
        # l, t = self.db.select(sql,self.subusr_id)
        #
        # if t == 0:
        #     return self.jsons({'code': 404, 'msg': '请到后台填写‘微信设置’'})
        # app_id = l[0][0]
        # secret = l[0][1]
        mall = self.oMALL.get(self.subusr_id)
        if mall == {}:
            return self.jsons({'code': 404, 'msg': '请到店铺设置填写小程序设置'})
        app_id = mall['appid']
        secret = mall['secret']
        try:
            api=wx_minapp_login(app_id,secret)
            session_info = api.get_session_info(code=code)
            if session_info.get('errcode'):
                return self.jsons(
                    {'code': 602, 'msg': '微信用户信息解密错误请检查appid和secret信息', 'data': session_info.get('errmsg')})
            session_key = session_info.get('session_key')

            crypt = WXBizDataCrypt(app_id, session_key)
            # 解密得到 用户信息
            user_info = crypt.decrypt(encrypted_data, iv)
        except:
            return self.jsons({'code': 602, 'msg': '微信用户信息解密错误请检查appid和secret信息'})
        try:
            register_ip=self.objHandle.headers["X-Real-IP"]
        except:
            register_ip = self.objHandle.remote_addr
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=7)
        n_days = now + delta
        up_time = n_days.strftime('%Y-%m-%d %H:%M:%S')
        data={
            'cname': user_info['nickName'],
            'open_id': user_info['openId'],
            'gender': user_info['gender'],
            'languages': user_info['language'],
            'country': user_info['country'],
            'province': user_info['province'],
            'city': user_info['city'],
            'avatar_url': user_info['avatarUrl'],
            'register_ip': register_ip,
            'usr_id':self.subusr_id,
            'ctime':self.getToday(9),
            'up_time': up_time,
            'del_flag':0
        }
        openId=user_info['openId']

        user = self.oUSER.get(self.subusr_id,user_info['openId'])

        if user == {}:
            sqll = """select id from wechat_mall_user 
                            where open_id=%s and usr_id=%s and coalesce(del_flag,0)=0
                            """
            lT, iN = self.db.select(sqll, [openId, self.subusr_id])
            if iN>0:
                return self.jsons({'code': 0, 'msg': 'success'})
            self.db.insert('wechat_mall_user', data)

        sqll ="""select id from wechat_mall_user 
                where open_id=%s and usr_id=%s and coalesce(del_flag,0)=0
                """
        lT, iN = self.db.select(sqll, [openId, self.subusr_id])
        if iN==0:
            return self.jsons({'code': 10000, 'msg': self.error_code[10000]})
        wid = lT[0][0]
        self.oUSER.update(self.subusr_id, wid)
        sql="select coalesce(new_score,0) from shop_set where usr_id=%s"
        l,t=self.db.select(sql,self.subusr_id)
        if t>0:#注册送积分
            new_score=l[0][0]
            if new_score>0:
                sql="update wechat_mall_user set score=coalesce(score,0)+%s where open_id=%s and  usr_id=%s"
                self.db.query(sql,[new_score,openId,self.subusr_id])

        self.oUSER.update(self.subusr_id,wid)
        self.oOPENID.update(wid)
        return self.jsons({'code': 0, 'msg': 'success'})



    def goPartlogin(self):#登录
        code=self.REQUEST.get('code','')

        if code == '' or code == 'None' or code=='undefined':
            return self.jsons({'code': 300, 'data': {'msg': self.error_code[300].format('code')}})

        mall=self.oMALL.get(self.subusr_id)
        if mall=={}:
            return self.jsons({'code': 404, 'msg': '请到店铺设置填写小程序设置'})
        app_id = mall['appid']
        secret = mall['secret']

        api = wx_minapp_login(app_id, secret)
        session_info = api.get_session_info(code=code)
        if session_info.get('errcode'):
            return self.jsons({'code': 602, 'msg': '微信用户信息解密错误请检查appid和secret信息', 'data': session_info.get('errmsg')})
        open_id = session_info['openid']


        user=self.oUSER.get(self.subusr_id,open_id)
        #self.print_log('subusr_id:%s,open_id:%s'%(self.subusr_id,open_id),'%s'%self.oUSER.get(self.subusr_id,open_id))
        if user=={}:
            sqll ="""select id  from wechat_mall_user 
                    where open_id=%s and  usr_id=%s and COALESCE(del_flag,0)=0
                    """
            lT,iN=self.db.select(sqll,[open_id,self.subusr_id])
            if iN==0:
                return self.jsons({'code': 10000, 'msg': self.error_code[10000]})
            wechat_user_id = lT[0][0]
        else:
            wechat_user_id = user['id']
        try:
            ip=self.objHandle.headers["X-Real-IP"]
        except:
            ip = self.objHandle.remote_addr

        sqli="update wechat_mall_user set utime=now(),last_login_ip=%s where  id =%s and usr_id=%s "
        self.db.query(sqli,[ip,wechat_user_id,self.subusr_id])

        token = self.create_token(self.subusr_id, open_id, wechat_user_id)
        self.oUSER.update(self.subusr_id, wechat_user_id)
        return self.jsons({'code':0,'data':{'token': token,'uid':wechat_user_id}})

    def goPartadvertis_banner(self):#分类后的图片广告接口
        ctype = self.RQ('type', '')

        l=self.oSHOP.get(self.subusr_id,'advertis_banner')
        #print(l)
        if len(l)==0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        L = []
        if ctype != '' and ctype != 'None' and ctype!='undefined':

            for i in l:
                itype=i.get('ctype')
                if str(itype)==str(ctype):
                    L.append(i)
            if len(L)==0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            l=L
        return self.jsons({'code': 0, 'data': l,'msg':self.error_code['ok']})


    def goPartbanner_list(self):#图片广告接口
        ctype = self.RQ('type', '')

        l=self.oSHOP.get(self.subusr_id,'banner_list')

        if len(l)==0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        L = []
        if ctype != '' and ctype != 'None' and ctype!='undefined':

            for i in l:
                itype=i.get('ctype')
                if str(itype)==str(ctype):
                    L.append(i)
            if len(L)==0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            l=L
        return self.jsons({'code': 0, 'data': l,'msg':self.error_code['ok']})

    def goParttextarea_list(self):#文字广告
        key=self.RQ('key', '')
        if key == '' or key == 'None' or key=='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('key')})

        # sql="""select id,key,content as value,remark,
        #         to_char(ctime,'YYYY-MM-DD HH:MM')time_add,to_char(utime,'YYYY-MM-DD HH:MM')time_update
        #         from config_set  where usr_id=%s and key=%s and COALESCE(del_flag,0)=0"""
        #
        # l,t=self.db.fetchall(sql,[self.subusr_id,key])
        # if t==0:
        #     return self.jsons({'code': 404,'msg':self.error_code[404]})

        l = self.oSHOP.get(self.subusr_id, 'textarea_list')

        if len(l) == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        L = []
        for i in l:
            if str(i.get('key')) == key:
                L.append(i)
        l = L

        return self.jsons({'code':0,'data':l,'msg':self.error_code['ok']})


    def goPartshopinfo(self):#店铺信息接口
        #https://daxue.qinghuan.app/read/maliapp/maliapi-005
        """
        :return:
        参数名称	参数说明
        shopInfo	店铺信息
            gname	店铺名称
            gpic	店铺Logo图片地址
            gadds	店铺地址
            sname	首页分享标题
            spic	首页分享海报图片地址
            home_type	首页商品推荐类型
            cart_type	购物车页商品推荐类型
        orderInfo	订单信息
            orderfree	订单包邮金额
            orderclose	订单关闭时间
            orderclose_id	订单取消模版ID
            ordersend_id	订单发货模版ID
            ordereputation_id	订单评价模版ID
            ordersuccess_id	订单完成模版ID
        vipInfo	会员信息
            vip_id	会员级别ID
            vip_price	会员级别价格
            vip_name	会员级别名字
            vip_sale	会员级别折扣
        homeGoods	首页商品信息
            指定的商品	同商品列表字段
        cartGoods	购物车页商品信息
            指定的商品	同商品列表字段
        cartText	购物车页文字说明信息
            id	文字说明信息ID
            name	文字说明内容
        searchTag	分类页搜索关键字
            id	关键字ID
            name	关键字内容
        """
        # data = {}
        # sql="""select cname as gname,logo_pic_link as gpic,gadds,
        #                 home_title as sname,home_pic_link as spic,
        #                 (select up_type_str from member where usr_id=%s)vip_type
        #         from shopinfo where usr_id =%s"""
        # shopInfo=self.db.fetch(sql,[self.subusr_id,self.subusr_id])
        #
        #
        # sql="""select use_money as orderfree,close_time as orderclose,cancel_id as orderclose_id,
        #             send_id as ordersend_id,evaluate_id as ordereputation_id,complete_id as ordersuccess_id
        #         from  order_set where usr_id=%s"""
        # orderInfo=self.db.fetch(sql,self.subusr_id)
        #
        # vipInfo=[]
        #
        # sql="select id ,vip_price,up_type,up_type_str,discount  from member where usr_id=%s"
        # k,t=self.db.select(sql,self.subusr_id)
        # if t>0:
        #     vip_id,vip_price,vname,vip_,vip_sale = k[0]
        #     if str(vname)=='1':
        #         vipInfo.append({'vip_id':vip_id,'vip_price':vip_price,'vip_name':'会员','vip_sale':vip_sale})
        #     elif str(vname)=='2':
        #         sql="""select id as vip_id,cname as vip_name,
        #                     up_price as vip_price,level_discount as vip_sale
        #                     from hy_up_level where usr_id =%s"""
        #         vipInfo,t=self.db.fetchall(sql,self.subusr_id)
        # #data = {'shopInfo': shopInfo, 'orderInfo': orderInfo, 'vipInfo': vipInfo}
        # sql="""select id,home_goods,home_goods_str,shop_goods,shop_goods_str,home_goods_id,shop_goods_id,shop_cart_memo,menu_memo from global_config where usr_id=%s"""
        # l,t=self.db.select(sql,self.subusr_id)
        # if t>0:
        #     id,home_goods,home_goods_str,shop_goods,shop_goods_str,home_goods_id,shop_goods_id,shop_cart_memo,menu_memo=l[0]
        #     shopInfo['home_type'] = home_goods_str
        #     shopInfo['cart_type'] = shop_goods_str
        #     shop=shop_cart_memo.split(',')
        #     menu=menu_memo.split(',')
        #
        #     if len(shop)>0:
        #         cartText=[]
        #         for s in shop:
        #             cartText.append({'id': id, 'name': s})
        #         data['cartText'] = cartText
        #     if len(menu)>0:
        #         searchTag=[]
        #         for m in menu:
        #             searchTag.append( {'id': id, 'name': m})
        #         data['searchTag'] = searchTag
        #
        #     if str(home_goods)!='0':
        #         sql="""
        #             select id	--商品ID
        #                 ,name	--商品名称
        #                 ,introduce	--商品简介
        #                 ,recomm as status 	--是否推荐
        #                 ,pic	--商品第一张图片
        #                 ,originalprice as original_price	--商品原价
        #                 ,minprice as mini_price	--商品现价
        #                 ,limited	--限购数量
        #                 ,COALESCE(stores,0) as stores	--商品库存
        #                 ,barcodes	--商品编码
        #                 ,COALESCE(orders,0) as orders	--商品销量
        #                 ,COALESCE(views,0) as views	--商品浏览量
        #                 ,COALESCE(favorite,0) as favorite	--商品收藏量
        #                 ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
        #             from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id in (%s)
        #         """%(self.subusr_id,home_goods_id)
        #         homeGoods,n=self.db.fetchall(sql)
        #         data['homeGoods'] = homeGoods
        #     if str(shop_goods)!='0':
        #         sql = """
        #             select id	--商品ID
        #                 ,name	--商品名称
        #                 ,introduce	--商品简介
        #                 ,recomm as status 	--是否推荐
        #                 ,pic	--商品第一张图片
        #                 ,originalprice as original_price	--商品原价
        #                 ,minprice as mini_price	--商品现价
        #                 ,limited	--限购数量
        #                 ,COALESCE(stores,0) as stores	--商品库存
        #                 ,barcodes	--商品编码
        #                 ,COALESCE(orders,0) as orders	--商品销量
        #                 ,COALESCE(views,0) as views	--商品浏览量
        #                 ,COALESCE(favorite,0) as favorite	--商品收藏量
        #                 ,to_char(ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
        #             from goods_info  where usr_id=%s and COALESCE(del_flag,0)=0 and status=0 and id in (%s)
        #         """%(self.subusr_id, home_goods_id)
        #         cartGoods, n = self.db.fetchall(sql)
        #         data['cartGoods'] = cartGoods
        #
        #
        # data['shopInfo']=shopInfo
        # data['orderInfo']=orderInfo
        # data['vipInfo']= vipInfo
        data=self.oSHOP.get(self.subusr_id,'ShopInfo')


        return self.jsons({'code': 0, 'msg': self.error_code['ok'],'data':data})

    def goPartorder_delivery_list(self):#https://daxue.qinghuan.app/read/maliapp/maliapi-006
        """
        参数名称	参数说明
        id	配送列表ID
        delivery_name	配送方式名称
        delivery_free	是否包邮
        :return:
        """
        token = self.REQUEST.get('token', '')
        if token == '' or token == 'None' or token=='undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] == 1:
            return self.jsons({'code': 901, 'msg': dR['MSG']})

        # sql="select id,cname as delivery_name,is_mail as delivery_free from logistics_way where usr_id=%s"
        # l,n=self.db.fetchall(sql,self.subusr_id)
        # if n==0:
        #     return self.jsons({'code': 700, 'msg': self.error_code[700]})
        l=self.oSHOP.get(self.subusr_id,'order_delivery_list')

        if len(l)==0:
            return self.jsons({'code': 700, 'msg': self.error_code[700]})

        return self.jsons({'code': 0, 'msg': self.error_code['ok'],'data':l})

    def goPartUser_info(self):#用户信息接口
        # https://daxue.qinghuan.app/read/maliapp/maliapi-007
        token = self.REQUEST.get('token', '')
        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] == 1:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id=dR['wechat_user_id']

        # sql="""
        #     select id,cname as name,avatar_url as avatar,city,province,phone,COALESCE(balance,0) as money,COALESCE(score,0)score,
        #         coalesce(hy_flag,0)vip_state,coalesce(usr_level,0) as vip_level,usr_level_str as vip_level_name,to_char(hy_etime,'YYYY-MM-DD')vip_time
        #         from wechat_mall_user where id=%s
        # """
        # data=self.db.fetch(sql,wechat_user_id)
        data = self.oUSER.get(self.subusr_id,wechat_user_id)
        if data=={}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        del_flag = data.get('del_flag','')
        if del_flag=='':
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        if str(del_flag) == '1' :
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({'code': 0, 'msg': self.error_code['ok'],'data':data})



    def goPartshop_category(self):#商品分类接口
        ilevel = self.RQ('level', '')
        ctype = self.RQ('type', '')

        if ilevel == '' or  ilevel == 'None' or ilevel == 'undefined' or  ilevel == 'null':
            ilevel= ''
        if  ctype == '' and ctype == 'None' and ctype == 'undefined' and ctype == 'null':
            ctype=''

        l = self.oSHOP.get(self.subusr_id, 'shop_category')
        if len(l) == 0:
            return self.jsons({'code': 700, 'msg': self.error_code[700]})

        if ilevel == '' and ctype == '':
            return self.jsons({'code':0,'data':l,'msg':self.error_code['ok']})

        if ilevel != ''  and ctype != '':
            L = []
            for i in l:
                if str(ilevel)==str(i.get('ilevel','')) and str(ctype)==str(i.get('ctype','')):
                    L.append(i)
            l = L

        elif ilevel != '' and ctype == '':
            L = []
            for i in l:
                if str(ilevel) == str(i.get('ilevel', '')):
                    L.append(i)
            l = L
        elif ilevel == '' and ctype != '':
            L = []
            for i in l:
                if str(type) == str(i.get('ctype', '')):
                    L.append(i)
            l=L

        return self.jsons({'code':0,'data':l,'msg':self.error_code['ok']})

    def goPartcategory_detail(self):  # 商品分类详情接口(会根据id改变排序)
        id = self.RQ('id', '')
        tid = self.RQ('tid', '')
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if tid == '' or tid == 'None' or tid == 'undefined' or tid == 'null':
            tid = ''
        #########
        if tid == '':


            oCATEGORY=self.oCATEGORY.get(self.subusr_id)
            if len(oCATEGORY)==0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            l=[]
            for i in oCATEGORY:
                pid=i.get('pid','')
                if str(id)==str(pid):
                    l.append(i)
            if len(l)==0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})


        sql = """select c.id,c.cname,c.ctype,c.pid,ca.cname as pid_name,
                    c.pic_icon,c.pic_imgs,c.remark,
                    c.paixu,to_char(c.ctime,'YYYY-MM-DD HH24:MI')time_add 
                from category c 
                left join category ca on ca.id=c.pid
                where COALESCE(c.del_flag,0)=0 and c.usr_id=%s and c.pid=%s and c.id=%s"""
        l, t = self.db.fetchall(sql, [self.subusr_id, id, tid])

        L = l
        sql = """select c.id,c.cname,c.ctype,c.pid,ca.cname as pid_name,
                        c.pic_icon,c.pic_imgs,c.remark,
                        c.paixu,to_char(c.ctime,'YYYY-MM-DD HH24:MI')time_add 
                from category c 
                left join category ca on ca.id=c.pid
                where COALESCE(c.del_flag,0)=0 and c.usr_id=%s and c.pid=%s and c.id!=%s order by c.paixu"""
        ll, tt = self.db.fetchall(sql, [self.subusr_id, id, tid])
        if tt > 0:
            L += ll
        return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})




    def goPartcategory_detail_a(self):  # 商品分类详情接口(不会根据id改变排序)
        id = self.RQ('id', '')
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        sql = """select c.id,c.name,c.type,c.pid,ca.name as pid_name,
                c.pic_icon,c.pic_imgs,c.remark,
                c.paixu,to_char(c.ctime,'YYYY-MM-DD HH24:MI')time_add 
                from category c 
                left join category ca on ca.id=c.pid
                where COALESCE(c.del_flag,0)=0 and c.usr_id=%s and c.pid=%s """
        l, t = self.db.fetchall(sql, [self.subusr_id,id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})


        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})


    def goPartgoods_qrcode(self):
        scene = self.REQUEST.get('scene', '')
        page = self.REQUEST.get('page', '')
        if scene == '' or scene == 'None' or scene == 'undefined' or scene == 'null':
            return self.jsons({'code': 300, 'data': {'msg': self.error_code[300].format('scene')}})
        if page == '' or page == 'None' or page == 'undefined' or page == 'null':
            return self.jsons({'code': 300, 'data': {'msg': self.error_code[300].format('page')}})
        sql = "select url from qrcode where usr_id=%s and scene=%s and page=%s "
        l, t = self.db.select(sql, [self.subusr_id, scene, page])
        if t > 0:
            url = l[0][0]
            return self.jsons({'code': 0, 'data': {'qrimg': url}, 'msg': self.error_code['ok']})

        wxa = self.get_wecthpy()
        if wxa == 0:
            return self.jsons({'code': 10, 'msg': "请到后台的店铺设置--小程序配置填写appid和secret"})
        qrcode = wxa.get_wxa_code_unlimited(scene, page=page)

        timeStamp = time.time()
        md5name = hashlib.md5()
        md5name.update(str(timeStamp).encode('utf-8'))
        filename = md5name.hexdigest() + '.jpg'

        file_content = qrcode.content
        if self.qiniu_ctype == 0:
            url = self.qiniu_upload_file(file_content, filename)
        else:
            url = self.ali_upload_file(file_content, filename)
        # url = self.qiniu_upload_file(file_content, filename)
        if url==None:
            return self.jsons({'code': 404, 'msg':self.error_code[404]})
        url = url.replace('http://', 'https://')
        sql = "insert into qrcode(usr_id,img_name,url,scene,page,ctime)values(%s,%s,%s,%s,%s,now())"
        self.db.query(sql, [self.subusr_id, filename, url, scene, page])
        return self.jsons({'code': 0, 'data': {'qrimg':url},'msg':self.error_code['ok']})

    def goPartshopinfo_shops(self):#商铺列表接口

        l = self.oSHOP.get(self.subusr_id, 'shopinfo_shops')

        if len(l) == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({'code': 0,'data':l, 'msg': self.error_code['ok']})

    def goPartuser_history_list(self):  # 商品浏览记录列表接口
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']


        sqlv=""" select to_char(ctime,'YYYY-MM-DD')s from view_history  
                    where usr_id=%s and wechat_user_id=%s
                    group by s   order by s desc
            """
        lT,iN=self.db.select(sqlv,[self.subusr_id,wechat_user_id])

        if iN==0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        L=[]

        for i in lT:
            sqls = """
            select v.g_id as id 
                ,g.cname	--商品名称
                ,g.introduce	--商品简介
                ,g.recomm as status 	--是否推荐
                ,g.pic	--商品第一张图片
                ,g.originalprice as original_price	--商品原价
                ,g.minprice as mini_price	--商品现价
                ,g.limited	--限购数量
                ,COALESCE(g.stores,0) as stores	--商品库存
                ,g.barcodes	--商品编码
                ,g.weight
                ,COALESCE(g.orders,0) as orders	--商品销量
                ,COALESCE(g.see,0) as views	--商品浏览量
                ,COALESCE(g.favorite,0) as favorite	--商品收藏量
                ,to_char(g.ctime,'YYYY-MM-DD HH24:MI')date_add	--商品添加时间
                ,to_char(v.ctime,'YYYY-MM-DD')date	--浏览日期      
            from view_history  v
            left join goods_info g on g.id=g_id and g.usr_id=v.usr_id and COALESCE(g.del_flag,0)=0 and g.status=0
            where v.usr_id=%s and v.wechat_user_id=%s and to_char(v.ctime,'YYYY-MM-DD')=%s 
            order by v.ctime desc

            """
            lg,gt = self.db.fetchall(sqls, [self.subusr_id, wechat_user_id,i[0]])
            if gt>0:
                L.append({'date': i[0], 'data': lg})
        if len(L)==0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

    def goPartuser_history_add(self):  # 增加商品浏览记录接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        try:
            id = int(id)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
            select id
            from goods_info  
            where usr_id=%s and COALESCE(del_flag,0)=0  and id=%s and status=0
            """
        parm = [self.subusr_id, id]
        l, t = self.db.select(sql, parm)
        if t == 0:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        data = {
            'usr_id': self.subusr_id,
            'wechat_user_id': wechat_user_id,
            'g_id': id,
            'cid':wechat_user_id,
            'ctime':self.getToday(9)
        }
        fvl = """select id from view_history 
                where usr_id=%s and wechat_user_id=%s and g_id=%s 
                and to_char(ctime,'YYYY-MM-DD')=to_char(now(),'YYYY-MM-DD')
                """
        lt, ni = self.db.select(fvl, [self.subusr_id, wechat_user_id, id])
        if ni > 0:
            #data['del_flag']=0
            #data['del_time']=None
            data['uid'] = wechat_user_id
            data['utime'] = self.getToday(9)
            self.db.update('view_history', data, 'id=%s' % lt[0][0])
            return self.jsons({'code': 0, 'msg': '浏览记录增加成功'})

        self.db.insert('view_history', data)
        return self.jsons({'code': 0, 'msg': '浏览记录增加成功'})

    def goPartuser_history_del(self):  # 清空商品浏览记录接口
        token = self.REQUEST.get('token', '')
        date = self.RQ('date', '')
        id = self.RQ('goods_id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if date == '' or date == 'None' or date == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('date')})
        if id != '' and  id != 'None' and  id != 'undefined' and id!='null':

            try:
                id = int(id)
            except:
                return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        fvl = """select g_id from view_history 
                        where usr_id=%s and wechat_user_id=%s
                        and to_char(ctime,'YYYY-MM-DD')=%s
                        """
        lt, ni = self.db.select(fvl, [self.subusr_id, wechat_user_id,date])
        if ni==0:
            return self.jsons({'code': 100, 'msg': '日期参数不正确'})
        if id != '' and  id != 'None' and  id != 'undefined' and id!='null':
            L=[]
            for i in lt:
                L.append(i[0])
            if id not in L:
                return self.jsons({'code': 200, 'msg': '商品ID参数不正确'})


        sqls = "delete from  view_history where usr_id=%s and wechat_user_id=%s and to_char(ctime,'YYYY-MM-DD')=%s"
        parm=[self.subusr_id,wechat_user_id,date]
        if id != '' and id != 'None' and id != 'undefined' and id != 'null':
            sqls+=" and g_id=%s"
            parm.append(id)
        self.db.query(sqls,parm )
        return self.jsons({'code': 0, 'msg': '浏览记录删除成功'})

    def goPartOrder_coupons(self):  # 检索订单可用优惠券列表接口
        token = self.REQUEST.get('token', '')
        goodsJsonStr = self.REQUEST.get('goodsJsonStr', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if goodsJsonStr == '' or goodsJsonStr == 'None' or goodsJsonStr == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goodsJsonStr')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        sql = """
            select id,cname as name,apply_ext_num as money,type_str as type,remark,icons,pics,
            case when to_char(now(),'YYYY-MM-DD')<case when use_time=1 then 
                    to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
            	else to_char(date_end,'YYYY-MM-DD')end and COALESCE(state,0)=0 then 0 
            when COALESCE(state,0)=1 then 1
          when to_char(now(),'YYYY-MM-DD')>case when use_time=1 then 
                    to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
            	else to_char(date_end,'YYYY-MM-DD')end or COALESCE(state,0)=2 then 2
           when COALESCE(state,0)=3 then 3 end state,
                    goods_id,COALESCE(apply_ext_money,0) as max_money,apply_str as money_type,to_char(ctime,'YYYY-MM-DD')data_add,to_char(date_end,'YYYY-MM-DD')date_end 
            from my_coupons where usr_id=%s and wechat_user_id=%s
        and case when to_char(now(),'YYYY-MM-DD')<case when use_time=1 then 
                    to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
            	else to_char(date_end,'YYYY-MM-DD')end and COALESCE(state,0)=0 then 0 
         when COALESCE(state,0)=1 then 1
          when to_char(now(),'YYYY-MM-DD')>case when use_time=1 then 
                    to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
            	else to_char(date_end,'YYYY-MM-DD')end or COALESCE(state,0)=2 then 2
           when COALESCE(state,0)=3 then 3 
            when COALESCE(validday,0)!=0 and date_part('day', to_char(now(),'YYYY-MM-DD')::timestamp - to_char(ctime,'YYYY-MM-DD')::timestamp) < validday then 0 end =0
        """
        lT, iN = self.db.fetchall(sql, [self.subusr_id, wechat_user_id])
        #lT, iN = self.db.fetchall(sql,[1,1])
        if iN == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        goods_json = json.loads(goodsJsonStr)
        good_ids, goods_price = [], 0.0
        for each_goods in goods_json:
            if each_goods['goods_id'] == 'undefined':
                return self.jsons({'code': 300, 'msg': self.error_code[300].format('goodsJsonStr')})
            good_id = each_goods['goods_id']  # 商品id
            good_ids.append(str(good_id))
            sql = "select status,COALESCE(limited,0) from goods_info where id=%s"
            l, t = self.db.select(sql, good_id)
            if t == 0:
                return self.jsons({'code': 700, 'msg': '订单中存在已下架的商品，请重新下单。'})
            if str(l[0][0]) == '1':
                return self.jsons({'code': 700, 'msg': '订单中存在已下架的商品，请重新下单。'})

            good_dict = self.db.fetch(
                "select cname,pic,minprice,COALESCE(stores,0)stores,COALESCE(weight,0)weight,pt_price from goods_info where id=%s",
                good_id)
            amount = int(each_goods['buy_number'])  # 购买数量
            limited=int(l[0][1])
            if limited>0:
                if amount>limited:
                    return self.jsons({'code': 700, 'msg': '订单中存在商品超过限购商品，请重新下单!'})

            property_child_ids = each_goods.get('goods_childs', '')  # 商品规格
            each_goods_total, dr = self.c_count_goods_price(
                good_dict, amount, property_child_ids, good_id
            )
            if dr != 0:
                return self.jsons({'code': 300, 'msg': self.error_code[300].format(goodsJsonStr)})
            goods_price += each_goods_total
        L, D = [], []
        for i in lT:
            max_money=i.get('max_money')
            if goods_price >= float(max_money):
                L.append(i)

        for j in L:
            if j.get('goods_id', '') != '' and j.get('goods_id', '') != '0':
                ids = j.get('goods_id', '').split(',')
                if list(set(ids).intersection(set(good_ids))) != []:
                    D.append(j)
            else:
                D.append(j)

        if len(D) == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({'code': 0, 'json': D, 'msg': self.error_code['ok']})

    def c_count_goods_price(self, goods, amount, property_child_ids, good_id):
        """
        计算商品价格
        :param goods: model('wechat_mall.goods')
        :param amount: int
        :param property_child_ids: string
        :return: price, total, property_str, dR(返回标识)
        """
        property_str, dR = '', 0

        if property_child_ids != '' and property_child_ids != 'null':

            sql = """
            select sc_name,newprice,store_c,ptprice from spec_child_price 
            where usr_id=%s and goods_id=%s and sc_id=%s
            """
            l, t = self.db.select(sql, [self.subusr_id, good_id, property_child_ids[:-1]])
            if t == 0:
                return 0, 2
            property_str, price, store,ptprice = l[0]
            total = price * amount

        else:
            price = goods['minprice']
            total = price * amount

        return total, dR

    def goPartGet_upload(self):#文件上传接口
        file = self.objHandle.files['name']
        filePath = self.RQ('filePath', '')
        timestamp=self.RQ('timestamp', '')
        orderId=self.RQ('orderId', '')
        goodsId = self.RQ('goodsId', '')
        ctype = self.RQ('ctype', '')
        type_D={'0':'申请退款','1':'申请售后','2':'意见反馈','3':'商品评论'}
        ctype_str=type_D.get(ctype,'')

        try:
            other_id=int(orderId)
        except:
            other_id=0
        try:
            goodsid = int(goodsId)
            # goodsid = self.db.fetchcolumn("select good_id from wechat_mall_order_detail where id=%s", [did])
        except:
            goodsid = 0

        url = ''
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[-1].lower()
            timeStamp = time.time()
            md5name = hashlib.md5()
            md5name.update(str(timeStamp).encode('utf-8'))
            filename = md5name.hexdigest() + '.' + file_ext
            file_content = file.read()
            file_size = float(len(file_content)) / 1024
            # url = self.qiniu_upload_file(file_content, filename)
            if self.qiniu_ctype == 0:
                url = self.qiniu_upload_file(file_content, filename)
            else:
                url = self.ali_upload_file(file_content, filename)
            self.Save_pic_table(file_ext, file_size, filename, url, ctype, timestamp, ctype_str, other_id, goodsid)

        # if file.filename.find('.') > 0:
        #     file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
        #
        #     timeStamp = time.time()
        #     md5name = hashlib.md5()
        #     md5name.update(str(timeStamp).encode('utf-8'))
        #     filename = md5name.hexdigest() + '.' + file_ext
        #     file.save(os.path.join(public.PEM_ROOTR, filename))

        return self.jsons({'code':0,'url':url,'msg':self.error_code[404]})

    def get_tx_vides_url(self,a):

        gUrl = 'http://vv.video.qq.com/getinfo?vids=%s&platform=101001&charge=0&otype=json' % a
        heads = {}
        heads[
            'Accept'] = 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8'
        heads[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        videoUrl=''
        try:

            r = requests.get(gUrl, headers=heads)
            r_text=r.text
            #self.print_log('最终返回数据', '%s' %r_text)
            str_json = r_text[:-1].replace('QZOutputJson=', '')
            data_json = json.loads(str_json)
            if data_json.get('vl', '') != '':
                fileName = data_json['vl']['vi'][0]['fn']
                fvkey = data_json['vl']['vi'][0]['fvkey']
                host = data_json['vl']['vi'][0]['ul']['ui'][2]['url']
                videoUrl = host + fileName + '?vkey=' + fvkey
                #self.print_log('videoUrl请求链接', '%s'%videoUrl)

            return videoUrl
        except:
            self.print_log('videoUrl请求出错','')
            return videoUrl


    def check_my_coupons(self,id,wechat_user_id):
        sql = """
                select id,cname,apply_ext_num as money,apply_ext_money as max_money,COALESCE(apply_id,0)
                    from my_coupons where usr_id=%s and wechat_user_id=%s
                
                    and case when to_char(now(),'YYYY-MM-DD')<case when use_time=1 then 
                            to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
                    	else to_char(date_end,'YYYY-MM-DD')end and COALESCE(state,0)=0 then 0 
                 when COALESCE(state,0)=1 then 1
                  when to_char(now(),'YYYY-MM-DD')>case when use_time=1 then 
                            to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
                    	else to_char(date_end,'YYYY-MM-DD')end or COALESCE(state,0)=2 then 2
                   when COALESCE(state,0)=3 then 3 end =0 
                   and  type_id=3 and id=%s
                """
        parm = [self.subusr_id, wechat_user_id,id]
        l,t=self.db.select(sql,parm)
        if t>0:
            return l[0]
        return []








