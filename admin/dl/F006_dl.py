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

class cF006_dl(cBASE_DL):
    def init_data(self):
        #self.usr_dept_id=self.dActiveUser['usr_dept'][0]
        #以字典形式创建列表上要显示的字段
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['红包单号',      "o.code",             '150px','center'],#0
            ['红包类型',        "isnull(mt1.txt1,'')",           '110px','center'],#1
            ['货号',        "h.item_id",           '100px','center'],#2
            ['条码' ,"h.tm",'120px','center'],#3
            ['红包名称',    "o.cname",      '','center'],#4
            ['面值/价值',    "ABS(o.price)",      '','center'],#5
            ['数量',    "o.amount",      '','center'],#6
            ['会员姓名',      "us.usr_name",'','center'],#7
            ['会员卡号',      "hvi.vipcard",'','center'],#7
            ['电话号码',      "hvi.tel",'','center'],#7
            ['红包时间',      "r.ctime",'','center'],#8
            ['过期时间',      "r.edtime",'','center'],#9
            ['红包状态',    "h.cstatus",     '','center'],#10
        ]
        #self.GNL=[] #列表上出现的
        #self.SNL=[]     #排序
        #self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0,1,2,3,4,5,6,7,8,9,10,11,12])


    #在子类中重新定义
    def myInit(self):
        self.src = 'F006'
        pass

    def mRight(self):
        ddzt = self.GP('ddzt','')
        sDate=self.GP('stime','')
        eDate=self.GP('etime','')
        sql = u"""
            SELECT o.code,
                coalesce(mt1.txt1,'')  vtype,
                --h.item_id,
                --h.tm,
                o.cname,
                ABS(o.price) price,
                o.amount,
                coalesce(us.login_id,''),
                --coalesce(hvi.vipcard,''),
                --coalesce(hvi.tel,''),
                to_char(o.ctime,'YYYY-MM-DD') ctime,
                --to_char(o.edtime,'YYYY-MM-DD') 
                edtime,
                case when coalesce(o.cstatus,0) = 0 /*and o.edtime <= now()*/ then 2
                    else coalesce(o.cstatus,0) end
            from v_reddetail o
            --left join hd_item_info h on h.item_id=o.item_id
            --LEFT JOIN mtc_t AS mt ON mt.type = 'DW' AND mt.id = h.unit
            LEFT JOIN mtc_t AS mt1 ON mt1.id = o.vtype AND mt1.type = 'RTYPE'
            LEFT JOIN users us ON us.usr_id = o.cid
            --left join hd_vip_info hvi on hvi.vipcode=us.vip
            WHERE coalesce(o.gid,0) != -10000
        """
        if ddzt != '':
            if str(ddzt) == '2':
                sql+=""" and o.cstatus = 0 and o.edtime <= now() """
            elif str(ddzt) == '0':
                sql+=""" and o.cstatus = 0 and o.edtime > now() """
            else:
                sql+=""" and o.cstatus = %s"""%ddzt
        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+=self.QNL + " LIKE '%%%s%%' "%(self.qqid)

        if sDate!='':
            sql+=" and to_char(o.ctime,'YYYY-MM-DD')>='%s'"%sDate

        if eDate!='':
            sql+=" and to_char(o.ctime,'YYYY-MM-DD')<='%s'"%eDate

        #ORDER BY
        # if self.orderby!='':
        #     sql+=' ORDER BY %s %s' % (self.orderby,self.orderbydir)
        # else:
        sql+=" ORDER BY o.ctime desc"
        #self.log(sql)
        if self.part == 'excel':
            L,select_size=self.db.select(sql)
            PL=[]
        else:
            L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
            PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        L = []
        return L