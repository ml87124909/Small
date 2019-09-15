

jQuery.extend({

	/**  

	 * 清除当前选择内容  

	 */  

	unselectContents: function(){

		if(window.getSelection)

			window.getSelection().removeAllRanges();

		else if(document.selection)

			document.selection.empty();

	}

});

jQuery.fn.extend({

	/**  

	 * 选中内容  

	 */  

	selectContents: function(){   

		$(this).each(function(i){   

			var node = this;   

			var selection, range, doc, win;   

			if ((doc = node.ownerDocument) &&   

				(win = doc.defaultView) &&   

				typeof win.getSelection != 'undefined' &&   

				typeof doc.createRange != 'undefined' &&   

				(selection = window.getSelection()) &&   

				typeof selection.removeAllRanges != 'undefined')   

			{   

				range = doc.createRange();   

				range.selectNode(node);   

				if(i == 0){   

					selection.removeAllRanges();   

				}   

				selection.addRange(range);   

			}   

			else if (document.body &&   

					 typeof document.body.createTextRange != 'undefined' &&   

					 (range = document.body.createTextRange()))   

			{   

				range.moveToElementText(node);   

				range.select();   

			}   

		});   

	},   

	/**  

	 * 初始化对象以支持光标处插入内容  

	 */  

	setCaret: function(){   

		if(!$.browser.msie) return;   

		var initSetCaret = function(){   

			var textObj = $(this).get(0);   

			textObj.caretPos = document.selection.createRange().duplicate();   

		};   

		$(this)   

		.click(initSetCaret)   

		.select(initSetCaret)   

		.keyup(initSetCaret);   

	},   

	/**  

	 * 在当前对象光标处插入指定的内容  

	 */  

	insertAtCaret: function(textFeildValue){   

	   var textObj = $(this).get(0);   

	   if(document.all && textObj.createTextRange && textObj.caretPos){   

		   var caretPos=textObj.caretPos;   

		   caretPos.text = caretPos.text.charAt(caretPos.text.length-1) == '' ?   

							   textFeildValue+'' : textFeildValue;   

	   }   

	   else if(textObj.setSelectionRange){   

		   var rangeStart=textObj.selectionStart;   

		   var rangeEnd=textObj.selectionEnd;   

		   var tempStr1=textObj.value.substring(0,rangeStart);   

		   var tempStr2=textObj.value.substring(rangeEnd);   

		   textObj.value=tempStr1+textFeildValue+tempStr2;   

		   textObj.focus();   

		   var len=textFeildValue.length;   

		   textObj.setSelectionRange(rangeStart+len,rangeStart+len);   

		   textObj.blur();   

	   }   

	   else {   

		   textObj.value+=textFeildValue;   

	   }   

	}   

}); 



jQuery.getScripts = function() {

	var urls = new Array();

	var callback;

	for (var i = 0; i<arguments.length; i++) {

		if (typeof arguments[i] == 'function') {

			callback = arguments[i];

		} else {

			urls.push(arguments[i]);

		}

	}

	var url = urls.shift();

	getscript(url);

	function getscript(url) {

		$.getScript(url, function() {

			url = urls.shift();

			getscript(url);

		});

	}

}



jQuery.getCss = function(url) {

	var fileref = document.createElement('link');

	fileref.setAttribute("rel", "stylesheet");

	fileref.setAttribute("type", "text/css");

	fileref.setAttribute("href", url);

	document.getElementsByTagName("head")[0].appendChild(fileref);

}



var cookie= {

	'prefix' : '',

	// 保存 Cookie

	'set' : function(name, value, seconds) {

		expires = new Date();

		expires.setTime(expires.getTime() + (1000 * seconds));

		document.cookie = this.name(name) + "=" + escape(value) + "; expires=" + expires.toGMTString() + "; path=/";

	},

	// 获取 Cookie

	'get' : function(name) {

		cookie_name = this.name(name) + "=";

		cookie_length = document.cookie.length;

		cookie_begin = 0;

		while (cookie_begin < cookie_length)

		{

			value_begin = cookie_begin + cookie_name.length;

			if (document.cookie.substring(cookie_begin, value_begin) == cookie_name)

			{

				var value_end = document.cookie.indexOf ( ";", value_begin);

				if (value_end == -1)

				{

					value_end = cookie_length;

				}

				return unescape(document.cookie.substring(value_begin, value_end));

			}

			cookie_begin = document.cookie.indexOf ( " ", cookie_begin) + 1;

			if (cookie_begin == 0)

			{

				break;

			}

		}

		return null;

	},

	// 清除 Cookie

	'del' : function(name) {

		var expireNow = new Date();

		document.cookie = this.name(name) + "=" + "; expires=Thu, 01-Jan-70 00:00:01 GMT" + "; path=/";

	},

	'name' : function(name) {

		return this.prefix + name;

	}

};



function message(msg, redirect, type) {

	if (parent == window) {

		 _message(msg, redirect, type);

	} else {

		parent.message(msg, redirect, type);

	}

	function _message(msg, redirect, type) {

		var modalobj = $('#modal-message');

		if(modalobj.length == 0) {

			$(document.body).append('<div id="modal-message" class="modal hide fade" tabindex="-1" role="dialog" aria-hidden="true"></div>');

			var modalobj = $('#modal-message');

		}

		if($.inArray(type, ['success', 'error', 'tips']) == -1) {

			type = '';

		}

		if(type == '') {

			type = redirect == '' ? 'error' : 'success';

		}

        var icons = {};

        icons['success'] = 'ok';

        icons['error'] = 'remove';

        icons['tips'] = 'exclamation-sign';

		html = '<div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="myModalLabel">系统提示</h3></div>' +

				'<div class="modal-body"><i class="icon-' + icons[type] + ' icon-large icon-3x pull-left"></i><div class="pull-left"><p>'+ msg +'</p>' +

				(redirect ? '<p><a href="' + redirect + '" target="main" data-dismiss="modal" aria-hidden="true">如果你的浏览器在<span id="timeout"></span>秒后没有自动跳转，请点击此链接</a></p>' : (redirect == 'back' ? '<p>[<a href="javascript:;" onclick="history.go(-1)">返回上一页</a>] &nbsp; [<a href="./?refresh">回首页</a>]</p></div></div>' : ''));

		modalobj.html(html);

		modalobj.addClass('alert alert-'+type);

		if(redirect) {

			var timer = '';

			timeout = 3;

			modalobj.find("#timeout").html(timeout);

			modalobj.on('shown', function(){doredirect();});

			modalobj.on('hide', function(){timeout = 0;doredirect(); });

			modalobj.on('hidden', function(){modalobj.remove();});

			function doredirect() {

				timer = setTimeout(function(){

					if (timeout <= 0) {

						modalobj.modal('hide');

						clearTimeout(timer);

						window.frames['main'].location.href = redirect;

						return;

					} else {

						timeout--;

						modalobj.find("#timeout").html(timeout);

						doredirect();

					}

				}, 1000);

			}

		}

		return modalobj.modal();

	}

}

/*

	请求远程地址

*/

function ajaxopen(url, callback) {

	$.getJSON(url+'&time='+new Date().getTime(), function(data){

		if (data.type == 'error') {

			message(data.message, data.redirect, data.type);

		} else {

			if (typeof callback == 'function') {

				callback(data.message, data.redirect, data.type);

			} else if(data.redirect) {

				location.href = data.redirect;	

			}

		}

	});	

	return false;

}

/*

	打开远程地址

	@params string url 目标远程地址

	@params string title 打开窗口标题，为空则不显示标题。可在返回的HTML定义<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>控制关闭

	@params object options 打开窗口的属性配置，可选项backdrop,show,keyboard,remote,width,height。具体参考bootcss模态对话框的options说明

	@params object events 窗口的一些回调事件，可选项show,shown,hide,hidden,confirm。回调函数第一个参数对话框JQ对象。具体参考bootcss模态对话框的on说明.



	@demo ajaxshow('url', 'title', {'show' : true}, {'hidden' : function(obj) {obj.remove();}});

*/

