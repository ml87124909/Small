# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：hyj
# Start  Date:  2019
##############################################################################
"""start.py"""


import os, sys, traceback, time,requests
from imp import reload
reload(sys)

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
sys.stdout = sys.stderr
from  basic import publicw
reload(publicw)
from basic.RE_TOOL import *
ROOT,bugcode,DEBUG,CLIENT_NAME,nc_L = publicw.ROOT,publicw.bugcode,publicw.DEBUG,publicw.CLIENT_NAME,publicw.nc_L
requ,showweixin,showindex = publicw.requ,publicw.showweixin,publicw.showindex
showapi,showadmin,showvueapi,showsell=publicw.showapi,publicw.showadmin,publicw.showvueapi,publicw.showsell
showVipPay,showWxPay=publicw.showVipPay,publicw.showWxPay
bugcode_,cVIEW_wx=publicw.bugcode_,publicw.cVIEW_wx


sys.path.append(ROOT)
from flask import Flask, request,jsonify,redirect
from flask_cors import CORS



app=Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTYj'
CORS(app)
#不判断副文本
L_no=['newscontent','text_contents']


@app.route('/', methods=['GET', 'POST'])
@app.route('/admin' , methods=['GET', 'POST'])
def admin():

    RQ = requ(request)
    try:

        viewid = RQ.get('viewid','')
        # ======================系统新的安全处理方法================================================
        # 获取所有的请求参数的字典型式
        req_params = dict(RQ)
        for k, vs in req_params.items():
            # 不检查安全性的字段
            if k.lower() not in L_no:
                # 对所有参数据值循环，判断是否可以注入或可以XSS攻击，若是，则提示出来。
                for v in vs:
                    if check_sqlInjection_XSS(v):
                        # 真是防不胜防,防提示的XSS攻击
                        k = k.replace("'", "''").replace(">", "").replace("<", "")
                        return FireWallMsg(k)

        if 'X-Forwarded-For' in request.headers:
            v = request.headers.get('X-Forwarded-For', '')
            if check_sqlInjection_XSS(v):
                return FireWallMsg('X-Forwarded-For')

        if 'Referer' in request.headers:
            v = request.headers.get('Referer', '').replace('&', '').replace('=', '')
            if check_sqlInjection_XSS(v):
                return FireWallMsg('Referer')

        # ================================处理结束==================================================
        session_cookie = request.cookies.get("%s__session"%CLIENT_NAME)
        if not (session_cookie) and not (viewid  in nc_L):
            return redirect('admin?viewid=login')

        # if 'store.maliapi.com' not in request.base_url and '127.0.0.1' not in request.base_url and 'malishop.janedao.cn' not in request.base_url:
        #     return FireWallMsg(request.base_url)

        if viewid != '':
            return showadmin(viewid,request)
        else:
            return redirect('admin?viewid=home')
    except:
        return bugcode_(traceback)
        #return bugcode(traceback,RQ)



@app.route('/sell' , methods=['GET', 'POST'])
def sell():

    RQ = requ(request)
    try:

        viewid = RQ.get('viewid', '')
        # ======================系统新的安全处理方法================================================
        # 获取所有的请求参数的字典型式
        req_params = dict(RQ)
        for k, vs in req_params.items():
            # 不检查安全性的字段
            if k.lower() not in L_no:
                # 对所有参数据值循环，判断是否可以注入或可以XSS攻击，若是，则提示出来。
                for v in vs:
                    if check_sqlInjection_XSS(v):
                        # 真是防不胜防,防提示的XSS攻击
                        k = k.replace("'", "''").replace(">", "").replace("<", "")
                        return FireWallMsg(k)


        if 'X-Forwarded-For' in request.headers:
            v = request.headers.get('X-Forwarded-For', '')
            if check_sqlInjection_XSS(v):
                return FireWallMsg('X-Forwarded-For')

        if 'Referer' in request.headers:
            v = request.headers.get('Referer', '').replace('&', '').replace('=', '')
            if check_sqlInjection_XSS(v):
                return FireWallMsg('Referer')

        # ================================处理结束==================================================
        # if 'api.maliapi.com' not in request.base_url and '127.0.0.1' not in request.base_url and 'malishop.janedao.cn' not in request.base_url:
        #     return FireWallMsg(request.base_url)

        if viewid == 'home':
            return showsell(request,RQ)
        else:
            return jsonify({'code': 404, 'msg': '您请求的路径有问题，请检查！'})
    except:
        bugcode(traceback,RQ, '2')
        return jsonify({'code': -1, 'msg': '服务器内部错误'})
        # errInf = str(traceback.format_exc())
        # return jsonify({'code': -1, 'data':errInf,'msg': '服务器内部错误'})

