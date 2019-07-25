/*创建一个tr字符串*/
function mk_tr(){
	/*下面三个是形参，为了方便处理默认值所以就不写到函数小括号中*/
	var td_str = arguments[0] ? arguments[0] : '';     /* 第一个参数，tr 的innerHtml */
	var sty_str = arguments[1] ? arguments[1] : '';    /* 第二个参数，tr 的style字符串 */
	var class_str = arguments[2] ? arguments[2] : '';  /* 第三个参数，tr 的class字符串 */
	return '<tr style="'+sty_str+'" class="'+class_str+'">'+td_str+'</tr>'
}

/*创建一个td字符串*/
function mk_td(){
	/*下面三个是形参，为了方便处理默认值所以就不写到函数小括号中*/
	var con_str = arguments[0] ? arguments[0] : '';    /* 第一个参数，td 的innerHtml */
	var sty_str = arguments[1] ? arguments[1] : '';    /* 第二个参数，td 的style字符串 */
	var class_str = arguments[2] ? arguments[2] : '';  /* 第三个参数，td 的class字符串 */
	return '<td style="'+sty_str+'" class="'+class_str+'">'+con_str+'</td>'
}

/*创建一个th字符串*/
function mk_th(){
	/*下面三个是形参，为了方便处理默认值所以就不写到函数小括号中*/
	var con_str = arguments[0] ? arguments[0] : '';    /* 第一个参数，td 的innerHtml */
	var sty_str = arguments[1] ? arguments[1] : '';    /* 第二个参数，td 的style字符串 */
	var class_str = arguments[2] ? arguments[2] : '';  /* 第三个参数，td 的class字符串 */
	return '<th style="'+sty_str+'" class="'+class_str+'">'+con_str+'</th>'
}

/*创建一个label字符串*/
function mk_label(){
	/*下面五个是形参，为了方便处理默认值所以就不写到函数小括号中*/
	var con_str = arguments[0] ? arguments[0] : '';    /* 第一个参数，label 的innerHtml */
	var sty_str = arguments[1] ? arguments[1] : '';    /* 第二个参数，label 的style字符串 */
	var class_str = arguments[2] ? arguments[2] : '';  /* 第三个参数，label 的class字符串 */
	var name_str = arguments[3] ? arguments[3] : '';  /* 第四个参数，label 的name字符串 */
	var id_str = arguments[4] ? arguments[4] : '';  /* 第五个参数，label 的id字符串 */
	return '<label style="'+sty_str+'" class="'+class_str+'" name="'+name_str+'" id="'+id_str+'">'+con_str+'</label>'
}

/*创建一个div字符串*/
function mk_div(){
	/*下面三个是形参，为了方便处理默认值所以就不写到函数小括号中*/
	var td_str = arguments[0] ? arguments[0] : '';     /* 第一个参数，tr 的innerHtml */
	var sty_str = arguments[1] ? arguments[1] : '';    /* 第二个参数，tr 的style字符串 */
	var class_str = arguments[2] ? arguments[2] : '';  /* 第三个参数，tr 的class字符串 */
	return '<div style="'+sty_str+'" class="'+class_str+'">'+td_str+'</div>'
}

/** 
 * 功能：用js 构造一个 模态窗
 * title 是表格的大标题
 * list_title 是 列表形式的表格标题
 * data_list 是二维列形式的数据
 */
function showMyModal_list(title,list_title,data_list){
	var sModal = $('<div id="showMyModal_list" name="showMyModal_list" class="modal hide fade" style="margin-left:-400px;width:800px;"></div>');
	var modal_header = $('<div class="modal-header"></div>');
	var modal_body = $('<div class="modal-body"></div>');
	var modal_footer = $('<div class="modal-footer"></div>');
	
	var modal_title = $('<h3 id="myModalLabel">'+title+'</h3>');
	var modal_title_close_btn = $('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>');
	
	var modal_footer_close_btn = $('<button class="btn" data-dismiss="modal" aria-hidden="true">关闭</button>');
	
	/*组装modal的ui*/
	modal_header.append(modal_title_close_btn);
	modal_header.append(modal_title);
	
	/*构造一个table*/
	var table=$('<table class="table table-striped"></table>');
	var tHead= $('<thead></thead>');
	var tbody= $('<tbody></tbody>');
	var i = 0;
	var j = 0;
	
	//标题行
	var thr = $(mk_tr());
	thr.append( $(mk_th('查看')) );
	for(i=0;i<list_title.length;i++){
		var thd = $(mk_th(list_title[i]));
		thr.append(thd);
	}
	tHead.append(thr);
	table.append(tHead);
	
	//数据行
	for(i=0;i<data_list.length;i++){
		var tr = $(mk_tr());
		tr.append( $(mk_td( '<a class="btn btn-mini" onclick=\'showDetails('+data_list[i][0]+');\' title="查看"><i class="icon-search"></i></a>' )) );
		for(j=0;j<data_list[i].length;j++){
			var td = $(mk_td(data_list[i][j]));
			tr.append(td);
		}
		tbody.append(tr);
	}
	table.append(tbody);
	
	/*table放入模态窗主题*/
	modal_body.append(table);
	/*模态窗底部放入按钮*/
	modal_footer.append(modal_footer_close_btn);
	
	/*组合模态窗*/
	sModal.append(modal_header);
	sModal.append(modal_body);
	sModal.append(modal_footer);
	
	sModal.modal();
	
}

