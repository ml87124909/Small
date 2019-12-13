#coding:utf-8
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""models/model.py"""

from sqlalchemy import create_engine,Column, Integer,Text,DateTime,SMALLINT,Float#, Table, Column, Integer, Text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from dbconfig import tiger,scott,host,port,dbname
url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (scott, tiger, host,port,dbname)
engine = create_engine(url)
DBSession = sessionmaker(bind=engine)


class advertis(Base):
    """ 图片广告分类"""
    __tablename__ = "advertis"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer,  nullable=True,index=True)
    ctype = Column(SMALLINT,  nullable=True,index=True)
    field =  Column(Text,  nullable=True,index=True)
    cname = Column(Text,  nullable=True)
    sort = Column(Integer, nullable=True)
    picurl = Column(Text, nullable=True)
    linkurl = Column(Text, nullable=True)
    buseid = Column(Integer, nullable=True)
    status = Column(SMALLINT, nullable=True)
    random_no = Column(Text, nullable=True,index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class area(Base):
    """地址区域"""
    __tablename__ =  "area"

    id = Column(Integer, primary_key = True, nullable = False,autoincrement=True)
    cname = Column(Text, nullable = True)
    code = Column(Text, nullable = True)
    parent_code = Column(Text, nullable=True)

class backup_log(Base):
    """数据库自动备份记录"""
    __tablename__ ="backup_log"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True)
    bname = Column(Text, nullable=True)
    btime = Column(DateTime, nullable=True)
    ctime = Column(DateTime, nullable=True)
    type = Column(SMALLINT, nullable=True)

class balance_log(Base):
    """小程序用户加钱记录"""
    __tablename__ = "balance_log"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True)
    usr_id = Column(Integer,  nullable=True)
    wechat_user_id =Column(Integer,  nullable=True)
    add_money = Column(Integer,  nullable=True)
    cid =Column(Integer,  nullable=True)
    ctime = Column(DateTime,nullable=True)

class banner(Base):
    """图片广告"""
    __tablename__ =  "banner"
    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True)
    usr_id = Column(Integer, nullable=True)
    title = Column(Text,  nullable=True)
    business_id = Column(Integer, nullable=True)
    good_name = Column(Text, nullable=True)
    link_url = Column(Text, nullable=True)
    pic_url = Column(Text, nullable=True)
    remark = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    ctype = Column(Integer, nullable=True)
    sort = Column(Integer, nullable=True)
    topic_id = Column(Integer, nullable=True)
    cms_name = Column(Text, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)

class brand(Base):
    """ 商品品牌表"""
    __tablename__ = "brand"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer,  nullable=True,index=True)
    cname = Column(Text,  nullable=True,index=True)
    pic_icon = Column(Text, nullable=True, index=True)
    sort = Column(Text, nullable=True, index=True)
    hot = Column(SMALLINT, nullable=True)
    status = Column(SMALLINT, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class cash_log(Base):
    """ 消费记录"""
    __tablename__ = "cash_log"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer,  nullable=True,index=True)
    wechat_user_id = Column(Integer, nullable=True)
    ctype = Column(SMALLINT,  nullable=True)
    ctype_str =  Column(Text,  nullable=True)
    change_money = Column(Float,  nullable=True)
    real_money = Column(Float, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    typeid = Column(Integer, nullable=True)
    typeid_str = Column(Text, nullable=True)
    remark = Column(Text, nullable=True)
    cnumber = Column(Text, nullable=True)
    goods_id = Column(Integer, nullable=True, index=True)
    goods_name = Column(Text, nullable=True)
    give = Column(Float, nullable=True)
    pay_ctime = Column(DateTime, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class category(Base):
    """ 商品分类"""
    __tablename__ = "category"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer,  nullable=True)
    cname = Column(Text, nullable=True)
    ctype = Column(Text,  nullable=True,index=True)
    pid =  Column(Integer,  nullable=True)
    pic_icon = Column(Text, nullable=True)
    pic_imgs = Column(Text, nullable=True)
    paixu = Column(Integer, nullable=True)
    ilevel = Column(SMALLINT, nullable=True)
    status = Column(SMALLINT, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    remark = Column(Text, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)
    cp_id = Column(Integer, nullable=True)

class celery_log(Base):
    """ celery处理log"""
    __tablename__ = "celery_log"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    errors =  Column(Text,  nullable=True,index=True)
    cname = Column(Text,  nullable=True)
    ctime = Column(DateTime, nullable=True)

class city(Base):
    """ 地址的城市"""
    __tablename__ = "city"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    code =  Column(Text,  nullable=True,index=True)
    cname = Column(Text,  nullable=True)
    parent_code = Column(Text, nullable=True)
    telcode = Column(Text, nullable=True)

class cms_doc(Base):
    """ 文章列表"""
    __tablename__ = "cms_doc"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer,  nullable=True,index=True)
    class_id = Column(Integer,  nullable=True,index=True)
    title =  Column(Text,  nullable=True,index=True)
    ctype = Column(Text,  nullable=True)
    keywords = Column(Text, nullable=True)
    pic = Column(Text, nullable=True)
    sort = Column(Integer, nullable=True)
    contents = Column(Text, nullable=True, index=True)
    status = Column(SMALLINT, nullable=True)
    sketch = Column(Text, nullable=True, index=True)
    recom = Column(SMALLINT, nullable=True)
    see = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    favorite = Column(Integer, nullable=True)
    goods = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class cms_favorite(Base):
    """ 文章收藏记录"""
    __tablename__ = "cms_favorite"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer,  nullable=True,index=True)
    wechat_user_id = Column(Integer,  nullable=True,index=True)
    doc_id = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)

class cms_fl(Base):
    """ 文章分类"""
    __tablename__ = "cms_fl"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer,  nullable=True,index=True)
    cname = Column(Text, nullable=True)
    ctype = Column(Text,  nullable=True,index=True)
    pic = Column(Text, nullable=True)
    sort = Column(Integer, nullable=True)
    memo =  Column(Text,  nullable=True,index=True)
    status = Column(SMALLINT, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class cms_likes(Base):
    """ 文章点赞记录"""
    __tablename__ = "cms_likes"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    doc_id = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)

class config_set(Base):
    """ 文字广告设置"""
    __tablename__ = "config_set"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    type = Column(SMALLINT, nullable=True, index=True)
    type_str = Column(Text, nullable=True)
    key = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    remark = Column(Text, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class coupons(Base):
    """ 优惠券表"""
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    remark = Column(Text, nullable=True)
    total = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)
    type_id = Column(Integer, nullable=True)
    type_str = Column(Text, nullable=True)
    type_ext = Column(Text, nullable=True)
    apply_id = Column(Integer, nullable=True)
    apply_str = Column(Text, nullable=True)
    apply_ext_num = Column(Integer, nullable=True)
    apply_ext_money = Column(Integer, nullable=True)
    apply_goods = Column(Integer, nullable=True)
    apply_goods_str = Column(Text, nullable=True)
    apply_goods_id = Column(Text, nullable=True,index=True)
    apply_goods_name = Column(Text, nullable=True)
    use_time = Column(Integer, nullable=True)
    use_time_str = Column(Text, nullable=True)
    datestart = Column(DateTime, nullable=True)
    dateend = Column(DateTime, nullable=True)
    validday = Column(Integer, nullable=True)
    icons = Column(Text, nullable=True)
    pics = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    remain_total = Column(Integer, nullable=True)
    isshow = Column(SMALLINT, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class favorite(Base):
    """ 商品收藏"""
    __tablename__ = "favorite"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    g_id = Column(Integer, nullable=True)
    g_name = Column(Text, nullable=True)
    introduce = Column(Text, nullable=True)
    mini_price = Column(Float, nullable=True)
    original_price = Column(Float, nullable=True)
    pic = Column(Text, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    del_time = Column(DateTime, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class feedback(Base):
    """ 用户反馈"""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    type = Column(Text, nullable=True, index=True)
    text = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    reply = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class gifts(Base):
    """ 充值赠送列表"""
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    add_money = Column(Float, nullable=True)
    giving = Column(Float, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class goods_feedback(Base):
    """ 商品反馈"""
    __tablename__ = "goods_feedback"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    wname = Column(Text, nullable=True, index=True)
    phone = Column(Text, nullable=True)
    gname = Column(Text, nullable=True)
    barcode = Column(Text, nullable=True)
    feedback_memo = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class goods_info(Base):
    """ 商品档案"""
    __tablename__ = "goods_info"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True, index=True)
    introduce = Column(Text, nullable=True, index=True)
    recomm = Column(SMALLINT, nullable=True, index=True)
    status = Column(SMALLINT, nullable=True, index=True)
    category_ids = Column(Text, nullable=True, index=True)
    pic = Column(Text, nullable=True)
    video = Column(Text, nullable=True)
    contents = Column(Text, nullable=True)
    originalprice = Column(Float, nullable=True)
    minprice = Column(Float, nullable=True)
    barcodes = Column(Text, nullable=True)
    stores = Column(Integer, nullable=True)
    logisticsid = Column(Integer, nullable=True)
    limited = Column(Integer, nullable=True)
    discount = Column(Integer, nullable=True)
    orders = Column(Integer, nullable=True)
    see = Column(Integer, nullable=True)
    favorite = Column(Integer, nullable=True)
    share_open = Column(SMALLINT, nullable=True)
    share_open_str = Column(Text, nullable=True)
    share_type = Column(SMALLINT, nullable=True)
    share_type_str = Column(Text, nullable=True)
    share_time = Column(Integer, nullable=True)
    share_title = Column(Text, nullable=True)
    share_imgs = Column(Text, nullable=True)
    goods_reputation = Column(Integer, nullable=True)
    paixu = Column(Integer, nullable=True)
    remark = Column(Text, nullable=True, index=True)
    random_no = Column(Text, nullable=True, index=True)
    share_time_str = Column(Text, nullable=True)
    category_ids_str = Column(Text, nullable=True)
    return_ticket = Column(Integer, nullable=True)
    share_return = Column(Integer, nullable=True)
    return_ticket_str = Column(Text, nullable=True)
    weight = Column(Float, nullable=True)
    pt_status = Column(SMALLINT, nullable=True)
    pt_price = Column(Float, nullable=True)
    hy_price = Column(Float, nullable=True)
    big_price = Column(Float, nullable=True)
    pf_price = Column(Float, nullable=True)
    ls_price = Column(Float, nullable=True)
    dl_price = Column(Float, nullable=True)
    copy_id = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class goods_pics(Base):
    """ 商品图片"""
    __tablename__ = "goods_pics"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    goods_id = Column(Integer, nullable=True, index=True)
    pic = Column(Text, nullable=True, index=True)
    m_id = Column(Integer, nullable=True)
    goodsid_mid = Column(Integer, nullable=True)
    syn_ctime = Column(DateTime, nullable=True)
    syn_utime = Column(DateTime, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class hot_sell(Base):
    """ 商品热销榜"""
    __tablename__ = "hot_sell"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    sort = Column(Integer, nullable=True)
    gid = Column(Integer, nullable=True)
    gname = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class hy_up_level(Base):
    """ 会员级别设置"""
    __tablename__ = "hy_up_level"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    m_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    up_price = Column(Float, nullable=True)
    level_discount = Column(Float, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class images(Base):
    """ 后台上传图片记录"""
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    f_year = Column(Text, nullable=True, index=True)
    f_ext = Column(Text, nullable=True, index=True)
    f_size = Column(Text, nullable=True)
    cname = Column(Text, nullable=True)
    pic = Column(Text, nullable=True)
    num = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class images_api(Base):
    """ 小程序上传图片记录"""
    __tablename__ = "images_api"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    ctype_str = Column(Text, nullable=True, index=True)
    other_id = Column(Integer, nullable=True)
    f_year = Column(Text, nullable=True, index=True)
    f_ext = Column(Text, nullable=True, index=True)
    f_size = Column(Text, nullable=True)
    cname = Column(Text, nullable=True)
    pic = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)
    ctype = Column(Integer, nullable=True)
    goodsid = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class ims_wechats(Base):
    """ 微信公众号设置"""
    __tablename__ = "ims_wechats"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    hash = Column(Text, nullable=True, index=True)
    ctype = Column(Integer, nullable=True)
    uid = Column(Integer, nullable=True)
    token = Column(Text, nullable=True, index=True)
    access_token = Column(Text, nullable=True, index=True)
    expires_in = Column(Integer, nullable=True)
    cname = Column(Text, nullable=True, index=True)
    account = Column(Text, nullable=True, index=True)
    original = Column(Text, nullable=True)
    signature = Column(Text, nullable=True)
    country = Column(Text, nullable=True)
    province = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    username = Column(Text, nullable=True)
    passwd = Column(Text, nullable=True, index=True)
    welcome = Column(Text, nullable=True, index=True)
    is_defaults = Column(Text, nullable=True)
    default_message = Column(Text, nullable=True)
    default_period = Column(SMALLINT, nullable=True)
    lastupdate = Column(Integer, nullable=True)
    mykey = Column(Text, nullable=True, index=True)
    secret = Column(Text, nullable=True, index=True)
    styleid = Column(Integer, nullable=True)
    payment = Column(Text, nullable=True)
    shortcuts = Column(Text, nullable=True)
    quickmenu = Column(Text, nullable=True, index=True)
    qrcode = Column(Integer, nullable=True)
    headimg = Column(Text, nullable=True)
    parentid = Column(Integer, nullable=True)


class ims_fans(Base):
    """ 微信公众号粉丝"""
    __tablename__ = "ims_fans"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    we_id = Column(Integer, nullable=True, index=True)
    from_user = Column(Text, nullable=True, index=True)
    salt = Column(Text, nullable=True)
    follow = Column(SMALLINT, nullable=True)
    credit1 = Column(Integer, nullable=True, index=True)
    credit2 = Column(Float, nullable=True, index=True)
    createtime = Column(Integer, nullable=True)
    realname = Column(Text, nullable=True, index=True)
    nickname = Column(Text, nullable=True, index=True)
    avatar = Column(Text, nullable=True)
    qq = Column(Text, nullable=True)
    mobile = Column(Text, nullable=True)
    fakeid = Column(Text, nullable=True)
    vip = Column(SMALLINT, nullable=True)
    gender = Column(SMALLINT, nullable=True)
    birthyear = Column(SMALLINT, nullable=True, index=True)
    birthmonth = Column(SMALLINT, nullable=True, index=True)
    birthday = Column(SMALLINT, nullable=True)
    constellation = Column(Text, nullable=True)
    zodiac = Column(Text, nullable=True)
    telephone = Column(Text, nullable=True)
    idcard  = Column(Text, nullable=True, index=True)
    studentid = Column(Text, nullable=True, index=True)
    grade = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    zipcode = Column(Text, nullable=True)
    nationality = Column(Text, nullable=True)
    resideprovince = Column(Text, nullable=True)
    residecity = Column(Text, nullable=True)
    residedist = Column(Text, nullable=True)
    graduateschool = Column(Text, nullable=True)
    company = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    occupation = Column(Text, nullable=True, index=True)
    positions = Column(Integer, nullable=True)
    revenue = Column(Text, nullable=True)
    affectivestatus = Column(Text, nullable=True)
    lookingfor = Column(Text, nullable=True)
    bloodtype = Column(Text, nullable=True)
    heights = Column(Text, nullable=True)
    weight = Column(Text, nullable=True)
    alipay = Column(Text, nullable=True)
    msn = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    taobao = Column(Text, nullable=True)
    site = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    interest = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True)
    utime = Column(DateTime, nullable=True)


class integral_log(Base):
    """ 消费记录"""
    __tablename__ = "integral_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    type = Column(Integer, nullable=True, index=True)
    typestr = Column(Text, nullable=True)
    in_out = Column(Integer, nullable=True)
    inoutstr = Column(Text, nullable=True)
    amount = Column(Integer, nullable=True)
    now_amount = Column(Integer, nullable=True)
    picurl = Column(Text, nullable=True)
    linkurl = Column(Text, nullable=True)
    memo = Column(Text, nullable=True, index=True)
    good_id = Column(Integer, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)

class login_log(Base):
    """ 登录日志"""
    __tablename__ = "login_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    login_id = Column(Text, nullable=True, index=True)
    login_ip = Column(Text, nullable=True)
    http_user_agent = Column(Text, nullable=True)
    login_type = Column(Text, nullable=True)
    login_status = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    ctime = Column(DateTime, nullable=True)

class logistics_way(Base):
    """ 配送方式及运费设置"""
    __tablename__ = "logistics_way"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    status = Column(SMALLINT, nullable=True)
    c_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    is_mail = Column(SMALLINT, nullable=True)
    counts = Column(SMALLINT, nullable=True)
    piece = Column(Integer, nullable=True)
    only_money = Column(Float, nullable=True, index=True)
    add_piece = Column(Integer, nullable=True)
    add_money = Column(Float, nullable=True)
    is_default = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class mall(Base):
    """ 小程序配置"""
    __tablename__ = "mall"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    appid = Column(Text, nullable=True, index=True)
    secret = Column(Text, nullable=True)
    mchid = Column(Text, nullable=True)
    mchkey = Column(Text, nullable=True)
    certpem = Column(Text, nullable=True)
    keypem = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class menu_func(Base):
    """ 后台菜单"""
    __tablename__ = "menu_func"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    menu_id = Column(Integer, nullable=True, index=True)
    vtype = Column(SMALLINT, nullable=True, index=True)
    menu_name = Column(Text, nullable=True)
    menu = Column(Integer, nullable=True, index=True)
    sort = Column(Integer, nullable=True, index=True)
    parent_id = Column(Integer, nullable=True)
    func_id = Column(Text, nullable=True, index=True)
    status = Column(SMALLINT, nullable=True, index=True)
    img = Column(Text, nullable=True)

class mtc_t(Base):
    """ 关联说明表"""
    __tablename__ = "mtc_t"

    seq = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    id = Column(Integer, nullable=True, index=True)
    type = Column(Text, nullable=True, index=True)
    txt1 = Column(Text, nullable=True, index=True)
    txt2 = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    sort = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class my_coupons(Base):
    """ 小程序用户的优惠券"""
    __tablename__ = "my_coupons"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    m_id = Column(Integer, nullable=True)
    cname = Column(Text, nullable=True)
    type_id = Column(Integer, nullable=True)
    type_str = Column(Text, nullable=True)
    type_ext = Column(Text, nullable=True)
    remark = Column(Text, nullable=True)
    icons = Column(Text, nullable=True)
    pics = Column(Text, nullable=True)
    goods_id = Column(Text, nullable=True)
    datestart = Column(DateTime, nullable=True)
    date_end = Column(DateTime, nullable=True)
    state = Column(SMALLINT, nullable=True)
    state_str = Column(Text, nullable=True)
    num = Column(Integer, nullable=True)
    apply_id = Column(Integer, nullable=True)
    apply_str = Column(Text, nullable=True)
    apply_ext_num = Column(Float, nullable=True)
    apply_ext_money = Column(Float, nullable=True)
    use_time = Column(Integer, nullable=True)
    use_time_str = Column(Text, nullable=True)
    validday = Column(Integer, nullable=True)
    good_id = Column(Integer, nullable=True)
    re_status = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class offline_pay(Base):
    """ 线下支付"""
    __tablename__ = "offline_pay"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    wname = Column(Text, nullable=True)
    avatar = Column(Text, nullable=True)
    order_num = Column(Text, nullable=True, index=True)
    status = Column(SMALLINT, nullable=True)
    total = Column(Float, nullable=True)
    counpon = Column(Float, nullable=True)
    vipsale = Column(Float, nullable=True)
    truemoney = Column(Float, nullable=True)
    score = Column(Float, nullable=True)
    couponid = Column(Integer, nullable=True)
    couponname = Column(Text, nullable=True)
    ctype = Column(SMALLINT, nullable=True)
    paykey = Column(Text, nullable=True, index=True)
    data_close = Column(DateTime, nullable=True)
    paytime = Column(DateTime, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class open_pt(Base):
    """ 开启的拼团"""
    __tablename__ = "open_pt"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    ptid = Column(Integer, nullable=True, index=True)
    order_id = Column(Integer, nullable=True, index=True)
    name = Column(Text, nullable=True)
    avatar = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    number = Column(Integer, nullable=True)
    short = Column(Integer, nullable=True)
    stores = Column(Integer, nullable=True)
    status = Column(SMALLINT, nullable=True)
    date_end = Column(DateTime, nullable=True)
    gid = Column(Integer, nullable=True)
    gname = Column(Text, nullable=True)
    gintr = Column(Text, nullable=True)
    gpic = Column(Text, nullable=True)
    gcontent = Column(Text, nullable=True)
    ptprice = Column(Float, nullable=True)
    mnprice = Column(Float, nullable=True)
    ok_type = Column(SMALLINT, nullable=True)
    add_type = Column(SMALLINT, nullable=True)
    tk_type = Column(SMALLINT, nullable=True)
    kt_type = Column(SMALLINT, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class open_pt_detail(Base):
    """ 拼团明细"""
    __tablename__ = "open_pt_detail"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    ptid = Column(Integer, nullable=True, index=True)
    opid = Column(Integer, nullable=True, index=True)
    order_id = Column(Integer, nullable=True, index=True)
    name = Column(Text, nullable=True, index=True)
    avatar = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    title = Column(Integer, nullable=True)
    status = Column(SMALLINT, nullable=True)
    date_end = Column(DateTime, nullable=True)
    ct_type = Column(SMALLINT, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class order_exchange(Base):
    """ 售后订单"""
    __tablename__ = "order_exchange"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    w_name = Column(Text, nullable=True, index=True)
    avatar = Column(Text, nullable=True)
    e_num = Column(Text, nullable=True)
    order_id = Column(Integer, nullable=True)
    order_num = Column(Text, nullable=True)
    ctype = Column(SMALLINT, nullable=True)
    ctype_str = Column(Text, nullable=True)
    status = Column(Integer, nullable=True)
    status_str = Column(Text, nullable=True)
    r_money = Column(Float, nullable=True)
    order_money = Column(Float, nullable=True)
    reason = Column(Text, nullable=True)
    not_memo = Column(Text, nullable=True)
    kd_number = Column(Text, nullable=True)
    refund_type = Column(SMALLINT, nullable=True)
    old_status = Column(Integer, nullable=True)
    old_status_str = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)
    kuaname = Column(Text, nullable=True)
    e_kuainame = Column(Text, nullable=True)
    e_kuaicode = Column(Text, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class order_exchange_detail(Base):
    """ 售后订单商品明细"""
    __tablename__ = "order_exchange_detail"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    e_id = Column(Integer, nullable=True, index=True)
    e_num = Column(Text, nullable=True, index=True)
    e_amount = Column(Integer, nullable=True, index=True)
    all_amount = Column(Integer, nullable=True, index=True)
    o_gid = Column(Integer, nullable=True, index=True)
    old_status = Column(Integer, nullable=True, index=True)
    old_status_str = Column(Text, nullable=True)
    good_id = Column(Integer, nullable=True)
    good_name = Column(Text, nullable=True)
    pic = Column(Text, nullable=True)
    spec = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class print_log(Base):
    """ 打印记录"""
    __tablename__ = "print_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    errors = Column(Text, nullable=True)
    cname = Column(Text, nullable=True, index=True)
    ctime = Column(DateTime, nullable=True)

class profit_record(Base):
    """ 分享返收益记录"""
    __tablename__ = "profit_record"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True)
    ctype = Column(Integer, nullable=True, index=True)
    ctype_str = Column(Text, nullable=True, index=True)
    share_type = Column(Integer, nullable=True, index=True)
    share_type_str = Column(Text, nullable=True)
    change_money = Column(Float, nullable=True)
    remark = Column(Text, nullable=True)
    goods_id = Column(Integer, nullable=True)
    goods_name = Column(Text, nullable=True)
    ticket_id = Column(Integer, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)

class province(Base):
    """ 地址省级"""
    __tablename__ = "province"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    cname = Column(Text, nullable=True)
    sort = Column(Integer, nullable=True)
    code = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class preload_log(Base):
    """ 缓存记录"""
    __tablename__ = "preload_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    errors = Column(Text, nullable=True)
    cname = Column(Text, nullable=True, index=True)
    ctime = Column(DateTime, nullable=True)


class pt_conf(Base):
    """ 拼团设置"""
    __tablename__ = "pt_conf"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    goods_id = Column(Integer, nullable=True, index=True)
    good_name = Column(Text, nullable=True, index=True)
    pt_price = Column(Float, nullable=True)
    sort = Column(Integer, nullable=True)
    pt_num = Column(Integer, nullable=True)
    ok_num = Column(Integer, nullable=True)
    timeout_h = Column(Integer, nullable=True)
    kt_type = Column(SMALLINT, nullable=True)
    add_type = Column(SMALLINT, nullable=True)
    tk_type = Column(SMALLINT, nullable=True)
    ok_type = Column(SMALLINT, nullable=True)
    status = Column(SMALLINT, nullable=True)
    date_add = Column(DateTime, nullable=True)
    date_end = Column(DateTime, nullable=True)
    recom = Column(SMALLINT, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class pt_log(Base):
    """ 拼团记录"""
    __tablename__ = "pt_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    openpt_id = Column(Integer, nullable=True, index=True)
    pt_id = Column(Integer, nullable=True)
    pt_num = Column(Text, nullable=True, index=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class qiniu(Base):
    """ OSS存储设置"""
    __tablename__ = "qiniu"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    ctype = Column(SMALLINT, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    access_key = Column(Text, nullable=True, index=True)
    secret_key = Column(Text, nullable=True)
    domain_url = Column(Text, nullable=True)
    endpoint = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class qrcode(Base):
    """ 小程序海报链接地址"""
    __tablename__ = "qrcode"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    url = Column(Text, nullable=True, index=True)
    scene = Column(Text, nullable=True)
    page = Column(Text, nullable=True)
    img_name = Column(Text, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class refund_money(Base):
    """ 退款"""
    __tablename__ = "refund_money"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    w_name = Column(Text, nullable=True, index=True)
    avatar = Column(Text, nullable=True)
    r_num = Column(Text, nullable=True)
    order_id = Column(Integer, nullable=True)
    order_num = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    r_money = Column(Float, nullable=True)
    order_money = Column(Float, nullable=True)
    reason = Column(Text, nullable=True, index=True)
    not_memo = Column(Text, nullable=True, index=True)
    refund_type = Column(SMALLINT, nullable=True)
    timestamp = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class reputation_list(Base):
    """ 商品评价"""
    __tablename__ = "reputation_list"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_mall_usr_id = Column(Integer, nullable=True, index=True)
    usr_name = Column(Text, nullable=True)
    user_avatar = Column(Text, nullable=True)
    orderid = Column(Integer, nullable=True)
    goods_id = Column(Integer, nullable=True)
    goods = Column(Text, nullable=True)
    goods_reputation = Column(Text, nullable=True)
    goods_star = Column(Text, nullable=True)
    star_id = Column(SMALLINT, nullable=True)
    goods_reply = Column(Text, nullable=True)
    order_detail_id = Column(Integer, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class role_menu(Base):
    """ 角色菜单"""
    __tablename__ = "role_menu"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    role_id = Column(Integer, nullable=True, index=True)
    menu_id = Column(Integer, nullable=True, index=True)
    can_add = Column(Integer, nullable=True)
    can_upd = Column(Integer, nullable=True)
    can_del = Column(Integer, nullable=True)
    can_see = Column(Integer, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class roles(Base):
    """ 角色表"""
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    role_name = Column(Text, nullable=True, index=True)
    sort = Column(Integer, nullable=True)
    dept_id = Column(Integer, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True, index=True)
    random_no = Column(Text, nullable=True, index=True)
    memo = Column(Text, nullable=True, index=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class score_set(Base):
    """ 签到积分"""
    __tablename__ = "score_set"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    score = Column(Integer, nullable=True, index=True)
    days = Column(Integer, nullable=True)
    status = Column(SMALLINT, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True, index=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class search_key(Base):
    """ 搜索关键字"""
    __tablename__ = "search_key"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True, index=True)
    num = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    utime = Column(DateTime, nullable=True)

class self_paykey(Base):
    """ 线下扫码支付key"""
    __tablename__ = "self_paykey"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    paykey = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True)

class shop_set(Base):
    """ 店铺设置"""
    __tablename__ = "shop_set"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    logo_pic = Column(Text, nullable=True)
    logo_pic_link = Column(Text, nullable=True)
    home_title = Column(Text, nullable=True)
    home_pic = Column(Text, nullable=True)
    home_pic_link = Column(Text, nullable=True)
    gadds = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    times = Column(Text, nullable=True)
    use_money = Column(Float, nullable=True)
    close_time = Column(Integer, nullable=True)
    cancel_id = Column(Text, nullable=True)
    send_id = Column(Text, nullable=True)
    evaluate_id = Column(Text, nullable=True)
    complete_id = Column(Text, nullable=True)
    cancel_url = Column(Text, nullable=True)
    send_url = Column(Text, nullable=True)
    evaluate_url = Column(Text, nullable=True)
    complete_url = Column(Text, nullable=True)
    take_day = Column(Integer, nullable=True)
    close_time_pk = Column(Integer, nullable=True)
    vip_price = Column(Float, nullable=True)
    up_type = Column(SMALLINT, nullable=True)
    discount = Column(Float, nullable=True)
    vip_sale = Column(Float, nullable=True)
    home_goods = Column(SMALLINT, nullable=True)
    ebusinessid = Column(Text, nullable=True)
    home_goods_id = Column(Text, nullable=True)
    shop_goods = Column(SMALLINT, nullable=True)
    appkey = Column(Text, nullable=True)
    shop_goods_id = Column(Text, nullable=True)
    memo = Column(Text, nullable=True)
    shop_cart_memo = Column(Text, nullable=True)
    menu_memo = Column(Text, nullable=True)
    order_goods_str = Column(Text, nullable=True)
    order_goods = Column(SMALLINT, nullable=True)
    order_goods_id = Column(Text, nullable=True)
    return_ticket = Column(Integer, nullable=True)
    return_ticket_str = Column(Text, nullable=True)
    vip_integral = Column(Integer, nullable=True)
    integral = Column(Integer, nullable=True)
    new_score = Column(Integer, nullable=True)
    max_cash = Column(Float, nullable=True)
    mini_cash = Column(Float, nullable=True)
    arrive = Column(Text, nullable=True)
    topup = Column(Integer, nullable=True)
    topup_str = Column(Text, nullable=True)
    drawal = Column(Integer, nullable=True)
    drawal_str = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class shopconfig(Base):
    """ 商铺设置"""
    __tablename__ = "shopconfig"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    contact = Column(Text, nullable=True)
    wd = Column(Float, nullable=True)
    jd = Column(Float, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class signin(Base):
    """ 小程序签到"""
    __tablename__ = "signin"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    con_amount = Column(Integer, nullable=True)
    memo = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class signin_log(Base):
    """ 签到日志"""
    __tablename__ = "signin_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)

class spec(Base):
    """ 商品规格"""
    __tablename__ = "spec"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    ctype = Column(Text, nullable=True)
    cicon = Column(Text, nullable=True)
    sort = Column(Integer, nullable=True, index=True)
    cp_id = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True, index=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class spec_child(Base):
    """ 商品规格子属性"""
    __tablename__ = "spec_child"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    spec_id = Column(Integer, nullable=True, index=True)
    cname_c = Column(Text, nullable=True)
    ctype_c = Column(Text, nullable=True)
    cicon_c = Column(Text, nullable=True)
    sort_c = Column(Integer, nullable=True, index=True)
    cp_id = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True, index=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class spec_child_price(Base):
    """ 商品规格组合价格"""
    __tablename__ = "spec_child_price"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    goods_id = Column(Integer, nullable=True, index=True)
    sc_id = Column(Text, nullable=True, index=True)
    sc_name = Column(Text, nullable=True, index=True)
    oldprice = Column(Float, nullable=True)
    newprice = Column(Float, nullable=True)
    ptprice = Column(Float, nullable=True)
    hyprice = Column(Float, nullable=True)
    bigprice = Column(Float, nullable=True)
    pfprice = Column(Float, nullable=True)
    lsprice = Column(Float, nullable=True)
    dlprice = Column(Float, nullable=True)
    store_c = Column(Integer, nullable=True)
    barcode = Column(Text, nullable=True)
    sc_icon = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class top_up(Base):
    """ 充值记录"""
    __tablename__ = "top_up"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    order_no = Column(Text, nullable=True, index=True)
    add_money = Column(Float, nullable=True)
    real_money = Column(Float, nullable=True)
    status = Column(SMALLINT, nullable=True, index=True)
    status_str = Column(Text, nullable=True)
    give = Column(Float, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class update_order(Base):
    """ 定时更新订单"""
    __tablename__ = "update_order"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    remark = Column(Text, nullable=True, index=True)
    ctime = Column(DateTime, nullable=True)

class update_psw(Base):
    """ 定时更新??"""
    __tablename__ = "update_psw"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    vip = Column(Integer, nullable=True, index=True)
    oldpsw = Column(Integer, nullable=True)
    newpsw = Column(Integer, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)

class update_pt(Base):
    """ 定时更新拼团"""
    __tablename__ = "update_pt"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    remark = Column(Text, nullable=True, index=True)
    ctime = Column(DateTime, nullable=True)

class update_refund(Base):
    """ 定时更新退款"""
    __tablename__ = "update_refund"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    remark = Column(Text, nullable=True, index=True)
    ctime = Column(DateTime, nullable=True)

class use_log(Base):
    """ 操作记录"""
    __tablename__ = "use_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    viewid = Column(Text, nullable=True, index=True)
    memo = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True)

class user_log(Base):
    """ 小程序用户记录"""
    __tablename__ = "user_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    memo = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True)

class users(Base):
    """ 系统用户表"""
    __tablename__ = "users"

    usr_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    login_id = Column(Text, nullable=True, index=True)
    passwd = Column(Text, nullable=True)
    dept_id = Column(Integer, nullable=True, index=True)
    usr_id_p = Column(Integer, nullable=True, index=True)
    status = Column(SMALLINT, nullable=True)
    mini_openid = Column(Text, nullable=True)
    wx_openid = Column(Text, nullable=True)
    with_flag = Column(SMALLINT, nullable=True)
    expire_flag = Column(SMALLINT, nullable=True)
    expire_time = Column(DateTime, nullable=True)
    login_lock = Column(SMALLINT, nullable=True)
    login_lock_time = Column(DateTime, nullable=True)
    vip_flag = Column(Integer, nullable=True)
    last_login = Column(DateTime, nullable=True)
    last_ip = Column(Text, nullable=True)
    inviteid = Column(Integer, nullable=True)
    oss_all = Column(Integer, nullable=True)
    oss_now = Column(Integer, nullable=True)
    qiniu_flag = Column(SMALLINT, nullable=True)
    oss_flag = Column(SMALLINT, nullable=True)
    oss_time = Column(DateTime, nullable=True)
    vip_days = Column(Integer, nullable=True)
    invite_days = Column(Integer, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class usr_role(Base):
    """ 用户角色表"""
    __tablename__ = "usr_role"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    role_id = Column(Integer, nullable=True, index=True)
    usr_name = Column(Text, nullable=True)
    access_son = Column(Integer, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)


class view_history(Base):
    """ 浏览记录"""
    __tablename__ = "view_history"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    g_id = Column(Integer, nullable=True, index=True)
    g_name = Column(Text, nullable=True, index=True)
    introduce = Column(Text, nullable=True)
    mini_price = Column(Float, nullable=True)
    original_price = Column(Float, nullable=True)
    pic = Column(Text, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    del_time = Column(DateTime, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class vip_member(Base):
    """ 小程序会员购买"""
    __tablename__ = "vip_member"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    order_no = Column(Text, nullable=True, index=True)
    real_money = Column(Float, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class virtual_conf(Base):
    """ 促拼团虚拟用户设置"""
    __tablename__ = "virtual_conf"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    avatar = Column(Text, nullable=True, index=True)
    phone = Column(Text, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class wechat_address(Base):
    """ 小程序收货地址"""
    __tablename__ = "wechat_address"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    phone = Column(Text, nullable=True, index=True)
    province = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    district = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    code = Column(Text, nullable=True)
    is_default = Column(SMALLINT, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    del_time = Column(DateTime, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    provinceid = Column(Integer, nullable=True)
    provincestr = Column(Text, nullable=True)
    cityid = Column(Integer, nullable=True)
    citystr = Column(Text, nullable=True)
    districtid = Column(Integer, nullable=True)
    districtstr = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class wechat_formid(Base):
    """ 小程序表单ID"""
    __tablename__ = "wechat_formid"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    order_id = Column(Integer, nullable=True, index=True)
    formid = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True)
    utime = Column(DateTime, nullable=True)

class wechat_mall_order(Base):
    """ 小程序订单表"""
    __tablename__ = "wechat_mall_order"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    w_name = Column(Text, nullable=True)
    cname = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    kuaid = Column(Integer, nullable=True)
    kuaid_str = Column(Text, nullable=True)
    province = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    district = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    code = Column(Text, nullable=True)
    order_num = Column(Text, nullable=True, index=True)
    number_goods = Column(Integer, nullable=True)
    goods_price = Column(Float, nullable=True)
    couponid = Column(Integer, nullable=True)
    coupon_name = Column(Text, nullable=True)
    coupon_price = Column(Float, nullable=True)
    logistics_price = Column(Float, nullable=True)
    vip_sale = Column(Float, nullable=True)
    vip_price = Column(Float, nullable=True)
    vip_total = Column(Float, nullable=True)
    new_total = Column(Float, nullable=True)
    vip_small = Column(Float, nullable=True)
    balance = Column(Float, nullable=True)
    wx_pay_total = Column(Float, nullable=True)
    freetaxs = Column(Float, nullable=True)
    data_close = Column(DateTime, nullable=True)
    ctype = Column(SMALLINT, nullable=True,index=True)
    ctype_str = Column(Text, nullable=True)
    shipper_id = Column(Integer, nullable=True)
    shipper_str = Column(Text, nullable=True)
    shipper_code = Column(Text, nullable=True)
    tracking_number = Column(Text, nullable=True)
    shipper_time = Column(DateTime, nullable=True)
    pay_status = Column(SMALLINT, nullable=True)
    pay_status_str = Column(DateTime, nullable=True)
    pay_ctime = Column(DateTime, nullable=True)
    mendian_id = Column(Integer, nullable=True)
    pick_number = Column(Text, nullable=True)
    check_id = Column(SMALLINT, nullable=True)
    check_time = Column(DateTime, nullable=True)
    check_uid = Column(Integer, nullable=True)
    price_status = Column(SMALLINT, nullable=True)
    price_time = Column(DateTime, nullable=True)
    price_num = Column(Text, nullable=True)
    s_type = Column(SMALLINT, nullable=True)
    c_type = Column(SMALLINT, nullable=True)
    o_type = Column(SMALLINT, nullable=True)
    e_type = Column(SMALLINT, nullable=True)
    ptkid = Column(Integer, nullable=True)
    pt_type = Column(SMALLINT, nullable=True)
    ptid = Column(Integer, nullable=True)
    pt_kt = Column(Integer, nullable=True)
    agent_status = Column(SMALLINT, nullable=True)
    agent_time = Column(DateTime, nullable=True)
    total = Column(Float, nullable=True)
    remark = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True,index=True)
    status_str = Column(Text, nullable=True)
    message_last_post = Column(DateTime, nullable=True)
    memo = Column(Text, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class wechat_mall_order_detail(Base):
    """ 订单商品明细"""
    __tablename__ = "wechat_mall_order_detail"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    order_id = Column(Integer, nullable=True, index=True)
    order_num = Column(Text, nullable=True, index=True)
    good_id = Column(Integer, nullable=True)
    good_name = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    pic = Column(Text, nullable=True)
    amount = Column(Integer, nullable=True)
    property_str = Column(Text, nullable=True)
    shipper_id = Column(Integer, nullable=True)
    tracking_number = Column(Text, nullable=True)
    sale = Column(Float, nullable=True)
    total = Column(Float, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True, index=True)
    original_price = Column(Float, nullable=True)
    shipper_str = Column(Text, nullable=True)
    shipper_time = Column(DateTime, nullable=True)
    shipper_code = Column(Text, nullable=True)
    kuastate = Column(SMALLINT, nullable=True)
    e_status = Column(SMALLINT, nullable=True)
    inviter_user = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class wechat_mall_order_log(Base):
    """ 订单日志"""
    __tablename__ = "wechat_mall_order_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    order_id = Column(Integer, nullable=True, index=True)
    edit_name = Column(Text, nullable=True)
    edit_memo = Column(Text, nullable=True)
    edit_remark = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)

class wechat_mall_payment(Base):
    """ 微信支付记录"""
    __tablename__ = "wechat_mall_payment"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    ctype = Column(SMALLINT, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    openid = Column(Text, nullable=True, index=True)
    order_id = Column(Integer, nullable=True, index=True)
    transaction_id = Column(Text, nullable=True)
    payment_number = Column(Text, nullable=True)
    total_fee = Column(Integer, nullable=True)
    settlement_total_fee = Column(Integer, nullable=True)
    cash_fee = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    coupon_fee = Column(Integer, nullable=True)
    cash_fee_type = Column(Integer, nullable=True)
    fee_type = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    err_code_des = Column(Text, nullable=True)
    bank_type = Column(Text, nullable=True)
    coupon_count = Column(Integer, nullable=True)
    result_code = Column(Text, nullable=True)
    err_code = Column(Text, nullable=True)
    prepay_id = Column(Text, nullable=True)
    noncestr = Column(Text, nullable=True)
    package = Column(Text, nullable=True)
    paysign = Column(Text, nullable=True)
    timestamp_ = Column(Text, nullable=True)
    time_end = Column(Text, nullable=True)
    renoncestr = Column(Text, nullable=True)
    sign = Column(Text, nullable=True)
    order_num = Column(Text, nullable=True,index=Text)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class wechat_mall_refund(Base):
    """ 微信退款记录"""
    __tablename__ = "wechat_mall_refund"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    out_trade_no = Column(Text, nullable=True, index=True)
    out_refund_no = Column(Text, nullable=True,index=True)
    transaction_id = Column(Text, nullable=True)
    total_fee = Column(Integer, nullable=True)
    refund_fee = Column(Integer, nullable=True)
    refund_id = Column(Text, nullable=True, index=True)
    cash_fee = Column(Integer, nullable=True)
    return_msg = Column(Text, nullable=True)
    result_code = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True)
    utime = Column(DateTime, nullable=True)

class wechat_mall_user(Base):
    """ 小程序用户"""
    __tablename__ = "wechat_mall_user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    phone = Column(Text, nullable=True, index=True)
    cname = Column(Text, nullable=True)
    open_id = Column(Text, nullable=True, index=True)
    union_id = Column(Text, nullable=True)
    languages = Column(Text, nullable=True)
    country = Column(Text, nullable=True)
    province = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True)
    register_ip = Column(Text, nullable=True)
    last_login_ip = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    gender = Column(Integer, nullable=True)
    usr_flag = Column(Integer, nullable=True)
    usr_flag_str = Column(Text, nullable=True)
    usr_level = Column(Integer, nullable=True)
    usr_level_str = Column(Text, nullable=True)
    balance = Column(Float, nullable=True)
    djje = Column(Float, nullable=True)
    hy_flag = Column(SMALLINT, nullable=True)
    hy_flag_str = Column(Text, nullable=True)
    hy_ctime = Column(DateTime, nullable=True)
    hy_etime = Column(DateTime, nullable=True)
    integral = Column(Float, nullable=True)
    up_time = Column(DateTime, nullable=True)
    score = Column(Integer, nullable=True)
    count_total = Column(Float, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    del_flag = Column(SMALLINT, nullable=True,index=True)
    ctime = Column(DateTime, nullable=True,index=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class webapge_log(Base):
    """ 小程序用户记录"""
    __tablename__ = "webapge_log"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    errors = Column(Text, nullable=True)
    cname = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True)

class wechat_user_change_log(Base):
    """ 小程序用户记录"""
    __tablename__ = "wechat_user_change_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    name = Column(Text, nullable=True)
    old_level = Column(Text, nullable=True)
    new_level = Column(Text, nullable=True)
    up_type_str = Column(Text, nullable=True)
    end_time = Column(DateTime, nullable=True)
    up_mode_str = Column(Text, nullable=True)
    memo = Column(Text, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class withdraw_cash(Base):
    """ 小程序现金变化"""
    __tablename__ = "withdraw_cash"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    wechat_user_id = Column(Integer, nullable=True, index=True)
    del_money = Column(Float, nullable=True)
    status = Column(SMALLINT, nullable=True)
    status_str = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    remark = Column(Text, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class platform_conf(Base):
    """ 平台管理"""
    __tablename__ = "platform_conf"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    base_url = Column(Text,  nullable=True,comment='平台微信支付回调地址')
    back_url = Column(Text, nullable=True, comment='VIP微信支付回调地址')
    pay_status = Column(SMALLINT, nullable=True, comment='收费控制')
    try_days = Column(Integer, nullable=True, comment='注册体验时间')
    invite_days = Column(Integer, nullable=True, comment='邀请注册赠送时间')
    vip_days = Column(Integer, nullable=True, comment='被邀请人付费后赠送时间')
    combo_one_name = Column(Text, nullable=True, comment='付费套餐一名称')
    combo_one_price = Column(Float, nullable=True, comment='付费套餐一价格')
    combo_one_day = Column(Integer, nullable=True, comment='付费套餐一使用时间')
    combo_one_status = Column(SMALLINT, nullable=True, comment='付费套餐一是否启用')
    combo_one_txt= Column(Text, nullable=True, comment='付费套餐一说明')
    combo_two_name = Column(Text, nullable=True, comment='付费套餐二名称')
    combo_two_price = Column(Float, nullable=True, comment='付费套餐二价格')
    combo_two_day = Column(Integer, nullable=True, comment='付费套餐二使用时间')
    combo_two_status = Column(SMALLINT, nullable=True, comment='付费套餐二是否启用')
    combo_two_txt = Column(Text, nullable=True, comment='付费套餐二说明')
    combo_thr_name = Column(Text, nullable=True, comment='付费套餐三名称')
    combo_thr_price = Column(Float, nullable=True, comment='付费套餐三价格')
    combo_thr_day = Column(Integer, nullable=True, comment='付费套餐三使用时间')
    combo_thr_status = Column(SMALLINT, nullable=True, comment='付费套餐三是否启用')
    combo_thr_txt = Column(Text, nullable=True, comment='付费套餐三说明')
    dbname = Column(Text, nullable=True, comment='要备份数据库名')
    notices = Column(Text, nullable=True, comment='顶部消息')
    memo = Column(Text, nullable=True, comment='滚动消息')
    appid = Column(Text, nullable=True, comment='后台登录用的微信appid')
    secret = Column(Text, nullable=True, comment='后台登录用的微信secret')
    wx_status = Column(SMALLINT, nullable=True, comment='后台是否开启微信登录')
    wxtoken = Column(Text, nullable=True, comment='后台登录用的微信token')
    wxaeskey = Column(Text, nullable=True, comment='后台登录用的微信验证密钥')
    mchid = Column(Text, nullable=True, comment='微信支付商户id')
    mchkey = Column(Text, nullable=True, comment='微信支付商户密钥')
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)


def createall(engine_):
    try:
        Base.metadata.drop_all(engine_)
    except:
        pass
    Base.metadata.create_all(engine_)