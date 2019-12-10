# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/dl/DL_BASE.py"""

import time
import random
from basic.base import set_cookie
from basic.publicw import PEM_ROOTR,db,CLIENT_NAME,md5code,localurl,dActiveUser,user_menu,access_allow,\
    oSHOP,oUSER,oMALL,oQINIU,oGOODS,oGOODS_D,oORDER_SET,oGOODS_N,oGOODS_G,oOPENID,oSHOP_T,oCATEGORY,\
    oGOODS_SELL,oGOODS_PT,oGOODS_DPT,oPT_GOODS,oUSERS_OSS,oGOODS_H,cDL,_http,oTOLL
#from qcloudsms_py import QcloudSms

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
        self.qr_ticket = ''
        self._http=_http
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

        self.viewid = self.GP('viewid', 'home')
        self.initMenuData()# 初始当前菜单的数据
        # *****************************************************************
        self.part = self.GP('part', 'list')
        self.backUrl = self.REQUEST.get('backUrl', '')
        self.qqid = self.GP('qqid', '')
        self.pk = self.GP('pk','')
        self.pageNo = self.GP('pageNo', '')

        if self.pageNo == '':
            self.pageNo = '1'
        self.pageNo = int(self.pageNo)

        # *********************************************************获取网址请求过来的常用参数

        self.system_menu = {}

        self.lR = ['', '', '', '']
        self.access = True
        self.modifyUrl = False

        if session_user and self.viewid not in ['login']:

            self.usr_id = int(session_user['value'])
            if not dActiveUser or not dActiveUser.get(self.usr_id):
                f = self.checkuser(self.usr_id)
            self.dActiveUser = dActiveUser.get(self.usr_id, {})
            self.usr_name = self.dActiveUser.get('usr_name', '')
            self.usr_id_p = self.dActiveUser.get('usr_id_p', '')
            self.dept_id = self.dActiveUser.get('dept_id', '')


            if not 'roles' in self.dActiveUser:
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

        #####################################################################
        self.specialinit()
        self.init_data()
        self.myInit()

        self.oSHOP = oSHOP
        self.oUSER = oUSER
        self.oMALL = oMALL
        self.oQINIU=oQINIU
        self.oGOODS=oGOODS
        self.oGOODS_D=oGOODS_D
        self.oORDER_SET=oORDER_SET
        self.oGOODS_N=oGOODS_N
        self.oGOODS_G=oGOODS_G
        self.oOPENID=oOPENID
        self.oSHOP_T=oSHOP_T
        self.oCATEGORY=oCATEGORY
        self.oGOODS_SELL = oGOODS_SELL
        self.oGOODS_PT = oGOODS_PT
        self.oGOODS_DPT = oGOODS_DPT
        self.oPT_GOODS = oPT_GOODS
        self.oUSERS_OSS = oUSERS_OSS
        self.oGOODS_H=oGOODS_H
        self.oTOLL=oTOLL
        # #####################################################################

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
        self.base_url = self.oTOLL.get().get('base_url')#平台支付回调域名
        #self.wx_appid = self.oTOLL.get().get('appid')
        #self.wx_secret = self.oTOLL.get().get('secret')
        self.pay_status = self.oTOLL.get().get('pay_status')
        self.try_days = self.oTOLL.get().get('try_days')
        self.invite_days = self.oTOLL.get().get('invite_days')
        self.vip_days = self.oTOLL.get().get('vip_days')
        self.wxstatus = self.oTOLL.get().get('wx_status')
        #######

    def GP(self, key, default=None, ctype=1):
        value = self.REQUEST.get(key, default)
        #L_error = ['"', "'", '%', '#', '&', '*', '(', ')', '@', '`', '\\', ']', '=', '<', '>','?',':','//','/']
        L_error = ['"', "'", '%', '#', '&', '*', '(', ')', '@', '`', '\\', ']', '=', '<', '>', '?']
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











