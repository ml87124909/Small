# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""admin/vi/common.py"""

from imp import reload
from basic.publicw import DEBUG,user_menu
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL


class ccommon(cBASE_TPL):
    
    def specialinit(self):
        pass

    def goPartRefeshmenu(self):
        referer = self.objHandle.headers.get('referer')

        if not referer: 
            referer = 'admin?viewid=home'
        menu1,menu2,menu3 = self.dl.getSysMenu(self.dl.usr_id)

        if self.dl.usr_id in user_menu:
            user_menu[self.dl.usr_id] = {
                'menu1':menu1,'menu2':menu2,'menu3':menu3
            }
        else:
            user_menu.update( {self.dl.usr_id:{
                'menu1':menu1,'menu2':menu2,'menu3':menu3
            }} )

        s = self.redirect(referer)

        return s

    def goPartTopmenu(self):
        self.getBreadcrumb()  # 获取面包屑
        self.mnuid = self.dl.mnuid = self.dl.GP('mnuid')
        s = self.runApp('topmenu.html')
        return s

    def goPartMenu(self):
        self.mnuid = self.dl.mnuid = self.dl.GP('mnuid')
        s = self.runApp('common.html')
        return s
    
    
    
        
 