/*获取随机数*/
function getRandomNum(){
		return parseInt( Math.random()*1000000000000000 );
}

/*按下按钮的处理*/
function clickListBtn(obj,sUrl){
		/*加载数据*/
		$.ajax({
				type: "GET",
				cache:false, /*IE9 缓存模式会不刷新数据*/
				async:false, /*取消异步*/
				url: sUrl,
				dataType:'json',
				success:function(data){ /*获得数据就执行处理*/
						
						if( $($(obj).find('i')[0]).attr("class") == "icon-minus" ){ /*如果是减号，那就删掉之前插入的行*/
								delRow(obj);
						}else{
								showRow(obj,data);
						}
				},
				error:function(XMLHttpRequest,errorMsg){
						alert('异步请求异常请联系管理员');
				}
		});
}

/*插入行的处理*/
function showRow(obj,dataList){
		
		var this_tr = getParentObj(obj,'tr');        /*该按钮所在的tr对象*/
		var this_table = getParentObj(obj,'table');  /*该按钮所在的table对象*/
		var cols = this_tr.find('td').length;        /*table的列数*/
		var dataCols = dataList[0].length;	         /*数据列数*/
		var needCols = cols-dataCols+1;              /*需要合并的列数*/
		var ranCode = getRandomNum();                /*随机码*/
		
		var trs = []; /*空的列表用来放数据拼接后的tr的*/
		
		var i = 0,j=0;
		for( i=0;i<dataList.length;i++ ){
				var tr = $('<tr></tr>').attr("random",ranCode);
				for(j=0;j<dataList[0].length;j++){
						/*第一列是 th ，然后最后一列需要合并掉多余的列*/
						var td = ( j==0 ? $('<th></th>') : ( j== dataList[0].length-1? $('<td></td>').attr("colspan",needCols):$('<td></td>') ) );
						tr.append( td.html( dataList[i][j] ) );
				}
				trs.push(tr);
		}
		/*东西放进trs后，就开始加入到table吧*/
		for(i=dataList.length-1;i>=0;i--){
				trs[i].insertAfter( this_tr ); /*插入行*/
				
		}
		/*执行完毕就在button上放ranCode作为标记*/
		$(obj).attr("random",ranCode);
		$($(obj).find('i')[0]).attr("class","icon-minus"); /*处理完了，就换成减号的class*/
}

/*删除行的处理*/
function delRow(obj){
		var this_tr = getParentObj(obj,'tr');        /*该按钮所在的tr对象*/
		var this_table = getParentObj(obj,'table');  /*该按钮所在的table对象*/
		var ranCode = $(obj).attr("random");
		var trs = this_table.find("tr[random="+ranCode+"]");
		var i = 0;
		for(i=0;i<trs.length;i++){
				$(trs[i]).remove();
		}
		$($(obj).find('i')[0]).attr("class","icon-plus"); /*处理完了，就换成加号的class*/
		$(obj).removeAttr("random"); /*移除random属性*/
}

/*通过obj对象获取指定的父jq对象，如果10个之内获取不到，那就暂停了*/
function getParentObj(obj,pTagName){
		var i = 0;
		var parent = null;
		var p = $(obj);
		for(i=0;i<10;i++){
			  p = p.parent();
				if( p[0].tagName==pTagName.toLocaleUpperCase() ){
						parent = p;
						break;
				}
		}
		return parent;
}

/*这个是扩展接口，用来扩展隐藏模态窗后的处理*/
function doAfterHid_modal_alert(){
	
}

/**
 * 功能：用来显示消息而已
 * 参数: 参数1 是 消息的内容
 *       参数2 是 回调函数，用于执行隐藏后的处理，默认是 神马也不做
 */