function ajaxshow(url, title, options, events) {

	var modalobj = $('#modal-message');

	var defaultoptions = {'remote' : url, 'show' : true};

	var defaultevents = {};

	var option = $.extend({}, defaultoptions, options);

	var events = $.extend({}, defaultevents, events);



	if(modalobj.length == 0) {

		$(document.body).append('<div id="modal-message" class="modal hide fade" tabindex="-1" role="dialog" aria-hidden="true" style="position:absolute;"></div>');

		var modalobj = $('#modal-message');

	}

	html = (typeof title != 'undefined' ? '<div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="myModalLabel">'+title+'</h3></div>' : '') +

			'<div class="modal-body"></div>' +

			'<div class="modal-footer">'+(typeof events['confirm'] == 'function' ? '<a href="#" class="btn btn-primary confirm">确定</a>' : '') + '<a href="#" class="btn" data-dismiss="modal" aria-hidden="true">关闭</a></div>';

	modalobj.html(html);

	if (typeof option['width'] != 'undeinfed' && option['width'] > 0) {

		modalobj.css({'width' : option['width'], 'marginLeft' : 0 - option['width'] / 2});

	}

	if (typeof option['height'] != 'undeinfed' && option['height'] > 0) {

		modalobj.find('.modal-body').css({'max-height' : option['height']});

	}

	if (events) {

		for (i in events) {

			if (typeof events[i] == 'function') {

				modalobj.on(i, events[i]);

			}

		}

	}

	modalobj.on('hidden', function(){modalobj.remove();});

	if (typeof events['confirm'] == 'function') {

		modalobj.find('.confirm', modalobj).on('click', events['confirm']);

	}

	return modalobj.modal(option);

}



/*

	根据html数据创建一个ITEM节点

*/

function buildAddForm(id, targetwrap) {

	var sourceobj = $('#' + id);

	var html = $('<div class="item">');

	id = id.split('-')[0];

	var size = $('.item').size();

	var htmlid = id + '-item-' + size;

	while (targetwrap.find('#' + htmlid).size() >= 1) {

		var htmlid = id + '-item-' + size++;

	}

	html.html(sourceobj.html().replace(/\(itemid\)/gm, htmlid));

	html.attr('id', htmlid);

	targetwrap.append(html);

	return html;

}

/*

	切换一个节点的编辑状态和显示状态

*/

function doEditItem(itemid) {

	$('#append-list .item').each(function(){

		$('#form', $(this)).css('display', 'none');

		$('#show', $(this)).css('display', 'block');		

	});

	var parent = $('#' + itemid);

	$('#form', parent).css('display', 'block');

	$('#show', parent).css('display', 'none');	

}



function doDeleteItem(itemid, deleteurl) {

	if (confirm('删除操作不可恢复，确认删除吗？')){

		if (deleteurl) {

			ajaxopen(deleteurl, function(){

				$('#' + itemid).remove();

			});

		} else {

			$('#' + itemid).remove();

		}	

	}

	return false;

}



function doDeleteItemImage(obj, url) {

	ajaxopen(url, function(){

		$(obj).parent().parent().find('#upload-file-view').html('');

	});

	return false;

}



function ignoreSpaces(string) {

	var temp = "";

	string = '' + string;

	splitstring = string.split(" ");

	for(i = 0; i < splitstring.length; i++)

	temp += splitstring[i];

	return temp;

}



//初始化kindeditor编辑器

var UE = null;

var UE_LOADED = false;

var UE_SELECTOR = new Array();

function kindeditor1(selector, callback) {

	UE_SELECTOR.push(selector);

	if (UE_LOADED) {

		return false;

	}

	UE_LOADED = true;

	if (!UE) {

		$.getScript('attachment/ueditor/ueditor.config.js', function(){

			$.getScript('attachment/ueditor/ueditor.all.js',function(){

				$.getScript('attachment/ueditor/lang/zh-cn/zh-cn.js',function(){

					UEditor(UE_SELECTOR, callback);

				});

			});

		});

	} else {

		UEditor(UE_SELECTOR, callback);

	}

}



//初始化ueditor编辑器

function kindeditor(selector, callback) {

	var selector = selector ? selector : 'textarea[class="richtext"]';

	var option = {

		toolbars:[

			['fullscreen', 'source', '|', 'undo', 'redo', '|',
                'bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', 'cleardoc', '|',
                'rowspacingtop', 'rowspacingbottom', 'lineheight', '|',
                'customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
                'directionalityltr', 'directionalityrtl', 'indent', '|',
                'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
                'link', 'unlink', 'anchor', '|', 'image', 'imageleft', 'imageright', 'imagecenter', '|',
                'insertimage', 'emotion', 'music', 'attachment', 'map', 'pagebreak',  'background', '|',
                'horizontal', 'date', 'time', 'spechars', 'snapscreen', 'wordimage', '|',
                'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols', 'charts', '|',
                 'searchreplace', 'help', 'drafts']

		],

		savePath : ['images'],

		imageFieldName : 'imgFile',

		imageUrl : '../../../../../index.php?act=attachment&do=ueupload',

		imagePath : './resource/attachment/'

	}

	$.each(selector, function(i, n){

		if ($(n).size() > 1) {

			$(n).each(function(){

				initUEditor(this);

			});

		} else {

			initUEditor($(n).get(0));

		}

	});



	function initUEditor(obj) {

		if ($(obj).get(0).tagName.toLowerCase() == 'textarea') {

			$(obj).css("margin","0");

			if(!$(obj).get(0).isload){

				$(obj).get(0).isload = true;

				var editor = new UE.ui.Editor(option);

				editor.render(obj);

				$(obj).parents('form').submit(function() {

					if (editor.queryCommandState('source')) {

						editor.execCommand('source');

					}

				});	

				if (typeof callback == 'function') {

					callback(obj, editor);

				}

			}

		}

	}

}



//初始化kindeditor编辑器
function kindeditor2(selector) {
	var selector = selector ? selector : 'textarea[class="richtext"]';
	var option = {
		basePath : 'attachment/kindeditor/',
		themeType : 'simple',
		langType : 'zh_CN',
		uploadJson : './index.php?act=attachment&do=upload',
		resizeType : 1,
		allowImageUpload : true,
		minWidth : '500px',
		items : [
			'undo', 'redo', '|', 'formatblock', 'fontname', 'fontsize', '|', 
			'forecolor', 'hilitecolor', 'bold', 'italic', 'underline', 'strikethrough', '|', 'justifyleft', 'justifycenter', 'justifyright', 'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', '|',
			'image', 'table', 'hr', 'emoticons', 'link', 'unlink', '|',
			'preview', 'plainpaste', '|', 'removeformat','source', 'fullscreen'
		]
	}
	if (typeof KindEditor == 'undefined') {
		$.getScript('attachment/kindeditor/kindeditor-min.js', function(){initKindeditor(selector, option)});
	} else {
		initKindeditor(selector, option);
	}
	function initKindeditor(selector, option) {
		var editor = KindEditor.create(selector, option);
	}
}

function kindeditorUploadBtn(obj, callback) {
	if (typeof KindEditor == 'undefined') {
		$.getScript('attachment/kindeditor/kindeditor-min.js', initUploader);
	} else {
		initUploader();
	}
	function initUploader() {
		var uploadbutton = KindEditor.uploadbutton({
			button : obj,
			fieldName : 'imgFile',
			url : 'attachment?action=upload',
			width : 100,
			afterUpload : function(data) {
				if (data.error === 0) {
					if (typeof callback == 'function') {
						callback(uploadbutton, data);
					} else {
						var url = KindEditor.formatUrl(data.url, 'absolute');
						$(uploadbutton.div.parent().parent()[0]).find('#upload-file-view').html('<input value="'+data.filename+'" type="hidden" name="'+obj.attr('fieldname')+'" id="'+obj.attr('id')+'-value" /><img src="'+url+'" width="100" />');
						$(uploadbutton.div.parent().parent()[0]).find('#upload-file-view').addClass('upload-view');
						$(uploadbutton.div.parent().parent()[0]).find('#upload-delete').show();
						$(uploadbutton.div.parent().parent()[0]).find('input[name=news-picture-old]').val(url);
					}
				} else {
					layer.alert('上传失败，错误信息：'+data.message);
				}
			},
			afterError : function(str) {
				layer.alert('上传失败，错误信息：'+str);
			}
		});	
		uploadbutton.fileBox.change(function(e) {
			uploadbutton.submit();
		});
	}
}




function fetchChildCategory(cid) {

	var html = '<option value="0">请选择二级分类</option>';

	if (!category || !category[cid]) {

		$('#cate_2').html(html);

		return false;

	}

	for (i in category[cid]) {

		html += '<option value="'+category[cid][i][0]+'">'+category[cid][i][1]+'</option>';

	}

	$('#cate_2').html(html);

}



