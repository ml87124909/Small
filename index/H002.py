# -*- coding: utf-8 -*-
##############################################################################
#
#
#
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG=='1':
    import index.VI_BASE
    reload(index.VI_BASE)
from index.VI_BASE             import cVI_BASE

from flask import session

import time,datetime
#import source.wzhifu as wzhifu
# exec('from %s.source.wzhifu         import *'%share.CLIENT_NAME)
# exec('import %s.index.wzhifu  as mwzhifu '%share.CLIENT_NAME)


class cH002(cVI_BASE):

    def specialinit(self):

        if self.GP('ared'):
            self.part = "addqg"
            self.assign("site_title","抢购活动")
        elif self.GP('cancel'):
            self.part = "cancel"
            self.assign("site_title","抢购活动")
        elif self.GP('local'):
            self.part = "localfrom"
            self.assign("site_title","抢购活动")
        elif self.GP('detail'):
            self.part = "detail"
            self.assign("site_title","我的排名")
        elif self.GP('ord'):
            self.part = "orddetail"
            self.assign("site_title","抢购活动下单")
        elif self.GP('a'):
            self.part = "local_add_save"
            self.assign("site_title","抢购活动下单")
        elif self.GP('toshowgoods'):
            self.part = 'showgoods'
            self.assign("site_title","商品详情")
        else:
            self.assign("site_title","抢购活动")

    def goPartMenu(self):
        dict = {'status':0,'times':0,'memo':''}
        v_code = self.GP('mycode','')
        ppmid = self.GP('ppmid','')
        if ppmid !='':
            sql_del=""" update qgpm_detail set cstatus = 2 where id = %s """%ppmid
            self.db.query(sql_del)
        errors,times,v_code = self.get_my_qgtimes(v_code)
        if errors == 1:#活动结束
            status = 9
        elif errors == 0:
            status = 1
        else:
            status = errors

        if status == 9:#活动结束
            sql = '''
               select coalesce(memo,'') memo from qgsales where coalesce(memo,'') !='' 
            '''
            if v_code !='':
                sql+=''' and v_code = '%s' '''%v_code
            sql+='''
               order by (case when coalesce(cstatus,0) = 0 THEN 3 ELSE cstatus END ) asc,csetime desc limit 1
            '''
        else:
            sql = '''
               select coalesce(memo,'') memo from qgsales where coalesce(cstatus,0) = 1 
            '''
            if v_code !='':
                sql+=''' and v_code = '%s' '''%v_code
            sql+=" limit 1"

        item = self.db.fetch(sql)
        memo = item.get('memo','').replace('\r\n',r'<br>')

        dict['cstatus'] = status
        dict['times'] = times
        dict['memo'] = memo
        dict['v_code'] = v_code
        sql = """
            SELECT distinct fqd.item_id,'第'||cast(fqd.pm as varchar)||'名' pm,case when len(limit 1(fqd.vcname,'')) > 10
                                               THEN substring(isnull(fqd.vcname,''),1,10)+'...'
                                               ELSE limit 1(fqd.vcname,'') END vcname,
                                               cast(fqd.price as varchar)||'元' price ,
                    hii.pic,limit 1(hii.item_id,0) item_id
             FROM dbo.f_qg_detail('%s') AS fqd
             LEFT JOIN hd_item_info AS hii ON fqd.item_id = hii.item_id
             where not exists(select top 1 1 from qgpm_detail qd(nolock) where 
              qd.m_id = fqd.id and fqd.pm = qd.pmid and qd.cstatus = 1)
        """%v_code

        #self.print_log('000','%s'%sql)
        L=[]#,t = self.db.fetchall(sql)

        ##“已下单 和未下单未过期”参与 排名
        sql_pm = """
            SELECT '第'||cast(fqd.pm as varchar)+'名' pm,
                case when len(limit 1(qd.vcname,'')) > 10
                                                            THEN substring(limit 1(qd.vcname,''),1,10)+'...'
                                                    ELSE limit 1(qd.vcname,'') END
                                         vcname,
                qd.price,
                limit 1(substring(limit 1(us.usr_name,''),1,1),'')+'**'+limit 1(substring(limit 1(us.usr_name,''),3,5),'') usr_name,
                limit 1(substring(limit 1(us.mobile,''),1,3),'')+'**'+limit 1(substring(limit 1(us.mobile,''),8,11),'') mobile,
                ( select sum(limit 1(hii1.ls_price,0)*limit 1(hid.amount,0))
                            from hd_item_db hid(nolock)
                            left join hd_item_info hii1(nolock) on hid.item_id = hii1.item_id
                            where hid.sitem_id = hii.item_id)  ls_price
            from qgpm_detail qgd(nolock)
            left JOIN qgsales_detail AS qd(nolock) ON qgd.m_id = qd.id
            LEFT JOIN dbo.f_qg_detail('') AS fqd ON fqd.pm = qgd.pmid and fqd.id = qd.id
            LEFT JOIN users us(nolock) ON us.usr_id = qgd.cid
            left join hd_item_info hii(nolock) on  qgd.item_id = hii.item_id
            WHERE isnull(cstatus,0) = 1
            and qd.v_code = '%s'
            ORDER BY qgd.pmid ASC
        """%v_code
        L1=[]#,t1 = self.db.fetchall(sql_pm)
        self.assign("v_code",v_code)
        self.assign("item",dict)
        self.assign("itemlist",L)
        self.assign("pmlist",L1)
        #
        return self.display('H002.html')

    def goPartDetail(self):
        srfid = self.GP('srfid','H002')

        searchText=self.GP('searchText','')
        sql='''
           SELECT
                r.id,
                coalesce(o.code,'') v_code,
                qd.vcname,
                qd.price,
                r.amount,
                r.pmid,
                r.ctime,
                to_char(r.etime,'YYYY-MM-DD') etime,
                coalesce(r.cstatus,0) cstatus,
                case when coalesce(r.cstatus,0) = 0 AND coalesce(od.cstatus,0) != 3 THEN '未下单'
                WHEN coalesce(r.cstatus,0) = 1 AND coalesce(od.cstatus,0) = 1 THEN '已下单'
                WHEN coalesce(r.cstatus,0) = 1 AND coalesce(od.cstatus,0) = 2 THEN '已领'
                WHEN coalesce(r.cstatus,0) = 1 AND coalesce(od.cstatus,0) = 3 THEN '已失效'
                WHEN coalesce(r.cstatus,0) = 1 AND coalesce(od.cstatus,0) = 0 THEN '未付款'
                else '待删' end istatus
            FROM qgpm_detail r
            INNER JOIN qgsales_detail AS qd ON r.m_id = qd.id
            left join orderdetail o on r.id = o.qgid and o.vtype = 188
            LEFT JOIN orders od ON o.code = od.code
        WHERE (coalesce(r.cstatus,0)= 1 OR coalesce(r.cstatus,0)= 0 AND etime >now())
            AND r.cid=%s
        '''%self.usr_id
        if searchText != '':
            sql+="""
                and (qd.vcname like '%%%s%%')
            """%(searchText)
        sql+=""" order by r.ctime desc """
        l,n=self.db.fetchall(sql)
        self.assign('datalist',l)
        self.assign("srfid",srfid)
        return self.display('H002_detail.html')

    def goPartAddqg(self):
        error = 0
        times = 0
        msg = ''
        id = 0
        v_code = self.GP('my_code','')
        if v_code == '':
            yz = self.db.fetch("""select top 1 v_code st from qgsales where coalesce(cstatus,0) = 1 and btime < now() and endtime >now() """)
            v_code = yz.get('st','')
        if v_code == '':
            return self.jsons({'error':10,'msg':'活动敬请期待...','times':times,'ppmid':0})
        try:
            errors,times,v_code = self.get_my_qgtimes(v_code)
            if errors == 1:#活动已结束
                error = 4
                msg = '活动已结束...'
                return self.jsons({'error':error,'msg':str(msg),'times':times,'ppmid':0})
            elif errors == 2:#本次活动已用完机会
                error = 5
                msg = '您本次抢购活动次数已用完...'
                return self.jsons({'error':error,'msg':str(msg),'times':times,'ppmid':0})
            elif errors == 11:#还有未过期
                error = 11
                msg = '您本次活动还有抢购商品未下单...'
                return self.jsons({'error':error,'msg':str(msg),'times':times,'ppmid':0})
            else:
                pass
            code = self.Get_New_Code('R',6,0)
            ###抢购开始###
            I,iN = self.db.select("""select * from qgmybag( '%s',%s)"""%(v_code,self.usr_id))
            #zid,pm,id 抢购表id 排名 抢购活动明细表id
            if iN >0:
                id = int(I[0][0]) #qgpm_detail表 id
                if id == 0:
                    error = 6
                    msg = '很遗憾，已被抢光了'
                else:
                    id = int(I[0][0])
                    pm = int(I[0][1])
                    qgid = int(I[0][2])
                    L = self.db.fetch(""" SELECT  case when len(coalesce(qd.vcname,'')) > 10
                                                            THEN substring(coalesce(qd.vcname,''),1,10)+'...'
                                                    ELSE coalesce(qd.vcname,'') END
                                         vcname,cast(coalesce(qd.price,0) as numeric(16,2))  price ,
                                         cast( ( select sum(coalesce(hii1.ls_price,0)*coalesce(hid.amount,0))
                                                from hd_item_db hid(nolock)
                                                left join hd_item_info hii1 on hid.item_id = hii1.item_id
                                                where hid.sitem_id = hii.item_id)
                                          as numeric(16,2)) ls_price
                                         FROM qgsales_detail AS qd
                                         left join hd_item_info hii= on hii.item_id = qd.item_id
                                         where qd.id = %s  limit 1;"""%(qgid))
                    vcname = L.get('vcname','')
                    price = L.get('price',0.00)
                    ls_price = L.get('ls_price',0.00)
                    msg = "<br><br>恭喜您<br>"
                    msg += "抢到第&nbsp;"+str(pm)+"&nbsp;名<br>"
                    msg += str(vcname)+' '+str(price)+'元（原价'+str(ls_price)+'元）<br>'
                    msg += "确认下单？"
            else:
                error = 6
                msg = '很遗憾，已被抢光了'
        except Exception as ex:
            error = 3
            msg = '抢购活动已停止...'+str(ex)
        return self.jsons({'error':error,'msg':str(msg),'times':times,'ppmid':id})

    def goPartOrddetail(self):

        srfid = self.GP('srfid','H002')
        pmmid = self.GP('pmmid','')
        totolMoney = 0.00
        if srfid=='H002' and pmmid == '':
            return self.redirect('index/%s?viewid=H002'%self.sub_id)

        L = []
        t = 0
        sqlit = """ select top 1 1 from qgpm_detail where id = %s and cid = %s and cstatus = 0 and etime > now()"""%(pmmid,self.usr_id)
        F,it = self.db.select(sqlit)
        if it >0:
            pass
        else:
            MSG ='您手慢了一步，排名已失效'
            self.assign('MSG',MSG)
            self.assign("srfid",srfid)
            return self.display('myorders.html')
        sqlL = """
            SELECT top 1 s.id,hii.cname spname ,s.amount,qd.price,coalesce(m.txt1,'') unit  FROM qgpm_detail AS s(nolock)
            INNER JOIN qgsales_detail AS qd(NOLOCK) ON qd.id = s.m_id
            inner join hd_item_info hii(nolock) on hii.item_id = s.item_id
            left join mtc_t m(nolock) on m.[type]='DW' and m.id = hii.unit
            where s.cid = %s and s.id = %s
        """%(self.usr_id,pmmid)

        L,t = self.db.fetchall(sqlL)
        for e in L:
            totolMoney+=float(e.get('price',0))
        sql = """
              select '阳江市阳东区东城镇合章路东润市场A02商铺' addr,
                      hv.vipname,
                      hv.tel
              from hd_vip_info hv(nolock)
              inner join users us(nolock)
                   on us.vip = hv.vipcode
              where usr_id = %s
        """%self.usr_id
        item = self.db.fetch(sql)


        self.assign("item",item)
        self.assign("dataList",L)
        self.assign("totalMoney",totolMoney)
        self.assign("count",t)
        self.assign("srfid",srfid)
        self.assign("gwgoodid",pmmid)

        wftime = self.db.fetch("""select max(coalesce(dftimes,0)) dftimes from qgsales(nolock) where  cstatus = 1""")
        
        #默认时间
        ddtime = datetime.datetime.now()+datetime.timedelta(8) #不计当天 7天 第8天截止
        dtime1 = ddtime.strftime('%Y年%m月%d日')
        dtime = ddtime.strftime('%Y年%m月%d日')
        dftimes = wftime.get('dftimes',0) or 0
        if dftimes >0:
            ddtime = datetime.datetime.now()+datetime.timedelta(hours=dftimes) #不计当天 7天 第8天截止
            dtime = ddtime.strftime('%Y年%m月%d日 %H:%M')

        
        #如果有限制时间发布 取最大一个商品拿货时间