function modal_alert(){
	
	var content = arguments[0] ? arguments[0] : '这是一个消息';     /* 第一个参数，tr 的innerHtml */
	var title = '温馨提示';    /* 第二个参数，tr 的style字符串 */
	var callback_hid = arguments[1] ? arguments[1] : doAfterHid_modal_alert;
	
	var sModal = $('<div id="globalAlert" class="modal fade"></div>');
	var dialog = $('<div class="modal-dialog"></div>');
	var mcontent = $('<div class="modal-content"></div>')
	var modal_header = $('<div class="modal-header"></div>');
	var modal_body = $('<div class="modal-body"></div>');
	var modal_footer = $('<div class="modal-footer"></div>');
	
	var modal_title = $('<h3>'+title+'</h3>');
	var modal_title_close_btn = $('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>');
	var modal_footer_close_btn = $('<button class="btn btn-default" data-dismiss="modal" aria-hidden="true">关闭</button>');
	
	/*组装modal的ui*/
	modal_header.append(modal_title_close_btn);
	modal_header.append(modal_title);
	
	/*content放入模态窗主题*/
	modal_body.append(content);
	
	/*模态窗底部放入按钮*/
	modal_footer.append(modal_footer_close_btn);
	
	/*组合模态窗*/
	mcontent.append(modal_header);
	mcontent.append(modal_body);
	mcontent.append(modal_footer);
	dialog.append(mcontent);
	sModal.append(dialog);
	$(document.body).append(sModal); /*加入到html文档中，不是特定的容器内*/
	
	$("div[id='globalAlert']").on('hidden', function () {
		/*将刚才弹窗从html上清理掉，避免残留*/
		$("#globalAlert").remove();
		
		callback_hid(); /*执行扩展*/
	});
	
	$("#globalAlert").modal('show');
	
}

/*确认的操作*/
function doAfterYes_modal_alert(){
	
}

/*取消的操作*/
function doAfterNo_modal_alert(){
	
}

/**
 * 功能：用来 模拟confirm 操作的效果
 * 参数: 参数1 是 消息的内容
 *       参数2 是 回调函数，用于按下确认之后的处理
 *       参数3 是 回调函数，用于按下取消之后的处理，默认是 神马也不做
 *       参数4 是 回调函数，用于执行隐藏后的处理，默认是 神马也不做
 */
function modal_confirm(){
	
	var content = arguments[0] ? arguments[0] : '这是一个确认消息';     /* 第一个参数，tr 的innerHtml */
	var title = '温馨提示';    /* 第二个参数，tr 的style字符串 */
	
	var callback_Yes = arguments[1] ? arguments[1] : doAfterYes_modal_alert;
	var callback_No = arguments[2] ? arguments[2] : doAfterNo_modal_alert;
	
	var callback_hid = arguments[3] ? arguments[3] : doAfterHid_modal_alert;
	
	var sModal = $('<div id="globalAlert" class="modal fade"></div>');
	var modal_header = $('<div class="modal-header"></div>');
	var modal_body = $('<div class="modal-body"></div>');
	var modal_footer = $('<div class="modal-footer"></div>');
	
	var modal_title = $('<h3>'+title+'</h3>');
	var modal_title_close_btn = $('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>');
	var modal_footer_Yes_btn = $('<button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">确认</button>');
	var modal_footer_No_btn = $('<button class="btn" data-dismiss="modal" aria-hidden="true">取消</button>');
	
	/*给确认和取消按钮添加事件处理*/
	modal_footer_Yes_btn.bind('click',callback_Yes);
	modal_footer_No_btn.bind('click',callback_No);
	
	/*组装modal的ui*/
	modal_header.append(modal_title_close_btn);
	modal_header.append(modal_title);
	
	/*content放入模态窗主题*/
	modal_body.append(content);
	
	/*模态窗底部放入按钮*/
	modal_footer.append(modal_footer_Yes_btn);
	modal_footer.append(modal_footer_No_btn);
	
	/*组合模态窗*/
	var dialog = $('<div class="modal-dialog"></div>');
	var mcontent = $('<div class="modal-content"></div>')
	mcontent.append(modal_header);
	mcontent.append(modal_body);
	mcontent.append(modal_footer);
	dialog.append(mcontent);
	sModal.append(dialog);
	
	$(document.body).append(sModal); /*加入到html文档中，不是特定的容器内*/
	
	$("div[id='globalAlert']").on('hidden', function () {
		/*将刚才弹窗从html上清理掉，避免残留*/
		$("#globalAlert").remove();
		
		callback_hid(); /*执行扩展*/
	});
	
	$("#globalAlert").modal({
		backdrop:'static',
		keyboard:false,
		show:true
	});
	
}