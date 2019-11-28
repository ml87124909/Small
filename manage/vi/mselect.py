# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/mselect.py"""


from basic.publicw import cTag, CHtml

class mselect:
    def __init__(self , name = 'm' , nl = [],title = '选择人员' , wh = [800,300] , can = [1,1]):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.name = name
        self.title = title
        self.wh = wh
        if self.wh[0] == 0:
            self.wh[0] = 800
        if self.wh[1] == 0:
            self.wh[1] = 300
        self.sUrl = ''
        self.Html = CHtml()
        self._search_html = self.search_html()
        self.cln_btnb = """<button type="button" class="btnb" onclick="%s_clearPutOut();">清除</button>""" %self.name
        self.callback()
        
    def getHTML(self):
        return self.selusers() + self.cln_btnb
        
    def selusers(self):
        html=''
        html = ''
        #触发按钮
        btnb_role = cTag('input','',{"value":"选择",
                                    "type":"button",
                                    "class":"btnb",
                                    "onclick":"%s_loadUsersList('');"%self.name})
        html += btnb_role.getHTML()

        #模态框内容，最外层框
        div_modal = cTag('div','',{"id"      :"%s_Modal"%self.name, 
                                   "class"   :"modal hide fade myModalStyle",
                                   "tabindex":"-1", 
                                   "role"    :"dialog", 
                                   "aria-labelledby"  :"%s_ModalLabel"%self.name, 
                                   "aria-hidden"      :"true"})
        if self.wh!=[]:
            div_modal.addAttr({'style':'width:%spx'%self.wh[0]})
        
        #模态框头部
        div_modal_head = cTag('div','',{"class":"modal-header"})
        btnb_head_close = cTag('button','×',{"type"        :"button", 
                                            "class"       :"close", 
                                            "data-dismiss":"modal",
                                            "aria-hidden" :"true"})
        txt_head_content = cTag('h3',self.title,{"id":"%s_ModalLabel"%self.name})
        div_modal_head.add( btnb_head_close.getHTML() )
        div_modal_head.add( txt_head_content.getHTML() )
        div_modal.add( div_modal_head.getHTML() )       

        #模态框搜索框
        
        div_modal.add( self._search_html )       

        #模态框的body
        div_modal_body  = cTag('div', '', {'class':'modal-body',"style":"height:%spx;"%self.wh[1]})
        table_users     = cTag('table','',{'id':'table_%s_List'%self.name,'class':'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add( cTag('th', n).getHTML() )
        thead.add( tr.getHTML() )
        table_users.add( thead.getHTML() )   # table 分开 thead 和 tbody 标签

        #tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody','', {'class':'table table-hover'})
        table_users.add( tbody.getHTML() )
        div_modal_body.add( table_users.getHTML() )
        div_modal.add( div_modal_body.getHTML() )
        
        #模态框的脚部
        div_modal_footer = cTag('div','', {'class':'modal-footer'} )
        btnb_modal_ok = cTag('button','确定', {'class':'btnb', 'data-dismiss':'modal','onclick':'%s_OutPut();'%self.name , 'aria-hidden':'true'})
        btnb_modal_close = cTag('button','关闭', {'class':'btnb', 'data-dismiss':'modal', 'aria-hidden':'true'})
        div_modal_footer.add( btnb_modal_ok.getHTML() )
        div_modal_footer.add( btnb_modal_close.getHTML() )
        div_modal.add( div_modal_footer.getHTML() )
        
        aValue = self.Html.input('','aValue','hidden',{'id':'%s_aValue'%self.name})
        #最后整块处理
        html += div_modal.getHTML()+aValue
        return html + self.js()

    
    def search_html(self):
        div_modal_search = cTag('div','',{"class":"modal-header"})
        key_search = self.Html.input('','%s_keyword'%self.name,'text',{'id':'%s_keyword'%self.name,'class':'form-control span3','placeholder':'请输入关键字'})
        btnb_search = cTag('input','',{"value":"搜索",
                                      "type":"button",
                                      "class":"btnb",
                                      "onclick":"var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};"%(self.name,self.name)})
        div_modal_search.add( key_search)
        div_modal_search.add( btnb_search.getHTML() )
        self.searchUrl = '+"&keyword="+keyword'
        return div_modal_search.getHTML()
    
    def js(self):
        s="""<script>

                function %(name)s_loadUsersList(keyword){
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';

                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<data.list[i].length;j++){
                            tr += '<td>'+data.list[i][j]+'</td>';      /*ID*/
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){
                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(){
                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtnb:first-child{margin-left:212px;width:100px;}
            #%(name)s_Modal{width:%(outWidth)spx;left:50%%;margin-left:%(mLeftWidth)spx;}

            .table-hover tbody tr:hover>td{BackGround-Color: #3778EC}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC}                
            </style>
        """%{'sUrl':self.sUrl,'name':self.name,'ojs':self.confirmjs,'cjs':self.clearjs,'searchUrl':self.searchUrl
             ,'outWidth':self.wh[0],'mLeftWidth':int(self.wh[0] * 0.5) * -1}
        return s
    
    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''

#list 专用 mselect
class mselect_forList:
    top_btnbs_script=''   ##top_btnbs的JS
    top_btnbs=''   ##按钮 | 筛选
    __searchUrl = ''
    def __init__(self , name = 'm' , nl = [],title = '选择数据' , wh = [800,0] , can = [1,1] , has_open_botton=1):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.has_open_botton=has_open_botton
        self.nl = nl
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btnb = '''&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>'''%self.name
        self.callback()
        
    def getHTML(self):
        if self.has_open_botton==1:
            return self.selusers() + self.cln_btnb
        else:
            return self.selusers() 
        
    def selusers(self):
        
        html = ''
        #触发按钮
        if self.has_open_botton==1:
            btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>'''%self.name
            html += btnb_role

        #模态框内容，最外层框
        div_modal = cTag('div','',{"id"      :"%s_Modal"%self.name, 
                                   "class"   :"modal fade myModalStyle",
                                   "tabindex":"-1", 
                                   "role"    :"dialog", 
                                   "aria-labelledby"  :"%s_ModalLabel"%self.name, 
                                   "aria-hidden"      :"true"})
        if self.wh!=[]:
            div_modal.addAttr({'style':'width:%spx;margin-left:-%spx;left:50%%;'%(self.wh[0],self.wh[0]!='' and float(self.wh[0])/2 or '')})

        #模态框头部
        div_modal_head = cTag('div','',{"class":"modal-header"})
        btn_head_close = cTag('button','×',{"type"        :"button", 
                                            "class"       :"close", 
                                            "data-dismiss":"modal",
                                            "aria-hidden" :"true"})
        txt_head_content = cTag('h3',self.title,{"id":"%s_ModalLabel"%self.name,"style":"font-size:20px;"})
        div_modal_head.add( btn_head_close.getHTML() )
        div_modal_head.add( txt_head_content.getHTML() )
        div_modal.add( div_modal_head.getHTML() )

        #模态框搜索框
        
        div_modal.add( self.search_html() )       

        #模态框的body
        div_modal_body  = cTag('div', '', {'class':'modal-body',"style":"height:%spx;"%self.wh[1]})
        ####
        div_modal_body_s= cTag('div', '', {'class':'modal-body',"style":"height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;"%(self.wh[1])})

        ##########
        table_users     = cTag('table','',{'id':'table_%s_List'%self.name,'class':'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add( cTag('th', n).getHTML() )
        thead.add( tr.getHTML() )
        table_users.add( thead.getHTML() )   # table 分开 thead 和 tbody 标签

        #tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody','', {'class':'table table-hover'})
        table_users.add( tbody.getHTML() )
        #div_modal_body.add( table_users.getHTML() )
        ############
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        ############
        div_modal.add( div_modal_body.getHTML() )
        
        #模态框的脚部
        div_modal_footer = cTag('div','', {'class':'modal-footer'} )
        btn_modal_ok = cTag('button','确定', {'class':'btn', 'data-dismiss':'modal','onclick':'%s_OutPut();'%self.name , 'aria-hidden':'true'})
        btn_modal_close = cTag('button','关闭', {'class':'btn', 'data-dismiss':'modal', 'aria-hidden':'true'})
        div_modal_footer.add( btn_modal_ok.getHTML() )
        div_modal_footer.add( btn_modal_close.getHTML() )
        div_modal.add( div_modal_footer.getHTML() )
        
        aValue = self.Html.input('','aValue','hidden',{'id':'%s_aValue'%self.name})
        #最后整块处理
        html += div_modal.getHTML()+aValue
        return html + self.js()

    def top_btnbs_btnb(self):
        s='%s%s'%(self.top_btnbs,self.top_btnbs_script)
        
        return s
    
    def getUrlStr(self):
            return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])
    
    def search_html(self):
        div_modal_search = cTag('div','',{"class":"modal-header"})
        key_search = self.Html.input('','%s_keyword'%self.name,'text',{'id':'%s_keyword'%self.name,'class':'form-control span3','placeholder':'请输入关键字'})
        btnb_search = cTag('input','',{"value":"搜索",
                                      "type":"button",
                                      "class":"btn",
                                      "onclick":"var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};"%(self.name,self.name)})
        div_modal_search.add( key_search)
        div_modal_search.add( btnb_search.getHTML() )
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btnbs_btnb())
        #self.searchUrl = '+"&keyword="+keyword+"&matSele="+matSele'
        self.searchUrl= self.__searchUrl+'+"&keyword="+keyword'
        return div_modal_search.getHTML()
    
    def js(self):
        s="""<script>
                 $(function(){
                    $("#%(name)s_keyword").keydown(function(event){
                        if (event.keyCode == 13){
                            event.preventDefault();
                            %(name)s_loadUsersList($('#%(name)s_keyword').val());
                        }
                    });
                });
                function %(name)s_loadUsersList(keyword,matSele){
                    matSele=arguments[1]?arguments[1]:'';
              
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';

                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<data.list[i].length;j++){
                            tr += '<td>'+data.list[i][j]+'</td>';      /*ID*/
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){
                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){
                    
                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtnb:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

                 
            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}     
            .table th,td{white-space: nowrap;}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}  
            </style>
        """%{'sUrl':self.sUrl,'name':self.name,'ojs':self.confirmjs,'cjs':self.clearjs,'searchUrl':self.searchUrl}
        return s
    
    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''

class mselect_forList_forMeet(mselect_forList):
    def js(self):
        s="""<script>
                 $(function(){
                    $("#%(name)s_keyword").keydown(function(event){
                        if (event.keyCode == 13){
                            event.preventDefault();
                            %(name)s_loadUsersList($('#%(name)s_keyword').val());
                        }
                    });
                });
                function %(name)s_loadUsersList(keyword,matSele){
                    matSele=arguments[1]?arguments[1]:'';
              
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';

                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<data.list[i].length;j++){
                            if(j!=0){
                                tr += '<td>'+data.list[i][j]+'</td>';      /*ID*/
                            }
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){
                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){
                    
                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtnb:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

                 
            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}     
            .table th,td{white-space: nowrap;}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}  
            </style>
        """%{'sUrl':self.sUrl,'name':self.name,'ojs':self.confirmjs,'cjs':self.clearjs,'searchUrl':self.searchUrl}
        return s

class mselect_forMatList:
    top_btnbs_script=''   ##top_btnbs的JS
    top_btnbs=''   ##按钮 | 筛选
    def __init__(self , name = 'm' , nl = [],title = '选择数据' , wh = [800,0] , can = [1,1]):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btnb = ''
        self.callback()
        
    def getHTML(self):
        return self.selusers() + self.cln_btnb
        
    def selusers(self):
        
        html = ''
        #触发按钮
        btnb_role = cTag('div','',{"style":"display:none", "listRow":"0", "id":"matListRow"})

        html += btnb_role.getHTML()

        #模态框内容，最外层框
        div_modal = cTag('div','',{"id"      :"%s_Modal"%self.name, 
                                   "class"   :"modal hide fade myModalStyle", 
                                   "tabindex":"-1", 
                                   "role"    :"dialog", 
                                   "aria-labelledby"  :"%s_ModalLabel"%self.name, 
                                   "aria-hidden"      :"true"})
        
        #模态框头部
        div_modal_head = cTag('div','',{"class":"modal-header"})
        btnb_head_close = cTag('button','×',{"type"        :"button", 
                                            "class"       :"close", 
                                            "data-dismiss":"modal",
                                            "aria-hidden" :"true"})
        txt_head_content = cTag('h3',self.title,{"id":"%s_ModalLabel"%self.name})
        div_modal_head.add( btnb_head_close.getHTML() )
        div_modal_head.add( txt_head_content.getHTML() )
        div_modal.add( div_modal_head.getHTML() )       

        #模态框搜索框
        
        div_modal.add( self.search_html() )       

        #模态框的body
        div_modal_body  = cTag('div', '', {'class':'modal-body',"style":"height:300px;"})
        table_users     = cTag('table','',{'id':'table_%s_List'%self.name,'class':'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add( cTag('th', n).getHTML() )
        thead.add( tr.getHTML() )
        table_users.add( thead.getHTML() )   # table 分开 thead 和 tbody 标签

        #tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody','', {'class':'table table-hover'})
        table_users.add( tbody.getHTML() )
        div_modal_body.add( table_users.getHTML() )
        div_modal.add( div_modal_body.getHTML() )
        
        #模态框的脚部
        div_modal_footer = cTag('div','', {'class':'modal-footer'} )
        btnb_modal_ok = cTag('button','确定', {'class':'btnb', 'data-dismiss':'modal','onclick':'%s_OutPut();'%self.name , 'aria-hidden':'true'})
        btnb_modal_close = cTag('button','关闭', {'class':'btnb', 'data-dismiss':'modal', 'aria-hidden':'true'})
        div_modal_footer.add( btnb_modal_ok.getHTML() )
        div_modal_footer.add( btnb_modal_close.getHTML() )
        div_modal.add( div_modal_footer.getHTML() )
        
        aValue = self.Html.input('','aValue','hidden',{'id':'%s_aValue'%self.name})
        #最后整块处理
        html += div_modal.getHTML()+aValue
        return html + self.js()

    def top_btnbs_btnb(self):
        s='%s%s'%(self.top_btnbs,self.top_btnbs_script)
        
        return s
    
    def search_html(self):
        div_modal_search = cTag('div','',{"class":"modal-header"})
        key_search = self.Html.input('','%s_keyword'%self.name,'text',{'id':'%s_keyword'%self.name,'class':'form-control span3','placeholder':'请输入关键字'})
        btnb_search = cTag('input','',{"value":"搜2索",
                                      "type":"button",
                                      "class":"btnb",
                                      "onclick":"var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};"%(self.name,self.name)})
        div_modal_search.add( key_search)
        div_modal_search.add( btnb_search.getHTML() )
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btnbs_btnb())
        self.searchUrl = '+"&keyword="+keyword+"&matSele="+matSele+"&matType="+matType'
        return div_modal_search.getHTML()
    
    def js(self):
        s="""<script>

                function %(name)s_loadUsersList(keyword,matSele,matType){
                alert(matType)
                    matSele=arguments[1]?arguments[1]:'';
              
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';

                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<data.list[i].length;j++){
                            tr += '<td>'+data.list[i][j]+'</td>';      /*ID*/
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){
                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){
                    
                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtnb:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #3778EC}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC}                
            </style>
        """%{'sUrl':self.sUrl,'name':self.name,'ojs':self.confirmjs,'cjs':self.clearjs,'searchUrl':self.searchUrl}
        return s
    
    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''    
# wjwcw项目关联经费列支渠道

class mselect_forJF_type:
    top_btns_script=''   ##top_btns的JS
    top_btns=''   ##按钮 | 筛选
    __searchUrl=''
    def __init__(self , name = 'm' , nl = [],title = '选择数据' , wh = [800,0] , can = [1,1] ,showSearch=1,dnl=[],search_holder='请输入项目名称'):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.showSearch=showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btn = '''&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>'''%self.name
        self.callback()
        self.search_holder=search_holder
        self.dnl = []
        if len(dnl)<=0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl=dnl
            
        #self.dnl 查询语句需要返回的字段索引 
                
    def getHTML(self):
        return self.selusers() + self.cln_btn
        
    def selusers(self):
        
        html = ''
        #触发按钮
        btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>'''%self.name
        html += btnb_role

        #模态框内容，最外层框
        div_modal = cTag('div','',{"id"      :"%s_Modal"%self.name, 
                                   "class"   :"modal fade myModalStyle",
                                   "tabindex":"-1", 
                                   "role"    :"dialog", 
                                   "aria-labelledby"  :"%s_ModalLabel"%self.name, 
                                   "aria-hidden"      :"true"})
        if self.wh!=[]:
            div_modal.addAttr({'style':'width:%spx;margin-left:-%spx;left:50%%;'%(self.wh[0],self.wh[0]!='' and float(self.wh[0])/2 or '')})

        #模态框头部
        div_modal_head = cTag('div','',{"class":"modal-header"})
        btn_head_close = cTag('button','×',{"type"        :"button", 
                                            "class"       :"close", 
                                            "data-dismiss":"modal",
                                            "aria-hidden" :"true"})
        txt_head_content = cTag('h3',self.title,{"id":"%s_ModalLabel"%self.name,"style":"font-size:20px;"})
        div_modal_head.add( btn_head_close.getHTML() )
        div_modal_head.add( txt_head_content.getHTML() )
        div_modal.add( div_modal_head.getHTML() )

        #模态框搜索框
        
        div_modal.add( self.search_html() )       

        #模态框的body
        div_modal_body  = cTag('div', '', {'class':'modal-body',"style":"height:%spx;"%self.wh[1]})
        ####
        div_modal_body_s= cTag('div', '', {'class':'modal-body',"style":"height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;"%(self.wh[1])})

        ##########
        table_users     = cTag('table','',{'id':'table_%s_List'%self.name,'class':'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add( cTag('th', n).getHTML() )
        thead.add( tr.getHTML() )
        table_users.add( thead.getHTML() )   # table 分开 thead 和 tbody 标签

        #tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody','', {'class':'table table-hover'})
        table_users.add( tbody.getHTML() )
        #div_modal_body.add( table_users.getHTML() )
        ############
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        ############
        div_modal.add( div_modal_body.getHTML() )
        
        #模态框的脚部
        div_modal_footer = cTag('div','', {'class':'modal-footer'} )
        btn_modal_ok = cTag('button','确定', {'class':'btn', 'data-dismiss':'modal','onclick':'%s_OutPut();'%self.name , 'aria-hidden':'true'})
        btn_modal_close = cTag('button','关闭', {'class':'btn', 'data-dismiss':'modal', 'aria-hidden':'true'})
        div_modal_footer.add( btn_modal_ok.getHTML() )
        div_modal_footer.add( btn_modal_close.getHTML() )
        div_modal.add( div_modal_footer.getHTML() )
        
        aValue = self.Html.input('','aValue','hidden',{'id':'%s_aValue'%self.name})
        #最后整块处理
        html += div_modal.getHTML()+aValue
        return html + self.js()

    def top_btns_btn(self):
        s='%s%s'%(self.top_btns,self.top_btns_script)
        
        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self,dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s'%(e,dis[e])

    def search_html(self):
        div_modal_search = cTag('div','',{"class":"modal-header"})
        o = [['','--经费性质--'],
            ['1', '行政经费'],
            ['4', '事业经费']
        ]

        jf_type = self.Html.select(o, 'jf_type','' ,
                                     {'onchange': "%s_jf(this.value)"%(self.name)
                ,'class': 'span1 inputed', 'style': 'width:115px;height:32px;margin-left:5px;'})

        key_search = self.Html.input('','%s_keyword'%self.name,'text',{'id':'%s_keyword'%self.name,'class':'form-control span1','style':'padding:4px 6px;margin:5px;','placeholder':self.search_holder})

        btn_search = cTag('input','',{"value":"搜索",
                                      "type":"button",
                                      'style':'margin:5px;',
                                      "class":"btn",
                                      "onclick":"var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};"%(self.name,self.name)})
        if self.showSearch==1:
            div_modal_search.add(jf_type)
            div_modal_search.add( key_search)
            div_modal_search.add( btn_search.getHTML() )
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword'
        return div_modal_search.getHTML()
    
    def js(self):
        s="""<script>

                function %(name)s_loadUsersList(keyword){
                    a= $('input[name=jf_type]:checked').val();
                    if(a){
                        $('select[name=jf_type]').val(a);
                    }
                    if (a==undefined){
                        a='';
                    }
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"+"&jf_type="+a+""%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }
                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){

                            tr += '<td >'+data.list[i][dnl[j]]+'</td>';   //原来的方式，不用区分对齐
                            //
                            //if(j%%2==0){
                            //    tr += '<td style="text-align:left;">'+data.list[i][dnl[j]]+'</td>';      /*ID因为td要按不同方式对齐，所以要这样处理*/
                           // }else{
                            //    tr += '<td style="text-align:right;">'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            //}
                            //
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }
                function %(name)s_jf(jf){
                    var keyd=document.getElementById('%(name)s_keyword').value
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"+"&jf_type="+jf+"&keyword="+keyd,
                        dataType:"json",
                        success:%(name)s_loadUsers_success2,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }


                /*这个是成功访问服务之后返回的处理2*/
                function %(name)s_loadUsers_success2(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){

                            tr += '<td >'+data.list[i][dnl[j]]+'</td>';   //原来的方式，不用区分对齐
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    a= $('select[name=jf_type]').val();
                    b= $('input[name=jf_type]:checked').val();
                    if(b){
                        if(a==1){
                            $("input[name='jf_type']").removeAttr("checked");
                            $("input[name='jf_type'][value='1']").prop("checked",'1');
                        }
                        if(a==2){
                            $("input[name='jf_type']").removeAttr("checked");
                            $("input[name='jf_type'][value='2']").prop("checked",'1');
                        }
                        if(a==3){
                            $("input[name='jf_type']").removeAttr("checked");
                            $("input[name='jf_type'][value='3']").prop("checked",'1');
                        }
                        if(a==4){
                            $("input[name='jf_type']").removeAttr("checked");
                            $("input[name='jf_type'][value='4']").prop("checked",'1');
                        }
                    }
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){

                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){
                    
                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
            </style>
        """%{'sUrl':self.sUrl,'name':self.name,'nllen':len(self.nl),'ojs':self.confirmjs,'cjs':self.clearjs,'searchUrl':self.__searchUrl,'dnl':self.dnl}
        return s
    
    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''

# wjwcw项目关联合同
class mselect_forHT:
        top_btns_script = ''  ##top_btns的JS
        top_btns = ''  ##按钮 | 筛选
        __searchUrl = ''

        def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                     search_holder='请输入合同名称'):
            self.can_select = can[0]
            self.can_clear = can[1]
            self.nl = nl
            self.showSearch = showSearch
            self.name = name
            self.title = title
            self.wh = wh
            self.sUrl = ''
            self.Html = CHtml()
            self.cln_btn = '''&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>'''%self.name
            self.callback()
            self.search_holder = search_holder
            self.dnl = []
            if len(dnl) <= 0:
                for idd in range(len(self.nl)):
                    self.dnl.append(idd)
            else:
                self.dnl = dnl
                # self.dnl 查询语句需要返回的字段索引
            #self.nl.append('查看')
            #self.dnl.append(-1)

        def getHTML(self):
            return self.selusers() + self.cln_btn

        def selusers(self):

            html = ''
            # 触发按钮
            btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>'''%self.name
            html += btnb_role

            # 模态框内容，最外层框
            div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                         "class": "modal fade myModalStyle",
                                         "tabindex": "-1",
                                         "role": "dialog",
                                         "aria-labelledby": "%s_ModalLabel" % self.name,
                                         "aria-hidden": "true"})
            if self.wh != []:
                div_modal.addAttr({'style': 'width:%spx;margin-left:-%spx;left:50%%;' % (
                self.wh[0], self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

            # 模态框头部
            div_modal_head = cTag('div', '', {"class": "modal-header"})
            btn_head_close = cTag('button', '×', {"type": "button",
                                                  "class": "close",
                                                  "data-dismiss": "modal",
                                                  "aria-hidden": "true"})
            txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name,"style":"font-size:20px;"})
            div_modal_head.add(btn_head_close.getHTML())
            div_modal_head.add(txt_head_content.getHTML())
            div_modal.add(div_modal_head.getHTML())

            # 模态框搜索框

            div_modal.add(self.search_html())

            # 模态框的body
            div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;" % self.wh[1]})
            div_modal_body_s = cTag('div', '', {'class': 'modal-body',
                                                "style": "height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;" % (
                                                self.wh[1])})
            table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
            thead = cTag('thead')
            tr = cTag('tr')
            for n in self.nl:
                tr.add(cTag('th', n).getHTML())
            tr.add(cTag('th', '查看').getHTML())
            thead.add(tr.getHTML())
            table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

            # tbody 的内容由js构造，确保能获取最新的权限情况
            tbody = cTag('tbody', '', {'class': 'table table-hover'})
            table_users.add(tbody.getHTML())
            #div_modal_body.add(table_users.getHTML())
            div_modal_body_s.add(table_users.getHTML())
            div_modal_body.add(div_modal_body_s.getHTML())
            div_modal.add(div_modal_body.getHTML())

            # 模态框的脚部
            div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
            btn_modal_ok = cTag('button', '确定',
                                {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                                 'aria-hidden': 'true'})
            btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
            div_modal_footer.add(btn_modal_ok.getHTML())
            div_modal_footer.add(btn_modal_close.getHTML())
            div_modal.add(div_modal_footer.getHTML())

            aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
            # 最后整块处理
            html += div_modal.getHTML() + aValue
            return html + self.js()

        def top_btns_btn(self):
            s = '%s%s' % (self.top_btns, self.top_btns_script)

            return s

        def getUrlStr(self):
            return self.__searchUrl

        def setUrlArg(self, dis={}):
            ##追加参数
            for e in dis.keys():
                self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

        def search_html(self):
            div_modal_search = cTag('div', '', {"class": "modal-header"})

            key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                         {'id': '%s_keyword' % self.name, 'class': 'form-control span1',
                                          'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})

            btn_search = cTag('input', '', {"value": "搜索",
                                            "type": "button",
                                            'style': 'margin:5px;',
                                            "class": "btn",
                                            "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                            self.name, self.name)})
            if self.showSearch == 1:

                div_modal_search.add(key_search)
                div_modal_search.add(btn_search.getHTML())
            div_modal_search.add('&nbsp;&nbsp;')
            div_modal_search.add(self.top_btns_btn())
            self.__searchUrl += '+"&keyword="+keyword'
            return div_modal_search.getHTML()

        def js(self):
            s = """<script>

                    function %(name)s_loadUsersList(keyword){

                        $.ajax({
                            type: "GET",
                            url: "%(sUrl)s"%(searchUrl)s,
                            dataType:"json",
                            success:%(name)s_loadUsers_success,
                            error:function(XMLHttpRequest,errorMsg){
                                alert('异步请求异常请联系管理员');
                            }
                        });
                    }

                    /*这个是成功访问服务之后返回的处理*/
                    function %(name)s_loadUsers_success(data){
                        //data=$.parseJSON(data)

                        var listLen = data.list.length;     /*列表的长度*/
                        var tbody = $("#table_%(name)s_List").find('tbody');
                        var i = 0;
                        var tr_total = '';
                        var listlen = %(nllen)s;
                        var dnl=%(dnl)s;
                        for(i=0;i<listLen;i++){
                            if(i%%2==0){
                                tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                            }else{
                                tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                            }
                            for(j=0;j<listlen;j++){
                                tr += '<td>'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            }
                            tr += '<td >'+'<a  href="admin?fid=F012&pageNo=1&part=localfrm&pk='+data.list[i][dnl[0]]+'" target="_blank">查看</a>'+'</td>';
                            tr += '</tr>';
                            tr_total += tr;
                        }
                        tbody.html(tr_total);

                        /*然后显示模态框*/

                         a= $('input[name=jf_type]:checked').val();
                        $('select[name=jf_type]').val(a);
                        $('#%(name)s_Modal').modal({backdrop: 'static'});
                        $('#%(name)s_Modal').modal('show');
                        $("#%(name)s_aValue").val('');


                    }

                    function %(name)s_rowSel(objMe,aValue,i){

                        thisTr = $(objMe);
                        var tbody = $("#table_%(name)s_List").find('tbody');
                        tbody.find('tr').removeClass('lsTRSel');
                        tbody.find('tr').children('td').children('a').removeAttr("style");//修改查看的样式
                        thisTr.children('td').children('a').css("color","#ffffff");//修改查看的样式
                        thisTr.addClass('lsTRSel');
                        tbody.find('tr').not(thisTr).addClass('lsTR0');
                        tbody.find('tr').not(thisTr).children('td').children('a').removeAttr("style");//修改查看的样式
                        $("#%(name)s_aValue").val(aValue);
                    }

                    function %(name)s_OutPut(obj){

                        sData=$("#%(name)s_aValue").val();
                        %(name)s_setOutPut(sData);
                    }
                    function %(name)s_setOutPut(sData){
                        %(ojs)s
                    }
                    function %(name)s_clearPutOut(){
                        %(cjs)s
                    }
                </script>
                <style>
                .form-horizontal .mylabel{display:inline-block;text-align:left;}
                .separ{margin-bottom:10px;margin-top:10px;}
                .mybadge{display:inline-block;margin-right:5px;}
                .mytextarea{width:300px;height:100px;}
                .form .mysubbtn:first-child{margin-left:212px;width:100px;}
                .myModalStyle{width:800px;left:40%%}

                .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
                .lsTR0{CURSOR: hand; BackGround-Color: white}
                .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
                .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
                .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
                </style>
            """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs,
                   'cjs': self.clearjs, 'searchUrl': self.__searchUrl, 'dnl': self.dnl}
            return s

        def callback(self):
            self.confirmjs = '''
            alert(sData);
            '''
            self.clearjs = '''
            alert('clear');
            '''

# wjwcw项目关联公文
class mselect_forlink_GW:
        top_btns_script = ''  ##top_btns的JS
        top_btns = ''  ##按钮 | 筛选
        __searchUrl = ''

        def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],width=[],
                     search_holder='请输入公文名称'):
            self.can_select = can[0]
            self.can_clear = can[1]
            self.nl = nl
            self.showSearch = showSearch
            self.name = name
            self.title = title
            self.wh = wh
            self.width=width
            self.sUrl = ''
            self.Html = CHtml()
            self.cln_btn = '''&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>'''%self.name
            self.callback()
            self.search_holder = search_holder
            self.dnl = []
            if len(dnl) <= 0:
                for idd in range(len(self.nl)):
                    self.dnl.append(idd)
            else:
                self.dnl = dnl
                # self.dnl 查询语句需要返回的字段索引
            #self.nl.append('查看')
            #self.dnl.append(-1)

        def getHTML(self):
            return self.selusers() + self.cln_btn

        def selusers(self):

            html = ''
            # 触发按钮
            btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>'''%self.name
            html += btnb_role

            # 模态框内容，最外层框
            div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                         "class": "modal fade myModalStyle",
                                         "tabindex": "-1",
                                         "role": "dialog",
                                         "aria-labelledby": "%s_ModalLabel" % self.name,
                                         "aria-hidden": "true"})
            if self.wh != []:
                div_modal.addAttr({'style': 'width:%spx;margin-left:-%spx;left:50%%;' % (
                self.wh[0], self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

            # 模态框头部
            div_modal_head = cTag('div', '', {"class": "modal-header"})
            btn_head_close = cTag('button', '×', {"type": "button",
                                                  "class": "close",
                                                  "data-dismiss": "modal",
                                                  "aria-hidden": "true"})
            txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name,"style":"font-size:20px;"})
            div_modal_head.add(btn_head_close.getHTML())
            div_modal_head.add(txt_head_content.getHTML())
            div_modal.add(div_modal_head.getHTML())

            # 模态框搜索框

            div_modal.add(self.search_html())

            # 模态框的body
            div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;" % self.wh[1]})
            div_modal_body_s = cTag('div', '', {'class': 'modal-body',
                                                "style": "height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;" % (
                                                self.wh[1])})
            table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
            thead = cTag('thead')
            tr = cTag('tr')
            i=0
            for n in self.nl:
                tr.add(cTag('th', n , {'width':self.width[i]}).getHTML())
                i+=1
            tr.add(cTag('th', '查看' ,{'width':'10%%'}).getHTML())
            thead.add(tr.getHTML())
            table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

            # tbody 的内容由js构造，确保能获取最新的权限情况
            tbody = cTag('tbody', '', {'class': 'table table-hover'})
            table_users.add(tbody.getHTML())
            #div_modal_body.add(table_users.getHTML())
            div_modal_body_s.add(table_users.getHTML())
            div_modal_body.add(div_modal_body_s.getHTML())
            div_modal.add(div_modal_body.getHTML())

            # 模态框的脚部
            div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
            btn_modal_ok = cTag('button', '确定',
                                {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                                 'aria-hidden': 'true'})
            btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
            div_modal_footer.add(btn_modal_ok.getHTML())
            div_modal_footer.add(btn_modal_close.getHTML())
            div_modal.add(div_modal_footer.getHTML())

            aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
            # 最后整块处理
            html += div_modal.getHTML() + aValue
            return html + self.js()

        def top_btns_btn(self):
            s = '%s%s' % (self.top_btns, self.top_btns_script)

            return s

        def getUrlStr(self):
            return self.__searchUrl

        def setUrlArg(self, dis={}):
            ##追加参数
            for e in dis.keys():
                self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

        def search_html(self):
            div_modal_search = cTag('div', '', {"class": "modal-header"})

            key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                         {'id': '%s_keyword' % self.name, 'class': 'form-control span1',
                                          'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})

            btn_search = cTag('input', '', {"value": "搜索",
                                            "type": "button",
                                            'style': 'margin:5px;',
                                            "class": "btn",
                                            "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                            self.name, self.name)})
            if self.showSearch == 1:

                div_modal_search.add(key_search)
                div_modal_search.add(btn_search.getHTML())
            div_modal_search.add('&nbsp;&nbsp;')
            div_modal_search.add(self.top_btns_btn())
            self.__searchUrl += '+"&keyword="+keyword'
            return div_modal_search.getHTML()

        def js(self):
            s = """<script>

                    function %(name)s_loadUsersList(keyword){

                        $.ajax({
                            type: "GET",
                            url: "%(sUrl)s"%(searchUrl)s,
                            dataType:"json",
                            success:%(name)s_loadUsers_success,
                            error:function(XMLHttpRequest,errorMsg){
                                alert('异步请求异常请联系管理员');
                            }
                        });
                    }

                    /*这个是成功访问服务之后返回的处理*/
                    function %(name)s_loadUsers_success(data){
                        //data=$.parseJSON(data)

                        var listLen = data.list.length;     /*列表的长度*/
                        var tbody = $("#table_%(name)s_List").find('tbody');
                        var i = 0;
                        var tr_total = '';
                        var listlen = %(nllen)s;
                        var dnl=%(dnl)s;
                        for(i=0;i<listLen;i++){
                            if(i%%2==0){
                                tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                            }else{
                                tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                            }
                            for(j=0;j<listlen;j++){
                                tr += '<td>'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            }
                            if(data.list[i][4]!=6){
                                tr += '<td >'+'<a  href="admin?fid=F008&pageNo=1&part=localfrm&pk='+data.list[i][0]+'" target="_blank">查看</a>'+'</td>';
                            }else{
                                tr += '<td >'+'<a  href="admin?fid=F104&pageNo=1&part=localfrm&pk='+data.list[i][0]+'" target="_blank">查看</a>'+'</td>';
                            }
                            
                            tr += '</tr>';
                            tr_total += tr;
                        }
                        tbody.html(tr_total);

                        /*然后显示模态框*/

                         a= $('input[name=jf_type]:checked').val();
                        $('select[name=jf_type]').val(a);
                        $('#%(name)s_Modal').modal({backdrop: 'static'});
                        $('#%(name)s_Modal').modal('show');
                        $("#%(name)s_aValue").val('');


                    }

                    function %(name)s_rowSel(objMe,aValue,i){

                        thisTr = $(objMe);
                        var tbody = $("#table_%(name)s_List").find('tbody');
                        tbody.find('tr').removeClass('lsTRSel');
                        tbody.find('tr').children('td').children('a').removeAttr("style");//修改查看的样式
                        thisTr.children('td').children('a').css("color","#ffffff");//修改查看的样式
                        thisTr.addClass('lsTRSel');
                        tbody.find('tr').not(thisTr).addClass('lsTR0');
                        tbody.find('tr').not(thisTr).children('td').children('a').removeAttr("style");//修改查看的样式
                        $("#%(name)s_aValue").val(aValue);
                    }

                    function %(name)s_OutPut(obj){

                        sData=$("#%(name)s_aValue").val();
                        %(name)s_setOutPut(sData);
                    }
                    function %(name)s_setOutPut(sData){
                        %(ojs)s
                    }
                    function %(name)s_clearPutOut(){
                        %(cjs)s
                    }
                </script>
                <style>
                .form-horizontal .mylabel{display:inline-block;text-align:left;}
                .separ{margin-bottom:10px;margin-top:10px;}
                .mybadge{display:inline-block;margin-right:5px;}
                .mytextarea{width:300px;height:100px;}
                .form .mysubbtn:first-child{margin-left:212px;width:100px;}
                .myModalStyle{width:800px;left:40%%}

                .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
                .lsTR0{CURSOR: hand; BackGround-Color: white}
                .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
                .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
                .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
                </style>
            """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs,
                   'cjs': self.clearjs, 'searchUrl': self.__searchUrl, 'dnl': self.dnl}
            return s

        def callback(self):
            self.confirmjs = '''
            alert(sData);
            '''
            self.clearjs = '''
            alert('clear');
            '''


class mselect_forSW(mselect_forHT):            
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                 search_holder='请输入合同名称'):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btn = '''&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>'''%self.name
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl
            # self.dnl 查询语句需要返回的字段索引
        #self.nl.append('查看')
        #self.dnl.append(-1)

    def getHTML(self):
        return self.selusers() + self.cln_btn

    def selusers(self):

        html = ''
        # 触发按钮
        btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>'''%self.name
        html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;margin-left:-%spx;left:50%%;' % (
            self.wh[0], self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name,"style":"font-size:20px;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())
        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框

        div_modal.add(self.search_html())

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;" % self.wh[1]})
        div_modal_body_s = cTag('div', '', {'class': 'modal-body',
                                            "style": "height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;" % (
                                            self.wh[1])})
        table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add(cTag('th', n).getHTML())
        tr.add(cTag('th', '查看').getHTML())
        thead.add(tr.getHTML())
        table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

        # tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody', '', {'class': 'table table-hover'})
        table_users.add(tbody.getHTML())
        #div_modal_body.add(table_users.getHTML())
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = '%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header"})

        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'form-control span1',
                                      'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})

        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                        self.name, self.name)})
        if self.showSearch == 1:

            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword'
        return div_modal_search.getHTML()      
    
    def js(self):
        s = """<script>

                function %(name)s_loadUsersList(keyword){

                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){
                            if (j==0){
                                tr += '<td style=width:15%%>'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            }else{tr += '<td>'+data.list[i][dnl[j]]+'</td>';      /*ID*/}
                        }
                        tr += '<td style=width:10%%>'+'<a  href="admin?fid=F104&pageNo=1&part=localfrm&pk='+data.list[i][dnl[0]]+'" target="_blank">查看</a>'+'</td>';
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/

                     a= $('input[name=jf_type]:checked').val();
                    $('select[name=jf_type]').val(a);
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');


                }

                function %(name)s_rowSel(objMe,aValue,i){

                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    tbody.find('tr').children('td').children('a').removeAttr("style");//修改查看的样式
                    thisTr.children('td').children('a').css("color","#ffffff");//修改查看的样式
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    tbody.find('tr').not(thisTr).children('td').children('a').removeAttr("style");//修改查看的样式
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){

                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
            </style>
        """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs,
               'cjs': self.clearjs, 'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s
    
    def callback(self):
            self.confirmjs = '''
            alert(sData);
            '''
            self.clearjs = '''
            alert('clear');
            '''
        

class mselect_forSH(mselect_forHT):      
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                 search_holder='请输入合同名称'):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btn = '''&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>'''%self.name
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl
            # self.dnl 查询语句需要返回的字段索引
        #self.nl.append('查看')
        #self.dnl.append(-1)

    def getHTML(self):
        return self.selusers() + self.cln_btn

    def selusers(self):

        html = ''
        # 触发按钮
        btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>'''%self.name
        html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;margin-left:-%spx;left:50%%;' % (
            self.wh[0], self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name,"style":"font-size:20px;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())
        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框

        div_modal.add(self.search_html())

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;" % self.wh[1]})
        div_modal_body_s = cTag('div', '', {'class': 'modal-body',
                                            "style": "height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;" % (
                                            self.wh[1])})
        table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add(cTag('th', n).getHTML())
        tr.add(cTag('th', '查看').getHTML())
        thead.add(tr.getHTML())
        table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

        # tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody', '', {'class': 'table table-hover'})
        table_users.add(tbody.getHTML())
        #div_modal_body.add(table_users.getHTML())
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = '%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header"})

        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'form-control span1',
                                      'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})

        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                        self.name, self.name)})
        if self.showSearch == 1:

            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword'
        return div_modal_search.getHTML()      
    
    def js(self):
        s = """<script>

                function %(name)s_loadUsersList(keyword){

                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){
                            if (j==0){
                                tr += '<td style=width:15%%>'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            }else{tr += '<td>'+data.list[i][dnl[j]]+'</td>';      /*ID*/}
                        }
                        tr += '<td style=width:10%%>'+'<a  href="admin?fid=SH204&pageNo=1&part=localfrm&pk='+data.list[i][dnl[0]]+'" target="_blank">查看</a>'+'</td>';
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/

                     a= $('input[name=jf_type]:checked').val();
                    $('select[name=jf_type]').val(a);
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');


                }

                function %(name)s_rowSel(objMe,aValue,i){

                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    tbody.find('tr').children('td').children('a').removeAttr("style");//修改查看的样式
                    thisTr.children('td').children('a').css("color","#ffffff");//修改查看的样式
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    tbody.find('tr').not(thisTr).children('td').children('a').removeAttr("style");//修改查看的样式
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){

                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
            </style>
        """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs,
               'cjs': self.clearjs, 'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s
    
    def callback(self):
            self.confirmjs = '''
            alert(sData);
            '''
            self.clearjs = '''
            alert('clear');
            '''
        
