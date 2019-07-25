# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) janedao
# Author：hyj
# Start  Date:  2019
##############################################################################
from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
import time
class cD005_dl(cBASE_DL):
    def init_data(self):
        #self.usr_dept_id=self.dActiveUser['usr_dept'][0]
        #以字典形式创建列表上要显示的字段
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['发布单号',      "rs.v_code",             '120px','center'],#0
            ['活动名称',      "rs.cname",             '350px','left'],#1
            ['活动开始时间',        "",           '150px','center'],#2
            ['活动结束时间' ,"",'150px','center'],#3
            ['活动期限' ,"",'100px','center'],#4
            ['是否开始',      "",'70px','center'] #5
        ]
        #self.GNL=[] #列表上出现的
        #self.SNL=[]     #排序
        #self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0,1,2,3,4,5])


    #在子类中重新定义
    def myInit(self):
        self.src = 'D005'
        pass

    def mRight(self):
        zszt = self.REQUEST.get('zszt','')
        istp = self.REQUEST.get('istp','')

        sql = u"""
             SELECT
                rs.v_code,
                rs.cname,
                to_char(rs.btime,'YYYY-MM-DD' ) btime,
                to_char(rs.endtime,'YYYY-MM-DD') endtime,
                case when rs.btime <= now() and rs.endtime >= now() then '活动期'
                     when rs.btime > now() and rs.endtime > now() then '未到期'
                     when rs.btime < now() and rs.endtime < now() then '过期'
                    else '过期' end,
                coalesce(rs.cstatus,0)
            FROM redsales rs
            WHERE usr_id=%s
        """%self.usr_id_p
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


        #ORDER BY

        sql+=" ORDER BY rs.v_code DESC"
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
              SELECT v_code,
                  cname,
                  daytimes,
                  maxdaytimes,
                  to_char(btime,'YYYY-MM-DD') btime,
                  to_char(endtime,'YYYY-MM-DD') endtime,
                  coalesce(to_char(endtime,'YYYY-MM-DD'),'') endtime,
                  coalesce(edays,0) edays,
                  coalesce(mtimes,0) mtimes,
                  coalesce(mdtimes,0) mdtimes,
                  coalesce(to_char(edtime,'YYYY-MM-DD'),'') edtime,
                  cstatus,
                  memo
                FROM redsales
            where v_code = '%s'
            """%pk
            L = self.db.fetch( sql )
        else:
            L = {}

        List = []

        sql_list = """
            SELECT rd.id,
                rd.vtype,
                coalesce(rd.amount,0) amount,
                rd.price,
                
                coalesce(rd.xg_amount,0) xg_amount
            from redsale_detail rd
           
            WHERE v_code = '%s'
        """%pk
        List,iT = self.db.select(sql_list)
        return L,List

    def local_add_save(self):
        dR={'R':'','MSG':'活动保存成功！','B':'1','isadd':'','furl':''}
        #这些是表单值
        cname = self.REQUEST.get('cname','')  #菜单名称
        daytimes = self.REQUEST.get('daytimes',0)
        maxdaytimes = self.REQUEST.get('maxdaytimes',0)
        btime = self.REQUEST.get('btime','')
        etime = self.REQUEST.get('etime','')
        edays = self.REQUEST.get('edays',0)
        cstatus = self.REQUEST.get('cstatus','')
        memo = self.REQUEST.get('memo','')
        mtimes = self.REQUEST.get('mtimes','')
        edtime = self.REQUEST.get('edtime','')
        mdtimes = self.REQUEST.get('mdtimes',0)

        pk = self.pk


        data = {
                'cname':cname or '',
                'daytimes':daytimes,
                'maxdaytimes':maxdaytimes,
                'mtimes':mtimes or None,
                'edtime':edtime or None,
                'btime':btime or None,
                'endtime':etime or None,
                'edays':edays or 0,
                'mdtimes':mdtimes or  0,
                'cstatus':cstatus or 0,
                'memo':memo or ''
                }

        if str(cstatus) == '1':
            if btime == '' or etime == '':
                dR['R'] = '1'
                dR['MSG'] = '此红包活动发布失败，请确认发布的时间是否正确！'
                return dR

            sql_yz = """
                        select  1 from redsales gs where cstatus = 1
                    """
            lt,iN = self.db.select(sql_yz)
            if iN>0:
                    dR['R'] = '1'
                    dR['MSG'] = '存在红包活动进行中，不能修改'
                    return dR

            MSG = '活动开启成功'
            data['cstime'] = self.getToday(9)
        if pk != '':  #update
            data['uid'] = self.usr_id
            data['utime'] = self.getToday(9)
            sql_st = """
                select * from redsales gs where cstatus = 1 and gs.v_code = '%s' limit 1;
            """%pk
            lt,iN = self.db.select(sql_st)
            if iN>0 and str(cstatus) != '1':
                data['csetime'] = self.getToday(9)
                data['cstatus'] = 2
            self.db.update('redsales',data," v_code = '%s' "%pk)
            self.use_log('修改红包管理%s' % pk)
        else:

            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
            romcode = str(time.time()).split('.')[-1]  # [3:]

            code = 'RFD' + danhao[2:] + romcode
            data['usr_id'] = self.usr_id_p
            data['v_code'] = code
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            self.db.insert('redsales',data)
            self.use_log('增加红包管理%s' % code)
            pk = code
        dR['pk'] = pk
        self.local_save_list(pk)
        dR['isadd'] = 1
        return dR

    def local_save_list(self,v_code):
        xs_type =  self.REQUEST.getlist('xs_type')
        id =  self.REQUEST.getlist('id')
        # item_id =  self.REQUEST.getlist('item_id')
        # itname =  self.REQUEST.getlist('itname')
        amount =  self.REQUEST.getlist('amount')
        price =  self.REQUEST.getlist('price')
        # xg_amount =self.REQUEST.getlist('xg_amount')
        # cstatus = self.REQUEST.get('cstatus','')
        for i in range(len(xs_type)):
            data = {
                    'vtype':xs_type[i] or 0,
                    'amount':amount[i] or 0,
                    'price':price[i] or 0,

                }
            if id[i] not in [0,'',None]:#修改不能修改已用发布量 MINZ20171206
#                 if str(cstatus) == '1':
#                 data['samount'] = amount[i] or 0
                sql_s = """
                    select 1 from redsales gs 
                    where coalesce((gs.csetime > current_timestamp)::integer,2)=2 and gs.v_code = '%s' limit 1;
                """%v_code
                lt,iN = self.db.select(sql_s)
                if iN>0:
                    data['samount'] = amount[i] or 0
                self.db.update('redsale_detail',data," id = %s"%id[i])
            else:
                if amount[i] != '0' and price [i] != '0':
                    data['samount'] = amount[i] or 0
                    data['v_code'] = v_code
                    self.db.insert('redsale_detail',data)
        return

    def local_ajax_stopsale(self):
        status = 0
        pk = self.REQUEST.get('pk','')
        if pk !='':
            sql="""
                update redsales set cstatus = 0 where v_code = '%s'
            """%pk
            self.db.query(sql)
            status = 1
        return status

    def local_ajax_cansale(self):
        status = 0
        pk = self.REQUEST.get('pk','')
        if pk !='':
            sql="""
                update redsales set cstatus = 0 where v_code = '%s'
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
                update redsales set cstatus = 0 where v_code = '%s'
            """%pk
            self.db.query(sql)
            status = 1
        status = 1
        return status

    def local_ajax_getSelectItem(self):

        kw = self.GP('keyword','')

        sql = u"""
                   select id,name,minprice from goods_info
                   where coalesce(del_flag,0)= 0 and coalesce(status,0) = 0 and usr_id=%s
                   """ % self.usr_id_p

        if kw != '':
            sql += " and (name LIKE '%%%s%%')" % (kw)
        sql += " ORDER BY id"
        lT, iN = self.db.select(sql)
        return self.sendMselectData(lT)

    #批量停售
    def lotstop(self):#这里操作停止 用cstatus
        item_id_list = self.REQUEST.get('item_id_list')
        self.db.query("update redsales set cstatus = 2,csetime=getdate() where v_code = '%s'"%item_id_list)
        return 1

    #批量开售
    def lotstar(self):
        item_id_list = self.REQUEST.get('item_id_list')
        yz = self.db.fetch("""select top 1 v_code st from redsales where isnull(cstatus,0) = 1""")
        v_code = yz.get('st','')
        if v_code == '':
            L = self.db.fetch("""SELECT top 1
                                	daytimes,
                                	coalesce(to_char(btime,'YYYY-MM-DD'),'') btime,
                                	coalesce(to_char(endtime,'YYYY-MM-DD'),'') endtime,
                                	coalesce(to_char(edtime,'YYYY-MM-DD'),'') edtime
                                 FROM redsales where v_code = '%s' """%item_id_list)
            if L.get('daytimes',0) == 0 or L.get('btime','') == '' or L.get('endtime','') == '' or L.get('edtime','') == '':
                return 3
            self.db.query("update redsales set cstatus = 1,cstime=getdate() where v_code = '%s' "%item_id_list)
        else:
            return 0
        return 1