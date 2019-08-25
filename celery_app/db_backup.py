# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""celery_app/db_backup.py"""


from flask import Flask, json
# from flask_mail import Mail,Message
from celery import Celery
from celery_app import c
import time

app = Flask(__name__)

import requests, json, os, random, traceback, oss2
from imp import reload
import datetime
from basic import publicw as public



db, ATTACH_ROOT, getToday = public.db, public.ATTACH_ROOT, public.getToday
oUSER, oPT_GOODS, oMALL = public.oUSER, public.oPT_GOODS, public.oMALL
from qiniu import Auth, put_stream, put_data, put_file, BucketManager
from basic.wxbase import wx_minapp_login, WXBizDataCrypt, WxPay


# app.config['MAIL_SERVER'] = ''
# app.config['MAIL_PORT'] = 994
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_DEBUG'] = True
# app.config['MAIL_DEFAULT_SENDER'] = ''
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ""

# mails=Mail(app)

@c.task
def backup_db():  #####备份数据库

    try:
        sql = "insert into backup_log(bname,btime,ctime)values('数据库备份进入开始',now(),now())"
        db.query(sql)
    except:
        return
    sql = "select access_key,secret_key,name,domain,endpoint,COALESCE(ctype,0) from qiniu where usr_id=1"
    l, t = db.select(sql)
    if t == 0:
        return
    sql = "select dbname from toll_config"
    lT, iN = db.select(sql)
    if iN == 0:
        return
    access_key, secret_key, name, domain, endpoint, ctype = l[0]
    dbname = lT[0][0]
    try:
        datets = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ts = time.strftime('%Y%m%d%H%M%S', time.localtime())
        MaLiShop = '%s%s' % (dbname, ts)
        bat = '/usr/local/bin/pg_dump --file "/var/data_h/%s.sql" --host localhost --port "5432" --username "postgres" --no-password --verbose --format=c --blobs "%s"' % (
            MaLiShop, dbname)
        os.system(bat)

        path = '/var/data_h/%s.sql' % MaLiShop
        if os.path.isfile(path):

            if ctype == 0:
                key = '%s.sql' % MaLiShop
                q = Auth(access_key, secret_key)
                token = q.upload_token(name, key, 3600)
                ret, info = put_file(token, key, path)
                if ret.get('key') == key:

                    try:
                        sql = "insert into backup_log(bname,btime,ctime,type)values('%s','%s',now(),1)" % (key, datets)
                        db.query(sql)
                        os.remove(path)
                    except:
                        pass
            else:
                key = '/backup_db/%s.sql' % MaLiShop
                auth = oss2.Auth(access_key, secret_key)
                bucket = oss2.Bucket(auth, endpoint, name)
                result = bucket.put_object_from_file(key, path)  # 上传
                if result.status == 200:

                    try:
                        sql = "insert into backup_log(bname,btime,ctime,type)values('%s','%s',now(),2)" % (key, datets)
                        db.query(sql)
                        os.remove(path)
                    except:
                        pass
    except:
        try:
            sql = "insert into backup_log(bname,btime,ctime)values('数据库备份出错',now(),now())"
            db.query(sql)
        except:
            pass