class cSel_Dept_User:
    """docstring for mselect_1"""
    def __init__(self , name , url, nl = [],title = '选择数据' ,sc = '',**kwargs):
        
        self.nl = nl
        self.name = name
        self.title = title
        if not sc:
            self.sc=len(self.nl)
        else:
            self.sc=sc
        self.sUrl = url
        self.Html = CHtml()
        
        self.attrs={}
        self.init_attrs(kwargs)
        
        self._search_html = self.search_html()
        
        # self.cln_btn = """<button type="button" class="btn" onclick="%s_clearPutOut();">清除</button>""" %self.name
        # self.callback()

    def init_attrs(self,kwargs):
        self.attrs['right_title']=kwargs.get('right_title','已选人员')

        self.attrs['selbtn']=kwargs.get('selbtn',True)
        self.attrs['clrbtn']=kwargs.get('clrbtn',True)
        self.attrs['selbtn_name']=kwargs.get('selbtn_name','选择')
        self.attrs['clrbtn_name']=kwargs.get('clrbtn_name','清除')

        self.attrs['width']=kwargs.get('width',800)
        self.attrs['height']=kwargs.get('height',300)
        self.attrs['show_head']=kwargs.get('show_head',True)
        self.attrs['tr_hover_sty']=kwargs.get('tr_hover_sty','BackGround-Color : #3778EC;')

        self.attrs['url_data']=kwargs.get('url_data','{}')
        
        self.attrs['seach_ext']=kwargs.get('seach_ext','')


        tr_sel_js="""
            thisCK=$(objMe);
            thisTr = $(objMe);
            var tbody = $("#table_%s_List").find('tbody');
            tbody.find('tr').removeClass('lsTRSel');
            thisTr.addClass('lsTRSel');
            tbody.find('tr').not(thisTr).addClass('lsTR0');

            var aValue=thisTr.attr('l-data');
            $("#%s_aValue").val(aValue);
        """%(self.name,self.name)
        self.attrs['tr_sel_js']=kwargs.get('tr_sel_js',tr_sel_js)

        output_js="""
            sData=$("#%s_aValue").val();
            %s_setOutPut(sData);
        """%(self.name,self.name)
        self.attrs['output_js']=kwargs.get('output_js',output_js)

        self.attrs['before_js']=kwargs.get('before_js',"")
        self.attrs['confirm_js']=kwargs.get('confirm_js','alert(sData);')
        self.attrs['clear_js']=kwargs.get('clear_js','alert(sData);')

    def __setitem__(self,key,value):
        if self.attrs.has_key(key):
            self.attrs[key]=value

        return self


    def getHTML(self):
        return self.selusers()

    def selusers(self, ext=''):
        html=''
        html = ''
        #触发按钮
        if self.attrs['selbtn']:
            btn_role = cTag('input','',{"value":self.attrs['selbtn_name'],
                                        "type":"button",
                                        "style":"margin-left:5px;color:#FFF;background-color:#36648B",
                                        "class":"btn btn-success span2",
                                        "onclick":"%s_loadList('', '%s');"%(self.name,ext)})
            html += btn_role.getHTML()

        if self.attrs['clrbtn']:
            btn_clr = cTag('input','',{"value":self.attrs['clrbtn_name'],
                                        "type":"button",
                                        "style":"margin-left:5px;color:#FFF;background-color:#36648B",
                                        "class":"btn btn-success span2",
                                        "onclick":"%s_clearPutOut('', '%s');"%(self.name,ext)})
            html += btn_clr.getHTML()

        #模态框内容，最外层框
        div_modal = cTag('div','',{"id"      :"%s_Modal"%self.name, 
                                   "class"   :"modal fade myModalStyle", 
                                   "tabindex":"-1", 
                                   "role"    :"dialog", 
                                   "aria-labelledby"  :"%s_ModalLabel"%self.name,
                                   "aria-hidden"      :"true"})
        
        #模态框头部
        div_modal_head = cTag('div','',{"class":"modal-header"})
        btn_head_close = cTag('button','×',{"type"        :"button", 
                                            "class"       :"close", 
                                            "data-dismiss":"modal",
                                            "aria-hidden" :"true",
                                            "onclick":"clear_put('%s');"%self.name})
        txt_head_content = cTag('h4',self.title,{"id":"%s_ModalLabel"%self.name,'style':'margin-top:15px;margin-left:25px'})
        div_modal_head.add( btn_head_close.getHTML() )
        div_modal_head.add( txt_head_content.getHTML() )
        div_modal.add( div_modal_head.getHTML() )       

        #模态框搜索框
        self._search_html='' #不需要搜索
        div_modal.add( self._search_html )       

        #模态框的body
        div_modal_body  = cTag('div', '', {'class':'modal-body',"style":"height:300px; clear:both;"})
        
        div_source_head=cTag('div', '通讯录', {'class':'modal-body','style':"  background-color: rgb(203, 203, 203); padding: 10px; text-align: center;font-size: 16px;"})
        div_modal_body_left=cTag('div', '', {'class':'modal-body',"style":"height:300px; width:35%;float:left;border: 1px solid rgb(238, 238, 238);margin-left: 25px;"})
        
        div_modal_body_center=cTag('div', '', {'class':'modal-body',"style":"height:200px; width:10%;float:left;padding:0;margin-top:100px;"})
        
        div_modal_body_right=cTag('div', '', {'class':'modal-body',"style":"height:300px; width:35%;float:left; border: 1px solid rgb(238, 238, 238);margin-left: 5px; border-radius: 5px;"})
        
        
        table_users     = cTag('div','<ul id="%s_treeObj" class="ztree"></ul>'%self.name,{'id':'table_%s_List'%self.name,'class':'table table-hover'})
        
        if self.attrs['right_title']:
           div_sel_head=cTag('div', self.attrs['right_title'], {'class':'modal-body','style':"  background-color: rgb(203, 203, 203); padding: 10px; text-align: center;font-size: 16px;"})
        else:
           div_sel_head=cTag('div', '已选人员', {'class':'modal-body','style':"  background-color: rgb(203, 203, 203); padding: 10px; text-align: center;font-size: 16px;"})

        div_sel_value=cTag('div', '<ul id="%s_selvalues" class="sel_ul"></ul>'%self.name, {'class':'modal-body','id':'div_%s_sel_value'%(self.name)})
        
        #左边显示查询结果集
        div_modal_body_left.add(div_source_head.getHTML())
        div_modal_body_left.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_left.getHTML())
        
        #中间操作区
        str_aleft="<div style='text-align:center; height:25%%'>%s</div>"%cTag("button",'<i class="icon-step-forward"></i>',
            {"class":"btn fa fa-angle-double-right", "name":"aleft",  "type":"button", "onclick":"%s_selAdd();"%self.name}).getHTML()
        
        str_aright="<div style='text-align:center; height:25%%'>%s</div>"%cTag("button",'<i class="icon-step-backward"></i>',
            {"class":"btn fa fa-angle-double-left", "name":"aright", "type":"button", "onclick":"%s_selDel();"%self.name}).getHTML()
        
      
        div_modal_body_center.add(str_aleft)
        div_modal_body_center.add(str_aright)        
        div_modal_body.add(div_modal_body_center.getHTML())
        
        #右边显示勾选的结果集
        div_modal_body_right.add(div_sel_head.getHTML())
        div_modal_body_right.add(div_sel_value.getHTML())
        div_modal_body.add(div_modal_body_right.getHTML())
        
        div_modal.add( div_modal_body.getHTML() )
        
        #模态框的脚部
        div_modal_footer = cTag('div','', {'class':'modal-footer'} )
        btn_modal_ok = cTag('button','确定', {'class':'btn', 'data-dismiss':'modal','onclick':'%s_OutPut();'%self.name , 'aria-hidden':'true'})
        btn_modal_close = cTag('button','关闭', {'class':'btn', 'data-dismiss':'modal', 'aria-hidden':'true', 'onclick':"clear_put('%s');"%self.name})
        div_modal_msg=cTag('div','',{'class':'%s-model-msg pull-left'%(self.name)})
        div_modal_footer.add(div_modal_msg.getHTML())
        div_modal_footer.add( btn_modal_ok.getHTML() )
        div_modal_footer.add( btn_modal_close.getHTML() )
        div_modal.add( div_modal_footer.getHTML() )
        
        aValue = self.Html.input('','aValue','hidden',{'id':'%s_aValue'%self.name})
        #最后整块处理
        html += div_modal.getHTML()+aValue
        return html + self.js()

    def search_html(self):
        div_modal_search = cTag('div','',{"class":"modal-header","id":'search_area'})
        key_search = self.Html.input('','%s_keyword'%self.name,'text',{'id':'%s_keyword'%self.name,'class':'form-control span3','placeholder':'请输入关键字'})
        btn_search = cTag('input','',{"value":"搜索",
                                      "type":"button",
                                      "class":"btn",
                                      "onclick":"var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};"%(self.name,self.name),
                                      'style':"vertical-align: top;"                                      
                                      })
        div_modal_search.add( key_search)
        div_modal_search.add( btn_search.getHTML() )
        div_modal_search.add(self.attrs['seach_ext'])
        self.searchUrl = '+"&keyword="+keyword'
        return div_modal_search.getHTML()
    
    def js(self):
        s=""" <style>
                 .sel_ul li{
                      font-size: 14px;
                      font-family: Verdana, Arial, Helvetica, AppleGothic, sans-serif;
                 }
                 .sel_li{
                         cursor: pointer;
                         }
                 .sel_li:hover {background-color:#f5f5f5; color:#FF5300;}
                 .sel{
                     background-color:#f5f5f5; color:#FF5300;
                 }
              </style>     
            <script>
                var setting = {
                    data: {
                        key: {
                            title:"t"
                        },
                        simpleData: {
                            enable: true
                        }                        
                    },
                    view: {
                        dblClickExpand: false
                    },
                    callback: {
                        onDblClick: %(name)s_OnDblClick
                    }
                };
                
                //$(document).ready(function(){
                //    $.fn.zTree.init($("#%(name)s_treeObj"), setting, zNodes);
                //});
                
                $(function(){
                    $('#%(name)s_Modal').appendTo('body');
                });

                function clear_put(name){
                    $('[name='+name+'_keyword]').val('');
                }
                function %(name)s_loadList(keyword){                    
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        data:%(url_data)s,
                        beforeSend:%(name)s_before,
                        success:%(name)s_load_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_load_success(data){
                    data=eval('('+data+')');
                    var listLen = data.list.length;     /*列表的长度*/
                    var i = 0;                    
                    s=''
                    var zNodes=[];
                    for(i=0;i<listLen;i++){
                        if (data.list[i][3]==0){
                            t={id:data.list[i][0],pId:data.list[i][2], name:data.list[i][1],t:data.list[i][1],type:data.list[i][4],ilevel:data.list[i][3], open:false}
                        }else{
                            t={id:data.list[i][0],pId:data.list[i][2], name:data.list[i][1],t:data.list[i][1], type:data.list[i][4],ilevel:data.list[i][3], open:false}
                        }
                        zNodes.push(t);
                        //s+="<div style='width:50%%; float:left;'><div><input type='checkbox' value="+data.list[i][0]+" onclick='%(name)s_rowSel(this);' style='float: left;margin-right: 5px;margin-top: 3px;'><label style='float: left;'>"+data.list[i][1]+"</label></div></div>"
                    } 
                    $.fn.zTree.init($("#%(name)s_treeObj"), setting, zNodes);
                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe){
                    %(tr_sel_js)s
                }
                
                function %(name)s_delSel(objMe){
                    var mychk=$(objMe);
                    var conbox=$('#table_%(name)s_List')
                    var myparent=mychk.parent();
                    myparent.remove();
                    var chk=conbox.find('input[value="'+mychk[0].value+'"]')
                    if (chk.length>0){
                        chk[0].checked=false;
                    }
                }
                function %(name)s_OnDblClick(event, treeId, treeNode) {
                    var treename= treeId.split('_')[0];
                    var vobj=$('#'+treename+'_selvalues');
                    var o=vobj.find($('li[key_oid='+treeNode.id+']'));
                    if (o.length>0){
                        alert('该数据已选择！')
                        return;
                    }
                    if (treeNode.type==1){         
                        var sid=treeNode.id;
                        sid=sid.split('-')[1];
                        s='<li key_oid='+treeNode.id+' key_id='+sid+' key_type='+treeNode.type+' key_name='+treeNode.name+' class="sel_li" onclick="%(name)s_changeSel(this)" ondblclick="%(name)s_delSel(this)">'+treeNode.name+'</li>';
                    }else{
                        s='<li key_oid='+treeNode.id+' key_id='+treeNode.id+' key_type='+treeNode.type+' key_name='+treeNode.name+' class="sel_li" onclick="%(name)s_changeSel(this)" ondblclick="%(name)s_delSel(this)">'+treeNode.name+'</li>';
                    }
                    vobj.append(s);
                };
                
                function %(name)s_selAdd(){
                    var treeObj = $.fn.zTree.getZTreeObj('%(name)s_treeObj');
                    var nodes = treeObj.getSelectedNodes();
                    var node=nodes[0]
                    
                    var vobj=$('#%(name)s_selvalues');
                    
                    var o=vobj.find($('li[key_oid='+node.id+']'));
                    if (o.length>0){
                        alert('该数据已选择！')
                        return;
                    }
                    
                    if (node.type==1){         
                        var sid=node.id;
                        sid=sid.split('-')[1];
                        s='<li key_oid='+node.id+' key_id='+sid+' key_type='+node.type+' key_name='+node.name+' class="sel_li" onclick="%(name)s_changeSel(this)"  ondblclick="%(name)s_delSel(this)">'+node.name+'</li>';
                    }else{
                        s='<li key_oid='+node.id+' key_id='+node.id+' key_type='+node.type+' key_name='+node.name+' class="sel_li" onclick="%(name)s_changeSel(this)"  ondblclick="%(name)s_delSel(this)">'+node.name+'</li>';
                    }
                    vobj.append(s);
                }
                
                function %(name)s_selDel(){
                    var vobj=$('.sel')
                    vobj.remove();
                }
                
                function %(name)s_changeSel(obj){
                    var vobj=$('#%(name)s_selvalues');
                    var li=vobj.find('li');
                    li.removeClass('sel');
                    $(obj).addClass('sel');                    
                }
                
                function %(name)s_delSel(obj){
                    var vobj=$(obj)
                    vobj.remove();
                }
                
                function %(name)s_OutPut(){
                    %(output_js)s                    
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                } 
                function %(name)s_before(){
                    %(before_js)s
                }   
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:%(outWidth)spx;left:50%%;margin-left:%(mLeftWidth)spx;text-align:left;}

            .table-hover tbody tr:hover>td{%(tr_hover_sty)s}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC}                
            </style>
        """%{'sUrl':self.sUrl,'name':self.name,'ojs':self.attrs['confirm_js'],'cjs':self.attrs['clear_js'],'searchUrl':self.searchUrl
             ,'outWidth':self.attrs['width'],'mLeftWidth':int(self.attrs['width'] * 0.5) * -1, 'sc':self.sc,
             'tr_sel_js':self.attrs['tr_sel_js'],'output_js':self.attrs['output_js'],
             'url_data':self.attrs['url_data'],'before_js':self.attrs['before_js'],'tr_hover_sty':self.attrs['tr_hover_sty']}
   
        return s
    
    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''


