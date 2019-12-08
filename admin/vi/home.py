# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/home.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL


class chome(cBASE_TPL):
    def setClassName(self):
        self.dl_name = 'home_dl'

        
    def goPartList(self):
        self.getBreadcrumb()  # 获取面包屑

        self.assign({
            'user_amount': self.dl.get_wx_users()#用户数量
            , 'goods_amount': self.dl.get_goods_info()#商品数量
            , 'orders_amount': self.dl.get_order_all()#订单总数
            ,'today_order': self.dl.get_today_order() # 今日销售额
            , 'today_views': self.dl.get_today_views()  # 今日浏览量
            , 'orders_status_2':self.dl.get_order_2()  # 未发货订单
            , 'base_me': self.dl.get_base_me()  # 基本信息(小程序信息等)
            , 'goods_sell': self.dl.get_goods_sell()  # 出售中
            , 'sold_out': self.dl.get_sold_out()  # 已下架
            , 'score_warn': self.dl.get_score_warn()  # 库存预警(库存小于5件)
            , 'evaluation': self.dl.get_evaluation()  # 商品评价
            , 'feedback': self.dl.get_feedback()  # 用户反馈
            , 'drawal_audit': self.dl.get_drawal_audit()  # 提现审核
            , 'order_status_1': self.dl.get_order_status_1()  # 待付款
            , 'order_status_10': self.dl.get_order_status_10()  # 拼团中
            , 'order_status_7': self.dl.get_order_status_7()  # 已完成
            , 'order_status_4': self.dl.get_order_status_4()  # 待自提
            , 'order_status_5': self.dl.get_order_status_5()  # 待收货
            , 'order_status_99': self.dl.get_order_status_99()  # 退款中
            , 'order_status_89': self.dl.get_order_status_89()  # 未发货订单
            ,'yesterday_a':self.dl.get_yesterday_a()#昨日销量
            ,'this_month': self.dl.get_this_month()  # 本月销量

        })
        s = self.runApp('home.html')

        return s

    def goPartSync(self):
        dR=self.dl.set_sync_data()
        return self.jsons(dR)

    def goPartVip_db(self):
        dR = self.dl.vip_db_data()
        return self.jsons(dR)

    def goPartCache(self):
        dR=self.dl.cache_data()
        return self.jsons(dR)

    def goPartBuy_vip(self):
        dR = self.dl.buy_vip_data()

        return self.jsons(dR)

    def goPartVip_oss(self):
        dR = self.dl.vip_oss_data()
        return self.jsons(dR)

    def goPartBuy_oss(self):
        dR = self.dl.buy_oss_data()
        return self.jsons(dR)