@app.route('/MP_verify_KdlipTo3ilSXE03j.txt')
def MP():
    return 'KdlipTo3ilSXE03j'


@app.route('/api/<int:subid>', methods=['GET','POST'])
def api(subid):

    RQ = requ(request)
    try:

        viewid = RQ.get('viewid', '')
        # ======================系统新的安全处理方法================================================
        # 获取所有的请求参数的字典型式
        req_params = dict(RQ)
        for k, vs in req_params.items():
            # 不检查安全性的字段
            if k.lower() not in L_no:
                # 对所有参数据值循环，判断是否可以注入或可以XSS攻击，若是，则提示出来。
                for v in vs:
                    if check_sqlInjection_XSS(v):
                        # 真是防不胜防,防提示的XSS攻击
                        k = k.replace("'", "''").replace(">", "").replace("<", "")
                        return FireWallMsg(k)

        if 'X-Forwarded-For' in request.headers:
            v = request.headers.get('X-Forwarded-For', '')
            if check_sqlInjection_XSS(v):
                return FireWallMsg('X-Forwarded-For')

        if 'Referer' in request.headers:
            v = request.headers.get('Referer', '').replace('&', '').replace('=', '')
            if check_sqlInjection_XSS(v):
                return FireWallMsg('Referer')

        # ================================处理结束==================================================
        # if 'api.maliapi.com' not in request.base_url and '127.0.0.1' not in request.base_url and 'malishop.janedao.cn' not in request.base_url:
        #     return FireWallMsg(request.base_url)

        if viewid == 'home':

            return showapi(viewid,request,subid)
        else:
            return jsonify({ 'code':404,"hello": subid,'msg':'您请求的路径有问题，请检查！'})
    except:
        bugcode(traceback, RQ, '1')
        #errstr = str(traceback.format_exc())
        return jsonify({'code': -1, 'msg': '服务器内部错误'})



@app.route('/pay/<int:subid>/notify', methods=['GET','POST'])
def pay(subid):#平台商家的用户微信支付回调处理

    try:
        if request.method == 'POST':
            try:
                return showWxPay(request,subid)
                # xml_data = request.data
                # dR=paynotify(subid,xml_data)
                # if dR==1:
                #     result_data = {
                #         'return_code': 'FAIL',
                #         'return_msg': '参数格式校验错误'
                #     }
                # else:
                #     result_data = {
                #         'return_code': 'SUCCESS',
                #         'return_msg': 'OK'
                #     }
                # return dict_to_xml(result_data), {'Content-Type': 'application/xml'}
            except:
                bugcode(traceback,'3')
                result_data = {
                    'return_code': 'FAIL',
                    'return_msg': '参数格式校验错误'
                }
                return dict_to_xml(result_data), {'Content-Type': 'application/xml'}
    except:
        errstr = str(traceback.format_exc())
        return jsonify({'code': -1, 'msg': '服务器内部错误', 'error_data': errstr})


@app.route('/vipnotify', methods=['GET', 'POST'])
def vipnotify():#平台vip付费支付回调处理
    try:
        return showVipPay(request)
    except:
        result_data = {
            'return_code': 'FAIL',
            'return_msg': '参数格式校验错误'
        }
        return dict_to_xml(result_data), {'Content-Type': 'application/xml'}



@app.route('/wechat', methods=['GET','POST'])
def weixin():
    return showweixin(request)



@app.route('/error' , methods=['GET', 'POST'])
def mError():
    err = request.values.get('err','')
    msg = ''
    if str(err) == '1':
        msg = '微信版本较低，请升级版本'
    return msg#ErrorInfo(msg)


# 游客登录
@app.route('/index/<int:subid>', methods=['GET', 'POST'])
def index(subid):

    try:
        return showindex(request,subid)
    except:
        return bugcode_(traceback)




if __name__ == '__main__':
    #app.run(port=5001)
    app.run(port=5001)

application=app