class cSel_Dept_User1(cSel_Dept_User):
    """docstring for mselect_1"""
    def js(self):
        s=""" <style>
                #tom
                dept_modal{z-index:1;}
                 .sel_ul li{
                      font-size: 14px;
                      font-family: Verdana, Arial, Helvetica, AppleGothic, sans-serif;
                 }
                 .sel_li{
                         cursor: pointer;
                         }
                 .sel_li:hover {background-color:#f5f5f5; color:#FF5300;}
                 .sel{
                     background-color:#f5f5f5; color:#FF5300;
                 }
              </style> 
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:%(outWidth)spx;left:50%%;margin-left:%(mLeftWidth)spx;text-align:left;bottom: -100px;}
            .table-hover tbody tr:hover>td{%(tr_hover_sty)s}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC}                
            </style>"""%{'tr_hover_sty':self.attrs['tr_hover_sty'],'mLeftWidth':int(self.attrs['width'] * 0.5) * -1,'outWidth':self.attrs['width']}

        return s


# wqoa项目关联
class mselect_forproj:
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[], search_holder=''):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btn = """&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>""" % self.name
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl

            # self.dnl 查询语句需要返回的字段索引

    def getHTML(self):
        return self.selusers() + self.cln_btn

    def selusers(self):

        html = ''
        # 触发按钮
        btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>''' % self.name
        html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;margin-left:-%spx;left:50%%;' % (
            self.wh[0], self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())
        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框

        div_modal.add(self.search_html())

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;" % self.wh[1]})
        table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add(cTag('th', n).getHTML())
        thead.add(tr.getHTML())
        table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

        # tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody', '', {'class': 'table table-hover'})
        table_users.add(tbody.getHTML())
        div_modal_body.add(table_users.getHTML())
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = '%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header"})
        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'form-control span3',
                                      'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})
        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                        self.name, self.name)})
        if self.showSearch == 1:
            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btns_btn())
        #self.__searchUrl += '+"&keyword="+keyword+"&hscode="+hscode+"&scode="+scode+"&mselect_hs="+mselect_hs+"&mselect_kc="+mselect_kc'
        self.__searchUrl += '+"&keyword="+keyword'
        return div_modal_search.getHTML()

    def js(self):
        s = """<script>

                function %(name)s_loadUsersList(keyword){

                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){
                            tr += '<td>'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){
                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){

                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC}
            </style>
        """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs, 'cjs': self.clearjs,
               'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s

    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''
        

# wqoa项目关联tip
class mselect_forproj_tip(mselect_forproj):
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[], search_holder='',control={'lineClick':'','lineStyle':''}):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btn = """&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>""" % self.name
        self.control = control
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl

            # self.dnl 查询语句需要返回的字段索引

    def selusers(self):

        html = ''
        # 触发按钮
        btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>''' % self.name
        html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;margin-left:-%spx;left:55%%;' % (
            self.wh[0], self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())
        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框

        div_modal.add(self.search_html())
        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;" % self.wh[1]})
        table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add(cTag('th', n).getHTML())
        thead.add(tr.getHTML())
        table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

        # tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody', '', {'class': 'table table-hover'})
        table_users.add(tbody.getHTML())
        div_modal_body.add(table_users.getHTML())
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header"})
        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'form-control span3',
                                      'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})
        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                        self.name, self.name)})
        if self.showSearch == 1:
            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btns_btn())
        #self.__searchUrl += '+"&keyword="+keyword+"&hscode="+hscode+"&scode="+scode+"&mselect_hs="+mselect_hs+"&mselect_kc="+mselect_kc'
        self.__searchUrl += '+"&keyword="+keyword'
        return div_modal_search.getHTML()
        
    def js(self):
        s = """<script>

                function %(name)s_loadUsersList(keyword){
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        dlist = data.list[i];
                        if(i%%2==0){
                            dlist = data.list[i];
                            tr = '<tr class="lsTR0" id = "Mesge'+dlist[dlist.length-1]+'" style="%(lineStyle)s" %(lineClick)s onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" id = "Mesge'+dlist[dlist.length-1]+'" style="%(lineStyle)s" %(lineClick)s onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){
                            if(j==0){
                                tr += '<td>'+data.list[i][dnl[j]]+'<input type="hidden" name="valuemsge" value="'+dlist[dlist.length-1]+'"></td>';      /*ID*/
                            }else{
                                tr += '<td>'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            }
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){
                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){

                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .table th,td{white-space: nowrap;}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
            </style>
        """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs, 'cjs': self.clearjs,
               'searchUrl': self.__searchUrl, 'dnl': self.dnl,'lineClick':self.control.get('lineClick',''),'lineStyle':self.control.get('lineStyle','')}
        return s

    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''
        