function closetips() {

	$('#we7_tips').slideUp(100);

	cookie.set('we7_tips', '0', 4*3600);

}



function selectall(obj, name){

	$('input[name="'+name+'[]"]:checkbox').each(function() {

		$(this).attr("checked", $(obj).attr('checked') ? true : false);

	});

}



function tokenGen() {

	var letters = 'abcdefghijklmnopqrstuvwxyz0123456789';

	var token = '';

	for(var i = 0; i < 32; i++) {

		var j = parseInt(Math.random() * (31 + 1));

		token += letters[j];

	}

	$(':text[name="wetoken"]').val(token);

}



function colorpicker() {

	$(".colorpicker:visible").spectrum({

		className : 'colorpicker',

		showInput: true,

		showInitial: true,

		showPalette: true,

		maxPaletteSize: 10,

		preferredFormat: "hex",

		change: function(color) {

			$('#' + $(this).attr('target')).val(color.toHexString());

		},

		palette: [

			["rgb(0, 0, 0)", "rgb(67, 67, 67)", "rgb(102, 102, 102)", "rgb(153, 153, 153)","rgb(183, 183, 183)",

			"rgb(204, 204, 204)", "rgb(217, 217, 217)","rgb(239, 239, 239)", "rgb(243, 243, 243)", "rgb(255, 255, 255)"],

			["rgb(152, 0, 0)", "rgb(255, 0, 0)", "rgb(255, 153, 0)", "rgb(255, 255, 0)", "rgb(0, 255, 0)",

			"rgb(0, 255, 255)", "rgb(74, 134, 232)", "rgb(0, 0, 255)", "rgb(153, 0, 255)", "rgb(255, 0, 255)"],

			["rgb(230, 184, 175)", "rgb(244, 204, 204)", "rgb(252, 229, 205)", "rgb(255, 242, 204)", "rgb(217, 234, 211)",

			"rgb(208, 224, 227)", "rgb(201, 218, 248)", "rgb(207, 226, 243)", "rgb(217, 210, 233)", "rgb(234, 209, 220)",

			"rgb(221, 126, 107)", "rgb(234, 153, 153)", "rgb(249, 203, 156)", "rgb(255, 229, 153)", "rgb(182, 215, 168)",

			"rgb(162, 196, 201)", "rgb(164, 194, 244)", "rgb(159, 197, 232)", "rgb(180, 167, 214)", "rgb(213, 166, 189)",

			"rgb(204, 65, 37)", "rgb(224, 102, 102)", "rgb(246, 178, 107)", "rgb(255, 217, 102)", "rgb(147, 196, 125)",

			"rgb(118, 165, 175)", "rgb(109, 158, 235)", "rgb(111, 168, 220)", "rgb(142, 124, 195)", "rgb(194, 123, 160)",

			"rgb(166, 28, 0)", "rgb(204, 0, 0)", "rgb(230, 145, 56)", "rgb(241, 194, 50)", "rgb(106, 168, 79)",

			"rgb(69, 129, 142)", "rgb(60, 120, 216)", "rgb(61, 133, 198)", "rgb(103, 78, 167)", "rgb(166, 77, 121)",

			"rgb(133, 32, 12)", "rgb(153, 0, 0)", "rgb(180, 95, 6)", "rgb(191, 144, 0)", "rgb(56, 118, 29)",

			"rgb(19, 79, 92)", "rgb(17, 85, 204)", "rgb(11, 83, 148)", "rgb(53, 28, 117)", "rgb(116, 27, 71)",

			"rgb(91, 15, 0)", "rgb(102, 0, 0)", "rgb(120, 63, 4)", "rgb(127, 96, 0)", "rgb(39, 78, 19)",

			"rgb(12, 52, 61)", "rgb(28, 69, 135)", "rgb(7, 55, 99)", "rgb(32, 18, 77)", "rgb(76, 17, 48)"]

		]

	});



}



//隐藏显示切换 多处用到 勿动

$(function() {

	$('#adv-setting').click(function(){

		var a = $(this).attr('hideclass');

		if(this.checked) {

			$('.'+a).show();

		} else {

			$('.'+a).hide();

		}

	});

	$('#adv-setting').each(function() {

		var a = $(this).attr('hideclass');

		if(this.checked) {

			$('.'+a).show();

		} else {

			$('.'+a).hide();

		}		

	});

});

function gotopage(page){	

  //this.form.pageNo.value=page;  
  $("input[name=pageNo]").val(page);
 // alert($("input[name=pageNo]").val() + '' + $("input[name=total_pages]").val())
  if ($("input[name=pageNo]").val() < 1 ) $("input[name=pageNo]").val(1);
  if (parseInt($("input[name=pageNo]").val()) > parseInt($("input[name=total_pages]").val())) $("input[name=pageNo]").val($("input[name=total_pages]").val());
  
  $("form[name=frmMain]")[0].submit();
}

/**
 * 功能：用于显示输入框提示信息的函数
 * name 是 span id 的 前缀，span的 id 都统一命名为 对应输入框的name 属性，加上 后缀 _msg ,例如 xxx_msg
 * msg 是你要显示的信息，随便你写
 * type 是你要显示的信息类型 danger -红色 ,warning - 黄色, success - 绿色 , info - 蓝色
 * showHid 是 显示或者 隐藏的标志 show / hid
 */
function showOrHidMsg(name, msg, type, showHid){

	var needScroll = arguments[4] ? arguments[4] :'scroll';  /*默认是滚动*/

    var span_id = name+'_msg' ;
    var span_obj = $('#'+span_id);
    var txt = $.trim(msg);
    var showOrHid = $.trim(showHid);
    var sType = $.trim(type);
    
    if(txt.length <= 0){
        txt = '&nbsp;&nbsp;';
    }
    
    if(showOrHid=='show'){
        showOrHid = 'inline';
    }else{
        showOrHid = 'none';
    }
    
    if(sType.length <= 0){
        sType = 'info';
    }
    
    switch(sType){
        case 'danger':
            span_obj.removeClass().addClass('alert alert-danger');
            break;
        case 'warning':
            span_obj.removeClass().addClass('alert alert-warning');
            break;
        case 'success':
            span_obj.removeClass().addClass('alert alert-success');
            break;
        default:
            span_obj.removeClass().addClass('alert alert-info');
            break;
    }
    
    span_obj.html(txt);
    
    span_obj.css('marginLeft','5px');
    span_obj.css('paddingTop','5px');
    span_obj.css('paddingBottom','7px');
    
    span_obj.css('display',showOrHid);
	
	if(showOrHid=='inline' && (type=="danger" || type=="warning") && needScroll=='scroll'){
		var ot = 0;
		try{
			var ot = (($("#"+span_id).offset().top - 80) <= 0 ? 0 : ($("#"+span_id).offset().top - 80));
		}catch(e){
			ot = 0;
		}
		$('body,html').animate({scrollTop:ot},1000); /*将页面滚回顶部方便显示错误信息*/
	}
	
    
}

/**
 * 功能：用于显示输入框提示信息的函数
 * name 是 span id 的 前缀，span的 id 都统一命名为 对应输入框的name 属性，加上 后缀 _msg ,例如 xxx_msg
 * msg 是你要显示的信息，随便你写
 * type 是你要显示的信息类型 danger -红色 ,warning - 黄色, success - 绿色 , info - 蓝色
 * showHid 是 显示或者 隐藏的标志 show / hid
 */
function showOrHid_popMsg(name, msg, type, showHid){

	var needScroll = arguments[4] ? arguments[4] :'scroll';  /*默认是滚动*/

    var txt = $.trim(msg);
    var showOrHid = $.trim(showHid);
    var sType = $.trim(type);
	
	var jqObj = $($("[name='"+name+"']")[0])
    
    if(txt.length <= 0){
        txt = '&nbsp;&nbsp;';
    }
    
    if(showOrHid=='show'){
        showOrHid = 'inline';
    }else{
        showOrHid = 'none';
    }
    
    if(sType.length <= 0){
        sType = 'info';
    }
    
    switch(sType){
        case 'danger':
            span_obj.removeClass().addClass('alert alert-danger');
            break;
        case 'warning':
            span_obj.removeClass().addClass('alert alert-warning');
            break;
        case 'success':
            span_obj.removeClass().addClass('alert alert-success');
            break;
        default:
            span_obj.removeClass().addClass('alert alert-info');
            break;
    }
    
    span_obj.html(txt);
    
    span_obj.css('marginLeft','5px');
    span_obj.css('paddingTop','5px');
    span_obj.css('paddingBottom','7px');
    
    span_obj.css('display',showOrHid);
	
	jqObj.popover({
		title : '温馨提示',
		content: txt
	});
	
	if( showOrHid=='inline' ) {
		jqObj.popover('show');
	}else{
		jqObj.popover('hide');
	}
	
	if(showOrHid=='inline' && (type=="danger" || type=="warning") && needScroll=='scroll'){
		var ot = 0;
		try{
			var ot = (($("#"+span_id).offset().top - 80) <= 0 ? 0 : ($("#"+span_id).offset().top - 80));
		}catch(e){
			ot = 0;
		}
		$('body,html').animate({scrollTop:ot},1000); /*将页面滚回顶部方便显示错误信息*/
	}
	
    
}


