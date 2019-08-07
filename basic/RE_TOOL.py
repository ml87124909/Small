# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""basic/RE_TOOL.py"""
import re

#常用的几个符号的一些Unicode编码：
#单引号:   %u0027、%u02b9、%u02bc、%u02c8、%u2032、%uff07、%c0%27、%c0%a7、%e0%80%a7
#空格：%u0020、%uff00、%c0%20、%c0%a0、%e0%80%a0
#左括号：%u0028、%uff08、%c0%28、%c0%a8、%e0%80%a8
#右括号：%u0029、%uff09、%c0%29、%c0%a9、%e0%80%a9

rule=[      
      '\.\./'
      ,'\:\$'
      ,'\$\{'
      ,'(%uff07|%u0027|%u02b9|%u02bc|%u02c8|%u2032|%c0%27|%c0%a7|%e0%80%a7|%u0020|%uff00|%c0%20|%c0%a0|%e0%80%a0|%u0028|%uff08|%c0%28|%c0%a8|%e0%80%a8|%u0029|%uff09|%c0%29|%c0%a9|%e0%80%a9)'
      #,'\'|select'
      ,'(update|delete|select).+(from|limit|case|char|when|else|end|@@|\+)'
      , '(?:(union(.*?)select))'
      #, '^(.+)\\sand\\s(.+)|(.+)\\sor(.+)\\s$'
      #,'^((?:\d|\=|\s)+)\\sand\\s((?:\d|\=|\s)+)|(.+)\\sor((?:\d|\=|\s)+)\\s$'
      ,'[\s\S]*?(or|and){1}[\s\/\\\*]*?\d+[\s\S]*?=[\s]*?\d+'       #防像这种型式:10/**/or/**/7659=7659   
      , 'having|rongjitest|function([\s]*)\(([\s\S]*)\)|ltrim|rtrim|drop|insert([\s]*)into'
      , 'waitfor(.*?)delay'
      , 'sleep\\((\\s*)(\\d*)(\\s*)\\)'
      , 'benchmark\\((.*)\\,(.*)\\)'
      , 'base64_decode\\('
      , '(?:from\\W+information_schema\\W)'
      , '(?:(?:current_)user|database|schema|connection_id)\\s*\\('
      , '(?:etc\\/\\W*passwd)'
      , 'into(\\s+)+(?:dump|out)file\\s*'
      , 'group\\s+by.+\\('
      , 'xwork.MethodAccessor'
      , '(?:define|eval|file_get_contents|include|require|require_once|shell_exec|phpinfo|system|passthru|preg_\\w+|execute|echo|print|print_r|var_dump|(fp)open|alert|showmodaldialog)\\('      
      , 'xwork\\.MethodAccessor'
      #, '(gopher|doc|php|glob|file|phar|zlib|ftp|ldap|dict|ogg|data|tostring)\\:\\/'
      , '(gopher|doc|php|glob|file|phar|zlib|ftp|ldap|dict|ogg|data|tostring|valueof)\\:'
      , 'java\\.lang'
      , '\\$_(GET|post|cookie|files|session|env|phplib|GLOBALS|SERVER)\\['
      , '\\<(.*)(iframe|script|body|img|layer|div|meta|style|base|object|input|span|table|tr|th|td|tbody|tfoot|thead|select|label|ul|li|textarea|button)'
      , '(onmouseover|onerror|onload|onclick|onfocus|onblur|onchange|ondblclick|onkeydown|onkeypress|onkeyup|onload|onmousedown|onmousemove|onmouseout|onmouseup|onreset|onresize|onselect|onsubmit|onunload|style|class|window|window\[([\S]*)]|windw.location|window.location.href)([\s]*)\\='  #(.*?)
      ]


def check_sqlInjection_XSS(fv):
    fv=str(fv)
    if fv!='':
        for r in rule:            
            result = re.findall('%s'%r,fv.lower())
            if len(result)>0:
                # SHARE.log(r)
                # SHARE.log(fv.lower())
                return 1
        return 0
    return 0

def is_int(s_input):
    # 判断输入的数字是否整数，整数返回1，非整数返回0
    s_input = str(s_input)
    re_int = re.compile(r'[0-9]+$')
    result = re_int.match(s_input)
    if result:
        if int(s_input) > 2147483647:
            return 0
        else:
            return 1
    else:
        return 0


