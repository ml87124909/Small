# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/A001_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

class cA001_dl(cBASE_DL):
    def init_data(self):
        self.GNL=['','店铺名称','店铺简介','店铺logo','店铺地址','添加时间','修改时间'] #列表表头



    #在子类中重新定义         
    def myInit(self):
        self.part = self.GP('part','Localfrm')
        self.tab = self.GP("tab", "1")



    def get_local_data(self):
        """获取 local 表单的数据
        """
        L={}
        sql = ""
        if str(self.tab)=='1':
            sql="""
                select 
                convert_from(decrypt(access_key::bytea, %s, 'aes'),'SQL_ASCII')access_key
                ,convert_from(decrypt(secret_key::bytea, %s, 'aes'),'SQL_ASCII')secret_key
                ,convert_from(decrypt(cname::bytea, %s, 'aes'),'SQL_ASCII')cname
                ,convert_from(decrypt(domain_url::bytea, %s, 'aes'),'SQL_ASCII')domain_url
                ,endpoint
                ,ctype
                from qiniu  where usr_id=%s
            
            """
        elif str(self.tab)=='2':
            sql="""select cname,convert_from(decrypt(gadds::bytea, %s, 'aes'),'SQL_ASCII') as gadds,
                    logo_pic,logo_pic_link,home_title,home_pic,home_pic_link,
                    convert_from(decrypt(phone::bytea, %s, 'aes'),'SQL_ASCII') as phone,times
                    from  shop_set where usr_id=%s """
        elif str(self.tab)=='3':
            sql="""select cname,convert_from(decrypt(address::bytea, %s, 'aes'),'SQL_ASCII') as address,
                    convert_from(decrypt(contact::bytea, %s, 'aes'),'SQL_ASCII') as contact,wd,jd 
                    from  shopconfig where usr_id=%s"""

        elif str(self.tab)=='4':
            sql="""select use_money,close_time,
                cancel_id,send_id,evaluate_id,complete_id,
                 cancel_url,send_url,evaluate_url,complete_url,
                take_day,close_time_pk,appkey,ebusinessid from shop_set where usr_id=%s"""

        elif str(self.tab)=='5':
            sql = """select convert_from(decrypt(appid::bytea, %s, 'aes'),'SQL_ASCII')appid,
                    convert_from(decrypt(secret::bytea, %s, 'aes'),'SQL_ASCII')secret,
                    convert_from(decrypt(mchid::bytea, %s, 'aes'),'SQL_ASCII') as mchid
                    ,convert_from(decrypt(mchkey::bytea, %s, 'aes'),'SQL_ASCII')mchkey,
                    certpem,keypem from mall where usr_id=%s"""

        elif str(self.tab)=='6':
            sql="select vip_price,up_type,discount,vip_sale from shop_set where usr_id=%s"

        elif str(self.tab)=='7':
            sql="""select home_goods,home_goods_id,
                        shop_goods,shop_goods_id,
                        order_goods,order_goods_str,order_goods_id,
                        shop_cart_memo,menu_memo,return_ticket,return_ticket_str 
                    from shop_set where usr_id=%s"""
        elif str(self.tab) == '8':
            sql = """select vip_integral,integral,new_score
                    from  shop_set where usr_id=%s"""
        elif str(self.tab) == '9':
            sql = """select topup,topup_str
                           from shop_set where usr_id=%s"""
        elif str(self.tab) == '10':
            sql = """select appkey,ebusinessid from shop_set where usr_id=%s"""

        if sql!='':
            if str(self.tab) in ('1','5'):
                L= self.db.fetch(sql,[self.md5code,self.md5code,self.md5code,self.md5code,self.usr_id_p])
            elif str(self.tab) =='2':
                L= self.db.fetch(sql,[self.md5code,self.md5code,self.usr_id_p])
            elif str(self.tab)=='3':
                l,t= self.db.fetchall(sql,[self.md5code,self.md5code,self.usr_id_p])
                if t>0:
                    L=l
            else:
                L = self.db.fetch(sql, [self.usr_id_p])
        return L
    
    def local_add_save(self):

        dR={'code':'','MSG':'保存成功','pk':''}
        try:
            self.tab=self.GP('multab','')
            sql = "select id,up_type from shop_set where usr_id=%s"

            if str(self.tab) == '1':

                ctype = self.GP('ctype', '')
                access_key = self.GP('access_key', '')  #
                secret_key = self.GP('secret_key', '')  #
                cname = self.GP('cname', '')  #
                domain_url = self.GP('domain_url', '')
                endpoint = self.GP('endpoint', '')
                sql = "select id from qiniu where usr_id=%s"
                l, t = self.db.select(sql, [self.usr_id_p])

                if ctype!='2':
                    if access_key=='' or secret_key=='' or cname=='' or domain_url=='':
                        dR['code']='0'
                        dR['MSG'] = '请填写相关数值!'
                        return dR
                    if ctype=='1':
                        if endpoint == '':
                            dR['code'] = '0'
                            dR['MSG'] = '请填写endpoint!'
                            return dR
                if ctype=='2':
                    access_key = ''
                    secret_key = ''
                    cname = ''
                    domain_url = ''
                    endpoint = ''
                if t==0:
                    if ctype != '2':
                        sqlq = "update users set qiniu_flag=1 where usr_id = %s"
                        self.db.query(sqlq, [self.usr_id_p])
                    else:
                        dR['code'] = '0'
                        dR['MSG'] = '数据不需要处理!'
                        return dR

                    try:
                        sql='''insert into qiniu(usr_id,cname,access_key,secret_key,domain_url,endpoint,ctype,cid,ctime)
                            values(%s,encrypt(%s,%s,'aes'),encrypt(%s,%s,'aes'),
                            encrypt(%s,%s,'aes'),encrypt(%s,%s,'aes'),%s,%s,%s,now());
                        '''
                        parm=[self.usr_id_p,cname,self.md5code,access_key,self.md5code,secret_key,
                              self.md5code,domain_url,self.md5code,endpoint,ctype,self.usr_id]
                        self.db.query(sql,parm)
                        sqlq = "update users set qiniu_flag=1 where usr_id = %s"
                        self.db.query(sqlq, [self.usr_id_p])
                        self.oQINIU.update(self.usr_id_p)
                        self.use_log('店铺设置--修改七牛设置')
                        dR['code'] = '0'
                        dR['MSG'] = '保存成功!'
                        return dR
                    except:
                        dR['code'] = '1'
                        dR['MSG'] = '新增数据失败，请联系平台管理员'
                        return dR
                try:
                    sql = '''update qiniu set cname=encrypt(%s,%s,'aes'),access_key=encrypt(%s,%s,'aes'),
                            secret_key=encrypt(%s,%s,'aes'),domain_url=encrypt(%s,%s,'aes'),
                            endpoint=%s,ctype=%s,uid=%s,utime=now() where usr_id=%s
                    '''
                    parm = [cname,self.md5code, access_key,self.md5code, secret_key,self.md5code,
                            domain_url,self.md5code, endpoint, ctype, self.usr_id,self.usr_id_p]
                    self.db.query(sql, parm)
                    if ctype != '2':
                        sqlq = "update users set qiniu_flag=1 where usr_id = %s"
                        self.db.query(sqlq, [self.usr_id_p])
                    else:
                        sqlq = "update users set qiniu_flag=0 where usr_id = %s"
                        self.db.query(sqlq, [self.usr_id_p])

                    self.use_log('店铺设置--修改七牛设置')
                    self.oQINIU.update(self.usr_id_p)
                    dR['code'] = '0'
                    dR['MSG'] = '修改保存成功!'
                    return dR
                except:
                    dR['code'] = '1'
                    dR['MSG'] = '更新数据失败，请联系平台管理员!'
                    return dR

            elif str(self.tab)=='2':
                cname=self.GP('cname','')#店铺名称
                logo_pic_link = self.GP('logo_pic_link', '')  # 店铺logo图片链接
                home_title=self.GP('home_title','')#店铺首页分享标题
                home_pic_link = self.GP('home_pic_link', '')  # 店铺首页分享图链接
                phone = self.GP('phone', '')  # 客服电话
                times = self.GP('times', '')  # 客服时间
                gadds=self.GP('gadds','gadds')
                data={
                    'cname':cname,
                    'logo_pic_link':logo_pic_link,
                    'home_title':home_title,
                    'home_pic_link':home_pic_link,
                    'times':times,
                }

                l, t = self.db.select(sql,self.usr_id_p)
                if t == 0:  # insert
                    data['usr_id'] = self.usr_id_p
                    data['cid']=self.usr_id
                    data['ctime']=self.getToday(9)
                    self.db.insert('shop_set', data)
                else:  # update
                    data['uid']=self.usr_id
                    data['utime']=self.getToday(9)
                    self.db.update('shop_set', data, " id = %s " % l[0][0])
                sqlu="update shop_set set gadds=encrypt(%s,%s,'aes'),phone=encrypt(%s,%s,'aes') where usr_id=%s"
                self.db.query(sqlu,[gadds,self.md5code,phone,self.md5code,self.usr_id_p])
                self.use_log('店铺设置--修改店铺信息')

            elif str(self.tab) == '3':
                lid = self.REQUEST.getlist('lid')
                cname = self.REQUEST.getlist('cname')#商铺名称
                address = self.REQUEST.getlist('address')#商铺地址
                contact = self.REQUEST.getlist('contact')#商铺联系方式
                wd = self.REQUEST.getlist('wd')#商铺坐标纬度
                jd = self.REQUEST.getlist('jd')#商铺坐标经度

                if len(cname) > 0:
                    sql = "select id from shopconfig where usr_id=%s;"
                    l, t = self.db.select(sql, self.usr_id_p)
                    if t > 0:
                        for j in l:
                            if str(j[0]) not in lid:
                                self.db.query("delete from  shopconfig where id=%s;", j[0])
                    for i in range(len(cname)):
                        if cname[i] != '':
                            if lid[i] == '':
                                sql = """
                                insert into shopconfig(usr_id,cname,address,contact,wd,jd,cid,ctime)
                                    values(%s,%s,encrypt(%s,%s,'aes'),encrypt(%s,%s,'aes'),%s,%s,%s,now());
                                """
                                L = [self.usr_id_p, cname[i], address[i],self.md5code, contact[i],
                                     self.md5code, wd[i] or None, jd[i] or None, self.usr_id]
                                self.db.query(sql, L)
                            else:
                                sql = """
                                update shopconfig set cname=%s,address=encrypt(%s,%s,'aes'),
                                contact=encrypt(%s,%s,'aes'),wd=%s,jd=%s,uid=%s,utime=now()  where id=%s
                                """
                                L = [cname[i], address[i],self.md5code,
                                     contact[i],self.md5code,wd[i] or None, jd[i] or None, self.usr_id, lid[i]]
                                self.db.query(sql, L)
                else:
                    self.db.query("delete from  shopconfig where usr_id=%s;", self.usr_id_p)
                self.use_log('店铺设置--修改商铺设置')


            elif str(self.tab) == '4':
                use_money = self.GP('use_money')  # 订单包邮金额(元)
                close_time = self.GP('close_time')  # 订单关闭时间(分钟)
                cancel_id = self.GP('cancel_id', '')  # 订单取消通知
                send_id = self.GP('send_id', '')  # 订单发货通知
                evaluate_id = self.GP('evaluate_id', '')  # 订单评价通知
                complete_id = self.GP('complete_id', '')  # 订单完成通知
                take_day = self.GP('take_day', '')  # 订单完成通知
                close_time_pk=self.GP('close_time_pk','')#活动订单关闭时间
                cancel_url = self.REQUEST.get('cancel_url', '')  # 订单取消通知
                send_url = self.REQUEST.get('send_url', '')  # 订单发货通知
                evaluate_url = self.REQUEST.get('evaluate_url', '')  # 订单评价通知
                complete_url = self.REQUEST.get('complete_url', '')  # 订单完成通知

                data = {
                    'use_money': use_money or None,
                    'close_time': close_time or None,
                    'cancel_id': cancel_id,
                    'send_id': send_id,
                    'evaluate_id': evaluate_id,
                    'complete_id': complete_id,
                    'take_day':take_day,
                    'close_time_pk':close_time_pk or None,
                    'cancel_url':cancel_url,
                    'send_url':send_url,
                    'evaluate_url':evaluate_url,
                    'complete_url':complete_url,

                }  #
                l, t = self.db.select(sql, self.usr_id_p)

                if t == 0:  # insert
                    data[ 'usr_id']=self.usr_id_p
                    data['cid'] = self.usr_id
                    data['ctime'] = self.getToday(9)
                    self.db.insert('shop_set', data)
                else:  # update
                    # 如果是插入 就去掉 uid，utime 的处理
                    oid=l[0][0]
                    data['uid'] = self.usr_id
                    data['utime'] = self.getToday(9)
                    self.db.update('shop_set', data, " id = %s " % oid)
                self.save_logistics_way()
                self.use_log('店铺设置--修改订单设置')

            elif str(self.tab) == '5':

                appid = self.GP('appid', '')  # 小程序appid
                secret = self.GP('secret', '')  # 小程序secret
                mchid = self.GP('mchid', '')  # 微信支付商户号
                mchkey = self.GP('mchkey', '')  # 微信支付秘钥
                certpem = self.GP('certpem', '')  # 微信支付证书
                keypem = self.GP('keypem', '')  # 微信支付证书
                if appid!='':
                    lT, iN = self.db.select("select id from mall where appid=%s and usr_id!=%s", [appid,self.usr_id_p])
                    if iN > 0:
                        dR['code'] = '1'
                        dR['MSG'] = '数据库已存在相同的appid！'
                        return dR
                data = {
                    'certpem': certpem,
                    'keypem': keypem,
                }  # mall
                l, t = self.db.select("select id from mall where usr_id=%s", self.usr_id_p)

                if t == 0:  # insert
                    # 如果是更新，就去掉cid，ctime 的处理.
                    data['usr_id'] = self.usr_id_p
                    data['cid'] = self.usr_id
                    data['ctime'] = self.getToday(9)
                    self.db.insert('mall', data)

                else:  # update
                    # 如果是插入 就去掉 uid，utime 的处理
                    data['uid'] = self.usr_id
                    data['utime'] = self.getToday(9)
                    self.db.update('mall', data, " usr_id = %s " %self.usr_id_p)

                sqlu = """
                       update mall set appid=encrypt(%s,%s,'aes'),secret=encrypt(%s,%s,'aes'),
                       mchid=encrypt(%s,%s,'aes'),mchkey=encrypt(%s,%s,'aes')   where usr_id=%s
                       """
                Lu = [appid, self.md5code,secret, self.md5code,mchid, self.md5code,mchkey, self.md5code,self.usr_id_p]
                self.db.query(sqlu, Lu)
                self.oMALL.update(self.usr_id_p)
                self.use_log('店铺设置--修改小程序设置')

            elif str(self.tab) == '6':
                vip_price = self.GP('vip_price', '')  # 年费会员价格
                up_type = self.GP('up_type', '')  # 会员升级方式
                discount = self.GP('discount', '')  # 会员折扣百分比
                vip_sale = self.GP('vip_sale', '')  # 会员每年可省元
                data = {
                    'vip_price': vip_price or None,
                    'up_type': up_type,
                    'discount': discount or None,
                    'vip_sale': vip_sale or None,
                }  #
                l, t = self.db.select(sql, self.usr_id_p)

                if t == 0:  # insert
                    data['usr_id'] = self.usr_id_p
                    data['cid'] = self.usr_id
                    data['ctime'] = self.getToday(9)
                    self.db.insert('shop_set', data)

                else:  # update

                    data['uid'] = self.usr_id
                    data['utime'] = self.getToday(9)
                    self.db.update('shop_set', data, " id = %s " % l[0][0])
                    if str(up_type)!=str(l[0][1]):
                        sqlu="""
                            select id,cname,usr_level_str  from wechat_mall_user where usr_id=%s
                        """
                        U,ui=self.db.select(sqlu,self.usr_id_p)
                        if ui>0:
                            for u in U:
                                sqlc="""insert into wechat_user_change_log(
                                wechat_user_id,name,old_level,new_level,up_type_str,ctime,end_time,up_mode_str,memo,cid,usr_id)values(
                                %s,%s,%s,%s,'系统变更',now(),null,'手动','注:变更会员升级方式',%s,%s)
                                """
                                self.db.query(sqlc,[u[0],u[1],u[2],'无',self.usr_id,self.usr_id_p])

                        sqlstr="""
                            update wechat_mall_user set usr_level=0,usr_level_str='无',hy_flag=0,
                            hy_ctime=null,hy_etime=null where usr_id=%s
                        """
                        self.db.query(sqlstr,self.usr_id_p)


                self.save_hy_up_level()
                self.use_log('店铺设置--修改会员设置')


            elif str(self.tab) == '7':
                home_goods = self.GP('home_goods', '')  # 首页推荐商品设置
                home_goods_id = self.GP('goods_id', '')  # 首页推荐指定商品（多）
                shop_goods = self.GP('shop_goods', '')  # 购物车推荐商品设置
                shop_goods_id = self.GP('goods_ids', '')  # 购物车推荐指定商品（多）
                order_goods = self.GP('order_goods', '')  # 订单页推荐商品设置
                order_goods_id = self.GP('order_goods_id', '')  # 订单页推荐指定商品（多）
                menu_memo = self.GP('menu_memo', '')  # 菜单页面搜索关键词设置（多）
                shop_cart_memo = self.GP('shop_cart_memo', '')  # 购物车页信息设置（多）
                return_ticket = self.GP('return_ticket', '')  # 首页赠送优惠券id
                return_ticket_str = self.GP('return_ticket_str', '')  # 首页赠送优惠券名称
                data = {
                    'home_goods': home_goods or None,
                    'home_goods_id': home_goods_id,
                    'shop_goods': shop_goods or None,
                    'shop_goods_id': shop_goods_id,
                    'order_goods':order_goods,
                    'order_goods_id':order_goods_id,
                    'shop_cart_memo':shop_cart_memo,
                    'menu_memo':menu_memo,
                    'return_ticket':return_ticket or None,
                    'return_ticket_str':return_ticket_str

                }  #
                l, t = self.db.select(sql, self.usr_id_p)

                if t == 0:  # insert
                    data['usr_id'] = self.usr_id_p
                    data['cid'] = self.usr_id
                    data['ctime'] = self.getToday(9)
                    self.db.insert('shop_set', data)

                else:  # update
                    #oid = l[0][0]
                    data['uid'] = self.usr_id
                    data['utime'] = self.getToday(9)
                    self.db.update('shop_set', data, " id = %s " % l[0][0])
                self.use_log('店铺设置--修改全局设置')

            elif str(self.tab) == '8':
                vip_integral = self.GP('vip_integral', '')  # 会员购物返积分比例
                integral = self.GP('integral', '')  # 非会员购物返积分比例
                new_score = self.GP('new_score', '')  # 新用户注册送多少积分
                data = {
                    'vip_integral': vip_integral or None,
                    'integral': integral or None,
                    'new_score': new_score or None,
                }  #
                l, t = self.db.select(sql, self.usr_id_p)

                if t == 0:  # insert
                    data['usr_id'] = self.usr_id_p
                    data['cid'] = self.usr_id
                    data['ctime'] = self.getToday(9)
                    self.db.insert('shop_set', data)
                else:  # update
                    data['uid'] = self.usr_id
                    data['utime'] = self.getToday(9)
                    self.db.update('shop_set', data, " id = %s " % l[0][0])
                self.save_score_set()

                self.use_log('店铺设置--修改积分规则设置')

            elif str(self.tab) == '9':
                topup = self.GP('topup', '')
                topup_str = self.GP('topup_str', '')
                data = {
                    'topup': topup or None,
                    'topup_str': topup_str,

                }
                l, t = self.db.select(sql, self.usr_id_p)
                if t == 0:
                    data['usr_id'] = self.usr_id_p
                    data['cid'] = self.usr_id
                    data['ctime'] = self.getToday(9)
                    self.db.insert('shop_set', data)
                else:
                    data['uid'] = self.usr_id
                    data['utime'] = self.getToday(9)
                    self.db.update('shop_set', data, 'usr_id=%s' % self.usr_id_p)

                self.save_top_set()
                self.use_log('店铺设置--修改充值设置')

            elif str(self.tab) == '10':
                ebusinessid = self.REQUEST.get('ebusinessid', '')  # 快递鸟ID
                appkey = self.REQUEST.get('appkey', '')  # 快递鸟KEY
                data = {
                    'ebusinessid': ebusinessid,
                    'appkey': appkey
                }  #
                l, t = self.db.select(sql, self.usr_id_p)

                if t == 0:  # insert
                    data['usr_id'] = self.usr_id_p
                    data['cid'] = self.usr_id
                    data['ctime'] = self.getToday(9)
                    self.db.insert('shop_set', data)

                else:  # update
                    # 如果是插入 就去掉 uid，utime 的处理

                    data['uid'] = self.usr_id
                    data['utime'] = self.getToday(9)
                    self.db.update('shop_set', data, " usr_id = %s " %self.usr_id_p)
                self.use_log('店铺设置--修改快递鸟设置')
            else:
                pass
            self.oSHOP.update(self.usr_id_p)

            dR['code'] = '0'
        except:
            dR['MSG'] = '保存失败，请重试!'
        return dR


    def save_top_set(self):
        lid = self.REQUEST.getlist('lid')
        add_money = self.REQUEST.getlist('add_money')  # 充值金额
        giving = self.REQUEST.getlist('giving')  # 赠送金额

        if len(add_money) > 0:
            sql = "select id from gifts where usr_id=%s;"
            l, t = self.db.select(sql, self.usr_id_p)
            if t > 0:
                for j in l:
                    if str(j[0]) not in lid:
                        self.db.query("delete from  gifts where id=%s and usr_id=%s;", [j[0],self.usr_id_p])
            for i in range(len(add_money)):
                if add_money[i] != '':
                    if lid[i] == '':
                        sql = """
                                    insert into gifts(usr_id,add_money,giving,cid,ctime)
                                        values(%s,%s,%s,%s,now());
                                    """
                        L = [self.usr_id_p, add_money[i] or None, giving[i] or None, self.usr_id]
                        self.db.query(sql, L)
                    else:
                        sql = """
                                    update gifts set add_money=%s,giving=%s,uid=%s,utime=now()
                                            where id=%s
                                    """
                        L = [add_money[i] or None, giving[i] or None,  self.usr_id, lid[i]]
                        self.db.query(sql, L)
        else:
            self.db.query("delete from  gifts where usr_id=%s;", self.usr_id_p)
        return

    def save_score_set(self):
        lid=self.REQUEST.getlist('lid')
        days = self.REQUEST.getlist('days')
        score = self.REQUEST.getlist('score')

        if len(days)>0:
            sql="select id from score_set where usr_id=%s;"
            l,t=self.db.select(sql,self.usr_id_p)
            if t>0:
                for j in l:
                    if str(j[0]) not in lid:
                        self.db.query("delete from  score_set where id=%s and usr_id=%s;",[j[0],self.usr_id_p])
            for i in range(len(days)):
                if days[i]!='':
                    if lid[i]=='':
                        sql="""
                        insert into score_set(usr_id,days,score,cid,ctime)
                            values(%s,%s,%s,%s,now());
                        """
                        L=[self.usr_id_p,days[i],score[i],self.usr_id]
                        self.db.query(sql,L)
                    else:
                        sql="""
                        update score_set set days=%s,score=%s,uid=%s,utime=now()
                                where id=%s
                        """
                        L=[days[i],score[i],self.usr_id,lid[i]]
                        self.db.query(sql, L)
        else:
            self.db.query("delete from  score_set where usr_id=%s;", self.usr_id_p)
        return


    def save_logistics_way(self):
        lid=self.REQUEST.getlist('lid')
        c_id = self.REQUEST.getlist('c_id')
        cname = self.REQUEST.getlist('cname')
        status = self.REQUEST.getlist('status')
        is_mail = self.REQUEST.getlist('is_mail')
        counts = self.REQUEST.getlist('counts')
        default = self.REQUEST.get('default')
        piece = self.REQUEST.getlist('piece')
        only_money = self.REQUEST.getlist('only_money')
        add_piece = self.REQUEST.getlist('add_piece')
        add_money = self.REQUEST.getlist('add_money')
        if default=='0':
            default=['1','0','0']
        elif default=='1':
            default=['0','1','0']
        elif default=='2':
            default=['0','0','1']
        else:
            default = ['0', '0', '0']
        sql="select id from logistics_way where usr_id=%s;"
        l,t=self.db.select(sql,[self.usr_id_p])

        if t>0:
            for i in range(len(cname)):

                sql = """
                    update logistics_way set c_id=%s,cname=%s,status=%s,is_mail=%s,counts=%s,
                            piece=%s,only_money=%s,add_piece=%s,add_money=%s,uid=%s,is_default=%s,utime=now()
                            where id=%s
                        """
                L = [c_id[i],cname[i], status[i], is_mail[i] or None, counts[i] or None, piece[i] or None,
                     only_money[i] or None,add_piece[i] or None, add_money[i] or None, self.usr_id,default[i] or None, lid[i]]
                self.db.query(sql, L)

            return
        for i in range(len(cname)):
            sql="""
            insert into logistics_way(usr_id,c_id,cname,status,is_mail,counts,piece,only_money,add_piece,add_money,cid,is_default,ctime)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now());
            """
            L=[self.usr_id_p,c_id[i],cname[i],status[i] or None,is_mail[i]  or None,counts[i]  or None,piece[i]  or None,only_money[i]  or None,add_piece[i]  or None,add_money[i]  or None,self.usr_id,default[i] or None]
            self.db.query(sql,L)
        return



    def save_hy_up_level(self):
        lid=self.REQUEST.getlist('lid')
        cname = self.REQUEST.getlist('cname')
        up_price = self.REQUEST.getlist('up_price')
        level_discount = self.REQUEST.getlist('level_discount')

        if len(cname)>0:
            sql="select id from hy_up_level where usr_id=%s;"
            l,t=self.db.select(sql,[self.usr_id_p])
            if t>0:
                for j in l:
                    if str(j[0]) not in lid:
                        self.db.query("delete from  hy_up_level where id=%s and usr_id=%s;",[j[0],self.usr_id_p])
            for i in range(len(cname)):
                if cname[i]!='':
                    if lid[i]=='':
                        sql="""
                        insert into hy_up_level(usr_id,cname,up_price,level_discount,cid,ctime)
                            values(%s,%s,%s,%s,%s,now());
                        """
                        L=[self.usr_id_p,cname[i],up_price[i],level_discount[i],self.usr_id]
                        self.db.query(sql,L)
                    else:
                        sql="""
                        update hy_up_level set cname=%s,up_price=%s,level_discount=%s,uid=%s,utime=now()
                                where id=%s
                        """
                        L=[cname[i],up_price[i],level_discount[i],self.usr_id,lid[i]]
                        self.db.query(sql, L)
        else:
            self.db.query("delete from  hy_up_level where usr_id=%s;", [self.usr_id_p])
        return

    # def save_global_memo(self):
    #     lid = self.REQUEST.getlist('lid')
    #     memo = self.REQUEST.getlist('memo')
    #     if len(memo) > 0:
    #         sql = "select id from global_memo where usr_id=%s;"
    #         l, t = self.db.select(sql, [self.usr_id])
    #         if t > 0:
    #             for j in l:
    #                 if str(j[0]) not in lid:
    #                     self.db.query("delete from  global_memo where id=%s and usr_id=%s;", [j[0],self.usr_id_p])
    #         for i in range(len(memo)):
    #             if memo[i] != '':
    #                 if lid[i] == '':
    #                     sql = """
    #                             insert into global_memo(usr_id,memo,cid,ctime)
    #                                 values(%s,%s,%s,now());
    #                             """
    #                     L = [self.usr_id_p, memo[i],self.usr_id]
    #                     self.db.query(sql, L)
    #                 else:
    #                     sql = """
    #                             update global_memo set memo=%s,uid=%s,utime=now()
    #                                     where id=%s
    #                             """
    #                     L = [memo[i], self.usr_id, lid[i]]
    #                     self.db.query(sql, L)
    #     else:
    #         self.db.query("delete from  global_memo where usr_id=%s ;", [self.usr_id_p])
    #     return


    def get_logistics_way(self):
        L=[]
        sql="""
            select id,c_id,cname,status,is_mail,counts,piece,only_money,add_piece,add_money,is_default 
            from logistics_way where usr_id=%s order by id
        """
        l,n=self.db.fetchall(sql,self.usr_id_p)
        if n>0:
            L=l
        return L

    # def get_global_memo(self):
    #     L=[]
    #     sql=" select id,memo from global_memo where usr_id =%s "
    #     l,n=self.db.fetchall(sql,self.usr_id_p)
    #     if n>0:
    #         L=l
    #     return L
    def get_score_set(self):
        L=[]
        sql="""
            select id,days,score from score_set where usr_id=%s
        """
        l,n=self.db.fetchall(sql,self.usr_id_p)
        if n>0:
            L=l
        return L

    def get_gifts(self):
        sql = "select id,add_money,giving from gifts where usr_id=%s"
        l, t = self.db.fetchall(sql, self.usr_id_p)
        return l
    #
    # def delete_data(self):
    #     pk = self.pk
    #     dR = {'R':'', 'MSG':''}
    #     self.db.query("update shop_set set del_flag=1 where id= %s and usr_id=%s" ,[pk,self.usr_id_p])
    #     return dR