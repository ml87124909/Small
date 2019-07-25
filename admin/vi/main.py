# -*- coding: utf-8 -*-
##############################################################################
#
#
#
#
##############################################################################
from imp import reload
from basic.publicw import DEBUG

if DEBUG == '1':
    import admin.vi.VI_BASE
    reload(admin.vi.VI_BASE)
from admin.vi.VI_BASE             import cVI_BASE


def mShow():
    return cmain().mShowHtml()


class cmain(cVI_BASE):
    def setClassName(self):
        # 设定要实例的 BIZ类和TPL类，为空则继承基类，可以能过判断part的值来设置不同的类名
        '''
        if self.part == 'xxx':
            self.biz_name = 'xxx_biz'
        '''
        self.biz_name = ''

    def goPartMain(self):
        # 跳到个人中心..
        self.js.append('idangerous.swiper.min.js')
        self.css.append('member.css')
        data = []
        if self.mnuid:
            data = self.biz.getLeftMenu(self.mnuid)
        self.assign('data', data)
        s = self.runApp('main.html')
        return s




