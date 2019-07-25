// JavaScript Document
var submit_disabled = true;
var isTrue=0;//验证码 reg
var isTrue2=0;//验证码 找回密码
var isTrue3=0;//邮箱验证码 reg


//登出
function dologout(){
	$.ajax({
			url:"menu" ,
			data:{'fid':'login','act':'dologout'},
			type:"GET",
			success:function(data){
				window.location = 'menu?fid=login';
			}
	 });	
}

//登陆
function login(){
	var username = $("input[name=login_username]").val();
	var password = $("input[name=login_password]").val();
	var checkcode = $("input[name=checkcode]").val();//验证码
	var remenber = $("[name=yhxy]:checked");//记住用户名
	var rem_val="";
    if (remenber.length>0){
    	rem_val="1";
    }

	$.ajax({
		url:"menu" ,
		data:{'fid':'login','act':'dologin','username':username,'password':password,'checkcode':checkcode,'remenber':rem_val},
		type:"POST",
		dataType:'json',
		success:function(data){
			if(data.R == '-1'){
				ialert('登陆失败,用户名或密码错误');
			}else if(data.R == '-2'){
				ialert("验证码错误");
				refreshnum();
			}else if(data.R == '1'){
				window.location = 'menu';
			}
		}
	});	
}

//注册
function reg(){
	var mobile = $("input[name=mobile]").val();
	var password = $("input[name=password]").val();
	var repass = $("input[name=repass]").val();
	var yzm = $("input[name=yzm]").val();
	var regtype = $("input[name=regtype]").val();
	var usrname = $("input[name=usrname]").val();
	var nbrithday = $("input[name=nbrithday]").val();
	if (regtype == 3)
	{
		if(usrname == ''){
		ialert("请输入姓名");
		return false;
		}

		if(nbrithday == ''){
		ialert("请输入农历生日");
		return false;
		}
	}

	if (mobile==""||!isMobile(mobile))
	{
		ialert("请输入正确的手机号码");
		return false;
	}
	
	if(password == ''){
		ialert("请输入密码");
		return false;
	}
	if (password.length < 6)
	{
		ialert("密码至少6个字符");
		return false;
	}
	/*
	var hasNumber = false;
	var hasUpper = false;
	for(var i =0;i<password.length;i++){
		var s =  password[i];
		if(s.match(/^\d+$/)){
			hasNumber = true;
		}
		if(s.charCodeAt() >= 65 && s.charCodeAt() <= 90){
			hasUpper = true;
		}
	}
	if (!hasNumber){
		ialert("密码必须含有一个数字");
		return false;
	}
	if (!hasUpper){
		ialert("密码必须含有一个大写字母");
		return false;
	}*/

	if(password!=repass){
		ialert("两次输入的密码不一致");
		return false;
	}

    checkSjyz(mobile,yzm,regtype)
    if(isTrue==0){
        ialert('验证码错误');
        return false;
    }

	$.ajax({
		url:"menu",
		data:{'fid':'login','act':'doreg','password':password, 'mobile':mobile,'regtype':regtype,'usrname':usrname,'nbrithday':nbrithday},
		type:"POST",
		dataType:'json',
		success:function(data){
			regUserCallback(data.R , mobile);
		}
	});
}


function regUserCallback(result , username){
	function GetRequest() {
 		var url = location.search; //获取url中"?"符后的字串
   		var theRequest = new Object();
	    if (url.indexOf("?") != -1) {
		   var str = url.substr(1);
		   strs = str.split("&");
		   for(var i = 0; i < strs.length; i ++) {
			 theRequest[strs[i].split("=")[0]]=(strs[i].split("=")[1]);
		   }
	    }
	    return theRequest;
	}
	var Request = new Object();
	Request = GetRequest();
	backUrl=Request["backUrl"];
	if ( result == '1' ){
		if(backUrl!=undefined){
			window.location.href=decodeURIComponent(backUrl);
		}else{
			window.location.href="menu";
		}
	}else if(result == '-4'){
		ialert("账号"+username+"是店铺会员，即将转到会员注册");
		window.location.href="menu?fid=login&act=reg&tel="+username;
		return false;
	}else if(result == '-3'){
		ialert("账号"+username+"不是店铺会员，即将转到店铺会员注册");
		window.location.href="menu?fid=login&act=vreg&tel="+username;
		return false;
	}else if(result == '-2'){
		ialert("注册失败");
		return false;
	}else if(result == '-1'){
		ialert("账号"+username+"已存在");
		return false;
	}
}

