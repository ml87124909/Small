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

import os


class cH001(cVI_BASE):

    def specialinit(self):

        if self.GP('ared'):
            self.part = "addred"
            self.assign("site_title","领取红包")
        elif self.GP('local'):
            self.part = "localfrom"
            self.assign("site_title","我的红包")
        elif self.GP('detail'):
            self.part = "detail"
            self.assign("site_title","我的红包")
        else:
            self.assign("site_title","领取红包")

    def goPartMenu(self):
        dict = {'status':0,'times':0,'memo':''}
        errors,times = self.get_my_redtimes()
        rvtype = 0
        if errors == 1:#活动结束
            status = 9
        elif errors == 0:
            status = 1
        else:
            status = errors

        if status == 9:#活动结束
            sql = '''
               select  coalesce(memo,'') memo from redsales where coalesce(memo,'')!= ''
               order by csetime desc limit 1
            '''
        else:
            sql = '''
               select  coalesce(memo,'') memo from redsales where coalesce(cstatus,0) = 1 limit 1
            '''
        item = self.db.fetch(sql)
        memo = item.get('memo','').replace('\r\n',r'<br>')
        sql_all = """
            select coalesce(SUM(coalesce(samount,0)),0) samount
                from redsale_detail rd inner join
                redsales r ON rd.v_code = r.v_code
                where coalesce(cstatus,0) = 1
        """
        am = self.db.fetchcolumn(sql_all)
        if am <= 0:#红包已领取完
            status = 10
            times = 0

        dict['cstatus'] = status
        dict['times'] = times
        dict['memo'] = memo
        self.assign("item",dict)
        self.assign("rvtype",rvtype)
        #测试显示
        self.assign('mvipcode',item.get('vipcode',0))
        #
        return self.display('H001.html')

    def goPartDetail(self):
        srfid = self.GP('srfid','')
        if str(srfid) == '1':
            srfid = 'H001'
        else:
            srfid = 'home'
        searchText=self.GP('searchText','')
        sql='''
            SELECT
                r.code,
                r.cname,
                r.amount,
                CASE WHEN r.vtype = 233 and coalesce(r.cstatus,0) = 1 THEN '已充值'
                 WHEN r.vtype = 233 and coalesce(r.cstatus,0) = 0 THEN '充值中'
                 WHEN r.vtype = 232 and coalesce(r.cstatus,0) = 0 and r.edtime::timestamp < now() THEN '已过期'
                 WHEN r.vtype = 232 and coalesce(r.cstatus,0) = 0 and r.edtime::timestamp > now() THEN '未领取'
                 WHEN r.vtype = 232 and coalesce(r.cstatus,0) = 1 THEN '已领取'
                 WHEN r.vtype = 231 AND coalesce(r.cstatus,0) = 1 THEN '已使用'
                 WHEN r.vtype = 231 AND coalesce(r.cstatus,0) = 0 AND r.edtime::timestamp < now() THEN '已过期'
                 WHEN r.vtype = 231 AND coalesce(r.cstatus,0) = 0 AND r.edtime::timestamp > now() THEN '未使用'
                ELSE '无效' END cstatus
            FROM v_reddetail r
            where  coalesce(r.cstatus,0) !=3 AND r.item_id != -10000 AND r.cid=%s
            and  (coalesce(r.cstatus,0) = 1 or (coalesce(r.cstatus,0) = 0 and date_part('day', r.edtime::timestamp -now()) < 3 ))
        '''%self.usr_id    ######3天数据过期不显示
        if searchText != '':
            sql+="""
                and (r.cname like '%%%s%%' or r.code like '%%%s%%')
            """%(searchText,searchText)
        sql+=""" order by r.ctime desc """
        #print(sql)
        l,n=self.db.fetchall(sql)
        self.assign('datalist',l)
        self.assign("srfid",srfid)
        return self.display('H001_detail.html')

    def goPartLocalfrom(self):
        from hubarcode.code128 import Code128Encoder
        ATTACH_ROOT = share.dINI['ATTACH_ROOT']
        tmpath = os.path.join(ATTACH_ROOT,'tm')
        code=self.GP('code','0') or 0

        sql_z = """
            select coalesce(cstatus,0) cstatus from reddetail where code = '%s'
        """% code
        Lz= self.db.fetch(sql_z)
        cstatus = Lz.get('cstatus',0)
        sql = """
            SELECT top 1
                h.item_id,
                h.tm,
                o.cname,
                ABS(o.price) price,
                o.amount,
                coalesce(mt.txt1,'张') dw,
                h.pic,
                case when o.item_id = -10000 then 1
                when o.vtype = 233 then 1
                else (case when o.edtime < now()  then 1 else coalesce(o.cstatus,0) end)
                end cstatus,
                o.vtype,
                 case when o.vtype = 231 and o.edays > 0 then to_char(edtime,'YYYY-MM-DD HH24:mm:ss') else to_char(edtime,'YYYY-MM-DD HH24:mm:ss') end edtime,
                 CASE WHEN o.vtype = 233 and coalesce(o.cstatus,0) = 1 THEN '（已充值）'
                 WHEN o.vtype = 233 and coalesce(o.cstatus,0) = 0 THEN '（充值中）'
                 WHEN o.vtype = 232 and coalesce(o.cstatus,0) = 0 and o.edtime < now() THEN '（已过期）'
                 WHEN o.vtype = 232 and coalesce(o.cstatus,0) = 0 and o.edtime > now() THEN '（未领取）'
                 WHEN o.vtype = 232 and coalesce(o.cstatus,0) = 1 THEN '（已领取）'
                 WHEN o.vtype = 231 AND coalesce(o.cstatus,0) = 1 THEN '（已使用）'
                 WHEN o.vtype = 231 AND coalesce(o.cstatus,0) = 0 AND o.edtime < now() THEN '（已过期）'
                 WHEN o.vtype = 231 AND coalesce(o.cstatus,0) = 0 AND o.edtime > now() THEN '（未使用）'
                ELSE '（无效）' END icstatus
            from v_reddetail o
            left join hd_item_info h(nolock) on h.item_id=o.item_id
            LEFT JOIN mtc_t AS mt ON mt.[type] = 'DW' AND mt.id = h.unit
            where o.code='%s' and o.cid = %s
        """ % (code,self.usr_id)
        L= self.db.fetch( sql )
        self.assign('code',code)
        self.assign('cstatus',cstatus)
        self.assign('item',L)
        encoder = Code128Encoder(code,options={"ttf_font":"C:/Windows/Fonts/SimHei.ttf","ttf_fontsize":13,"bottom_border":0,"height":90,"label_border":3})
        mytm = os.path.join(tmpath,"%s.png"%code)
        encoder.save(mytm,bar_width=2)

        #判断订单是否可以自主取消
        order_status=self.get_order_status(code)
        return self.display('H001_local.html')

    def goPartAddred(self):
        error = 0
        times = 0
        msg = ''
        yz = self.db.fetch("select v_code st from redsales where coalesce(cstatus,0)=1 and btime<now() limit 1")
        v_code = yz.get('st','')
        if v_code == '':
            return self.jsons({'error':10,'msg':'活动敬请期待...','times':times})
        try:
            errors,times = self.get_my_redtimes()
            if errors == 1:#活动已结束
                error = 4
                msg = '活动已结束...'
                return self.jsons({'error':error,'msg':str(msg),'times':times})
            elif errors == 2:#本次活动红包已领完
                error = 5
                msg = '您本次活动红包已领完...'
                return self.jsons({'error':error,'msg':str(msg),'times':times})
            elif errors == 3:#今天红包已领完
                error = 6
                msg = '您今天红包已领完...'
                return self.jsons({'error':error,'msg':str(msg),'times':times})
            else:
                pass
            code = self.Get_New_Code('R',6,0)
            ###红包抽奖开始###
            I,iN = self.db.select("""select * from myredbag('%s');"""%yz.get('st',''))
            if iN >0:
                id = int(I[0][0])
                sql = """
                    select  rd.vtype,rd.vcname,rd.price,
                        CASE WHEN  r.edays > 0  then
                        	convert(varchar(10),GETDATE()+coalesce(r.edays,0)-1,121)
                        	else convert(varchar(10),r.edtime,121) end edtime 
                    from redsale_detail rd
                     left join redsales AS r on rd.v_code = r.v_code where rd.id = %s limit 1
                """%(id)
                L = self.db.fetch(sql)
                vtype = L.get('vtype',0)
                vcname = L.get('vcname','')
                price = L.get('price',0)
                edtime = L.get('edtime','')

                if id == 0:
                    vtype = 0
                    gid = 0
                    vcname = '谢谢参与'
                data = {
                    'code':code,
                    'm_id':id,
                    'vtype':vtype,
                    'cname':vcname,
                    'amount':1,
                    'price':price,
                    'cid':self.usr_id,
                    'ctime':self.getToday(9),
                    'cstatus':0
                    }
                # if str(item_id) == '-10000' or id == 0:
                #     data['cstatus'] = 1
                #     data['wtime'] = self.getToday(9)
                self.db.insert('reddetail',data)
                dtime = '活动'
                if edtime != '':
                    jt = str(edtime).split('-')
                    dtime = str(jt[0])+'年'+str(jt[1])+'月'+str(jt[2])+'日'

                #if str(item_id) == '-10000' or id == 0:
                if id == 0:
                    error = 1
                    msg = '谢谢参与'
                # elif str(vtype) == '233' and str(item_id) != '-10000':
                #     if vcname == '':
                #         msg = '领到储值 '+str(price)+' 元'
                #     else:
                #         msg = str(vcname)
                #     msg += '，请稍后查询您的储值'
                #elif str(vtype) == '231':
                #    msg = '获得 '+str(vcname)+' ，请在'+str(dtime)+'前在店铺使用'
                else:
                    msg = '获得 '+str(vcname)+' ，请在'+str(dtime)+'前到店使用' #20180305 MINZ
            else:
                error = 1
                msg = '谢谢参与'
            ###红包抽奖结束###
            ###红包抽没抽中 都要插入到记录抽奖次数中###
            sql_t = """
                insert into red_times(v_code,daytimes,cid,ctime)
                values ('%s',1,%s,getdate())
            """%(v_code,self.usr_id)
            self.db.query(sql_t)
            ##记录结束
            times = times - 1
        except Exception as  ex:
            error = 3
            msg = '活动已停止...'
        return self.jsons({'error':error,'msg':str(msg),'times':times})

    def get_my_redtimes(self):
        times = 0
        error = 0
        yz_sql="""select v_code st,
                        extract(epoch FROM (now()-endtime))etime,
                        coalesce(daytimes,0) dtimes,
                        coalesce(maxdaytimes,0) mtimes
                      from redsales where coalesce(cstatus,0) = 1  and btime < now() limit 1"""
        yz = self.db.fetch(yz_sql)
        v_code = yz.get('st','')
        etime = int(yz.get('etime',0))
        dtimes = int(yz.get('dtimes',0))
        mtimes = int(yz.get('mtimes',0))

        sam = self.db.fetch("""SELECT SUM(coalesce(samount,0)) samount FROM redsale_detail AS rd INNER JOIN redsales AS r
                on rd.v_code = r.v_code WHERE r.cstatus = 1""")
        samount = sam.get('samount','')
        if int(samount) == 0:
            error = 1
            return error,times
        if v_code == '' or etime >= 0:#活动期判断
            error = 1 #红包活动结束
        else:#活动期次数判断
            sql = """
                select coalesce(sum(daytimes),0) sdays from red_times where v_code = '%s' and cid = %s
            """%(v_code,self.usr_id)
            t =  self.db.fetch(sql)
            sdays = int(t.get('sdays',0))

            if sdays >= mtimes and mtimes != 0:#
                error = 2 #红包领取已领完
            else:
                if mtimes <=dtimes and mtimes !=0 :#最大小于每天次数
                    dtimes = mtimes
                sql_d = """
                        select coalesce(sum(daytimes),0) ddays from red_times where v_code = '%s' and cid = %s
                        and now()::date-ctime::date = 0
                """%(v_code,self.usr_id)
                d = self.db.fetch(sql_d)
                ddays = int(d.get('ddays',0))

                if ddays >= dtimes:
                    error = 3 #红包今天领取次数已到
                elif ddays >=mtimes and mtimes != 0:
                    error = 2 #红包领取已领完
                else:
                    error = 0
                    ##还有领取次数 但是还有优惠券未用未过期 就判断为未使用还可领取，应使用完才可继续领##
                    sql_xz = """
                        SELECT  1 FROM v_reddetail AS r
                        WHERE coalesce(r.cstatus,0) = 0 
                        AND extract(day FROM (age(r.ctime::date , now()::date))) > 0
                        AND r.edtime::timestamp > now()  
                        and r.cid = %s and r.v_code = '%s' and r.edays >0
                    """%(self.usr_id,v_code)

                    it,iN = self.db.select(sql_xz)
                    if iN>0:
                        error = 11
                    times = dtimes - ddays
        self.print_log('%s,%s'%(error,times), '抢红包')
        return error,times