#
# @c.task
# def send_mail():
#
#     sql="""select p.id,p.email,to_char(p.ctime,'YYYY-MM-DD HH:MM')ctime,p.content,p.mp3,COALESCE(p.tomp3,0)
#             from post_future p
#             where COALESCE(p.del_flag,0)=0 and COALESCE(p.status,0)!=1 and to_time<now() """
#     l,t=db.select(sql)
#     if t>0:
#         with app.app_context():
#             with mails.connect() as conn:
#                 for i in l:
#                     id,email,ctime,content,audio,flag=i[0],i[1],i[2],i[3],i[4],i[5]
#                     path = os.path.join(ATTACH_ROOT, audio)
#
#                     html = u'''
#                         <style type="text/css">
#                         /*** BMEMBF Start ***/
#                         @media only screen and (max-width: 480px){table.blk, table.tblText, .bmeHolder, .bmeHolder1, table.bmeMainColumn{width:100% !important;} }
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable td.tblCell{padding:0px 20px 20px 20px !important;} }
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable.bmeCaptionTableMobileTop td.tblCell{padding:20px 20px 0 20px !important;} }
#                         @media only screen and (max-width: 480px){table.bmeCaptionTable td.tblCell{padding:10px !important;} }
#                         @media only screen and (max-width: 480px){table.tblGtr{ padding-bottom:20px !important;} }
#                         @media only screen and (max-width: 480px){td.blk_container, .blk_parent, .bmeLeftColumn, .bmeRightColumn, .bmeColumn1, .bmeColumn2, .bmeColumn3, .bmeBody{display:table !important;max-width:600px !important;width:100% !important;} }
#                         @media only screen and (max-width: 480px){table.container-table, .bmeheadertext, .container-table { width: 95% !important; } }
#                         @media only screen and (max-width: 480px){.mobile-footer, .mobile-footer a{ font-size: 13px !important; line-height: 18px !important; } .mobile-footer{ text-align: center !important; } table.share-tbl { padding-bottom: 15px; width: 100% !important; } table.share-tbl td { display: block !important; text-align: center !important; width: 100% !important; } }
#                         @media only screen and (max-width: 480px){td.bmeShareTD, td.bmeSocialTD{width: 100% !important; } }
#                         @media only screen and (max-width: 480px){td.tdBoxedTextBorder{width: auto !important;}}
#                         @media only screen and (max-width: 480px){table.blk, table[name=tblText], .bmeHolder, .bmeHolder1, table[name=bmeMainColumn]{width:100% !important;} }
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable td[name=tblCell]{padding:0px 20px 20px 20px !important;} }
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable.bmeCaptionTableMobileTop td[name=tblCell]{padding:20px 20px 0 20px !important;} }
#                         @media only screen and (max-width: 480px){table.bmeCaptionTable td[name=tblCell]{padding:10px !important;} }
#                         @media only screen and (max-width: 480px){table[name=tblGtr]{ padding-bottom:20px !important;} }
#                         @media only screen and (max-width: 480px){td.blk_container, .blk_parent, [name=bmeLeftColumn], [name=bmeRightColumn], [name=bmeColumn1], [name=bmeColumn2], [name=bmeColumn3], [name=bmeBody]{display:table !important;max-width:600px !important;width:100% !important;} }
#                         @media only screen and (max-width: 480px){table[class=container-table], .bmeheadertext, .container-table { width: 95% !important; } }
#                         @media only screen and (max-width: 480px){.mobile-footer, .mobile-footer a{ font-size: 13px !important; line-height: 18px !important; } .mobile-footer{ text-align: center !important; } table[class="share-tbl"] { padding-bottom: 15px; width: 100% !important; } table[class="share-tbl"] td { display: block !important; text-align: center !important; width: 100% !important; } }
#                         @media only screen and (max-width: 480px){td[name=bmeShareTD], td[name=bmeSocialTD]{width: 100% !important; } }
#                         @media only screen and (max-width: 480px){td[name=tdBoxedTextBorder]{width: auto !important;}}
#                         @media only screen and (max-width: 480px){.bmeImageCard table.bmeImageTable{height: auto !important; width:100% !important; padding:20px !important;clear:both; float:left !important; border-collapse: separate;} }
#                         @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable{height: auto !important; width:100% !important; padding:10px !important;clear:both;} }
#                         @media only screen and (max-width: 480px){.bmeMblInline table.bmeCaptionTable{width:100% !important; clear:both;} }
#                         @media only screen and (max-width: 480px){table.bmeImageTable{height: auto !important; width:100% !important; padding:10px !important;clear:both; } }
#                         @media only screen and (max-width: 480px){table.bmeCaptionTable{width:100% !important;  clear:both;} }
#                         @media only screen and (max-width: 480px){table.bmeImageContainer{width:100% !important; clear:both; float:left !important;} }
#                         @media only screen and (max-width: 480px){table.bmeImageTable td{padding:0px !important; height: auto; } }
#                         @media only screen and (max-width: 480px){img.mobile-img-large{width:100% !important; height:auto !important;} }
#                         @media only screen and (max-width: 480px){img.bmeRSSImage{max-width:320px; height:auto !important;}}
#                         @media only screen and (min-width: 640px){img.bmeRSSImage{max-width:600px !important; height:auto !important;} }
#                         @media only screen and (max-width: 480px){.trMargin img{height:10px;} }
#                         @media only screen and (max-width: 480px){div.bmefooter, div.bmeheader{ display:block !important;} }
#                         @media only screen and (max-width: 480px){.tdPart{ width:100% !important; clear:both; float:left !important; } }
#                         @media only screen and (max-width: 480px){table.blk_parent1, table.tblPart {width: 100% !important; } }
#                         @media only screen and (max-width: 480px){.tblLine{min-width: 100% !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblCenter img { margin: 0 auto; } }
#                         @media only screen and (max-width: 480px){.bmeMblCenter, .bmeMblCenter div, .bmeMblCenter span  { text-align: center !important; text-align: -webkit-center !important; } }
#                         @media only screen and (max-width: 480px){.bmeNoBr br, .bmeImageGutterRow, .bmeMblStackCenter .bmeShareItem .tdMblHide { display: none !important; } }
#                         @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable, .bmeMblInline table.bmeCaptionTable, td.bmeMblInline { clear: none !important; width:50% !important; } }
#                         @media only screen and (max-width: 480px){.bmeMblInlineHide, .bmeShareItem .trMargin { display: none !important; } }
#                         @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable img, .bmeMblShareCenter.tblContainer.mblSocialContain, .bmeMblFollowCenter.tblContainer.mblSocialContain{width: 100% !important; } }
#                         @media only screen and (max-width: 480px){.bmeMblStack> .bmeShareItem{width: 100% !important; clear: both !important;} }
#                         @media only screen and (max-width: 480px){.bmeShareItem{padding-top: 10px !important;} }
#                         @media only screen and (max-width: 480px){.tdPart.bmeMblStackCenter, .bmeMblStackCenter .bmeFollowItemIcon {padding:0px !important; text-align: center !important;} }
#                         @media only screen and (max-width: 480px){.bmeMblStackCenter> .bmeShareItem{width: 100% !important;} }
#                         @media only screen and (max-width: 480px){ td.bmeMblCenter {border: 0 none transparent !important;}}
#                         @media only screen and (max-width: 480px){.bmeLinkTable.tdPart td{padding-left:0px !important; padding-right:0px !important; border:0px none transparent !important;padding-bottom:15px !important;height: auto !important;}}
#                         @media only screen and (max-width: 480px){.tdMblHide{width:10px !important;} }
#                         @media only screen and (max-width: 480px){.bmeShareItemBtn{display:table !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblStack td {text-align: left !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblStack .bmeFollowItem{clear:both !important; padding-top: 10px !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblStackCenter .bmeFollowItemText{padding-left: 5px !important;}}
#                         @media only screen and (max-width: 480px){.bmeMblStackCenter .bmeFollowItem{clear:both !important;align-self:center; float:none !important; padding-top:10px;margin: 0 auto;}}
#                         @media only screen and (max-width: 480px){
#                         .tdPart> table{width:100% !important;}
#                         }
#                         @media only screen and (max-width: 480px){.tdPart>table.bmeLinkContainer{ width:auto !important; }}
#                         @media only screen and (max-width: 480px){.tdPart.mblStackCenter>table.bmeLinkContainer{ width:100% !important;}}
#                         .blk_parent:first-child, .blk_parent{float:left;}
#                         .blk_parent:last-child{float:right;}
#                         /*** BMEMBF END ***/
#
#                         table[name="bmeMainBody"], body {background-color:#000000;}
#                          td[name="bmePreHeader"] {background-color:#000000;}
#                          td[name="bmeHeader"] {background:#ffffff;}
#                          td[name="bmeBody"], table[name="bmeBody"] {background-color:#ffffff;}
#                          td[name="bmePreFooter"] {background-color:#ffffff;}
#                          td[name="bmeFooter"] {background-color:#e6e6e8;}
#                          td[name="tblCell"], .blk {font-family:initial;font-weight:normal;font-size:initial;}
#                          table[name="blk_blank"] td[name="tblCell"] {font-family:Arial, Helvetica, sans-serif;font-size:14px;}
#                          [name=bmeMainContentParent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;border-collapse:separate;border-spacing:0px;overflow:hidden;}
#                          [name=bmeMainColumnParent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;overflow:visible;}
#                          [name=bmeMainColumn] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;border-collapse:separate;border-spacing:0px;}
#                          [name=bmeMainContent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;overflow:visible;border-collapse:separate;border-spacing:0px;}
#
#                         </style>
#                         <style type="text/css">
#                         body{margin:0;padding:0;}
#                         .blk_img_dd_wrap{background: #f5f5f7;padding: 40px 0;}
#                         .blk_img_drop{border: 2px dashed #e6e6e8;border-radius: 0px;color: #9ca8af;margin: 0 auto;overflow: hidden;padding: 10px;position: relative;max-width: 210px;}
#                         .blk_img_drop_icon{background: url('/images/icn/img-block-dd.png') no-repeat top;display: inline-block;float: left;height: 65px;margin-right: 10px;width: 65px;}
#                         .blk_img_txt_wrap { float: left; max-width: 135px; }
#                         .blk_img_drop_txt{font-size: 22px;font-weight: bold;line-height: 26px;margin: 5px 0; }
#                         .blk_img_drop_link{font-size: 13px;margin: 0;}
#                         .blk_img_drop_link a{color: #16a7e0;cursor: pointer;font-weight: 600;margin-left: 5px;text-decoration: underline;text-transform: lowercase;}
#                         .blk_img_drop_link a:hover{color: #72c2a1;}
#                         .blk_img_drop_txt.no-dd {display: none;}
#                         .blk_img_drop_link.no-dd span{display: none;}
#                         .blk_img_drop_link.no-dd a{ font-size: 14px; display: inline-block; margin-left: 0; padding: 0;}
#                         .ie8 .blk_img_drop_link.no-dd a { padding-top: 20px; }
#                         .blk_vid_dd_wrap{ background: #f5f5f7; padding: 40px 0; }
#                         .blk_vid_dd{ border: 2px solid #e6e6e8; border-radius: 6px; display: inline-block; padding: 10px 12px; }
#                         .blk_vid_txt{ color: #16a7e0; cursor: pointer; font-size: 20px; font-weight: 600; line-height: 40px; text-decoration: underline; }
#                         .blk_vid_txt:before{ background: url('/images/icn/editor-video-play.png') no-repeat center; border: 4px solid #9ca8af; border-radius: 8px; content: ''; display: inline-block; float: left; height: 39px; width: 39px; margin-right: 10px; }
#                         @media screen { @media (min-width: 0px) {
#                         .blk_img_drop_icon{
#                         background-image: url('/images/icn/img-block-dd.svg');
#                         background-size: 65px 65px;
#                         }
#                         }
#                         }
#                         </style>
#
#                         <table width="100%" cellspacing="0" cellpadding="0" border="0" name="bmeMainBody" style="text-align: center; background-color: rgb(0, 0, 0);" bgcolor="#000000"><tbody><tr><td width="100%" valign="top" align="center">
#                         <table cellspacing="0" cellpadding="0" border="0" name="bmeMainColumnParentTable" style="text-align: center;"><tbody><tr><td name="bmeMainColumnParent" style="border: 0px none transparent; border-radius: 0px; border-collapse: separate; overflow: visible;">
#                         <table name="bmeMainColumn" class="bmeHolder bmeMainColumn" style="max-width: 600px; overflow: visible; border-radius: 0px; border-collapse: separate; border-spacing: 0px;" cellspacing="0" cellpadding="0" border="0" align="center">    <tbody><tr><td width="100%" class="blk_container bmeHolder" name="bmePreHeader" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(0, 0, 0);" bgcolor="#000000"><div id="dv_8" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_divider" style="background-color: rgb(0, 0, 0);"><tbody><tr><td class="tblCellMain" style="padding: 10px 20px;">
#                         <table class="tblLine" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top-width: 0px; border-top-style: none; min-width: 1px;"><tbody><tr><td><span></span></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div><div id="dv_1" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_text"><tbody><tr><td>
#                         <table cellpadding="0" cellspacing="0" border="0" width="100%" class="bmeContainerRow"><tbody><tr><td class="tdPart" valign="top" align="center">
#                         <table cellspacing="0" cellpadding="0" border="0" width="600" name="tblText" class="tblText" style="float:left; background-color:transparent;" align="left"><tbody><tr><td valign="top" align="left" name="tblCell" class="tblCell" style="padding: 0px; text-align: left;"><div style="text-align: center;"><font color="#ffffff" face="Arial, Helvetica, sans-serif"><span style="font-size: 20px;">'''
#                     html += u'一封来自' + str(ctime[:4]) + u'年的信件'
#                     html += u'''</span></font></div></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div></td></tr> <tr><td width="100%" class="bmeHolder" valign="top" align="center" name="bmeMainContentParent" style="border: 0px none transparent; border-radius: 0px; border-collapse: separate; border-spacing: 0px; overflow: hidden;">
#                         <table name="bmeMainContent" style="border-radius: 0px; border-collapse: separate; border-spacing: 0px; border: 0px none transparent; overflow: visible;" width="100%" cellspacing="0" cellpadding="0" border="0" align="center"> <tbody><tr><td width="100%" class="blk_container bmeHolder" name="bmeHeader" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#                         <div id="dv_3" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_divider" style="background-color: rgb(0, 0, 0);"><tbody><tr><td class="tblCellMain" style="padding: 10px 20px;">
#                         <table class="tblLine" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top-width: 0px; border-top-style: none; min-width: 1px;"><tbody><tr><td><span></span></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div></td></tr> <tr><td width="100%" class="blk_container bmeHolder bmeBody" name="bmeBody" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#
#
#                         <div id="dv_11" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_boxtext"><tbody><tr><td align="center" name="bmeBoxContainer" style="padding-left:10px; padding-right:10px; padding-top:5px; padding-bottom:5px;">
#                         <table cellspacing="0" cellpadding="0" width="100%" name="tblText" class="tblText" border="0"><tbody><tr><td valign="top" align="left" style="padding: 20px; font-family:Arial, Helvetica, sans-serif; font-weight: normal; font-size: 14px; color: #383838;background-color:rgba(0, 0, 0, 0); border-collapse: collapse;" name="tblCell" class="tblCell"><div style=""><span style=""><br></span></div><div style=""><span style="">'''
#
#                     html += content
#
#                     html += u'''</span></div></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div><div id="dv_2" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_text"><tbody><tr><td>
#                         <table cellpadding="0" cellspacing="0" border="0" width="100%" class="bmeContainerRow"><tbody><tr><td class="tdPart" valign="top" align="center">
#                         <table cellspacing="0" cellpadding="0" border="0" width="600" name="tblText" class="tblText" style="float:left; background-color:transparent;" align="left"><tbody><tr><td valign="top" align="left" name="tblCell" class="tblCell" style="padding: 5px 20px; text-align: left;"><div style=""><div style="color: rgb(56, 56, 56); font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 400; text-align: right;"><span style=""><br></span></div><div style="color: rgb(56, 56, 56); font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 400; text-align: right;"><span style="">'''
#                     html += ctime
#
#                     html += u'''</span></div><span style=""><div style="text-align: right;"><span style="background-color: transparent;">'''
#                     html+=u'从未来邮局寄出'
#                     html+=u'''</span></div><div style="text-align: right;"><span style="background-color: transparent;"><br></span></div></span></div></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></td></tr></tbody>
#                         </table></div></td></tr>
#                          </tbody>
#                         </table> </td></tr>  <tr><td width="100%" class="blk_container bmeHolder" name="bmeFooter" valign="top" align="center" style="color: rgb(102, 102, 102); border: 0px none transparent; background-color: rgb(230, 230, 232);" bgcolor="#e6e6e8"><div id="dv_10" class="blk_wrapper">
#                         <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_footer" style="background-color: rgb(0, 0, 0);"><tbody><tr><td name="tblCell" class="tblCell" style="padding:5px;" valign="top" align="left">
#                         <table cellpadding="0" cellspacing="0" border="0" width="100%"><tbody><tr><td name="bmeBadgeText" style="text-align:center; word-break: break-word;" align="center"><span id="spnFooterText" style=" font-family: Arial, Helvetica, sans-serif; font-weight: normal; font-size: 11px ; ">
#                         <br><font color="#ffffff">'''
#                     if int(flag) == 1 and os.path.isfile(path):
#                         html+=u'附件包含录音文件，您可以下载到本地播放'
#                     html+=u'''</font></span><font color="#ffffff">
#                         <br></font><br></td></tr></tbody>
#                         </table>    </td></tr></tbody></table></div></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table>
#                         '''
#                     sender=("未来邮局", "weilai@eoen.org")
#                     subject = u'一封来自' + str(ctime[:4]) + u'年的信件'  # 邮件主题
#                     msg = Message(recipients=[email],
#                                   html=html,sender=sender,
#                                   subject=subject)
#
#                     if int(flag) == 1 and os.path.isfile(path):
#                         with app.open_resource(path) as fp:
#                             msg.attach(audio, "audio/mp3", fp.read())
#                     conn.send(msg)
#                     db.query("update post_future set status=1 where id=%s", id)
#
#
# def mail_proj(id,email,ctime,content):
#     apiUser='weilai'#API_USER
#     apiKey='JlAG4Q5G4kNLGpQC'#API_KEY
#     _from='weilai@eoen.org'#发件人地址
#     to=email#收件人地址
#     subject='一封来自'+str(ctime[:4])+'年的信件'#邮件主题
#     #html#邮件内容 (text/html)
#
#     html="""
#     <!DOCTYPE html>
#     <html>
#     <head>
#     <meta content="width=device-width, initial-scale=1.0" name="viewport">
#     <style type="text/css">
#     /*** BMEMBF Start ***/
#     [name=bmeMainBody]{min-height:1000px;}
#     @media only screen and (max-width: 480px){table.blk, table.tblText, .bmeHolder, .bmeHolder1, table.bmeMainColumn{width:100% !important;} }
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable td.tblCell{padding:0px 20px 20px 20px !important;} }
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable.bmeCaptionTableMobileTop td.tblCell{padding:20px 20px 0 20px !important;} }
#     @media only screen and (max-width: 480px){table.bmeCaptionTable td.tblCell{padding:10px !important;} }
#     @media only screen and (max-width: 480px){table.tblGtr{ padding-bottom:20px !important;} }
#     @media only screen and (max-width: 480px){td.blk_container, .blk_parent, .bmeLeftColumn, .bmeRightColumn, .bmeColumn1, .bmeColumn2, .bmeColumn3, .bmeBody{display:table !important;max-width:600px !important;width:100% !important;} }
#     @media only screen and (max-width: 480px){table.container-table, .bmeheadertext, .container-table { width: 95% !important; } }
#     @media only screen and (max-width: 480px){.mobile-footer, .mobile-footer a{ font-size: 13px !important; line-height: 18px !important; } .mobile-footer{ text-align: center !important; } table.share-tbl { padding-bottom: 15px; width: 100% !important; } table.share-tbl td { display: block !important; text-align: center !important; width: 100% !important; } }
#     @media only screen and (max-width: 480px){td.bmeShareTD, td.bmeSocialTD{width: 100% !important; } }
#     @media only screen and (max-width: 480px){td.tdBoxedTextBorder{width: auto !important;}}
#     @media only screen and (max-width: 480px){table.blk, table[name=tblText], .bmeHolder, .bmeHolder1, table[name=bmeMainColumn]{width:100% !important;} }
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable td[name=tblCell]{padding:0px 20px 20px 20px !important;} }
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeCaptionTable.bmeCaptionTableMobileTop td[name=tblCell]{padding:20px 20px 0 20px !important;} }
#     @media only screen and (max-width: 480px){table.bmeCaptionTable td[name=tblCell]{padding:10px !important;} }
#     @media only screen and (max-width: 480px){table[name=tblGtr]{ padding-bottom:20px !important;} }
#     @media only screen and (max-width: 480px){td.blk_container, .blk_parent, [name=bmeLeftColumn], [name=bmeRightColumn], [name=bmeColumn1], [name=bmeColumn2], [name=bmeColumn3], [name=bmeBody]{display:table !important;max-width:600px !important;width:100% !important;} }
#     @media only screen and (max-width: 480px){table[class=container-table], .bmeheadertext, .container-table { width: 95% !important; } }
#     @media only screen and (max-width: 480px){.mobile-footer, .mobile-footer a{ font-size: 13px !important; line-height: 18px !important; } .mobile-footer{ text-align: center !important; } table[class="share-tbl"] { padding-bottom: 15px; width: 100% !important; } table[class="share-tbl"] td { display: block !important; text-align: center !important; width: 100% !important; } }
#     @media only screen and (max-width: 480px){td[name=bmeShareTD], td[name=bmeSocialTD]{width: 100% !important; } }
#     @media only screen and (max-width: 480px){td[name=tdBoxedTextBorder]{width: auto !important;}}
#     @media only screen and (max-width: 480px){.bmeImageCard table.bmeImageTable{height: auto !important; width:100% !important; padding:20px !important;clear:both; float:left !important; border-collapse: separate;} }
#     @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable{height: auto !important; width:100% !important; padding:10px !important;clear:both;} }
#     @media only screen and (max-width: 480px){.bmeMblInline table.bmeCaptionTable{width:100% !important; clear:both;} }
#     @media only screen and (max-width: 480px){table.bmeImageTable{height: auto !important; width:100% !important; padding:10px !important;clear:both; } }
#     @media only screen and (max-width: 480px){table.bmeCaptionTable{width:100% !important;  clear:both;} }
#     @media only screen and (max-width: 480px){table.bmeImageContainer{width:100% !important; clear:both; float:left !important;} }
#     @media only screen and (max-width: 480px){table.bmeImageTable td{padding:0px !important; height: auto; } }
#     @media only screen and (max-width: 480px){img.mobile-img-large{width:100% !important; height:auto !important;} }
#     @media only screen and (max-width: 480px){img.bmeRSSImage{max-width:320px; height:auto !important;}}
#     @media only screen and (min-width: 640px){img.bmeRSSImage{max-width:600px !important; height:auto !important;} }
#     @media only screen and (max-width: 480px){.trMargin img{height:10px;} }
#     @media only screen and (max-width: 480px){div.bmefooter, div.bmeheader{ display:block !important;} }
#     @media only screen and (max-width: 480px){.tdPart{ width:100% !important; clear:both; float:left !important; } }
#     @media only screen and (max-width: 480px){table.blk_parent1, table.tblPart {width: 100% !important; } }
#     @media only screen and (max-width: 480px){.tblLine{min-width: 100% !important;}}
#     @media only screen and (max-width: 480px){.bmeMblCenter img { margin: 0 auto; } }
#     @media only screen and (max-width: 480px){.bmeMblCenter, .bmeMblCenter div, .bmeMblCenter span  { text-align: center !important; text-align: -webkit-center !important; } }
#     @media only screen and (max-width: 480px){.bmeNoBr br, .bmeImageGutterRow, .bmeMblStackCenter .bmeShareItem .tdMblHide { display: none !important; } }
#     @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable, .bmeMblInline table.bmeCaptionTable, td.bmeMblInline { clear: none !important; width:50% !important; } }
#     @media only screen and (max-width: 480px){.bmeMblInlineHide, .bmeShareItem .trMargin { display: none !important; } }
#     @media only screen and (max-width: 480px){.bmeMblInline table.bmeImageTable img, .bmeMblShareCenter.tblContainer.mblSocialContain, .bmeMblFollowCenter.tblContainer.mblSocialContain{width: 100% !important; } }
#     @media only screen and (max-width: 480px){.bmeMblStack> .bmeShareItem{width: 100% !important; clear: both !important;} }
#     @media only screen and (max-width: 480px){.bmeShareItem{padding-top: 10px !important;} }
#     @media only screen and (max-width: 480px){.tdPart.bmeMblStackCenter, .bmeMblStackCenter .bmeFollowItemIcon {padding:0px !important; text-align: center !important;} }
#     @media only screen and (max-width: 480px){.bmeMblStackCenter> .bmeShareItem{width: 100% !important;} }
#     @media only screen and (max-width: 480px){ td.bmeMblCenter {border: 0 none transparent !important;}}
#     @media only screen and (max-width: 480px){.bmeLinkTable.tdPart td{padding-left:0px !important; padding-right:0px !important; border:0px none transparent !important;padding-bottom:15px !important;height: auto !important;}}
#     @media only screen and (max-width: 480px){.tdMblHide{width:10px !important;} }
#     @media only screen and (max-width: 480px){.bmeShareItemBtn{display:table !important;}}
#     @media only screen and (max-width: 480px){.bmeMblStack td {text-align: left !important;}}
#     @media only screen and (max-width: 480px){.bmeMblStack .bmeFollowItem{clear:both !important; padding-top: 10px !important;}}
#     @media only screen and (max-width: 480px){.bmeMblStackCenter .bmeFollowItemText{padding-left: 5px !important;}}
#     @media only screen and (max-width: 480px){.bmeMblStackCenter .bmeFollowItem{clear:both !important;align-self:center; float:none !important; padding-top:10px;margin: 0 auto;}}
#     @media only screen and (max-width: 480px){
#     .tdPart> table{width:100% !important;}
#     }
#     @media only screen and (max-width: 480px){.tdPart>table.bmeLinkContainer{ width:auto !important; }}
#     @media only screen and (max-width: 480px){.tdPart.mblStackCenter>table.bmeLinkContainer{ width:100% !important;}}
#     .blk_parent:first-child, .blk_parent{float:left;}
#     .blk_parent:last-child{float:right;}
#     /*** BMEMBF END ***/
#
#     table[name="bmeMainBody"], body {background-color:#000000;}
#      td[name="bmePreHeader"] {background-color:#000000;}
#      td[name="bmeHeader"] {background:#ffffff;}
#      td[name="bmeBody"], table[name="bmeBody"] {background-color:#ffffff;}
#      td[name="bmePreFooter"] {background-color:#ffffff;}
#      td[name="bmeFooter"] {background-color:#e6e6e8;}
#      td[name="tblCell"], .blk {font-family:initial;font-weight:normal;font-size:initial;}
#      table[name="blk_blank"] td[name="tblCell"] {font-family:Arial, Helvetica, sans-serif;font-size:14px;}
#      [name=bmeMainContentParent] {border-color:transparent;border-width:0px;border-style:none;border-radius:5px;border-collapse:separate;border-spacing:0px;overflow:hidden;}
#      [name=bmeMainColumnParent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;overflow:visible;}
#      [name=bmeMainColumn] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;border-collapse:separate;border-spacing:0px;}
#      [name=bmeMainContent] {border-color:transparent;border-width:0px;border-style:none;border-radius:0px;overflow:visible;border-collapse:separate;border-spacing:0px;}
#
#     </style>
#     <!--[if gte mso 9]>
#     <xml>
#     <o:OfficeDocumentSettings>
#     <o:AllowPNG/>
#     <o:PixelsPerInch>96</o:PixelsPerInch>
#     </o:OfficeDocumentSettings>
#     </xml>
#     <![endif]-->
#
#     </head>
#     <body marginheight=0 marginwidth=0 topmargin=0 leftmargin=0 style="height: 100% !important; margin: 0; padding: 0; width: 100% !important;min-width: 100%;">
#     <style type="text/css">
#     body{height:100%;margin:0;padding:0;}
#     .blk_img_dd_wrap{background: #f5f5f7;padding: 40px 0;}
#     .blk_img_drop{border: 2px dashed #e6e6e8;border-radius: 6px;color: #9ca8af;margin: 0 auto;overflow: hidden;padding: 10px;position: relative;max-width: 210px;}
#     .blk_img_drop_icon{background: url('/images/icn/img-block-dd.png') no-repeat top;display: inline-block;float: left;height: 65px;margin-right: 10px;width: 65px;}
#     .blk_img_txt_wrap { float: left; max-width: 135px; }
#     .blk_img_drop_txt{font-size: 22px;font-weight: bold;line-height: 26px;margin: 5px 0; }
#     .blk_img_drop_link{font-size: 13px;margin: 0;}
#     .blk_img_drop_link a{color: #16a7e0;cursor: pointer;font-weight: 600;margin-left: 5px;text-decoration: underline;text-transform: lowercase;}
#     .blk_img_drop_link a:hover{color: #72c2a1;}
#     .blk_img_drop_txt.no-dd {display: none;}
#     .blk_img_drop_link.no-dd span{display: none;}
#     .blk_img_drop_link.no-dd a{ font-size: 14px; display: inline-block; margin-left: 0; padding: 0;}
#     .ie8 .blk_img_drop_link.no-dd a { padding-top: 20px; }
#     .blk_vid_dd_wrap{ background: #f5f5f7; padding: 40px 0; }
#     .blk_vid_dd{ border: 2px solid #e6e6e8; border-radius: 6px; display: inline-block; padding: 10px 12px; }
#     .blk_vid_txt{ color: #16a7e0; cursor: pointer; font-size: 20px; font-weight: 600; line-height: 40px; text-decoration: underline; }
#     .blk_vid_txt:before{ background: url('/images/icn/editor-video-play.png') no-repeat center; border: 4px solid #9ca8af; border-radius: 8px; content: ''; display: inline-block; float: left; height: 39px; width: 39px; margin-right: 10px; }
#     @media screen { @media (min-width: 0px) {
#     .blk_img_drop_icon{
#     background-image: url('/images/icn/img-block-dd.svg');
#     background-size: 65px 65px;
#     }
#     }
#     }
#     </style>
#
#
#     <table width="100%" cellspacing="0" cellpadding="0" border="0" name="bmeMainBody" style="background-color: rgb(0, 0, 0);" bgcolor="#000000"><tbody><tr><td width="100%" valign="top" align="center">
#     <table cellspacing="0" cellpadding="0" border="0" name="bmeMainColumnParentTable"><tbody><tr><td name="bmeMainColumnParent" style="border: 0px none transparent; border-radius: 0px; border-collapse: separate; overflow: visible;">
#     <table name="bmeMainColumn" class="bmeHolder bmeMainColumn" style="max-width: 600px; overflow: visible; border-radius: 0px; border-collapse: separate; border-spacing: 0px;" cellspacing="0" cellpadding="0" border="0" align="center">    <tbody><tr><td width="100%" class="blk_container bmeHolder" name="bmePreHeader" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(0, 0, 0);" bgcolor="#000000"><div id="dv_8" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_divider" style="background-color: rgb(0, 0, 0);"><tbody><tr><td class="tblCellMain" style="padding: 10px 20px;">
#     <table class="tblLine" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top-width: 0px; border-top-style: none; min-width: 1px;"><tbody><tr><td><span></span></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div><div id="dv_1" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_text"><tbody><tr><td>
#     <table cellpadding="0" cellspacing="0" border="0" width="100%" class="bmeContainerRow"><tbody><tr><td class="tdPart" valign="top" align="center">
#     <table cellspacing="0" cellpadding="0" border="0" width="600" name="tblText" class="tblText" style="float:left; background-color:transparent;" align="left"><tbody><tr><td valign="top" align="left" name="tblCell" class="tblCell" style="padding: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 400; color: rgb(56, 56, 56); text-align: left;"><div style="line-height: 200%; text-align: center;"><span style="color: #ffffff; font-size: 20px; line-height: 200%; font-family: '微軟正黑體', 'Microsoft JhengHei', STXihei, '华文细黑', sans-serif;">一封来自
#     """
#     html+=str(ctime[:4])
#
#     html+="""年的信件</span></div></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div></td></tr> <tr><td width="100%" class="bmeHolder" valign="top" align="center" name="bmeMainContentParent" style="border: 0px none transparent; border-radius: 5px; border-collapse: separate; border-spacing: 0px; overflow: hidden;">
#     <table name="bmeMainContent" style="border-radius: 0px; border-collapse: separate; border-spacing: 0px; border: 0px none transparent; overflow: visible;" width="100%" cellspacing="0" cellpadding="0" border="0" align="center"> <tbody><tr><td width="100%" class="blk_container bmeHolder" name="bmeHeader" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#     <div id="dv_3" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_divider" style="background-color: rgb(0, 0, 0);"><tbody><tr><td class="tblCellMain" style="padding: 10px 20px;">
#     <table class="tblLine" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top-width: 0px; border-top-style: none; min-width: 1px;"><tbody><tr><td><span></span></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div></td></tr> <tr><td width="100%" class="blk_container bmeHolder bmeBody" name="bmeBody" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#
#
#     <div id="dv_11" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_boxtext"><tbody><tr><td align="center" name="bmeBoxContainer" style="padding-left:10px; padding-right:10px; padding-top:5px; padding-bottom:5px;">
#     <table cellspacing="0" cellpadding="0" width="100%" name="tblText" class="tblText" border="0"><tbody><tr><td valign="top" align="left" style="padding: 20px; font-family:Arial, Helvetica, sans-serif; font-weight: normal; font-size: 14px; color: #383838;background-color:rgba(0, 0, 0, 0); border-collapse: collapse;" name="tblCell" class="tblCell"><div style="line-height: 200%;"><span style="font-size: 14px; font-family: '微軟正黑體', 'Microsoft JhengHei', STXihei, '华文细黑', sans-serif; color: #191919; line-height: 200%;">
#     """""
#     html+=content
#     html+="""</span></div></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div><div id="dv_2" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_text"><tbody><tr><td>
#     <table cellpadding="0" cellspacing="0" border="0" width="100%" class="bmeContainerRow"><tbody><tr><td class="tdPart" valign="top" align="center">
#     <table cellspacing="0" cellpadding="0" border="0" width="600" name="tblText" class="tblText" style="float:left; background-color:transparent;" align="left"><tbody><tr><td valign="top" align="left" name="tblCell" class="tblCell" style="padding: 5px 20px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 400; color: rgb(56, 56, 56); text-align: left;"><div style="line-height: 200%; text-align: right;"><span style="font-family: '微軟正黑體', 'Microsoft JhengHei', STXihei, '华文细黑', sans-serif; font-size: 16px;">
#     """
#     html+=str(ctime)
#     html+="""
#     <br>从未来邮局寄出</span><br><br></div></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></td></tr></tbody>
#     </table></div></td></tr> <tr><td width="100%" class="blk_container bmeHolder" name="bmePreFooter" valign="top" align="center" style="color: rgb(56, 56, 56); border: 0px none transparent; background-color: rgb(255, 255, 255);" bgcolor="#ffffff">
#
#     </td></tr> </tbody>
#     </table> </td></tr>  <tr><td width="100%" class="blk_container bmeHolder" name="bmeFooter" valign="top" align="center" style="color: rgb(102, 102, 102); border: 0px none transparent; background-color: rgb(230, 230, 232);" bgcolor="#e6e6e8"><div id="dv_10" class="blk_wrapper">
#     <table width="600" cellspacing="0" cellpadding="0" border="0" class="blk" name="blk_footer" style="background-color: rgb(0, 0, 0);"><tbody><tr><td name="tblCell" class="tblCell" style="padding:5px;" valign="top" align="left">
#     <table cellpadding="0" cellspacing="0" border="0" width="100%"><tbody><tr><td name="bmeBadgeText" style="text-align:center; word-break: break-word;" align="center"><span id="spnFooterText" style="font-family: Arial, Helvetica, sans-serif; font-weight: normal; font-size: 11px; line-height: 140%; color: rgb(255, 255, 255);">
#     <br>&#27492;&#23553;&#20449;&#20214;&#26159;&#24744;&#20197;&#21069;&#23492;&#20986;&#30340;&#26410;&#26469;&#20449;&#20214;&#65292;&#24744;&#29616;&#22312;&#26159;&#21542;&#36824;&#35760;&#24471;&#65311;</span>
#     <br></td></tr></tbody>
#     </table>
#     <!-- /Test Path -->
#     </body>
#     </html>
#     """
#
#     url='https://sendcloud.sohu.com/apiv2/mail/send'
#     data={
#         'apiUser':apiUser,
#         'apiKey':apiKey,
#         'from':_from,
#         'to':to,
#         'subject':subject,
#         'html':html
#     }
#     re=requests.post(url,data=data)
#     dictinfo = json.loads(re.text)
#     status=1
#     if dictinfo.get('statusCode') != 200:
#         status=2
#     db.query("update post_future set status=%s where id=%s",[status,id])
#


if __name__ == '__main__':
    app.run()