class mselect_mult_forList:
    top_btnbs_script=''   ##top_btnbs的JS
    top_btnbs=''   ##按钮 | 筛选
    __searchUrl = ''
    def __init__(self , name = 'm' , nl = [],title = '选择数据' , wh = [800,0] , can = [1,1] , has_open_botton=1):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.has_open_botton=has_open_botton
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btnb = '''&nbsp;<button class="btn_none" type="button" onclick="%s_clearPutOut()"><img src="asset/images/clr.png" style="width:28px;height:28px;" /></button>'''%self.name
        self.record_sel_js = ''
        self.callback()
        
    def getHTML(self):
        if self.has_open_botton==1:
            return self.selusers() + self.cln_btnb
        else:
            return self.selusers()
        
    def selusers(self):
        
        html = ''
        #触发按钮
        if self.has_open_botton==1:
            btnb_role = '''&nbsp;<button class="btn_none" type="button" onclick="%s_loadUsersList('')"><img src="asset/images/opt.png" style="width:28px;height:28px;" /></button>'''%self.name
            html += btnb_role
        
            

        #模态框内容，最外层框
        div_modal = cTag('div','',{"id"      :"%s_Modal"%self.name, 
                                   "class"   :"modal fade myModalStyle",
                                   "tabindex":"-1", 
                                   "role"    :"dialog", 
                                   "aria-labelledby"  :"%s_ModalLabel"%self.name, 
                                   "aria-hidden"      :"true"})
        if self.wh!=[]:
            div_modal.addAttr({'style':'width:%spx;margin-left:-%spx;left:50%%;'%(self.wh[0],self.wh[0]!='' and float(self.wh[0])/2 or '')})

        #模态框头部
        div_modal_head = cTag('div','',{"class":"modal-header"})
        btn_head_close = cTag('button','×',{"type"        :"button", 
                                            "class"       :"close", 
                                            "data-dismiss":"modal",
                                            "aria-hidden" :"true"})
        txt_head_content = cTag('h3',self.title,{"id":"%s_ModalLabel"%self.name,"style":"font-size:20px;"})
        div_modal_head.add( btn_head_close.getHTML() )
        div_modal_head.add( txt_head_content.getHTML() )
        div_modal.add( div_modal_head.getHTML() )

        #模态框搜索框
        
        div_modal.add( self.search_html() )       

        #模态框的body
        div_modal_body  = cTag('div', '', {'class':'modal-body',"style":"height:%spx;"%self.wh[1]})
        ####
        div_modal_body_s= cTag('div', '', {'class':'modal-body',"style":"height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;"%(self.wh[1])})

        ##########
        table_users     = cTag('table','',{'id':'table_%s_List'%self.name,'class':'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        tr.add( cTag('th', "<input type='checkbox' value=1 name='%s_selAllchk' onclick='%s_selAll(this)'/>"%(self.name,self.name)).getHTML() )
        for n in self.nl:
            tr.add( cTag('th', n).getHTML() )
        thead.add( tr.getHTML() )
        table_users.add( thead.getHTML() )   # table 分开 thead 和 tbody 标签

        #tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody','', {'class':'table table-hover'})
        table_users.add( tbody.getHTML() )
        #div_modal_body.add( table_users.getHTML() )
        ############
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        ############
        div_modal.add( div_modal_body.getHTML() )
        
        #模态框的脚部
        div_modal_footer = cTag('div','', {'class':'modal-footer'} )
        btn_modal_ok = cTag('button','确定', {'class':'btn', 'data-dismiss':'modal','onclick':'%s_OutPut();'%self.name , 'aria-hidden':'true'})
        btn_modal_close = cTag('button','关闭', {'class':'btn', 'data-dismiss':'modal', 'aria-hidden':'true'})
        div_modal_footer.add( btn_modal_ok.getHTML() )
        div_modal_footer.add( btn_modal_close.getHTML() )
        div_modal.add( div_modal_footer.getHTML() )
        
        aValue = self.Html.input('','aValue','hidden',{'id':'%s_aValue'%self.name})
        #最后整块处理
        html += div_modal.getHTML()+aValue
        return html + self.js()

    def top_btnbs_btnb(self):
        s='%s%s'%(self.top_btnbs,self.top_btnbs_script)
        
        return s
    
    def getUrlStr(self):
            return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])
    
    def search_html(self):
        div_modal_search = cTag('div','',{"class":"modal-header"})
        key_search = self.Html.input('','%s_keyword'%self.name,'text',{'id':'%s_keyword'%self.name,'class':'form-control span3','placeholder':'请输入关键字'})
        btnb_search = cTag('input','',{"value":"搜索",
                                      "type":"button",
                                      "class":"btn",
                                      "onclick":"var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};"%(self.name,self.name)})
        div_modal_search.add( key_search)
        div_modal_search.add( btnb_search.getHTML() )
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btnbs_btnb())
        #self.searchUrl = '+"&keyword="+keyword+"&matSele="+matSele'
        self.searchUrl= self.__searchUrl+'+"&keyword="+keyword'
        return div_modal_search.getHTML()
    
    def js(self):
        s="""<script>    
                $(function(){
                    $("#%(name)s_keyword").keydown(function(event){
                        if (event.keyCode == 13){
                            event.preventDefault();
                            %(name)s_loadUsersList($('#%(name)s_keyword').val());
                        }
                    });
                });
                function %(name)s_loadUsersList(keyword,matSele){
                    matSele=arguments[1]?arguments[1]:'';
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';

                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        tr += "<td><input type='checkbox' value='"+data.value[i]+"' data_id='"+data.list[i][0]+"' name='%(name)s_sel' onclick='%(name)s_change(this)'></td>"
                        for(j=1;j<data.list[i].length;j++){
                            tr += '<td>'+data.list[i][j]+'</td>';      /*ID*/
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);
                    %(recordseljs)s
                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel_old(objMe,aValue,i){
                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    //tbody.find('tr').removeClass('lsTRSel');
                                        
                    if ($(thisTr.find('input[type=checkbox]')[0]).prop('checked')==true){
                        $(thisTr.find('input[type=checkbox]')[0]).prop('checked',false);
                        thisTr.removeClass('lsTRSel');
                        thisTr.addClass('lsTR0');                        
                    }else{
                        $(thisTr.find('input[type=checkbox]')[0]).prop('checked',true);
                        thisTr.addClass('lsTRSel');
                    }
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }
                
                function %(name)s_change(obj){
                    thisTr=$(obj).parent().parent();
                    if ($(obj).prop('checked')==true){
                        thisTr.addClass('lsTRSel');
                    }else{
                        thisTr.removeClass('lsTRSel');
                        thisTr.addClass('lsTR0');
                    }
                    $("#%(name)s_aValue").val(aValue);
                }
                
                
                function %(name)s_selAll(obj){                                        
                    $('input[name=%(name)s_sel]').each(function(){
                        thisTr=$(this).parent().parent();
                        if ($(obj).prop('checked')==true){
                            $(this).prop('checked',true);
                            thisTr.addClass('lsTRSel');
                        }else{
                            $(this).prop('checked',false);
                            thisTr.removeClass('lsTRSel');
                            thisTr.addClass('lsTR0');
                        }
                    });
                } 
                
                
                function %(name)s_OutPut(obj){
                    
                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtnb:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

                 
            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}     
            .table th,td{white-space: nowrap;}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}  
            </style>
        """%{'sUrl':self.sUrl,'name':self.name,'ojs':self.confirmjs,'cjs':self.clearjs,'searchUrl':self.searchUrl,'recordseljs':self.record_sel_js}
        return s
    
    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''                
        self.record_sel_js = ''