def is_changgui_char(s_input):
    # 判断输入的是否常规字符，如果果，返回1，如果不是，返回0
    # 常规字符只包括0-9，A-Z，a-z
    #print s_input, '000000000000'
    s_input = str(s_input).upper()
    #print s_input, '11111111111'
    re_char = re.compile(r'[\w\d]+$')
    result = re_char.match(s_input)
    if result:
        return 1
    else:
        return 0


def is_date(s_input):
    s_input = str(s_input).upper()
    re_char = re.compile(r'[\d-]+$')
    result = re_char.match(s_input)
    if result:
        return 1
    else:
        return 0


def is_login_id(s_input):
    s_input = str(s_input).upper()
    re_char = re.compile(r'[\w@._-]{2,20}$')
    result = re_char.match(s_input)
    if result:
        return 1
    else:
        return 0


def is_password(s_input):
    # 检查字符是否有不符合要求的
    # 合要求的，返回1，不合要求的，返回0
    s_input = str(s_input).upper()
    re_char = re.compile(r'[\w_!@#$%^&*-.]{8,20}$')
    result = re_char.match(s_input)
    if not result:
        return 0

    if re.search("[0-9]", s_input):
        a = 1
    else:
        a = 0
    if re.search("[a-zA-Z]", s_input):
        b = 1
    else:
        b = 0
    if re.search("[_!@#$%^&*-]", s_input):
        c = 1
    else:
        c = 0
    if a + b + c >= 2:  # 至少包括两种以上的字符
        return 1
    else:
        return 0


def is_mobile(s_input):
    re_char = re.compile(r'[\d]{11,11}$')
    result = re_char.match(s_input)
    if result:
        return 1
    else:
        return 0


def is_id_no(s_input):
    # 判断是否是身份证号码，是返回1，不是返回0
    re_char = re.compile(r'[\dX]{18}$')
    result = re_char.match(s_input)
    if result:
        return 1
    else:
        return 0


def is_cn_name(s_input):
    # 是否中国姓名，汉字，最长6个
    u_s_input = unicode(str(s_input), 'eucgb2312_cn')
    re_char = re.compile(u'[\u4e00-\u9fa5]{2,6}$')
    result = re_char.match(u_s_input)
    if result:
        return 1
    else:
        return 0


def is_china_txt(s_input):
    # 是否全中文字
    u_s_input = unicode(str(s_input), 'eucgb2312_cn')
    re_char = re.compile(u'[\u4e00-\u9fa5]+$')
    result = re_char.match(u_s_input)
    if result:
        return 1
    else:
        return 0


def is_email(s_input):
    # 检查邮件地址
    re_char = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
    result = re_char.match(s_input)
    if result:
        return 1
    else:
        return 0


def is_postcode(s_input):
    # 邮政编码
    re_char = re.compile(r'[\d]{6}$')
    result = re_char.match(s_input)
    if result:
        return 1
    else:
        return 0


def is_md5(s_input):
    re_char = re.compile(r'[0-9a-zA-Z]{32}$')
    result = re_char.match(s_input)
    if result:
        return 1
    else:
        return 0

#只能是数据与字母组成的字符串
def is_NumAndLetter(s_input):        
    re_char=re.compile(r'[0-9a-zA-Z]+$')
    result=re_char.match(s_input)  
    if result:
        return 1
    else:
        return 0

def is_changgui(s_input):
    #判断输入的是否常规字符，如果果，返回1，如果不是，返回0
    #常规字符只包括0-9，A-Z，a-z, .,_,中文    
    u_s_input=unicode(str(s_input), 'utf-8')
    re_char=re.compile(u'[\u4e00-\u9fa5._a-zA-Z0-9]+$')
    result=re_char.match(u_s_input)    
    if result:
        return 1
    else:
        return 0

def test():
    s_input = 'Maddddd32ccc'
    s_input = '12313412@3a-'
    s1 = re.search("[0-9]", s_input).group(0)
    s2 = re.search("[a-zA-Z]", s_input).group(0)
    s3 = re.search("[_!@#$%^&*-]", s_input).group(0)
    print(s_input)
    print(s1)
    print(s2)
    print(s3)


if __name__ == "__main__":
    # R=is_int('0+0+0+3')
    # R=is_changgui_char('0')
    # R=is_date('2017-10-12')
    # R=is_login_id('hwj_026@163.>com')
    # R=is_login_id('hwj-02_6>@163.com')
    # print R
    # test()
    # s1='匹配中文字符的正则表达式'
    # s1="叶璐"
    s1 = '175254165@qq.com'
    s1 = '518043'
    s1 = '5af0a5609d11136267cab8571a6ed0c2'
    print(is_md5(s1))