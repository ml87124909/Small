# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
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
#


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
        except:
            return render_template("setup-error.html", code=3)

        create_config(username, passwd, host, port,dbname)
        if os.path.exists(filename):
            from models.model import createall
            createall(engine_)
            return render_template("setup2.html")
        return render_template("setup-error.html", code=3)


    elif step == 3:
        login_id = RES.get('login_id', '')
        passwd = RES.get('passwd', '')
        try:
            from models.model import DBSession,users as  User
            session = DBSession()
            result =session.execute("SELECT usr_id FROM users WHERE usr_id=1;")
            row=result.fetchone()
            try:
                sql_del="""
                    delete from menu_func
                """
                session.execute(sql_del)
                session.commit()
            except:
                pass
            sql_menu="""
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (8,'系统管理',1,1,10,NULL,NULL,1,'fa-cogs');
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (801,'个人帐号',0,2,1,8,'H001',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (805,'登录日志',0,2,5,8,'H005',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (806,'帐号解锁',0,2,6,8,'H006',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (1,'小程序管理',1,1,1,NULL,NULL,1,'fa-link');
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (101,'店铺设置',0,2,1,1,'A001',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (102,'图片广告',0,2,2,1,'A002',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (103,'文字广告',0,2,3,1,'A003',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (104,'文章分类',0,2,4,1,'A004',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (105,'文章列表',0,2,5,1,'A005',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (106,'用户列表',0,2,6,1,'A006',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (2,'用户画像',1,1,3,NULL,NULL,1,'fa-address-card-o');
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (202,'用户标签',0,2,2,2,'B002',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (203,'模板推送',0,2,3,2,'B003',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (204,'收货地址',0,2,4,2,'B004',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (3,'商品管理',1,1,4,NULL,NULL,1,'fa-shopping-bag');
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (301,'商品分类',0,2,1,3,'C001',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (302,'商品规格',0,2,2,3,'C002',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (303,'商品品牌',0,2,3,3,'C003',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (304,'商品档案',0,2,4,3,'C004',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (305,'商品评价',0,2,5,3,'C005',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (306,'商品热销榜',0,2,6,3,'C006',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (307,'商品反馈',0,2,7,3,'C007',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (4,'营销中心',1,1,5,NULL,NULL,1,'fa-gift');
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (401,'优惠券',0,2,1,4,'D001',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (403,'拼团活动',0,2,3,4,'D003',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (5,'订单管理',1,1,6,NULL,NULL,1,'fa-file-text-o');
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (501,'销售订单',0,2,1,5,'E001',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (503,'退款订单',0,2,3,5,'E003',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (504,'售后订单',0,2,4,5,'E004',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (6,'综合查询',1,1,7,NULL,NULL,1,'fa-search');
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (601,'优惠券查询',0,2,1,6,'F001',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (602,'充值查询',0,2,2,6,'F002',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (603,'返现查询',0,2,3,6,'F003',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (604,'消费查询',0,2,4,6,'F004',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (605,'会员升级查询',0,2,5,6,'F005',1,NULL);
            INSERT INTO public.menu_func (menu_id,menu_name,"type",menu,sort,parent_id,func_id,status,img) VALUES (609,'图片查询',0,2,9,6,'F009',1,NULL);
            
            """
            session.execute(sql_menu)
            session.commit()
            if row is not None:
                sql="""update users set login_id=encrypt('%s','%s','aes'),status=1,
                    passwd= crypt('%s', gen_salt('md5')) where usr_id=1;"""%(login_id,md5code,passwd)
                session.execute(sql)
                session.commit()
                session.close()
                return render_template('setup.html',code=0)
            sql = """insert into users(usr_id,login_id,passwd,status)values(1,encrypt('%s','%s','aes'),crypt('%s', gen_salt('md5')),1)
                    """ % (login_id, md5code,passwd)

            session.execute(sql)
            session.commit()
            session.close()

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
    #app.run(port=5001)
    app.run(host='127.0.0.1', port=5000,debug=True)




