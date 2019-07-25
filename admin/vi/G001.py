# -*- coding: utf-8 -*-
##############################################################################
#
#
#
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG=='1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL             import cBASE_TPL

class cG001(cBASE_TPL):
    
    def setClassName(self):

        self.dl_name = 'G001_dl'
        self.inframe = 1
    def specialinit(self):
        pass

    def goPartList(self):
        self.initHiddenLocal()  # 初始隐藏域
        self.navTitle = '财务设置' #% self.objHandle.method
        self.getBreadcrumb() #获取面包屑
        info = self.dl.getInfo()
        self.assign('item',info)
        detail=self.dl.get_gifts()
        self.assign('detail', detail)

        s = self.runApp('G001_list.html')
        return s
    
    
    
    
        
 