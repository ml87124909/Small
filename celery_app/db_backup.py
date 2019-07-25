# -*- coding: utf-8 -*-

##############################################################################
#
#
##############################################################################


from flask import Flask, json
# from flask_mail import Mail,Message
from celery import Celery
from celery_app import c
import time

app = Flask(__name__)

import requests, json, os, random, traceback, oss2
from imp import reload
import datetime
import basic

reload(basic)
from basic import public

db, ATTACH_ROOT, getToday = public.db, public.ATTACH_ROOT, public.getToday
oUSER, oPT_GOODS, oMALL = public.oUSER, public.oPT_GOODS, public.oMALL
from qiniu import Auth, put_stream, put_data, put_file, BucketManager
from basic.wxbase import wx_minapp_login, WXBizDataCrypt, WxPay


# app.config['MAIL_SERVER'] = ''
# app.config['MAIL_PORT'] = 994
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_DEBUG'] = True
# app.config['MAIL_DEFAULT_SENDER'] = ''
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ""

# mails=Mail(app)

@c.task
def backup_db():  #####备份数据库

    try:
        sql = "insert into backup_log(bname,btime,ctime)values('数据库备份进入开始',now(),now())"
        db.query(sql)
    except:
        return
    sql = "select access_key,secret_key,name,domain,endpoint,COALESCE(ctype,0) from qiniu where usr_id=1"
    l, t = db.select(sql)
    if t == 0:
        return
    sql = "select dbname from toll_config"
    lT, iN = db.select(sql)
    if iN == 0:
        return
    access_key, secret_key, name, domain, endpoint, ctype = l[0]
    dbname = lT[0][0]
    try:
        datets = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ts = time.strftime('%Y%m%d%H%M%S', time.localtime())
        MaLiShop = '%s%s' % (dbname, ts)
        bat = '/usr/local/bin/pg_dump --file "/var/data_h/%s.sql" --host localhost --port "5432" --username "postgres" --no-password --verbose --format=c --blobs "%s"' % (
            MaLiShop, dbname)
        os.system(bat)

        path = '/var/data_h/%s.sql' % MaLiShop
        if os.path.isfile(path):

            if ctype == 0:
                key = '%s.sql' % MaLiShop
                q = Auth(access_key, secret_key)
                token = q.upload_token(name, key, 3600)
                ret, info = put_file(token, key, path)
                if ret.get('key') == key:

                    try:
                        sql = "insert into backup_log(bname,btime,ctime,type)values('%s','%s',now(),1)" % (key, datets)
                        db.query(sql)
                        os.remove(path)
                    except:
                        pass
            else:
                key = '/backup_db/%s.sql' % MaLiShop
                auth = oss2.Auth(access_key, secret_key)
                bucket = oss2.Bucket(auth, endpoint, name)
                result = bucket.put_object_from_file(key, path)  # 上传
                if result.status == 200:

                    try:
                        sql = "insert into backup_log(bname,btime,ctime,type)values('%s','%s',now(),2)" % (key, datets)
                        db.query(sql)
                        os.remove(path)
                    except:
                        pass
    except:
        try:
            sql = "insert into backup_log(bname,btime,ctime)values('数据库备份出错',now(),now())"
            db.query(sql)
        except:
            pass



if __name__ == '__main__':
    app.run()
