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
from basic.publicw import cVIEWS_ad,CHtml


class cVIEWS(cVIEWS_ad):

    def __init__(self, request):

        self.objHandle = request

        self.REQUEST = self.objHandle.values
        self.RQ = self.REQUEST
        self.Html=CHtml()
        self._http = requests.Session()
        self.dl = None
        self.classpath = 'admin'
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
            , 'hidden': self.hidden, 'qqid': self.qqid,'base_url':self.dl.base_url,
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
    def goPartDelete(self):
        dR = self.dl.delete_data()
        return self.jsons(dR)

    def goPartUpload(self):

        url = self.dl.qiniu_Upload()
        return self.jsons({'url':url})

    def goPartInsert(self):
        dR = self.dl.local_add_save()
        return self.jsons(dR)

    def goPartAjax(self):
        actions='local_ajax_%s'% self.dl.GP('action', '')
        dR = getattr(self.dl, actions)()
        return self.jsons(dR)#self.dl.json_encode(dR)

    def make_sub_path(self, sPATH):
        """检查os的最后一级子目录，如果不存在，生成之"""
        if os.path.exists(sPATH) == 0:
            os.makedirs(sPATH)
        return 0

    def goPartAjax_delete(self):
        dR = self.dl.ajax_delete_data()
        return self.jsons(dR)

    def goPartAjax_del(self):
        dR = self.dl.ajax_del_data()
        return self.jsons(dR)

    def goPartQiniuUpload(self):
        url = self.dl.qiniu_Upload()
        return self.jsons({'url':url})


    def getBreadcrumb(self):

        breadcrumb = ''
        if self.mnuid:

            menu1 = self.dl.getMenuNameById(self.mnuid)
            if menu1:
                breadcrumb += (
                            '<li style="float:left;"><strong>%s</strong></li>' % (
                    menu1))
        if self.sub1id:
            menu2 = self.dl.getMenuNameById(self.sub1id)
            if menu2:
                breadcrumb += ('<li style="float:left;"><a href="%s?viewid=%s">%s</a></li>' %
                               (self.classpath,self.viewid, menu2))

        if self.sub2id:
            menu3 = self.dl.getMenuNameById(self.sub2id)
            if menu3:
                breadcrumb += ('<li style="float:left;"><a href="%s?viewid=%s">%s</a></li>' %
                               (self.classpath,self.viewid, menu3))
        # breadcrumb = ol.getHTML()
        self.assign('breadcrumb', breadcrumb)


    def getPagination(self, PL):
        self.cur_page = PL[0]
        self.total_pages = PL[1]
        PagiUrl = self.initPagiUrl()
        html_pager = self.pagination(PL[2], self.cur_page, url=PagiUrl)
        self.assign('html_pager', html_pager)

    def initHiddenMain(self):
        txtUrlData = ''
        for k, v in self.UrlData.items():
            if v and v != '':
                txtUrlData += '&%s=%s' % (k, v)
        self.hidden['UrlData'] = txtUrlData

    def initHiddenLocal(self):
        txtUrlData = ''
        for k, v in self.UrlData.items():
            if v and v != '':
                txtUrlData += '&%s=%s' % (k, v)
        self.hidden['qqid'] = self.qqid
        self.hidden['UrlData'] = txtUrlData

    def getBackBtn(self):
        if not self.backurl:
            listLink = "%s&pageNo=%s" % (self.sUrl, self.pageNo)
        else:
            listLink = self.backurl
        listLink += self.getAddUrlStr()
        oncl = "window.location = '%s';" % listLink
        sUrlBack = '''
            <input type="button" class="btn btn-success btn-sm" value="返回列表"  onClick="%s"/>''' % oncl
        self.assign('sUrlBack', sUrlBack)

    def getAddUrlStr(self):
        addUrlStr = ''
        for e in self.addUrlData.keys():
            if self.addUrlData[e] and self.addUrlData[e] != '':
                addUrlStr += '&%s=%s' % (e, self.addUrlData[e])
        txtUrlData = self.dl.GP('UrlData')
        if txtUrlData and txtUrlData != '':
            addUrlStr = txtUrlData
        return addUrlStr

    def getAddUrlStrA(self):
        return self.getAddUrlStr()

    def showMsgLink(self, dR):
        R = dR['R']
        if str(R) == '1':  # 错误
            s = self.mScriptMsg(dR['MSG'])
        else:
            if dR.get('isadd', '') != '':
                self.pageNo = 1
            url = '%s?viewid=%s&pageNo=%s' % (self.classpath, self.viewid, self.pageNo)
            url2 = '%s&part=localfrm&pk=%s&mode=%s' % (url, self.pk, self.mode)

            if 'add_save' in self.REQUEST and self.pk != '':
                if dR.get('furl', '') != '':  # 返回表单链接
                    url2 = dR.get('furl', '')
                url2 += self.getAddUrlStr()
                url += self.getAddUrlStr()
                s = self.mScriptMsg(dR['MSG'] or '数据更新成功',
                                    [[url2, '返回表单 编号：<font style="color:#0000ff;">%s</font>' % self.pk], [url, '返回列表']],
                                    'success')
            else:
                url += self.getAddUrlStr()
                s = self.mScriptMsg(dR['MSG'] or '数据更新成功', [[url, '返回列表']], 'success')
        return s

    def mScriptMsg(self, msg, url=[], type='error'):
        notflag = 0
        icon = ''
        if type == 'error' or type == 'danger':
            type = 'danger'
            icon = 'times-circle'
            notflag = 1
        elif type == 'success':
            icon = 'check'
            self.dl.cookie.setcookie("__flag", '', 0)

        if not url:
            url = [['javascript:history.go(-1);', '点击这里返回上一页']]

        link = ''
        for u in url:
            link += '[<a href="%s">%s</a>] ' % (u[0], u[1])
        self.assign({'type': type, 'icon': icon, 'msg': msg, 'link': link, 'notflag': notflag})
        return self.runApp('showmsg.html')

    def pagination(self, count, page, pagesize=10, url='', params={}):
        pagenum = 6
        prepage = pagesize
        curpage = int(page)
        pagestr = ''

        start = (curpage - 1) * pagesize + 1
        end = start + pagesize - 1
        if end > count:
            end = count

        if url.find('?') >= 0:
            url += '&'
        else:
            url += '?'
        paramurl = '&'.join('%s=%s' % (k, v) for k, v in params.items())
        if paramurl != '': url += paramurl + '&'
        # print url
        realpages = 1
        if (float(count) > prepage):
            t = float(count) / prepage
            if t > int(t):
                realpages = int(t) + 1
            else:
                realpages = int(t)
            # realpages = @ceil()
            if (realpages < pagenum):
                froms = 1;
                to = realpages;
            else:
                offset = (pagenum / 2)
                froms = curpage - offset
                to = froms + pagenum
                if (froms < 1):
                    froms = 1
                    to = froms + pagenum - 1
                elif (to > realpages):
                    to = realpages
                    froms = realpages - pagenum + 1

            pagestr += '<li><a href="%spageNo=1">第一页</a></li>' % url
            if curpage - 1 > 0: pagestr += '<li><a href="%spageNo=%s">上一页</a></li>' % (url, curpage - 1)

            for i in range(int(froms), int(to) + 1):
                if (i == curpage):
                    pagestr += '<li class="active"><a>%s</a></li>' % (i)
                else:
                    pagestr += '<li><a href="%spageNo=%s">%s</a></li>' % (url, i, i)
            if (curpage < realpages): pagestr += '<li><a href="%spageNo=%s">下一页</a></li>' % (url, curpage + 1)
            pagestr += '<li><a href="%spageNo=%s">最后页</a></li>' % (url, realpages)
            pagestr = '<ul class="pagination" style="display:inline-block;padding-left:80px;">%s</ul>' % (pagestr)
            sty = 'width:60px;height:33px;line-height:33px;border:1px solid #ddd;text-align:center;'
            pagestr = '''
                        <div class="pagination_div" style="text-align:center;">
                                %s
                            <div class="jumppage"  style="position:relative;float:right;display:inline-block;width:350px;margin:20px 180px 20px auto;">
                                <span style="color:#333333;">共有&nbsp;%s&nbsp;条记录,此为第%s-%s条</span>
                                <span>跳到第&nbsp;</span> <input style="%s" type="text" name="jumppage" onkeyup="checkNum(this)" value="%s" />&nbsp;页
                                &nbsp;<div style="%s background:#f0f0f0;display:inline-block;position:absolute;top:1px;cursor:pointer" onclick="jumppage()">确定</div>
                            </div>
                            <div style="clear:both"></div>
                        </div>
                        <script>
                            function gotopage(page){
                                var keywork=$('input[name=help_search_input]').val();
                                var page=checkPage(page)
                                var url="%s";
                                if($("input[name=pageSize]").length > 0){
                                    var pageSize=$("input[name=pageSize]").val();
                                    url += "&pageSize="+pageSize;
                                }
                                window.location.href=url+"&pageNo="+page;
                            }

                            function jumppage(){
                                var page=$("input[name=jumppage]").val();
                                gotopage(page);
                            }
                            function checkNum(obj){
                                if(!$(obj).val().match(/^[0-9]+[0-9]*]*$/)){
                                    $(obj).val('1');
                                }
                            }

                            function checkPage(page){
                                var total=$("input[name=total]").val();
                                var pageSize=$("input[name=pageSize]").val();
                                var total_pages=Math.ceil(total/pageSize);
                                if ( parseInt(page,10) < 1 || total_pages==0){
                                    page=1;
                                }else{
                                    if (parseInt(page,10) > parseInt(total_pages,10)){
                                        page=parseInt(total_pages,10);
                                    }
                                }
                                return page;
                            }
                        </script>
                    ''' % (pagestr, count, start, end, sty, curpage, sty, url)

        return pagestr


    def qiniu_upload_file(source_file, save_file_name):
        # 生成上传 Token，可以指定过期时间等
        # token = q.upload_token(bucket_name, save_file_name)
        #
        # ret, info = put_data(token, save_file_name, source_file.stream)
        #
        # print(type(info.status_code), info)
        # if info.status_code == 200:
        #     return domain_prefix + save_file_name
        return None