function main_delete(del_pk){    
  //主GRID的删除操作 	
	layer.confirm('你确信要删除记录吗？', {
		btn: ['是','否'] //按钮
	}, function(index,layero){
	    layer.close(index);
	    layer.load()
	    $("input[name=pk]").val(del_pk);
		$("input[name=part]").val('delete');
		var viewid=$("input[name=viewid]").val();
	    var form = new FormData(document.getElementById("frmMain"));
        $.ajax({
            url:"admin?viewid="+viewid+"&part=delete",
            type:"post",
            data:form,
            processData:false,
            contentType:false,
            success:function(data){
                layer.closeAll();
                if (data.code=='0'){
                    layer.msg(data.MSG);
                    setTimeout("location.reload()", 2000);
                }else{
                    layer.msg(data.MSG);
                }
            }
        });
		//$("input[name=pk]").val(del_pk);
		//$("input[name=part]").val('delete');
		//$("form[name=frmMain]")[0].submit();
	}, function(){
		layer.closeAll();
	});
 
}



function ajax_delete(del_pk){
  //主GRID的删除操作
	layer.confirm('你确信要删除记录吗？', {
		btn: ['是','否'] //按钮
	}, function(index,layero){
	    layer.close(index);
	    $.ajax({
            url:sUrl+"&part=ajax_delete&pk="+del_pk,
            async:false,
            success: function(data){
                layer.msg(data.MSG);
                location.reload();
            }
        });

	}, function(){
		layer.closeAll();
	});

}

function ajax_del(del_pk){
  //主GRID的删除操作
	layer.confirm('你确信要删除记录吗？', {
		btn: ['是','否'] //按钮
	}, function(index,layero){
	    layer.close(index);
	    $.ajax({
            url:sUrl+"&part=ajax_del&pk="+del_pk,
            async:false,
            success: function(data){
                layer.msg(data.MSG);
                location.reload();
            }
        });

	}, function(){
		layer.closeAll();
	});

}

function searchtblData(){
	var ctrl = $(".searchtbl input[type=text],.searchtbl select");
	var data = {};
	for(var i=0;i<ctrl.length;i++){
		data[ctrl.eq(i).attr('name')] = ctrl.eq(i).val();
	}
	var u = '';
	for (var k in data)
	{
		if (data[k] && data[k] != '')
		{
			u += '&' + k + "=" + data[k];
		}
	}
	return u;
}

function main_excel(){
	$("input[name=pk]").val('');
	$("input[name=pageNo]").val('1');
	$("input[name=part]").val('excel');  
	$("form[name=frmMain]")[0].submit(); 
}


function main_search(){
	$("input[name=pk]").val('');
	$("input[name=pageNo]").val('1');
	$("input[name=part]").val('list');
	$("form[name=frmMain]")[0].submit(); 
}

function main_update(pk){
	 //$("input[name=pk]").val(pk);
	 //$("input[name=mode]").val('upd');
	 //$("input[name=part]").val('localfrm');                
	pageNo = $("input[name=pageNo]").val();   
	window.location = sUrl + "&mode=upd&pageNo=" + pageNo + "&part=localfrm&pk=" + pk + searchtblData();
}

function main_add(){
	//alert(sUrl)
	window.location = sUrl + "&mode=add&pageNo=1&part=localfrm";
}

function main_view(pk){
	//$("input[name=pk]").val(pk);
	// $("input[name=mode]").val('view');
	// $("input[name=part]").val('localfrm');                
	//$("form[name=frmMain]")[0].submit();   
	pageNo = $("input[name=pageNo]").val(); 
	window.location = sUrl + "&pageNo=" + pageNo + "&part=localfrm&pk=" + pk+ searchtblData();
}

function main_do(pk,method,text){ 
 //主GRID的操作 
	if (text=='')
	{	text = '处理';
	}
	layer.confirm('你确定要'+text+'该记录吗？', {
		btn: ['是','否'] //按钮
	}, function(){
		fid =  $("input[name=fid]").val();
		url =  "admin?fid="+fid+"&part=ajax&action="+method+"&pk="+pk,
        data=sendXMLHTTP(url);
		if (data == 1)
		{
			layer.alert(text+'成功',{},function(){$("form[name=frmMain]")[0].submit(); });
		}
		else{
			layer.alert(text+'失败');
		}
	}, function(){
		layer.closeAll();
		$("form[name=frmMain]")[0].submit(); 
	});
	
}

function formcheck(form){
	var viewid=$("input[name=viewid]").val();
	if(formcheck_2(form)){

		$("input[name=part]").val('insert');  
		$("#div_mul_btns").hide();
		var form = new FormData(document.getElementById("frmMain"));
        $.ajax({
            url:"admin?viewid="+viewid+"&part=insert",
            type:"post",
            data:form,
            processData:false,
            contentType:false,
            success:function(data){
                if (data.code=='0'){
                    layer.msg(data.MSG);

                     if (data.pk!=''){
                        window.location = sUrl + "&pageNo=" + pageNo + "&part=localfrm&pk=" + data.pk+ searchtblData();
                        setTimeout(window.location, 5000);
                    }else{
                        setTimeout(location.reload(), 5000);
                    }

                }else{
                    layer.msg(data.MSG);
                    $("#div_mul_btns").show();
                }
            }
        });
        return false;
	}else{
		
		return false;
	
	}


}

function formcheck_2(form){
            return true;
        }  


