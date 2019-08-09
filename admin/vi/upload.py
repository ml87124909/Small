# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/upload.py"""

import os
import time
import hashlib
from flask import jsonify
from werkzeug import secure_filename
from qiniu import Auth, put_data,BucketManager
import oss2
from basic.base import set_cookie
from basic.publicw import cUP,PEM_ROOTR,db,CLIENT_NAME,md5code,dActiveUser,access_allow,oQINIU,oUSERS_OSS

class cupload(cUP):


    def __init__(self,request):

        self.objHandle = request
        self.REQUEST = self.objHandle.values
        self.PEM_ROOTR=PEM_ROOTR
        self.db = db
        self.cookie = set_cookie(self.objHandle, CLIENT_NAME)
        self.dActiveUser = {}
        self.access=True
        session_user = self.cookie.igetcookie("__session")
        self.usr_id = 0
        self.dept_id = 0
        self.usr_id_p = 0
        self.lR = ['', '', '', '']  # 增，改，删，查
        self.viewid = self.GP('viewid', 'home')
        self.initMenuData()  # 初始当前菜单的数据
        # *****************************************************************
        self.part = self.GP('part', '')
        if session_user:
            self.usr_id = int(session_user['value'])  # self.REQUEST.SESSION.get('usr_id')
            if not dActiveUser or not dActiveUser.get(self.usr_id):
                result = self.cookie.clearcookie("__session")

            self.dActiveUser = dActiveUser.get(self.usr_id, {})
            self.usr_id_p = self.dActiveUser.get('usr_id_p', '')
            self.dept_id = self.dActiveUser.get('dept_id', '')

            if not 'roles' in self.dActiveUser:
                result = self.cookie.clearcookie("__session")
            if 1 in self.dActiveUser['roles'].keys():
                self.bIsAdmin = 1
            else:
                self.bIsAdmin = 0
            roleData = None
            if self.bIsAdmin == 0:
                if self.sub1id != -1:
                    roleData = self.dActiveUser.get('menu_role').get(self.sub1id)
                elif self.mnuid != -1:
                    roleData = self.dActiveUser.get('menu_role').get(self.mnuid)
                # else:
                if roleData:
                    n = 0
                    for r in roleData:
                        if r == 0:
                            self.lR[n] = '1'
                        n = n + 1
                elif self.viewid not in access_allow:
                    self.lR = ['1', '1', '1', '1']
                    self.access = False

            else:
                self.lR = ['', '', '', '']

        self.SECRET_KEY='5bf030dbb13422031ea802a9ab75900a'

        # *****************************************************************
        self.oQINIU = oQINIU
        self.oUSERS_OSS = oUSERS_OSS

    # ###########################################
        ########OSS用户自有调用
        self.oss_ctype = self.oQINIU.get(self.usr_id_p).get('ctype', '')
        self.oss_access_key = self.oQINIU.get(self.usr_id_p).get('access_key', '')
        self.oss_secret_key = self.oQINIU.get(self.usr_id_p).get('secret_key', '')
        self.oss_bucket_name = self.oQINIU.get(self.usr_id_p).get('cname', '')
        self.oss_domain = self.oQINIU.get(self.usr_id_p).get('domain_url', '')
        self.oss_endpoint = self.oQINIU.get(self.usr_id_p).get('endpoint', '')
        ########OSS公共调用
        self.oss_ctype_all = self.oQINIU.get(1).get('ctype', '')
        self.oss_access_key_all = self.oQINIU.get(1).get('access_key', '')
        self.oss_secret_key_all = self.oQINIU.get(1).get('secret_key', '')
        self.oss_bucket_name_all = self.oQINIU.get(1).get('cname', '')
        self.oss_domain_all = self.oQINIU.get(1).get('domain_url', '')
        self.oss_endpoint_all = self.oQINIU.get(1).get('endpoint', '')
        ########计算处理
        self.oss_all = self.oUSERS_OSS.get(self.usr_id_p).get('oss_all', 0)
        self.oss_now = self.oUSERS_OSS.get(self.usr_id_p).get('oss_now', 0)
        self.qiniu_flag = self.oUSERS_OSS.get(self.usr_id_p).get('qiniu_flag', 0)
        self.oss_flag = self.oUSERS_OSS.get(self.usr_id_p).get('oss_flag', 0)
        #########



    def GP(self, key, default=None, ctype=1):
        value = self.REQUEST.get(key, default)
        L_error = ['"', "'", '%', '#', '&', '*', '(', ')', '@', '`', '\\', ']', '=', '<', '>','?']
        if ctype==1 and value and isinstance(value, str):
            for c in L_error:
                if c in value:
                    value=value.replace(c,'')
        return value

    def initMenuData(self):

        self.mnuid = -1  # menuid值
        self.menu_name = ''
        self.parent_name = ''
        self.sub1id = -1  # sub1id值
        self.sub2id = -1  # sub2id值
        if self.viewid == 'menu':
            self.mnuid = self.GP('mnuid')
        sql = u"""
        SELECT 
          mf.menu_id,mf.menu_name
          ,COALESCE(mf.parent_id,null) AS parent_id
          ,COALESCE(mf2.menu_name,null) AS parent_name
          ,COALESCE(mf2.parent_id,null) AS parent_id2
          ,COALESCE(mf3.menu_name,null) AS parent_name2
          FROM menu_func AS mf 
          LEFT JOIN menu_func AS mf2 ON mf2.menu_id = mf.parent_id
          LEFT JOIN menu_func AS mf3 ON mf3.menu_id = mf2.parent_id
          WHERE mf.func_id = %s and mf.status=1"""

        data = self.db.fetch(sql,self.viewid)
        if data:
            if data.get('parent_id2'):
                self.mnuid = int(data.get("parent_id2", -1))
                self.sub1id = int(data.get("parent_id", -1))
                self.sub2id = int(data.get("menu_id", -1))
                self.menu_name = data.get("menu_name", '')
                self.parent_name = data.get("parent_name", '')
            elif data.get("parent_id"):
                self.mnuid = int(data.get("parent_id", -1))
                self.sub1id = int(data.get("menu_id", -1))
                self.menu_name = data.get("menu_name", '')
                self.parent_name = data.get("parent_name", '')
            else:
                self.mnuid = int(data.get("menu_id", -1))
                self.menu_name = data.get("menu_name", '')
                

    def make_sub_path(self, sPATH):
        """检查os的最后一级子目录，如果不存在，生成之"""
        if os.path.exists(sPATH) == 0:
            os.makedirs(sPATH)
        return 0

    def jsons(self, data):
        return jsonify(data)


    
    def checkuser(self, usr_id):

        sql = """
        SELECT U.usr_id                   -- 0
              , convert_from(decrypt(U.login_id::bytea,%s, 'aes'),'SQL_ASCII')                -- 1
              ,U.dept_id                  -- 2
              ,case when COALESCE(u.usr_id_p,0)=0 then U.usr_id else u.usr_id_p end     -- 3
           FROM users U 
           WHERE U.usr_id=%s AND  U.status=1
        """

        lT, iN = self.db.select(sql,[md5code,usr_id])
        if not iN:
            return 0

        usr_name = lT[0][1]

        # 求得用户的权限
        dActiveUser[usr_id] = {}
        dActiveUser[usr_id]['roles'] = {}  # 用户角色
        dActiveUser[usr_id]['login_time'] = time.time()  # 登入时间
        dActiveUser[usr_id]['usr_name'] = usr_name
        dActiveUser[usr_id]['usr_id'] = usr_id  # 用户名
        dActiveUser[usr_id]['login_id'] = usr_name  # 登陆ID
        dActiveUser[usr_id]['usr_id_p'] = lT[0][3]  # 主ID
        dActiveUser[usr_id]['dept_id'] = lT[0][3]  #部门ID

        ###################################################################如果是无权限的，
        # sql = """SELECT WUR.role_id,WR.role_name,WR.sort,WR.dept_id
        #        FROM usr_role WUR LEFT JOIN roles WR ON WUR.role_id=WR.role_id
        #        WHERE WUR.usr_id=%s
        #     """
        # lT1, iN1 = self.db.select(sql,usr_id)
        # if iN1 > 0:
        #     for e in lT1:
        #         dActiveUser[usr_id]['roles'][e[0]] = e[1:]
        # dActiveUser[usr_id]['menu_role'] = self.get_usr_menu_role(usr_id, dActiveUser[usr_id]['roles'])
        ######################################################
        return dActiveUser

    def get_usr_menu_role(self, usr_id, roles={}):

        menu_role = {}
        if usr_id == 1:  # 对于管理员，那就妥妥是全部权限都有了
            sql = ''' select menu_id,1 as can_add,1 as can_del,1 as can_upd ,1 as can_see from menu_func m where m.status =1 order by menu_id '''
            L, t = self.db.fetchall(sql)
            for row in L:
                if row['menu_id'] in menu_role:
                    menu_role[row['menu_id']][0] = 1
                    menu_role[row['menu_id']][1] = 1
                    menu_role[row['menu_id']][2] = 1
                    menu_role[row['menu_id']][3] = 1
                else:
                    menu_role[row['menu_id']] = [1, 1, 1, 1]
        else:
            ids = ','.join('%s' % k for k in roles.keys())

            if ids != '':
                sql = '''
                select menu_id , can_add , can_del , can_upd , can_see from role_menu where role_id in (%s) order by menu_id
                ''' % (ids)
                L, t = self.db.fetchall(sql)
                for row in L:
                    if row['menu_id'] in menu_role:
                        menu_role[row['menu_id']][0] = row['can_add'] and row['can_add'] or menu_role[row['menu_id']][0]
                        menu_role[row['menu_id']][1] = row['can_upd'] and row['can_upd'] or menu_role[row['menu_id']][1]
                        menu_role[row['menu_id']][2] = row['can_del'] and row['can_del'] or menu_role[row['menu_id']][2]
                        menu_role[row['menu_id']][3] = row['can_see'] and row['can_see'] or menu_role[row['menu_id']][3]
                    else:
                        menu_role[row['menu_id']] = [row['can_add'], row['can_upd'], row['can_del'], row['can_see']]
        return menu_role



    def goPartImg(self):#保存到七牛
        if self.oss_now > self.oss_all and self.oss_flag != 7 and (self.oss_ctype==2 or self.qiniu_flag==0):
            dR = {'code': '1', 'msg': '您的容量已超！'}
            return self.jsons(dR)
        file = self.objHandle.files['file']  # request的files属性为请求中文件的数据<input 里的name="file">
        url = ''
        if file and self.allowed_file(file.filename):
            # if file.filename.find('.') > 0:
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[-1].lower()
            timeStamp = time.time()
            md5name = hashlib.md5()
            md5name.update(str(timeStamp).encode('utf-8'))
            filename = md5name.hexdigest() + '.' + file_ext
            file_content = file.read()
            file_size = float(len(file_content)) / 1024
            
            
            if self.oss_ctype==2 or self.qiniu_flag==0:#使用平台公共
                if self.oss_ctype_all == 0:
                    access_key=self.oss_access_key_all
                    secret_key=self.oss_secret_key_all
                    bucket_name= self.oss_bucket_name_all
                    domain=self.oss_domain_all
                    url = self.qiniu_upload_file(access_key,secret_key,bucket_name,domain,file_content, filename)
                else:
                    access_key = self.oss_access_key_all
                    secret_key = self.oss_secret_key_all
                    bucket_name = self.oss_bucket_name_all
                    domain = self.oss_domain_all
                    endpoint=self.oss_endpoint_all
                    url = self.ali_upload_file(access_key,secret_key,bucket_name,domain,endpoint,file_content, filename)
            else:#使用自己的
                if self.oss_ctype == 0:
                    access_key = self.oss_access_key
                    secret_key = self.oss_secret_key
                    bucket_name = self.oss_bucket_name
                    domain = self.oss_domain
                    url = self.qiniu_upload_file(access_key,secret_key,bucket_name,domain,file_content, filename)
                else:#1阿里
                    access_key = self.oss_access_key
                    secret_key = self.oss_secret_key
                    bucket_name = self.oss_bucket_name
                    domain = self.oss_domain
                    endpoint = self.oss_endpoint
                    url = self.ali_upload_file(access_key,secret_key,bucket_name,domain,endpoint,file_content, filename)
            if url:
                self.Save_pic_table(file_ext, file_size, filename, url)
            dR = {'code': '0', 'msg': '上传成功', 'url': url}
            return self.jsons(dR)
        dR = {'code': '1', 'msg': '上传失败', 'url': url}
        return self.jsons(dR)


    def goPartPem(self):#PEM证书保存到本地

        file = self.objHandle.files['file']  # request的files属性为请求中文件的数据<input 里的name="file">
        url = ''
        if file and self.PEM_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[-1].lower()
            timeStamp = time.time()
            md5name = hashlib.md5()
            md5name.update(str(timeStamp).encode('utf-8'))
            filename = md5name.hexdigest() + '.' + file_ext
            paths = os.path.join(PEM_ROOTR, '%s' % self.usr_id_p)
            self.make_sub_path(paths)
            file.save(os.path.join(paths, filename))
            url = '/var/data_h/%s/%s/' % (CLIENT_NAME,self.usr_id_p) + filename
            dR = {'code': '0', 'msg': '上传成功','url': url}
            return self.jsons(dR)
        dR = {'code': '1', 'msg': '上传失败', 'url': url}
        return self.jsons(dR)

    def qiniu_upload_file(self,access_key,secret_key,bucket_name,domain,source_file, filename):

        # 构建鉴权对象
        q = Auth(access_key,secret_key)
        token = q.upload_token(bucket_name,filename)
        ret, info = put_data(token, filename, source_file)
        if info.status_code == 200:
            return domain + filename
        return None

    def ali_upload_file(self,access_key,secret_key,bucket_name,domain,endpoint,source_file, filename):
        
        auth = oss2.Auth(access_key, secret_key)
        bucket = oss2.Bucket(auth, endpoint,bucket_name)
        new_filename='%s/'%self.usr_id_p+filename
        result = bucket.put_object(new_filename, source_file)  # 上传
        if result.status == 200:
            return domain + new_filename
        return None

    def PEM_allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ['pem']

    def allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ['bmp', 'png', 'jpg', 'jpeg', 'gif']


    def Save_pic_table(self, f_ext, f_size, filename, url):

        f_year = self.getToday(6)[:4]
        sql = """insert into images(usr_id,f_year,f_ext,f_size,cname,pic,cid,ctime)
                        values(%s,%s,%s,%s,%s,%s,%s,now())"""
        L = [self.usr_id_p, f_year, f_ext, f_size, filename, url, self.usr_id]
        self.db.query(sql, L)
        print(url)
        if ('http://' in url or 'https://' in url) and self.oss_ctype==2 and self.oss_flag!=7:
            nums=(float(f_size) / 1024)
            self.oUSERS_OSS.updates(self.usr_id_p,nums)
            try:
                sqlu = "update users set oss_now=coalesce(oss_now,0)+(%s/1024),utime=now(),uid=%s where usr_id=%s"
                self.db.query(sqlu, [f_size, self.usr_id, self.usr_id_p])
            except Exception as e:
                self.print_log('处理oss_now出错', '%s' % e)
        return
    
    def getToday(self, format=3):
        """返回今天的日期字串"""
        # format=1	yyyymmdd
        # format=2	hh:mm
        # format=3	yyyy/mm/dd
        # format=4	yyyy/mm/dd  hh:mm
        # format=5	yymmdd
        t = time.time()
        date_ary = time.localtime(t)
        if format == 1:
            x = time.strftime("%Y%m%d", date_ary)
        elif format == 2:
            x = time.strftime("%H:%M", date_ary)
        elif format == 3:
            x = time.strftime("%Y/%m/%d", date_ary)
        elif format == 4:
            x = time.strftime("%Y/%m/%d %H:%M", date_ary)
        elif format == 5:
            x = time.strftime("%y%m%d", date_ary)
        elif format == 6:
            x = time.strftime("%Y-%m-%d", date_ary)
        elif format == 7:
            x = time.strftime("%Y/%m/%d %H:%M:%S", date_ary)
        elif format == 8:
            x = time.strftime("%Y-%m-%d %H:%M", date_ary)
        elif format == 9:
            x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
        elif format == 10:
            x = time.strftime("%Y年%m月%d日 %H:%M", date_ary)
        else:
            x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
        
        return x
    
    def print_log(self,cname,errors):
        sql="insert into print_log(cname,errors,ctime)values(%s,%s,now())"
        self.db.query(sql,[cname,errors])
        return



