# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/C004.py"""

from imp import reload
from basic.publicw import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL


class cC004(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'C004_dl'

    def specialinit(self):
        pass

    def initPagiUrl(self):
        qqid = self.REQUEST.get('qqid','')
        url = self.sUrl
        if qqid:
            url += "&qqid=%s" % qqid
        return url

    def goPartList(self):
        self.getBreadcrumb()  # 获取面包屑
        self.assign('NL',self.dl.GNL)
        PL,L = self.dl.mRight()
        self.assign('dataList',L)
        self.getPagination(PL)
        self.assign('sorting', self.dl.sorting)
        s = self.runApp('C004_list.html')
        return s
    
    def goPartLocalfrm(self):
        self.getBreadcrumb()  # 获取面包屑
        self.navTitle = ''
        self.need_editor = 1
        self.initHiddenLocal()#初始隐藏域
        self.getBackBtn()
        item = self.dl.get_local_data()
        if self.pk!='':
            category_list=self.dl.category_list_pk(self.pk)
        else:
            category_list = self.dl.category_list()
        L_p, L_c=self.dl.get_spec_data(self.pk)
        # print(L_p, L_c)
        spec_all = ','.join(str(i) for i in L_p)
        spec_amount = len(L_p)
        spec_childx = {}
        for j in L_p:
            kstr = ''
            for k in L_c:
                if j == k[0]:
                    if kstr == '':
                        kstr += str(k[1])
                    else:
                        kstr += ',' + str(k[1])
            spec_childx[str(j)] = kstr
        self.assign({'item':item,

                     'spec_child_price':self.dl.spec_child_price(self.pk),  #商品规格价格对应数据
                     'category_list':category_list,  #商品分类
                     'pics_list':self.dl.pics_list(self.pk),  #图片列表
                     'spec_list':self.dl.spec_list(),  #商品规格
                    'spec_child_list': self.dl.spec_child_list(),  #商品规格子属性
                    'hy_level':self.dl.get_hy_up_level(),  #会员级别
                     'L_p': L_p, 'L_c': L_c, 'spec_all': spec_all, 'spec_amount': spec_amount,
                     'spec_childx': spec_childx,
                     #'Discount_list':self.dl.Discount_list(self.pk),  #单独会员折扣
                     'show_ticket': self.show_ticket(),
                     'show_spec': self.Spec_mselect_child()
                     })

       
        s = self.runApp('C004_local.html')
        return s


    def goPartAddids(self):
        ids=self.dl.GP('ids','')
        pk = self.dl.GP('pk','')
        l=self.dl.get_ids(ids)
        p = self.dl.get_property(ids)

        M=[]
        for i in p:
            for j in l:
                if i[0]==j[0]:
                    A=str(i[0])+':'+str(j[1])+','
                    B = i[1] + '(' + j[2] + ')'
                    M.append([B,A])

        d=''
        L=self.dl.get_gg(pk)

        for k in M:
            if len(L)>0:
                for v in L:
                    if v[0]==k[0]:
                        d+='<div class="row">%s<input type="hidden" name="ggname" value="%s"><input type="hidden" name="property_child_ids" value="%s"><div class="col-sm-12 ">'%(v[0],v[0],v[1])
                        d+='原价:<input type="text" name="originalpriceext" style="width:60px;" value="%s">'%v[2]
                        d+='现价:<input type="text" name="minpriceext" style="width:60px;" value="%s">'%v[3]
                        d+= '拼团价:<input type="text" name="ptpriceext" style="width:60px;" value="%s">'%v[4]
                        d+='会员价:<input type="text" name="hypriceext" style="width:60px;" value="%s">'%v[7]
                        d += '积分:<input type="text" name="scoreext" style="width:60px;" value="%s">' % v[5]
                        d+='库存数:<input type="text" name="storesext" style="width:60px;" value="%s">'%v[6]
                        d+='</div></div><br>'
            else:
                d += '<div class="row">%s<input type="hidden" name="ggname" value="%s"><input type="hidden" name="property_child_ids" value="%s"><div class="col-sm-12 ">' % (k[0],k[0], k[1])
                d += '原价:<input type="text" name="originalpriceext" style="width:60px;" value="0">'
                d += '现价:<input type="text" name="minpriceext" style="width:60px;" value="0">'
                d += '拼团价:<input type="text" name="ptpriceext" style="width:60px;" value="0">'
                d += '会员价:<input type="text" name="hypriceext" style="width:60px;" value="0">'
                d += '积分:<input type="text" name="scoreext" style="width:60px;" value="0">'
                d += '库存数:<input type="text" name="storesext" style="width:60px;" value="0">'
                d += '</div></div><br>'

        return d

    def goPartAddsel(self):

        ids = self.dl.GP('ids', '')
        idsn = self.dl.GP('idsn', '')
        d = ''
        try:
            int(ids)
            l = self.dl.get_property_no(ids)
        except:
            return d
        try:
            a=int(idsn)
        except:
            a=''

        if len(l)>0:
            d+='<select class ="form-control" onchange="property_sel2()"  name="property_seln" >'
            for k in l:
                if a==k[0]:
                    d += '<option value="%s" selected="selected">%s</option>' % (k[0], k[1])
                else:
                    d+='<option value="%s">%s</option>'%(k[0],k[1])
            d += '</select>'

        return d

    def goPartAddidsnext(self):
        ids = self.dl.GP('ids', '')
        idsn = self.dl.GP('idsn', '')
        pk = self.dl.GP('pik', '')
        l = self.dl.get_ids(ids)
        p = self.dl.get_property(ids)
        ln = self.dl.get_ids(idsn)
        pn = self.dl.get_property(idsn)

        M = []
        Mn = []
        MM=[]
        for i in p:
            for j in l:
                if i[0] == j[0]:
                    A = str(i[0]) + ':' + str(j[1])
                    B = i[1] + '(' + j[2] + ')'
                    M.append([B, A])
        if len(pn)>0:
            for i in pn:
                for j in ln:
                    if i[0] == j[0]:
                        A = str(i[0]) + ':' + str(j[1])
                        B = i[1] + '(' + j[2] + ')'
                        Mn.append([B, A])

        if len(Mn)>0:
            for m in M:
                for n in Mn:
                    A=m[1]+','+n[1]+','
                    B=m[0]+'—'+n[0]
                    MM.append([B, A])
        else:
            MM=M

        d = ''
        L = self.dl.get_gg(pk)

        for k in MM:
            if len(L) > 0:
                for v in L:
                    if v[0] == k[0]:
                        d += '<div class="row">%s<input type="hidden" name="ggname" value="%s"><input type="hidden" name="property_child_ids" value="%s"><div class="col-sm-12 ">' % (
                        v[0], v[0], v[1])
                        d += '原价:<input type="text" name="originalpriceext" style="width:60px;" value="%s">' % v[2]
                        d += '现价:<input type="text" name="minpriceext" style="width:60px;" value="%s">' % v[3]
                        d += '拼团价:<input type="text" name="ptpriceext" style="width:60px;" value="%s">' % v[4]
                        d += '会员价:<input type="text" name="hypriceext" style="width:60px;" value="%s">' % v[7]
                        d += '积分:<input type="text" name="scoreext" style="width:60px;" value="%s">' % v[5]
                        d += '库存数:<input type="text" name="storesext" style="width:60px;" value="%s">' % v[6]
                        d += '</div></div><br>'
            else:
                d += '<div class="row">%s<input type="hidden" name="ggname" value="%s"><input type="hidden" name="property_child_ids" value="%s"><div class="col-sm-12 ">' % (
                k[0], k[0], k[1])
                d += '原价:<input type="text" name="originalpriceext" style="width:60px;" value="0">'
                d += '现价:<input type="text" name="minpriceext" style="width:60px;" value="0">'
                d += '拼团价:<input type="text" name="ptpriceext" style="width:60px;" value="0">'
                d += '会员价:<input type="text" name="hypriceext" style="width:60px;" value="0">'
                d += '积分:<input type="text" name="scoreext" style="width:60px;" value="0">'
                d += '库存数:<input type="text" name="storesext" style="width:60px;" value="0">'
                d += '</div></div><br>'

        return d

    def goPartGet_spec_child(self):
        dR = self.dl.get_spec_child_data()
        return self.jsons(dR)

    def goPartSet_spec_child(self):
        dR = {'code': '1', 'MSG': '没有数据返回'}
        sid, l = self.dl.set_spec_child_data()
        if sid == 0:
            return self.jsons(dR)

        d = ''
        L = []
        for i in l:
            d += '''
             <div class="specDiv col-sm-2" style="line-height:4rem;">
                <input name="sp%s" type="hidden" value="%s">
                <button type="button" class="badge badge-danger" onclick="sp_del(this,'%s')">
                    <i class="ace-icon fa fa-times red2"></i>
                </button>
                <span>%s</span>
                <img src="%s" style="width:50px;">
            </div>
            ''' % (sid, i[0], sid, i[1], i[2])
            L.append(str(i[0]))
        if d != '':
            ids = ','.join(L)
            dR = {'code': '0', 'data': d, 'ids': ids, 'sid': sid}

        return self.jsons(dR)

    def goPartAdd_spec_child(self):
        dR = self.dl.add_spec_child_data()
        return self.jsons(dR)

    def goPartGet_spec_class(self):
        dR = {'code': '', 'msg':''}
        l, spa = self.dl.get_spec_class_data()
        d = '''
            <div class="panel panel-default" id="ppd%(spa)s">
            <div class="panel-heading" id="ph%(spa)s">
                <div class="form-group">
            <div class="col-sm-10">
            <input name="spec_p%(spa)s" type="hidden" value="">
            <input name="spec_str%(spa)s" type="hidden" value="">
            <input name="spec_child%(spa)s" type="hidden" value="">
            <select class="js-example-basic-single col-sm-12"
                    style="width:150px;" onchange="onshow_ch(this,'%(spa)s')" name="spec_p">
            <option value="">选择规格分类</option>
        ''' % ({'spa': spa})
        for i in l:
            d += ' <option value="%s">%s</option>' % (i[0], i[1])
        d += '''
          <option value="0">自定义</option>
          </select>
           <button type="button" class="btn btn-primary btn-sm" onclick="show_spec_child('%s')">
                    添加规格型号(规格子属性)
           </button>
           </div>
           <div class="col-sm-2">
                <button type="button" class="btn btn-sm btn-warning"
                        onclick="del_spec(this,'%s')">
                    删除分类
                </button>
            </div>
           </div>
           </div>
            <div class="panel-body" id="pb%s">  
            </div>
        </div>
        ''' % (spa, spa, spa)
        dR = {'code': '0', 'data': d}
        return self.jsons(dR)

    def goPartSave_add_spec(self):
        dR = self.dl.save_add_spec_data()
        if dR['code'] == '0':
            l = dR['data']
            data = ' <option value="%s" selected="selected">%s</option>' % (l['id'], l['cname'])
            dR['data'] = data
        return self.jsons(dR)

    def goPartGet_spec_class_re(self):
        dR = {'code': '', }
        l, L, S, D = self.dl.get_spec_class_re_data()
        # print(D)
        k = 1
        d = ''
        for j in L:

            d += '''
            <div class="panel panel-default" id="ppd%(spa)s">
            <div class="panel-heading" id="ph%(spa)s">
                <div class="form-group">
            <div class="col-sm-10">
            <input name="spec_p%(spa)s" type="hidden" value="%(spv)s">
            <input name="spec_str%(spa)s" type="hidden" value="">
            <input name="spec_child%(spa)s" type="hidden" value="%(scd)s">
            <select class="js-example-basic-single col-sm-12"
                    style="width:150px;" onchange="onshow_ch(this,'%(spa)s')" name="spec_p">
            <option value="">选择规格分类</option>
            ''' % ({'spa': k, 'spv': j, 'scd': D[str(j)]})
            for i in S:
                if i[0] == j:
                    d += ' <option value="%s" selected="selected">%s</option>' % (i[0], i[1])
                else:
                    d += ' <option value="%s">%s</option>' % (i[0], i[1])

            d += '''
              <option value="0">自定义</option>
              </select>
               <button type="button" class="btn btn-primary btn-sm" onclick="show_spec_child('%s')">
                        添加规格型号(规格子属性)
               </button>
               </div>
               <div class="col-sm-2">
                    <button type="button" class="btn btn-sm btn-warning"
                            onclick="del_spec(this,'%s')">
                        删除分类
                    </button>
                </div>
               </div></div>
                <div class="panel-body" id="pb%s">''' % (k, k, k)
            for a in l:
                if a[0] == j:
                    d += '''
                         <div class="specDiv col-sm-2" style="line-height:4rem;">
                            <input name="sp%s" type="hidden" value="%s">
                            <button type="button" class="badge badge-danger" onclick="sp_del(this,'%s')">
                                <i class="ace-icon fa fa-times red2"></i>
                            </button>
                            <span>%s</span>
                            <img src="%s" style="width:50px;">
                        </div>
                        ''' % (k, a[1], k, a[2], a[3])

            d += '''  
                </div>
            </div>
            '''
            k += 1
        dR = {'code': '0', 'data': d}
        return self.jsons(dR)
