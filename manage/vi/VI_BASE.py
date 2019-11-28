# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""manage/vi/VI_BASE.py"""


import os

from qiniu import Auth, put_stream, put_data
#需要填写你的 Access Key 和 Secret Key
#access_key = app.config['QINIU_ACCESS_KEY']
#secret_key = app.config['QINIU_SECRET_KEY']
#构建鉴权对象
#q = Auth(access_key, secret_key)
#要上传的空间
#bucket_name = app.config['QINIU_BUCKET_NAME']
#domain_prefix = app.config['QINIU_DOMAIN']
from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import manage.vi.VIEWS
    reload(manage.vi.VIEWS)
from manage.vi.VIEWS             import cVIEWS


class cVI_BASE(cVIEWS):

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

    def cbx(self, name, default='', arg=dict, mtc_type='', types='checkbox', isbr=0):
        # 参数说明
        # 1 元素name
        # 2 默认选中id串 格式"1,2,3,4" (checkbox允许多个值，radio只允许单个值)
        # 3 属性 参考源文件
        # 4 mtc类型 / 或者直接 传 数据数组格式[[id,text]]
        # 5 元素类型（checkbox，radio）
        # 6 是否换行 0不换行 其他按所填数量换行
        default = '%s' % default
        dl = default.split(',')
        cbx = ''
        if type(mtc_type) == type([]):
            o = mtc_type
        else:
            o = self.dl.getmtcdata(mtc_type, '')
        n = 0
        for i in o:
            br = ''
            if isbr != 0 and n % isbr == 0:
                br = "<br>"

            if types == 'checkbox':
                b = ''
                if str(i[0]) in dl:
                    b = '1'

                p1 = [i[0], i[1], b]
                if i[0] != '':
                    cbx += self.Html.checkbox(p1, name, arg) + br
            else:
                narg = {}
                if i[0] != '':
                    if str(i[0]) == str(dl[0]):
                        narg['checked'] = '1'
                    else:
                        narg = arg
                    cbx += '<label class="checkbox inline">' + self.Html.radio(i[0], name, narg) + i[
                        1] + '</label>' + br
            n += 1
        return cbx

    # 与上边cbx一样，对页面样式修改，占少点位置
    def cbx_s(self, name, default='', arg=dict, mtc_type='', type='checkbox', isbr=0):
        # 参数说明
        # 1 元素name
        # 2 默认选中id串 格式"1,2,3,4" (checkbox允许多个值，radio只允许单个值)
        # 3 属性 参考源文件
        # 4 mtc类型
        # 5 元素类型（checkbox，radio）
        # 6 是否换行 0不换行 其他按所填数量换行
        default = '%s' % default
        dl = default.split(',')
        cbx = ''
        o = self.dl.getmtcdata(mtc_type, '')
        n = 0
        for i in o:
            br = ''
            if isbr != 0 and n % isbr == 0:
                br = "<br>"

            if type == 'checkbox':
                b = ''
                if str(i[0]) in dl:
                    b = '1'

                p1 = [i[0], i[1], b]
                if i[0] != '':
                    cbx += self.Html.checkbox(p1, name, arg) + br
            else:
                narg = {}
                if i[0] != '':
                    if str(i[0]) == str(dl[0]):
                        narg['checked'] = '1'
                    else:
                        narg = arg
                    cbx += '<span >' + self.Html.radio(i[0], name, narg) + '&nbsp;' + i[
                        1] + '</span>&emsp;&nbsp;' + br
            n += 1
        return cbx

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










