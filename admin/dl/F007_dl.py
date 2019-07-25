# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2016 HDH
# Author：MINZ
# Start  Date:  2016/04/26

##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.dl.BASE_DL

    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL import cBASE_DL

class cF007_dl(cBASE_DL):
    def init_data(self):
        #self.usr_dept_id=self.dActiveUser['usr_dept'][0]
        #以字典形式创建列表上要显示的字段
        #以下字典为列表逻辑所用 , 所有数组元素的位置必须对应好
        #[列表名,查询用别名,表格宽度,对齐]
        self.FDT=[
            ['订单号',      "od.code",             '150px','center'],#0
            ['抢购类型',        "isnull(mt.txt1,'')",           '110px','center'],#1
            ['货号',        "h.item_id",           '100px','center'],#2
            ['条码' ,"h.tm",'120px','center'],#3
            ['抢购商品名称',    "qd.vcname",      '','left'],#4
            ['面值/价值',    "ABS(o.price)",      '','right'],#5
            ['数量',    "o.amount",      '','right'],#6
            ['会员姓名',      "isnull(us.usr_name,'')",'','center'],#7
            ['会员卡号',      "isNull(hvi.vipcard,'')",'','center'],#8
            ['手机号码',      "isnull(us.usr_name,'')",'','center'],#9
            ['抢购时间',      "od.ctime",'','center'],#10
            ['过期时间',      "r.edtime",'','center'],#11
            ['抢购状态',    "h.cstatus",     '','center'],#12
            ['订单状态',    "h.cstatus",     '','center'],#13
        ]
        #self.GNL=[] #列表上出现的
        #self.SNL=[]     #排序
        #self.QNL=''  #where查询
        self.GNL = self.parse_GNL([0,2,3,4,5,6,7,8,9,10,12,13])


    #在子类中重新定义
    def myInit(self):
        self.src = 'F007'
        pass

    def mRight(self):
        ddzt = self.GP('ddzt','')
        mddzt = self.GP('mddzt','')

        sDate=self.GP('stime','')
        eDate=self.GP('etime','')

        sql = u"""
            SELECT od.code,
                --h.item_id,
               -- h.tm,
                qd.vcname,
                ABS(qd.price) price,
                o.amount,
                coalesce(us.login_id,''),
                --coalesce(hvi.vipcard,''),
                --coalesce(hvi.tel,''),
                to_char(od.ctime,'YYYY-MM-DD') ctime,
                case when coalesce(o.cstatus,0) = 1 then '有效'
                    else '无效' end,
                case when os.cstatus=1 then '有效订单' when os.cstatus=2 then '交易成功' 
                when os.cstatus=3 then '无效订单' when os.cstatus=4 then '待删订单' else '未生效订单' end
            from qgpm_detail o
            INNER JOIN qgsales_detail  qd ON o.m_id = qd.id
            left join qgsales r on r.v_code=qd.v_code
            --left join hd_item_info h on h.item_id=o.item_id
            left join orderdetail od on od.qgid=o.id
            left join orders os on os.code = od.code
            --LEFT JOIN mtc_t AS mt ON mt.type = 'DW' AND mt.id = h.unit
            LEFT JOIN users us ON us.usr_id = o.cid
            --left join hd_vip_info hvi on hvi.vipcode=us.vip
            WHERE od.vtype = 188
        """
        if ddzt != '':
            sql+=""" and coalesce(o.cstatus,0) = %s"""%ddzt
        if mddzt != '':
            sql+=""" and coalesce(os.cstatus,0) = %s"""%mddzt

        if sDate!='':
            sql+=" and to_char(od.ctime,'YYYY-MM-DD')>='%s'"%sDate

        if eDate!='':
            sql+=" and to_char(od.ctime,'YYYY-MM-DD')<='%s'"%eDate

        # if self.qqid!='' and len(self.QNL) > 0:
        #     sql+=self.QNL + " LIKE '%%%s%%' "%(self.qqid)
        #ORDER BY
        # if self.orderby!='':
        #     sql+=' ORDER BY %s %s' % (self.orderby,self.orderbydir)
        # else:
        sql+=" ORDER BY o.id desc"
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