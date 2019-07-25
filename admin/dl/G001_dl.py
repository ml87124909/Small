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
import hashlib , os , time , random

class cG001_dl(cBASE_DL):
    #在子类中重新定义         
    def myInit(self):
        self.src = 'G001'
        pass

    def getInfo(self):

        info  =  self.db.fetch("""
        select max_cash,mini_cash,arrive,topup,topup_str,drawal,drawal_str from topup_set where usr_id = %s
        """ ,self.usr_id_p)
        return info

    def local_add_save(self):
        dR={'R':'','MSG':'保存成功','B':'1','isadd':'','furl':''}
        arrive = self.GP('arrive','')
        mini_cash = self.GP('mini_cash','')
        topup = self.GP('topup', '')
        topup_str = self.GP('topup_str', '')
        drawal = self.GP('drawal', '')
        drawal_str = self.GP('drawal_str', '')


        data = {
            'arrive' : arrive or None,
            'mini_cash':mini_cash,
            'topup':topup or None,
            'topup_str':topup_str,
            'drawal':drawal or None,
            'drawal_str':drawal_str
        }
        l, t = self.db.select("select id from topup_set where usr_id =%s;" ,self.usr_id_p)
        if t==0:
            data['usr_id']=self.usr_id_p
            data['cid'] = self.usr_id
            data['ctime'] = self.getToday(9)
            self.db.insert('topup_set',data)
        else:
            data['uid'] = self.usr_id
            data['utime'] = self.getToday(9)
            self.db.update('topup_set',data,'usr_id=%s'%self.usr_id_p)

        self.save_top_set()
        self.oSHOP.update(self.usr_id_p)

        return dR

    def save_top_set(self):
        lid = self.REQUEST.getlist('lid')
        add_money = self.REQUEST.getlist('add_money')  # 充值金额
        giving = self.REQUEST.getlist('giving')  # 赠送金额


        if len(add_money) > 0:
            sql = "select id from gifts where usr_id=%s;"
            l, t = self.db.select(sql, self.usr_id_p)
            if t > 0:
                for j in l:
                    if str(j[0]) not in lid:
                        self.db.query("delete from  gifts where id=%s and usr_id=%s;", [j[0],self.usr_id_p])
            for i in range(len(add_money)):
                if add_money[i] != '':
                    if lid[i] == '':
                        sql = """
                                    insert into gifts(usr_id,add_money,giving,cid,ctime)
                                        values(%s,%s,%s,%s,now());
                                    """
                        L = [self.usr_id_p, add_money[i] or None, giving[i] or None, self.usr_id]
                        self.db.query(sql, L)
                    else:
                        sql = """
                                    update gifts set add_money=%s,giving=%s,uid=%s,utime=now()
                                            where id=%s
                                    """
                        L = [add_money[i] or None, giving[i] or None,  self.usr_id, lid[i]]
                        self.db.query(sql, L)
        else:
            self.db.query("delete from  gifts where usr_id=%s;", self.usr_id_p)
        return

    def get_gifts(self):
        sql="select id,add_money,giving from gifts where usr_id=%s"
        l,t=self.db.fetchall(sql,self.usr_id_p)
        return l


