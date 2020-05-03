# Small  一个达到国家等级保护2级的项目，让您安心无忧！

# 更新说明  2020-05-03    
只保留SAAS版本，B2B2C版本及个人版本另起项目处理。

体验请到  https://store.yjyzj.cn

![](https://github.com/mn3711698/Small/blob/master/923.png)

![](https://github.com/mn3711698/Small/blob/master/1574772580.jpg)

#### 注意：用docker镜像mn3711698/small:004的一定要git pull，这个docker镜像我不再更新，需要自己git pull更新项目代码,不然代码会很旧，没法用!

## 请务必使用python3.6  请务必使用python3.6  请务必使用python3.6
## 请务必将项目放到/var/games路径下  请务必将项目放到/var/games路径下  请务必将项目放到/var/games路径下
我开发用的是windows 10(linux子系统:ubuntu 18.04) + python3.6.8 演示环境用的是centos 7.6+python3.6.9
# 说明  2019-08-07
docker镜像:mn3711698/small:004,我测试过OK。基于ubuntu 18.04 的python3.6.8+postgresql-10。
<br>您完全可以直接在里边的/var/games/Small下，先安装(python3 install.py)，安装好再运行(python3 start.py)。
<br>以后docker里的代码我就不更新了，有需要的直接git pull就好了。
<br>我是将整个环境都弄好打包成一个，直接在docker里边运行，我也不懂别的方法，这样有个问题就是，那个安装生成的dbconfig.py文件没有，每次都要重新搞。
<br>python3 start.py启动项目通常是用来调试的，如果要生产运行，您可以用nginx+apache或者别的方法，我是用nginx+apache或nginx+gunicorn+supervisor都可以。

本系统采用python3,基于flask搭建的脚手架开发。数据库是postgresql.
<br>请注意config.py这个配置文件，默认开启调试日志。

配合SmallStore开源小程序使用：https://github.com/mn3711698/SmallStore

目标是满足进销存ERP，供销等各种功能及接口（小程序，微信公众号，H5，APP）。
> 目前功能是比较少，将会不断增加，同时也期待您贡献代码或者功能(插件)。

# 功能特性
> - [x] 表示已开发
> - [ ] 表示准备开发


- [x] 小程序管理
    * 店铺设置
        * OSS存储设置
        * 店铺信息设置
        * 商铺设置
        * 订单设置
        * 小程序设置
        * 会员设置
        * 全局设置
        * 积分规则设置
        * 充值设置
        * 快递鸟设置
    * 图片广告
    * 文字广告
    * 文章分类
    * 文章列表
    * 用户列表
    * 用户地址
    * 用户反馈
    
- [x] 商品管理
    * 商品分类
    * 商品规格
    * 商品档案
    * 商品评价
    * 商品热销榜
    * 商品反馈
    
- [x] 营销中心
    * 优惠券
    * 拼团活动
    
- [x] 订单管理
    * 销售订单
    * 退款订单
    * 售后订单
    
- [x] 综合查询
    * 优惠券查询
    * 充值查询
    * 返现查询
    * 消费查询
    * 会员升级查询
    * 图片查询
    
- [x] 系统管理
    * 个人帐号
    * 角色授权
    * 人员管理
    * 人员授权
    * 登录日志
    * 帐号解锁

- [x] 公众号管理
    * 基本设置
    * 菜单设置
    * 文字回复
    * 特殊回复
    * 粉丝列表

- [ ] 帐号管理
    * 子帐号设置
    * 子帐号角色
    * 子帐号授权
    
- [ ] 平台管理
    * 平台设置
        * 相关设置
        * 商家公告
    
  


                                                                        
## 目录模块

```
├── admin  #SAAS后台目录（比较多，还未整理）
│   ├── dl  #路由映射的数据处理
│   │
│   ├── html  #html文件
│   │
│   └── vi  #对应路由文件
│
│
├── api  # SAAS小程序接口目录
│   ├── BASE_LOC.py
│   ├── BASE_TPL.py
│   ├── helper.py
│   ├── home.py
│   ├── pay.py
│   ├── VI_BASE.py
│   ├── VIEWS.py
│   └── wxpay.py
│
├── basic  #共用文件目录
│   ├── base.py #后台cookie处理
│   ├── indb.so #安装时调用的数据库类
│   ├── pay.py  #微信支付
│   ├── preload.py  #缓存处理
│   ├── publicw.so  #基础类
│   ├── wxbase.py
│   └── wxpublic.py
│ 
├── celery_app  #定时任务目录
│   ├── celeryconfig.py
│   ├── db_backup.py
│   └── pfc.py
│
│   
│
├── models  #数据库表
│   └── model.py
│   
│
│   
│
├── static  #css,js,img等静态文件
│     
│   
├── templates  #安装过程的html
│   
│   
└── wxpay  # 微信支付回调
│     ├── mPay.py #b2b2c版支付回调处理
│     ├── sPay.py #个人版支付回调处理
│     └── WxPay.py #SAAS版支付回调处理 
│   
├── config.py #基本配置
├── install.py #项目安装启动
├── runall.py #启动所有版本(专为开发调试)
├── start.py #启动SAAS版
├── startm.py #启动B2B2C版
├── starts.py #启动个人版
└── zone.py #七牛上传修改
```

## 目前系统还在完善中，如果有bug请加下边的QQ群反馈，感谢！
 QQ群：528289471


# License
为了增加运行效率及安全加固(国家等保2级)，特将部分代码采用cython处理。不会收集任何个人敏感信息，并且项目将客户存在数据库的敏感信息有加密处理，具体可以看代码。
> 此项目为个人项目，不会中断维护及功能(插件)更新。bug的维护效率还是可以的(不少使用者都这么认为)。
> 不禁止任何形式的使用、修改、发布、分发该项目。
> 不涉及源码无任何商业授权费用。






