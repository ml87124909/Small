# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################

from imp import reload
from .publicw import DEBUG,SITE_ROOT,db,md5code

from flask import make_response
from  xml.dom import  minidom
import time , os,base64,importlib,json,requests


class cWxApi:
    def __init__(self):
        self.db=db
        self.md5code=md5code
        self._http = requests.Session()
        self.account = {}
        self.weid = 1 #默认1
        self.uid = 0
        sql = """
                SELECT weid,coalesce(uid,0),coalesce(access_token,'') as access_token,
                coalesce(expires_in,0) as expires_in,convert_from(decrypt(key::bytea, %s, 'aes'),'SQL_ASCII') as key,
                convert_from(decrypt(secret::bytea, %s, 'aes'),'SQL_ASCII') as secret FROM ims_wechats limit 1;
        
        """
        self.account = self.db.fetch(sql,[self.md5code,self.md5code])
        #print(self.account)
        #self.domain='http://small.yjyzj.cn/wx/menu'
        self.uid = self.account.get('uid', 0)
        self.weid = self.account.get('weid', 0)
        self.access_token_d = {'token': self.account.get("access_token", ''),
                               'expire': self.account.get("expires_in", 0)}
        self.access_token = ''
        self.wx_appKey = self.account.get('key', '')
        self.wx_secret = self.account.get('secret', '')
        #self.domain = self.account.get('domain', '')

        # #本地测试号
        # self.account['key']='wxf51a70a03192222'
        # self.account['secret']='d4624c36b6795d22222'
        # self.domain='http://192.168.1.118/wx/menu'

    def get_access_token(self):  # 获取令牌
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        self.wx_appKey, self.wx_secret)

        content = self._http.post(url) #requests.post(url)
        content=content.json()
        #print(content,'content')
        if content.get('errmsg'):
            return content.get('errmsg')

        # record = {}
        # record['token'] = content['access_token']
        # record['expire'] = int(time.time()) + content['expires_in']
        expires_in=int(time.time()) + content['expires_in']
        self.access_token = content['access_token']
        sql="update ims_wechats set access_token = %s,expires_in=%s where weid = %s"
        self.db.query(sql,[self.access_token,expires_in,self.weid])
        return self.access_token#content['access_token']

    def init_token(self):
        if self.access_token_d and self.access_token_d['expire'] > time.time() and self.access_token_d['token'] != '':
            return self.access_token_d['token']
        return self.get_access_token()

    def menuQuery(self):
        token = self.init_token()
        url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % token

        content = self._http.post(url)#requests.post(url)
        content = content.json()
        if content.get('errcode') and content.get('errcode') != 0:
            return {}
        if content.get('menu'):
            return content.get('menu')
        else:
            return {}

    def menuCreate(self, menu=None, isjson=True):
        if not menu:
            return False
        token = self.init_token()
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % token

        if isinstance(menu, dict):
            body = json.dumps(menu, ensure_ascii=False)
            data = body.encode('utf-8')
            content = self._http.post(url, data=data)
            content = content.json()
            return content.get('errcode')
        return False

    def menuDelete(self):
        token = self.init_token()
        url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % token

        content = self._http.post(url)#requests.post(url)
        content = content.json()
        if content.get('errcode') == 0:
            return True
        else:
            return False

    def getFans(self, weid, openid):
        sql = '''
        select id,weid,from_user,follow,createtime , realname,nickname,nickname2,avatar,qq,mobile
        ,resideprovince,residecity,nationality,residedist,gender,credit1,credit2
        from ims_fans where weid = '%s' and from_user = '%s'
        ''' % (weid, openid)
        fans = self.db.fetch(sql)
        if not fans:
            return None
        else:
            fans['nickname2'] = base64.b64decode(fans['nickname2'])
            return fans

    def addFans(self, openid):
        token = self.init_token()
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (token, openid)

        content = self._http.post(url)#requests.post(url)
        content = content.json()
        if content.get('errcode'):
            print(content.get('errcode'))
            pass
        else:
            data = {
                'weid': self.weid
                , 'from_user': openid
                , 'salt': 'aaaa'
                , 'follow': content.get('subscribe', '0')
                , 'credit1': 0
                , 'credit2': 0
                , 'createtime': int(time.time())
                , 'realname': ''
                , 'nickname': content.get('nickname', '')
                , 'nickname2': base64.b64encode(content.get('nickname', ''))
                , 'avatar': content.get('headimgurl', '')
                , 'qq': ''
                , 'mobile': ''
                , 'fakeid': ''
                , 'resideprovince': content.get('province', '')
                , 'residecity': content.get('city', '')
                , 'residedist': ''
                , 'nationality': content.get('country', '')
                , 'gender': content.get('sex', '')
            }

            csql = '''
                select id from ims_fans where from_user='%s' and weid=%s
            ''' % (openid, self.weid)
            hasFans = self.db.fetch(csql)
            if hasFans.get('id', ''):
                self.db.update('ims_fans', data, '''from_user='%s' and weid=%s''' % (openid, self.weid))
            else:
                self.db.insert('ims_fans', data)

    def delFans(self, openid):
        self.db.query("delete from ims_fans where from_user = '%s'" % openid)

    def weixin_code(self, code):
        errors = {
            '-1': '系统繁忙',
            '0': '请求成功',
            '40001': '获取access_token时AppSecret错误，或者access_token无效',
            '40002': '不合法的凭证类型',
            '40003': '不合法的OpenID',
            '40004': '不合法的媒体文件类型',
            '40005': '不合法的文件类型',
            '40006': '不合法的文件大小',
            '40007': '不合法的媒体文件id',
            '40008': '不合法的消息类型',
            '40009': '不合法的图片文件大小',
            '40010': '不合法的语音文件大小',
            '40011': '不合法的视频文件大小',
            '40012': '不合法的缩略图文件大小',
            '40013': '不合法的APPID',
            '40014': '不合法的access_token',
            '40015': '不合法的菜单类型',
            '40016': '不合法的按钮个数',
            '40017': '不合法的按钮个数',
            '40018': '不合法的按钮名字长度',
            '40019': '不合法的按钮KEY长度',
            '40020': '不合法的按钮URL长度',
            '40021': '不合法的菜单版本号',
            '40022': '不合法的子菜单级数',
            '40023': '不合法的子菜单按钮个数',
            '40024': '不合法的子菜单按钮类型',
            '40025': '不合法的子菜单按钮名字长度',
            '40026': '不合法的子菜单按钮KEY长度',
            '40027': '不合法的子菜单按钮URL长度',
            '40028': '不合法的自定义菜单使用用户',
            '40029': '不合法的oauth_code',
            '40030': '不合法的refresh_token',
            '40031': '不合法的openid列表',
            '40032': '不合法的openid列表长度',
            '40033': '不合法的请求字符，不能包含\\uxxxx格式的字符',
            '40035': '不合法的参数',
            '40038': '不合法的请求格式',
            '40039': '不合法的URL长度',
            '40050': '不合法的分组id',
            '40051': '分组名字不合法',
            '41001': '缺少access_token参数',
            '41002': '缺少appid参数',
            '41003': '缺少refresh_token参数',
            '41004': '缺少secret参数',
            '41005': '缺少多媒体文件数据',
            '41006': '缺少media_id参数',
            '41007': '缺少子菜单数据',
            '41008': '缺少oauth code',
            '41009': '缺少openid',
            '42001': 'access_token超时',
            '42002': 'refresh_token超时',
            '42003': 'oauth_code超时',
            '43001': '需要GET请求',
            '43002': '需要POST请求',
            '43003': '需要HTTPS请求',
            '43004': '需要接收者关注',
            '43005': '需要好友关系',
            '44001': '多媒体文件为空',
            '44002': 'POST的数据包为空',
            '44003': '图文消息内容为空',
            '44004': '文本消息内容为空',
            '45001': '多媒体文件大小超过限制',
            '45002': '消息内容超过限制',
            '45003': '标题字段超过限制',
            '45004': '描述字段超过限制',
            '45005': '链接字段超过限制',
            '45006': '图片链接字段超过限制',
            '45007': '语音播放时间超过限制',
            '45008': '图文消息超过限制',
            '45009': '接口调用超过限制',
            '45010': '创建菜单个数超过限制',
            '45015': '回复时间超过限制',
            '45016': '系统分组，不允许修改',
            '45017': '分组名字过长',
            '45018': '分组数量超过上限',
            '46001': '不存在媒体数据',
            '46002': '不存在的菜单版本',
            '46003': '不存在的菜单数据',
            '46004': '不存在的用户',
            '47001': '解析JSON/XML内容错误',
            '48001': 'api功能未授权',
            '50001': '用户未授权该api',
        }
        return errors.get(str(code), 'unkwon error')

    def goPartGetToken(self):
        import random , hashlib.md5
        r = str(random.randint(100000,999999))
        token = md5.md5(r).hexdigest()
        return token

    def checkSign(self , token):
        data = self.objHandle.values
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        import hashlib
        if (hashlib.sha1(s).hexdigest() == signature):
            print(1)
            return True
        else:
            print(2)
            return True#False

    def goPartToken(self):
        #微信认证token
        token=self.account.get('token','')
        #core.log(token)
        if token == '':
            return 'Access Denied'
        if not self.checkSign(token):
            print(3)
            return 'Access Denied'
        if self.objHandle.method == 'GET':
            return make_response(self.objHandle.values.get('echostr',''))
        #与用户的对话
        else:
            data={}
            rec = str(self.objHandle.stream.read()).replace(" ","")
            xml_rec =self.xmlParse(rec)# ElementTree.fromstring(rec)
            msgtype = xml_rec.get('MsgType')
            ToUserName = xml_rec.get('ToUserName')
            FromUserName = xml_rec.get('FromUserName')
            data['CreateTime']=int(time.time())
            data['ToUserName']=ToUserName
            data['FromUserName']=FromUserName
            data['Content'] = self.account.get('default','功能开发中，请持续关注~')
            if not data['Content'] or data['Content'].strip() == '':
                data['Content'] = '功能开发中，请持续关注~'
            response = make_response(self.send_text(data))
            if not self.account:

                data['Content']='系统出现问题啦！'#默认回复
                response = make_response(self.send_text(data))
                response.mimetype='application/xml'
                response.content_type='text/xml; charset=utf-8'
                return response
            fans = self.getFans(self.weid,FromUserName)
            if not fans:
                fans = self.addFans(FromUserName)
                fans = self.getFans(self.weid,FromUserName)
            #事件
            if msgtype == "event":
                event = xml_rec.get('Event')
                if event=='subscribe':#订阅
                    if not fans:
                        fans = self.addFans(FromUserName)
                    data['Content'] = self.account.get('welcome','功能开发中，请持续关注~')
                    response = make_response(self.send_text(data))
                elif event=='unsubscribe':#取消订阅
                    self.delFans(FromUserName)
                    response = make_response(self.send_text(data))
                elif event=='LOCATION':#上报地理位置事件

                    response = make_response(self.send_text(data))
                elif event=='CLICK':#自定义菜单事件
                    EventKey=xml_rec.get('EventKey')
                    className = "key_%s" % EventKey
                    if os.path.exists(os.path.join(SITE_ROOT , 'rule\\%s.py' % className)):
                        #exec 'import rule.%s as ruleObj' % className
                        ruleObj  = importlib.import_module(' rule.%s' % (className))
                        if DEBUG == '1':
                            reload(ruleObj)
                        #bj = eval('ruleObj.c%s(WeEngine,ToUserName,FromUserName)'% className)
                        obj = getattr(ruleObj, className)(self,ToUserName,FromUserName)
                        response = obj.send_response()
                    else:
                        response = make_response(self.send_text(data))

                else:
                    response = make_response(self.send_text(data))
            elif msgtype == "image":#图片消息
                PicUrl=xml_rec.get('PicUrl')#图片链接（由系统生成）
                MediaId=xml_rec.get('MediaId')#消息媒体id，可以调用多媒体文件下载接口拉取数据。
                data['Content']='图片消息'
                response = make_response(self.send_text(data))
            elif msgtype == "voice":#语音消息
                Format=xml_rec.get('Format')#语音格式，如amr，speex等
                MediaId=xml_rec.get('MediaId')#消息媒体id，可以调用多媒体文件下载接口拉取数据。

                data['Content']='语音消息'
                response = make_response(self.send_text(data))
            elif msgtype == "video":#视频消息
                ThumbMediaId=xml_rec.get('ThumbMediaId')#消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。
                MediaId=xml_rec.get('MediaId')#消息媒体id，可以调用多媒体文件下载接口拉取数据。
                data['Content']='视频消息'
                response = make_response(self.send_text(data))
            elif msgtype == "shortvideo":#小视频消息
                ThumbMediaId=xml_rec.get('ThumbMediaId')#消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。
                MediaId=xml_rec.get('MediaId')#消息媒体id，可以调用多媒体文件下载接口拉取数据。
                data['Content']='小视频消息'
                response = make_response(self.send_text(data))
            elif msgtype == "location":#地理位置消息
                Location_X=xml_rec.get('Location_X')#地理位置维度
                Location_Y=xml_rec.get('Location_Y')#地理位置经度
                Scale=xml_rec.get('Scale')#地图缩放大小
                Label=xml_rec.get('Label')#地理位置信息
                data['Content']='地理位置消息'
                response = make_response(self.send_text(data))
            elif msgtype == "link":#链接消息
                Title=xml_rec.get('Title')#消息标题
                Description=xml_rec.get('Description')#消息描述
                Url=xml_rec.get('Url')#消息链接
                data['Content']='链接消息'
                response = make_response(self.send_text(data))
            else:#普通文本消息
                content = xml_rec.get('Content')

                # response = make_response(self.send_text(data))
                # return response

                pars = []
                sql = '''
                SELECT TOP 10 * FROM
                ims_rule_keyword where
                [status]=1 AND ([weid]='%(weid)s' OR [weid]=0 ) AND displayorder > -1
                 AND ((([type] = '1' OR [type] = '2') AND [content] = '%(input)s')
                 OR ([type] = '4')
                 OR ([type] = '3' AND dbo.find_regular_expression('%(input)s',[content],0) = 1)
                 OR ([type] = '2' AND '%(input)s' like '%%'+[content]+'%%'))
                 ORDER BY displayorder DESC, id DESC
                 ''' % {'input':content , 'weid':self.weid}
                keywords,total = self.db.fetchall(sql)
                for kw in keywords:
                    params = {
                        'module' : kw['module'],
                        'rule': kw['rid'],
                        'priority' : kw['displayorder'],
                        'keyword' : kw
                    }
                    pars.append(params)

                pars.append({'module' : 'default', 'rule' : '-1'})
                ruleMod = None
                response = make_response('')
                for par in pars:
                    if not par.get('module') or par.get('module') == '':
                        continue
                    #core.log(par.get('module'))
                    ruleMod = self.createRuleModule(par,self,ToUserName,FromUserName)

                    if ruleMod:
                        response = ruleMod.send_response()

                        if response:
                            createtime = int(time.time())
                            self.db.insert("ims_stat_rule",{'weid':self.weid,'rid':par.get('rule','-1'),'hit':1,'lastupdate':createtime,'createtime':createtime,'from_user':FromUserName})
                            break
                if not response:
                    data['Content'] = '功能开发中，请关注~'
                    response = make_response(self.send_text(data))

            response.mimetype='application/xml'
            response.content_type='text/xml; charset=utf-8'

            return response

    def createRuleModule(self,keyword,ToUserName,FromUserName):
        if os.path.exists(os.path.join(SITE_ROOT , 'rule\\%s.py' % keyword.get('module'))):
            ruleObj = importlib.import_module(' rule.%s' % (keyword.get('module')))
            if DEBUG == '1':
                reload(ruleObj)
            # bj = eval('ruleObj.c%s(WeEngine,ToUserName,FromUserName)'% className)
            obj = getattr(ruleObj, keyword.get('module'))(self, ToUserName,FromUserName,keyword)

            #exec 'import rule.%s as ruleObj' % keyword.get('module')
            # if core.config.DEBUG == 1:
            #     reload(ruleObj)
            #obj = eval('ruleObj.c%s(WeEngine,ToUserName,FromUserName,keyword)'% keyword.get('module'))
            return obj
        else:
            return None

    def xmlParse(self, xml): #uft-8
        d = {}
        if xml is None:
            return d
        #xml = deStrcode(xml)
        doc=minidom.parseString(xml)
        dom = doc.firstChild
        body= dom.childNodes
        for e in body:
            node = e.nodeName
            if node=='#text': continue  #去掉换行 '\n    '
            child=e.firstChild
            if child is None: continue
            data = child.data
            d[str(node)]=data
        return d

    #回复文本消息
    def send_text(self,data):
        s="""
            <xml>
                <ToUserName><![CDATA[%(FromUserName)s]]></ToUserName>
                <FromUserName><![CDATA[%(ToUserName)s]]></FromUserName>
                <CreateTime>%(CreateTime)s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%(Content)s]]></Content>
            </xml>
        """%data
        return s

    #回复图片消息
    def send_imags(self,data):
        s="""
            <xml>
                <ToUserName><![CDATA[%(FromUserName)s]]></ToUserName>
                <FromUserName><![CDATA[%(ToUserName)s]]></FromUserName>
                <CreateTime>%(CreateTime)s</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[%(MediaId)s]]></MediaId>
                </Image>
            </xml>
        """%data
        return s

    #回复语音消息
    def send_voice(self,data):
        s="""
            <xml>
                <ToUserName><![CDATA[%(FromUserName)s]]></ToUserName>
                <FromUserName><![CDATA[%(ToUserName)s]]></FromUserName>
                <CreateTime>%(CreateTime)s</CreateTime>
                <MsgType><![CDATA[voice]]></MsgType>
                <Voice>
                <MediaId><![CDATA[%(MediaId)s]]></MediaId>
                </Voice>
            </xml>
        """%data
        return s

    #回复视频消息
    def send_video(self,data):
        s="""
            <xml>
                <ToUserName><![CDATA[%(FromUserName)s]]></ToUserName>
                <FromUserName><![CDATA[%(ToUserName)s]]></FromUserName>
                <CreateTime>%(CreateTime)s</CreateTime>
                <MsgType><![CDATA[video]]></MsgType>
                <Video>
                <MediaId><![CDATA[media_id]]></MediaId>
                <Title><![CDATA[%(Title)s]]></Title>
                <Description><![CDATA[%(Description)s]]></Description>
                </Video>
            </xml>
        """%data
        return s

    #回复音乐消息
    def send_music(self,data):
        s="""
            <xml>
                <ToUserName><![CDATA[%(FromUserName)s]]></ToUserName>
                <FromUserName><![CDATA[%(ToUserName)s]]></FromUserName>
                <CreateTime>%(CreateTime)s</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music>
                <Title><![CDATA[%(Title)s]]></Title>
                <Description><![CDATA[%(Description)s]]></Description>
                <MusicUrl><![CDATA[%(MusicUrl)s]]></MusicUrl>
                <HQMusicUrl><![CDATA[%(HQMusicUrl)s]]></HQMusicUrl>
                <ThumbMediaId><![CDATA[%(ThumbMediaId)s]]></ThumbMediaId>
                </Music>
            </xml>
        """%data
        return s

    #回复图文消息
    def send_news(self,data):
        item_list=''
        data['ArticleCount']=0
        if data.get('items') and type(data.get('items'))==type([]):
            data['ArticleCount']=len(data.get('items'))
            for i in data.get('items'):
                item_list+='''
                    <item>
                        <Title><![CDATA[%(Title)s]]></Title>
                        <Description><![CDATA[%(Description)s]]></Description>
                        <PicUrl><![CDATA[%(PicUrl)s]]></PicUrl>
                        <Url><![CDATA[%(Url)s]]></Url>
                    </item>
                '''%i
        data['item_list']=item_list
        s="""
            <xml>
                <ToUserName><![CDATA[%(FromUserName)s]]></ToUserName>
                <FromUserName><![CDATA[%(ToUserName)s]]></FromUserName>
                <CreateTime>%(CreateTime)s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>%(ArticleCount)s</ArticleCount>
                <Articles>
                    %(item_list)s
                </Articles>
            </xml>
        """%data
        return s