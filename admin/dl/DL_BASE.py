# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
"""admin/dl/DL_BASE.py"""

import time
import random
from basic.base import set_cookie
from basic.publicw import PEM_ROOTR,db,CLIENT_NAME,md5code,localurl,dActiveUser,user_menu,access_allow,\
    oSHOP,oUSER,oMALL,oQINIU,oGOODS,oGOODS_D,oORDER_SET,oGOODS_N,oGOODS_G,oOPENID,oSHOP_T,oCATEGORY,\
    oGOODS_SELL,oTOLL,oGOODS_PT,oGOODS_DPT,oPT_GOODS,oUSERS_OSS,oGOODS_H,cDL
from qcloudsms_py import QcloudSms

class cDL_BASE(cDL):

    def __init__(self, objHandle):

        # if objHandle.method == 'POST':
        #     self.RQ = objHandle.form
        # else:
        #     self.RQ = objHandle.args
        self.REQUEST = objHandle.values
        self.PEM_ROOTR = PEM_ROOTR
        self.objHandle = objHandle
        self.db = db
        self.cookie = set_cookie(self.objHandle, CLIENT_NAME)
        self.dActiveUser = {}
        self.account = {}
        session_user = self.cookie.igetcookie("__session")
        self.usr_id = 0
        self.dept_id = 0
        self.usr_id_p = 0
        self.md5code=md5code
        self.debug = []  # 输出str信息

        self.usr_name = ''
        self.usrPic = ''
        self.LANG = {}
        self.lang = ''
        self.localurl = localurl
        self.usr_name = ''

        # 获取网址请求过来的常用参数

        self.viewid = self.GP('viewid', 'home')#self.REQUEST.get('viewid', 'home')  # viewid值
        self.initMenuData()  # 初始当前菜单的数据

        # *****************************************************************
        self.part = self.GP('part', 'list')#self.REQUEST.get('part', 'list')

        self.mode = self.GP('mode', 'view')#self.REQUEST.get('mode', 'view')
        self.backUrl = self.REQUEST.get('backUrl', '')  # 登陆后跳转
        self.qqid = self.GP('qqid', '')#self.REQUEST.get('qqid', '').replace("'", "''")
        self.pk = self.GP('pk','')#self.REQUEST.get('pk', '')  # 表单参数
        self.pageNo = self.GP('pageNo', '')#self.REQUEST.get('pageNo', '')

        if self.pageNo == '': self.pageNo = '1'
        self.pageNo = int(self.pageNo)

        # *********************************************************获取网址请求过来的常用参数
        self.src = self.viewid
        self.system_menu = {}

        self.lR = ['', '', '', '']
        self.access = True
        self.modifyUrl = False

        if session_user and self.viewid not in ['login']:

            self.usr_id = int(session_user['value'])  # self.REQUEST.SESSION.get('usr_id')
            if not dActiveUser or not dActiveUser.get(self.usr_id):
                # print 'load user'
                f = self.checkuser(self.usr_id)

            # 当前用户

            self.dActiveUser = dActiveUser.get(self.usr_id, {})
            self.usr_name = self.dActiveUser.get('usr_name', '')
            self.usr_id_p = self.dActiveUser.get('usr_id_p', '')
            self.dept_id = self.dActiveUser.get('dept_id', '')
            # self.bIsAdmin 表示是否为系统管理员

            if not 'roles' in self.dActiveUser:  ###没有此key就跳转到login页重新登录,防止后面语句报错. zhili.lu 2015-01-17
                result = self.cookie.clearcookie("__session")

            if 1 in self.dActiveUser['roles'].keys():
                self.bIsAdmin = 1
            else:
                self.bIsAdmin = 0

            # lR 的 顺序是 增，删 ，改，查。用来控制框架的几个基本权限。
            # 增 lR[0] == '' 时有权限，能控制增加按钮的显示
            # 删 lR[1] == '' 时有权限，能控制删除按钮的显示
            # 改 lR[2] == '' 时有权限，能控制修改按钮的显示
            # 查 lR[3] == '' 时有权限，能控制是否显示列表信息，以及查询框

            #####修改后
            if user_menu.get(self.usr_id, {}):
                self.system_menu = user_menu.get(self.usr_id, {})
            else:
                menu1, menu2, menu3 = self.getSysMenu(self.usr_id)
                if self.usr_id in user_menu:
                    user_menu[self.usr_id] = {
                        'menu1': menu1, 'menu2': menu2, 'menu3': menu3
                    }
                else:
                    user_menu.update({self.usr_id: {
                        'menu1': menu1, 'menu2': menu2, 'menu3': menu3
                    }})
                self.system_menu = user_menu.get(self.usr_id, {})

            roleData = None
            if self.bIsAdmin == 0:
                if self.sub1id != -1:
                    # self.lR=getUsrRight(self.dActiveUser.get('menu_role') , self.sub1id,self.sub2id,self.sub3id)    #当前用户的权限list
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

            self.cur_random_no = "%s%s%s" % (time.time(), self.usr_id, random.random())
            self.account = self.my_account(self.usr_id_p)
        # 用户类型
        self.usr_type = self.dActiveUser.get('usr_type', 0)
        # self.usrPic = self.dMemberUser['member']['pic']
        self.uid = self.account.get('uid', 0)
        self.weid = self.account.get('weid', 0)
        self.access_token_d = {'token': self.account.get("access_token", ''),
                               'expire': self.account.get("expires_in", 0)}
        self.access_token = ''
        self.wx_appKey = self.account.get('key', '')
        self.wx_secret = self.account.get('secret', '')
        self.domain = self.account.get('domain', '')
        #####################################################################
        self.specialinit()
        self.init_data()
        self.myInit()

        self.oSHOP = oSHOP
        self.oUSER = oUSER
        self.oMALL = oMALL
        self.oQINIU=oQINIU
        #self.oKUAIDI=oKUAIDI
        self.oGOODS=oGOODS
        self.oGOODS_D=oGOODS_D
        self.oORDER_SET=oORDER_SET
        self.oGOODS_N=oGOODS_N
        self.oGOODS_G=oGOODS_G
        self.oOPENID=oOPENID
        self.oSHOP_T=oSHOP_T
        self.oCATEGORY=oCATEGORY
        self.oGOODS_SELL = oGOODS_SELL
        self.oTOLL = oTOLL.get()
        self.oGOODS_PT = oGOODS_PT
        self.oGOODS_DPT = oGOODS_DPT
        self.oPT_GOODS = oPT_GOODS
        self.oUSERS_OSS = oUSERS_OSS
        self.oGOODS_H=oGOODS_H
        # #####################################################################

        # ########七牛公共调用

        self.qiniu_access_key_all = self.oTOLL.get('access_key')
        self.qiniu_secret_key_all = self.oTOLL.get('secret_key')
        self.qiniu_bucket_name_all = self.oTOLL.get('bucket')
        self.qiniu_domain_all = self.oTOLL.get('qiniu_domain')

        #
        # ##########
        self.ali_appid= self.oTOLL.get('ali_appid')
        self.app_private_key= self.oTOLL.get('app_private_key')
        self.ali_public_key= self.oTOLL.get('ali_public_key')
        self.sms_appid = self.oTOLL.get('sms_appkey')
        self.sms_appkey = self.oTOLL.get('sms_appsecret')
        self.SMS_template_id = self.oTOLL.get('sms_appcode')
        self.try_out = self.oTOLL.get('try_out')
        self.combo_one_name = self.oTOLL.get('combo_one_name')
        self.combo_one_price = self.oTOLL.get('combo_one_price')
        self.combo_one_day = self.oTOLL.get('combo_one_day')
        self.combo_two_name = self.oTOLL.get('combo_two_name')
        self.combo_two_price = self.oTOLL.get('combo_two_price')
        self.combo_two_day = self.oTOLL.get('combo_two_day')
        self.combo_thr_name = self.oTOLL.get('combo_thr_name')
        self.combo_thr_price = self.oTOLL.get('combo_thr_price')
        self.combo_thr_day = self.oTOLL.get('combo_thr_day')
        self.call_url = self.oTOLL.get('call_url')
        self.re_url = self.oTOLL.get('re_url')
        self.wx_appid=self.oTOLL.get('appid')
        self.wx_secret=self.oTOLL.get('secret')
        self.wxstatus=self.oTOLL.get('wxstatus')
        self.SMS_SEND = QcloudSms(self.sms_appid, self.sms_appkey)
        #
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

    def getSysMenu(self, usr_id):

        sql = """
            select mf.menu
                  ,mf.menu_id
                  ,mf.func_id
                  ,mf.menu_name
                  ,mf.type
                  ,mf.sort
                  ,mf.parent_id
                  ,mf.img
              from menu_func mf
             where mf.menu_id in (select rm.menu_id
                                    from usr_role ur
                                        ,role_menu rm
                                   where exists (select 1 from roles r where r.role_id = ur.role_id)
                                     and exists (select 1 from menu_func m where m.status =1 and  m.menu_id = rm.menu_id)
                                     and ur.role_id= rm.role_id
                                     and ur.usr_id = %s)
             order by mf.sort asc
                """
        parm=[usr_id]
        if usr_id == 1:
            sql = """
                select mf.menu
                      ,mf.menu_id
                      ,mf.func_id
                      ,mf.menu_name
                      ,mf.type
                      ,mf.sort
                      ,mf.parent_id
                      ,mf.img
                  from menu_func mf
                 where mf.status=1
                 order by mf.sort asc
            """
            parm = []
        L, iN = self.db.fetchall(sql,parm)

        menu1 = []
        menu2 = {}
        menu3 = {}
        # print sql
        for row in L:
            if row.get('menu') == 1:
                menu1.append([row['menu_id'], row['menu_name'], row['func_id'], row['img']])
            elif row.get('menu') == 2:
                if not row.get('parent_id') in menu2:
                    menu2[row.get('parent_id')] = []
                menu2[row.get('parent_id')].append([row['menu_id'], row['menu_name'], row['func_id'], row['parent_id'], row['img']])
            elif row.get('menu') == 3:
                if not row.get('parent_id') in menu3:
                    menu3[row.get('parent_id')] = []
                menu3[row.get('parent_id')].append([row['menu_id'], row['menu_name'], row['func_id'], row['parent_id'], row['img']])

        return menu1, menu2, menu3

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
        dActiveUser[usr_id]['usr_id_p'] = lT[0][3]  # 登陆ID
        dActiveUser[usr_id]['dept_id'] = lT[0][3]  #部门ID


        sql = """SELECT WUR.role_id,WR.role_name,WR.sort,WR.dept_id
               FROM usr_role WUR LEFT JOIN roles WR ON WUR.role_id=WR.role_id
               WHERE WUR.usr_id=%s
            """
        lT1, iN1 = self.db.select(sql,usr_id)
        if iN1 > 0:
            for e in lT1:

                dActiveUser[usr_id]['roles'][e[0]] = e[1:]

        dActiveUser[usr_id]['menu_role'] = self.get_usr_menu_role(usr_id, dActiveUser[usr_id]['roles'])
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

    def specialinit(self):
        pass

    def init_data(self):
        pass

    def myInit(self):
        pass

    def parse_GNL(self, list=[]):
        L = []
        for n in list: L.append(self.FDT[n])
        return L

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

    def getip(self):
        return self.objHandle.remote_addr

    def my_account(self,usr_id_p):
        sql = "SELECT * FROM ims_wechats where usr_id=%s"
        account = self.db.fetch(sql,[usr_id_p])
        return account


    # 是否登陆
    def isLogin(self):
        if self.dActiveUser:
            return 1
        else:
            return 0

        # 面包屑网站地图
    def getMenuNameById(self, id):
        if not id:
            return ''
        return self.db.fetchcolumn("select menu_name from menu_func where menu_id = %s" , id)

    def delete_data(self):
        return {'R': '0', 'MSG': ''}




    def send_SMS_msg(self, mobile, passwd, Vtime='10'):

        # 需要发送短信的手机号码
        phone_numbers = "%s" % mobile
        # 短信模板ID，需要在短信应用中申请
        template_id = self.SMS_template_id  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
        # 签名
        from qcloudsms_py.httpclient import HTTPError
        # 创建单发短信(SmsSingleSender)对象
        ssender = self.SMS_SEND.SmsSingleSender()
        # ssender = SmsSingleSender(appid, appkey)
        params = [passwd, Vtime]  # 当模板没有参数时，`params = []`
        try:
            result = ssender.send_with_param(86, phone_numbers,
                                             template_id, params, sign="", extend="",
                                             ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
            code = result.get('result', '')
            if code == 0:
                return 0
            return 1
        except HTTPError as e:
            return 1
        except Exception as e:
            return 1






