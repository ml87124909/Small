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
from admin.dl.BASE_DL import cBASE_DL

class cF008_dl(cBASE_DL):
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
        #self.SNL=[]     #排序
        #self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0,1,2,3,4,5,6,7])


    #在子类中重新定义
    def myInit(self):
        self.src = 'F008'
        pass

    def mRight(self):
        zszt = self.REQUEST.get('zszt','')
        sql = u"""
            SELECT
                rs.v_code,
                rs.cname,
                to_char(rs.btime,'YYYY-MM-Dd') btime,
                to_char(rs.endtime,'YYYY-MM-Dd') endtime,
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
#         if zszt == '1':
#             sql+=""" and isnull(rs.cstatus,0) = 1 """
#         elif zszt == '2':
#             sql+=""" and isnull(rs.cstatus,0) = 0 """
#         elif zszt == '3':
#             sql+=""" and isnull(rs.cstatus,0) = 2 """
#         else:
#             pass


        #ORDER BY
        # if self.orderby!='':
        #     sql+=' ORDER BY %s %s' % (self.orderby,self.orderbydir)
        # else:
        sql+=" ORDER BY rs.v_code DESC"
        #self.log(sql)
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        
        qqid = self.GP('sqqid','')
        L = {}
        if pk != '':
            sql = """
              SELECT t.v_code,
                  t.cname
              FROM tpsales t(nolock)
            where v_code = '%s'
            """%pk
            L = self.db.fetch( sql )

        List = []
        sql_list = """
            SELECT  A.pm ,A.tps,A.id,A.cname,A.tel,A.memo,convert(varchar(16),A.ctime,121) ctime FROM        
                 (          
                SELECT 
                     ROW_NUMBER() OVER (ORDER BY  (SELECT isnull(SUM(1),0) FROM tpdetail AS t1(NOLOCK)
                                                   WHERE t1.pid = t.id) DESC,t.ctime asc ) pm,
                 isnull((SELECT isnull(SUM(1),0) FROM tpdetail AS t1(NOLOCK)
                                                   WHERE t1.pid = t.id),0) tps,t.id,t.v_code,t.cname,t.tel,t.memo,t.ctime
                FROM tpmanager t(nolock) WHERE t.v_code = '%s' 
                 ) A
                 WHERE 1 = 1 
        """%pk
        if qqid != '':
            sql_list+= """
                and cast(A.id as varchar)+isnull(A.cname,'')+cast(isnull(A.tel,'') as varchar) like '%%%s%%'
            """%qqid
        Li,iT = self.db.select(sql_list)
        if iT>0:
            List = Li

        return L,List

    def local_add_save(self):
        dR={'R':'','MSG':'保存！','B':'1','isadd':'','furl':''}
        #这些是表单值
        return dR

    def local_ajax_stopsale(self):
        status = 0
        pk = self.REQUEST.get('pk','')
        if pk !='':
            sql="""
                update tpmanager set cstatus = 2 where id = '%s'
            """%pk
            self.db.query(sql)
            status = 1
        return status

    def local_ajax_cansale(self):
        status = 0
        pk = self.REQUEST.get('pk','')
        if pk !='':
            sql="""
                update tpmanager set cstatus = 1 where id = '%s'
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
                update tpmanager set cstatus = 0 where v_code = '%s'
            """%pk
            self.db.query(sql)
            status = 1
        status = 1
        return status