function sendXMLHTTP(sURL){
  //发送一个http请求获并得返回值
  var sResult='';
  if(window.ActiveXObject) //判断是否是IE内核,是就执行以下代码,如果不是,就执行else if部分.
    {
        xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    else
    {
        xmlHttp=new XMLHttpRequest();
    }
  xmlHttp.open("get", sURL, false);
  xmlHttp.send();
  sResult=xmlHttp.responseText;
  return sResult;
}



function isEmpty (str) {
  str=mystrip(str);
  if ((str==null)||(str.length==0)) return true;
  else return(false);
}
function mystrip(str){
   var i = 0;
   var len = str.length;
   if ( str == "" ) return( str );
   j = len -1;
   flagbegin = true;
   flagend = true;

   while (( flagbegin == true) && (i< len)){
     if ( str.charAt(i) == " " ){
        i=i+1;
        flagbegin=true;
     }else{
        flagbegin=false;
     }
   }

   while  ((flagend== true) && (j>=0)){
     if (str.charAt(j)==" "){
       j=j-1;
       flagend=true;
     }else{
       flagend=false;
     }
   }

   if ( i > j ) return ("");
   trimstr = str.substring(i,j+1);
   return trimstr;
}

function nisEmpty(s){
	//增加判断空格
     var ns =String(s);
     ns=ns.replace(/(^\s+)|(\s+$)/g, "");
     if(ns==""||ns.length==0)return true;
     else{return false;}
}

/* 查空值
* inputName 是 要校验的对象的name属性
* errMsg  是 假如校验出为空 ，就显示的信息
*/
function check_null(inputName,errMsg){
	var res = false;
	var param = $.trim($($("input[name='"+inputName+"']")[0]).val());
	if( !isEmpty(param) ){
              showOrHidMsg(inputName,'','info','hid','noScroll');
			  res = true;
            }else{
              showOrHidMsg(inputName,errMsg,'danger','show','noScroll');
             }
    return res;
  }

function onlyNum(event,obj){ 
                    //响应鼠标事件，允许左右方向键移动 
                    
                    event = window.event||event; 
                    if(event.keyCode == 37 | event.keyCode == 39){ 
                        return; 
                    } 
                    //先把非数字的都替换掉，除了数字和. 
                    obj.value = obj.value.replace(/[^\d.]/g,""); 
                    //必须保证第一个为数字而不是. 
                    obj.value = obj.value.replace(/^\./g,""); 
                    //保证只有出现一个.而没有多个. 
                    obj.value = obj.value.replace(/\.{2,}/g,"."); 
                    //保证.只出现一次，而不能出现两次以上 
                    obj.value = obj.value.replace(".","$#$").replace(/\./g,"").replace("$#$","."); 
                    testKeyUpFloat(obj,6);//精确到2位小数
                } 

function onlyNum_test(event,obj){ 
                    //响应鼠标事件，允许左右方向键移动 
                    event = window.event||event; 
                    if(event.keyCode == 37 | event.keyCode == 39){ 
                        return; 
                    } 
                    //先把非数字的都替换掉，除了数字和. 
                    obj.value = obj.value.replace(/[^\d.]/g,""); 
                    //必须保证第一个为数字而不是. 
                    obj.value = obj.value.replace(/^\./g,""); 
                    //保证只有出现一个.而没有多个. 
                    obj.value = obj.value.replace(/\.{2,}/g,"."); 
                    //保证.只出现一次，而不能出现两次以上 
                    obj.value = obj.value.replace(".","$#$").replace(/\./g,"").replace("$#$","."); 
                } 

function onlyNum_fixed(event,obj,n){ 
    //响应鼠标事件，允许左右方向键移动 
    
    event = window.event||event; 
    if(event.keyCode == 37 | event.keyCode == 39){ 
        return; 
    } 
    //先把非数字的都替换掉，除了数字和. 
    obj.value = obj.value.replace(/[^\d.]/g,""); 
    //必须保证第一个为数字而不是. 
    obj.value = obj.value.replace(/^\./g,""); 
    //保证只有出现一个.而没有多个. 
    obj.value = obj.value.replace(/\.{2,}/g,"."); 
    //保证.只出现一次，而不能出现两次以上 
    obj.value = obj.value.replace(".","$#$").replace(/\./g,"").replace("$#$","."); 
    testKeyUpFloat(obj,n);//精确到n位小数
} 


function testKeyUpFloat(obj,num){
	//在onkeyup事件中判断浮点数 保存后num位
	nNum=num+1
	var re = new RegExp("\\.\\d{"+nNum+",}");
    obj.value=obj.value.replace(/^[0]+\d{1}/,obj.value.charAt(obj.value.search(/[1-9]{1}/)==-1?0:obj.value.search(/[1-9]{1}/))); //处理开头为零接数字
    obj.value=obj.value.replace(/[^0-9,\.]{1}/g,"");   //处理非(数字、点)
    obj.value=obj.value.replace(/\.{2,}/g,".");       //处理两个以上的点
	obj.value=obj.value.replace(/^\.{1}/g,"");      //处理头部"."
	//if(obj.value.match(/\.{1}\d*\.+$/)){obj.value=obj.value.slice(0,-1);}
	
	if(obj.value.match(/^\d+\.{1}\d+\.+/)){obj.value=obj.value.slice(0,obj.value.indexOf('.',obj.value.search(/\.+/)+1));}     //处理复制到输入框的多点分隔情况(123.12.1231)
    if(obj.value.match(re)){            //保留num位,截断后面的数字
        obj.value=obj.value.slice(0,obj.value.search(re)+nNum);
    }
}

function isEmpty(str){
	if(str == ""){
		return true;
	}
	return false;
}

function isDate(sDate) {
	var iYear, iMonth, iDay, iIndex

	var	reg
	reg = new RegExp('[^0-9-]','')
	if (sDate.search(reg) >= 0)
		return false;
	
	iIndex = sDate.indexOf('-');
	if ( iIndex == -1 )
		return false;
	else {
		iYear = parseFloat(sDate.substr(0, iIndex));
		if ( isNaN(iYear) || iYear < 1900 || iYear > 2099 )
			return false;
		else
			sDate = sDate.substring(iIndex + 1, sDate.length);
	}
	
	iIndex = sDate.indexOf('-');
	if ( iIndex == -1 )
		return false;
	else {
		iMonth = parseFloat(sDate.substr(0, iIndex));
		if ( isNaN(iMonth) || iMonth < 1 || iMonth > 12 )
			return false;
		else
			sDate = sDate.substring(iIndex + 1, sDate.length);
	}
	
	iIndex = sDate.indexOf('-');
	if ( iIndex >= 0 )
		return false;
	else {
		iDay = parseFloat(sDate);
		if ( isNaN(iDay) || iDay < 1 || iDay > 31 )
			return false;
	}

	switch(iMonth) {
		case 4:
		case 6:
		case 9:
		case 11:
			if ( iDay > 30 )
				return false;
			else
				break;
		case 2:
			if ( ( ( iYear % 4 == 0 && iYear % 100 != 0 ) || iYear % 400 == 0 ) && iDay > 29 )
				return false;
			else if ( (iYear % 4 != 0 || (iYear % 100 == 0 && iYear % 400 != 0)) && iDay > 28 )
				return false;
			else
				break;
		default:
	}
	return true;
}

function isEmail(s){
   if (s.length > 100){
       window.alert("Email地址长度不能超过100位!");
       return false;
   }

   var regu = "^(([0-9a-zA-Z]+)|([0-9a-zA-Z]+[_.0-9a-zA-Z-]*[0-9a-zA-Z]+))@([a-zA-Z0-9-]+[.])+([a-zA-Z]{2}|net|com|gov|mil|org|edu|int)$"
   var re = new RegExp(regu);
   if (s.search(re) != -1){
      return true;
   }else{
      window.alert ("请输入有效合法的E-mail地址 ！")
      return false;
   }
}

function checkEmail(s){
   if (s.length > 100){
       //window.alert("Email地址长度不能超过100位!");
       return false;
   }

   var regu = "^(([0-9a-zA-Z]+)|([0-9a-zA-Z]+[_.0-9a-zA-Z-]*[0-9a-zA-Z]+))@([a-zA-Z0-9-]+[.])+([a-zA-Z]{2}|net|com|gov|mil|org|edu|int)$"
   var re = new RegExp(regu);
   if (s.search(re) != -1){
      return true;
   }else{
      //window.alert ("请输入有效合法的E-mail地址 ！")
      return false;
   }
}

function checkPhone(str){
	var reg = /^(((13[0-9]{1})|(14[0-9]{1})|(15[0-9]{1})|(17[0-9]{1})|(18[0-9]{1}))+\d{8})$/; 
	return reg.test(str);
}

function checkNumber(str)
{
     var re = /^[0-9]+.?[0-9]*$/;   //判断字符串是否为数字     //判断正整数 /^[1-9]+[0-9]*]*$/  

    str = rmoney(str);
     if (!re.test(str))
    {
        return false;
     }else{
		return true;
	 }
}
function checkMoney(str)
{
     if (str.indexOf(".") != -1)
     {
		 return true;
     }else{
		return false;
	 }
}
function checkNumber2(str)
{
     var re = /^[0-9]+[0-9]*]*$/;   //判断字符串是否为数字     //判断正整数 /^[1-9]+[0-9]*]*$/  

    
     if (!re.test(str))
    {
        return false;
     }else{
		return true;
	 }
}

//限制只能输入数字,配合onkeyup使用，传input对象
function checkNum(obj){
    if(!$(obj).val().match(/^\d+$/)){
        $(obj).val('');
    }
}

function main_delete_list(){    
    //主GRID的删除操作
    var check_lines = $("input[name='check_line']:checked"); //所有 check_lines 的 元素lie表
    if (check_lines.length > 0) {
        $("input[name=part]").val('delete');  
        $("form[name=frmMain]")[0].submit(); 
    }else{
        alert('请选择一个记录，再删除');
        return false;
    }
    
}


