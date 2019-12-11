# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) small.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""install.py"""

from config import md5code
import os, sys
from imp import reload
reload(sys)

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
sys.stdout = sys.stderr

from flask import Flask, request,redirect,render_template
from sqlalchemy import *

app=Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTYj'
filename = "{}/dbconfig.py".format(app.root_path)

def create_config(username, password, host,port, dbname):
    data = render_template("config.html",username=username,password=password,host=host,port=port,dbname=dbname)
    fd = open(filename, "w")
    fd.write(data)
    fd.close()

@app.route('/install', methods=['GET', 'POST'])
def install():
    code=0
    if os.path.exists(filename):
        code=3
    return render_template('install.html',code=code)

@app.route('/setup', methods=['GET', 'POST'])
def setup():

    step = request.args.get("step", type=int)
    RES = request.values
    if step == 1:
        return render_template("setup1.html")
    elif step == 2:

        host = RES.get('host','')
        username = RES.get('username','')
        passwd = RES.get('passwd','')
        dbname = RES.get('dbname','')
        port = RES.get('port','')

        url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (username, passwd, host,port,dbname)
        try:
            engine_ = create_engine(url)
            connection = engine_.connect()
        except Exception as e:
            print(e)
            return render_template("setup-error.html", code=3)

        create_config(username, passwd, host, port,dbname)
        if os.path.exists(filename):
            from models.model import createall
            createall(engine_)

            try:  # 增加开启加解密扩展
                connection.execute('create extension pgcrypto;')
            except Exception as e:
                print(e, '开启pgcrypto扩展失败！')
                pass
            return render_template("setup2.html")
        return render_template("setup-error.html", code=3)


    elif step == 3:
        login_id = RES.get('login_id', '')
        passwd = RES.get('passwd', '')
        ctype = RES.get('ctype', '')#0:个人版本,1:SAAS版本,2:B2B2C版本
        from basic.indb import db
        try:

            if ctype=='0':#个人版本
                sql_menu="""
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (8,'系统管理',1,1,10,NULL,NULL,1,'fa-cogs');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (801,'个人帐号',0,2,1,8,'H001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (802,'角色授权',0,2,2,8,'H002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (803,'人员管理',0,2,3,8,'H003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (804,'人员授权',0,2,4,8,'H004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (805,'登录日志',0,2,5,8,'H005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (806,'帐号解锁',0,2,6,8,'H006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (1,'小程序管理',1,1,1,NULL,NULL,1,'fa-link');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (101,'店铺设置',0,2,1,1,'A001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (102,'图片广告',0,2,2,1,'A002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (103,'文字广告',0,2,3,1,'A003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (104,'文章分类',0,2,4,1,'A004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (105,'文章列表',0,2,5,1,'A005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (106,'用户列表',0,2,6,1,'A006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (107,'用户反馈',0,2,7,1,'A007',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (108,'收货地址',0,2,8,1,'A008',1,NULL);
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,img)values(2,'公众号管理',1,1,2,1,'fa-wechat');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(201,'基本设置',0,2,1,1,2,'seetting');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(202,'菜单管理',0,2,2,1,2,'menu');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(203,'文字回复',0,2,3,1,2,'basic');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(204,'特殊回复',0,2,4,1,2,'sp_reply');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(205,'粉丝列表',0,2,5,1,2,'fans');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (3,'商品管理',1,1,4,NULL,NULL,1,'fa-shopping-bag');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (301,'商品分类',0,2,1,3,'C001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (302,'商品规格',0,2,2,3,'C002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (303,'商品品牌',0,2,3,3,'C003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (304,'商品档案',0,2,4,3,'C004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (305,'商品评价',0,2,5,3,'C005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (306,'商品热销榜',0,2,6,3,'C006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (307,'商品反馈',0,2,7,3,'C007',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (4,'营销中心',1,1,5,NULL,NULL,1,'fa-gift');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (401,'优惠券',0,2,1,4,'D001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (403,'拼团活动',0,2,3,4,'D003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (5,'订单管理',1,1,6,NULL,NULL,1,'fa-file-text-o');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (501,'销售订单',0,2,1,5,'E001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (503,'退款订单',0,2,3,5,'E003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (504,'售后订单',0,2,4,5,'E004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (6,'综合查询',1,1,7,NULL,NULL,1,'fa-search');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (601,'优惠券查询',0,2,1,6,'F001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (602,'充值查询',0,2,2,6,'F002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (603,'返现查询',0,2,3,6,'F003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (604,'消费查询',0,2,4,6,'F004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (605,'会员升级查询',0,2,5,6,'F005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (609,'图片查询',0,2,9,6,'F009',1,NULL);
                
                """
            elif ctype == '1':#SAAS版本
                sql_menu = """
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (8,'系统管理',1,1,10,NULL,NULL,1,'fa-cogs');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (801,'个人帐号',0,2,1,8,'H001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (802,'角色授权',0,2,2,8,'H002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (803,'人员管理',0,2,3,8,'H003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (804,'人员授权',0,2,4,8,'H004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (805,'登录日志',0,2,5,8,'H005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (806,'帐号解锁',0,2,6,8,'H006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (9,'平台管理',1,1,11,NULL,NULL,1,'fa-cubes');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (901,'平台设置',0,2,1,9,'I001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (1,'小程序管理',1,1,1,NULL,NULL,1,'fa-link');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (101,'店铺设置',0,2,1,1,'A001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (102,'图片广告',0,2,2,1,'A002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (103,'文字广告',0,2,3,1,'A003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (104,'文章分类',0,2,4,1,'A004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (105,'文章列表',0,2,5,1,'A005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (106,'用户列表',0,2,6,1,'A006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (107,'用户反馈',0,2,7,1,'A007',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (108,'收货地址',0,2,8,1,'A008',1,NULL);
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,img)values(2,'公众号管理',1,1,2,1,'fa-wechat');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(201,'基本设置',0,2,1,1,2,'seetting');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(202,'菜单管理',0,2,2,1,2,'menu');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(203,'文字回复',0,2,3,1,2,'basic');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(204,'特殊回复',0,2,4,1,2,'sp_reply');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(205,'粉丝列表',0,2,5,1,2,'fans');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (3,'商品管理',1,1,4,NULL,NULL,1,'fa-shopping-bag');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (301,'商品分类',0,2,1,3,'C001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (302,'商品规格',0,2,2,3,'C002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (303,'商品品牌',0,2,3,3,'C003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (304,'商品档案',0,2,4,3,'C004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (305,'商品评价',0,2,5,3,'C005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (306,'商品热销榜',0,2,6,3,'C006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (307,'商品反馈',0,2,7,3,'C007',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (4,'营销中心',1,1,5,NULL,NULL,1,'fa-gift');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (401,'优惠券',0,2,1,4,'D001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (403,'拼团活动',0,2,3,4,'D003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (5,'订单管理',1,1,6,NULL,NULL,1,'fa-file-text-o');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (501,'销售订单',0,2,1,5,'E001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (503,'退款订单',0,2,3,5,'E003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (504,'售后订单',0,2,4,5,'E004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (6,'综合查询',1,1,7,NULL,NULL,1,'fa-search');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (601,'优惠券查询',0,2,1,6,'F001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (602,'充值查询',0,2,2,6,'F002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (603,'返现查询',0,2,3,6,'F003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (604,'消费查询',0,2,4,6,'F004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (605,'会员升级查询',0,2,5,6,'F005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (609,'图片查询',0,2,9,6,'F009',1,NULL);

                """
            else:#B2B2C版本
                sql_menu = """
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (8,'系统管理',1,1,10,NULL,NULL,1,'fa-cogs');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (801,'个人帐号',0,2,1,8,'H001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (802,'角色授权',0,2,2,8,'H002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (803,'人员管理',0,2,3,8,'H003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (804,'人员授权',0,2,4,8,'H004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (805,'登录日志',0,2,5,8,'H005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (806,'帐号解锁',0,2,6,8,'H006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (1,'小程序管理',1,1,1,NULL,NULL,1,'fa-link');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (101,'店铺设置',0,2,1,1,'A001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (102,'图片广告',0,2,2,1,'A002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (103,'文字广告',0,2,3,1,'A003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (104,'文章分类',0,2,4,1,'A004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (105,'文章列表',0,2,5,1,'A005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (106,'用户列表',0,2,6,1,'A006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (107,'用户反馈',0,2,7,1,'A007',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (108,'收货地址',0,2,8,1,'A008',1,NULL);
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,img)values(2,'公众号管理',1,1,2,1,'fa-wechat');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(201,'基本设置',0,2,1,1,2,'seetting');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(202,'菜单管理',0,2,2,1,2,'menu');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(203,'文字回复',0,2,3,1,2,'basic');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(204,'特殊回复',0,2,4,1,2,'sp_reply');
                insert into menu_func(menu_id,menu_name,vtype,menu,sort,status,parent_id,func_id)values(205,'粉丝列表',0,2,5,1,2,'fans');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (3,'商品管理',1,1,4,NULL,NULL,1,'fa-shopping-bag');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (301,'商品分类',0,2,1,3,'C001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (302,'商品规格',0,2,2,3,'C002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (303,'商品品牌',0,2,3,3,'C003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (304,'商品档案',0,2,4,3,'C004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (305,'商品评价',0,2,5,3,'C005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (306,'商品热销榜',0,2,6,3,'C006',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (307,'商品反馈',0,2,7,3,'C007',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (4,'营销中心',1,1,5,NULL,NULL,1,'fa-gift');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (401,'优惠券',0,2,1,4,'D001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (403,'拼团活动',0,2,3,4,'D003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (5,'订单管理',1,1,6,NULL,NULL,1,'fa-file-text-o');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (501,'销售订单',0,2,1,5,'E001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (503,'退款订单',0,2,3,5,'E003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (504,'售后订单',0,2,4,5,'E004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (6,'综合查询',1,1,7,NULL,NULL,1,'fa-search');
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (601,'优惠券查询',0,2,1,6,'F001',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (602,'充值查询',0,2,2,6,'F002',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (603,'返现查询',0,2,3,6,'F003',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (604,'消费查询',0,2,4,6,'F004',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (605,'会员升级查询',0,2,5,6,'F005',1,NULL);
                INSERT INTO public.menu_func (menu_id,menu_name,vtype,menu,sort,parent_id,func_id,status,img) VALUES (609,'图片查询',0,2,9,6,'F009',1,NULL);

                """
            db.query(sql_menu)

            sql_mtc_t="""
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (1,'YESNO','是',NULL,NULL,0,1,NULL,NULL,NULL,NULL)
                ,(0,'YESNO','否',NULL,NULL,0,2,NULL,NULL,NULL,NULL)
                ,(2,'JZLX','领取N天后到期','截止类型',NULL,0,2,NULL,NULL,NULL,NULL)
                ,(1,'JZLX','填写固定截止时间','截止类型',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(1,'ZFZSGZ','注册送','积分赠送规则',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(2,'ZFZSGZ','消费送','积分赠送规则',NULL,0,2,NULL,NULL,NULL,NULL)
                ,(3,'ZFZSGZ','好评送','积分赠送规则',NULL,0,3,NULL,NULL,NULL,NULL)
                ,(3,'DDZT','待评价','订单状态',NULL,0,3,NULL,NULL,NULL,NULL)
                ,(4,'DDZT','已完成','订单状态',NULL,0,4,NULL,NULL,NULL,NULL)
                ,(5,'DDZT','已关闭','订单状态',NULL,0,5,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (1,'KD','SF','顺丰速运',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(2,'KD','HTKY','百世快递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(3,'KD','ZTO','中通快递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(4,'KD','STO','申通快递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(5,'KD','YTO','圆通速递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(6,'KD','YD','韵达速递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(7,'KD','YZPY','邮政快递包裹',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(8,'KD','EMS','EMS',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(9,'KD','HHTT','天天快递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(10,'KD','JD','京东快递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(11,'KD','UC','优速快递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(12,'KD','DBL','德邦快递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(13,'KD','ZJS','宅急送',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(14,'KD','TNT','TNT快递',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (15,'KD','UPS','UPS',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(16,'KD','DHL','DHL',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(17,'KD','FEDEX','FEDEX联邦(国内件)',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(18,'KD','FEDEX_GJ','FEDEX联邦(国际件)',NULL,0,1,1,'2018-12-06 10:53:42.993',NULL,NULL)
                ,(18,'KD','AJ','安捷快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(19,'KD','ALKJWL','阿里跨境电商物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(20,'KD','AX','安讯物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(21,'KD','AYUS','安邮美国',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(22,'KD','AMAZON','亚马逊物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(23,'KD','AOMENYZ','澳门邮政',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (24,'KD','ANE','安能物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(25,'KD','ADD','澳多多',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(26,'KD','AYCA','澳邮专线',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(27,'KD','AXD','安鲜达',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(28,'KD','ANEKY','安能快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(29,'KD','BDT','八达通',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(30,'KD','BETWL','百腾物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(31,'KD','BJXKY','北极星快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(32,'KD','BNTWL','奔腾物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(33,'KD','BFDF','百福东方',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (34,'KD','BHGJ','贝海国际',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(35,'KD','BFAY','八方安运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(36,'KD','BTWL','百世快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(37,'KD','CFWL','春风物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(38,'KD','CHTWL','诚通物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(39,'KD','CXHY','传喜物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(40,'KD','CG','程光',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(41,'KD','CITY100','城市100',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(42,'KD','CJKD','城际快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(43,'KD','CNPEX','CNPEX中邮快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (44,'KD','COE','COE东方快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(45,'KD','CSCY','长沙创一',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(46,'KD','CDSTKY','成都善途速运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(47,'KD','CTG','联合运通',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(48,'KD','CRAZY','疯狂快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(49,'KD','CBO','CBO钏博物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(50,'KD','CND','承诺达',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(51,'KD','DSWL','D速物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(52,'KD','DLG','到了港',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(53,'KD','DTWL','大田物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (54,'KD','DJKJWL','东骏快捷物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(55,'KD','DEKUN','德坤',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(56,'KD','DBLKY','德邦快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(57,'KD','ETK','E特快',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(58,'KD','EWE','EWE',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(59,'KD','FKD','飞康达',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(60,'KD','FTD','富腾达',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(61,'KD','FYKD','凡宇货的',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(62,'KD','FASTGO','速派快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(63,'KD','FT','丰通快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (64,'KD','GD','冠达',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(65,'KD','GTO','国通快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(66,'KD','GDEMS','广东邮政',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(67,'KD','GSD','共速达',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(68,'KD','GTONG','广通',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(69,'KD','GAI','迦递快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(70,'KD','GKSD','港快速递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(71,'KD','GTSD','高铁速递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(72,'KD','HFWL','汇丰物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(73,'KD','HGLL','黑狗冷链',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (74,'KD','HLWL','恒路物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(75,'KD','HOAU','天地华宇',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(76,'KD','HOTSCM','鸿桥供应链',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(77,'KD','HPTEX','海派通物流公司',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(78,'KD','hq568','华强物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(79,'KD','HQSY','环球速运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(80,'KD','HXLWL','华夏龙物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(81,'KD','HXWL','豪翔物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(82,'KD','HFHW','合肥汇文',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(83,'KD','HLONGWL','辉隆物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (84,'KD','HQKD','华企快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(85,'KD','HRWL','韩润物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(86,'KD','HTKD','青岛恒通快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(87,'KD','HYH','货运皇物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(88,'KD','HYLSD','好来运快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(89,'KD','HJWL','皇家物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(90,'KD','JAD','捷安达',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(91,'KD','JGSD','京广速递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(92,'KD','JIUYE','九曳供应链',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(93,'KD','JXD','急先达',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (94,'KD','JYKDD','晋越快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(95,'KD','JYM','加运美',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(96,'KD','JGWL','景光物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(97,'KD','JYWL','佳怡物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(98,'KD','JDKY','京东快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(99,'KD','KFW','快服务',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(100,'KD','KYSY','跨越速运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(101,'KD','KYWL','跨越物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(102,'KD','KSDWL','快速递物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(103,'KD','KBSY','快8速运',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (104,'KD','LB','龙邦快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(105,'KD','LJSKD','立即送',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(106,'KD','LHT','联昊通速递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(107,'KD','MB','民邦快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(108,'KD','MHKD','民航快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(109,'KD','MK','美快',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(110,'KD','MDM','门对门快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(111,'KD','MRDY','迈隆递运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(112,'KD','MLWL','明亮物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(113,'KD','NF','南方',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (114,'KD','NEDA','能达速递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(115,'KD','PADTF','平安达腾飞快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(116,'KD','PANEX','泛捷快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(117,'KD','PJ','品骏快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(118,'KD','PCA','PCA Express',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(119,'KD','UAPEX','全一快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(120,'KD','QCKD','全晨快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(121,'KD','QRT','全日通快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(122,'KD','QUICK','快客快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(123,'KD','QXT','全信通',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (124,'KD','RQ','荣庆物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(125,'KD','RFD','如风达',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(126,'KD','RRS','日日顺物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(127,'KD','RFEX','瑞丰速递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(128,'KD','SAD','赛澳递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(129,'KD','SNWL','苏宁物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(130,'KD','SAWL','圣安物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(131,'KD','SBWL','晟邦物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(132,'KD','SDWL','上大物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(133,'KD','SFWL','盛丰物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (134,'KD','ST','速通物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(135,'KD','STWL','速腾快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(136,'KD','SUBIDA','速必达物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(137,'KD','SDEZ','速递e站',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(138,'KD','SCZPDS','速呈宅配',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(139,'KD','SURE','速尔快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(140,'KD','TAIWANYZ','台湾邮政',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(141,'KD','TSSTO','唐山申通',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(142,'KD','TJS','特急送',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(143,'KD','TYWL','通用物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (144,'KD','ULUCKEX','优联吉运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(145,'KD','UEQ','UEQ Express',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(146,'KD','WJK','万家康',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(147,'KD','WJWL','万家物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(148,'KD','WHTZX','武汉同舟行',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(149,'KD','WPE','维普恩',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(150,'KD','WXWL','万象物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(151,'KD','WTP','微特派',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(152,'KD','WTWL','温通物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(153,'KD','XCWL','迅驰物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (154,'KD','XFEX','信丰物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(155,'KD','XYT','希优特',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(156,'KD','XJ','新杰物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(157,'KD','YADEX','源安达快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(158,'KD','YCWL','远成物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(159,'KD','YCSY','远成快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(160,'KD','YDH','义达国际物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(161,'KD','YDT','易达通',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(162,'KD','YFHEX','原飞航物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(163,'KD','YFSD','亚风快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (164,'KD','YTKD','运通快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(165,'KD','YXKD','亿翔快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(166,'KD','YUNDX','运东西网',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(167,'KD','YMDD','壹米滴答',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(168,'KD','YZBK','邮政国内标快',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(169,'KD','YZTSY','一站通速运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(170,'KD','YFSUYUN','驭丰速运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(171,'KD','YSDF','余氏东风',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(172,'KD','YF','耀飞快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(173,'KD','YDKY','韵达快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (174,'KD','ZENY','增益快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(175,'KD','ZHQKD','汇强快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(176,'KD','ZTE','众通快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(177,'KD','ZTKY','中铁快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(178,'KD','ZTWL','中铁物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(179,'KD','SJ','郑州速捷',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(180,'KD','ZTOKY','中通快运',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(181,'KD','ZYKD','中邮快递',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(182,'KD','WM','中粮我买网',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(183,'KD','ZMKM','芝麻开门',NULL,0,1,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (184,'KD','ZHWL','中骅物流',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(1,'t_type','新人团','拼团类型',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(2,'t_type','老用户团','拼团类型',NULL,0,2,NULL,NULL,NULL,NULL)
                ,(3,'t_type','新老用户团','拼团类型',NULL,0,3,NULL,NULL,NULL,NULL)
                ,(0,'KD','ZITI','商家配送',NULL,0,1,1,'2019-03-04 15:22:59.432',NULL,NULL)
                ,(0,'SEX','未知',NULL,1,0,1,NULL,NULL,NULL,NULL)
                ,(1,'SEX','男',NULL,1,0,1,NULL,NULL,NULL,NULL)
                ,(2,'SEX','女',NULL,1,0,2,NULL,NULL,NULL,NULL)
                ,(1,'RSXZT','已开启',NULL,1,0,1,NULL,NULL,NULL,NULL)
                ,(2,'RSXZT','未开启',NULL,1,0,2,NULL,NULL,NULL,NULL)
                ;
                INSERT INTO public.mtc_t (id,"type",txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (3,'RSXZT','已结束',NULL,1,0,3,NULL,NULL,NULL,NULL)
                ,(1,'VIPUP','付费升级','会员设置的会员升级方式',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(2,'VIPUP','购物升级','会员设置的会员升级方式',NULL,0,2,NULL,NULL,NULL,NULL)
                ,(0,'ALL','全部商品','全局设置的推荐商品设置',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(1,'ALL','全部推荐商品','全局设置的推荐商品设置',NULL,0,2,NULL,NULL,NULL,NULL)
                ,(2,'ALL','指定商品','全局设置的推荐商品设置',NULL,0,3,NULL,NULL,NULL,NULL)
                ,(1,'TAG','会员','用户标签',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(2,'TAG','代理','用户标签',NULL,0,2,NULL,NULL,NULL,NULL)
                ,(3,'TAG','大客户','用户标签',NULL,0,3,NULL,NULL,NULL,NULL)
                ,(4,'TAG','批发','用户标签',NULL,0,4,NULL,NULL,NULL,NULL)
                ,(5,'TAG','连锁','用户标签',NULL,0,5,NULL,NULL,NULL,NULL)
                ;
        
            """
            db.query(sql_mtc_t)

            fu1="""
                CREATE OR REPLACE FUNCTION public.p_getmenurightlist(id integer)
                 RETURNS TABLE(t_menu_id integer, t_menu_name character varying, t_menu integer, t_type integer, t_sort integer, t_parent_id integer, t_can_see integer, t_can_add integer, t_can_upd integer, t_can_del integer, status integer)
                 LANGUAGE plpgsql
                AS $function$
                    
                DECLARE
                    tmp_lev1Id int;     
                        lev1Count int;    
                           
                        tmp_lev2Id int;     
                        lev2Count int;    
                             
                        tmp_lev3Id int;     
                        lev3Count int; 
                
                    lev1sql text;
                    
                BEGIN
                    CREATE TEMP TABLE if not exists tb(t_menu_id int,t_menu_name varchar(100),t_menu int,t_type int,t_sort int,t_parent_id int,t_can_see int,t_can_add int,t_can_upd int,t_can_del int,status int) on commit drop;
                    
                    TRUNCATE table tb;
                    
                    tmp_lev1Id := 0;
                    lev1Count := 0;
                   
                    select COUNT(1) INTO lev1Count from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 where m.menu=1 and m.menu_id not in (select c.menu_id from menu_func c where c.menu in (2,3) and  COALESCE(c.parent_id,0)=0 );
                    
                    WHILE lev1Count > 0 LOOP
                        begin		--COALESCE(c.parent_id,0)=0
                            
                         
                            select m.menu_id INTO tmp_lev1Id from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 where m.menu = 1 and m.menu_id not in (select c.menu_id from menu_func c where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ) and m.menu_id not in (select t.t_menu_id from tb t) order by COALESCE(m.sort,null),COALESCE(m.menu_id,null) LIMIT 1;
                
                          
                            insert into tb     
                                 select m.menu_id,m.menu_name,m.menu,m.vtype,COALESCE(m.sort,null)sort,COALESCE(m.parent_id,null)parent_id,COALESCE(r.can_see,null)can_see,COALESCE(r.can_add,null)can_add,COALESCE(r.can_upd,null)can_upd,COALESCE(r.can_del,null)can_del,m.status
                                from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 where m.menu = 1 and m.menu_id = tmp_lev1Id and m.menu_id not in (select c.menu_id from menu_func c where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ); 
                            
                            --一级菜单正常-----
                            
                            begin
                                tmp_lev2Id := 0;    
                                lev2Count := 0;
                
                                select COUNT(1) INTO lev2Count from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 
                                    where m.menu=2 and m.parent_id = tmp_lev1Id and m.menu_id not in (select c.menu_id from menu_func c     
                                    where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 );
                                    
                                while lev2Count > 0 loop
                                    
                                    begin
                                       
                                        select (select m.menu_id INTO tmp_lev2Id from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1    
                                            where m.menu = 2 and m.parent_id = tmp_lev1Id and m.menu_id not in (select c.menu_id from menu_func c     
                                            where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ) and m.menu_id not in (select t.t_menu_id from tb t)     
                                            order by COALESCE(m.sort,null),COALESCE(m.menu_id,null) LIMIT 1);
                                       
                                        ---------
                                       
                                        insert into tb
                                            select m.menu_id,m.menu_name,m.menu,m.vtype,COALESCE(m.sort,null) sort,COALESCE(m.parent_id,null) parent_id,COALESCE(r.can_see,null) can_see,COALESCE(r.can_add,null) can_add,COALESCE(r.can_upd,null) can_upd,COALESCE(r.can_del,null) can_del,m.status 
                                            from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 where m.menu =2 and m.menu_id = tmp_lev2Id and m.menu_id not in (select c.menu_id from menu_func c where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ); 
                                        ---二级菜单正常
                                        begin
                                            tmp_lev3Id := 0;    
                                            lev3Count := 0;    
                                           
                                            select COUNT(1) INTO lev3Count from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1    
                                                where m.menu=3 and m.parent_id = tmp_lev2Id and m.menu_id not in (select c.menu_id from menu_func c     
                                                where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 );
                
                                            while lev3Count > 0 loop
                                                begin
                                                   
                                                    /**/
                                                    select m.menu_id INTO tmp_lev3Id from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1    
                                                        where m.menu = 3 and m.parent_id = tmp_lev2Id and m.menu_id not in (select c.menu_id from menu_func c     
                                                        where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ) and m.menu_id not in (select t.t_menu_id from tb t)    
                                                        order by COALESCE(m.sort,null),COALESCE(m.menu_id,null) LIMIT 1 ;
                                                    
                
                
                                                    
                                                    insert into tb    
                                                        select m.menu_id,m.menu_name,m.menu,m.vtype,COALESCE(m.sort,null) sort,COALESCE(m.parent_id,null) parent_id,COALESCE(r.can_see,null) can_see,COALESCE(r.can_add,null) can_add,COALESCE(r.can_upd,null) can_upd,COALESCE(r.can_del,null) can_del,m.status  
                                                        from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1   
                                                        where m.menu =3 and m.menu_id = tmp_lev3Id and m.menu_id not in (select c.menu_id from menu_func c     
                                                        where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 );
                
                                                    lev3Count := lev3Count-1;
                                                end;
                                                
                                            end loop;
                                        
                                        end;
                                        
                                        --二级菜单
                                        lev2Count := lev2Count-1;
                                    end;
                                    
                                    
                                end loop;
                
                                
                            end;
                                
                            ----一级菜单正常--
                        end;
                        lev1Count := lev1Count-1;
                        
                    END LOOP;
                    return query 
                    select * from tb;
                    
                END
                $function$
                ;
            
            
            """
            db.query(fu1)
            fu2="""
                CREATE OR REPLACE FUNCTION public.p_save_rolemenu(role_id integer, see_str character varying, add_str character varying, del_str character varying, upd_str character varying, optuserid integer)
                 RETURNS void
                 LANGUAGE plpgsql
                AS $function$
                    
                DECLARE
                    new_cid int;  
                        new_uid int;  
                        new_ctime timestamp;
                        new_utime timestamp;
                    t_count_roleMenu int;  
                    id int;
                    test int;
              
                BEGIN
                    id :=role_id;
                    t_count_roleMenu := 0;  
                    new_cid := 0;  
                    new_uid := 0;  
                    new_ctime := now();  
                    new_utime := now();
                    
                    CREATE TEMP TABLE if not exists tb(t_menu_id int,t_can_see int default 0,t_can_add int default 0,t_can_del int default 0,t_can_upd int default 0  ) ON COMMIT DROP;
                    TRUNCATE table tb;
                    
                    BEGIN
                        --将需要操作的menu都放入临时表变量  
                          
                           insert into tb(t_menu_id)(select regexp_split_to_table(see_str,',')::integer  
                            union  
                            select regexp_split_to_table(add_str,',')::integer  
                            union  
                            select regexp_split_to_table(del_str,',')::integer  
                            union  
                            select regexp_split_to_table(upd_str,',')::integer);
                            
                              -- 这些menu的上级和上上级都应该加入权限里面去  
                        
                            insert into tb(select COALESCE(parent_id,null) ,0 ,0 ,0 ,0 from menu_func where menu_id in (select t.t_menu_id from tb t)  
                            union  
                            select COALESCE(parent_id,null) ,0 ,0 ,0 ,0 from menu_func where menu_id in (select parent_id from menu_func where menu_id in (select t.t_menu_id from tb t) ));  
                        --先将多余的空数据删除  
                        delete from tb where t_menu_id = 0;
                     
                        --然后update 查询权限情况到临时表变量  
                        update tb set t_can_see = 1 where t_menu_id in ( select  regexp_split_to_table(see_str,',')::integer );
                     
                           --然后update 查询权限情况到临时表变量  
                        update tb set t_can_add = 1 where t_menu_id in ( select regexp_split_to_table(add_str,',')::integer ); 
                             
                           --然后update 查询权限情况到临时表变量  
                        update tb set t_can_del = 1 where t_menu_id in ( select regexp_split_to_table(del_str,',')::integer ); 
                             
                           --然后update 查询权限情况到临时表变量  
                        update tb set t_can_upd = 1 where t_menu_id in ( select regexp_split_to_table(upd_str,',')::integer );
                        
                        select COUNT(1) INTO t_count_roleMenu from role_menu r where r.role_id = $1 ;
                
                        if t_count_roleMenu > 0 then -- 如果是update 模式  
                            begin  
                             -- update模式的话，原有的cid，ctime需要保留下来，uid ，是operUserId，utime是当前时间 
                            select   COALESCE(MAX(r.cid),null)  ,COALESCE(MAX(r.ctime),null) ,$6 ,now() INTO new_cid,new_ctime,new_uid,new_utime from role_menu r where r.role_id = $1 LIMIT 1;
                            end;  
                        else                      -- 否则是create 模式  
                               begin  
                                --create 模式的话，cid 是 oprUserId，ctime 是 当前时间，uid ，是 Null，utime是null  
                                 new_cid := optUserId;  
                                 new_ctime := now();  
                                 new_uid := optUserId;  
                                 new_utime := now();  
                               end; 
                        end if;
                    
                        
                        --然后动手吧，把role_menu 的数据处理掉，然后将新的放进去  
                        delete from role_menu r where r.role_id = $1;
        
                        insert into role_menu(role_id, menu_id, can_see, can_add, can_del, can_upd, cid, ctime, uid, utime)  
                           (select $1, COALESCE(t_menu_id,0), t_can_see, t_can_add, t_can_del, t_can_upd, new_cid, new_ctime,new_uid,new_utime from tb);
                    END;
                END;
                $function$
                ;
            """
            db.query(fu2)
            fu3 = """
                CREATE OR REPLACE FUNCTION public.p_getmenurightlist_s(id integer)
                 RETURNS TABLE(t_menu_id integer, t_menu_name character varying, t_menu integer, t_type integer, t_sort integer, t_parent_id integer, t_can_see integer, t_can_add integer, t_can_upd integer, t_can_del integer, status integer)
                 LANGUAGE plpgsql
                AS $function$

                DECLARE
                    tmp_lev1Id int;     
                        lev1Count int;    

                        tmp_lev2Id int;     
                        lev2Count int;    

                        tmp_lev3Id int;     
                        lev3Count int; 

                    lev1sql text;



                BEGIN
                    CREATE TEMP TABLE if not exists tb(t_menu_id int,t_menu_name varchar(100),t_menu int,t_type int,t_sort int,t_parent_id int,t_can_see int,t_can_add int,t_can_upd int,t_can_del int,status int) on commit drop;

                    TRUNCATE table tb;

                    tmp_lev1Id := 0;
                    lev1Count := 0;

                    select COUNT(1) INTO lev1Count from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 where m.menu=1 and m.status=1 and m.menu_id not in (select c.menu_id from menu_func c where c.menu in (2,3) and  COALESCE(c.parent_id,0)=0 );

                    WHILE lev1Count > 0 LOOP
                        begin		


                            select m.menu_id INTO tmp_lev1Id from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 where m.menu = 1 and m.status=1 and m.menu_id not in (select c.menu_id from menu_func c where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ) and m.menu_id not in (select t.t_menu_id from tb t) order by COALESCE(m.sort,null),COALESCE(m.menu_id,null) LIMIT 1;


                            insert into tb     
                                 select m.menu_id,m.menu_name,m.menu,m.vtype,COALESCE(m.sort,null)sort,COALESCE(m.parent_id,null)parent_id,COALESCE(r.can_see,null)can_see,COALESCE(r.can_add,null)can_add,COALESCE(r.can_upd,null)can_upd,COALESCE(r.can_del,null)can_del,m.status
                                from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 where m.menu = 1 and m.status=1 and m.menu_id = tmp_lev1Id and m.menu_id not in (select c.menu_id from menu_func c where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ); 

                            --一级菜单正常-----

                            begin
                                tmp_lev2Id := 0;    
                                lev2Count := 0;


                                select COUNT(1) INTO lev2Count from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 
                                    where m.menu=2 and m.status=1 and m.parent_id = tmp_lev1Id and m.menu_id not in (select c.menu_id from menu_func c     
                                    where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 );

                                while lev2Count > 0 loop

                                    begin

                                        select (select m.menu_id INTO tmp_lev2Id from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1    
                                            where m.menu = 2 and m.status=1 and m.parent_id = tmp_lev1Id and m.menu_id not in (select c.menu_id from menu_func c     
                                            where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ) and m.menu_id not in (select t.t_menu_id from tb t)     
                                            order by COALESCE(m.sort,null),COALESCE(m.menu_id,null) LIMIT 1);

                                        insert into tb
                                            select m.menu_id,m.menu_name,m.menu,m.vtype,COALESCE(m.sort,null) sort,COALESCE(m.parent_id,null) parent_id,COALESCE(r.can_see,null) can_see,COALESCE(r.can_add,null) can_add,COALESCE(r.can_upd,null) can_upd,COALESCE(r.can_del,null) can_del,m.status 
                                            from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1 where m.menu =2 and m.status=1 and m.menu_id = tmp_lev2Id and m.menu_id not in (select c.menu_id from menu_func c where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ); 
                                        ---二级菜单正常
                                        begin
                                            tmp_lev3Id := 0;    
                                            lev3Count := 0;    

                                            select COUNT(1) INTO lev3Count from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1    
                                                where m.menu=3 and m.status=1 and m.parent_id = tmp_lev2Id and m.menu_id not in (select c.menu_id from menu_func c     
                                                where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 );

                                            while lev3Count > 0 loop
                                                begin

                                                    /**/
                                                    select m.menu_id INTO tmp_lev3Id from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1    
                                                        where m.menu = 3 and m.status=1 and m.parent_id = tmp_lev2Id and m.menu_id not in (select c.menu_id from menu_func c     
                                                        where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 ) and m.menu_id not in (select t.t_menu_id from tb t)    
                                                        order by COALESCE(m.sort,null),COALESCE(m.menu_id,null) LIMIT 1 ;

                                                    insert into tb    
                                                        select m.menu_id,m.menu_name,m.menu,m.vtype,COALESCE(m.sort,null) sort,COALESCE(m.parent_id,null) parent_id,COALESCE(r.can_see,null) can_see,COALESCE(r.can_add,null) can_add,COALESCE(r.can_upd,null) can_upd,COALESCE(r.can_del,null) can_del,m.status  
                                                        from menu_func m left join role_menu r on m.menu_id = r.menu_id and r.role_id=$1   
                                                        where m.menu =3 and m.status=1 and m.menu_id = tmp_lev3Id and m.menu_id not in (select c.menu_id from menu_func c     
                                                        where c.menu in (2,3) and COALESCE(c.parent_id,0)=0 );

                                                    lev3Count := lev3Count-1;
                                                end;

                                            end loop;

                                        end;

                                        --二级菜单
                                        lev2Count := lev2Count-1;
                                    end;


                                end loop;


                            end;

                            ----一级菜单正常--
                        end;
                        lev1Count := lev1Count-1;

                    END LOOP;
                    return query 
                    select * from tb;

                END
                $function$
                ;
            """
            db.query(fu3)
            fu4 = """

                CREATE OR REPLACE FUNCTION public.func_rolename(a integer)
                 RETURNS character varying
                 LANGUAGE plpgsql
                AS $function$
                declare r text;
                BEGIN 
                    r := null;
                    select r.role_name
                    from usr_role ur
                    left join roles r on r.role_id = ur.role_id
                    where ur.usr_id = a INTO r;
                    return r;
                END 
                $function$
                ;
                """
            db.query(fu4)
            l,t = db.select("SELECT usr_id FROM users WHERE usr_id=1;")
            if t>0:
                sql="""update users set login_id=encrypt(%s,%s,'aes'),status=1,
                    passwd= crypt(%s, gen_salt('md5')) where usr_id=1;"""
                db.query(sql,[login_id,md5code,passwd])

                return render_template('setup.html',code=0)
            sql = """insert into users(login_id,passwd,status)values(encrypt(%s,%s,'aes'),crypt(%s, gen_salt('md5')),1);
                    """
            db.query(sql,[login_id, md5code,passwd])
            return render_template('setup.html',code=0)
        except Exception as e:
            print(e,'eeee')
            return render_template('setup.html', code=3)
    return render_template('install.html')



@app.route('/', methods=['GET', 'POST'])
def start():
    if not os.path.exists(filename):
        return redirect('/install')
    return render_template('ok.html')



if __name__ == '__main__':
    app.run(port=5001)
    #app.run(host='0.0.0.0', port=5001,debug=True)




