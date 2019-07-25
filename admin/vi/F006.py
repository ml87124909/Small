# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.vi.BASE_TPL

    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL import cBASE_TPL


class cF006(cBASE_TPL):

    def setClassName(self):
        #设定要实例的 BIZ类和TPL类，为空则继承基类，可以能过判断part的值来设置不同的类名
        self.dl_name = 'F006_dl'
        #self.inframe = 1


    def specialinit(self):
        self.navTitle = '红包查询'
        self.getBreadcrumb() #获取面包屑
        #self.isFile=1

    def goPartList(self):


        self.assign('NL',self.dl.GNL)

        self.assign('stime',self.dl.GP('stime',''))
        self.assign('etime',self.dl.GP('etime',''))

        ddzt = self.dl.GP('ddzt','')

        ddzt1=self.dl.getmtcdata('RZTCX',ddzt)

        self.assign('ddzt',ddzt1)
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        s = self.runApp('F006_list.html')
        return s

    def initPagiUrl(self):
        ddzt = self.REQUEST.get('ddzt','')
        qqid = self.REQUEST.get('qqid','')
        stime = self.REQUEST.get('stime','')
        etime = self.REQUEST.get('etime','')
        url = self.sUrl
        if stime:
            url += "&stime=%s"%stime
        if etime:
            url += "&etime=%s"%etime
        if qqid:
            url += "&qqid=%s" % qqid
        if ddzt:
            url += "&ddzt=%s" % ddzt
        return url

    def goPartExcel(self):
        import xlwt,random , md5 , mimetypes , os
        filename=xlwt.Workbook()
        sheet=filename.add_sheet("%s"%self.navTitle)
        txt_center = xlwt.XFStyle()
        txt_center.alignment.horz  = xlwt.Alignment.HORZ_CENTER
        txt_left = xlwt.XFStyle()
        txt_left.alignment.horz  = xlwt.Alignment.HORZ_LEFT
        txt_right = xlwt.XFStyle()
        txt_right.alignment.horz  = xlwt.Alignment.HORZ_RIGHT

        sheet.col(0).width = 256 * 20
        sheet.col(1).width = 256 * 20
        sheet.col(2).width = 256 * 20
        sheet.col(3).width = 256 * 20
        sheet.col(4).width = 256 * 20
        sheet.col(5).width = 256 * 20
        sheet.col(6).width = 256 * 20
        sheet.col(7).width = 256 * 20
        sheet.col(8).width = 256 * 20
        sheet.col(9).width = 256 * 20
        sheet.col(10).width = 256 * 20
        sheet.col(11).width = 256 * 20
        sheet.col(12).width = 256 * 20

        #第一行
        sheet.write(0,0,"红包单号",txt_center)
        sheet.write(0,1,"红包类型",txt_center)
        sheet.write(0,2,"货号",txt_center)
        sheet.write(0,3,"条码",txt_center)
        sheet.write(0,4,"红包名称",txt_center)
        sheet.write(0,5,"面值/价值",txt_center)
        sheet.write(0,6,"数量",txt_center)
        sheet.write(0,7,"会员姓名",txt_center)
        sheet.write(0,8,"会员卡号",txt_center)
        sheet.write(0,9,"电话号码",txt_center)
        sheet.write(0,10,"红包时间",txt_center)
        sheet.write(0,11,"过期时间",txt_center)
        sheet.write(0,12,"红包状态",txt_center)

        PL,L = self.dl.mRight()

        i = 0
        for e in L:
            sheet.write(i+1,0,e[0],txt_left)
            sheet.write(i+1,1,e[1],txt_left)
            sheet.write(i+1,2,e[2],txt_left)
            sheet.write(i+1,3,e[3],txt_center)
            sheet.write(i+1,4,e[4],txt_left)
            sheet.write(i+1,5,e[5],txt_right)
            sheet.write(i+1,6,e[6],txt_right)
            sheet.write(i+1,7,e[7],txt_left)
            sheet.write(i+1,8,e[8],txt_right)
            sheet.write(i+1,9,e[9],txt_center)
            sheet.write(i+1,10,str(e[10]),txt_center)
            sheet.write(i+1,11,str(e[11]),txt_center)
            if e[12] == 1:
                e10 = "已使用"
            elif e[12] == 2:
                e10 = "已过期"
            else:
                e10 = "未使用"
            sheet.write(i+1,12,e10,txt_center)
            i+=1

        filePATH = r"D:/webpy/data/hjnwx/excel/%s.xls" %(md5.md5("%s" % random.random()).hexdigest())
        filename.save(filePATH)

        from flask import make_response
        file = open(filePATH,'rb').read()
        response = make_response(file)
        response.headers['content-type'] = mimetypes.guess_type(filePATH)[0]
        response.headers['content-length'] = os.stat(filePATH)[6]

        filename="%s%s.xls" % (self.navTitle,self.dl.getdate)
        response.headers['Content-Disposition'] = "attachment; filename=%s"%filename.encode("gbk")
        os.remove(filePATH)
        return response