/*信息提交后弹窗*/
function InfosubmitPop(error,MSG,clickfun){
	$(".bigbackframe").bigbackfrm();
	var infopop = $(".InfoFrame").popfrm({background:".bigbackframe"}); 
	$("#InfoPopMain").html(MSG);
	
	if (error == 0){
		//成功
		$("#InfoImg").removeClass('InfoImg-fail');
		$("#InfoImg").addClass('InfoImg-success');
	}else{
		//失败
		$("#InfoImg").removeClass('InfoImg-success');
		$("#InfoImg").addClass('InfoImg-fail');			
	}
	//按钮'
	var btn_html = '<input type="button" id="infopop_btn" name="infopop_btn" class="infopop_btn" value="确定" onclick="InfosubmitHidePop();'+clickfun.toString()+'" />';
	$("#InfoBtnDiv").html(btn_html);
	
	infopop.showpop();
}
/*日历文章弹框*/
function myInfosubmitPop(MSG,clickfun){
	$(".bigbackframe").mybigbackfrm();
	var infopop = $(".InfoFrame").popfrm({background:".bigbackframe"}); 
	$("#InfoPopMain").html(MSG);
	
	//var	wholepage='<span onclick="wholepage()">弹出页面</span>';
	var	clse='<span onclick="InfosubmitHidePop()">关闭</span>';
	var mydateid='<span id ="mydateid" name="mydateid">'+clickfun.toString()+'</span>'
	$(".tit").html(clse+'&nbsp;&nbsp;&nbsp;'+mydateid);
	
	//关闭
	//var btn_html = '<input type="button" id="infopop_btn" name="infopop_btn" class="infopop_btn" value="关闭" onclick="InfosubmitHidePop();'+clickfun.toString()+'" />';
	
	//$("#InfoBtnDiv").html(btn_html);
	//$(".InfoMain").html(r);
	infopop.showpop();
}
function InfosubmitHidePop(){
	$(".bigbackframe").bigbackfrm();
	var infopop = $(".InfoFrame").popfrm({background:".bigbackframe"});
	infopop.hidepop();
}
function wholepage(){
	$(".bigbackframe").mybigbackfrm();
	var infopop = $(".InfoFrame").popfrm({background:".bigbackframe","margin-left": 10 , 
					"margin-top":10});
	
	
	infopop.showpop();
}

var pay_callback = null;
//微信支付
function wzhifu(out_trade_no){
	pay_callback = arguments[1] ? arguments[1] : null;
	$.ajax({
		async:false, 
        url:"menu",
        data:{
            'fid':'wzhifu',
            'act':'unifiedOrder',
            'out_trade_no':out_trade_no
        },
        dataType:'json',
        success:function(d){
            if(d.code==0){
				WeixinJSBridge.invoke(
				'getBrandWCPayRequest',
				d.data,
				function(res){
					if(res.err_msg == "get_brand_wcpay_request:ok" ){
						$.ajax({
							async:false, 
					        url:"menu",
					        data:{
					            'fid':'wzhifu',
					            'act':'queryOrder',
					            'out_trade_no':d.out_trade_no
					        },
					        dataType:'json',
					        success:function(d0){
								if(d0.code==2){
									ialert(d0.msg);
								}
									setTimeout(function(){
										if (d0.r_table != 'hd_vip_cz_wx')
										{
											window.location.href = "menu?fid=C001&act=order&code="+d.out_trade_no;
										}
										else{
											window.location.href = "menu?fid=F001&act=order&code="+d.out_trade_no;
										}
										
									},800);
					        }
					    });
					}
				})
			}else if(d.code==3){
				ialert(d.msg);
				return false;
			}else{
				ialert(d.msg);
				return false;
			}
        }
    });
}


function bwzhifu(out_trade_no,srfid){
	$.ajax({
		async:false, 
		url:"menu",
		data:{
			'fid':'wzhifu',
			'act':'queryOrder',
			'out_trade_no':d.out_trade_no,
			'srfid':srfid
		},
		dataType:'json',
		success:function(d0){           
				return true;
		}
	});
}
/*
//锁定表头和列
function FixTable(TableID, FixColumnNumber, width, height) {
    //TableID            要锁定的Table的ID
    //FixColumnNumber    要锁定列的个数
    //width              显示的宽度
    //height             显示的高度
    if ($("#" + TableID + "_tableLayout").length != 0) {
        $("#" + TableID + "_tableLayout").before($("#" + TableID));
        $("#" + TableID + "_tableLayout").empty();
    }
    else {
        $("#" + TableID).after("<div id='" + TableID + "_tableLayout' style='overflow:hidden;height:" + height + "px; width:" + width + "px;'></div>");
    }
    $('<div id="' + TableID + '_tableFix"></div>'
    + '<div id="' + TableID + '_tableHead"></div>'
    + '<div id="' + TableID + '_tableColumn"></div>'
    + '<div id="' + TableID + '_tableData"></div>').appendTo("#" + TableID + "_tableLayout");
    var oldtable = $("#" + TableID);
    var tableFixClone = oldtable.clone(true);
    tableFixClone.attr("id", TableID + "_tableFixClone");
    $("#" + TableID + "_tableFix").append(tableFixClone);
    var tableHeadClone = oldtable.clone(true);
    tableHeadClone.attr("id", TableID + "_tableHeadClone");
    $("#" + TableID + "_tableHead").append(tableHeadClone);
    var tableColumnClone = oldtable.clone(true);
    tableColumnClone.attr("id", TableID + "_tableColumnClone");
    $("#" + TableID + "_tableColumn").append(tableColumnClone);
    $("#" + TableID + "_tableData").append(oldtable);
    $("#" + TableID + "_tableLayout table").each(function () {
        $(this).css("margin", "0");
    });
    var HeadHeight = $("#" + TableID + "_tableHead thead").height();
    HeadHeight += 2;
    $("#" + TableID + "_tableHead").css("height", HeadHeight);
    $("#" + TableID + "_tableFix").css("height", HeadHeight);
    var ColumnsWidth = 0;
    var ColumnsNumber = 0;
    $("#" + TableID + "_tableColumn tr:first td:lt(" + FixColumnNumber + ")").each(function () {
        ColumnsWidth += $(this).outerWidth(true);
        ColumnsNumber++;
    });
    ColumnsWidth += 2;
    if ($.browser.msie) {
        switch ($.browser.version) {
            case "7.0":
                if (ColumnsNumber >= 3) ColumnsWidth--;
                break;
            case "8.0":
                if (ColumnsNumber >= 2) ColumnsWidth--;
                break;
        }
    }
    $("#" + TableID + "_tableColumn").css("width", ColumnsWidth);
    $("#" + TableID + "_tableFix").css("width", ColumnsWidth);
    $("#" + TableID + "_tableData").scroll(function () {
        $("#" + TableID + "_tableHead").scrollLeft($("#" + TableID + "_tableData").scrollLeft());
        $("#" + TableID + "_tableColumn").scrollTop($("#" + TableID + "_tableData").scrollTop());
    });
    $("#" + TableID + "_tableFix").css({ "overflow": "hidden", "position": "relative", "z-index": "50", "background-color": "Silver" });
    $("#" + TableID + "_tableHead").css({ "overflow": "hidden", "width": width - 17, "position": "relative", "z-index": "45", "background-color": "white" });
    $("#" + TableID + "_tableColumn").css({ "overflow": "hidden", "height": height - 17, "position": "relative", "z-index": "40", "background-color": "white" }); //Silver
    $("#" + TableID + "_tableData").css({ "overflow": "scroll", "width": width, "height": height, "position": "relative", "z-index": "35" });
    if ($("#" + TableID + "_tableHead").width() > $("#" + TableID + "_tableFix table").width()) {
        $("#" + TableID + "_tableHead").css("width", $("#" + TableID + "_tableFix table").width());
        $("#" + TableID + "_tableData").css("width", $("#" + TableID + "_tableFix table").width() + 17);
    }
    if ($("#" + TableID + "_tableColumn").height() > $("#" + TableID + "_tableColumn table").height()) {
        $("#" + TableID + "_tableColumn").css("height", $("#" + TableID + "_tableColumn table").height());
        $("#" + TableID + "_tableData").css("height", $("#" + TableID + "_tableColumn table").height() + 27);
    }
    $("#" + TableID + "_tableFix").offset($("#" + TableID + "_tableLayout").offset());
    $("#" + TableID + "_tableHead").offset($("#" + TableID + "_tableLayout").offset());
    $("#" + TableID + "_tableColumn").offset($("#" + TableID + "_tableLayout").offset());
    $("#" + TableID + "_tableData").offset($("#" + TableID + "_tableLayout").offset());
}
*/
function fixedNum(v,e){
	var t = 1;
	for(;e>0;t*=10,e--);
	for(;e<0;t/=10,e++);
	return Math.round(v*t)*t;
}

function changeNTF(value,num){
	return parseFloat(value).toFixed(num);
}

function InitNum(val){
	if(val==""||val==undefined){
		return '0';
	}else{
		return ''+val;
	}
}

