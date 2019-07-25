# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
"""config.py"""
#pip3 install --upgrade psycopg2==2.8.3
import os
CLIENT_NAME = 'Small'#注意:这个是项目名，要跟下边的路径对应
DEBUG='1'
user_link=0

WEBSITE_PATHR = os.path.join('/var/games/', CLIENT_NAME)
fnamer = r'/var/games/%s/%s.log' %(CLIENT_NAME,CLIENT_NAME)
ROOTR = r'/var/games'
SITE_ROOTR = r'/var/games/' + CLIENT_NAME
PDF_OUT_PATHR = r'/var/games/%s/static/data/pdf'%CLIENT_NAME
ATTACH_ROOTR = r'/var/games/%s/static/data'%CLIENT_NAME
PEM_ROOTR = r'/var/data_h/%s'%CLIENT_NAME
#################数据库相关配置


################