class mselect_forList1(mselect_forList):
    def js(self):
        s="""<script>

                function %(name)s_loadUsersList(keyword,matSele){
                    matSele=arguments[1]?arguments[1]:'';
              
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';

                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        
                            tr += '<td>'+data.list[i][0]+'</td>';      
                            tr += '<td>'+data.list[i][2]+'</td>';  
                            tr += '<td>'+data.list[i][3]+'至'+data.list[i][4]+'</td>';      
                            
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){
                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){
                    
                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtnb:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

                 
            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}     
            .table th,td{white-space: nowrap;}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}  
            </style>
        """%{'sUrl':self.sUrl,'name':self.name,'ojs':self.confirmjs,'cjs':self.clearjs,'searchUrl':self.searchUrl}
        return s



class mselect_forYK:
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                 search_holder='请输入项目名称', btn='选择商品'):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.btn = btn
        self.cln_btn = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_clearPutOut()">清除</button>''' % self.name
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl

            # self.dnl 查询语句需要返回的字段索引

    def getHTML(self):
        return self.selusers() + self.cln_btn

    def selusers(self):

        html = ''
        # 触发按钮
        btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList('')">%s</button>''' % (
        self.name, self.btn)
        html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;margin-left:-%spx;left:50%%;' % (
            self.wh[0], self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name, "style": "font-size:20px;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())
        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框

        div_modal.add(self.search_html())

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;" % self.wh[1]})
        ####
        div_modal_body_s = cTag('div', '', {'class': 'modal-body',
                                            "style": "height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;" % (
                                            self.wh[1])})

        ##########
        table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add(cTag('th', n).getHTML())
        thead.add(tr.getHTML())
        table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

        # tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody', '', {'class': 'table table-hover'})
        table_users.add(tbody.getHTML())
        # div_modal_body.add( table_users.getHTML() )
        ############
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        ############
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = '%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header"})
        o = [['', '--经费性质--'],
             ['1', '行政经费'],
             ['2', '专项基金'],
             ['3', '科研基金'],
             ['4', '其他(自筹)']
             ]

        yk_type = self.Html.select(o, 'yk_type', '',
                                   {'onchange': "%s_jf(this.value)" % (self.name)
                                       , 'class': 'span1 inputed', 'style': 'width:115px;height:32px;margin-left:5px;'})

        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'col-sm-3 span1',
                                      'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})

        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                        self.name, self.name)})
        if self.showSearch == 1:
            #div_modal_search.add(yk_type)
            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword'
        return div_modal_search.getHTML()

    def js(self):
        s = """<script>

                function %(name)s_loadUsersList(keyword){
                    a= $('select[name=money_source]').val();
                    if(a){
                        $('select[name=yk_type]').val(a);
                    }
                    if (a==undefined){
                        a='';
                    }
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }
                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){

                            tr += '<td >'+data.list[i][dnl[j]]+'</td>';   //原来的方式，不用区分对齐
                            //
                            //if(j%%2==0){
                            //    tr += '<td style="text-align:left;">'+data.list[i][dnl[j]]+'</td>';      /*ID因为td要按不同方式对齐，所以要这样处理*/
                           // }else{
                            //    tr += '<td style="text-align:right;">'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            //}
                            //
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/

                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }
                function %(name)s_jf(jf){
                    var keyd=document.getElementById('%(name)s_keyword').value
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"+"&keyword="+keyd,
                        dataType:"json",
                        success:%(name)s_loadUsers_success2,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }


                /*这个是成功访问服务之后返回的处理2*/
                function %(name)s_loadUsers_success2(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){

                            tr += '<td >'+data.list[i][dnl[j]]+'</td>';   //原来的方式，不用区分对齐
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    a= $('select[name=yk_type]').val();
                    b= $('select[name=money_source]').val();
                    if(a!=b){
                        $('select[name=money_source]').val(a);
                    }
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){

                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){

                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
            </style>
        """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs, 'cjs': self.clearjs,
               'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s

    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''


