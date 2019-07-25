# -*- coding: utf-8 -*-
####################################################################
#
#
#####################################################################
from imp import reload
from basic.publicw import DEBUG


if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import  os , time , random ,uuid
 

class cXME_dl(cBASE_DL):
    
    def specialinit(self):
        """功能：提供额外的初始化"""

    def init_data(self):
        #self.usr_dept_id=self.of_id
        #以字典形式创建列表上要显示的字段 
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['ID','l.id','',''],  #0
            ['栏目信息标题','l.title','',''],  #1
            ['栏目类型','','',''],#2
            ['建立人','u.usr_name','',''],#3
            ['建立时间','l.ctime','',''],#4
            ['发布时间','l.utime','',''],#5
            ['微信链接','','','']#6
        ]
        #self.GNL=[] #列表上出现的
        #self.SNL=[]     #排序
        #self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0,1,3,4])

        
    #在子类中重新定义         
    def myInit(self):
        self.src = 'XME'
        pass

    def mRight(self):
        
        filter=self.REQUEST.get('filter','')
        
        sql = """
        SELECT
                l.id,
                l.title,
                u.usr_name,
                to_char(l.ctime,'YYYY-MM-DD')
            FROM send_message l
            left join users u on u.usr_id=l.cid
            left join mtc_t m on m.id=l.xh_message and m.type='xhmss'
            WHERE 1 = 1 and coalesce(l.is_old,0)=1 and coalesce(l.del_flag,0)=0
        """
        #wheresql = ''
        #ordersql = ''
        #Where 
        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+=self.QNL + " LIKE '%"+self.qqid+"%' "
        if filter != '':
            sql+='and l.xh_message=%s'%filter
        #ORDER BY 

        sql+=" ORDER BY l.id"

        data = {'qqid':self.qqid}
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def mRightSql(self):
            
        sql = """
         SELECT
                l.id,
                l.title,
                '',
                u.usr_name,
                to_char(l.ctime,'YYYY-MM-DD')
            FROM send_message l
            left join users u on u.usr_id=l.cid
            WHERE 1 = 1 and coalesce(l.is_old,0)=1
        """
            
        #除超级管理员外，其他人不允许操作和查看  默认权限、系统管理员权限、默认权限
        if str(self.usr_id) != '1':
            sql += """
            and 1=0
            """      
        return sql         
            
    def local_ajax_isOtherSystemRoles(self,role_id=0):
        ##从其它系统中同步过来的角色
        #return '0'
        if role_id==0:role_id=self.REQUEST.get('role_id','0')
        if role_id=='':role_id=0
        sql="select count(role_id) from roles where role_id=%s"%role_id
        lT,lN=self.db.select(sql)
        if lT[0][0]>0:
            return '1'
        else:
            return '0'
            
    def getPageData(self , pk):
        
        """获取 local 表单的数据
        """
        
        L = {}
        
        sql = """
        SELECT
                    l.id,
                    l.title,
                    '',
                    l.sort,
                    l.url,
                    u.usr_name,
                    to_char(l.ctime,'YYYY-MM-DD'),
                    u1.usr_name,
                    to_char(l.utime,'YYYY-MM-DD'),
                    l.logo,
                    l.content
                FROM send_message l
                left join users u on u.usr_id=l.cid
                left join users u1 on u1.usr_id=l.uid
                WHERE l.id=%s
        """ % pk
        
        if pk != '':
            L = self.db.fetch( sql )
        
        return L
    
    def local_add_save(self):
        
        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        pass

        
    def get_mtype(self):
        return ({'mtype':[], 'parent':[], 'groups':[], 'course':[]})

    def local_ajax_get_mtype(self):
        return self.get_mtype()

    def get_lm_type(self,title='---'):
        sql="select id,title from lm_type"
        lT,iN=self.db.select(sql)
        if title=='':        
            L=[]
        else:
            L=[['',title,'','']]
        for e in lT:
            id=e[0]
            txt=e[1]
            L.append([id,txt,'',''])
        return L

    def local_ajax_showData(self):
        show_id = self.REQUEST.get('show_id','0')


        re = {"code":0,"message":"Common:OK","data":{'version': "0.1",'title': '','desc': '','cover': '','backgroundMusic': '','scene': "flw.vertical.one-page",
				'cname': '','infoType':'','show_id':show_id,'pages':[],'infoTypeList':[],'mGroupList':self.get_xhmss_data()
                ,'mGroup':'','course':'','wbUrl':'','isShow':'',
				'mSort': 0,"show_data_url":""
                ,"show_url":"","hit_count":2,"cur_hits":2,"official_copy":False
                ,"history_hits":0,"created_at":"2015-12-17T00:47:05.000Z","updated_at":"2015-12-17T00:47:49.000Z"
                ,"right_vip_host":1,"right_freeshow":0,"mask_no_modification":0,"mask_on_locking":0,"traffic":0,"points":0
                ,"show_data_name":"1jjY/0a70417fd8e38f2a91f65041d55b8c15","right_no_logo":0,"right_no_advert":0
                }}

        l,i = self.db.select(""" select li.id,ISNULL(li.title,''),ISNULL(li.lm_type,0),ISNULL(li.[desc],''),isNull(li.sort,0),isNull(li.url,''),ISNULL(li.show_data,'') from send_message li where li.id=%s"""%(show_id))
        
        if i>0:
            re['data']['show_id'] = l[0][0]
            re['data']['title'] = l[0][1]
            re['data']['infoType'] = l[0][2]
            re['data']['desc'] = l[0][3]
            re['data']['sort'] = l[0][4]
            re['data']['wbUrl'] = l[0][5]
            re['data']['show_data'] = l[0][6]
            
            re['data']['show_data_url'] = '%sadmin?fid=XME&part=ajax&action=getData&pk=%s'%(localurl , l[0][0])
        
        
        return re

    def local_ajax_getStatus(self,pk=''):
        if pk=='':pk=self.REQUEST.get('pk','')
        data={'code':0}

        return data
            
    def local_ajax_show(self):
        import json
        data = {}
        pid = self.REQUEST.get('pid','0').strip()
        show_id = self.REQUEST.get('show_id','0').strip()
        showData = self.REQUEST.get('showData','{}')#.decode('utf-8').encode('gbk')
        showData1 = self.REQUEST.get('showData','{}')
        dict_data=json.loads(showData1)
        sd = read(str(showData))

        ctime=self.getnow
        utime=self.getnow



        re={"code":0,"message":"Common:OK","data":{"show_id":'0',"mSort":''
                ,'infoType':'','mGroup':'','course':'','wbUrl':''
                ,"show_data_url":""
                ,'isShow':''
                ,"show_url":"","hit_count":2,"cur_hits":2,"official_copy":False
                ,"history_hits":0,"created_at":"2015-12-17T00:47:05.000Z","updated_at":"2015-12-17T00:47:49.000Z"
                ,"right_vip_host":1,"right_freeshow":0,"mask_no_modification":0,"mask_on_locking":0,"traffic":0,"points":0
                ,"show_data_name":"1jjY/0a70417fd8e38f2a91f65041d55b8c15","right_no_logo":0,"right_no_advert":0
                ,'mGroupList':self.get_xhmss_data()
                }}

        course = sd.get('course',{})
        if course=='':course={}
        data['title'] = sd.get('title','') or ''
        data['lm_type'] = sd.get('infoType','') or '0'
        data['sort'] = sd.get('mSort','') or ''
        data['url'] = sd.get('wbUrl','') or ''
        data['hDesc'] = sd.get('html','') or ['NULL']
        data['show_data'] = showData or ''
        data['desc'] = sd.get('desc','') or ''
        data['cover'] = sd.get('cover','') or ''
        data['is_old']=1
        data['pid']=pid

        statusCode=read(self.local_ajax_getStatus(show_id)).get('code',0)

        if show_id=='' or show_id in[ '0',0,None]:
            data['cid'] = self.usr_id
            data['uuid'] = str(uuid.uuid1())
            data['ctime'] = ctime
            data['xh_message'] = dict_data.get('mGroup','')
            mSql=self.db.insert('send_message', data,1)
            self.db.query(mSql)
            l,i = self.db.select(""" select li.id,ISNULL(li.title,''),ISNULL(li.lm_type,0),ISNULL(li.[desc],''),isNull(li.sort,0),isNull(li.url,''),ISNULL(li.show_data,'') from send_message li where li.uuid='%s'"""%(data['uuid']))
        else:
            data['uid'] = self.usr_id
            data['utime'] = utime
            data['xh_message'] = dict_data.get('mGroup','')
            mSql=self.db.update('send_message', data, " id = '%s' "%str(show_id),1)
            self.db.query(mSql)
            l,i = self.db.select(""" select li.id,ISNULL(li.title,''),ISNULL(li.lm_type,0),ISNULL(li.[desc],''),isNull(li.sort,0),isNull(li.url,''),ISNULL(li.show_data,'') from send_message li where li.id=%s"""%(show_id))
        
        re['data']['show_id'] = l[0][0]
        re['data']['title'] = l[0][1]
        re['data']['infoType'] = l[0][2]
        re['data']['desc'] = l[0][3]
        re['data']['sort'] = l[0][4]
        re['data']['wbUrl'] = l[0][5]
        re['data']['show_data'] = l[0][6]
        
        re['data']['show_data_url'] = '%sadmin?fid=XME&part=ajax&action=getData&pk=%s'%(localurl , l[0][0])
        
        return write(re)

    def local_ajax_getData(self):
        pk = self.REQUEST.get('pk','')
        l,i = self.db.select("SELECT id,show_data from send_message where id='%s' "%(pk))

        return l[0][1]
    
    def get_xhmss_data(self):
        l,n=self.db.select("select id,txt1 from mtc_t where type='xhmss'")
        L=[['','--请选择--']]
        L=L+l
        return L
        
    def delete_data(self):
        pk=self.GP('pk','')
        sql="""
            update send_message set del_flag=1 where id=%s
        """%pk
        self.db.query(sql)
        return {'R':'0','MSG':''}
    
    def local_ajax_release(self):
        id=self.GP('id','').split(',')
        for e in id:
            sql="update send_message set send_time=GETDATE(),rel_flag=1 where id = %s"%e
            
            self.db.query(sql)
            
        return 1
        