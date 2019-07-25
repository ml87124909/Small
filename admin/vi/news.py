# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################

from imp import reload
from admin.vi import WxApi
reload(WxApi)

class cnews(WxApi.cWxApi):
    
    def setClassName(self):
        #设定要实例的 BIZ类和TPL类，为空则继承基类，可以能过判断part的值来设置不同的类名
        self.dl_name = 'news_dl'

    def specialinit(self):
        self.navTitle = '图文回复'
        self.getBreadcrumb() #获取面包屑



    #管理公众号
    def goPartList(self):
        keyword = self.dl.GP('keyword','')
        status = self.dl.GP('status','1')
        pagesize = 5
        condition = " module = 'news'"
        sUrl = 'admin?viewid=news'
        param = {}
        childsql = "SELECT  id FROM ims_rule where %s" % condition
        if keyword :
            condition += "  AND name LIKE '%%%s%%'" % keyword
            childsql += "  AND name LIKE '%%%s%%'" % keyword
            param['keyword'] = keyword
        if status :
            condition += "  AND status = '%s'" % status
            childsql += "  AND status = '%s'" % status
            param['status'] = status
        childsql+=" limit %s"%((self.pageNo - 1) * pagesize)


        sql = "SELECT  * FROM ims_rule WHERE %s and id not in (%s) ORDER BY status DESC, displayorder DESC, id ASC limit %s" % (condition,childsql,pagesize)
        #self.dl.log(sql)
        L,t = self.dl.db.fetchall(sql)
        total = self.dl.db.fetchcolumn("select count(*) from ims_rule  where %s" % condition)
        html_pager = self.pagination(total,self.pageNo,pagesize,sUrl)
        self.assign('html_pager',html_pager)
        for i in range(len(L)):
            kws,total = self.dl.db.fetchall("SELECT * FROM ims_rule_keyword WHERE rid = '%s'"%L[i].get('id',''))
            L[i]['keywords'] = kws
        self.assign({
            'status':status,'keyword':keyword , 'list' : L , 'site_url':self.objHandle.environ.get('HTTP_HOST')
        })
        return self.runApp('rule_news.html')

    def goPartLocalform(self):
        rule = {'rule':{},'keyword':{}}
        reply = ''
        keyword = ''
        id = self.dl.GP('id','')
        if id:
            rule['rule'] = self.dl.db.fetch("SELECT * FROM ims_rule WHERE id = '%s'"%id)
            if not rule['rule'] :
                return self.mScriptMsg('抱歉，您操作的规则不在存或是已经被删除！',[['admin?viewid=basic&mnuid=9&sub1id=901','返回列表']])
            rule['keyword'],total = self.dl.db.fetchall("SELECT * FROM ims_rule_keyword WHERE rid = '%s'"%id)
            keyword_array = []
            for kw in rule['keyword']:
                if kw.get('type') != 1:
                    continue
                keyword_array.append(kw.get('content',''))
            keyword = ','.join('%s'%kw for kw in keyword_array)
            reply ,total = self.dl.db.fetchall("select id,title,description,url,thumb,thumbid,content from ims_news_reply where rid = '%s' ORDER BY parentid ASC , id ASC" % id)
        self.assign('rule',rule['rule'])
        self.assign('keyword',keyword)
        self.assign('specialkeyword',rule['keyword'])
        self.assign('replylist',reply)

        return self.runApp('rule_news_post.html')

    def goPartDelete(self):
        dR=self.delete_data()
        R=dR['R']
        if str(R)=='1':    #错误
            s=self.mScriptMsg(dR['MSG'])
        else:
            url  ='?viewid=%s&pageNo=%s'%(self.viewid , self.pageNo)

            url+=self.getAddUrlStrA()
            s=self.mScriptMsg('数据删除成功',[[url,'返回列表']],'success')
        return s

    def delete_data(self):
        dR = {'R':'','MSG':""}
        self.dl.db.query("delete from ims_rule where id = '%s'"%self.pk)
        self.dl.db.query("delete from ims_rule_keyword where rid = '%s'"%self.pk)
        self.dl.db.query("delete from ims_stat_rule where rid = '%s'"%self.pk)
        self.dl.db.query("delete from ims_stat_keyword where rid = '%s'"%self.pk)
        return dR

    def goPartDelnewsreply(self):
        id = self.dl.GP('id','')
        thumbid = self.dl.db.fetchcolumn("select thumbid from ims_news_reply where id = '%s'" % id)
        if thumbid:
            import os
            attachment = self.dl.db.fetch("select * from ims_attachment where id = '%s'" % thumbid)
            if attachment and attachment.get("attachment") and os.path.exists(self.dl.config.RESOURCE+attachment.get("attachment")):
                os.remove(self.dl.config.RESOURCE+attachment.get("attachment"))
                self.dl.db.query("delete from ims_attachment where id = '%s'" % thumbid)
        self.dl.db.query("delete from ims_news_reply where id = '%s'" % id)
        return self.dl.oFunc.json_encode({'error':0})

    def goPartWelcome(self):
        id = self.dl.GP('id','')
        weid = self.weid
        content = self.dl.db.fetchcolumn("select content from ims_basic_reply where rid = '%s'" % id)
        self.dl.db.query("update ims_wechats set welcome = '%s' where weid = '%s'" % (content , weid))
        return self.dl.oFunc.json_encode({'error':0})

    def goPartDefault(self):
        id = self.dl.GP('id','')
        weid = self.weid
        content = self.dl.db.fetchcolumn("select content from ims_basic_reply where rid = '%s'" % id)
        self.dl.db.query("update ims_wechats set defaults = '%s' where weid = '%s'" % (content , weid))
        return self.dl.oFunc.json_encode({'error':0})


    def goPartPost(self):
        pk = self.dl.GP('pk','')
        data = {'weid':self.weid,'cid':self.dl.usr_id,'displayorder':0}
        data['name'] = self.dl.GP('name','')
        data['status'] = self.dl.GP('status','0')
        data['module'] = self.dl.GP('module','')
        keywords = self.dl.GP('keywords','')
        if pk == "":
            self.dl.db.insert("ims_rule",data)
            pk = self.dl.db.insertid()
            
        else:
            rule = self.dl.db.fetch("select id from ims_rule where weid = '%s' and id = '%s'" % (self.weid , pk))
            if not rule:
                url  ='admin?viewid=news'
                return self.mScriptMsg('该规则不存在或已被删除了',[[url,'返回列表']],'error')
            self.dl.db.update("ims_rule",data," id='%s'" % pk)
            
        #更新，添加，删除关键字
        if pk:
            sql = "DELETE FROM ims_rule_keyword WHERE [rid]='%s' AND weid='%s'" % (pk,self.weid)
            self.dl.db.query(sql)
            rows = []
            
            kwds = keywords.split(",")
            keywordname = self.objHandle.values.getlist('keywordname')
            keywordvalue = self.objHandle.values.getlist('keywordvalue')
            for i in range(len(keywordname)):
                rowtpl = {
                    'rid' : pk , 'weid' : self.weid , 'module':data['module'],'status':data['status'],'displayorder':0
                }
                kn = keywordname[i]
                kv = keywordvalue[i]
                rowtpl['content'] = kn
                rowtpl['type'] = kv
                rows.append(rowtpl)
            for kw in kwds:
                rowtpl = {
                    'rid' : pk , 'weid' : self.weid , 'module':data['module'],'status':data['status'],'displayorder':0
                }
                rowtpl['content'] = kw
                rowtpl['type'] = 1
                rows.append(rowtpl)
            for rule_keyword in rows:
                self.dl.db.insert("ims_rule_keyword",rule_keyword)
            #处理图文回复
            news_reply_id = self.objHandle.values.getlist('news_reply_id')
            parentid = 0
            for rid in news_reply_id:
                if not rid or rid == '':
                    continue
                data = {'parentid':parentid}
                data['title'] = self.dl.GP('news-title_%s' % rid)
                data['description'] = self.dl.GP('news-description_%s' % rid)
                data['content'] = self.dl.GP('news-content_%s' % rid)
                data['url'] = self.dl.GP('news-url_%s' % rid)
                data['thumb'] = self.dl.GP('news-picture_%s' % rid)
                data['thumbid'] = self.dl.GP('news-picture-old_%s' % rid)
                self.dl.db.update("ims_news_reply",data," id='%s'"%rid)
                if parentid == 0:
                    parentid = rid
                
            title = self.objHandle.values.getlist('news-title')
            description = self.objHandle.values.getlist('news-description')
            content = self.objHandle.values.getlist('news-content')
            url = self.objHandle.values.getlist('news-url')
            thumb = self.objHandle.values.getlist('news-picture')
            thumbid = self.objHandle.values.getlist('news-picture-old')
            
            for i in range(len(title)):
                data = {'rid':pk,'parentid':parentid}
                data['title'] = title[i]
                data['description'] = description[i]
                data['content'] = content[i]
                data['url'] = url[i]
                data['thumb'] = thumb[i]
                data['thumbid'] = thumbid[i]
                self.dl.db.insert("ims_news_reply",data)
                if i == 0 and parentid == 0:
                    parentid = self.dl.db.insertid()
            return self.mScriptMsg('规则操作成功！',[['admin?viewid=news&part=localform&id=%s' % pk,'返回']],'success')
        else:
            return self.mScriptMsg('规则操作失败, 请联系网站管理员！')