//把有逗号分隔的金额还原成浮点数
function rmoney(s) { 
	return parseFloat(s.replace(/[^\d\.-]/g, "")); 
}

//金额格式化函数。可以控制小数位数，自动四舍五入
function fmoney(s, n){   
   n = n > 0 && n <= 20 ? n : 2;   
   s = parseFloat((s + "").replace(/[^\d\.-]/g, "")).toFixed(n) + "";   
   var l = s.split(".")[0].split("").reverse(),   
   r = s.split(".")[1];   
   t = "";   
   for(i = 0; i < l.length; i ++ )   
   {   
      t += l[i] + ((i + 1) % 3 == 0 && (i + 1) != l.length ? "," : "");   
   }   
   return t.split("").reverse().join("") + "." + r;   
}

function addsave(){
	$("form[name='frmMain']").append('<input name="save" type="hidden" value="0">');
}

function auditsave(){
	$("form[name='frmMain']").append('<input name="save" type="hidden" value="1">');
}

function unauditsave(){
	var pk = $("input[name=pk]").val();
	if (pk !='')
	{	
		$("form[name='frmMain']").append('<input name="save" type="hidden" value="2">');
		$("form[name='frmMain']")[0].submit();
	}
	else{
		alert('此单据未审核，不能反审！');
		return false;
	}
	
}

function unauditsave2(){
	var fid = $("input[name=fid]").val();
	var pk = $("input[name=pk]").val();
	if (pk !='')
	{	url =  "admin?fid="+fid+"&part=ajax&action=getVStatus&pk="+pk,
        data=sendXMLHTTP(url);
        if(data == 1 ){
			if (confirm("您确定反审此单据吗？")){
				url =  "admin?fid="+fid+"&part=ajax&action=createStore&save=2&pk="+pk,
				data=sendXMLHTTP(url);
				if (data == 0)
				{
					alert('单据反审成功！');
					window.location.reload();
				}
				else{
					alert(data);
					return false;
					}
			 }
			 else{
				return false;
			 }
		}
		else{
			alert("此单不能反审！");
            return false;
		}

	}
	else{
		alert('请选择单据！');
		return false;
	}
	
}

function auditsave2(){
	var fid = $("input[name=fid]").val();
	var pk = $("input[name=pk]").val();
	if (pk !='')
	{	url =  "admin?fid="+fid+"&part=ajax&action=getVStatus&pk="+pk,
        data=sendXMLHTTP(url);
        if(data == 0 || data == 2 ){
           if (confirm("您确定审核此单据吗？")){
				url =  "admin?fid="+fid+"&part=ajax&action=createStore&save=1&pk="+pk,
				data=sendXMLHTTP(url);
				if (data == 0)
				{
				  alert('单据审核成功！');
				  window.location.reload();
				}
				else{
					alert(data);
					return false;
					}
             }
            else{
                 return false;
                }
            }
        else{
             alert("此单不能审核！");
             return false;
        }
	}
	else{
		alert('请选择单据！');
		return false;
	}
	
}

function isEmpty(str) {
    str = mystrip(str);
    if ((str == null) || (str.length == 0)) return true;
    else return (false);
}
//禁止拖拽事件
$(function(){
	document.ondragstart = function() {
	    return false;
	};
	$("form[name=frmMain] .table.table-bordered tr:nth-child(odd)").hover(function(){
		$(this).attr('bgcolor','#F2F7FB');
	},function(){
		$(this).attr('bgcolor','#ffffff');
	});
	$("form[name=frmMain] .table.table-bordered tr:nth-child(even)").hover(function(){
		$(this).css("background-color","#F2F7FB")
	},function(){
		$(this).css('background-color','#F4F2F3');
	});
});

function accAdd(arg1,arg2){ 
	var r1,r2,m; 
	try{r1=arg1.toString().split(".")[1].length}catch(e){r1=0} 
	try{r2=arg2.toString().split(".")[1].length}catch(e){r2=0} 
	m=Math.pow(10,Math.max(r1,r2)); 
	return (arg1*m+arg2*m)/m; 
} 
function accMul(arg1,arg2) 
{ 
	var m=0,s1=arg1.toString(),s2=arg2.toString(); 
	try{m+=s1.split(".")[1].length}catch(e){} 
	try{m+=s2.split(".")[1].length}catch(e){} 
	return Number(s1.replace(".",""))*Number(s2.replace(".",""))/Math.pow(10,m) ;
}

function fullscreen(){
	if($("body").hasClass("fullscreen")){
		$("body").removeClass("fullscreen");
	}else{
		$("body").addClass("fullscreen");
	}
}

$(function(){
	$("input[name=qqid]").keydown(function(event){
		if(event.keyCode == 13){
			main_search()	;
		}
		//main_search()	
	});
	$(".nav-parent .children li").hover(function(){
		$(this).addClass("on-hover");
	},function(){
		$(this).removeClass("on-hover");
	});

	$(".nav-parent").find("a:eq(0)").click(function(){
		if(!$("body").hasClass("fullscreen")){
			if($(this).parent().hasClass("nav-active")){
				$(this).parent().removeClass("nav-active");
				$(this).parent().find(".children").slideUp(300);
			}else{
				$(this).parent().addClass("nav-active");
				$(this).parent().find(".children").slideDown(300);
				var other = $(".nav-parent").not($(this).parent());
				other.removeClass("nav-active");
				other.find(".children").slideUp(300);
			}
		}
		return false;	
	});

	$(".nav-parent").hover(function(){
		if($("body").hasClass("fullscreen")){
			$(this).addClass("nav-active");
			$(this).find(".children").show();
			var other = $(".nav-parent").not($(this));
			other.removeClass("nav-active");
			other.find(".children").hide();
		}
		return false;	
	},function(){
		if($("body").hasClass("fullscreen")){
			$(this).removeClass("nav-active");
			$(this).find(".children").hide();
		}
	});

	$(".right-frame").css('min-height',$(window).height()-50);
	$(window).resize(function(){
		$(".right-frame").css('min-height',$(window).height()-50);
	});
	
});

function cOrderBy(column,colid){
	var orderby=$("input[name=orderby]");
	var orderbydir=$("input[name=orderbydir]");
	if(orderbydir.val()==""||orderbydir.val()==undefined||orderbydir.val()=='asc'){
		orderbydir.val('desc');
	}else{
		orderbydir.val('asc');
	}
	orderby.val(column);
	$("input[name=column_id]").val(colid);
	main_search();
}

function order_cls_toggle(){
	var hobj=$("input[name=orderbydir]");
	var obj=$("#"+$("input[name=column_id]").val()+"_order").find('i');
	var dir=hobj.val();
	if(hobj.val()==""||hobj.val()==undefined){
		dir='desc';
	}

	obj.removeClass('fa-chevron-down');
	obj.removeClass('fa-chevron-up');
	if(dir=='asc'){
		obj.addClass('fa-chevron-up');
	}else{
		obj.addClass('fa-chevron-down');
	}
	$("#"+$("input[name=column_id]").val()+"_order").css('color','#428bca');
}

//日期相差天数 
function  DateDiff(sDate1,  sDate2){    //sDate1和sDate2是2006-12-18格式    
	var  aDate,  oDate1,  oDate2,  iDays    
	aDate  =  sDate1.split("-")    
	oDate1  =  new  Date(aDate[1]  +  '-'  +  aDate[2]  +  '-'  +  aDate[0])    //转换为12-18-2006格式    
	aDate  =  sDate2.split("-")    
	oDate2  =  new  Date(aDate[1]  +  '-'  +  aDate[2]  +  '-'  +  aDate[0])    
	iDays  =  parseInt(Math.abs(oDate1  -  oDate2)  /  1000  /  60  /  60  /24)    //把相差的毫秒数转换为天数   
	return  iDays + 1   
}

//比较日期大小
function dateSort(date1,date2){
    var oDate1 = new Date(date1);
    var oDate2 = new Date(date2);
    if(oDate1.getTime() > oDate2.getTime()){
        return 1;
    }else if(oDate1.getTime() == oDate2.getTime()){
        return 0;
    }else{
    	return -1;
    }
}