class mselect_forGoods_Info:
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                 search_holder='请输入项目名称'):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btn = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_clearPutOut()">清除</button>''' % self.name
        self.btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList('')">选择商品</button>''' % self.name
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl

            # self.dnl 查询语句需要返回的字段索引

    def getHTML(self):
        return self.selusers() + self.cln_btn

    def selusers(self):

        html = ''
        # 触发按钮
        #btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList('')">选择商品</button>''' % self.name
        html += self.btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;height:%spx;margin-left:-%spx;left:50%%;top:20px;' % (
                self.wh[0],self.wh[1]+205 ,self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header",'style':'padding:5px;'})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name, "style": "font-size:20px;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())
        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框

        div_modal.add(self.search_html())

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;padding: 2px 3px 30px 3px;" % self.wh[1]})
        ####
        div_modal_body_s = cTag('div', '', {'class': 'modal-body',
                                            "style": "height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;padding:initial;" % (
                                                self.wh[1])})

        ##########
        table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add(cTag('th', n).getHTML())
        thead.add(tr.getHTML())
        table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

        # tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody', '', {'class': 'table table-hover'})
        table_users.add(tbody.getHTML())
        # div_modal_body.add( table_users.getHTML() )
        ############
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        ############
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = '%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header",'style':'padding:5px;'})
        o = [['', '--经费性质--'],
             ['1', '行政经费'],
             ['2', '专项基金'],
             ['3', '科研基金'],
             ['4', '其他(自筹)']
             ]

        yk_type = self.Html.select(o, 'yk_type', '',
                                   {'onchange': "%s_jf(this.value)" % (self.name)
                                       , 'class': 'span1 inputed', 'style': 'width:115px;height:32px;margin-left:5px;'})

        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'col-sm-3 span1',
                                      'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})

        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                            self.name, self.name)})
        if self.showSearch == 1:
            # div_modal_search.add(yk_type)
            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword'
        return div_modal_search.getHTML()

    def js(self):
        s = """<script>

                function %(name)s_loadUsersList(keyword){
                    a= $('select[name=money_source]').val();
                    if(a){
                        $('select[name=yk_type]').val(a);
                    }
                    if (a==undefined){
                        a='';
                    }
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }
                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)
                    
                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){

                            tr += '<td >'+data.list[i][dnl[j]]+'</td>';   //原来的方式，不用区分对齐
                            //
                            //if(j%%2==0){
                            //    tr += '<td style="text-align:left;">'+data.list[i][dnl[j]]+'</td>';      /*ID因为td要按不同方式对齐，所以要这样处理*/
                           // }else{
                            //    tr += '<td style="text-align:right;">'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            //}
                            //
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/

                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }
                function %(name)s_jf(jf){
                    var keyd=document.getElementById('%(name)s_keyword').value
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"+"&keyword="+keyd,
                        dataType:"json",
                        success:%(name)s_loadUsers_success2,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }


                /*这个是成功访问服务之后返回的处理2*/
                function %(name)s_loadUsers_success2(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){

                            tr += '<td >'+data.list[i][dnl[j]]+'</td>';   //原来的方式，不用区分对齐
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    a= $('select[name=yk_type]').val();
                    b= $('select[name=money_source]').val();
                    if(a!=b){
                        $('select[name=money_source]').val(a);
                    }
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){

                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){

                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
            </style>
        """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs, 'cjs': self.clearjs,
               'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s

    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''


