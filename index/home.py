# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG=='1':
    import index.VI_BASE
    reload(index.VI_BASE)
from index.VI_BASE             import cVI_BASE


class chome(cVI_BASE):

    def specialinit(self):
        self.assign("site_title","简道平台商城")

    def goPartMenu(self):
        if self.usr_id == 0:
            self.assign("usr_id","0")
            self.assign("usr_type",0)
            self.assign("dlset",0)
        else:
            usr_type = self.db.fetchcolumn('select usr_type from users where usr_id = %s'%self.usr_id)
            self.assign("usr_type",usr_type)
            self.assign("dlset",1)

#        menu_data=self.menu_data()
        
        sql = """
              select  gs.id
                   ,'' as cname --hii.cname
                   ,'' as item_id--hii.item_id
                   ,'' as price --hii.hy_price price
                   ,'' as fext --hii.pic fext
                   ,coalesce(gs.amount,0) amount
                   from goodsale gs
                   --inner join hd_item_info hii on gs.item_id = hii.item_id
              WHERE gs.cstatus = 1 and gs.btime <=now() and gs.etime>=now()
             and (coalesce(gs.xs_type,1) = 1 or coalesce(gs.xs_type,1) = 0) limit 50
         """
        L,t = self.db.fetchall(sql)
        self.assign('item',L)
        #self.smarty.assign("menu_data",menu_data)
        self.assign('myvip',0)
        
        return self.display('home.html')

    def menu_data(self):
        sql='''
            select
                a.id,
                a.sort,
                a.cname,
                a.link,
                case when isnull(a.logo,'')!='' then 'resource/attachment/'+a.logo else a.logo end as logo,
                a.color,
                a.bgcolor,
                case when isnull(a.bgimage,'')!='' then 'resource/attachment/'+a.bgimage else a.bgimage end as bgimage,
                a.memo
            from menu_index a(nolock)
            where a.status=1
        '''
        l,n=self.db.fetchall(sql)
        L = {}
        for e in l:
            L[e.get('sort')] = e
        return L