function cDiv_toggle(name){
	var table=$("#mGridTable")
	var offset=table.find(".a_"+name).parent().offset();
	var tr_height=table.find(".a_"+name).parent().height();
	var cDiv=$("."+name);
	cDiv.css('position','fixed');
	cDiv.css('top',offset.top+tr_height+19);
	if(offset.left>=1150){
		cDiv.css('right',20);
	}else if(offset.left<=235){
		cDiv.css('left',235);
	}else{
		cDiv.css('left',offset.left);
	}
	
	var btn_yes=cDiv.find(".yes");
	var btn_no=cDiv.find(".no");
	btn_yes.on('click',function(){
		var arr =[];    
		$("input[name="+name+"]:checked").each(function(){    
				arr.push($(this).val());    
		}); 

		$("input[name="+name+"_ids]").val(arr.join());
		main_search();
	});
	btn_no.on('click',function(){
		cDiv.hide();
	});
	cDiv.toggle();
	$(".cDiv").not("."+name).each(function(){
		$(this).hide()
	})
}


/// 锁定表头和列 
function FixTable(TableID, FixColumnNumber, width, height) { 
/// 要锁定的Table的ID 
/// 要锁定列的个数 
/// 显示的宽度 
/// 显示的高度 

if ($("#" + TableID + "_tableLayout").length != 0) { 
$("#" + TableID + "_tableLayout").before($("#" + TableID)); 
$("#" + TableID + "_tableLayout").empty(); 
} 
else { 
$("#" + TableID).after("<div id='" + TableID + "_tableLayout' style='overflow:hidden;height:" + height + "px; width:" + width + "px;'></div>"); 
} 
$('<div id="' + TableID + '_tableFix"></div>' 
+ '<div id="' + TableID + '_tableHead"></div>' 
+ '<div id="' + TableID + '_tableColumn"></div>' 
+ '<div id="' + TableID + '_tableData"></div>').appendTo("#" + TableID + "_tableLayout"); 
var oldtable = $("#" + TableID); 
oldtable.addClass('fixmaxwidth');			//使表格的固定列兼容IE
var tableFixClone = oldtable.clone(true); 
tableFixClone.attr("id", TableID + "_tableFixClone"); 
$("#" + TableID + "_tableFix").append(tableFixClone); 
var tableHeadClone = oldtable.clone(true); 
tableHeadClone.attr("id", TableID + "_tableHeadClone"); 
$("#" + TableID + "_tableHead").append(tableHeadClone); 
var tableColumnClone = oldtable.clone(true); 
tableColumnClone.attr("id", TableID + "_tableColumnClone"); 
$("#" + TableID + "_tableColumn").append(tableColumnClone); 
$("#" + TableID + "_tableData").append(oldtable); 
$("#" + TableID + "_tableLayout table").each(function () { 
$(this).css("margin", "0"); 
}); 
var HeadHeight = $("#" + TableID + "_tableHead thead").height(); 
HeadHeight += 2; 
$("#" + TableID + "_tableHead").css("height", HeadHeight); 
$("#" + TableID + "_tableFix").css("height", HeadHeight); 
var ColumnsWidth = 0; 
var ColumnsNumber = 0; 
$("#" + TableID + "_tableColumn tr:last td:lt(" + FixColumnNumber + ")").each(function () { 
ColumnsWidth += $(this).outerWidth(true); 
ColumnsNumber++; 
}); 
ColumnsWidth += 2; 
if ($.browser.msie) { 
switch ($.browser.version) { 
case "7.0": 
if (ColumnsNumber >= 3) ColumnsWidth--; 
break; 
case "8.0": 
if (ColumnsNumber >= 2) ColumnsWidth--; 
break; 
} 
} 
$("#" + TableID + "_tableColumn").css("width", ColumnsWidth); 
$("#" + TableID + "_tableFix").css("width", ColumnsWidth); 
$("#" + TableID + "_tableData").scroll(function () { 
$("#" + TableID + "_tableHead").scrollLeft($("#" + TableID + "_tableData").scrollLeft()); 
$("#" + TableID + "_tableColumn").scrollTop($("#" + TableID + "_tableData").scrollTop()); 
}); 
$("#" + TableID + "_tableFix").css({ "overflow": "hidden", "position": "relative", "z-index": "50", "background-color": "Silver" }); 
$("#" + TableID + "_tableHead").css({ "overflow": "hidden", "width": width - 7, "position": "relative", "z-index": "45", "background-color": "Silver","margin-right":"10px" }); //加,"margin-right":"10px" 防IE出现列头与数据表不对齐
$("#" + TableID + "_tableColumn").css({ "overflow": "hidden", "height": height - 7, "position": "relative", "z-index": "40", "background-color": "Silver" }); 
$("#" + TableID + "_tableData").css({ "overflow": "scroll", "width": width, "height": height, "position": "relative", "z-index": "35" }); 
if ($("#" + TableID + "_tableHead").width() > $("#" + TableID + "_tableFix table").width()) { 
$("#" + TableID + "_tableHead").css("width", $("#" + TableID + "_tableFix table").width()); 
$("#" + TableID + "_tableData").css("width", $("#" + TableID + "_tableFix table").width() + 17); 
} 
if ($("#" + TableID + "_tableColumn").height() > $("#" + TableID + "_tableColumn table").height()) { 
$("#" + TableID + "_tableColumn").css("height", $("#" + TableID + "_tableColumn table").height()); 
$("#" + TableID + "_tableData").css("height", $("#" + TableID + "_tableColumn table").height() + 20);		//由原来的17改为20 兼容IE的滚动条。
} 
$("#" + TableID + "_tableFix").offset($("#" + TableID + "_tableLayout").offset()); 
$("#" + TableID + "_tableHead").offset($("#" + TableID + "_tableLayout").offset()); 
$("#" + TableID + "_tableColumn").offset($("#" + TableID + "_tableLayout").offset()); 
$("#" + TableID + "_tableData").offset($("#" + TableID + "_tableLayout").offset()); 
}

function main_recall(pk){

		layer.confirm('确定要撤回该流程？', {
		  title:'撤回确认',
		  btn: ['确定', '取消'] //可以无限个按钮
		  
		}, function(index, layero){
		  window.location.href=sUrl+'&part=recall&pk='+pk;//按钮【按钮一】的回调
		});
}

$(function(){
	$("body").on('click',function(e){
		var target = $(e.target);
	    if(!target.is(".cDiv *")) {
			$(".cDiv ").hide();
	    }
	});
});


//清除表单必填;
function clearRequired(){
	var form=$("[name=frmMain]");
	form.find("input,select,textarea").prop('required',false);
}

jQuery(function($){
	$('.required').each(function(){
        var prev=$(this).prev();
        if(prev.is('.tb-tag')){
            if($('.req-tag',prev).length==0){
                $('<div class="req-tag badge" />').text('必填').appendTo(prev);
            }
        }
    });
    $('.myrequired').each(function(){
        var prev=$(this).prev();
        if(prev.is('.tb-tag')){
            if($('.req-tag',prev).length==0){
                $('<div class="req-tag badge" />').text('必填').appendTo(prev);
            }
        }
    });
    $('.number').each(function(){
        var prev=$(this).prev();
        if(prev.is('.tb-tag')){
            if($('.req-tag',prev).length==0){
                $('<div class="req-tag badge" />').text('数字').appendTo(prev);
            }
        }
    });
});

function clearNoNum(obj,numtype,xiaoshuwei){    
	obj.value = obj.value.replace(/[^\d.]/g,"");  //清除"数字"和"."以外的字符  
	if (numtype==1){		//整数
		obj.value = obj.value.replace(/[^\d]/g,"");  //清除"数字"以外的字符
	}else{		//小数
		obj.value = obj.value.replace(/\.{2,}/g,"."); //只保留第一个. 清除多余的     
		obj.value = obj.value.replace(".","$#$").replace(/\./g,"").replace("$#$",".");    
		if (xiaoshuwei==1){		//只可输入1位小数
			obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d).*$/,'$1$2.$3');//只能输入1个小数，如果这样写(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3') 可输入2个小数
		}else{		//只可输入2位小数
			obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3');//只能输入1个小数，如果这样写(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3') 可输入2个小数
		}
	}
	if(obj.value.indexOf(".")< 0 && obj.value !=""){//以上已经过滤，此处控制的是如果没有小数点，首位不能为类似于 01、02的金额    
		obj.value= parseFloat(obj.value);    
	}    
}

function mAlertDialog(msg, func1, func2) {
    //使用了第三方layer组件，要在之前引入此库
    func2 = arguments[2] ? arguments[2] : function () { };
    layer.open({
        content: msg
        , btn: ['确定', '取消']
        , yes: function (index) {
            layer.close(index);
            func1();
        }
        , no: function (index) {
            layer.close(index);
            func2();
        }
    });
}