class mselect_forGoods_Infos:
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                 search_holder='请输入项目名称'):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.Html = CHtml()
        self.cln_btn = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_clearPutOut()">清除</button>''' % self.name
        self.btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList()">选择商品</button>''' % self.name
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl

            # self.dnl 查询语句需要返回的字段索引

    def getHTML(self):
        return self.selusers()  # + self.cln_btn

    def selusers(self):

        html = ''
        # 触发按钮
        # btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList('')">选择商品</button>''' % self.name
        # html += self.btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;height:%spx;margin-left:-%spx;left:50%%;top:20px;' % (
                self.wh[0], self.wh[1] + 205, self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header", 'style': 'padding:5px;'})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name, "style": "font-size:20px;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())
        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框

        div_modal.add(self.search_html())

        # 模态框的body
        div_modal_body = cTag('div', '',
                              {'class': 'modal-body', "style": "height:%spx;padding: 2px 3px 30px 3px;" % self.wh[1]})
        ####
        div_modal_body_s = cTag('div', '', {'class': 'modal-body',
                                            "style": "height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;padding:initial;" % (
                                                self.wh[1])})

        ##########
        table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add(cTag('th', n).getHTML())
        thead.add(tr.getHTML())
        table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

        # tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody', '', {'class': 'table table-hover'})
        table_users.add(tbody.getHTML())
        # div_modal_body.add( table_users.getHTML() )
        ############
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        ############
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = '%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header", 'style': 'padding:5px;'})
        o = [['', '--经费性质--'],
             ['1', '行政经费'],
             ['2', '专项基金'],
             ['3', '科研基金'],
             ['4', '其他(自筹)']
             ]

        yk_type = self.Html.select(o, 'yk_type', '',
                                   {'onchange': "%s_jf(this.value)" % (self.name)
                                       , 'class': 'span1 inputed', 'style': 'width:115px;height:32px;margin-left:5px;'})

        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'col-sm-3 span1',
                                      'style': 'padding:4px 6px;margin:5px;', 'placeholder': self.search_holder})

        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                            self.name, self.name)})
        if self.showSearch == 1:
            # div_modal_search.add(yk_type)
            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&nbsp;&nbsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword'
        return div_modal_search.getHTML()

    def js(self):
        s = """<script>

                function %(name)s_loadUsersList(keyword){
                    
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }
                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){

                            tr += '<td >'+data.list[i][dnl[j]]+'</td>';   //原来的方式，不用区分对齐
                            //
                            //if(j%%2==0){
                            //    tr += '<td style="text-align:left;">'+data.list[i][dnl[j]]+'</td>';      /*ID因为td要按不同方式对齐，所以要这样处理*/
                           // }else{
                            //    tr += '<td style="text-align:right;">'+data.list[i][dnl[j]]+'</td>';      /*ID*/
                            //}
                            //
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/

                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }
                function %(name)s_jf(jf){
                    var keyd=document.getElementById('%(name)s_keyword').value
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"+"&keyword="+keyd,
                        dataType:"json",
                        success:%(name)s_loadUsers_success2,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
                }


                /*这个是成功访问服务之后返回的处理2*/
                function %(name)s_loadUsers_success2(data){
                    //data=$.parseJSON(data)

                    var listLen = data.list.length;     /*列表的长度*/
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    var i = 0;
                    var tr_total = '';
                    var listlen = %(nllen)s;
                    var dnl=%(dnl)s;
                    for(i=0;i<listLen;i++){
                        if(i%%2==0){
                            tr = '<tr class="lsTR0" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }else{
                            tr = '<tr class="lsTR1" onclick="%(name)s_rowSel(this,\\\''+data.value[i]+'\\\','+i+')">';
                        }
                        for(j=0;j<listlen;j++){

                            tr += '<td >'+data.list[i][dnl[j]]+'</td>';   //原来的方式，不用区分对齐
                        }
                        tr += '</tr>';
                        tr_total += tr;
                    }
                    tbody.html(tr_total);

                    /*然后显示模态框*/
                    a= $('select[name=yk_type]').val();
                    b= $('select[name=money_source]').val();
                    if(a!=b){
                        $('select[name=money_source]').val(a);
                    }
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    $('#%(name)s_Modal').modal('show');
                    $("#%(name)s_aValue").val('');
                }

                function %(name)s_rowSel(objMe,aValue,i){

                    thisTr = $(objMe);
                    var tbody = $("#table_%(name)s_List").find('tbody');
                    tbody.find('tr').removeClass('lsTRSel');
                    thisTr.addClass('lsTRSel');
                    tbody.find('tr').not(thisTr).addClass('lsTR0');
                    $("#%(name)s_aValue").val(aValue);
                }

                function %(name)s_OutPut(obj){

                    sData=$("#%(name)s_aValue").val();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(sData){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC;color:#fff;}
            </style>
        """ % {'sUrl': self.sUrl, 'name': self.name, 'nllen': len(self.nl), 'ojs': self.confirmjs, 'cjs': self.clearjs,
               'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s

    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''


# list 专用 mselect
class mselect_forMList:
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', viewid='mselect', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                 search_holder='请输入商品名称', canjp=1):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.viewid = viewid
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.thisUrl = ''
        self.Html = CHtml()
        self.canjp = canjp  # 是否显示进价 0 不显示 1显示默认
        self.cln_btn = ''
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl
        # self.dnl 查询语句需要返回的字段索引

    def getHTML(self):
        return self.selusers() + self.cln_btn

    def selusers(self):

        html = ''
        #触发按钮
        btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList('')">选择商品</button>''' % self.name
        html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;height:%spx;margin-left:-%spx;left:50%%;top: 20px;' % (
            self.wh[0], self.wh[1]+105,self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header", "style": "height:22px;padding:3px;"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name, "style": "color:#000;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())

        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框
        div_modal.add(self.search_html())
        #

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "padding:3px;height:%spx;" % self.wh[1]})
        fiw = '165px'

        table_tree = '''<div style="float:left;width:''' + fiw + '''">
                <div>
                    <!-- 左侧菜单栏 -->
                    ''' + self.js_tree() + '''
                </div>
            </div>'''

        table_grid = ''' <!-- 右侧主体 -->
            <div style="float:left;width:720px">
                    <div id="global_show_grid" style="width:720px"></div>
                    <div style="display:none;"></div>
            </div> '''

        div_modal_body.add(table_tree)
        div_modal_body.add(table_grid)
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer', 'style': 'padding:3px;height:25px;'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'onclick': 'f_clearChecked();',
                                                'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = self.Html.checkbox(['0', '显示停销商品', ""], 'show_ts', {'class': '',
                                                                'onchange': "var keyd=document.getElementById('%s_keyword');%s_loadUsersList(keyd.value);" % (
                                                                self.name, self.name), "style": ""})
        self.top_btns += cTag('div', s, {'style': 'float:right;'}).getHTML()
        s = ''#'%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header", "style": "height:25px;padding:1px 80px; "})
        o = [
            ['1', '分类方式'],
            ['2', '货商方式']
        ]
        tree_type = self.Html.select(o, 'tree_type', '1',
                                     {'onchange': "$('input[name=tree_type]').val(this.value);sreloadtree();",
                                      'class': 'span1 inputed', 'style': 'width:115px;margin-left:5px;'})

        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'inputed span3',
                                      'style': 'padding:0px;margin:5px;', 'placeholder': self.search_holder,
                                      "onkeyup": "if(window.event.keyCode == 13){var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')}};" % (
                                      self.name, self.name)})
        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn inputed",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                        self.name, self.name)})

        btn_checkbox = '&emsp;&emsp;&emsp;&emsp;&emsp;全选：<input type="checkbox" onclick="f_CheckAllRows(this);" class="inputed" />'
        if self.showSearch == 1:
            #div_modal_search.add(tree_type)
            div_modal_search.add(btn_checkbox)
            div_modal_search.add('&emsp;&emsp;')
            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&emsp;&emsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword+"&tree_pk="+tree_pk'
        return div_modal_search.getHTML()

    def js(self):
        s = """<script>
                var itemdata = {};
                function %(name)s_loadUsersList(keyword,tree_pk,scode,tree_type,mselect_kc,hscode){
                    tree_pk=arguments[1]?arguments[1]:'';
                    scode =arguments[2]?arguments[2]:'';
                    tree_type =arguments[3]?arguments[3]:'';
                    mselect_kc =arguments[4]?arguments[4]:'';
                    hscode =arguments[5]?arguments[5]:'';
                    $('#pageloading').show();
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            $('#pageloading').hide();
                            alert('异步请求异常请联系管理员');
                        }
                    });

                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    if($('#%(name)s_Modal').css('display') != 'block'){
                        $('#%(name)s_Modal').modal('show');
                    }
                        itemdata = {Rows:data[0],Total:data[1]};
                        f_grid();
                        $("#%(name)s_aValue").val('');
                        $('#pageloading').hide();

                }

                function %(name)s_OutPut(obj){
                    sData=f_getChecked();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(res){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC}                
            </style>
        """ % {'sUrl': self.sUrl, 'thisUrl': self.thisUrl, 'name': self.name, 'nllen': len(self.nl),
               'ojs': self.confirmjs, 'cjs': self.clearjs, 'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s

    def js_tree(self):

        s = """
            <div style="width:165px; height:390px; margin-left:2px;margin-top:0px; float:left; border:1px solid #ccc; overflow:auto;  ">
               <input type="hidden" name="tree_pk" value="-1">
                <ul id="stree"></ul>
            </div> 
            <div style="display:none">
            </div>
            <script type="text/javascript">
             var stree = null;
             var sgrid = null;
             streemenu();
             function streemenu() {  
                    var tree_pk = $('input[name=tree_pk]').val(); 
                    if(tree_pk == undefined){
                        tree_pk = '-1'
                    }
                    urls = "admin?viewid=%(viewid)s&part=ajax&action=getTree&tree_pk="+tree_pk;
                    $.ajax({
                        type: "get",
                        async:false,
                        url: urls,
                        dataType:"json",
                        data:{
                            tree_type:$('select[name=tree_type]').val()
                        },
                        success:screatetree,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
             }

             function screatetree(data){
                var listLen = data.length;     /*列表的长度*/
                var i = 0;                    
                var tNodes=[];
                
                for(i=0;i<listLen;i++){
                    t={id:data[i][0],pid:data[i][1], text:data[i][2],ilevel:data[i][3],isselected:data[i][4]}
                    tNodes.push(t);
                    } 
                 stree = $("#stree").ligerTree({
                 nodeWidth:155,
                 data:tNodes,
                 idFieldName: 'id', 
                 parentIDFieldName: 'pid',
                 textFieldName:'text',
                 checkbox:false,
                 slide:false,
                 onSelect:SelectNode,
               });

               treeMan = $('#stree').ligerGetTreeManager();
               treeMan.collapseAll();
              }

            function SelectNode(note){
                var id = note.data.id;
                var tree_type = $('select[name=tree_type]').val();
                $('input[name=tree_pk]').val(id); 
                var keyword = $('input[name=%(name)s_keyword]').val();
                %(name)s_loadUsersList(keyword,id,'',tree_type,'');
                return true;
            }

            function sreloadtree(){
              streemenu();
            }

            function tolocalfrm(){
              window.location.reload();
            }


         function f_onCheckAllRow(checked){
             for (var rowid in this.records)
             { 
                 if(checked){
                     addcheckedItem(this.records[rowid]['id']);
                 }
                 else{
                     removecheckedItem(this.records[rowid]['id']);
                 }
             }
         }

         //实现分页记忆
         var checkedItem = [];
         function findcheckedItem(id)
         {    for(var i =0;i<checkedItem.length;i++)
             {
                 if(checkedItem[i] == id) return i;
             }
             return -1;
         }

         function addcheckedItem(id)
         {
             if(findcheckedItem(id) == -1)
                 checkedItem.push(id);
         }

         function removecheckedItem(id)
         {
             var i = findcheckedItem(id);
             if (i == -1) return ;
             checkedItem.splice(i,1);
         }
         function f_isChecked(rowdata)
         {    if (findcheckedItem(rowdata.id) == -1){
                 return false;
             }
             return true;
         }

         function f_onCheckRow(checked,data)
         {    if(checked){ 
                 addcheckedItem(data.id);
                 }
              else{
                  removecheckedItem(data.id);
              }
         }

         function f_IscheckAll(){
            var call = 0;
            for (var rowid in this.records)
             { 
                if ( checkedItem.indexOf(this.records[rowid]['id']) >=0 ){
                      call = 1;
                }
                else{
                     call = 0;
                     break;
                }
             }
            if (call == 1){
                $('#global_show_grid').find('.l-grid1').find('.l-grid-hd-row').addClass('l-checked');
            }
            else{
                $('#global_show_grid').find('.l-grid1').find('.l-grid-hd-row').removeClass('l-checked');
            }
         }

          function f_CheckAllRows(obj)
         {    var alldata = itemdata.Rows;
             if (obj.checked){
                 for (var i = 0; i< alldata.length;i++)
                     { 
                        addcheckedItem(alldata[i].id);
                     }
                 }
              else{
                for (var i = 0; i< alldata.length;i++)
                     { 
                        removecheckedItem(alldata[i].id);
                     }
              }
              f_grid();
         }

         function f_getChecked(){
             return checkedItem.join(',');
         }

         function f_clearChecked(){
             checkedItem = [];
         }

         function f_grid(){
                var rp =10
                var rp1 = $("#global_show_grid").find('select[name=rp]').val();
                if (rp1 != undefined){
                    rp = rp1
                }
                sgrid =  $("#global_show_grid").ligerGrid({
                checkbox:true,
                columns:[
                {display:'编号',name:'id',align:'left',width:92,type:'int'},
                {display:'名称',name:'name',align:'left',width:120,type:'string'},
                {display:'原价',name:'originalprice',align:'left',width:155,type:'float'},
                {display:'现价',name:'minprice',align:'left',width:50,type:'float'},
                {display:'库存',name:'stores',align:'left',width:30,type:'int'},
                {display:'限购',name:'limited',align:'right',width:55,type:'int'},
                
                ],
                page:1,
                dataAction:'server',
                usePager:true,
                pageSize:rp,
                data:itemdata,
                isScroll:true,
                width:'650',
                height:'385',
                isChecked:f_isChecked,
                onCheckRow:f_onCheckRow,
                onCheckAllRow:f_onCheckAllRow,
                allowUnSelectRow:true,
                onAfterShowData:f_IscheckAll
                }
            );
               /* if ('%(jjxs)s' != 1){
                   sgrid.toggleCol('jj_price', false);
               }*/
               
            }
            </script>
        """ % ({'viewid': self.viewid, 'name': self.name, 'jjxs': self.canjp})
        return s

    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''


# list 专用 mselect
class mselect_forMList_mul:
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', viewid='mselect', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                 search_holder='请输入商品名称', canjp=1):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.viewid = viewid
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.thisUrl = ''
        self.Html = CHtml()
        self.canjp = canjp  # 是否显示进价 0 不显示 1显示默认
        self.cln_btn = ''
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl
        # self.dnl 查询语句需要返回的字段索引

    def getHTML(self):
        return self.selusers() + self.cln_btn

    def selusers(self):

        html = ''
        # 触发按钮
        btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList('')">选择商品</button>''' % self.name
        html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;height:%spx;margin-left:-%spx;left:50%%;top: 20px;' % (
                self.wh[0], self.wh[1] + 105, self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header", "style": "height:22px;padding:3px;"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name, "style": "color:#000;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())

        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框
        div_modal.add(self.search_html())
        #

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "padding:3px;height:%spx;" % self.wh[1]})
        fiw = '165px'

        table_tree = '''<div style="float:left;width:''' + fiw + '''">
                <div>
                    <!-- 左侧菜单栏 -->
                    ''' + self.js_tree() + '''
                </div>
            </div>'''

        table_grid = ''' <!-- 右侧主体 -->
            <div style="float:left;width:720px">
                    <div id="global_show_grid%(name)s" style="width:720px"></div>
                    <div style="display:none;"></div>
            </div> ''' % {'name': self.name}

        div_modal_body.add(table_tree)
        div_modal_body.add(table_grid)
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer', 'style': 'padding:3px;height:25px;'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭',
                               {'class': 'btn', 'data-dismiss': 'modal', 'onclick': 'f_clearChecked%s();' % self.name,
                                                'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = self.Html.checkbox(['0', '显示停销商品', ""], 'show_ts', {'class': '',
                                                                'onchange': "var keyd=document.getElementById('%s_keyword');%s_loadUsersList(keyd.value);" % (
                                                                    self.name, self.name), "style": ""})
        self.top_btns += cTag('div', s, {'style': 'float:right;'}).getHTML()
        s = ''  # '%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header", "style": "height:25px;padding:1px 80px; "})
        o = [
            ['1', '分类方式'],
            ['2', '货商方式']
        ]
        tree_type = self.Html.select(o, 'tree_type', '1',
                                     {'onchange': "$('input[name=tree_type]').val(this.value);sreloadtree();",
                                      'class': 'span1 inputed', 'style': 'width:115px;margin-left:5px;'})

        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'inputed span3',
                                      'style': 'padding:0px;margin:5px;', 'placeholder': self.search_holder,
                                      "onkeyup": "if(window.event.keyCode == 13){var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')}};" % (
                                          self.name, self.name)})
        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn inputed",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                            self.name, self.name)})

        btn_checkbox = '&emsp;&emsp;&emsp;&emsp;&emsp;全选：<input type="checkbox" onclick="f_CheckAllRows(this);" class="inputed" />'
        if self.showSearch == 1:
            # div_modal_search.add(tree_type)
            div_modal_search.add(btn_checkbox)
            div_modal_search.add('&emsp;&emsp;')
            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
        div_modal_search.add('&emsp;&emsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword+"&tree_pk="+tree_pk'
        return div_modal_search.getHTML()

    def js(self):
        s = """<script>
                var itemdata = {};
                function %(name)s_loadUsersList(keyword,tree_pk,scode,tree_type,mselect_kc,hscode){
                    tree_pk=arguments[1]?arguments[1]:'';
                    scode =arguments[2]?arguments[2]:'';
                    tree_type =arguments[3]?arguments[3]:'';
                    mselect_kc =arguments[4]?arguments[4]:'';
                    hscode =arguments[5]?arguments[5]:'';
                    $('#pageloading').show();
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            $('#pageloading').hide();
                            alert('异步请求异常请联系管理员');
                        }
                    });

                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    if($('#%(name)s_Modal').css('display') != 'block'){
                        $('#%(name)s_Modal').modal('show');
                    }
                        itemdata = {Rows:data[0],Total:data[1]};
                        f_grid%(name)s();
                        $("#%(name)s_aValue").val('');
                        $('#pageloading').hide();

                }

                function %(name)s_OutPut(obj){
                    sData=f_getChecked%(name)s();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(res){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC}                
            </style>
        """ % {'sUrl': self.sUrl, 'thisUrl': self.thisUrl, 'name': self.name, 'nllen': len(self.nl),
               'ojs': self.confirmjs, 'cjs': self.clearjs, 'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s

    def js_tree(self):

        s = """
            <div style="width:165px; height:390px; margin-left:2px;margin-top:0px; float:left; border:1px solid #ccc; overflow:auto;  ">
               <input type="hidden" name="tree_pk" value="-1">
                <ul id="stree%(name)s"></ul>
            </div> 
            <div style="display:none">
            </div>
            <script type="text/javascript">
             var stree = null;
             var sgrid = null;
             streemenu();
             function streemenu() {  
                    var tree_pk = $('input[name=tree_pk]').val(); 
                    if(tree_pk == undefined){
                        tree_pk = '-1'
                    }
                    urls = "admin?viewid=%(viewid)s&part=ajax&action=getTree&tree_pk="+tree_pk;
                    $.ajax({
                        type: "get",
                        async:false,
                        url: urls,
                        dataType:"json",
                        data:{
                            tree_type:$('select[name=tree_type]').val()
                        },
                        success:screatetree,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
             }

             function screatetree(data){
                var listLen = data.length;     /*列表的长度*/
                var i = 0;                    
                var tNodes=[];

                for(i=0;i<listLen;i++){
                    t={id:data[i][0],pid:data[i][1], text:data[i][2],ilevel:data[i][3],isselected:data[i][4]}
                    tNodes.push(t);
                    } 
                 stree = $("#stree%(name)s").ligerTree({
                 nodeWidth:155,
                 data:tNodes,
                 idFieldName: 'id', 
                 parentIDFieldName: 'pid',
                 textFieldName:'text',
                 checkbox:false,
                 slide:false,
                 onSelect:SelectNode,
               });

               treeMan = $('#stree%(name)s').ligerGetTreeManager();
               treeMan.collapseAll();
              }

            function SelectNode(note){
                var id = note.data.id;
                var tree_type = $('select[name=tree_type]').val();
                $('input[name=tree_pk]').val(id); 
                var keyword = $('input[name=%(name)s_keyword]').val();
                %(name)s_loadUsersList(keyword,id,'',tree_type,'');
                return true;
            }

            function sreloadtree(){
              streemenu();
            }

            function tolocalfrm(){
              window.location.reload();
            }


         function f_onCheckAllRow%(name)s(checked){
             for (var rowid in this.records)
             { 
                 if(checked){
                     addcheckedItem%(name)s(this.records[rowid]['id']);
                 }
                 else{
                     removecheckedItem%(name)s(this.records[rowid]['id']);
                 }
             }
         }

         //实现分页记忆
         var checkedItem%(name)s = [];
         function findcheckedItem%(name)s(id)
         {    for(var i =0;i<checkedItem%(name)s.length;i++)
             {
                 if(checkedItem%(name)s[i] == id) return i;
             }
             return -1;
         }

         function addcheckedItem%(name)s(id)
         {
             if(findcheckedItem%(name)s(id) == -1)
                 checkedItem%(name)s.push(id);
         }

         function removecheckedItem%(name)s(id)
         {
             var i = findcheckedItem%(name)s(id);
             if (i == -1) return ;
             checkedItem%(name)s.splice(i,1);
         }
         function f_isChecked%(name)s(rowdata)
         {    if (findcheckedItem%(name)s(rowdata.id) == -1){
                 return false;
             }
             return true;
         }

         function f_onCheckRow%(name)s(checked,data)
         {    if(checked){ 
                 addcheckedItem%(name)s(data.id);
                 }
              else{
                  removecheckedItem%(name)s(data.id);
              }
         }

         function f_IscheckAll%(name)s(){
            var call = 0;
            for (var rowid in this.records)
             { 
                if ( checkedItem%(name)s.indexOf(this.records[rowid]['id']) >=0 ){
                      call = 1;
                }
                else{
                     call = 0;
                     break;
                }
             }
            if (call == 1){
                $('#global_show_grid%(name)s').find('.l-grid1').find('.l-grid-hd-row').addClass('l-checked');
            }
            else{
                $('#global_show_grid%(name)s').find('.l-grid1').find('.l-grid-hd-row').removeClass('l-checked');
            }
         }

          function f_CheckAllRows%(name)s(obj)
         {    var alldata = itemdata.Rows;
             if (obj.checked){
                 for (var i = 0; i< alldata.length;i++)
                     { 
                        addcheckedItem%(name)s(alldata[i].id);
                     }
                 }
              else{
                for (var i = 0; i< alldata.length;i++)
                     { 
                        removecheckedItem%(name)s(alldata[i].id);
                     }
              }
              f_grid%(name)s();
         }

         function f_getChecked%(name)s(){
             return checkedItem%(name)s.join(',');
         }

         function f_clearChecked%(name)s(){
             checkedItem%(name)s = [];
         }

         function f_grid%(name)s(){
                var rp =10
                var rp1 = $("#global_show_grid%(name)s").find('select[name=rp]').val();
                if (rp1 != undefined){
                    rp = rp1
                }
                sgrid =  $("#global_show_grid%(name)s").ligerGrid({
                checkbox:true,
                columns:[
                {display:'编号',name:'id',align:'left',width:92,type:'int'},
                {display:'名称',name:'name',align:'left',width:120,type:'string'},
                {display:'原价',name:'originalprice',align:'left',width:155,type:'float'},
                {display:'现价',name:'minprice',align:'left',width:50,type:'float'},
                {display:'库存',name:'stores',align:'left',width:30,type:'int'},
                {display:'限购',name:'limited',align:'right',width:55,type:'int'},

                ],
                page:1,
                dataAction:'server',
                usePager:true,
                pageSize:rp,
                data:itemdata,
                isScroll:true,
                width:'650',
                height:'385',
                isChecked:f_isChecked%(name)s,
                onCheckRow:f_onCheckRow%(name)s,
                onCheckAllRow:f_onCheckAllRow%(name)s,
                allowUnSelectRow:true,
                onAfterShowData:f_IscheckAll%(name)s
                }
            );
               /* if ('%(jjxs)s' != 1){
                   sgrid.toggleCol('jj_price', false);
               }*/

            }
            </script>
        """ % ({'viewid': self.viewid, 'name': self.name, 'jjxs': self.canjp})
        return s

    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''


# list 专用 mselect
class mselect_forMList_spec:
    top_btns_script = ''  ##top_btns的JS
    top_btns = ''  ##按钮 | 筛选
    __searchUrl = ''

    def __init__(self, name='m', viewid='mselect', nl=[], title='选择数据', wh=[800, 0], can=[1, 1], showSearch=1, dnl=[],
                 search_holder='请输入规格名称', canjp=1):
        self.can_select = can[0]
        self.can_clear = can[1]
        self.nl = nl
        self.viewid = viewid
        self.showSearch = showSearch
        self.name = name
        self.title = title
        self.wh = wh
        self.sUrl = ''
        self.thisUrl = ''
        self.Html = CHtml()
        self.canjp = canjp  # 是否显示进价 0 不显示 1显示默认
        self.cln_btn = ''
        self.callback()
        self.search_holder = search_holder
        self.dnl = []
        if len(dnl) <= 0:
            for idd in range(len(self.nl)):
                self.dnl.append(idd)
        else:
            self.dnl = dnl
        # self.dnl 查询语句需要返回的字段索引

    def getHTML(self):
        return self.selusers() + self.cln_btn

    def selusers(self):

        html = ''
        # 触发按钮
        # btnb_role = '''&nbsp;<button class="btn btn-sm btn-info" type="button" onclick="%s_loadUsersList('')">选择商品</button>''' % self.name
        # html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;height:%spx;margin-left:-%spx;left:50%%;top: 20px;' % (
                self.wh[0], self.wh[1] + 105, self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header", "style": "height:22px;padding:3px;"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name, "style": "color:#000;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())

        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框
        div_modal.add(self.search_html())
        #

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "padding:3px;height:%spx;" % self.wh[1]})
        fiw = '205px'

        table_tree = '''<div style="float:left;width:''' + fiw + '''">
                <div>
                    <!-- 左侧菜单栏 -->
                    ''' + self.js_tree() + '''
                </div>
            </div>'''

        table_grid = ''' <!-- 右侧主体 -->
            <div style="float:left;width:675px">
                    <div id="global_show_grid%(name)s" style="width:675px"></div>
                    <div style="display:none;"></div>
            </div> ''' % {'name': self.name}

        div_modal_body.add(table_tree)
        div_modal_body.add(table_grid)
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer', 'style': 'padding:3px;height:25px;'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭',
                               {'class': 'btn', 'data-dismiss': 'modal', 'onclick': 'f_clearChecked%s();' % self.name,
                                'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()

    def top_btns_btn(self):
        s = self.Html.checkbox(['0', '显示停销商品', ""], 'show_ts', {'class': '',
                                                                'onchange': "var keyd=document.getElementById('%s_keyword');%s_loadUsersList(keyd.value);" % (
                                                                    self.name, self.name), "style": ""})
        self.top_btns += cTag('div', s, {'style': 'float:right;'}).getHTML()
        s = ''  # '%s%s' % (self.top_btns, self.top_btns_script)

        return s

    def getUrlStr(self):
        return self.__searchUrl

    def setUrlArg(self, dis={}):
        ##追加参数
        for e in dis.keys():
            self.__searchUrl += '+"&%s="+%s' % (e, dis[e])

    def search_html(self):
        div_modal_search = cTag('div', '', {"class": "modal-header", "style": "height:40px;padding:1px 80px; "})
        o = [
            ['1', '分类方式'],
            ['2', '货商方式']
        ]
        tree_type = self.Html.select(o, 'tree_type', '1',
                                     {'onchange': "$('input[name=tree_type]').val(this.value);sreloadtree();",
                                      'class': 'span1 inputed', 'style': 'width:115px;margin-left:5px;'})

        key_search = self.Html.input('', '%s_keyword' % self.name, 'text',
                                     {'id': '%s_keyword' % self.name, 'class': 'inputed span3',
                                      'style': 'padding:0px;margin:5px;', 'placeholder': self.search_holder,
                                      "onkeyup": "if(window.event.keyCode == 13){var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')}};" % (
                                          self.name, self.name)})
        btn_search = cTag('input', '', {"value": "搜索",
                                        "type": "button",
                                        'style': 'margin:5px;',
                                        "class": "btn inputed",
                                        "onclick": "var keyd=document.getElementById('%s_keyword');if(keyd.value!=''){%s_loadUsersList(keyd.value)}else{alert('请在[输入框]键入搜索内容，再按【搜索】键。')};" % (
                                            self.name, self.name)})

        btn_add_sc = '<button class="btn btn-primary" data-dismiss="modal" style="margin-left:150px;" onclick="add_spec_child();" aria-hidden="true">添加型号</button>'

        btn_checkbox = '&emsp;&emsp;&emsp;&emsp;&emsp;全选：<input type="checkbox" onclick="f_CheckAllRows(this);" class="inputed" />'
        if self.showSearch == 1:
            # div_modal_search.add(tree_type)
            # div_modal_search.add(btn_checkbox)
            div_modal_search.add('&emsp;&emsp;')
            div_modal_search.add(key_search)
            div_modal_search.add(btn_search.getHTML())
            div_modal_search.add(btn_add_sc)
        div_modal_search.add('&emsp;&emsp;')
        div_modal_search.add(self.top_btns_btn())
        self.__searchUrl += '+"&keyword="+keyword+"&tree_pk="+tree_pk+"&tree_id="+tree_id'
        return div_modal_search.getHTML()

    def js(self):
        s = """<script>
                var itemdata = {};
                function %(name)s_loadUsersList(keyword){
                    var tree_pk = $('input[name=tree_pk]').val(); 
                    var tree_id = $('input[name=tree_id]').val(); 
                    
                    $('#pageloading').show();
                    $.ajax({
                        type: "GET",
                        url: "%(sUrl)s"%(searchUrl)s,
                        dataType:"json",
                        success:%(name)s_loadUsers_success,
                        error:function(XMLHttpRequest,errorMsg){
                            $('#pageloading').hide();
                            alert('异步请求异常请联系管理员');
                        }
                    });

                }

                /*这个是成功访问服务之后返回的处理*/
                function %(name)s_loadUsers_success(data){
                    /*然后显示模态框*/
                    $('#%(name)s_Modal').modal({backdrop: 'static'});
                    if($('#%(name)s_Modal').css('display') != 'block'){
                        $('#%(name)s_Modal').modal('show');
                    }
                    
                    itemdata = {Rows:data[0],Total:data[1]};
                    f_grid%(name)s();
                    $("#%(name)s_aValue").val('');
                    $('#pageloading').hide();

                }

                function %(name)s_OutPut(obj){
                    sData=f_getChecked%(name)s();
                    %(name)s_setOutPut(sData);
                }
                function %(name)s_setOutPut(res){
                    %(ojs)s
                }
                function %(name)s_clearPutOut(){
                    %(cjs)s
                }    
            </script>
            <style>
            .form-horizontal .mylabel{display:inline-block;text-align:left;}
            .separ{margin-bottom:10px;margin-top:10px;}
            .mybadge{display:inline-block;margin-right:5px;}
            .mytextarea{width:300px;height:100px;}
            .form .mysubbtn:first-child{margin-left:212px;width:100px;}
            .myModalStyle{width:800px;left:40%%}

            .table-hover tbody tr:hover>td{BackGround-Color: #87CEFA}
            .lsTR0{CURSOR: hand; BackGround-Color: white}
            .lsTR1{CURSOR: hand; BackGround-Color: #D0D0D0}
            .lsTR2{CURSOR: hand; BackGround-Color: #F9C18A}
            .lsTRSel{CURSOR: hand; BackGround-Color: #3778EC}                
            </style>
        """ % {'sUrl': self.sUrl, 'thisUrl': self.thisUrl, 'name': self.name, 'nllen': len(self.nl),
               'ojs': self.confirmjs, 'cjs': self.clearjs, 'searchUrl': self.__searchUrl, 'dnl': self.dnl}
        return s

    def js_tree(self):

        s = """
            <div style="width:202px; height:390px; margin-left:2px;margin-top:0px; float:left; border:1px solid #ccc; overflow:auto;  ">
               <input type="hidden" name="tree_pk" value="0">
               <input type="hidden" name="tree_id" value="">
                <ul id="stree%(name)s"></ul>
            </div> 
            <div style="display:none">
            </div>
            <script type="text/javascript">
             var stree = null;
             var sgrid = null;
             //streemenu();
             function streemenu() {  
                    var tree_pk = $('input[name=tree_pk]').val(); 
                    if(tree_pk == undefined){
                        tree_pk = '0'
                    }
                    urls = "admin?viewid=%(viewid)s&part=ajax&action=getSpec_c&tree_pk="+tree_pk;
                    $.ajax({
                        type: "get",
                        async:false,
                        url: urls,
                        dataType:"json",
                        data:{
                            tree_type:$('select[name=tree_type]').val()
                        },
                        success:screatetree,
                        error:function(XMLHttpRequest,errorMsg){
                            alert('异步请求异常请联系管理员');
                        }
                    });
             }

             function screatetree(data){
                var listLen = data.length;     /*列表的长度*/
                var i = 0;                    
                var tNodes=[];

                for(i=0;i<listLen;i++){
                    t={id:data[i][0],pid:data[i][1], text:data[i][2],ilevel:data[i][3],isselected:data[i][4]}
                    tNodes.push(t);
                    } 
                 stree = $("#stree%(name)s").ligerTree({
                 nodeWidth:155,
                 data:tNodes,
                 idFieldName: 'id', 
                 parentIDFieldName: 'pid',
                 textFieldName:'text',
                 checkbox:false,
                 slide:false,
                 onSelect:SelectNode,
               });

               treeMan = $('#stree%(name)s').ligerGetTreeManager();
               treeMan.collapseAll();
              }

            function SelectNode(note){
                var id = note.data.id;
                var tree_type = $('select[name=tree_type]').val();
                $('input[name=tree_pk]').val(id); 
                var keyword = $('input[name=%(name)s_keyword]').val();
                %(name)s_loadUsersList(keyword,id,'',tree_type,'');
                return true;
            }

            function sreloadtree(){
              streemenu();
            }

            function tolocalfrm(){
              window.location.reload();
            }


         function f_onCheckAllRow%(name)s(checked){
             for (var rowid in this.records)
             { 
                 if(checked){
                     addcheckedItem%(name)s(this.records[rowid]['id']);
                 }
                 else{
                     removecheckedItem%(name)s(this.records[rowid]['id']);
                 }
             }
         }

         //实现分页记忆
         var checkedItem%(name)s = [];
         function findcheckedItem%(name)s(id)
         {    for(var i =0;i<checkedItem%(name)s.length;i++)
             {
                 if(checkedItem%(name)s[i] == id) return i;
             }
             return -1;
         }

         function addcheckedItem%(name)s(id)
         {
             if(findcheckedItem%(name)s(id) == -1)
                 checkedItem%(name)s.push(id);
         }

         function removecheckedItem%(name)s(id)
         {
             var i = findcheckedItem%(name)s(id);
             if (i == -1) return ;
             checkedItem%(name)s.splice(i,1);
         }
         function f_isChecked%(name)s(rowdata)
         {    if (findcheckedItem%(name)s(rowdata.id) == -1){
                 return false;
             }
             return true;
         }

         function f_onCheckRow%(name)s(checked,data)
         {    if(checked){ 
                 addcheckedItem%(name)s(data.id);
                 }
              else{
                  removecheckedItem%(name)s(data.id);
              }
         }

         function f_IscheckAll%(name)s(){
            var call = 0;
            for (var rowid in this.records)
             { 
                if ( checkedItem%(name)s.indexOf(this.records[rowid]['id']) >=0 ){
                      call = 1;
                }
                else{
                     call = 0;
                     break;
                }
             }
            if (call == 1){
                $('#global_show_grid%(name)s').find('.l-grid1').find('.l-grid-hd-row').addClass('l-checked');
            }
            else{
                $('#global_show_grid%(name)s').find('.l-grid1').find('.l-grid-hd-row').removeClass('l-checked');
            }
         }

          function f_CheckAllRows%(name)s(obj)
         {    var alldata = itemdata.Rows;
             if (obj.checked){
                 for (var i = 0; i< alldata.length;i++)
                     { 
                        addcheckedItem%(name)s(alldata[i].id);
                     }
                 }
              else{
                for (var i = 0; i< alldata.length;i++)
                     { 
                        removecheckedItem%(name)s(alldata[i].id);
                     }
              }
              f_grid%(name)s();
         }

         function f_getChecked%(name)s(){
             return checkedItem%(name)s.join(',');
         }

         function f_clearChecked%(name)s(){
             checkedItem%(name)s = [];
         }

         function f_grid%(name)s(){
                var rp =10
                var rp1 = $("#global_show_grid%(name)s").find('select[name=rp]').val();
                if (rp1 != undefined){
                    rp = rp1
                }
                sgrid =  $("#global_show_grid%(name)s").ligerGrid({
                checkbox:true,
                columns:[
                {display:'编号',name:'id',align:'left',width:92,type:'int'},
                {display:'名称',name:'cname_c',align:'left',width:372,type:'string'},
                {display:'类型',name:'ctype_c',align:'left',width:155,type:'string'},
                //{display:'现价',name:'minprice',align:'left',width:50,type:'float'},
                //{display:'库存',name:'stores',align:'left',width:30,type:'int'},
                //{display:'限购',name:'limited',align:'right',width:55,type:'int'},

                ],
                page:1,
                dataAction:'server',
                usePager:true,
                pageSize:rp,
                data:itemdata,
                isScroll:true,
                width:'650',
                height:'385',
                isChecked:f_isChecked%(name)s,
                onCheckRow:f_onCheckRow%(name)s,
                onCheckAllRow:f_onCheckAllRow%(name)s,
                allowUnSelectRow:true,
                onAfterShowData:f_IscheckAll%(name)s
                }
            );
               /* if ('%(jjxs)s' != 1){
                   sgrid.toggleCol('jj_price', false);
               }*/

            }
            </script>
        """ % ({'viewid': self.viewid, 'name': self.name, 'jjxs': self.canjp})
        return s

    def callback(self):
        self.confirmjs = '''
        alert(sData);
        '''
        self.clearjs = '''
        alert('clear');
        '''


# wjwcw项目关联合同
class mselect_forM(mselect_forList):

    def getHTML(self):
        return self.selusers()

    def selusers(self):

        html = ''
        # 触发按钮
        btnb_role = '''&nbsp;'''
        html += btnb_role

        # 模态框内容，最外层框
        div_modal = cTag('div', '', {"id": "%s_Modal" % self.name,
                                     "class": "modal fade myModalStyle",
                                     "tabindex": "-1",
                                     "role": "dialog",
                                     "aria-labelledby": "%s_ModalLabel" % self.name,
                                     "aria-hidden": "true"})
        if self.wh != []:
            div_modal.addAttr({'style': 'width:%spx;margin-left:-%spx;left:50%%;' % (
            self.wh[0], self.wh[0] != '' and float(self.wh[0]) / 2 or '')})

        # 模态框头部
        div_modal_head = cTag('div', '', {"class": "modal-header"})
        btn_head_close = cTag('button', '×', {"type": "button",
                                              "class": "close",
                                              "data-dismiss": "modal",
                                              "aria-hidden": "true"})
        txt_head_content = cTag('h3', self.title, {"id": "%s_ModalLabel" % self.name, "style": "font-size:20px;"})
        div_modal_head.add(btn_head_close.getHTML())
        div_modal_head.add(txt_head_content.getHTML())
        div_modal.add(div_modal_head.getHTML())

        # 模态框搜索框

        div_modal.add(self.search_html())

        # 模态框的body
        div_modal_body = cTag('div', '', {'class': 'modal-body', "style": "height:%spx;" % self.wh[1]})
        ####
        div_modal_body_s = cTag('div', '', {'class': 'modal-body',
                                            "style": "height:%spx; margin-left:10px;overflow-y:scroll; overflow-x:scroll;" % (
                                            self.wh[1])})

        ##########
        table_users = cTag('table', '', {'id': 'table_%s_List' % self.name, 'class': 'table table-hover'})
        thead = cTag('thead')
        tr = cTag('tr')
        for n in self.nl:
            tr.add(cTag('th', n).getHTML())
        thead.add(tr.getHTML())
        table_users.add(thead.getHTML())  # table 分开 thead 和 tbody 标签

        # tbody 的内容由js构造，确保能获取最新的权限情况
        tbody = cTag('tbody', '', {'class': 'table table-hover'})
        table_users.add(tbody.getHTML())
        # div_modal_body.add( table_users.getHTML() )
        ############
        div_modal_body_s.add(table_users.getHTML())
        div_modal_body.add(div_modal_body_s.getHTML())
        ############
        div_modal.add(div_modal_body.getHTML())

        # 模态框的脚部
        div_modal_footer = cTag('div', '', {'class': 'modal-footer'})
        btn_modal_ok = cTag('button', '确定',
                            {'class': 'btn', 'data-dismiss': 'modal', 'onclick': '%s_OutPut();' % self.name,
                             'aria-hidden': 'true'})
        btn_modal_close = cTag('button', '关闭', {'class': 'btn', 'data-dismiss': 'modal', 'aria-hidden': 'true'})
        div_modal_footer.add(btn_modal_ok.getHTML())
        div_modal_footer.add(btn_modal_close.getHTML())
        div_modal.add(div_modal_footer.getHTML())

        aValue = self.Html.input('', 'aValue', 'hidden', {'id': '%s_aValue' % self.name})
        # 最后整块处理
        html += div_modal.getHTML() + aValue
        return html + self.js()
