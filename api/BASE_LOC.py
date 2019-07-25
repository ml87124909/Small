# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################


from imp import reload
from config import DEBUG

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import hashlib, time, json, datetime, os, random, requests, traceback
from .pay import WeixinPay
from .helper import md5_constructor as md5
from .wxpay import WxPay, get_nonce_str, dict_to_xml, xml_to_dict
from werkzeug import secure_filename

if DEBUG == '1':
    import api.BASE_TPL
    reload(api.BASE_TPL)

from api.BASE_TPL import cBASE_TPL

class cBASE_LOC(cBASE_TPL):

    def goPartgoods_list(self):  # 商品列表
        """
        参数名称	参数说明	是否必填
        page	获取第几页数据，不传该参数默认第一页	否
        page_size	每页获取多少条数据，不传该参数默认为100	否
        category_id	获取指定分类下的商品	否
        barcode	商品条码	否
        status	是否推荐，0为不推荐，1为推荐	否
        search_key	搜索关键词，会匹配商品标题+商品简介+商品详情	否
        paixu	排序规则：priceUp 商品升序，priceDown 商品倒序，ordersUp 销量升序，ordersDown 销量降序，addedUp 发布时间升序，addedDown 发布时间倒序

        """
        page = self.RQ('page', '')
        page_size = self.RQ('page_size', '')
        category_id = self.RQ('category_id', '')
        barcode = self.RQ('barcode', '')
        status = self.RQ('status', '')
        search_key = self.RQ('search_key', '')
        paixu = self.RQ('paixu', '')
        vip = self.RQ('vip', '')
        token = self.RQ('token', '')
        specInfo = self.RQ('specInfo', '')

        if token == 'null' or token == 'None' or token == 'undefined':
            token = ''
        if page == '' or page == 'None' or page == 'undefined':
            page = 1
        else:
            try:
                page = int(page)
            except:
                page = 1

        if page_size == '' or page_size == 'None' or page_size == 'undefined':
            page_size = 100
        else:
            try:
                page_size = int(page_size)
            except:
                page_size = 100

        l = self.oGOODS.get(self.subusr_id)

        if l == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        List = []
        if vip == '1':
            for i in l:
                discount = str(i.get('discount', ''))
                if discount == '1':
                    List.append(i)

            t = len(List)
            if t == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(List, t, pageNo=page,
                                                                                    select_size=page_size)
            return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

        if category_id != '':

            for i in l:
                ids = i.get('category_ids', '')
                category_ids = ids.split(',')

                if category_id in category_ids:
                    List.append(i)

            t = len(List)
            if t == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(List, t, pageNo=page,
                                                                                    select_size=page_size)
            return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

        if barcode != '':
            for m in l:
                barcodes = str(m.get('barcode', ''))
                if barcode == barcodes:
                    List.append(m)
            t = len(List)
            if t == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(List, t, pageNo=page,
                                                                                    select_size=page_size)
            return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

        if status != '':

            for k in l:
                if status == str(k.get('status', '')):
                    if specInfo!='':
                        sid=k.get('id')
                        datas = self.oGOODS_D.get(self.subusr_id, sid)
                        speci=datas.get('specInfo','')

                        if speci!='':
                            k['specInfo']=speci
                        if token != '':
                            dR = self.check_token(token)
                            if dR['code'] == 0:
                                wechat_user_id = dR['wechat_user_id']
                                k['favstate'] = 0
                                sql = """
                                select s.g_id
                                from favorite  s
                                where s.usr_id=%s and s.wechat_user_id=%s and  COALESCE(s.del_flag,0)=0  and s.g_id=%s     
                                        """
                                parm = [self.subusr_id, wechat_user_id, sid]
                                F, ft = self.db.select(sql, parm)
                                if ft > 0:
                                    k['favstate'] = 1

                    List.append(k)
            t = len(List)
            if t == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(List, t, pageNo=page,
                                                                                    select_size=page_size)
            return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

        if search_key != '':
            sql = "select id from search_key where cname=%s and usr_id=%s"
            lT, iN = self.db.select(sql, [search_key, self.subusr_id])
            if iN > 0:
                sk_id = lT[0][0]
                sql = "update search_key set num=num+1,utime=now() where id=%s and usr_id=%s"
                self.db.query(sql, [sk_id, self.subusr_id])
            else:
                sql = "insert into search_key(usr_id,cname,num,ctime)values(%s,%s,1,now())"
                self.db.query(sql, [self.subusr_id, search_key])

            for m in l:
                name = str(m.get('name', ''))
                introduce = str(m.get('introduce', ''))
                content = str(m.get('content', ''))
                if search_key in name or search_key in introduce or search_key in content:
                    List.append(m)
            t = len(List)
            if t == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(List, t, pageNo=page,
                                                                                    select_size=page_size)
            return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

        t = len(l)
        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(l, t, pageNo=page,
                                                                                select_size=page_size)
        return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

    def goPartgoods_detail(self):  # 获取商品详情接口

        id = self.RQ('id', '')
        token = self.REQUEST.get('token', '')
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if token == '' or token == 'None' or token == 'undefined':
            token = ''

        try:
            id = int(id)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        data = self.oGOODS_D.get(self.subusr_id, id)
        datas = data
        if datas == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        try:

            if token != '':
                dR = self.check_token(token)
                if dR['code'] == 0:

                    wechat_user_id = dR['wechat_user_id']
                    sqlpt = """
                            select p.id,g.pt_price as price,pt_num as number,
                            ok_num as success,to_char(date_add,'YYYY-MM-DD HH24:MI')date_start,
                            to_char(date_end,'YYYY-MM-DD HH24:MI')date_end,kt_type as ptkstat,
                            add_type as ptcstat,
                            case when to_char(date_end,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
                            then 0 else 2 end status
                            from pt_conf p
                            left join goods_info g on g.id=p.goods_id and g.usr_id=p.usr_id and coalesce(g.pt_status,0)=1
                            where p.usr_id=%s and goods_id=%s and coalesce(p.del_flag,0)=0 and coalesce(p.status,0)=0
                            """
                    lT, iN = self.db.fetchall(sqlpt, [self.subusr_id, id])
                    if iN > 0:
                        ptInfo = lT[0]
                        Lvip = datas.get('vipInfo', '')
                        """
                        商品拼团详情的 status 状态分为：
                        0 可以开团（拼团未到期且用户没有未完成的拼团）；
                        1 已经开过团（拼团未到期且用户有正在进行的拼团）；
                        2 不能开团 （拼团已经到期）
                        
                        """

                        sql = """select id from open_pt 
                                where usr_id=%s and wechat_user_id=%s and gid=%s and coalesce(status,0)=1"""
                        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
                        if str(ptInfo['status']) == '0' and t > 0:
                            ptInfo['status'] = 1

                        sqld = """
                            select opid from open_pt_detail o
                            left join open_pt p on p.id=o.opid and p.usr_id=o.usr_id
                            where o.usr_id=%s and o.wechat_user_id=%s and p.gid=%s and  coalesce(o.status,0)=1
                            order by o.title
                        """
                        lT, iN = self.db.select(sqld, [self.subusr_id, wechat_user_id, id])

                        if iN > 0:

                            ptkid = ''
                            j = iN
                            for i in lT:
                                ptkid += str(i[0])
                                j = j - 1
                                if j != 0:
                                    ptkid += ','
                            ptInfo['ptkid'] = ptkid
                        if type(Lvip) == list:
                            ptprice = ptInfo['price']
                            vipInfo = []
                            for v in Lvip:
                                vip_sale = v['vip_sale']
                                v['vip_price'] = round(float(vip_sale * ptprice / 100), 2)
                                vipInfo.append(v)

                            if len(vipInfo) > 0:
                                datas['vipInfo'] = vipInfo
                        datas['pingtuanInfo'] = ptInfo
        except:
            self.print_log('goPartgoods_detail:%s' % id, '%s' % str(traceback.format_exc()))

        self.db.query("update goods_info set views=COALESCE(views,0)+1 where id=%s", id)
        self.oGOODS_D.updatev(self.subusr_id, id)
        self.oGOODS.updatev(self.subusr_id, id)

        return self.jsons({'code': 0, 'data': datas, 'msg': self.error_code['ok']})

    def goPartgoods_reputation(self):  # 商品评价列表接口
        """
        参数名称	参数说明	是否必填
        goods_id	商品ID	是
        page	获取第几页数据，不传该参数默认第一页	否
        page_size	每页获取多少条数据，不传该参数默认为100	否
        返回参数说明
        参数名称	参数说明
        user_name	用户名字
        user_avatar	用户头像
        goods	购买的商品
        goods_reputation	商品评价
        goods_star	商品评分
        goods_ reply	商品评价回复内容
        date_add	发布评价时间
        :return:
        """

        goods_id = self.RQ('goods_id', '')
        page = self.RQ('page', '')
        page_size = self.RQ('page_size', '')
        if goods_id == '' or goods_id == 'None' or goods_id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_id')})

        if page == '' or page == 'None' or page == 'undefined':
            page = 1
        else:
            try:
                page = int(page)
            except:
                page = 1

        if page_size == '' or page_size == 'None' or page_size == 'undefined':
            page_size = 100
        else:
            try:
                page_size = int(page_size)
            except:
                page_size = 100

        sql = """
            select 
                r.usr_name as user_name,r.user_avatar,r.star_id as user_vip,
                r.goods,r.goods_reputation,r.goods_star,r.goods_reply,
                to_char(r.ctime,'YYYY-MM-DD HH24:MI') as date_add,
                (select array_to_json(array_agg(row_to_json(p))) 
                from (select id,pic from images_api 
                where images_api.usr_id=r.usr_id and images_api.goodsid=r.order_detail_id) p)pics
            from reputation_list r
            where r.usr_id=%s and r.goods_id=%s order by r.ctime desc
        """
        l, t = self.db.fetchall(sql, [self.subusr_id, goods_id])

        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        L, iTotal_length, iTotal_Page, pageNo, select_size = self.list_for_grid(l, t, pageNo=page,
                                                                                select_size=page_size)
        return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

    def goPartgoods_price(self):  # 选择规格和尺寸获取商品价格
        """
        :return:
        参数名称	参数说明
        goods_id	商品ID
        goods_original	商品原价
        goods_mini	商品现价
        goods_stores	商品库存
        goods_barcode	商品条码
        goods_childs	商品规格信息
        """
        goods_id = self.RQ('goods_id', '')
        goods_childs = self.REQUEST.get('goods_childs', '')
        if goods_id == '' or goods_id == 'None' or goods_id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_id')})
        if goods_childs == '' or goods_childs == 'None' or goods_childs == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_childs')})
        goods_childs = goods_childs[:-1]
        sql = """select  goods_id,old_price as goods_original,new_price as goods_mini,
                ptprice as goods_pingtuan,
                        store_c as goods_stores,barcode as goods_barcode,sc_id as goods_childs 
                from spec_child_price where goods_id=%s and usr_id=%s and sc_id=%s
            """
        l, t = self.db.fetchall(sql, [goods_id, self.subusr_id, goods_childs])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l[0], 'msg': self.error_code['ok']})

    def goPartCoupons_list(self):  # 优惠券列表接口
        """
        :return:
        参数名称	参数说明
        id	优惠券ID
        state	优惠券状态，1可领取/2已经领取
        name	优惠券名称
        money	优惠券面额或折扣
        type	优惠券类型
        remark	优惠券备注
        icons	优惠券图标
        pics	优惠券海报
        goods_id	适用商品ID
        max_money	满多少可以使用
        money_type	优惠券使用形式
        max_number	每人最大领取数量
        data_add	优惠券添加时间
        """
        token = self.REQUEST.get('token', '')
        type = self.RQ('type', '')
        goods = self.RQ('goods', '')
        id = self.RQ('id', '')
        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
        select c.id,c.cname as name,
            case when c.amount>(select count(m_id) from my_coupons m where m.m_id=c.id and wechat_user_id=%s) then 1 
            else 2 end state, 
            c.apply_ext_num as money,c.type_str as type,c.remark,c.icons,c.pics,total as number,c.remain_total as getnumber,
            c.apply_goods_id as goods_id,c.apply_ext_money as max_money,c.apply_str as money_type,c.amount as max_number,
            to_char(c.ctime,'YYYY-MM-DD')data_add,to_char(dateend,'YYYY-MM-DD')data_end,case when c.type_id=1 then COALESCE(type_ext,'0') else '0' end score,
            round(coalesce(remain_total,0)::numeric/total::numeric,2)*100 as percent 
        from coupons c
        where c.usr_id=%s  and COALESCE(c.datestart,c.ctime)<=now() and now()<=c.dateend and COALESCE(c.del_flag,0)=0 and COALESCE(c.isshow,0)=1
        """
        parm = [wechat_user_id, self.subusr_id]
        if type != '' and type != 'None' and type != 'undefined':
            sql += " and type_id=%s"
            parm.append(type)
        if goods != '' and goods != 'None' and goods != 'undefined':
            sql += " and apply_goods_id like %s"
            parm.append('%%%s%%' % goods)
        if id != '' and id != 'None' and id != 'undefined':
            sql += " and id=%s"
            parm.append(id)
        sql += " order by id "
        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartCoupons_fetch(self):  # 领取优惠券接口
        token = self.REQUEST.get('token', '')
        id = self.REQUEST.get('id', '')  # 优惠券id
        key = self.REQUEST.get('key', '')  # 优惠券口令

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 600, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 900, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        if key == '' or key == 'None' or key == 'undefined':
            if id == '' or id == 'None' or id == 'undefined':
                return self.jsons({'code': 600, 'msg': self.error_code[300].format('id')})

            try:
                id = int(id)
            except:
                return self.jsons({'code': 400, 'msg': self.error_code[400]})

            sql = """
                select to_char(now(),'YYYY-MM-DD'),
                    amount,to_char(dateend,'YYYY-MM-DD'),COALESCE(total,0),
                    cname,remark,type_id,type_str,case when type_id=1 then COALESCE(type_ext,'0') else '0' end type_ext,
                    apply_id,apply_str,apply_ext_num,apply_ext_money,apply_goods_id,
                    use_time,use_time_str,datestart,validday,icons,pics,remain_total
                from coupons 
                where usr_id=%s and COALESCE(del_flag,0)=0 and id=%s
                    """
            parm = [self.subusr_id, id]
            l, n = self.db.select(sql, parm)
            if n == 0:
                return self.jsons({'code': 100, 'msg': '优惠券ID不正确'})
            now_, max_num, dateend, total, cname, remark, type_id, type_str, type_ext = l[0][0:9]
            apply_id, apply_str, apply_ext_num, apply_ext_money, apply_goods_id, use_time, use_time_str = l[0][9:16]
            datestart, validday, icons, pics, remain_total = l[0][16:]
            if now_ > dateend:
                return self.jsons({'code': 301, 'msg': '优惠券已经发完'})
            if int(remain_total) == int(total):
                return self.jsons({'code': 301, 'msg': '优惠券已经发完'})

            sql = "select id from my_coupons where wechat_user_id=%s and usr_id=%s and m_id=%s"
            ll, t = self.db.select(sql, [wechat_user_id, self.subusr_id, id])
            if t >= max_num:
                return self.jsons({'code': 300, 'msg': '已经领过此优惠券'})
            if str(type_id) == '1':
                sql = "select COALESCE(score,0) from wechat_mall_user where usr_id=%s and id=%s"
                score = self.db.fetchcolumn(sql, [self.subusr_id, wechat_user_id])
                if int(type_ext) > int(score):
                    return self.jsons({'code': 302, 'msg': '您的积分不够!'})
                sql = "update wechat_mall_user set score=score-%s where usr_id=%s and id=%s"
                self.db.query(sql, [int(type_ext), self.subusr_id, wechat_user_id])
                self.user_log(wechat_user_id, 'score', '领取积分优惠券,扣%s积分' % type_ext)

            data = {
                'usr_id': self.subusr_id,
                'wechat_user_id': wechat_user_id,
                'm_id': id,
                'cname': cname,
                'type_id': type_id,
                'type_str': type_str,
                'type_ext': type_ext,
                'remark': remark,
                'icons': icons,
                'pics': pics,
                'goods_id': apply_goods_id,
                'datestart': datestart or None,
                'date_end': dateend or None,
                'apply_id': apply_id or None,
                'apply_str': apply_str,
                'apply_ext_num': apply_ext_num or None,
                'apply_ext_money': apply_ext_money or None,
                'use_time': use_time or None,
                'use_time_str': use_time_str,
                'validday': validday or None,
                'cid': self.subusr_id,
                'ctime': self.getToday(9)

            }

            self.db.insert('my_coupons', data)
            self.db.query("update coupons set remain_total=COALESCE(remain_total,0)+1 where id=%s", id)
            self.oUSER.update(self.subusr_id, wechat_user_id)
            return self.jsons({'code': 0, 'msg': '优惠券领取成功'})
        if len(key) < 6:
            return self.jsons({'code': 200, 'msg': '优惠券口令不正确'})
        sql = """
                        select to_char(now(),'YYYY-MM-DD'),
                            amount,to_char(dateend,'YYYY-MM-DD'),COALESCE(total,0),
                            cname,remark,type_id,type_str,type_ext,
                            apply_id,apply_str,apply_ext_num,apply_ext_money,apply_goods_id,
                            use_time,use_time_str,datestart,validday,icons,pics,remain_total,id
                        from coupons 
                        where usr_id=%s and COALESCE(del_flag,0)=0 and type_ext=%s
                            """
        parm = [self.subusr_id, key]
        l, n = self.db.select(sql, parm)
        if n == 0:
            return self.jsons({'code': 200, 'msg': '优惠券口令不正确'})
        now_, max_num, dateend, total, cname, remark, type_id, type_str, type_ext = l[0][0:9]
        apply_id, apply_str, apply_ext_num, apply_ext_money, apply_goods_id, use_time, use_time_str = l[0][9:16]
        datestart, validday, icons, pics, remain_total, id = l[0][16:]
        if now_ > dateend:
            return self.jsons({'code': 301, 'msg': '优惠券已经发完'})
        if int(remain_total) == int(total):
            return self.jsons({'code': 301, 'msg': '优惠券已经发完'})

        sql = "select id from my_coupons where wechat_user_id=%s and usr_id=%s and m_id=%s"
        ll, t = self.db.select(sql, [wechat_user_id, self.subusr_id, id])
        if t == max_num:
            return self.jsons({'code': 300, 'msg': '已经领过此优惠券'})

        data = {
            'usr_id': self.subusr_id,
            'wechat_user_id': wechat_user_id,
            'm_id': id,
            'cname': cname,
            'type_id': type_id,
            'type_str': type_str,
            'type_ext': type_ext,
            'remark': remark,
            'icons': icons,
            'pics': pics,
            'goods_id': apply_goods_id,
            'datestart': datestart or None,
            'date_end': dateend or None,
            'apply_id': apply_id or None,
            'apply_str': apply_str,
            'apply_ext_num': apply_ext_num or None,
            'apply_ext_money': apply_ext_money or None,
            'use_time': use_time or None,
            'use_time_str': use_time_str,
            'validday': validday or None,
            'cid': self.subusr_id,
            'ctime': self.getToday(9)

        }

        self.db.insert('my_coupons', data)
        self.db.query("update coupons set remain_total=COALESCE(remain_total,0)+1 where id=%s", id)
        self.oUSER.update(self.subusr_id, wechat_user_id)
        return self.jsons({'code': 0, 'msg': '优惠券领取成功'})

    def goPartmy_coupons(self):  # 我的优惠券列表接口
        """
        :return:
        返回参数说明
        参数名称	参数说明
        id	优惠券ID
        name	优惠券名字
        type	优惠券类型
        remark	优惠券备注
        icons	优惠券图标
        pics	优惠券海报
        state	优惠券状态
        goods_id	适用商品ID
        data_add	优惠券领取时间
        data_end	优惠券到期时间
        """
        token = self.REQUEST.get('token', '')
        status = self.RQ('status', '')
        check = self.RQ('check', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 600, 'msg': self.error_code[300].format('token')})
        if status == 'null' or status == 'None' or status == 'undefined':
            status=''
        if check == 'null' or check == 'None' or check == 'undefined':
            check=''

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
                    goods_id,apply_ext_money as max_money,apply_str as money_type,to_char(ctime,'YYYY-MM-DD')data_add,
                    case when use_time=1 then 
                    to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
            	else to_char(date_end,'YYYY-MM-DD') end date_end
            
            from my_coupons where usr_id=%s and wechat_user_id=%s
        """
        parm = [self.subusr_id, wechat_user_id]
        if status != '':
            sql += """
        and case when to_char(now(),'YYYY-MM-DD')<case when use_time=1 then 
                    to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
            	else to_char(date_end,'YYYY-MM-DD')end and COALESCE(state,0)=0 then 0 
         when COALESCE(state,0)=1 then 1
          when to_char(now(),'YYYY-MM-DD')>case when use_time=1 then 
                    to_char(to_char(ctime,'YYYY-MM-DD') ::timestamp + (validday || ' day')::interval,'YYYY-MM-DD')
            	else to_char(date_end,'YYYY-MM-DD')end or COALESCE(state,0)=2 then 2
           when COALESCE(state,0)=3 then 3 end =%s
            """
            parm.append(status)

        if check!='':
            sql+=" and type_id=3"
        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartuser_address_list(self):  # 用户地址列表接口
        token = self.REQUEST.get('token', '')
        default = self.RQ('default', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """select id,cname as name,phone,province,city,district,address,code,
                        is_default as default,to_char(ctime,'YYYY-MM-DD HH24:MI')
                from wechat_address
                where COALESCE(del_flag,0)=0 and wechat_user_id=%s and usr_id=%s 
                """
        parm = [wechat_user_id, self.subusr_id]
        if default != '' and default != 'None' and default != 'undefined':
            sql += "and  is_default=%s"
            parm.append(default)
        sql += " order by is_default desc ,id asc "

        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 700, 'msg': self.error_code[700]})
        return self.jsons({"code": 0, "data": l, "msg": "success"})

    def goPartuser_address(self):  # 用户地址详情接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """select id,cname as name,phone,province,city,district,address,code,
                                is_default as default,to_char(ctime,'YYYY-MM-DD HH24:MI')
                        from wechat_address
                        where COALESCE(del_flag,0)=0 and wechat_user_id=%s and usr_id=%s and id=%s
                        order by is_default desc ,id asc
                        """
        parm = [wechat_user_id, self.subusr_id, id]

        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({"code": 0, "data": l[0], "msg": "success"})

    def goPartuser_address_edit(self):  # 新增 / 修改用户地址接口
        token = self.REQUEST.get('token', '')
        name = self.RQ('name', '')
        phone = self.RQ('phone', '')
        province = self.RQ('province', '')
        city = self.RQ('city', '')
        district = self.RQ('district', '')
        address = self.RQ('address', '')
        id = self.RQ('id', '')
        code = self.RQ('code', '')
        default = self.RQ('default', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if name == '' or name == 'None' or name == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('name')})
        if phone == '' or phone == 'None' or phone == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('phone')})
        if province == '' or province == 'None' or province == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('province')})
        if city == '' or city == 'None' or city == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('city')})
        if district == '' or district == 'None' or district == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('district')})
        if address == '' or address == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('address')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        data = {
            "cname": name,
            #"phone": phone,
            "province": province,
            "city": city,
            "district": district,
            #"address": address,
        }
        if id != '' and id != 'None' and id != 'undefined':
            sql = "select id from wechat_address where usr_id=%s and wechat_user_id=%s and id =%s and COALESCE(del_flag,0)=0"
            l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
            if t == 0:
                return self.jsons({'code': 100, 'msg': '地址ID不正确'})
            if code != '' and code != 'None' and code != 'undefined':
                data['code'] = code
            if default != '' and default != 'None' and default != 'undefined':
                data['is_default '] = default
            data['uid'] = wechat_user_id
            data['utime'] = self.getToday(9)
            self.db.update('wechat_address', data, 'id=%s' % id)

            sql = """update wechat_address  set phone=encrypt(%s,%s,'aes'),
                        address=encrypt(%s,%s,'aes') where id =%s"""
            self.db.query(sql, [phone,self.md5code,address,self.md5code, id])

            if str(default) == '1':
                sql = "update wechat_address  set is_default=0 where wechat_user_id =%s and id !=%s"
                self.db.query(sql, [wechat_user_id, id])
            return self.jsons({'code': 0, 'msg': '地址修改成功'})

        if code != '' and code != 'None' and code != 'undefined':
            data['code'] = code
        if default != '' and default != 'None' and default != 'undefined':
            data['is_default '] = default
        data['cid'] = wechat_user_id
        data['ctime'] = self.getToday(9)
        cur_random_no = "%s%s" % (time.time(), random.random())
        data['random_no'] = cur_random_no
        data['wechat_user_id'] = wechat_user_id
        data['usr_id'] = self.subusr_id
        self.db.insert('wechat_address', data)
        l, t = self.db.select('select id from wechat_address where random_no=%s', cur_random_no)
        if t == 0:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})
        sql = """update wechat_address  set phone=encrypt(%s,%s,'aes'),
                                address=encrypt(%s,%s,'aes') where  id =%s"""
        self.db.query(sql, [phone, self.md5code, address, self.md5code, l[0][0]])
        if str(default) == '1':
            sql = "update wechat_address  set is_default=0 where wechat_user_id =%s and id !=%s"
            self.db.query(sql, [wechat_user_id, l[0][0]])
        return self.jsons({'code': 0, 'msg': '地址增加成功'})

    def goPartuser_address_del(self):  # 删除用户地址接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        sql = '''select id from wechat_address 
            where usr_id=%s and  wechat_user_id =%s and id =%s and COALESCE(del_flag,0)=0'''
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if t == 0:
            return self.jsons({'code': 10, 'msg': '地址ID不正确'})
        try:
            sql = """update wechat_address  set del_flag=1,del_time=now() 
                where usr_id=%s and  wechat_user_id =%s and id =%s"""
            self.db.query(sql, [self.subusr_id, wechat_user_id, id])
            return self.jsons({'code': 0, 'msg': '地址删除成功'})
        except:
            return self.jsons({'code': 100, 'msg': '地址ID不正确'})

    def goPartuser_favorite_list(self):  # 收藏商品列表接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('goods_id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id != '' and id != 'None' and id != 'undefined' and id != 'null':

            try:
                id = int(id)
            except:
                return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
            select s.g_id as id,s.g_name as name,s.introduce,
                    s.mini_price,s.original_price,s.pic,
                    case when COALESCE(g.del_flag,0)=1 then 3 else g.status end status,
                    to_char(s.ctime,'YYYY-MM-DD')data_add 
            from favorite  s
            left join goods_info g on g.id=s.g_id
            where s.usr_id=%s and s.wechat_user_id=%s and  COALESCE(s.del_flag,0)=0       
        """
        parm = [self.subusr_id, wechat_user_id]
        if id != '' and id != 'None' and id != 'undefined' and id != 'null':
            sql += " and s.g_id=%s"
            parm.append(id)
        sql += " order by s.id desc"
        l, ni = self.db.fetchall(sql, parm)
        if ni == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartuser_favorite_add(self):  # 添加收藏商品接口
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
        datas = self.oGOODS_D.get(self.subusr_id, id)

        if datas == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        sql = """
            select id
                ,name
                ,introduce
                ,pic
                ,minprice
                ,originalprice
            from goods_info  
            where usr_id=%s and COALESCE(del_flag,0)=0  and id=%s and status=0
            """
        parm = [self.subusr_id, id]
        l, t = self.db.select(sql, parm)
        if t == 0:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goodsid')})
        gid, gname, introduce, pic, minprice, originalprice = l[0]

        data = {
            'usr_id': self.subusr_id,
            'wechat_user_id': wechat_user_id,
            'g_id': gid,
            'g_name': gname,
            'introduce': introduce,
            'mini_price': minprice,
            'original_price': originalprice,
            'pic': pic,
            'cid': wechat_user_id,
            'ctime': self.getToday(9),

        }
        fvl = "select id,del_flag from favorite where usr_id=%s and wechat_user_id=%s and g_id=%s"
        lt, ni = self.db.select(fvl, [self.subusr_id, wechat_user_id, id])
        if ni > 0:
            if str(lt[0][1]) == '0':
                return self.jsons({'code': 405, 'msg': '您已经收藏过了!'})
            data['del_flag'] = 0
            data['del_time'] = None
            data['uid'] = wechat_user_id
            data['utime'] = self.getToday(9)
            self.db.update('favorite', data, 'id=%s' % lt[0][0])

            self.oGOODS_D.updatef(self.subusr_id, id, 1)
            self.oGOODS.updatef(self.subusr_id, id, 1)
            return self.jsons({'code': 0, 'msg': '商品收藏成功'})

        self.db.insert('favorite', data)
        self.oGOODS_D.updatef(self.subusr_id, id, 1)
        self.oGOODS.updatef(self.subusr_id, id, 1)
        return self.jsons({'code': 0, 'msg': '商品收藏成功'})

    def goPartuser_favorite_del(self):  # 删除收藏商品接口
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
        datas = self.oGOODS_D.get(self.subusr_id, id)
        if datas == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        fvl = "select id  from favorite where usr_id=%s and wechat_user_id=%s and g_id=%s and COALESCE(del_flag,0)=0"
        lt, ni = self.db.select(fvl, [self.subusr_id, wechat_user_id, id])
        if ni == 0:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        sqls = "update favorite set del_flag=1,uid=%s,utime=now(),del_time=now() where id=%s"
        self.db.query(sqls, [self.subusr_id, lt[0][0]])
        self.oGOODS_D.updatef(self.subusr_id, id, -1)
        self.oGOODS.updatef(self.subusr_id, id, -1)
        return self.jsons({'code': 0, 'msg': '删除收藏商品成功'})

    def goPartOrder_delivery(self):
        sql = """select c_id as key,cname as value,is_default as default 
                from logistics_way where COALESCE(status,0)=1 and usr_id =%s
        """
        l, t = self.db.fetchall(sql, self.subusr_id)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartuser_money_recharge(self):  # 充值到站内余额接口
        """
        :return:
        参数名称	参数说明
        id	充值订单id
        order_number	充值订单号
        """
        token = self.REQUEST.get('token', '')
        money = self.RQ('money', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if money == '' or money == 'None' or money == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('money')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        shop = self.oSHOP.get(self.subusr_id, 'ShopInfo')
        shopInfo = shop.get('shopInfo')
        if str(shopInfo.get('topup')) == '0':
            return self.jsons({'code': 701, 'msg': self.error_code[701]})

        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]
        order_num = 'F' + danhao[2:] + romcode  # 充值为F
        real_money = float(money)
        give = 0
        sql = "select giving from  gifts where add_money<=%s and usr_id=%s order by add_money desc limit 1 "
        lT, iN = self.db.select(sql, [money, self.subusr_id])
        if iN > 0:
            give = lT[0][0]
            real_money += float(give)

        order_dict = {
            'wechat_user_id': wechat_user_id,
            'cid': wechat_user_id,
            'ctime': self.getToday(9),
            'order_no ': order_num,
            'status': '1',
            'status_str': '待支付',
            'usr_id': self.subusr_id,
            'add_money': money,  # 充值
            'real_money': real_money,  # 实际到帐
            'give': give
        }

        self.db.insert('top_up', order_dict)
        order_id = self.db.fetchcolumn("select id from top_up where order_no=%s", order_num)

        return self.jsons(
            {'code': 0, 'data': {'id': order_id, 'order_number': order_num}, 'msg': self.error_code['ok']})

    def goPartuser_money_paypal(self):  # 用户发起提现请求接口
        """
        :return:
        参数名称	参数说明
        0	提现成功
        100	余额不足
        """
        token = self.REQUEST.get('token', '')
        money = self.RQ('money', '')
        phone = self.RQ('phone', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if money == '' or money == 'None' or money == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('money')})
        if phone == '' or phone == 'None' or phone == 'undefined' or phone == 'null':
            phone = ''

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        shop = self.oSHOP.get(self.subusr_id, 'ShopInfo')
        shopInfo = shop.get('shopInfo')
        if str(shopInfo.get('drawal')) == '0':
            return self.jsons({'code': 702, 'msg': '提现功能已关闭'})

        USER = self.oUSER.get(self.subusr_id, wechat_user_id)

        if USER == {}:
            return self.jsons({'code': 10000, 'msg': self.error_code[10000]})
        if str(USER.get('status', '')) == '1':
            return self.jsons({'code': 701, 'msg': '用户已经被禁用'})

        sql = "select COALESCE(balance,0) from wechat_mall_user where usr_id=%s and id=%s"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        balance = l[0][0]
        if float(money) > float(balance):
            return self.jsons({'code': 100, 'msg': '余额不足'})

        sql = """select round(add_money::numeric ,2) from top_up  
            where usr_id=%s and wechat_user_id=%s order by  ctime desc limit 1 """
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id])
        if t == 0:
            return self.jsons({'code': 703, 'msg': '赠送金额不能提现'})
        add_money = l[0][0]
        if float(money) > float(add_money):
            return self.jsons({'code': 703, 'msg': '赠送金额不能提现'})

        sql = """insert into withdraw_cash(usr_id,wechat_user_id,del_money,status,status_str,phone,cid,ctime)
        values(%s,%s,%s,1,'审核中',%s,%s,now())"""
        self.db.query(sql, [self.subusr_id, wechat_user_id, money, phone, wechat_user_id])

        cash_dict = {
            'wechat_user_id': wechat_user_id,
            'cid': wechat_user_id,
            'ctime': self.getToday(9),
            'usr_id': self.subusr_id,
            'status': '1',
            'status_str': '审核中',
            'change_money': money,  # 充值
            'ctype': '0',
            'ctype_str': '提现',

        }
        self.db.insert('cash_log', cash_dict)
        sql = """update wechat_mall_user set balance=balance-%s where  usr_id=%s and id=%s
                """
        self.db.query(sql, [money, self.subusr_id, wechat_user_id])
        self.user_log(wechat_user_id, 'balance:%s' % balance, '用户提现余额变化')
        self.oUSER.update(self.subusr_id, wechat_user_id)

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartuser_money_paypalinfo(self):  # 用户余额记录接口
        """
        :return:

        """
        token = self.REQUEST.get('token', '')
        type = self.RQ('type', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if type == '' or type == 'None' or type == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('type')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        if type == '0':
            sql = """select to_char(ctime,'YYYY-MM-DD HH24:MI')date,change_money as money,status_str as state ,remark 
                            from cash_log where usr_id=%s and wechat_user_id=%s and ctype=0 order by ctime desc"""
            l, t = self.db.fetchall(sql, [self.subusr_id, wechat_user_id])
        elif type == '1':
            sql = """select to_char(ctime,'YYYY-MM-DD HH24:MI')date,change_money as money,cnumber as number,real_money 
                        from cash_log where usr_id=%s and wechat_user_id=%s and ctype=1 order by ctime desc"""
            l, t = self.db.fetchall(sql, [self.subusr_id, wechat_user_id])
        elif type == '2':
            sql = """select to_char(ctime,'YYYY-MM-DD HH24:MI')date,change_money as money,typeid_str as type ,remark 
                        from cash_log where usr_id=%s and wechat_user_id=%s and ctype=2 order by ctime desc"""
            l, t = self.db.fetchall(sql, [self.subusr_id, wechat_user_id])
        elif type == '3':
            sql = """select to_char(ctime,'YYYY-MM-DD HH24:MI')date,change_money as money,typeid_str as type ,cnumber 
                    from cash_log where usr_id=%s and wechat_user_id=%s and ctype=3 order by ctime desc"""
            l, t = self.db.fetchall(sql, [self.subusr_id, wechat_user_id])
        else:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartorder_details(self):  # 订单详情接口
        """
        :return:
        参数名称	参数说明
        id	订单ID
        ctype	订单类型
        number	订单编号
        goods_price	商品合计金额
        order_total	订单合计金额
        order_yunfei	订单运费金额
        order_coupons	订单优惠券抵扣金额
        order_balance	订单余额抵扣金额
        order_ money	订单实际支付金额
        data_add	订单下单时间
        data_pay	订单支付时间
        pick_type	配送方式
        pick_number	提货码
        #receiver	订单收件人信息
        name	收件人姓名
        phone	收件人电话
        province	省
        city	市
        district	区
        address	街道门牌信息
        code	邮编地址信息
        goods	订单包裹列表
            kuaid	快递单号
            kuaname	快递公司名字
            kuatime	快递发货时间
                id	商品ID
                name	商品名字
                pic	商品图片
                spec	商品规格名称
                price	商品价格
        """

        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        # ORDER_D=self.oORDER_D.get(self.subusr_id,wechat_user_id,int(id))
        # if ORDER_D=={}:
        #     return self.jsons({'code': 404, 'msg': self.error_code[404]})
        # return self.jsons({'code': 0, 'data':ORDER_D, 'msg': self.error_code['ok']})

        sql = """select w.id,w.ctype_str as ctype,w.status,w.order_num as number,
                    w.cname as name,w.phone,w.province,w.city,w.district,w.address,w.code,w.remark,
                    w.goods_price,total as order_total,w.logistics_price as order_yunfei,
                    m.apply_str as coupons_type,coalesce(w.coupon_price,0.0) as order_coupons,
                    w.balance as order_balance,(w.new_total-w.balance) order_money,vip_sale as vip_sales,
                    to_char(w.ctime,'YYYY-MM-DD HH24:MI')data_add,to_char(w.pay_ctime,'YYYY-MM-DD HH24:MI')data_pay,
                    w.kuaid_str as pick_type,w.pick_number,
                    case when COALESCE(w.check_id,0)=0 then '未核验' else '已核验' end pick_status

                from wechat_mall_order w
                left join my_coupons m on m.id=w.couponid and w.usr_id=m.usr_id and m.wechat_user_id=w.wechat_user_id
                where w.id=%s and w.usr_id=%s and w.wechat_user_id=%s and COALESCE(w.del_flag,0)=0
                """
        l, t = self.db.fetchall(sql, [id, self.subusr_id, wechat_user_id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        for i in l:
            order_id = i.get('id', '')
            pick_number = i.get('pick_number', '')
            if order_id != '':
                sql = """
                    select tracking_number as kuaid,shipper_str as kuaname
                        ,coalesce(kuastate,0)kuastate
                    from wechat_mall_order_detail
                    where order_id =%s
                    group by kuaid,kuaname,kuastate order by kuaid
                """
                lT, iN = self.db.fetchall(sql, order_id)

                if iN == 1 and lT[0].get('kuaid', '') == '' and lT[0].get('kuaname', '') == '':
                    i['kuai_state'] = '未发货'
                    sqlk = """
                        select good_id as id,good_name as name,pic,property_str as spec,price,amount as number
                        from wechat_mall_order_detail
                        where order_id =%s
                    """
                    ll, Ni = self.db.fetchall(sqlk, order_id)
                    lT[0]['goods'] = ll

                else:
                    kuai_state = []
                    for j in lT:
                        kuaid = j.get('kuaid', '')
                        kuaname = j.get('kuaname', '')
                        kuai_state.append(kuaid)
                        if kuaid != '' or kuaname!='':
                            sqlk = """
                            select good_id as id,good_name as name,pic,property_str as spec,price,amount as number
                            from wechat_mall_order_detail
                            where order_id =%s and tracking_number=%s and coalesce(shipper_str,'')=%s
                                """
                            ll, Ni = self.db.fetchall(sqlk, [order_id, kuaid, kuaname])
                            j['goods'] = ll

                        else:
                            sqlk = """
                            select good_id as id,good_name as name,pic,property_str as spec,price,amount as number
                            from wechat_mall_order_detail
                            where order_id =%s and coalesce(shipper_id,0)=0 and coalesce(shipper_str,'')=%s
                                """
                            ll, Ni = self.db.fetchall(sqlk, [order_id,kuaname])
                            j['goods'] = ll
                    if '' in kuai_state:
                        i['kuai_state'] = '部分发货'
                    else:
                        i['kuai_state'] = '已发货'
                i['baoguo'] = lT
            if pick_number != '':
                sql = """select s.id,s.cname,s.address,s.contact,s.wd as latitude,s.jd as longitude
                            from  shopconfig s
                            left join wechat_mall_order w on w.usr_id=s.usr_id and w.mendian_id=s.id
                            where s.usr_id=%s and w.id =%s """
                shopinfo = self.db.fetch(sql, [self.subusr_id, order_id])
                i['shopinfo'] = shopinfo
            else:
                i.pop('pick_number')
                i.pop('pick_status')

        return self.jsons({'code': 0, 'data': l[0], 'msg': self.error_code['ok']})

    def goPartorder_evaluate(self):  # 订单评价接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')  # 订单id
        goods_id = self.RQ('goods_id', '')  # 订单明细id
        goods_star = self.RQ('goods_star', '')
        goods_text = self.RQ('goods_text', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if goods_id == '' or goods_id == 'None' or goods_id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_id')})
        if goods_star == '' or goods_star == 'None' or goods_star == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_star')})
        if goods_text == '' or goods_text == 'None' or goods_text == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_text')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        try:
            orderid = int(id)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        try:
            goods_id = int(goods_id)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods_id')})
        user = self.oUSER.get(self.subusr_id, wechat_user_id)

        if user == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        name = user.get('name', '')
        avatar = user.get('avatar', '')
        vip_state = user.get('vip_state', '')
        sql = """select status,price,amount,good_id,good_name from wechat_mall_order_detail  
            where usr_id=%s and order_id=%s and  id=%s """
        l, t = self.db.select(sql, [self.subusr_id, orderid, goods_id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status, price, amount, good_id, good_name = l[0]
        if str(status) != '6':
            return self.jsons({'code': 405, 'msg': self.error_code[405]})
        sql = """select id from reputation_list 
            where usr_id=%s and wechat_mall_usr_id=%s and orderid =%s and order_detail_id=%s"""
        m, n = self.db.select(sql, [self.subusr_id, wechat_user_id, orderid, goods_id])
        if n > 0:
            return self.jsons({'code': 100, 'msg': '已经发表过评价'})

        sql = """
        insert into reputation_list(usr_id,wechat_mall_usr_id,orderid,order_detail_id,goods_id,goods,goods_reputation,goods_star,cid,ctime,usr_name,user_avatar,star_id)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,%s,%s)"""
        self.db.query(sql,
                      [self.subusr_id, wechat_user_id, orderid, goods_id, good_id, good_name, goods_text, goods_star,
                       wechat_user_id, name, avatar, vip_state])

        sql = "update wechat_mall_order_detail  set status=7,status_str='已完成' where usr_id=%s  and id=%s"
        self.db.query(sql, [self.subusr_id, goods_id])
        self.write_order_log(orderid, '评价订单,改变明细订单状态为已完成', '明细id%s' % goods_id)

        ########更新用户总消费金额及会员级别
        sql = "update wechat_mall_user set count_total=coalesce(count_total,0)+%s where id=%s "
        self.db.query(sql, [round(price * amount, 2), wechat_user_id])
        shop = self.oSHOP.get(self.subusr_id, 'ShopInfo')

        shopInfo = shop.get('shopInfo')

        if str(shopInfo.get('ctype')) == '2':

            sql = """
               select h.id,h.cname,w.usr_level from  hy_up_level h 
                left join wechat_mall_user w on w.usr_id=h.usr_id 
                where coalesce(w.count_total,0.0)>= coalesce(h.up_price,0.0) and w.id=%s 
                order by id desc limit 1
            """
            l, t = self.db.select(sql, wechat_user_id)
            if t > 0:
                id, cname, usr_level = l[0]
                if str(id) != str(usr_level):
                    sql = "update wechat_mall_user set usr_level=%s,usr_level_str=%s,hy_flag=1 where id=%s"
                    self.db.query(sql, [id, cname, wechat_user_id])
                    self.user_log(wechat_user_id, 'usr_level', '消费达到升级会员级别')
                    self.oUSER.update(self.subusr_id, wechat_user_id)

        ####################

        sql = "select id from wechat_mall_order_detail  where usr_id=%s  and order_id=%s and status!=7"
        l, t = self.db.select(sql, [self.subusr_id, orderid])

        if t == 0:
            sql = "update wechat_mall_order set status=7,status_str='已完成' where usr_id=%s and wechat_user_id=%s and id=%s"
            self.db.query(sql, [self.subusr_id, wechat_user_id, orderid])
            self.write_order_log(orderid, '评价订单,改变订单状态为已完成', '订单id%s' % orderid)
            sql = "select coalesce(o_type,0),order_num from wechat_mall_order where usr_id=%s and wechat_user_id=%s and id=%s and status=7"
            ll, tt = self.db.select(sql, [self.subusr_id, wechat_user_id, orderid])
            if tt > 0:


                o_type, order_num = ll[0]

                if str(o_type) == '0':
                    sql = "select prepay_id from wechat_mall_payment where COALESCE(status,0)=1 and order_id=%s"
                    lT1, iN1 = self.db.select(sql, orderid)
                    if iN1 > 0:
                        prepay_id = lT1[0][0]
                        try:

                            a = self.order_complete_send(wechat_user_id, prepay_id, order_num, orderid=orderid)
                            if a == 1:
                                return self.jsons({'code': 0, 'msg': '评价成功,推送消息失败'})
                            if str(a.get('errcode', '')) == '0':
                                self.db.query("update wechat_mall_order set o_type=1 where id=%s ", orderid)

                        except:
                            pass

        return self.jsons({'code': 0, 'msg': '评价成功'})

    def goPartorder_cancel(self):  # 订单取消接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        try:
            orderid = int(id)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        sql = """select status,balance,order_num,coalesce(c_type,0),new_total,to_char(ctime,'YYYY-MM-DD HH24:MI') 
        from wechat_mall_order where id=%s and usr_id=%s and  wechat_user_id=%s"""
        l, t = self.db.select(sql, [orderid, self.subusr_id, wechat_user_id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status, balance, order_num, c_type, new_total, ctime = l[0]
        if str(status) != '1':
            return self.jsons({'code': 100, 'msg': '订单不能取消'})

        sql = "update wechat_mall_order set status=-1,status_str='已取消' where id=%s and usr_id=%s and  wechat_user_id=%s;"
        self.db.query(sql, [orderid, self.subusr_id, wechat_user_id])
        sql = "update wechat_mall_order_detail set status=-1,status_str='已取消'where order_id=%s and usr_id=%s ;"
        self.db.query(sql, [orderid, self.subusr_id])
        if balance > 0:
            sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
            self.db.query(sql, [balance, self.subusr_id, wechat_user_id])
            self.user_log(wechat_user_id, 'balance:%s' % balance, '用户取消订单余额变化')
            sql = """
            insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
            values(%s,%s,3,'消费',%s,4,'退回',%s,'取消订单退款',%s,now())
                    """
            self.db.query(sql, [self.subusr_id, wechat_user_id, -balance, order_num, self.subusr_id])
            self.oUSER.update(self.subusr_id, wechat_user_id)
        self.write_order_log(orderid, '取消订单', '订单id:%s' % orderid)
        if str(c_type) == '0':  # 推送取消订单消息
            sql = "select formid from wechat_formid where order_id=%s and coalesce(status,0)=0 order by id"
            lT1, iN1 = self.db.select(sql, id)
            if iN1 > 0:
                prepay_id = lT1[0][0]
                try:
                    a = self.order_cancel_send(wechat_user_id, prepay_id, order_num, total=new_total, ctime=ctime,
                                               orderid=orderid)
                    if a == 1:
                        self.db.query("update wechat_mall_order set c_type=2 where id=%s ", id)
                        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

                    if str(a.get('errcode', '')) == '0':
                        self.db.query("update wechat_mall_order set c_type=1 where id=%s ", orderid)
                        self.db.query("update wechat_formid set status=1,status_str='已使用' where order_id=%s ", orderid)
                except:
                    pass

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartorder_delete(self):  # 订单删除接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        try:
            orderid = int(id)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        sql = "select status from wechat_mall_order where id=%s and usr_id=%s and  wechat_user_id=%s"
        l, t = self.db.select(sql, [orderid, self.subusr_id, wechat_user_id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status = l[0][0]
        if str(status) != '-1':
            return self.jsons({'code': 100, 'msg': '订单不能删除'})

        sql = "update wechat_mall_order set del_flag=1 where id=%s and usr_id=%s and  wechat_user_id=%s;"
        self.db.query(sql, [orderid, self.subusr_id, wechat_user_id])
        sql = "update wechat_mall_order_detail set del_flag=1 where order_id=%s and usr_id=%s ;"
        self.db.query(sql, [orderid, self.subusr_id])
        self.write_order_log(orderid, '删除订单', '订单id%s' % orderid)
        # self.oORDER_D.update(self.subusr_id, wechat_user_id, orderid)

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartOrder_receiving(self):  # 订单确认收货接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')
        kuaid = self.RQ('kuaid', '')
        kuaname = self.RQ('kuaname', '')
        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        if kuaid == 'null' or kuaid == 'None' or kuaid == 'undefined':
            kuaid = ''

        if kuaname == 'null' or kuaname == 'None' or kuaname == 'undefined':
            kuaname = ''

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        try:
            orderid = int(id)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        sql = "select status,order_num,coalesce(e_type,0) from wechat_mall_order where id=%s and usr_id=%s and  wechat_user_id=%s"
        l, t = self.db.select(sql, [orderid, self.subusr_id, wechat_user_id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status, order_num, e_type = l[0]

        if str(status) in ('5', '3'):
            if kuaid == '':
                sql = """update wechat_mall_order set status=6,status_str='待评价' 
                        where id=%s and usr_id=%s and  wechat_user_id=%s;"""
                self.db.query(sql, [orderid, self.subusr_id, wechat_user_id])
                sql = """update wechat_mall_order_detail set status=6,status_str='待评价',kuastate=1
                        where order_id=%s and usr_id=%s """
                self.db.query(sql, [orderid, self.subusr_id])
                self.write_order_log(orderid, '全部确认收货订单', '订单id:%s' % orderid)
                if str(e_type) == '0':  # 推送评价订单消息
                    lT1, iN1 = self.db.select(
                        "select prepay_id from wechat_mall_payment where COALESCE(status,0)=1 and order_id=%s", orderid)
                    if iN1 > 0:
                        prepay_id = lT1[0][0]
                        try:

                            a = self.order_evaluation_send(wechat_user_id, prepay_id, order_num, orderid=orderid)
                            if a == 1:
                                self.db.query("update wechat_mall_order set e_type=2 where id=%s ", id)
                                return self.jsons({'code': 0, 'msg': self.error_code['ok']})
                            if str(a.get('errcode', '')) == '0':
                                self.db.query("update wechat_mall_order set e_type=1 where id=%s ", id)
                        except:
                            pass

            else:
                sql = """update wechat_mall_order_detail set status=6,status_str='待评价',kuastate=1
                        where order_id=%s and usr_id=%s and tracking_number=%s and shipper_str=%s;"""
                self.db.query(sql, [orderid, self.subusr_id, kuaid, kuaname])
                # self.oORDER_D.update(self.subusr_id, wechat_user_id, orderid)
                self.write_order_log(orderid, '部分确认收货订单', '订单id:%s,快递单号:%s,快递名:%s' % (orderid, kuaid, kuaname))
                if str(status) == '5':
                    sql = """
                        select id from wechat_mall_order_detail where status =5 and usr_id=%s and order_id=%s
                    """
                    ll, tt = self.db.select(sql, [self.subusr_id, orderid])
                    if tt == 0:
                        sql = """update wechat_mall_order set status=6,status_str='待评价' 
                                                where id=%s and usr_id=%s and  wechat_user_id=%s;"""
                        self.db.query(sql, [orderid, self.subusr_id, wechat_user_id])
                        self.write_order_log(orderid, '部分确认收货订单', '订单所有货物已收到,修改订单状态为待评价')
                        # self.oORDER_D.update(self.subusr_id, wechat_user_id, orderid)
                        if str(e_type) == '0':  # 推送评价订单消息
                            lT1, iN1 = self.db.select(
                                "select prepay_id from wechat_mall_payment where COALESCE(status,0)=1 and order_id=%s",
                                orderid)
                            if iN1 > 0:
                                prepay_id = lT1[0][0]
                                try:

                                    a = self.order_evaluation_send(wechat_user_id, prepay_id, order_num,
                                                                   orderid=orderid)
                                    if a == 1:
                                        self.db.query("update wechat_mall_order set e_type=2 where id=%s ", id)
                                        return self.jsons({'code': 0, 'msg': self.error_code['ok']})
                                    if str(a.get('errcode', '')) == '0':
                                        self.db.query("update wechat_mall_order set e_type=1 where id=%s ", id)
                                except:
                                    pass

            return self.jsons({'code': 0, 'msg': self.error_code['ok']})

        else:
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})

    def goPartUser_feedback(self):  #
        token = self.REQUEST.get('token', '')
        type = self.RQ('type', '')
        text = self.RQ('text', '')
        phone = self.RQ('phone', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if type == '' or type == 'None' or type == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('type')})
        if text == '' or text == 'None' or text == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('text')})
        if phone == '' or phone == 'None' or phone == 'undefined' or phone == 'null':
            phone = ''

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        cur_random_no = "%s%s" % (time.time(), random.random())
        data = {
            'usr_id': self.subusr_id,
            'wechat_user_id': wechat_user_id,
            'type': type,
            'text': text,
            #'phone': phone,
            'cid': wechat_user_id,
            'ctime': self.getToday(9),
            'status': 0,
            'status_str': '未处理',
            'random_no':cur_random_no,

        }
        self.db.insert('feedback', data)  # feedback
        l, t = self.db.select('select id from feedback where random_no=%s', cur_random_no)
        if t == 0:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})
        sql = """update feedback  set phone=encrypt(%s,%s,'aes')  where  id =%s"""
        self.db.query(sql, [phone, self.md5code, l[0][0]])
        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartScore_rules(self):  # 积分签到规则接口
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = "select id,days as day,score from score_set  where usr_id=%s order by days "

        l, t = self.db.fetchall(sql, self.subusr_id)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartscore_sign(self):  # 每日签到接口
        token = self.REQUEST.get('token', '')
        check = self.RQ('check', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = "select id from signin_log where wechat_user_id =%s and to_char(ctime,'YYYY-MM-DD')=%s and usr_id=%s"
        l, t = self.db.select(sql, [wechat_user_id, self.getToday(6), self.subusr_id])
        sql = "select id,con_amount,to_char(utime,'YYYY-MM-DD') from signin where usr_id=%s and wechat_user_id=%s"
        ll, tt = self.db.select(sql, [self.subusr_id, wechat_user_id])

        if t == 0 and tt == 0:
            if check:
                data = {'status': 1, 'day': 0}
                return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})
            sqls = "insert into signin_log(usr_id,wechat_user_id,cid,ctime)values(%s,%s,%s,now())"
            self.db.query(sqls, [self.subusr_id, wechat_user_id, wechat_user_id])
            sqls = "insert into signin(usr_id,wechat_user_id,con_amount,cid,ctime,utime)values(%s,%s,1,%s,now(),now())"
            self.db.query(sqls, [self.subusr_id, wechat_user_id, wechat_user_id])
            sql = "select score from  score_set where days=1 and usr_id=%s"
            lT, iN = self.db.select(sql, self.subusr_id)
            if iN > 0:
                score = lT[0][0]
                sql = """
                    insert into integral_log(usr_id,wechat_user_id,type,typestr,in_out,inoutstr,amount,cid,ctime)
                    values(%s,%s,2,%s,0,%s,%s,%s,now())
                """
                self.db.query(sql, [self.subusr_id, wechat_user_id, '每日签到', '收入', score or 0, wechat_user_id])

                sql = "update wechat_mall_user set score=COALESCE(score,0)+%s where id=%s"
                self.db.query(sql, [score or 0, wechat_user_id])

                self.oUSER.update(self.subusr_id, wechat_user_id)
            data = {'status': 2, 'day': 1}
            return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})

        elif t == 0 and tt != 0:
            id, counts, utime = ll[0]
            today = datetime.date.today()
            oneday = datetime.timedelta(days=1)
            yesterday = today - oneday
            days = 0

            if check:
                if utime == str(yesterday):
                    days = counts
                data = {'status': 1, 'day': days}
                return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})

            if utime == str(yesterday):
                days = counts + 1
                data = {'status': 2, 'day': days}
                sqls = "insert into signin_log(usr_id,wechat_user_id,cid,ctime)values(%s,%s,%s,now())"
                self.db.query(sqls, [self.subusr_id, wechat_user_id, wechat_user_id])
                sqls = "update signin set con_amount=con_amount+1,uid=%s,utime=now() where usr_id=%s and wechat_user_id=%s"
                self.db.query(sqls, [wechat_user_id, self.subusr_id, wechat_user_id])

                sql = "select score from  score_set where days<=%s and usr_id=%s order by days desc limit 1 "
                lT, iN = self.db.select(sql, [days, self.subusr_id])
                if iN > 0:
                    score = lT[0][0]
                    sql = """
                    insert into integral_log(usr_id,wechat_user_id,type,typestr,in_out,inoutstr,amount,cid,ctime)
                    values(%s,%s,2,%s,0,%s,%s,%s,now())
                                """
                    self.db.query(sql, [self.subusr_id, wechat_user_id, '每日签到', '收入', score or 0, wechat_user_id])

                    sql = "update wechat_mall_user set score=COALESCE(score,0)+%s where id=%s"
                    self.db.query(sql, [score or 0, wechat_user_id])

                    self.oUSER.update(self.subusr_id, wechat_user_id)
                return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})
            data = {'status': 2, 'day': days}
            sqls = "insert into signin_log(usr_id,wechat_user_id,cid,ctime)values(%s,%s,%s,now())"
            self.db.query(sqls, [self.subusr_id, wechat_user_id, wechat_user_id])
            sqls = "update signin set con_amount=1,uid=%s,utime=now() where usr_id=%s and wechat_user_id=%s"
            self.db.query(sqls, [wechat_user_id, self.subusr_id, wechat_user_id])
            sql = "select score from  score_set where days=1 and usr_id=%s"
            lT, iN = self.db.select(sql, self.subusr_id)
            if iN > 0:
                score = lT[0][0]
                sql = """
                    insert into integral_log(usr_id,wechat_user_id,type,typestr,in_out,inoutstr,amount,cid,ctime)
                    values(%s,%s,2,'每日签到',0,'收入',%s,%s,now())
                            """
                self.db.query(sql, [self.subusr_id, wechat_user_id, score, wechat_user_id])

                sql = "update wechat_mall_user set score=COALESCE(score,0)+%s where id=%s"
                self.db.query(sql, [score or 0, wechat_user_id])

                self.oUSER.update(self.subusr_id, wechat_user_id)
            return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})

        else:
            id, counts, utime = ll[0]
            data = {'status': 2, 'day': counts}
            return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})

    def goPartOrder_wuliuinfo(self):
        token = self.REQUEST.get('token', '')
        number = self.RQ('number', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if number == '' or number == 'None' or number == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('number')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        sql = """
            select m.txt1 from mtc_t m 
            left join wechat_mall_order_detail w on w.shipper_id=m.id
            where  m.type='KD' and w.usr_id=%s and w.tracking_number=%s limit 1;
        """
        l, t = self.db.select(sql, [self.subusr_id, number])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        ShipperCode = l[0][0]

        KUAIDI = self.oKUAIDI.get(self.subusr_id)

        if KUAIDI == {}:
            return self.jsons({'code': 404, 'msg': '请到其他设置填写快递鸟设置'})

        try:
            EBusinessID = KUAIDI['ebusinessid']
            apikey = KUAIDI['appkey']

            data1 = {'LogisticCode': number, 'ShipperCode': ShipperCode}
            d1 = json.dumps(data1, sort_keys=True)
            requestdata = self.encrypt(d1, apikey)
            post_data = {'RequestData': d1, 'EBusinessID': EBusinessID, 'RequestType': '1002', 'DataType': '2',
                         'DataSign': requestdata.decode()}
            sort_data = self.sendpost(post_data)
            return self.jsons({'code': 0, 'data': sort_data, 'msg': self.error_code['ok']})
        except:
            return self.jsons({'code': 405, 'msg': self.error_code[405]})

    def goPartUser_vip_paypal(self):  # 用户购买、续费会员接口
        """
        :return:
        参数名称	参数说明
        id	充值订单id
        order_number	充值订单号
        """
        token = self.REQUEST.get('token', '')
        type = self.RQ('type', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if type == '' or type == 'None' or type == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('type')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]
        order_num = 'H' + danhao[2:] + romcode  # 会员H

        sql = "select vip_price,up_type  from member where usr_id=%s"
        k, t = self.db.select(sql, self.subusr_id)
        if t == 0:
            return self.jsons({'code': 701, 'msg': self.error_code[701]})
        vip_price, up_type = k[0]
        if str(up_type) == '2':
            return self.jsons({'code': 701, 'msg': self.error_code[701]})
        real_money = vip_price

        order_dict = {
            'wechat_user_id': wechat_user_id,
            'cid': wechat_user_id,
            'ctime': self.getToday(9),
            'order_no ': order_num,
            'status': '1',
            'status_str': '待支付',
            'usr_id': self.subusr_id,
            'real_money': real_money,  # 购买会员的价格
        }

        self.db.insert(' vip_member', order_dict)
        order_id = self.db.fetchcolumn("select id from  vip_member where order_no=%s", order_num)

        return self.jsons(
            {'code': 0, 'data': {'id': order_id, 'order_number': order_num}, 'msg': self.error_code['ok']})

    def goPartGet_paypal_list(self):  # 充值赠送列表接口

        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        USER = self.oUSER.get(self.subusr_id, wechat_user_id)

        if USER == {}:
            return self.jsons({'code': 10000, 'msg': self.error_code[10000]})
        if str(USER.get('status', '')) == '1':
            return self.jsons({'code': 701, 'msg': self.error_code[701]})
        sql = """select add_money as money,giving as give,round(coalesce(add_money,0)::numeric+giving::numeric,2) 
        from gifts  where usr_id=%s"""
        l, t = self.db.fetchall(sql, self.subusr_id)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartorder_evaluate_list(self):  # 订单评价商列表品接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')
        kid = self.RQ('kid', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        try:
            orderid = int(id)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        sql = """
            select w.id,w.good_name as name,w.property_str as spec,w.pic,
                case when  coalesce(r.id,0)=0 then 0 else 1 end statse,
                r.goods_star ,r.goods_reputation as goods_text,to_char(r.ctime,'YYYY-MM-DD HH24:MI')data_time,
                (select array_to_json(array_agg(row_to_json(p))) 
                from (select id,pic from images_api 
                where images_api.usr_id=r.usr_id and images_api.goodsid=w.id) p)pics
                from wechat_mall_order_detail w
                left join reputation_list r on r.usr_id=w.usr_id and r.wechat_mall_usr_id=%s and r.orderid=w.order_id and r.order_detail_id=w.id
                where w.usr_id=%s and w.order_id=%s
        """
        parm = [wechat_user_id, self.subusr_id, orderid]
        if kid != '':
            sql += "  and w.tracking_number=%s"
            parm.append(kid)
        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartGoods_newday(self):  # 上新商品列表接口
        # token = self.REQUEST.get('token', '')
        # id = self.RQ('id', '')
        # kid = self.RQ('kid', '')
        #
        # if token == '' or token == 'None' or token == 'undefined':
        #     return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        # if id == '' or id == 'None' or id == 'undefined':
        #     return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        #
        #
        # dR = self.check_token(token)
        # if dR['code'] != 0:
        #     return self.jsons({'code': 901, 'msg': dR['MSG']})
        # wechat_user_id = dR['wechat_user_id']
        G = self.oGOODS_G.get(self.subusr_id)

        if G == []:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        goods = self.oGOODS_N.get(self.subusr_id)

        if goods == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        L1 = goods.values()

        List = []
        for i in G:
            L = []
            date = i[0]
            for j in L1:
                date_add = j.get('date_add')
                if date_add == date:
                    L.append(j)
            if len(L) > 0:
                List.append({'date': date, 'goods': L})
        if len(List) == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': List, 'msg': self.error_code['ok']})

    def goPartOrder_service_refund(self):  # 订单申请退款接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')
        reason = self.REQUEST.get('reason', '')
        money = self.RQ('money', '')
        timestamp = self.RQ('timestamp', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if reason == '' or reason == 'None' or reason == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('reason')})
        if money == '' or money == 'None' or money == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('money')})
        if timestamp == '' or timestamp == 'None' or timestamp == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('timestamp')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        user = self.oUSER.get(self.subusr_id, wechat_user_id)

        if user == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        w_name = user['name']
        avatar = user['avatar']

        sql = "select new_total,status,order_num from wechat_mall_order where usr_id=%s and wechat_user_id=%s and id=%s"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        new_total, status, order_num = l[0]

        if str(status) != '4' and str(status) != '2' and str(status) != '97':
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})

        if float(new_total) < float(money):
            return self.jsons({'code': 101, 'msg': '申请金额超出订单金额'})

        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]
        r_num = 'R' + danhao[2:] + romcode
        data_r = {
            'usr_id': self.subusr_id,
            'wechat_user_id': wechat_user_id,
            'w_name': w_name,
            'avatar': avatar,
            'r_num': r_num,
            'order_id': id,
            'order_num': order_num,
            'status': 99,
            'status_str': '退款处理中',
            'r_money': money,
            'order_money': new_total,
            'reason': reason,
            'cid': wechat_user_id,
            'ctime': self.getToday(9),
            'timestamp': timestamp
        }
        self.db.insert('refund_money', data_r)
        sql = "update wechat_mall_order set status=99,status_str='退款处理中' where usr_id=%s and wechat_user_id=%s and id=%s"
        self.db.query(sql, [self.subusr_id, wechat_user_id, id])
        sql = "update wechat_mall_order_detail set status=99,status_str='退款处理中' where usr_id=%s  and order_id=%s"
        self.db.query(sql, [self.subusr_id, id])
        self.write_order_log(id, 'status,status_str', 'status=99,status_str=退款处理中', '用户提交退款,更新订单表,订单明细表状态')

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartOrder_service_refund_cancel(self):  # 撤销退款申请接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = "select order_id,status from refund_money where usr_id=%s and wechat_user_id=%s and id =%s"
        ll, tt = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if tt == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        order_id, status = ll[0]
        if str(status) != '99':
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})
        sql = "select kuaid from wechat_mall_order where usr_id=%s and wechat_user_id=%s and id=%s and status=99"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, order_id])
        if t == 0:
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})
        kuaid = l[0][0]
        if str(kuaid) == '0':
            sql = "update wechat_mall_order set status=2,status_str='待发货' where usr_id=%s and wechat_user_id=%s and id=%s"
            self.db.query(sql, [self.subusr_id, wechat_user_id, order_id])
            sql = "update wechat_mall_order_detail set status=2,status_str='待发货' where usr_id=%s  and order_id=%s"
            self.db.query(sql, [self.subusr_id, order_id])
            self.write_order_log(id, 'status,status_str', 'status=2,status_str=待发货', '用户撤消退款,更新订单表,订单明细表状态')
        if str(kuaid) == '1':
            sql = "update wechat_mall_order set status=4,status_str='待自提' where usr_id=%s and wechat_user_id=%s and id=%s"
            self.db.query(sql, [self.subusr_id, wechat_user_id, order_id])
            sql = "update wechat_mall_order_detail set status=4,status_str='待自提' where usr_id=%s  and order_id=%s"
            self.db.query(sql, [self.subusr_id, order_id])
            self.write_order_log(id, 'status,status_str', 'status=4,status_str=待自提', '用户撤消退款,更新订单表,订单明细表状态')
        self.db.query("update refund_money set status=-1,status_str='已取消' where id=%s", id)

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartOrder_service_refund_delete(self):  # 删除退款申请接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = "select status from refund_money where usr_id=%s and wechat_user_id=%s and id=%s"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status = l[0][0]
        if str(status) != '-1' and str(status) != '97':
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})
        self.db.query("update refund_money set del_flag=1 where id=%s", id)
        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartOrder_service_refund_recovery(self):  # 恢复并删除退款订单状态接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = "select status,order_id from refund_money where usr_id=%s and wechat_user_id=%s and id=%s"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status, order_id = l[0]
        if str(status) != '97':
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})

        sql = "select kuaid from wechat_mall_order where usr_id=%s and wechat_user_id=%s and id=%s and status=97"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, order_id])
        if t == 0:
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})
        kuaid = l[0][0]
        if str(kuaid) == '0':
            sql = "update wechat_mall_order set status=2,status_str='待发货' where usr_id=%s and wechat_user_id=%s and id=%s"
            self.db.query(sql, [self.subusr_id, wechat_user_id, order_id])
            sql = "update wechat_mall_order_detail set status=2,status_str='待发货' where usr_id=%s  and order_id=%s"
            self.db.query(sql, [self.subusr_id, order_id])
            self.write_order_log(id, 'status,status_str', 'status=2,status_str=待发货', '用户恢复订单状态,更新订单表,订单明细表状态')
        if str(kuaid) == '1':
            sql = "update wechat_mall_order set status=4,status_str='待自提' where usr_id=%s and wechat_user_id=%s and id=%s"
            self.db.query(sql, [self.subusr_id, wechat_user_id, order_id])
            sql = "update wechat_mall_order_detail set status=4,status_str='待自提' where usr_id=%s  and order_id=%s"
            self.db.query(sql, [self.subusr_id, order_id])
            self.write_order_log(id, 'status,status_str', 'status=4,status_str=待自提', '用户恢复订单状态,更新订单表,订单明细表状态')

        self.db.query("update refund_money set del_flag=1 where id=%s", id)

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartOrder_service_exchange(self):  # 订单申请售后接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')
        ctype = self.RQ('type', '')
        reason = self.REQUEST.get('reason', '')
        money = self.RQ('money', '')
        timestamp = self.RQ('timestamp', '')
        goodsJsonStr = self.REQUEST.get('goodsJsonStr', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if ctype == '' or ctype == 'None' or ctype == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('type')})
        if reason == '' or reason == 'None' or reason == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('reason')})
        if goodsJsonStr == 'null' or goodsJsonStr == 'None' or goodsJsonStr == 'undefined' and goodsJsonStr == '':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goodsJsonStr')})

        if timestamp == 'null' or timestamp == 'None' or timestamp == 'undefined' and timestamp == '':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('timestamp')})

        if money == 'null' or money == 'None' or money == 'undefined':
            money = ''

        if ctype != '0' and money == '':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('money')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        user = self.oUSER.get(self.subusr_id, wechat_user_id)

        if user == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        w_name = user['name']
        avatar = user['avatar']

        type_D = {'0': '退换货', '1': '仅退款', '2': '退货退款'}
        ctype_str = type_D.get(ctype, '')
        try:
            goods_json = json.loads(goodsJsonStr)
        except:
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goodsJsonStr')})
        goods_list = []
        money_all = 0
        for each_goods in goods_json:
            gid = each_goods['id']
            number = each_goods['number']
            sql = """select status,status_str,amount,good_id,good_name,pic,property_str,price from wechat_mall_order_detail where usr_id=%s and cid=%s and id=%s """
            l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, gid])
            if t == 0:
                return self.jsons({'code': 404, 'msg': self.error_code[404]})
            status, status_str, amount, good_id, good_name, pic, property_str, price = l[0]
            if str(status) not in ('5', '6', '7', '87'):
                return self.jsons({'code': 100, 'data': {'id': gid, 'name': good_name}, 'msg': '订单状态不正确'})
            if int(number) > int(amount):
                return self.jsons({'code': 101, 'data': {'id': gid, 'name': good_name}, 'msg': '申请售后数量大于购买数量'})
            lT, iN = self.db.select('select e_amount from order_exchange_detail where o_gid=%s', gid)
            old_all = 0
            if iN > 0:
                old_e_amount = lT[0][0]
                old_all = int(old_e_amount) + int(number)
                if old_all > int(amount):
                    return self.jsons({'code': 101, 'data': {'id': gid, 'name': good_name}, 'msg': '申请售后数量大于购买数量'})
            money_all += int(number) * float(price)
            g_dict = {'old_status': status, 'old_status_str': status_str, 'e_amount': int(number),
                      'all_amount': int(amount), 'good_id': good_id, 'good_name': good_name,
                      'pic': pic, 'spec': property_str, 'usr_id': self.subusr_id, 'old_all': old_all, 'price': price,
                      'wechat_user_id': wechat_user_id, 'cid': self.subusr_id, 'o_gid': gid}
            goods_list.append(g_dict)
        if money != '' and money_all > 0:
            if float(money) > money_all:
                return self.jsons({'code': 102, 'msg': '申请金额超出订单金额'})

        sql = "select new_total,order_num from wechat_mall_order where usr_id=%s and wechat_user_id=%s and id=%s "
        ll, tt = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        new_total, order_num = ll[0]
        if tt == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        ctime = self.getToday(9)
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]
        e_num = 'E' + danhao[2:] + romcode
        random_no = "%s%s" % (timeStamp, random.random())
        data_r = {
            'usr_id': self.subusr_id,
            'wechat_user_id': wechat_user_id,
            'w_name': w_name,
            'avatar': avatar,
            'e_num': e_num,
            'order_id': id,
            'order_num': order_num,
            'ctype': ctype,
            'ctype_str': ctype_str,
            'status': 89,
            'status_str': '售后处理中',
            'r_money': money or None,
            'order_money': new_total,
            'reason': reason,
            'random_no': random_no,
            'cid': wechat_user_id,
            'ctime': ctime,
            'timestamp': timestamp
        }
        self.db.insert('order_exchange', data_r)
        pkid = self.db.fetchcolumn("select id from order_exchange where random_no=%s", random_no)
        for good_dict in goods_list:
            gid = good_dict['o_gid']
            good_dict['e_id'] = pkid
            good_dict['e_num'] = e_num
            good_dict['ctime'] = ctime
            all_amount = good_dict['all_amount']
            e_amount = good_dict['e_amount']
            old_all = good_dict['old_all']
            good_dict.pop('old_all')
            self.db.insert('order_exchange_detail', good_dict)
            if all_amount == e_amount:
                sql = "update wechat_mall_order_detail set status=89,status_str='售后处理中',e_status=1 where usr_id=%s and id=%s"
                self.db.query(sql, [self.subusr_id, gid])
                self.write_order_log(gid, 'status,status_str', 'status=89,status_str=退款处理中', '用户提交售后,订单明细表状态')
            else:
                if old_all == all_amount:
                    sql = "update wechat_mall_order_detail set status=89,status_str='售后处理中',e_status=1 where usr_id=%s and id=%s"
                    self.db.query(sql, [self.subusr_id, gid])
                    self.write_order_log(gid, 'status,status_str', 'status=89,status_str=退款处理中', '用户提交售后,订单明细表状态')
                else:
                    self.write_order_log(gid, '状态不变', '总数:%s,提交数:%s' % (all_amount, e_amount), '用户提交部分数量售后,订单状态不需改变')

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartOrder_service_exchange_cancel(self):  # 撤销售后申请接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = "select status from order_exchange where usr_id=%s and wechat_user_id=%s and id=%s"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status = l[0][0]
        if str(status) != '89':
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})

        sql = "select o_gid,old_status,old_status_str from order_exchange_detail where usr_id=%s and wechat_user_id=%s and e_id=%s"
        ll, tt = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if tt == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        for i in ll:
            o_gid, old_status, old_status_str = i
            sql = "update wechat_mall_order_detail set status=%s,status_str=%s where usr_id=%s  and id=%s"
            self.db.query(sql, [old_status, old_status_str, self.subusr_id, o_gid])
            self.write_order_log(o_gid, 'status,status_str', 'status=%s,status_str=%s' % (old_status, old_status_str),
                                 '用户撤消售后,更新订单明细表状态')

        self.db.query("update order_exchange set status=-1,status_str='已取消' where id=%s", id)

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartOrder_service_exchange_list(self):  # 订单申请售后商品列表接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """select w.id,w.good_name as name,w.property_str as spec,w.pic,
        (w.amount-coalesce((select sum(e_amount) from order_exchange_detail where o_gid =w.id group by o_gid),0))number,
            w.price,coalesce(w.e_status,0)e_status 
            from wechat_mall_order_detail  w
            where coalesce(del_flag,0)=0 and w.usr_id=%s  and w.cid=%s and w.order_id=%s """
        l, t = self.db.fetchall(sql, [self.subusr_id, wechat_user_id, id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartOrder_service_refund_list(self):  # 退款订单列表接口
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """select order_id,id as refund_id,r_num as refund_number,
                    to_char(ctime,'YYYY-MM-DD HH24:MI')date,r_money as money,reason,status,
                (select array_to_json(array_agg(row_to_json(p))) from (select i.other_id as order_id,i.id,i.pic
  				from images_api i where i."timestamp"= r."timestamp") p)pics,
  				not_memo as reason_re,order_money, 
            (select array_to_json(array_agg(row_to_json(t)))from (select good_id as id,good_name as name,
            property_str as spec,pic,amount as number,round(price::numeric,2)mini_price 
            from wechat_mall_order_detail  w where w.order_id=r.order_id)t )order_goods
            from refund_money r where coalesce(r.del_flag,0)=0 and usr_id=%s and r.wechat_user_id=%s
            order by r.ctime desc 
            """
        l, t = self.db.fetchall(sql, [self.subusr_id, wechat_user_id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartOrder_service_exchange_order_list(self):  # 售后订单列表接口
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """select order_id,id as refund_id,e_num as change_number,
                    to_char(ctime,'YYYY-MM-DD HH24:MI')date,ctype as type,r_money as money,kuaname as kuainame,kd_number as kuaicode,reason,status,
                (select array_to_json(array_agg(row_to_json(p))) from (select i.other_id as order_id,i.id,i.pic
                from images_api i where i."timestamp"= r."timestamp") p)pics,
                not_memo as reason_re,order_money, 
            (select array_to_json(array_agg(row_to_json(t)))from (select good_id as id,good_name as name,
            spec,pic,e_amount as number,round(coalesce(price,0)::numeric,2)mini_price 
            from order_exchange_detail  w where w.e_id=r.id)t )order_goods
            from order_exchange r where coalesce(r.del_flag,0)=0 and usr_id=%s and wechat_user_id=%s
            order by r.ctime desc """
        l, t = self.db.fetchall(sql, [self.subusr_id, wechat_user_id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({'code': 0, 'data': l, 'msg': self.error_code['ok']})

    def goPartOrder_service_exchange_addinfo(self):  # 补充售后信息接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')
        kuaname = self.RQ('kuaname', '')
        kuanumber = self.RQ('kuanumber', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})
        if kuaname == '' or kuaname == 'None' or kuaname == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('kuaname')})
        if kuanumber == '' or kuanumber == 'None' or kuanumber == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('kuanumber')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = "select status from order_exchange where usr_id=%s and wechat_user_id=%s and id=%s"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status = l[0][0]
        if str(status) != '86':
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})

        sql = "select o_gid from order_exchange_detail where usr_id=%s and wechat_user_id=%s and e_id=%s"
        ll, tt = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if tt == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        for i in ll:
            o_gid = i[0]
            sql = "update wechat_mall_order_detail set status=85,status_str='售后待确认信息' where usr_id=%s  and id=%s"
            self.db.query(sql, [self.subusr_id, o_gid])
            self.write_order_log(o_gid, 'status,status_str', 'status=85,status_str=售后待确认信息', '用户补充信息,更新订单明细表状态')
        sql = "update order_exchange set status=85,status_str='售后待确认信息',kd_number=%s,kuaname=%s where id=%s"
        self.db.query(sql, [kuanumber, kuaname, id])

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartOrder_service_exchange_delete(self):  # 删除售后申请接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = "select status from order_exchange where usr_id=%s and wechat_user_id=%s and id=%s"
        l, t = self.db.select(sql, [self.subusr_id, wechat_user_id, id])
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        status = l[0][0]
        if str(status) != '87' and str(status) != '-1':
            return self.jsons({'code': 100, 'msg': '订单状态不正确'})

        self.db.query("update order_exchange set del_flag=1 where id=%s", id)

        return self.jsons({'code': 0, 'msg': self.error_code['ok']})

    def goPartGoods_share(self):  # 商品分享返现接口
        token = self.REQUEST.get('token', '')
        user = self.RQ('user', '')
        goods = self.RQ('goods', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        if user == '' or user == 'None' or user == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('user')})
        if goods == '' or goods == 'None' or goods == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        if str(user) == str(wechat_user_id):
            return self.jsons({'code': 103, 'msg': '同一用户不能获得返现'})
        good_D = self.oGOODS_D.get(self.subusr_id, int(goods))

        if good_D == {}:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        shareInfo = good_D['shareInfo']
        basicInfo = good_D['basicInfo']
        share_type = shareInfo['share_type']
        share_time = shareInfo['share_time']
        share_number = shareInfo['share_number']

        gname = basicInfo['name']
        ticket_id = basicInfo['return_ticket']
        if share_type == 0:  # 返现
            return self.jsons({'code': 100, 'msg': '商品未开启返现'})
        if share_time == 1:

            if share_type == 1:  # 返现
                if share_number != '':
                    sql = """
                    select id from cash_log 
                    where usr_id=%s and wechat_user_id=%s and ctype=2 and goods_id=%s
                    """
                    l, t = self.db.select(sql, [self.subusr_id, user, goods])
                    if t > 0:
                        return self.jsons({'code': 102, 'msg': '已经获得过返现'})
                    sql = """
                    update wechat_mall_user set balance=coalesce(balance,0)+%s where usr_id=%s and id=%s 
                    """
                    self.db.query(sql, [float(share_number), self.subusr_id, wechat_user_id])
                    sql = """
                    insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,
                    typeid,typeid_str,remark,goods_id,goods_name,cid,ctime)
                    values(%s,%s,2,'返现',%s,1,'分享返现','单次分享返现返',%s,%s,%s,now())
                    """
                    parm = [self.subusr_id, user, float(share_number), goods, gname, wechat_user_id]
                    self.db.query(sql, parm)
                    sql = """insert into profit_record(usr_id,wechat_user_id,ctype,ctype_str,share_type,
                                    share_type_str,change_money,goods_id,goods_name,cid,ctime)
                                    values(%s,%s,0,'现金收益',0,'分享返现',%s,%s,%s,%s,now())
                                    """
                    parm = [self.subusr_id, user, float(share_number), goods, gname, wechat_user_id]
                    self.db.query(sql, parm)
                    return self.jsons({'code': 0, 'msg': self.error_code['ok']})
            elif share_type == 2:  # 返积分
                if share_number != '':
                    sql = """select id from integral_log 
                        where type=7 and good_id=%s and usr_id=%s and wechat_user_id=%s"""
                    l, t = self.db.select(sql, [goods, self.subusr_id, wechat_user_id])
                    if t > 0:
                        return self.jsons({'code': 102, 'msg': '已经获得过返现'})

                    sql = """
                    update wechat_mall_user set score=coalesce(score,0)+%s where usr_id=%s and id=%s 
                    """
                    self.db.query(sql, [float(share_number), self.subusr_id, wechat_user_id])
                    sql = """
                    insert into integral_log(usr_id,wechat_user_id,type,typestr,in_out,
                    inoutstr,amount,cid,ctime)values(%s,%s,7,'分享返',0,'收入',%s,%s,now())
                    """
                    parm = [self.subusr_id, user, float(share_number), wechat_user_id]
                    self.db.query(sql, parm)
                    sql = """insert into profit_record(usr_id,wechat_user_id,ctype,ctype_str,share_type,
                            share_type_str,change_money,goods_id,goods_name,cid,ctime)
                            values(%s,%s,1,'积分收益',1,'分享返积分',%s,%s,%s,%s,now())
                            """
                    parm = [self.subusr_id, user, float(share_number), goods, gname, wechat_user_id]
                    self.db.query(sql, parm)

                    return self.jsons({'code': 0, 'msg': self.error_code['ok']})
            elif share_type == 3:  # 返优惠券
                if ticket_id != '':
                    sql = """select id from my_coupons 
                    where  wechat_user_id=%s and usr_id=%s and m_id=%s and good_id=%s and re_status=1"""
                    ll, t = self.db.select(sql, [wechat_user_id, self.subusr_id, ticket_id, goods])
                    if t > 0:
                        return self.jsons({'code': 102, 'msg': '已经获得过返现'})

                    sql = """
                        select to_char(now(),'YYYY-MM-DD'),
                            amount,to_char(dateend,'YYYY-MM-DD'),COALESCE(total,0),
                            cname,remark,type_id,type_str,case when type_id=1 then COALESCE(type_ext,'0') else '0' end type_ext,
                            apply_id,apply_str,apply_ext_num,apply_ext_money,apply_goods_id,
                            use_time,use_time_str,datestart,validday,icons,pics,remain_total
                        from coupons 
                        where usr_id=%s and COALESCE(del_flag,0)=0 and id=%s
                            """
                    parm = [self.subusr_id, ticket_id]
                    l, n = self.db.select(sql, parm)
                    if n == 0:
                        return self.jsons({'code': 404, 'msg': self.error_code[404]})

                    now_, max_num, dateend, total, cname, remark, type_id, type_str, type_ext = l[0][0:9]
                    apply_id, apply_str, apply_ext_num, apply_ext_money, apply_goods_id, use_time, use_time_str = l[0][
                                                                                                                  9:16]
                    datestart, validday, icons, pics, remain_total = l[0][16:]
                    if now_ > dateend:
                        return self.jsons({'code': 104, 'msg': '优惠券已经领完'})
                    if int(remain_total) == int(total):
                        return self.jsons({'code': 104, 'msg': '优惠券已经领完'})
                    if str(apply_id) == '1':
                        change_money = float(apply_ext_num) / 100
                    else:
                        change_money = apply_ext_num

                    data = {
                        'usr_id': self.subusr_id,
                        'wechat_user_id': wechat_user_id,
                        'm_id': ticket_id,
                        'cname': cname,
                        'type_id': type_id,
                        'type_str': type_str,
                        'type_ext': type_ext,
                        'remark': remark,
                        'icons': icons,
                        'pics': pics,
                        'goods_id': apply_goods_id,
                        'datestart': datestart or None,
                        'date_end': dateend or None,
                        'apply_id': apply_id or None,
                        'apply_str': apply_str,
                        'apply_ext_num': apply_ext_num or None,
                        'apply_ext_money': apply_ext_money or None,
                        'use_time': use_time or None,
                        'use_time_str': use_time_str,
                        'validday': validday or None,
                        'cid': self.subusr_id,
                        'ctime': self.getToday(9),
                        'good_id': goods,
                        're_status': 1

                    }

                    self.db.insert('my_coupons', data)
                    self.db.query("update coupons set remain_total=COALESCE(remain_total,0)+1 where id=%s", ticket_id)
                    sql = """insert into profit_record(usr_id,wechat_user_id,ctype,ctype_str,share_type,
                                            share_type_str,change_money,goods_id,goods_name,cid,ctime,ticket_id)
                                            values(%s,%s,2,'优惠券收益',2,'分享返优惠券',%s,%s,%s,%s,now(),%s)
                                            """
                    parm = [self.subusr_id, user, change_money, goods, gname, wechat_user_id, ticket_id]
                    self.db.query(sql, parm)
                    self.oUSER.update(self.subusr_id, wechat_user_id)
                    return self.jsons({'code': 0, 'msg': self.error_code['ok']})

        return self.jsons({'code': 101, 'msg': '返现时效非分享返'})

    def goPartUser_profit_record(self):  # 用户收益记录接口
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """select COALESCE((select  sum(change_money) from profit_record where ctype=0 and usr_id=%s and wechat_user_id=%s),0)money,
	                COALESCE((select  sum(change_money::int) from profit_record where ctype=1 and usr_id=%s and wechat_user_id=%s),0)score,
	                COALESCE((select  count(id) from profit_record where ctype=2 and usr_id=%s and wechat_user_id=%s),0)coupon,
                        (select array_to_json(array_agg(row_to_json(t)))
                from(select to_char(ctime,'YYYY-MM-DD HH24:MI')as time,ctype as type,change_money as number ,share_type 
                from profit_record where  usr_id=%s and wechat_user_id=%s order by ctime desc)t)record
        """
        parm = [self.subusr_id, wechat_user_id, self.subusr_id, wechat_user_id,
                self.subusr_id, wechat_user_id, self.subusr_id, wechat_user_id, ]
        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l[0], 'msg': self.error_code['ok']})

    def goPartOrder_state_list(self):  # 订单状态列表接口
        token = self.REQUEST.get('token', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """select 
                (select count(id) from wechat_mall_order 
                where coalesce(status,0)=1 and usr_id=%s and wechat_user_id=%s)nopaypal,
                (select count(id) from wechat_mall_order 
                where coalesce(status,0) in(2,3) and usr_id=%s and wechat_user_id=%s)delivery,
                (select count(id) from wechat_mall_order 
                where coalesce(status,0)=5 and usr_id=%s and wechat_user_id=%s)receiving,
                (select count(id) from wechat_mall_order 
                where coalesce(status,0)=4 and usr_id=%s and wechat_user_id=%s)mentions,
                (select count(id) from wechat_mall_order 
                where coalesce(status,0)=6 and usr_id=%s and wechat_user_id=%s)evaluate,
                (select count(id) from wechat_mall_order 
                where coalesce(status,0)=7 and usr_id=%s and wechat_user_id=%s)completed,
                (select count(id) from wechat_mall_order 
                where coalesce(status,0)=99 and usr_id=%s and wechat_user_id=%s)tuikuan,
                (select count(id) from wechat_mall_order 
                where coalesce(status,0) in (85,86,89) and usr_id=%s and wechat_user_id=%s)shouhou
        """
        parm = [self.subusr_id, wechat_user_id, self.subusr_id, wechat_user_id,
                self.subusr_id, wechat_user_id, self.subusr_id, wechat_user_id,
                self.subusr_id, wechat_user_id, self.subusr_id, wechat_user_id,
                self.subusr_id, wechat_user_id, self.subusr_id, wechat_user_id]

        l, t = self.db.fetchall(sql, parm)
        if t == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': l[0], 'msg': self.error_code['ok']})

    def goPartCoupons_check(self):  # 检查优惠券是否领取接口
        token = self.REQUEST.get('token', '')
        id = self.RQ('id', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if id == '' or id == 'None' or id == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('id')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        sql = """
            select to_char(now(),'YYYY-MM-DD'),
                amount,to_char(dateend,'YYYY-MM-DD'),COALESCE(total,0),
                cname,remark,type_id,type_str,case when type_id=1 then COALESCE(type_ext,'0') else '0' end type_ext,
                apply_id,apply_str,apply_ext_num,apply_ext_money,apply_goods_id,
                use_time,use_time_str,datestart,validday,icons,pics,remain_total
            from coupons 
            where usr_id=%s and COALESCE(del_flag,0)=0 and id=%s
                """
        parm = [self.subusr_id, id]
        l, n = self.db.select(sql, parm)
        if n == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        now_, max_num, dateend, total, cname, remark, type_id, type_str, type_ext = l[0][0:9]
        apply_id, apply_str, apply_ext_num, apply_ext_money, apply_goods_id, use_time, use_time_str = l[0][9:16]
        datestart, validday, icons, pics, remain_total = l[0][16:]
        if now_ > dateend:
            return self.jsons({'code': 301, 'msg': '优惠券已经发完'})
        if int(remain_total) == int(total):
            return self.jsons({'code': 301, 'msg': '优惠券已经发完'})

        sql = "select id from my_coupons where wechat_user_id=%s and usr_id=%s and m_id=%s"
        ll, t = self.db.select(sql, [wechat_user_id, self.subusr_id, id])
        if t >= max_num:
            return self.jsons({'code': 300, 'msg': '已经领过此优惠券'})
        if str(type_id) == '1':
            sql = "select COALESCE(score,0) from wechat_mall_user where usr_id=%s and id=%s"
            score = self.db.fetchcolumn(sql, [self.subusr_id, wechat_user_id])
            if int(type_ext) > int(score):
                return self.jsons({'code': 302, 'msg': '您的积分不够!'})
        money_ = apply_ext_num
        # if str(apply_id)=='1':
        #     money_ = round(float(apply_ext_num)/100, 2)
        data = {
            'id': id,
            'name': cname,
            'money': money_,
            'type': apply_id,
            'remark': remark,
            'icons': icons,
            'pics': pics,
        }
        return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})

    def goPartPingtuan_goods_list(self):  # 获取可以拼团的商品列表
        token = self.REQUEST.get('token', '')
        ctype = self.RQ('ctype', '')
        ktype = self.RQ('ktype', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if ctype == '' or ctype == 'None' or ctype == 'undefined':
            ctype = ''
        if ktype == '' or ktype == 'None' or ktype == 'undefined':
            ktype = ''

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        sql = """select g.id 
                    ,g.name	--商品名称
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
                    and COALESCE(p.status,0)=0
                    """
        lT1, iN1 = self.db.fetchall(sql, self.subusr_id)
        if iN1 == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        if ctype != '' and ktype != '':
            data = []
            for j in lT1:
                kt_type = j.get('ptuan_ktype', '')
                add_type = j.get('ptuan_ctype', '')
                if ktype == str(kt_type) and ctype == str(add_type):
                    data.append(j)
        elif ctype != '' and ktype == '':
            data = []
            for j in lT1:
                add_type = j.get('ptuan_ctype', '')
                if ctype == str(add_type):
                    data.append(j)


        elif ctype == '' and ktype != '':
            data = []
            for j in lT1:
                kt_type = j.get('ptuan_ktype', '')
                if ktype == str(kt_type):
                    data.append(j)
        else:
            data = lT1
        if len(data) == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})

    def goPartPingtuan_goods_recommend(self):  # 获取推荐的拼团商品列表
        # token = self.REQUEST.get('token', '')
        # ctype = self.RQ('ctype', '')
        # ktype = self.RQ('ktype', '')
        #
        # if token == '' or token == 'None' or token == 'undefined':
        #     return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})
        #
        # if ctype == '' or ctype == 'None' or ctype == 'undefined':
        #     ctype = ''
        # if ktype == '' or ktype == 'None' or ktype == 'undefined':
        #     ktype = ''

        # dR = self.check_token(token)
        # if dR['code'] != 0:
        #     return self.jsons({'code': 901, 'msg': dR['MSG']})
        # wechat_user_id = dR['wechat_user_id']
        sql = """select g.id 
                    ,g.name	--商品名称
                    ,g.introduce	--商品简介
                    ,g.pic	--商品第一张图片
                    ,g.minprice as mini_price	--商品现价
                    ,g.originalprice as original_price	--商品原价
                    ,g.pt_price as ptuan_price
                    ,p.pt_num as ptuan_success
                    ,p.ok_num as ptuan_number
                    ,p.id as ptuan_id
                    ,p.kt_type as ptuan_ktype
                    ,p.add_type as ptuan_ctype
                from pt_conf p
                left join goods_info g on p.usr_id=g.usr_id and p.goods_id=g.id
                where p.usr_id=%s and COALESCE(g.del_flag,0)=0 and COALESCE(p.del_flag,0)=0
                    and COALESCE(g.status,0)=0  and COALESCE(g.pt_status,0)=1  and COALESCE(p.status,0)=0
                     and COALESCE(p.recom,0)=1
                     """
        lT1, iN1 = self.db.fetchall(sql, self.subusr_id)
        if iN1 == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': lT1, 'msg': self.error_code['ok']})

    def goPartPingtuan_goods(self):  # 获取商品开团列表
        token = self.REQUEST.get('token', '')
        gid = self.RQ('goods', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if gid == '' or gid == 'None' or gid == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('gid')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']
        sql = """
            select id as kid,ptid as id,name,avatar,number,short,
            case when to_char(date_end,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') 
            then to_char(date_end,'YYYY-MM-DD HH24:MI') 
            else '' end  date_end,
            to_char(ctime,'YYYY-MM-DD HH24:MI')date_add 
            from open_pt 
            where coalesce(del_flag,0)=0 and coalesce(status,0)=1 and usr_id=%s and gid=%s
            and wechat_user_id!=%s
            order by date_end ;
                """
        parm = [self.subusr_id, gid, wechat_user_id]
        l, n = self.db.fetchall(sql, parm)
        if n == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        L = []
        for i in l:
            date_end = i.get('date_end', '')
            kid = i.get('kid', '')
            # if date_end=='':
            #     sqlk="""select coalesce(ok_type,0),coalesce(add_type,0),coalesce(tk_type,0) from open_pt
            #         where usr_id=%s and id=%s and coalesce(del_flag,0)=0 and coalesce(status,0)=1"""
            #     lT,iN=self.db.select(sqlk,[self.subusr_id, kid])
            #     if iN>0:
            #         ok_type,add_type,tk_type=lT[0]
            #         if str(ok_type)=='1':#促团
            #             self.Pingtuan_ok_join(kid)
            #         else:#关闭并退款
            #             self.Pingtuan_close(kid,tk_type)
            #

            if len(L) > 9:
                break
            if date_end != '':
                L.append(i)
        if len(L) == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})

        return self.jsons({'code': 0, 'data': L, 'msg': self.error_code['ok']})

    def Pingtuan_close(self, ptkid, tk_type):  # 超时关团退款 11 拼团失败
        sql = "select order_id,ptid,wechat_user_id from open_pt_detail where usr_id=%s and status=1 and opid=%s"
        l, t = self.db.select(sql, [self.subusr_id, ptkid])
        if t == 0:
            return
        for i in l:
            orderid, ptid, wechat_user_id = i
            sql = """select pay_status,new_total,order_num,balance 
                    from wechat_mall_order where usr_id=%s and status=10 and id=%s and wechat_user_id=%s"""
            ll, tt = self.db.select(sql, [self.subusr_id, orderid, wechat_user_id])
            if tt != 0:
                pay_status, new_total, order_num, balance = ll[0]
                if str(tk_type) == '2':  # 退回余额
                    sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                    self.db.query(sql, [new_total, self.subusr_id, wechat_user_id])
                    self.user_log(wechat_user_id, 'balance:%s' % new_total, '用户取消订单余额变化')
                    sql = """
                    insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                    values(%s,%s,3,'消费',%s,4,'退回',%s,'取消订单退款',%s,now())
                            """
                    self.db.query(sql, [self.subusr_id, wechat_user_id, -new_total, order_num, self.subusr_id])
                if str(tk_type) == '1':  # 原路退回
                    sql = """
                    insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                    values(%s,%s,3,'消费',%s,4,'退回',%s,'取消订单退款',%s,now())
                            """
                    self.db.query(sql, [self.subusr_id, wechat_user_id, -new_total, order_num, self.subusr_id])
                    if str(pay_status) == '1':  # 微信
                        self.order_refund(orderid, order_num, wechat_user_id)
                    elif str(pay_status) == '2':  # 余额
                        sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                        self.db.query(sql, [new_total, self.subusr_id, wechat_user_id])
                        self.user_log(wechat_user_id, 'balance:%s' % new_total, '用户取消订单余额变化')
                        sql = """
                        insert into cash_log(usr_id,wechat_user_id,ctype,ctype_str,change_money,typeid,typeid_str,cnumber,remark,cid,ctime)
                        values(%s,%s,3,'消费',%s,4,'退回',%s,'取消订单退款',%s,now())
                                """
                        self.db.query(sql, [self.subusr_id, wechat_user_id, -new_total, order_num, self.subusr_id])
                    elif str(pay_status) == '3':  # 微信+余额
                        self.order_refund(orderid, order_num, wechat_user_id)
                        sql = "update wechat_mall_user set balance=balance+%s where usr_id=%s and id=%s"
                        self.db.query(sql, [balance, self.subusr_id, wechat_user_id])
                        self.user_log(wechat_user_id, 'balance:%s' % new_total, '用户取消订单余额变化')

                self.db.query("update open_pt set status=3 where id=%s and usr_id=%s", [ptkid, self.subusr_id])
                self.db.query("update open_pt_detail set status=3 where opid=%s and usr_id=%s", [ptkid, self.subusr_id])

                sqld = """
                    update wechat_mall_order set 
                    status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                     update wechat_mall_order_detail set 
                    status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                    """
                self.db.query(sqld, [self.subusr_id, orderid, self.subusr_id, orderid])
                self.write_order_log(orderid, '拼团失败', '更新订单状态为拼团失败',
                                     '订单id:%s' % orderid)
                self.oUSER.update(self.subusr_id, wechat_user_id)

        return

    def Pingtuan_ok_join(self, ptkid):  # 促团
        # self.print_log('order_id:%s'%order_id,'ptkid:%s'%ptkid)
        sql = "select wechat_user_id,cname,avatar from virtual_conf where usr_id=%s order by id desc"
        lT, iN = self.db.select(sql, [self.subusr_id])
        if iN == 0:
            return

        sql = "select ptid,order_id,number,short from open_pt where usr_id=%s and id=%s and status=1"
        l, t = self.db.select(sql, [self.subusr_id, ptkid])
        if t == 0:
            return
        ptid, orderid, number, short = l[0]

        while short > 0:

            ws = random.randint(0, iN - 1)
            wechat_user_id, cname, avatar = lT[ws]
            # self.print_log('number:%s'%number,'short:%s'%short)
            oPT_GOODS = self.oPT_GOODS.get(self.subusr_id, ptid)
            timeout_h = oPT_GOODS['timeout_h']
            cnow = datetime.datetime.now()
            # ctime = now.strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(hours=int(timeout_h))
            n_days = cnow + delta
            date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

            datad = {
                'usr_id': self.subusr_id,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'opid': ptkid,
                'name': cname,
                'avatar': avatar,
                'title': 2,
                'status': 1,
                'date_end': date_end,
                'cid': wechat_user_id,
                'ctime': self.getToday(9)
            }
            self.db.insert('open_pt_detail', datad)
            self.db.query("update open_pt set short=short-1 where id=%s and usr_id=%s", [ptkid, self.subusr_id])
            if int(short) == 1:
                self.db.query("update open_pt set status=2 where id=%s and usr_id=%s", [ptkid, self.subusr_id])
                self.db.query("update open_pt_detail set status=2 where opid=%s and usr_id=%s", [ptkid, self.subusr_id])
                ############处理订单状态
                sqlp = "select id,kuaid from wechat_mall_order where usr_id=%s and ptkid=%s and ctype=2"
                l, t = self.db.select(sqlp, [self.subusr_id, ptkid])
                if t > 0:
                    for i in l:
                        orderdid, kuaid = i
                        if str(kuaid) == '0':  # 快递单
                            sqld = """
                                    update wechat_mall_order set 
                                    status=2,status_str='待发货' where usr_id=%s and id=%s;
                                     update wechat_mall_order_detail set 
                                    status=2,status_str='待发货' where usr_id=%s and order_id=%s; 
                                    """
                            self.db.query(sqld, [self.subusr_id, orderdid, self.subusr_id, orderdid])
                            self.write_order_log(orderdid, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)


                        elif str(kuaid) == '1':  # 自提单
                            sqld = """
                                    update wechat_mall_order set 
                                        status=4,status_str='待自提' where usr_id=%s and id=%s; 
                                    update wechat_mall_order_detail set 
                                        status=4,status_str='待自提' where usr_id=%s and order_id=%s; 
                                    """
                            self.db.query(sqld, [self.subusr_id, orderdid, self.subusr_id, orderdid])
                            self.write_order_log(orderdid, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)

                        elif str(kuaid) == '2':  # 无须配送
                            sqld = """
                                update wechat_mall_order set 
                                    status=6,status_str='待评价' where usr_id=%s and id=%s;
                                update wechat_mall_order_detail set 
                                    status=6,status_str='待评价' where usr_id=%s and order_id=%s; 
                                """
                            self.db.query(sqld, [self.subusr_id, orderdid, self.subusr_id, orderdid])
                            self.write_order_log(orderdid, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)

            short = short - 1
        return

    def goPartPingtuan_new_tuan(self):  # 团长开新团
        token = self.REQUEST.get('token', '')
        goods = self.RQ('goods', '')
        ptid = self.RQ('ptid', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if goods == '' or goods == 'None' or goods == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods')})

        if ptid == '' or ptid == 'None' or ptid == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('ptid')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
            select kt_type,
            case when to_char(date_end,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') then 0 
            else 1 end 
            from pt_conf where usr_id=%s and goods_id=%s and id=%s 
            and coalesce(del_flag,0)=0 and coalesce(status,0)=0
        """
        parm = [self.subusr_id, goods, ptid]
        ll, tt = self.db.select(sql, parm)
        if tt == 0:
            return self.jsons({'code': 301, 'msg': '拼团ID不正确'})
        kt_type, date_end = ll[0]

        if str(date_end) == '1':
            return self.jsons({'code': 302, 'msg': '拼团已经结束'})

        sql = """
            select id from open_pt_detail 
            where usr_id=%s and wechat_user_id=%s and coalesce(status,0)=1 and coalesce(del_flag,0)=0 
            and ptid=%s
            """
        parm = [self.subusr_id, wechat_user_id, ptid]
        lT, iN = self.db.select(sql, parm)
        if iN > 0:
            return self.jsons({'code': 303, 'msg': '已有未完成的拼团'})

        sql = """
            select ptid,coalesce(status,0) from open_pt_detail 
            where usr_id=%s and wechat_user_id=%s and coalesce(del_flag,0)=0 
                """
        parm = [self.subusr_id, wechat_user_id]
        l, t = self.db.select(sql, parm)

        if t > 0 and str(kt_type) == '1':
            return self.jsons({'code': 304, 'msg': '仅限新用户开团'})

        if t == 0 and str(kt_type) == '2':
            return self.jsons({'code': 305, 'msg': '仅限老用户开团'})

        return self.jsons({'code': 0, 'msg': '开团成功'})

    def Pingtuan_add(self, wechat_user_id, ptid, order_id, phone):
        sqlw = """select id from wechat_mall_order 
                where ctype=2  and usr_id=%s and wechat_user_id=%s and id=%s and coalesce(pay_status,0)!=0
                """
        lT, iN = self.db.select(sqlw, [self.subusr_id, wechat_user_id, order_id])
        if iN == 0:
            return

        try:
            cur_random_no = "%s%s" % (time.time(), random.random())
            oUSER = self.oUSER.get(self.subusr_id, wechat_user_id)
            name = oUSER['name']
            avatar = oUSER['avatar']
            # self.print_log('subusr_id:%s,ptid:%s'%(self.subusr_id, ptid),'%s'%self.oPT_GOODS.get(self.subusr_id))
            oPT_GOODS = self.oPT_GOODS.get(self.subusr_id, ptid)
            number = oPT_GOODS['cnumber']
            gid = oPT_GOODS['gid']
            gname = oPT_GOODS['gname']
            gintr = oPT_GOODS['gintr']
            gpic = oPT_GOODS['gpic']
            gcontent = oPT_GOODS['gcontent']
            ptprice = oPT_GOODS['pt_price']
            mnprice = oPT_GOODS['mini_price']
            stores = oPT_GOODS['stores']
            ok_type = oPT_GOODS['ok_type']
            add_type = oPT_GOODS['add_type']
            tk_type = oPT_GOODS['tk_type']
            kt_type = oPT_GOODS['kt_type']
            timeout_h = oPT_GOODS['timeout_h']

            cnow = datetime.datetime.now()
            # ctime = now.strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(hours=int(timeout_h))
            n_days = cnow + delta
            date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

            data = {
                'usr_id': self.subusr_id,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'order_id': order_id,
                'name': name,
                'avatar': avatar,
                'number': number,
                'short': number - 1,
                'phone': phone,
                'status': 1,
                'ok_type': ok_type,
                'add_type': add_type,
                'tk_type': tk_type,
                'kt_type': kt_type,
                'date_end': date_end,
                'gid': gid,
                'gname': gname,
                'gintr': gintr,
                'gpic': gpic,
                'gcontent': gcontent,
                'ptprice': ptprice,
                'mnprice': mnprice,
                'stores': stores,
                'random_no': cur_random_no,
                'cid': wechat_user_id,
                'ctime': self.getToday(9)

            }
            self.db.insert('open_pt', data)
            opid = self.db.fetchcolumn("select id from open_pt where random_no=%s", cur_random_no)
            sqlo = """
                update wechat_mall_order set ptkid=%s,status=10,status_str='拼团中' where usr_id=%s and id=%s 
                        """
            self.db.query(sqlo, [opid, self.subusr_id, order_id])
            sqld = """
                update wechat_mall_order_detail set 
                status=10,status_str='拼团中' where usr_id=%s and order_id=%s; 
                """
            self.db.query(sqld, [self.subusr_id, order_id])
            datad = {
                'usr_id': self.subusr_id,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'opid': opid,
                'order_id': order_id,
                'name': name,
                'avatar': avatar,
                'phone': phone,
                'title': 1,
                'status': 1,
                'date_end': date_end,
                'cid': wechat_user_id,
                'ctime': self.getToday(9)
            }
            self.db.insert('open_pt_detail', datad)
            return
        except:
            self.print_log('subusr_id:%s,ptid:%s' % (self.subusr_id, ptid), '%s' % self.oPT_GOODS.get(self.subusr_id))
            self.print_log('拼团失败', '%s' % str(traceback.format_exc()))
            self.Pingtuan_add_close(order_id)
            return

    def Pingtuan_add_close(self, order_id):  # 开团数据处理失败进行拼团失败处理

        lT, iN = self.db.select("select id from open_pt where usr_id=%s and  order_id=%s", [self.subusr_id, order_id])
        if iN > 0:
            return

        sqlw = """select id from wechat_mall_order 
                        where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                        """
        lT, iN = self.db.select(sqlw, [self.subusr_id, order_id])
        if iN == 0:
            return

        sqld = """
            update wechat_mall_order set 
            status=11,status_str='拼团失败' where usr_id=%s and id=%s;
             update wechat_mall_order_detail set 
            status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
            """
        self.db.query(sqld, [self.subusr_id, order_id, self.subusr_id, order_id])
        self.write_order_log(order_id, '开团失败', '更新订单状态为拼团失败',
                             '订单id:%s' % order_id)
        return

    def Pingtuan_join(self, wechat_user_id, ptkid, order_id, phone):
        # self.print_log('order_id:%s'%order_id,'ptkid:%s'%ptkid)
        sqlw = """select id from wechat_mall_order 
                                where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                                """
        lT, iN = self.db.select(sqlw, [self.subusr_id, order_id])
        if iN == 0:
            return
        try:
            sql = "select ptid,number,short from open_pt where usr_id=%s and id=%s and coalesce(status,0)=1"
            l, t = self.db.select(sql, [self.subusr_id, ptkid])
            if t == 0:
                sqld = """
                    update wechat_mall_order set 
                    status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                     update wechat_mall_order_detail set 
                    status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                    """
                self.db.query(sqld, [self.subusr_id, order_id, self.subusr_id, order_id])
                self.write_order_log(order_id, '拼团成功', '更新订单状态为待发货',
                                     '订单id:%s' % order_id)
                return
            ptid, number, short = l[0]

            oUSER = self.oUSER.get(self.subusr_id, wechat_user_id)
            name = oUSER['name']
            avatar = oUSER['avatar']

            # self.print_log('number:%s'%number,'short:%s'%short)
            oPT_GOODS = self.oPT_GOODS.get(self.subusr_id, ptid)
            timeout_h = oPT_GOODS['timeout_h']
            cnow = datetime.datetime.now()
            # ctime = now.strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(hours=int(timeout_h))
            n_days = cnow + delta
            date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

            datad = {
                'usr_id': self.subusr_id,
                'wechat_user_id': wechat_user_id,
                'ptid': ptid,
                'opid': ptkid,
                'order_id': order_id,
                'name': name,
                'avatar': avatar,
                'phone': phone,
                'title': 2,
                'status': 1,
                'date_end': date_end,
                'cid': wechat_user_id,
                'ctime': self.getToday(9)
            }
            self.db.insert('open_pt_detail', datad)
            self.db.query("update open_pt set short=short-1 where id=%s and usr_id=%s", [ptkid, self.subusr_id])

            sqlo = """
                update wechat_mall_order set ptid=%s,status=10,status_str='拼团中' where usr_id=%s and id=%s 
                """
            self.db.query(sqlo, [ptid, self.subusr_id, order_id])

            sqld = """
                update wechat_mall_order_detail set 
                status=10,status_str='拼团中' where usr_id=%s and order_id=%s; 
                """
            self.db.query(sqld, [self.subusr_id, order_id])

            if int(short) == 1:
                self.db.query("update open_pt set status=2 where id=%s and usr_id=%s", [ptkid, self.subusr_id])
                self.db.query("update open_pt_detail set status=2 where opid=%s and usr_id=%s", [ptkid, self.subusr_id])
                ############处理订单状态
                sqlp = "select id,kuaid from wechat_mall_order where usr_id=%s and ptkid=%s and ctype=2 and status=10"
                l, t = self.db.select(sqlp, [self.subusr_id, ptkid])
                if t > 0:
                    for i in l:
                        orderdid, kuaid = i
                        if str(kuaid) == '0':  # 快递单
                            sqld = """
                                update wechat_mall_order set 
                                status=2,status_str='待发货' where usr_id=%s and id=%s;
                                 update wechat_mall_order_detail set 
                                status=2,status_str='待发货' where usr_id=%s and order_id=%s; 
                                """
                            self.db.query(sqld, [self.subusr_id, orderdid, self.subusr_id, orderdid])
                            self.write_order_log(orderdid, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)


                        elif str(kuaid) == '1':  # 自提单
                            sqld = """
                                    update wechat_mall_order set 
                                        status=4,status_str='待自提' where usr_id=%s and id=%s; 
                                    update wechat_mall_order_detail set 
                                        status=4,status_str='待自提' where usr_id=%s and order_id=%s; 
                                    """
                            self.db.query(sqld, [self.subusr_id, orderdid, self.subusr_id, orderdid])
                            self.write_order_log(order_id, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)

                        elif str(kuaid) == '2':  # 无须配送
                            sqld = """
                                    update wechat_mall_order set 
                                        status=6,status_str='待评价' where usr_id=%s and id=%s;
                                    update wechat_mall_order_detail set 
                                        status=6,status_str='待评价' where usr_id=%s and order_id=%s; 
                                    """
                            self.db.query(sqld, [self.subusr_id, orderdid, self.subusr_id, orderdid])
                            self.write_order_log(order_id, '拼团成功', '更新订单状态为待发货',
                                                 '订单id:%s' % orderdid)

            return
        except:
            self.print_log('参团失败', '%s' % str(traceback.format_exc()))
            self.Pingtuan_join_close(order_id)
            return

    def Pingtuan_join_close(self, order_id):  # 参团数据处理失败进行拼团失败处理

        lT, iN = self.db.select("select id from open_pt_detail where usr_id=%s and  order_id=%s",
                                [self.subusr_id, order_id])
        if iN > 0:
            return

        sqlw = """select id from wechat_mall_order 
                        where ctype=2  and usr_id=%s and id=%s and coalesce(pay_status,0)!=0
                        """
        lT, iN = self.db.select(sqlw, [self.subusr_id, order_id])
        if iN == 0:
            return

        sqld = """
            update wechat_mall_order set 
            status=11,status_str='拼团失败' where usr_id=%s and id=%s;
             update wechat_mall_order_detail set 
            status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
            """
        self.db.query(sqld, [self.subusr_id, order_id, self.subusr_id, order_id])
        self.write_order_log(order_id, '参团失败', '更新订单状态为拼团失败',
                             '订单id:%s' % order_id)
        return

    def goPartPingtuan_join_tuan(self):  # 团员加入拼团
        token = self.REQUEST.get('token', '')
        goods = self.RQ('goods', '')
        ptid = self.RQ('ptid', '')
        ptkid = self.RQ('ptkid', '')

        if token == '' or token == 'None' or token == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if goods == '' or goods == 'None' or goods == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('goods')})

        if ptid == '' or ptid == 'None' or ptid == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('ptid')})

        if ptkid == '' or ptkid == 'None' or ptkid == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('ptkid')})

        dR = self.check_token(token)
        if dR['code'] != 0:
            return self.jsons({'code': 901, 'msg': dR['MSG']})
        wechat_user_id = dR['wechat_user_id']

        sql = """
            select id from pt_conf where usr_id=%s and goods_id=%s and id=%s
                """
        parm = [self.subusr_id, goods, ptid]
        ll, tt = self.db.select(sql, parm)
        if tt == 0:
            return self.jsons({'code': 301, 'msg': '拼团ID不正确'})

        sql = """
            select coalesce(status,0),add_type,
            case when to_char(date_end,'YYYY-MM-DD HH24:MI')>to_char(now(),'YYYY-MM-DD HH24:MI') then 0 
            else 1 end  
            from open_pt
            where usr_id=%s and id=%s and ptid=%s and gid=%s and coalesce(del_flag,0)=0
            """
        parm = [self.subusr_id, ptkid, ptid, goods]
        lT, iN = self.db.select(sql, parm)
        if iN == 0:
            return self.jsons({'code': 302, 'msg': '开团ID不正确'})

        status, add_type, date_end = lT[0]

        if str(status) != '1':
            return self.jsons({'code': 303, 'msg': '拼团已经结束'})
        if str(date_end) == '1':
            return self.jsons({'code': 304, 'msg': '拼团已经过期'})

        sql = """
            select status from wechat_mall_order 
            where ctype=2  and usr_id=%s and wechat_user_id=%s 
            and coalesce(status,0) =10 and coalesce(del_flag,0)=0 and (ptkid=%s or ptid=%s)
            """
        parm = [self.subusr_id, wechat_user_id, ptkid, ptid]
        lT1, iN1 = self.db.select(sql, parm)
        if iN1 > 0:
            return self.jsons({'code': 307, 'msg': '已有未完成的拼团'})

        sql = """
            select id from open_pt_detail 
            where usr_id=%s and wechat_user_id=%s and ptid=%s and opid=%s
            and coalesce(status,0)!=3 and coalesce(del_flag,0)=0
            """
        parm = [self.subusr_id, wechat_user_id, ptid, ptkid]
        l, t = self.db.select(sql, parm)

        if t == 0 and str(add_type) == '2':
            return self.jsons({'code': 306, 'msg': '仅限老用户参团'})
        elif t > 0 and str(add_type) == '1':
            return self.jsons({'code': 305, 'msg': '仅限新用户参团'})

        return self.jsons({'code': 0, 'msg': '参团成功'})

    def goPartPingtuan_details(self):  # 拼团详情信息
        # token = self.REQUEST.get('token', '')
        ptkid = self.RQ('ptkid', '')

        # if token == '' or token == 'None' or token == 'undefined':
        #     return self.jsons({'code': 300, 'msg': self.error_code[300].format('token')})

        if ptkid == '' or ptkid == 'None' or ptkid == 'undefined':
            return self.jsons({'code': 300, 'msg': self.error_code[300].format('ptkid')})

        # dR = self.check_token(token)
        # if dR['code'] != 0:
        #     return self.jsons({'code': 901, 'msg': dR['MSG']})
        # wechat_user_id = dR['wechat_user_id']

        sql = """
            select coalesce(status,0) from open_pt_detail 
            where usr_id=%s  and opid=%s
                """
        parm = [self.subusr_id, ptkid]
        l, n = self.db.select(sql, parm)
        if n == 0:
            return self.jsons({'code': 404, 'msg': self.error_code[404]})
        sql = """
            select ptid as id,id as kid,status,"number",short,
            (stores + (select count(id) from pt_conf where coalesce(status,0)=2 and ptid=o.ptid))stores,
            ptprice,mnprice,(mnprice-ptprice)svprice,
            gid,gname,gintr,gpic,gcontent,to_char(ctime,'YYYY-MM-DD HH24:MI')date_start,
            to_char(date_end,'YYYY-MM-DD HH24:MI')date_end,
            (select array_to_json(array_agg(row_to_json(t)))
                from(select name,avatar,wechat_user_id as uid 
                from open_pt_detail where o.id=opid order by ctime)t)ptuser
            from open_pt o where usr_id=%s and id=%s
        
        """
        data = self.db.fetch(sql, [self.subusr_id, ptkid])
        return self.jsons({'code': 0, 'data': data, 'msg': self.error_code['ok']})
