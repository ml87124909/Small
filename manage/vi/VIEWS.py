# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/VIEWS.py"""

from flask import redirect, jsonify
from jinja2 import Environment, PackageLoader
import requests
from basic.publicw import cMANAGE_V,CHtml


class cVIEWS(cMANAGE_V):

    def __init__(self, request):

        self.objHandle = request

        self.REQUEST = self.objHandle.values
        self.RQ = self.REQUEST
        self.Html=CHtml()
        self._http = requests.Session()
        self.dl = None
        self.classpath = 'manage'
        self.sTitle, self.site_name = '', ''
        self.js = []
        self.css = []
        self.var = {}
        self.isPDF = 0  # 是否有PDF  0:无  1:有
        self.isFile = 0  # 是否有附件文件 0:无  1:有
        self.need_editor = 0
        self.setClassName()
        self.mInstantiate_odl()

        self.module = self.dl.viewid  # fid值
        self.viewid = self.dl.viewid
        self.name = self.dl.part
        self.part = self.name
        self.backUrl = self.dl.backUrl  # 登陆后跳转
        self.mnuid = self.dl.mnuid
        self.sub1id = self.dl.sub1id
        self.sub2id = self.dl.sub2id
        self.system_menu = self.dl.system_menu
        self.classname = self.viewid
        self.sUrl = '%s?viewid=%s' % (self.classpath, self.viewid)  # 基本的url
        self.addUrlData = {}  ##返回列表链接追回参数  数据更新 删除 表单返回
        self.UrlData = {}

        self.list_tab = []  # child ['title' , '' ,'_self',''] title , link , taget , ex_number
        self.tablist = self.REQUEST.get('tablist', 1)

        #################将列表GRID界面传过来的选择框的值暂存起来，以便在使用'返回列表'命令时，将这些值还原给原来界面那些选择框，以达到返回原来界面的目的###########
        self.pk = self.dl.pk  # 表单参数
        self.pageNo = self.dl.pageNo
        self.total_pages = 0
        self.cur_page = 1
        self.qqid = self.dl.qqid

        self.backurl = '%s?viewid=%s&pageNo=%s' % (self.classpath, self.viewid, self.pageNo)
        self.lR = ['', '', '', '']  # 增，改，删，查
        self.lR = self.dl.lR

        self.tType = 'manage'
        self.navTitle = '页面'
        self.specialinit()
        self.hidden = {
            'pk': self.pk,
            'viewid': self.viewid,
            'src': self.viewid,
            'part': self.part,
            'mnuid': self.mnuid,
            'sub1id': self.sub1id,
            'sub2id': self.sub2id,
            'pageNo': self.pageNo,

        }  # 用来存储公共参数以外的个性参数，比如合同管理功能的合同类型gw_type及财务登记模块的付款、取款状态等

        self.requiredIcon = '<font style="font-size:13px;color:red;">&nbsp;*</font>'

    def runApp(self, template='', istpl=True):

        if not template or template == '':
            return ''
        if not istpl:
            return template

        user = {}
        user['usr_id'] = self.dl.usr_id
        user['usr_name'] = self.dl.usr_name
        html_hidden = ''
        for h in self.hidden.items():
            html_hidden += '<input type="hidden" name="%s" value="%s" />' % (h[0], h[1])
        mainData = {
            'sTitle': self.sTitle, 'site_name': self.site_name, 'navTitle': self.navTitle
            , 'localurl': self.dl.localurl, 'session_user': user, 'backUrl': self.backUrl
            , 'cookieprefix': self.dl.cookie.keyname, 'sUrl': self.sUrl, 'pageNo': self.pageNo
            , 'hidden': self.hidden, 'qqid': self.qqid,
            'lR': self.lR, 'viewid': self.viewid
            , 'need_editor': self.need_editor
            , 'html_hidden': html_hidden
            , 'system_menu': self.system_menu
            , 'requiredIcon': self.requiredIcon
            , 'routepath': self.classpath, 'usr_id': self.dl.usr_id
            , 'pic_list': self.dl.pic_list(), 'pic_dict': self.dl.pic_dict()

        }

        self.assign(mainData)

        env = Environment(loader=PackageLoader('%s' % self.classpath, 'html'))
        template = env.get_template('%s' % template)
        html = template.render(self.var)
        return html

    def initPagiUrl(self):
        return self.sUrl

    def initSearchUrl(self):
        return self.sUrl

    def setClassName(self):
        self.dl_name = 'BASE_DL'

    def specialinit(self):
        return

    def redirect(self, url):
        return redirect(url)

    def jsons(self, data):
        return jsonify(data)

    def assign(self, param, value=None):
        if type(param) == str:
            self.var[param] = value
        elif type(param) == dict:
            for k, v in param.items():
                self.var[k] = v








