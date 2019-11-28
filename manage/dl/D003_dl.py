# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
""" admin/dl/D003_dl.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import  time , random,datetime,traceback

class cD003_dl(cBASE_DL):
    def init_data(self):
        self.GNL = ['', '积分规则设置', '积分商品设置']  # 列表表头



    #在子类中重新定义         
    def myInit(self):

        self.part = self.GP('part', 'Localfrm')
        self.tab = self.GP("tab", "1")

    def get_local_data(self):
        """获取 local 表单的数据
        """
        L = []
        sql = ""
        if str(self.tab) == '1':
            sql = """select p.id,p.good_name,
                    p.ok_num + (select count(id) from open_pt where status=2 and ptid=p.id ),
                    (select count(id) from open_pt where status=1 and ptid=p.id ),p.pt_num,p.timeout_h,
                    m.txt1,t.txt1 ,
                    case when p.tk_type=1 then '原路退回' else '退回余额' end,
                    to_char(p.date_add,'YYYY-MM-DD HH24:MI')date_add,
                    to_char(p.date_end,'YYYY-MM-DD HH24:MI')date_end,
                    case when p.status=1 then '禁用' else '启用' end
                    from  pt_conf p 
                    left join mtc_t m on m.id=p.kt_type and m.type='t_type' 
                    left join mtc_t t on t.id=p.add_type and t.type='t_type' 
                    where usr_id=%s  and coalesce(p.del_flag,0)=0 order by p.id
                
                """ % self.usr_id_p

        elif str(self.tab) == '2':
            sql = """
                 select o.id,o.ptid,o.gname,o.name,o.phone,(select count(id) from open_pt_detail where opid=o.id),
                 case when o.kt_type=1 then '新人团' when o.kt_type=2 then '老用户团' else '新老用户团' end ,
                 case when o.add_type=1 then '新人团' when o.add_type=2 then '老用户团' else '新老用户团' end ,
                 case when o.status=1 then '拼团中' when o.status=2 then '拼团成功' else '拼团失败' end,
                 to_char(o.ctime,'YYYY-MM-DD HH24:MI'),
                 to_char(o.date_end,'YYYY-MM-DD HH24:MI')
                from open_pt o
                    where o.usr_id=%s  order by o.ptid
            """ % self.usr_id_p

        elif str(self.tab) == '3':
            sql = """select o.id,o.ptid,o.gname,o.order_id,o.name,o.phone,
                        (select array_to_json(array_agg(row_to_json(t))) from(select name,coalesce(phone,'')phone from open_pt_detail 
                        where o.id=opid and title=2 order by ctime)t)ptuser,
                        to_char(o.ctime,'YYYY-MM-DD HH24:MI') from open_pt o 
                                where o.usr_id=%s order by o.id
                            """ % self.usr_id_p

        elif str(self.tab)=='4':
            sql = "select id,cname,avatar from virtual_conf where usr_id=%s order by id"% self.usr_id_p

        # elif str(self.tab)=='5':
        #     sql="select vip_price,up_type,discount,up_type_str from member where usr_id=%s"
        #
        # elif str(self.tab)=='6':
        #     sql="""select home_goods,home_goods_str,home_goods_id,
        #                 shop_goods,shop_goods_str,shop_goods_id,
        #                 order_goods,order_goods_str,order_goods_id,
        #                 shop_cart_memo,menu_memo
        #             from global_config where usr_id=%s"""
        # else:
        #     sql="select vip_price,up_type,discount from member where usr_id=%s"

        if sql != '':
            L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo)
            PL = [pageNo, iTotal_Page, iTotal_length, select_size]
            return PL, L
        return [], []
    
    def local_add_save(self):

        dR = {'code': '', 'MSG': '保存成功'}

        self.tab = self.GP('multab', '')
        if str(self.tab) == '1':
            ptid = self.GP('ptid', '')  # 商品id
            goods_id = self.GP('goods_id', '')  # 商品id
            good_name = self.GP('good_name', '')  # 商品名称
            pt_price = self.GP('pt_price', '')  # 拼团价格
            pt_num = self.GP('pt_num', '')  # 开团人数
            ok_num = self.GP('ok_num', '')  # 成团人数
            timeout_h = self.GP('timeout_h', '')  # 超时时间
            kt_type = self.GP('kt_type', '')  # 开团类型
            add_type = self.GP('add_type', '')  # 参团类型
            tk_type = self.GP('tk_type', '')  # 退款方式
            ok_type = self.GP('ok_type', '')  # 到期促团
            status = self.GP('status', '')  # 状态
            recom = self.GP('recom', '')  # 状态
            date_add = self.GP('date_add', '')  # 开始时间
            date_end = self.GP('date_end', '')  # 到期时间
            cur_random_no = "%s%s" % (time.time(), random.random())
            data = {
                'goods_id': goods_id,
                'good_name': good_name,

                'pt_num': pt_num,
                'ok_num': ok_num,
                'timeout_h': timeout_h,
                'kt_type': kt_type,
                'add_type': add_type,
                'tk_type': tk_type,
                'ok_type': ok_type,
                'status': status,
                'recom': recom,
                'date_add': date_add,
                'date_end': date_end,
                'random_no': cur_random_no,

            }  # pt_conf

            if str(ptid) == '0':  # insert
                data['usr_id'] = self.usr_id_p
                data['cid'] = self.usr_id
                data['ctime'] = self.getToday(9)
                self.db.insert('pt_conf', data)
                ptid = self.db.fetchcolumn('select id from pt_conf where random_no=%s', cur_random_no)  # 这个的格式是表名_自增字段
                self.use_log('增加拼团活动%s' % ptid)

            else:  #update
                data['uid'] = self.usr_id
                data['utime'] = self.getToday(9)
                self.db.update('pt_conf', data, " id = %s and usr_id=%s " % (ptid, self.usr_id_p))
                self.use_log('修改拼团活动%s' % ptid)

            #更新数据缓存
            # self.oGOODS_D.update(self.usr_id_p, goods_id)
            # self.oGOODS.update(self.usr_id_p, goods_id)
            # self.oGOODS_N.update(self.usr_id_p, goods_id)
            # self.oGOODS_SELL.update(self.usr_id_p)
            # self.oGOODS_PT.update(self.usr_id_p,goods_id)
            self.oPT_GOODS.update(self.usr_id_p,ptid)



        # if str(self.tab) == '2':
        #     lid = self.GP('lid')  # 商品id
        #     goods_id = self.GP('goods_id')  # 商品id
        #     good_name = self.GP('good_name')  # 商品名称
        #     score = self.GP('score', '')  # 所需积分
        #     amount = self.GP('amount', '')  # 限量多少件
        #     max_amount = self.GP('max_amount', '')  # 最大兑换数量
        #     #complete_id = self.GP('complete_id', '')  # 订单完成通知
        #     #if use_money==''
        #     data = {
        #         'goods_id': goods_id or None,
        #         'goods_name': good_name,
        #         'score': score or None,
        #         'amount': amount or None,
        #         'max_amount': max_amount or None,
        #         #'complete_id': complete_id,
        #
        #     }  # order_set
        #     #l, t = self.db.select("select id from score_goods where usr_id=%s", self.usr_id)
        #     if lid=='':
        #     #if t == 0:  # insert
        #         data[ 'usr_id']=self.usr_id_p
        #         data['cid'] = self.usr_id
        #         data['ctime'] = self.getToday(9)
        #         self.db.insert('score_goods', data)
        #
        #
        #     else:  # update
        #         # 如果是插入 就去掉 uid，utime 的处理
        #         data['uid'] = self.usr_id
        #         data['utime'] = self.getToday(9)
        #         self.db.update('score_goods', data, " id = %s " % lid)



        dR['code'] = 0
        return dR


    def ajax_update_data(self):
        pk = self.pk
        dR = {'code': '', 'MSG': ''}
        sql = """select id,goods_id,good_name,ok_num,pt_num,timeout_h,recom,status,
                    kt_type,add_type,tk_type,ok_type,
                    to_char(date_add,'YYYY-MM-DD HH24:MI')date_add,to_char(date_end,'YYYY-MM-DD HH24:MI')date_end
                from  pt_conf p     
                where usr_id=%s and id=%s
                        """
        d = self.db.fetch(sql, [self.usr_id_p, pk])
        if str(d.get('id', '')) != pk:
            dR['code'] = '1'
            return
        dR['code'] = '0'
        dR['data'] = d
        return dR

    def ajax_add_data(self):
        sid = self.GP('sid', '')  # 商品id
        cname = self.GP('cname', '')  # 商品名称
        avatar = self.GP('avatar', '')  # 拼团价格

        cur_random_no = "%s%s" % (time.time(), random.random())
        data = {
            'cname': cname,
            'avatar': avatar,
        }  # pt_conf

        if sid == '':  # insert
            wdata={
            'cname':cname,
            'open_id': cur_random_no,
            'avatar_url': avatar,
            'usr_id':self.usr_id_p,
            'ctime':self.getToday(9),
            'del_flag':0,
            'random_no':cur_random_no
            }
            self.db.insert('wechat_mall_user', wdata)
            uid = self.db.fetchcolumn('select id from wechat_mall_user where random_no=%s', cur_random_no)  # 这个的格式是表名_自增字段
            self.oUSER.update(self.usr_id_p, uid)
            data['wechat_user_id'] = uid
            data['usr_id'] = self.usr_id_p
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            self.db.insert('virtual_conf', data)
            self.use_log('增加虚拟用户')


        else:  #update
            data['uid'] = self.usr_id
            data['utime'] = self.getToday(9)
            self.db.update('virtual_conf', data, " id = %s and usr_id=%s " % (sid, self.usr_id_p))
            self.use_log('修改虚拟用户%s' % sid)
        dR = {'code': '', 'MSG': ''}

        dR['code'] = '0'
        dR['MSG'] = '保存成功'
        return dR

    def ajax_edit_data(self):
        id = self.GP('id', '')
        dR = {'code': '', 'MSG': ''}
        sql = """select id,cname,avatar
                from  virtual_conf   
                where usr_id=%s and id=%s
                        """
        d = self.db.fetch(sql, [self.usr_id_p, id])
        if str(d.get('id', '')) != id:
            dR['code'] = '1'
            return
        dR['code'] = '0'
        dR['data'] = d
        return dR

    def oktype_data(self):

        dR = {'code': '', 'MSG': ''}
        sql = """select id
                from  virtual_conf   
                where usr_id=%s 
                        """
        l,t = self.db.select(sql, [self.usr_id_p])
        if t== 0:
            dR['code'] = '1'
            dR['MSG'] = '请先设置促团设置才可以开启到期促团！'
            return
        dR['code'] = '0'
        return dR

    def ajax_del_data(self):
        pk = self.pk
        dR = {'R':'', 'MSG':''}
        self.db.query("update pt_conf set del_flag=1 where id= %s" % pk)
        self.use_log('删除拼团活动%s' % pk)
        self.oPT_GOODS.update(self.usr_id_p,pk)
        dR['MSG']='删除成功'
        return dR

    def Pingtuan_close(self,ptkid, subusr_id):#设为拼团失败
        #print_log('超时关团退款', 'ptkid:%s' % ptkid)
        try:
            sql = "select order_id,ptid,wechat_user_id from open_pt_detail where usr_id=%s and status=1 and opid=%s"
            l, t = self.db.select(sql, [subusr_id, ptkid])
            if t == 0:
                return
            for i in l:
                orderid, ptid, wechat_user_id = i
                self.db.query("update open_pt set status=3 where id=%s and usr_id=%s", [ptkid, subusr_id])
                self.db.query("update open_pt_detail set status=3 where opid=%s and usr_id=%s", [ptkid, subusr_id])

                sqld = """
                                       update wechat_mall_order set 
                                       status=11,status_str='拼团失败' where usr_id=%s and id=%s;
                                        update wechat_mall_order_detail set 
                                       status=11,status_str='拼团失败' where usr_id=%s and order_id=%s; 
                                       """
                self.db.query(sqld, [subusr_id, orderid, subusr_id, orderid])

                self.write_order_log( orderid, '拼团失败', '更新订单状态为拼团失败', '订单id:%s' % orderid)



        except:
            self.print_log('超时关团退款失败ptkid:%s' % ptkid, '%s' % str(traceback.format_exc()))

        return

    def Pingtuan_ok_join(self,ptkid, subusr_id):#设为拼团成功
        #print_log('促团', 'ptkid:%s' % ptkid)
        try:
            sql = "select wechat_user_id,cname,avatar from virtual_conf where usr_id=%s order by id desc"
            lT, iN = self.db.select(sql, [subusr_id])
            if iN == 0:
                return

            sql = "select ptid,order_id,number,short from open_pt where usr_id=%s and id=%s and status=1"
            l, t = self.db.select(sql, [subusr_id, ptkid])
            if t == 0:
                return
            ptid, orderid, number, short = l[0]

            while short > 0:

                ws = random.randint(0, iN - 1)
                wechat_user_id, cname, avatar = lT[ws]
                # self.print_log('number:%s'%number,'short:%s'%short)
                PT_GOODS = self.oPT_GOODS.get(subusr_id, ptid)
                timeout_h = PT_GOODS['timeout_h']
                cnow = datetime.datetime.now()
                # ctime = now.strftime('%Y-%m-%d %H:%M:%S')
                delta = datetime.timedelta(hours=int(timeout_h))
                n_days = cnow + delta
                date_end = n_days.strftime('%Y-%m-%d %H:%M:%S')

                datad = {
                    'usr_id': subusr_id,
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
                self.db.query("update open_pt set short=short-1 where id=%s and usr_id=%s", [ptkid, subusr_id])
                if int(short) == 1:
                    self.db.query("update open_pt set status=2 where id=%s and usr_id=%s", [ptkid, subusr_id])
                    self.db.query("update open_pt_detail set status=2 where opid=%s and usr_id=%s", [ptkid, subusr_id])
                    ############处理订单状态
                    sqlp = "select id,kuaid from wechat_mall_order where usr_id=%s and ptkid=%s and ctype=2"
                    l, t = self.db.select(sqlp, [subusr_id, ptkid])
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
                                self.db.query(sqld, [subusr_id, orderdid, subusr_id, orderdid])
                                self.write_order_log( orderdid, '拼团成功', '更新订单状态为待发货',
                                                '订单id:%s' % orderdid)


                            elif str(kuaid) == '1':  # 自提单
                                sqld = """
                                    update wechat_mall_order set 
                                        status=4,status_str='待自提' where usr_id=%s and id=%s; 
                                    update wechat_mall_order_detail set 
                                        status=4,status_str='待自提' where usr_id=%s and order_id=%s; 
                                    """
                                self.db.query(sqld, [subusr_id, orderdid, subusr_id, orderdid])
                                self.write_order_log(orderdid, '拼团成功', '更新订单状态为待发货',
                                                '订单id:%s' % orderdid)

                            elif str(kuaid) == '2':  # 无须配送
                                sqld = """
                                        update wechat_mall_order set 
                                            status=6,status_str='待评价' where usr_id=%s and id=%s;
                                        update wechat_mall_order_detail set 
                                            status=6,status_str='待评价' where usr_id=%s and order_id=%s; 
                                        """
                                self.db.query(sqld, [subusr_id, orderdid, subusr_id, orderdid])
                                self.write_order_log(orderdid, '拼团成功', '更新订单状态为待发货',
                                                '订单id:%s' % orderdid)

                short = short - 1
        except:

            self.print_log('促团失败ptkid:%s' % ptkid, '%s' % str(traceback.format_exc()))

        return


    def go_ok_data(self):
        id = self.GP('id', '')
        dR = {'code': '', 'MSG': ''}
        sql = """select id
                from  virtual_conf   
                where usr_id=%s 
                        """
        l,t = self.db.select(sql, [self.usr_id_p])
        if t== 0:
            dR['code'] = '1'
            dR['MSG'] = '请先设置促团设置才可以开启到期促团！'
            return
        self.Pingtuan_ok_join(id,self.usr_id_p)
        self.use_log('拼团活动设置为成功%s' %id)
        dR['code'] = '0'
        dR['MSG'] = '已设为拼团成功！'
        return dR

    def go_fail_data(self):
        id = self.GP('id', '')
        dR = {'code': '', 'MSG': ''}
        self.Pingtuan_close(id,self.usr_id_p)
        self.use_log('拼团活动设置为失败%s' % id)
        dR['code'] = '0'
        dR['MSG'] = '已设为拼团失败！'
        return dR