# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL

import  os , time , random
from flask import  request
class cD006_dl(cBASE_DL):
    def init_data(self):
        #self.usr_dept_id=self.dActiveUser['usr_dept'][0]
        #以字典形式创建列表上要显示的字段
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['发布单号',      "rs.v_code",             '120px','center'],#0
            ['活动名称',      "rs.cname",             '350px','left'],#1
            ['报名开始时间',        "",           '100px','center'],#2
            ['报名结束时间' ,"",'100px','center'],#3
            ['投票开始时间',        "",           '100px','center'],#4
            ['投票结束时间' ,"",'100px','center'],#5
            ['活动期限' ,"",'70px','center'],#6
            ['是否开始',      "",'70px','center'] #7
        ]
        #self.GNL=[] #列表上出现的
        self.GNL = self.parse_GNL([0,1,2,3,4,5,6,7])


    #在子类中重新定义
    def myInit(self):
        self.src = 'D006'
        pass

    def mRight(self):
        zszt = self.REQUEST.get('zszt','')
        sql = u"""
            SELECT
                rs.v_code,
                rs.cname,
                to_char(rs.btime,'YYYY-MM-DD') btime,
                to_char(rs.endtime,'YYYY-MM-DD') endtime,
                to_char(rs.tstime,'YYYY-MM-DD') tstime,
                to_char(rs.tetime,'YYYY-MM-DD') tetime,
                case when rs.btime <= now() and rs.tetime >= now() then '活动期'
                     when rs.btime > now() and rs.tstime > now() then '未开始'
                     when rs.btime < now() and rs.tetime < now() then '已过期'
                    else '' end,
                coalesce(rs.cstatus,0)
            FROM tpsales rs
            WHERE 1 = 1
        """
        # cstatus-- 0 未开启 1活动开启 2活动结束
        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+=self.QNL + " LIKE '%%%s%%' "%(self.qqid)
        if zszt == '1':
            sql+=""" and coalesce(rs.cstatus,0) = 1 """
        elif zszt == '2':
            sql+=""" and coalesce(rs.cstatus,0) = 0 """
        elif zszt == '3':
            sql+=""" and coalesce(rs.cstatus,0) = 2 """
        else:
            pass



        sql+=" ORDER BY rs.id DESC"
        #self.log(sql)
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):

        """获取 local 表单的数据
        """
        L = {}
        if pk != '':
            sql = """
              SELECT t.v_code,
                  t.cname,
                  t.alltimes,
                  to_char(t.btime,'YYYYY-MM-DD') btime,
                  to_char(t.endtime,'YYYY-MM-DD') endtime,
                  to_cahr(t.tstime,'YYYY-MM-DD') tstime,
                  to_cahr(t.tetime,'YYYY-MM-DD') tetime,
                  t.cstatus,
                  coalesce(t.pic,'') pic,
                  t.memo
              FROM tpsales t
              left join send_message sm on t.v_code = sm.pid
            where v_code = '%s'
            """%pk
            L = self.db.fetch( sql )
        else:
            L = {}

        List = [[]]

        sql_list = """
            SELECT rd.id,
                rd.item_id,
                hii.tm,
                rd.vcname,
               rd.sort
            from tpsale_detail rd(nolock)
            left join hd_item_info hii(nolock) on rd.item_id = hii.item_id
            WHERE rd.v_code = '%s'
        """%pk
        # Li,iT = self.db.select(sql_list)
        # if iT>0:
        #     List = Li
        L['XME_id']=L.get('XME_id','new') or 'new'
        return L,List

    def local_add_save(self):
        dR={'R':'','MSG':'活动保存成功！','B':'1','isadd':'','furl':''}
        #这些是表单值
        cname = self.REQUEST.get('cname','')  #菜单名称
        alltimes = self.REQUEST.get('alltimes',0)
        btime = self.REQUEST.get('btime','')
        etime = self.REQUEST.get('etime','')
        tstime = self.REQUEST.get('tstime','')
        tetime = self.REQUEST.get('tetime','')
        cstatus = self.REQUEST.get('cstatus','')
        memo = self.REQUEST.get('memo','')
        file_url=request.files.getlist('file_url')
        pk = self.pk


        
        if str(cstatus) == '1':
            sql_yz1 = """
                  select top 1 1 from tpsales gs(nolock) where cstatus = 1 and v_code <> '%s'
            """%pk
            lt1,t1 = self.db.select(sql_yz1)
            if t1 > 0:
                dR={'R':'1','MSG':'已存在发布活动，请停止后再发布新活动！','B':'1','isadd':'','furl':''}
                return dR
                    


        data = {
                'cname':cname or '',
                'alltimes':alltimes,
                'btime':btime or None,
                'endtime':etime or None,
                'tstime':tstime or None,
                'tetime':tetime or None,
                'cstatus':cstatus or 0,
                'memo':memo or ''
                }

        if str(cstatus) == '1':
            if btime == '' or etime == '':
                dR['R'] = '1'
                dR['MSG'] = '此投票活动发布失败，请确认发布的时间是否正确！'
                return dR

            MSG = '活动开启成功'
            data['cstime'] = self.getToday(9)
        if pk != '':  #update
            sql_yz = """
                        select 1 from tpsales gs(nolock) where cstatus = 1 and v_code = '%s'
                    """%pk
            lt,iN = self.db.select(sql_yz)
            if iN>0 and str(cstatus) == '1':
                dR['R'] = '1'
                dR['MSG'] = '此活动进行中，不能修改'
                return dR

            data['uid'] = self.usr_id
            data['utime'] = self.getToday(9)
            
            if iN>0 and str(cstatus) != '1':
                data['cstatus'] = 2
            self.db.update('tpsales',data," v_code = '%s' "%pk)
        else:
            code= self.Get_New_Code('TPD',6)
            data['v_code'] = code
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            self.db.insert('tpsales',data)
            sql_ms = """
                select top 1 id from send_message(nolock) where isnull(pid,'') = '' order by id desc
            """
            LS = self.db.fetch(sql_ms)
            lsid = LS.get('id',0) or 0
            if lsid != 0:
                sql_up = """ update send_message set pid = '%s' where id = %s"""%(code,lsid)
                self.db.query(sql_up)
            pk = code
          
        if pk != '':  #update
            for url in file_url:
                if url.filename != '':
                    file_name = url.filename.split('\\')[-1]   #文件名称
                    
                    ext = file_name.split('.')[-1]
                    
                    file_content = url.read()
                    
                    path = os.path.join(dINI['ATTACH_ROOT'] ,'tpgl')
                    #检查目录是否存在，如果不存在，生成目录  make_sub_path
                    self.make_sub_path(path)
                    PATH = os.path.join(path,'%s.%s'%(pk,ext))
                    
                    f = open(PATH,'wb')
                    f.write(file_content)
                    f.flush()
                    f.close()

                    sql=" update tpsales set pic = '%s' where v_code = '%s' "%(ext, pk)
                    self.db.query(sql)
                      
        dR['pk'] = pk
        self.local_save_list(pk)
        dR['isadd'] = 1
        return dR

    def local_save_list(self,v_code):
        id =  self.REQUEST.getlist('id')
        item_id =  self.REQUEST.getlist('item_id1')
        itname =  self.REQUEST.getlist('itname')
        sort =  self.REQUEST.getlist('sort')
        for i in range(len(itname)):
            data = {
                    'item_id':item_id[i] or 0,
                    'vcname':itname[i] or '',
                    'sort':sort[i] or 0
                }
            if id[i] not in [0,'',None]:#
                if itname[i] == '':
                    sql_del=""" delete from tpsale_detail where id = %s;"""%id[i]
                    self.db.query(sql_del)
                else:
                    self.db.update('tpsale_detail',data," id = %s"%id[i])
            else:
                if itname[i] != '':
                    data['v_code'] = v_code
                    self.db.insert('tpsale_detail',data)
                    
        return

    def local_ajax_stopsale(self):
        status = 0
        pk = self.REQUEST.get('pk','')
        if pk !='':
            sql="""
                update tpsales set cstatus = 0 where v_code = '%s'
            """%pk
            self.db.query(sql)
            status = 1
        return status

    def local_ajax_cansale(self):
        status = 0
        pk = self.REQUEST.get('pk','')
        if pk !='':
            sql="""
                update tpsales set cstatus = 0 where v_code = '%s'
            """%pk
            self.db.query(sql)
            status = 1
        status = 1
        return status

    def local_ajax_notsale(self):
        status = 0
        pk = self.REQUEST.get('pk','')
        if pk !='':
            sql="""
                update tpsales set cstatus = 0 where v_code = '%s'
            """%pk
            self.db.query(sql)
            status = 1
        status = 1
        return status

    def local_ajax_getSelectItem(self):

        kw = self.GP('keyword','')

        sql = u"""
            select top 1000
                h.item_id
                ,h.tm
                ,h.cname
                ,lq.price
                ,h.ls_price
                ,lq.qlb_code
                ,case when isnull(lq.qlb_code,0) = 1 then '全场通用' else isnull(lq.qlbname,'') end qlbname
            from hd_item_info h(nolock)
            left join hd_item_lq lq(nolock) on h.item_id = lq.item_id
            where isnull(h.del_flag,0)= 0 and isnull(h.status,0) <> 2
            """

        if kw != '':
            sql += " and (h.cname LIKE '%%%s%%' or h.tm like '%%%s%%')" % (kw,kw)
        sql += " ORDER BY h.item_id"
        lT, iN = self.db.select(sql)
        return self.sendMselectData(lT)

    #批量停售
    def lotstop(self):#这里操作停止 用cstatus
        item_id_list = self.REQUEST.get('item_id_list')
        self.db.query("update tpsales set cstatus = 2,utime=getdate() where v_code = '%s'"%item_id_list)
        return 1

    #批量开售
    def lotstar(self):
        item_id_list = self.REQUEST.get('item_id_list')
        R = self.get_tptime(item_id_list)
        if R == 1:
            return 0
        if item_id_list != '':
            self.db.query("update tpsales set cstatus = 1,utime=getdate() where v_code = '%s' "%item_id_list)
        else:
            return 0
        return 1
    
    def get_tptime(self,pk):
        R = 0
        sql_yz = """
                    select top 1 1 from tpsales gs(nolock) where cstatus = 1 and v_code <> '%s'
        """%pk
        lt,iN = self.db.select(sql_yz)
        if iN>0:
            R = 1
        return R