#             if srfid == 'B001':
#                 dtsql = """
#                    select isnull(convert(varchar(10),max(gs.jz_time),121),'')  jz_time from shopbox s(nolock)
#                   left join goodsale gs(nolock) on s.goodsid = gs.id  where s.cid = %s and s.goodsid in (%s)
#                 """%(self.usr_id,gwgoodid)
#             else:
#                 dtsql = """
#                     select isnull(convert(varchar(10),max(gs.jz_time),121),'') jz_time from shopbox s(nolock)
#                   left join goodsale gs(nolock) on s.goodsid = gs.id  where s.cid = %s
#                 """%self.usr_id
#             item = self.db.fetch(dtsql)
#             jztime = item.get('jz_time','')
#             if jztime != '':
#                 jt = jztime.split('-')
#                 dtime = str(jt[0])+'年'+str(jt[1])+'月'+str(jt[2])+'日'
        self.assign("ddtime",dtime)
        self.assign("ddtime1",dtime1)

        return self.display('H002_order.html')

    def goPartlocal_add_save(self):
        #支付方式 1.微信支付。2.到店付
        payfor = self.GP('payfor','')
        totalMoney = self.GP('totalMoney',0)
        srfid = self.GP('srfid','H002')
        gwgoodid = self.GP('gwgoodid','')
        MSG = '1'
        sqlit = """ select top 1 coalesce(cstatus,0) from qgpm_detail where id = %s and cid = %s and etime > now()"""%(gwgoodid,self.usr_id)
        F,it = self.db.select(sqlit)
        if it >0:
            Fstatus = F[0][0]
            if Fstatus == 0:
                pass
            else:
                MSG ='重复操作，请去查看我的排名'
                self.assign('MSG',MSG)
                self.assign('srfid',srfid)
                return self.display('myorders.html')
        else:
            MSG ='您手慢了一步，排名已失效'
            self.assign('MSG',MSG)
            self.assign('srfid',srfid)
            return self.display('myorders.html')
        if gwgoodid !='':
            sql_yz = """
                SELECT top 1 1 FROM qgpm_detail AS s
                INNER JOIN qgsales_detail AS qd(NOLOCK) ON qd.id = s.m_id
                inner join hd_item_info hii on hii.item_id = s.item_id
                where s.cid = %s and s.id = %s
                """%(self.usr_id,gwgoodid)
        else:
            MSG ='订单错误'
            self.assign('MSG',MSG)
            self.assign('srfid',srfid)
            return self.display('myorders.html')
        L,iN = self.db.fetchall(sql_yz)
        if iN>0:
            pass
        else:
            MSG ='订单错误'
            self.assign('MSG',MSG)
            self.assign('srfid',srfid)
            return self.display('A003.html')
        #0.新增订单表
        codeing = self.Get_New_Code('W9',6,0)

        zfzt = 0

        #zfstatus 0未付款 1付款
        #cstatus 0新订单 1有效订单  2已完成 3删除订单
        zt = 0
        if str(payfor) == '2':
            zt = 1
        
        wftime = self.db.fetch("""select max(coalesce(dftimes,0)) dftimes from qgsales(nolock) where  cstatus = 1""")
        dftimes = wftime.get('dftimes',0) or 0
        if str(payfor) == '2' and dftimes >0:
            sqldd="""
                insert into orders(code,totalmoney,zffs,zfstatus,cstatus,cid,ctime,ydtime)
                values ('%s',%s,%s,0,%s,%s,now(),dateadd(hh,%s,getdate()))
            """%(codeing,totalMoney,payfor,zt,self.usr_id,dftimes)
        else:
            sqldd="""
                insert into orders(code,totalmoney,zffs,zfstatus,cstatus,cid,ctime,ydtime)
                values ('%s',%s,%s,0,%s,%s,now(),now()+8)
            """%(codeing,totalMoney,payfor,zt,self.usr_id)
        self.db.query(sqldd)

        sqldt="""
            insert into orderdetail(code,goodsid,amount,price,cid,ctime,item_id,vtype,qgid)
            select '%s',0,s.amount,qd.price,s.cid,getdate(),s.item_id,188,s.id
              from qgpm_detail s
            INNER JOIN qgsales_detail AS qd ON s.m_id = qd.id
            where s.cid = %s and s.id = %s
        """%(codeing,self.usr_id,gwgoodid)
        self.db.query(sqldt)

        #1.更新状态
        sql_gl = """
            UPDATE s set s.cstatus = 1 FROM qgpm_detail AS s
                where s.cid = %s and s.id = %s
        """%(self.usr_id,gwgoodid)
        self.db.query(sql_gl)
        if str(payfor) == '1':
            mwzf = mwzhifu.wzhifu()
            openid=session.get('__openid','')
            body="黄金牛儿童百货-超市"
            mwzf.getOutTradeNo(body,totalMoney, 'orders',codeing,openid)

        self.assign('pkid',codeing)
        self.assign('payfor',payfor)
        self.assign('totalMoney',totalMoney)
        self.assign('MSG',MSG)
        self.assign('srfid',srfid)
        return self.display('myorders.html')

    def goPartShowgoods(self):
        id = self.GP('ttid','0')
        srfid = self.GP('srfid','H002')
        sql1 = """
                    select
                       hii.item_id
                       ,hii.cname
                       ,( select sum(coalesce(hii1.ls_price,0)*coalesce(hid.amount,0))
                            from hd_item_db hid(nolock)
                            left join hd_item_info hii1(nolock) on hid.item_id = hii1.item_id
                            where hid.sitem_id = hii.item_id) ls_price
                       ,hii.pic fext
                       ,isnull(sm.hDesc,'') hDesc
                    from  hd_item_info hii(nolock)
                    left join send_message sm(nolock) on cast(hii.item_id as varchar) = sm.pid
                    where hii.item_id = %s
                    """%id
        item = self.db.fetch(sql1)

        sql2 = """
                    select hii.item_id,hii.cname,hi.amount,coalesce(t.txt1,'') dw,hii.pic fext
                    from hd_item_db hi(nolock)
                    left join hd_item_info hii(nolock) on hi.item_id = hii.item_id
                    LEFT JOIN mtc_t AS t(nolock) ON t.id = hii.unit AND t.[type] = 'DW'
                    where hi.sitem_id = %s
        """%(id)
        tc_detail,t = self.db.fetchall(sql2)

        self.assign('tc_detail',tc_detail)
        self.assign('item',item)
        self.assign('srfid',srfid)
        return self.display('goods.html')

    def toorders(self):
        return ''

    def orders(self):
        return ''

    def get_my_qgtimes(self,v_code = ''):
        times = 0
        error = 0

        sql_yz ="""select  v_code st,
                                   daytimes
                                  from qgsales where coalesce(cstatus,0) = 1  and btime < now()
                                  and endtime >now()  """
        if v_code != '':
            sql_yz+= """ and v_code = '%s'"""%v_code
        sql_yz+=" limit 1"
        yz = self.db.fetch(sql_yz)
        v_code = yz.get('st','')
        dtimes = int(yz.get('daytimes',0))


        sql="""SELECT 1 as samount FROM f_qg_detail('%s') A limit 1"""%v_code
        #print(sql,'sql')
        sam = self.db.fetch(sql)
        samount = sam.get('samount',0)
        if samount == 0:
            error = 1
            return error,times,v_code
        if v_code == '' or samount == 0:#活动期判断
            error = 1 #活动结束
        else:#活动期次数判断
            sql = """
                select coalesce(sum(1),0) sdays from qgpm_detail q inner join
                        qgsales_detail AS qd on q.m_id = qd.id
                     where v_code = '%s' and cid = %s and coalesce(q.cstatus,1) = 1
            """%(v_code,self.usr_id)
            t =  self.db.fetch(sql)
            sdays = int(t.get('sdays',0))

            if sdays >= dtimes:#
                error = 2 #已用完活动次数
            else:
                error = 0
                times = dtimes - sdays

            sql_et = """ select coalesce(sum(1),0) stime1 from qgpm_detail q inner join
                                qgsales_detail AS qd on q.m_id = qd.id
                             where v_code = '%s' and cid = %s and coalesce(q.cstatus,1) = 0 and q.etime >now()
            """%(v_code,self.usr_id)
            t1 =  self.db.fetch(sql_et)
            if t1.get('stime1',0) > 0:
                error = 11
            else:
                pass

        return error,times,v_code

    def yz_status(self,qqid):
        R = 0
        sql="""
            select 1 from qgpm_detail where coalesce(cstatus,0) = 1 and id = %s
        """%qqid
        L,iN = self.db.select(sql)
        if iN>0:
            R =1
        return R