//短信验证码校验
function checkSjyz(mobile,val,type){
	$.ajax({
		async:false, 
        url:"menu?fid=login&act=ValidateNum",
        data:{
            'mobile':mobile,
            'val':val,
            'type':type
        },
        dataType:'json',
        success:function(res){
            if(res.error == 0){
            	if(type==1 || type==3){
            		isTrue=1;
            	}else if(type==2){
            		isTrue2=1;
            	}else{
            		isTrue3=1;
            	}
                return true;
            }else{
            	if(type==1  || type==3 ){
            		isTrue=0;
            	}else if(type==2){
            		isTrue2=0;
            	}else{
            		isTrue3=0;
            	}
                return false;
            }
        }
    });
}

function isMobile(mv){
	return mv.match(/^(0|86|17951)?(13[0-9]|15[012356789]|16[6]|17[0135678]|18[0-9]|19[0-9]|14[579])[0-9]{8}$/);
}

//获取短信验证码
function sjyz(mobile,type){
	if (mobile==""||!isMobile(mobile))
	{
		ialert("请输入正确的手机号码");
		return false;
	}

    $.ajax({
    	async:false, 
        url:"menu",
        data:{
            'fid':'login',
            'act':'sjyz',
            'mobile':mobile,
            'type':type
        },
        dataType:'json',
        success:function(res){
            if(res.error == 0){
                var obj=$(".btn_sjyz");
                obj.attr("disabled",true);
                obj.css("background-color",'#dddddd');
                setTimeout(function(){
                    obj.attr("disabled",false);
                	obj.css("background-color",'#00A0E9');
                },60000);
                ialert(res.msg);
                return false;
            }else{
                ialert(res.msg);
				if (res.error == -4)
				{	setTimeout(function(){
						window.location.href="menu?fid=login&act=vreg&tel="+mobile;
					 },1000);
				}
                return false;
            }
        }
    });
}

/*
$(function(){
    //判断是否存在该Cookie，存在则不执行，否则执行
    if(getCookie("remenber@iecshop")!=null&&getCookie("remenber@iecshop")!=""){
        //alert(getCookie("rps@hcrm"));
        var info=eval(getCookie("remenber@iecshop"))
        $("[name=yhxy]").attr("checked",true);
        $("[name=login_username]").val(info);
    }
});

//读取Cookie
function getCookie(name){ 
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg)){
        return unescape(arr[2]); 
    }else {
        return null; 
    }
} 

//删除Cookie
function delCookie(name){ 
    var exp = new Date(); 
    exp.setTime(exp.getTime() - 1); 
    var cval=getCookie(name); 
    if(cval!=null){
        document.cookie= name + "="+cval+";expires="+exp.toGMTString(); 
    }
} 

//设置Cookie
//这是有设定过期时间的使用示例： 
//s20是代表20秒 
//h是指小时，如12小时则是：h12 
//d是天数，30天则：d30 
//setCookie("name","hayden","s20");
function setCookie(name,value,time){ 
    var strsec = getsec(time); 
    var exp = new Date(); 
    exp.setTime(exp.getTime() + strsec*1); 
    document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString(); 
} 

function getsec(str){ 
   //alert(str); 
   var str1=str.substring(1,str.length)*1; 
   var str2=str.substring(0,1); 
   if (str2=="s"){ 
        return str1*1000; 
   }else if (str2=="h"){ 
       return str1*60*60*1000; 
   }else if (str2=="d"){ 
       return str1*24*60*60*1000; 
   } 
} 
*/

//清除提示
function clearRemark(){
	//$("div[name=username_remark]").html('');
	//$("div[name=password_remark]").html('');
	$("div[name=fail_remark]").html('');
}
