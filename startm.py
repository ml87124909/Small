# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""start.py"""

import os
import sys
from imp import reload
from flask import Flask, request
from flask_cors import CORS

reload(sys)

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
sys.stdout = sys.stderr

from  basic import publicw
reload(publicw)

ROOT = publicw.ROOT
showmanage,showmapi,showmPay=publicw.showmanage,publicw.showmapi,publicw.showmPay#btbtc平台
showupload = publicw.showupload

sys.path.append(ROOT)

app=Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTYj'
CORS(app)

@app.route('/' , methods=['GET', 'POST'])
@app.route('/manage' , methods=['GET', 'POST'])
def manage():
    return showmanage(request)

@app.route('/mapi/<int:mallid>', methods=['GET','POST'])
def mapi(mallid):
    return showmapi(request,mallid)


@app.route('/mpay/<int:mallid>/notify', methods=['GET','POST'])
def mpay(mallid):
    return showmPay(request,mallid)

@app.route('/upload' , methods=['GET', 'POST'])
def upload():
    return showupload(request)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

application=app



