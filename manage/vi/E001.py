# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/E001.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL
import time, os,xlsxwriter
from flask import make_response
from io import BytesIO

class cE001(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'E001_dl'


    def specialinit(self):
        self.tab_data = ['全部', '待付款', '待发货', '部分发货', '待收货', '待自提', '已完成', '已取消']
        self.assign('tab_data', self.tab_data)
        self.assign('tab', self.dl.tab)

    def initPagiUrl(self):
        qqid = self.dl.GP('qqid', '')
        ctype = self.dl.GP('ctype', '')
        url = self.sUrl

        if self.dl.tab:
            url += "&tab=%s" % self.dl.tab
        if qqid:
            url += "&qqid=%s" % qqid
        if ctype:
            url += "&ctype=%s" % ctype

        return url

    def goPartList(self):
        self.currentUrl = self.sUrl  # + "&part=list"
        self.assign('currentUrl', self.currentUrl)
        self.assign('NL',self.dl.GNL)
        PL,L = self.dl.mRight()
        self.navTitle = '订单管理'
        self.getBreadcrumb()  # 获取面包屑
        self.assign('dataList',L)
        self.assign('ctype',self.dl.GP('ctype','0'))
        self.assign('sdate', self.dl.GP('sdate', ''))
        self.assign('edate', self.dl.GP('edate', ''))
        self.assign('status', self.dl.GP('status', ''))
        self.getPagination(PL)
        s = self.runApp('E001_list.html')
        return s

    
    def goPartLocalfrm(self):

        self.need_editor = 1
        self.initHiddenLocal()#初始隐藏域
        self.navTitle = '订单详情'
        self.getBreadcrumb()  # 获取面包屑
        self.getBackBtn()
        item = self.dl.get_local_data()
        self.assign('item',item)
        self.assign('NL', self.dl.GNL2)
        s = self.runApp('E001_local.html')
        return s

    def goPartOrder_status(self):
        dR=self.dl.order_status_data()
        return self.jsons(dR)

    def goPartEdit_price(self):
        dR=self.dl.edit_price_data()
        return self.jsons(dR)


    def goPartPay_order_pay(self):
        dR=self.dl.Pay_order_pay_data()
        return self.jsons(dR)

    def goPartPay_order_status(self):
        dR=self.dl.pay_order_status_data()
        return self.jsons(dR)

    def goPartClose_order(self):
        dR = self.dl.close_order_data()
        return self.jsons(dR)

    def goPartOrder_shipments(self):
        dR=self.dl.order_shipments_data()
        return self.jsons(dR)

    def goPartOrder_shipment(self):
        dR=self.dl.order_shipment_detail()
        return self.jsons(dR)

    def goPartorder_after(self):#核销
        dR=self.dl.order_after_data()
        return self.jsons(dR)

    def goPartEditmemo(self):
        dR = self.dl.editmemo_data()
        return self.jsons(dR)

    def goPartExcel_import(self):
        dR = self.dl.excel_import()
        return self.jsons(dR)

    def goPartorder_refund(self):
        dR = self.dl.order_refund_data()
        return self.jsons(dR)

    def goPartExcel(self):


        L = self.dl.export_excel_data()

        NL = ['收件人昵称', '收件人姓名', '收件人手机','省', '市', '区', '详细地址', '邮政编码', '运费',
              '支付类型', '订单号', '商品名称',
              ]

        sa = time.time()
        s1 = 'send_%s' % sa
        sio = BytesIO()
        workbook = xlsxwriter.Workbook(sio)
        worksheet = workbook.add_worksheet(u'%s' % s1)

        # format = workbook.add_format({'bold': True, 'font_color': 'red'})
        format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#e0e0e0'})
        format.set_align('center')

        format1 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#e0e0e0'})
        format1.set_align('left')

        format2 = workbook.add_format()
        format2.set_align('center')

        format3 = workbook.add_format()
        format3.set_align('left')

        for row in range(len(NL)):
            worksheet.write(0, row, NL[row], format)
            #worksheet.set_column(row, row, NL[row] / 7)

        s, i = '', 0
        for e in L:
            j = 0
            for a in e:
                if j == 11:
                    for r in a:
                        s += r['good_name'] + ','

                    worksheet.write(i + 1, j, s, format3)
                else:
                    worksheet.write(i + 1, j, a, format2)
                j = j + 1
            i = i + 1

        workbook.close()

        response = make_response(sio.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=%s.xlsx;" % s1

        return response

    def goPartAllexcel(self):

        L = self.dl.allexcel_data()

        NL = ['收件人昵称', '收件人姓名', '收件人手机', '省', '市', '区', '详细地址', '邮政编码', '运费',
              '支付类型', '订单号', '状态', '商品名称'
              ]

        sa = time.time()
        s1 = 'AllExcel_%s_%s' % (self.dl.tab, sa)
        sio = BytesIO()
        workbook = xlsxwriter.Workbook(sio)
        worksheet = workbook.add_worksheet(u'%s' % s1)

        # format = workbook.add_format({'bold': True, 'font_color': 'red'})
        format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#e0e0e0'})
        format.set_align('center')

        format1 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#e0e0e0'})
        format1.set_align('left')

        format2 = workbook.add_format()
        format2.set_align('center')

        format3 = workbook.add_format()
        format3.set_align('left')

        for row in range(len(NL)):
            worksheet.write(0, row, NL[row], format)
            # worksheet.set_column(row, row, NL[row] / 7)

        s, i = '', 0
        for e in L:
            j = 0
            for a in e:
                if j == 12:
                    for r in a:
                        s += r['good_name'] + '(' + r['property_str'] + ')' + ','

                    worksheet.write(i + 1, j, s, format3)
                else:
                    worksheet.write(i + 1, j, a, format2)
                j = j + 1
            i = i + 1

        workbook.close()

        response = make_response(sio.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=%s.xlsx;" % s1

        return response


    def goPartExcel_(self):

        L = self.dl.export_excel_data()
        NL = ['shonjianrennicheng', 'shoujianrenxingming', 'shoujianrenshouji',
              'sheng', 'shi', 'qu', 'xiangxidizhi', 'youzhengbianma', 'youfei',
              'zhifuleibie', 'shangpingmingcheng',
              ]

        # 生成报表的数据比较多且是不定长的，为了减少py为变量oT重复申请内存地址而无谓地消耗时间，这里把数据先写到磁盘，然后再从磁盘读取数据，从而提高py处理效率
        self.make_sub_path('/var/data_h/%s/' % self.dl.usr_id)
        fname = r'/var/data_h/%s/%s_%s.xls' % (self.dl.usr_id, self.dl.usr_id, time.time())
        f = open(fname, 'w')

        GW = [200] * len(NL)
        GA = ['CENTER'] * len(NL)


        oT = self.Html.table(
            {"width": "100%", "align": "center", "bgcolor": "white", "valign": "top", 'cellpadding': "0",
             'cellspacing': "0", 'border': 1, 'style': 'border-collapse:collapse'})

        f.write('<table %s>' % oT.args)

        oTR = self.Html.tr()
        for n in range(len(NL)):
            oTR.add(self.Html.td(NL[n], {'width': GW[n], 'align': GA[n], 'bgcolor': '#e0e0e0'}))
            #oTR.add(self.Html.td(NL[n].encode('utf-8'), {'width': GW[n], 'align': GA[n], 'bgcolor': '#e0e0e0'}))
            # a = NL[n].encode('utf-8')
            #a = NL[n].decode("utf-8")
            #oTR.add(self.Html.td(a, {'width': GW[n], 'align': GA[n], 'bgcolor': '#e0e0e0'}))
        f.write(oTR.getHTML())

        n = 0
        for e in L:
            oTR = self.Html.tr()
            i = 0
            for j in range(len(e)):
                if i == 10:
                    s = ''
                    for r in e[j]:
                        s += r['good_name'] + ','
                else:
                    if e[j] is None or e[j] == '':
                        s = '&nbsp;'
                    else:
                        s = e[j]
                        # if i in (10,8,9):
                        #     total[i-1] += float(e[i])
                oTR.add(self.Html.td(s, {'align': 'center', 'style': 'vnd.ms-excel.numberformat:@'}))

                i = i + 1

            f.write(oTR.getHTML())
            n += 1

        f.write('</TABLE>')
        f.flush()
        f.close()

        f = open(fname, 'r')
        s = f.read()
        f.close()
        try:
            os.remove(fname)
        except:
            pass
        sa = time.time()
        s1 = 'Send_the_goods_%s' % sa
        # print(type(s1))
        # s1 = s1.encode('utf-8')
        # s1 = s1.encode('gbk')
        # s1=s1.decode('gbk')

        response = make_response(s)
        response.headers["Content-Disposition"] = "attachment; filename=%s.xls;" % s1
        return response

    def doWebExcel(self):
        import time
        L = self.biz.local_ajax_getLocalData()
        NL = self.biz.GNL2
        iW = 100 * len(NL)
        fname = r'd:\%s_%s.xls' % (self.biz.usr_id,
                                   time.time())  # 生成报表的数据比较多且是不定长的，为了减少py为变量oT重复申请内存地址而无谓地消耗时间，这里把数据先写到磁盘，然后再从磁盘读取数据，从而提高py处理效率
        f = open(fname, 'w')

        GW = [100] * len(NL)  # ['28','142','80','90','60','80','80','90','90','90','90','90','90','120','60']
        GA = ['CENTER'] * len(
            NL)  # ['CENTER','LEFT','CENTER','RIGHT','CENTER','CENTER','CENTER','RIGHT','RIGHT','RIGHT','RIGHT','RIGHT','RIGHT','RIGHT','CENTER']
        total = [0] * len(NL)
        oT = self.Html.table(
            {"width": "100%", "align": "center", "bgcolor": "white", "valign": "top", 'border': "0",
             'cellpadding': "0", 'cellspacing': "0", 'border': 1, 'style': 'border-collapse:collapse'})
        # oT=cTABLE(iW,'','','','','',1,0,0)
        f.write('<table %s>' % oT.args)

        # oTR=cTR()
        oTR = self.Html.tr()
        for n in range(len(NL)):
            oTR.add(self.Html.td(NL[n]['display'], {'width': GW[n], 'align': GA[n], 'bgcolor': '#e0e0e0'}))
            # oTR.add(TD(GW[n],'',NL[n],GA[n],'',dSTY['C3'],'','','GMTD'))
        oT.add(oTR)
        f.write(oTR.getHTML())

        n = 0
        for e in L:
            oTR = self.Html.tr()
            for i in range(len(e)):
                if e[i] is None or e[i] == '':
                    s = '&nbsp;'
                else:
                    s = e[i]
                    if i in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]:
                        total[i] += float(e[i].replace(',', ''))
                oTR.add(self.Html.td(s, {'width': GW[i], 'align': GA[i]}))
                # oTR.add(TD(GW[i],'',s,GA[i],'','','','','GITD'))
            oT.add(oTR)
            f.write(oTR.getHTML())
            n += 1

        oTR = self.Html.tr()
        oTR.add(self.Html.td('合计', {'width': GW[0], 'align': GA[0]}))
        # oTR.add(TD(GW[0],'','合计：',GA[0],'','','','','GITD'))
        for i in range(1, len(total)):
            if total[i] == 0:
                total[i] = '&nbsp;'
            else:
                total[i] = 0  #myRound(total[i], 2)
            oTR.add(self.Html.td(total[i], {'width': GW[i], 'align': GA[i]}))
            # oTR.add(TD(GW[i],'',total[i],GA[i],'','','','','GITD'))
        oT.add(oTR)
        f.write(oTR.getHTML())
        f.write('</TABLE>')
        f.flush()
        f.close()

        f = open(fname, 'r')
        s = f.read()
        f.close()
        try:
            os.remove(fname)
        except:
            pass
        s1 = '摘：'
        DateType = self.biz.GP('DateType', '1')
        InvType = self.biz.GP('InvType', '')
        if str(DateType) != '':
            if str(DateType) == '1':
                s1 += '录入日期'
            elif str(DateType) == '2':
                s1 += '开票日期'

            if self.s_time != '' and self.e_time != '':
                s1 += '从 %s 到 %s' % (self.s_time, self.e_time)
            elif self.s_time != '' and self.e_time == '':
                s1 += '为 %s 之后' % self.s_time
            elif self.s_time == '' and self.e_time != '':
                s1 += '为 % 之前'

        if str(InvType) == '1':
            s1 += '的工程发票数据'
        elif str(InvType) == '2':
            s1 += '的劳务发票数据'
        # s1=s1.encode('utf-8')
        s1 = s1.encode('GBK')
        #        self.objHandle.headers.set('Content-Disposition', "attachment; filename=%s"% filename)

        response = make_response(s)
        response.headers["Content-Disposition"] = "attachment; filename=%s.xls;" % s1
        return response

    def doWebExcel_(self):
        import time, xlsxwriter, StringIO

        L = self.biz.mRight()
        NL = self.biz.GNL

        sa = time.time()
        s1 = '项目费用明细报表%s' % sa
        sio = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(sio)
        worksheet = workbook.add_worksheet(u'%s' % s1)

        # format = workbook.add_format({'bold': True, 'font_color': 'red'})
        format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#e0e0e0'})
        format.set_align('center')

        format1 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#e0e0e0'})
        format1.set_align('left')

        format2 = workbook.add_format()
        format2.set_align('center')

        format3 = workbook.add_format()
        format3.set_align('left')

        for row in range(len(NL)):
            if row == 12:
                worksheet.write(0, row, NL[row]['display'], format1)
            else:
                worksheet.write(0, row, NL[row]['display'], format)
            worksheet.set_column(row, row, NL[row]['width'] / 7)

        s, i = 0, 0
        for e in L:
            j = 0
            for a in e:
                if j == 12:
                    s = s + float(a.replace(',', ''))
                    worksheet.write(i + 1, j, a, format3)
                else:
                    worksheet.write(i + 1, j, a, format2)
                j = j + 1
            i = i + 1
        worksheet.write(i + 1, 0, '合计', format)
        worksheet.write(i + 1, 12, '%s' % s)

        #        money_format = workbook.add_format({'num_format': '#,##0.00'})
        #        r,c=1,0
        #        for e in L:
        #            if c==12:
        #                worksheet.write_column(r, c, e, money_format)
        #            else:
        #                worksheet.write_column(r, c, e, format3)
        #            c+=1
        #        if len(L)>0:
        #            worksheet.write(len(L[0])+1, 0, '合计', format3)
        #            worksheet.write(len(L[0])+1, 12, '=SUM(M2:M%s)'%(len(L[0])+1), money_format)
        #

        workbook.close()

        s1 = s1.encode('GBK')
        response = make_response(sio.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=%s.xlsx;" % s1

        return response


