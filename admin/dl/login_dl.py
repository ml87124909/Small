# -*- coding: utf-8 -*-

##############################################################################
#
#
#
#
##############################################################################

from imp import reload
from basic.publicw import DEBUG

if DEBUG=='1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


class clogin_dl(cBASE_DL):

   
        
    #在子类中重新定义         
    def myInit(self):
        pass

    