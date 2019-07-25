// JavaScript Document
$(function(){
	$("input[name=gw_sign_offi]").click(function(){
		var child = $(this).parents("#div_sign_office").find("input[name=gw_sign_user]");
		if($(this).get(0).checked){
			child.prop("checked", true);
		}else{
			child.prop("checked", false);
		}
	});
	
	if($("input[name=gw_can_update]").val() != '1'){
		var form=$('#custom_form');
		form.find("textarea").attr("disabled","disabled");
		form.find("button").attr("disabled","disabled");
		form.find("input").attr("disabled","disabled");
		form.find("select").attr("disabled","disabled");
		form.find("[type=checkbox]").attr("disabled","disabled");
		form.find("[type=radio]").attr("disabled","disabled");
	}
	
	$("button[name=show_log]").click(function(){
		var sUrl = 'admin?fid=' + $("input[name=fid]").val() + '&part=show_log_ajax&t=1&pk=' + $("input[name=pk]").val();
			sUrl += '&' + Math.random();
		var R1 = sendXMLHTTP(sUrl);
		
		var sUrl = 'admin?fid=' + $("input[name=fid]").val() + '&part=show_log_ajax&t=2&pk=' + $("input[name=pk]").val();
			sUrl += '&' + Math.random();
		var R2 = sendXMLHTTP(sUrl);
		
		layer.tab({
			area: ['70%', '70%'],
			tab: [{
				title: '承办日志', 
				content: R1
			}, {
				title: '协办日志', 
				content: R2
			}]
		});
		
		$(".layui-layer-content").removeClass("layui-layer-content");
		$(this).blur();
	});
	
	$("#gw_log_cb_tab").click(function(){
		$("#gw_log_cb_tab").removeClass("log-tab");
		$("#gw_log_cb_tab").addClass("log-tab-sel");
		
		$("#gw_log_xb_tab").addClass("log-tab");
		$("#gw_log_xb_tab").removeClass("log-tab-sel");
		
		$("#gw_his_log_div").show();
		$("#gw_sign_log_div").hide();
	});
	
	$("#gw_log_xb_tab").click(function(){
		$("#gw_log_xb_tab").removeClass("log-tab");
		$("#gw_log_xb_tab").addClass("log-tab-sel");
		
		$("#gw_log_cb_tab").addClass("log-tab");
		$("#gw_log_cb_tab").removeClass("log-tab-sel");
		
		$("#gw_sign_log_div").show();
		$("#gw_his_log_div").hide();
	});
//	alert($(".shanghui:checked").val());
	$(".shanghui").click(function() {
		var v = $(this).val()
		if(v == 0){ //转换不上会
			v = 2;
		}else if(v == 1){ //转换上会
			v = 1;
		}else{ //转换不关联上会
			v = 0;
		}
		$("input[name=gw_shanghui]").val(v);
		var myForm = document.forms[0];
		gw_ckOpt(myForm)
	})
})
function element_show(obj, id){ //点击checkbox 显示或隐藏元素
	if(obj.checked){
		$("#" + id).show();
	}else{
		$("#" + id).hide();
	}
}
function autolog(obj){
	var info = $(obj).html();
	$("#logtable").slideToggle("fast");
	if(info=='展开'){
		$(obj).html("收缩")
	}
	else{$(obj).html("展开")}
}
function formcheck_3(form){
	var send = $("input[name=gw_send]").val();
	var work_type = $("input[name=gw_work_type]").val();
	if(work_type == '1'){ //主办
		if(send == '1'){  //提交
			var opt = $("input[name=gw_opt]:checked");
			if(opt.length == 0){
				alert("请选择 办理状态 ！");
				return false;
			}
			if(opt.val() == 1){
				var nflow = $("input[name=gw_nflow]:checked");
				if(nflow.length == 0){
					alert("请选择 下一流程！");
					return false;
				}
				if(nflow.val() != 'E1' && nflow.val() != 'E2' && opt.val() == '1'){
					var noUser = $("input[name=gw_noUser]").val();
					var ndept = $("input[name=gw_ndept]:checked");
					if(ndept.length == 0){
						alert("请选择 流程处理科室！");
						return false;
					}
					if(noUser != 1){
						var nuser = $("input[name=gw_nuser]:checked");
						if(nuser.length == 0){
							alert("请选择 处理人！");
							return false;
						}
					}
				}
			}
		}
	}
	
	if(work_type == '1' || work_type == '2'){ //主办  协办
		var ascLen = $("textarea[name=gw_memo]").val().length;
		if(ascLen > 500){
			alert('意见 最多不能超过 500 个字符， 您共输入了 '+ascLen+' 个字符！');
			$("textarea[name=gw_memo]").focus();
			return false;
		}
	}
	
	return true;
}
function allcheck(myObj){
	d=document.getElementsByName('F7')
	for(i=0;i<d.length;i++){
		d[i].checked = myObj.checked;
		u=document.getElementsByName('F8_'+d[i].value);
		for(j=0;j<u.length;j++){
			u[j].checked=myObj.checked;
		}
	}
}
function usrcheck(myObj){
	dept_id=myObj.name.split('_')[1];
	u=document.getElementsByName('F8_'+dept_id);
	dall=true;
	for(i=0;i<u.length;i++){
		if(u[i].checked==false){
			dall=false;
			break;
		}
	}
	d=document.getElementsByName('F7');
	all=true;
	for(i=0;i<d.length;i++){
		if(d[i].value==dept_id){
			d[i].checked=dall;
		}
		if(d[i].checked == false){
			all=false;
		}
	}
	document.getElementsByName('auth_all')[0].checked=all;
}
function deptcheck(myObj){
	dept_id = myObj.value;
	u=document.getElementsByName('F8_'+dept_id)
	for (i=0;i<u.length;i++){
		u[i].checked = myObj.checked;
	}
	d=document.getElementsByName('F7');
	all=true;
	for (i=0;i<d.length;i++){
		if(d[i].checked == false){
			all=false;
			break;
		}
	}
	document.getElementsByName('auth_all')[0].checked=all;
}
function display(divID,img){
	if(document.getElementById(divID).style.display=='none'){
		//document.getElementById(img).src='up/j2.png';
		document.getElementById(divID).style.display='';
	}else{
		//document.getElementById(img).src='up/j1.png';
		document.getElementById(divID).style.display='none';
	}
}
 
function DIV_dispaly(myDIV,myIMG){
	var div1 = document.getElementById(myDIV);
	if(div1.style.display==''){
		div1.style.display='none';
		//document.getElementById(myIMG).src='up/j1.png';
	}else{
		div1.style.display='';
		//document.getElementById(myIMG).src='up/j2.png';
	}
}
function gw_ckOpt(myForm){
	
	var pk = myForm.pk.value;
	var opt = getRadioValue(myForm.gw_opt); 
	var back_return = myForm.gw_back_return.value; //退回发起人再发回来
	var shanghui = myForm.gw_shanghui.value;
	if(back_return == 1){ //退回发起人，发起人重发
		var sUrl = 'admin?fid=' + myForm.fid.value + '&part=back_return_ajax&pk=' + pk + '&flow_id=' + sDF;
			sUrl += '&' + Math.random();
		var R = sendXMLHTTP(sUrl);
		R = R.split('|&&|');
	    document.getElementById('div_flow').innerHTML = R[0];
		document.getElementById('div_dept').innerHTML = R[1];
		document.getElementById('div_user').innerHTML = R[2];
		document.getElementById('snl_user').innerHTML = R[3];
		myForm.gw_noUser.value = R[4];
		myForm.gw_sel_type.value = R[5];
	}
	else if(opt == 0){ //退回
		var sUrl = 'admin?fid=' + myForm.fid.value + '&part=back_user_ajax&pk=' + pk + '&flow_id=' + sDF + '&hid=' + hid + '&opt=' + opt;
			sUrl += '&' + Math.random();
		var R = sendXMLHTTP(sUrl);
		R = R.split('|&&|');
	    document.getElementById('div_flow').innerHTML = R[0];
		document.getElementById('div_dept').innerHTML = R[1];
		document.getElementById('div_user').innerHTML = R[2];
		document.getElementById('snl_user').innerHTML = R[3];
		myForm.gw_noUser.value = R[4];
		myForm.gw_sel_type.value = R[5];
	}
	else if(opt == 2){ //退回发起人		
		var sUrl = 'admin?fid=' + myForm.fid.value + '&part=back_start_ajax&pk=' + pk + '&flow_id=' + sDF + '&hid=' + hid + '&opt=' + opt;
			sUrl += '&' + Math.random();
		var R = sendXMLHTTP(sUrl);
		R = R.split('|&&|');
	    document.getElementById('div_flow').innerHTML = R[0];
		document.getElementById('div_dept').innerHTML = R[1];
		document.getElementById('div_user').innerHTML = R[2];
		document.getElementById('snl_user').innerHTML = R[3];
		myForm.gw_noUser.value = R[4];
		myForm.gw_sel_type.value = R[5];
	}
	else{ //正常发送
		var gw_type = myForm.gw_type.value
		var sUrl = 'admin?fid=' + myForm.fid.value + '&part=next_flow_ajax&pk=' + pk + '&opt=' + opt;
			sUrl += '&back_return=' + back_return + '&shanghui=' + shanghui + '&gw_type=' + gw_type;
			sUrl += '&' + Math.random();
		var R = sendXMLHTTP(sUrl);
		var r = R.split('|&&|');
		
		var sDF = r[0];
		var S = r[1];
		var hid = r[2];
		
	    document.getElementById('div_flow').innerHTML = S;
		gw_ckFlow(myForm);
	}
}
function gw_ckFlow(myForm){
	var pk = myForm.pk.value;
	var opt = getRadioValue(myForm.gw_opt);
	var flow_id = getRadioValue(myForm.gw_nflow);
	
	if(flow_id == 'E'){
		document.getElementById('div_dept').innerHTML = "";
		document.getElementById('snl_user').innerHTML = "";
		document.getElementById('div_user').innerHTML = "";
	}else{
		var sUrl = 'admin?fid=' + myForm.fid.value + '&part=next_dept_ajax&pk=' + pk + '&flow_id=' + flow_id;
		sUrl += '&' + Math.random();
		var R = sendXMLHTTP(sUrl);
		var r = R.split('|&&|')
		
		var sDF = r[0]
		var S = r[1]
		var sel_type = r[2]
		var noUser = r[3]
		
		myForm.gw_sel_type.value = sel_type;
		myForm.gw_noUser.value = noUser;
		
		document.getElementById('div_dept').innerHTML = S;
		if(noUser == '1'){
			document.getElementById('div_user').innerHTML = '';
			document.getElementById('snl_user').innerHTML = '';
		}else{
			document.getElementById('snl_user').innerHTML = '办理人';
		}
		gw_ckDept(myForm);
	}
}
function gw_ckDept(myForm){
	var noUser = myForm.gw_noUser.value;
	if(noUser != '1'){
		var pk = myForm.pk.value;
		var dept_id = getRadioValue(myForm.gw_ndept);
		var flow_id = getRadioValue(myForm.gw_nflow);
		var sel_type = myForm.gw_sel_type.value;
		var sUrl = 'admin?fid=' + myForm.fid.value + '&part=next_user_ajax&pk=' + pk
			sUrl += '&dept_id=' + dept_id + '&flow_id=' + flow_id + '&sel_type=' + sel_type;
			sUrl += '&' + Math.random();
		var R = sendXMLHTTP(sUrl);
		var r = R.split('|&&|');
		var sDF = r[0];
		var S = r[1];
		//document.getElementById('div_user').innerHTML = R;
		document.getElementById('div_user').innerHTML = S;
	}
}
//跨级协办
function f6check(obj){
	if(obj.checked){
		document.getElementById('div_sign').style.display='inline';
	}
	else{
		document.getElementById('div_sign').style.display='none';
	}
}
function getRadioValue(radio) {
	if(!radio){
		return ''
	}
	if (!radio.length){
		if(radio.type.toLowerCase() == 'radio') {
			return (radio.checked)?radio.value:'';
		}else{
			return ''
		}
	}
	if (radio[0].tagName.toLowerCase()!= 'input'||radio[0].type.toLowerCase() != 'radio'){ return ''; }
	var len = radio.length;
	for(i=0; i<len; i++){
		if (radio[i].checked){
			return radio[i].value;
		}
	}
	return '';
}
function change_users_sign(obj){
	 var frmMain=document.forms[0]
	if(obj.value==''){
		return
	}
	txt=""
	uname=""
	for(i=0;i<frmMain.F5;i++){
		if(frmMain.F5[i].selected){
			uname=frmMain.F5[i].text;
			break;
		}
	}
	for(i=0;i<obj.length;i++){ //循环列表
		if(uname==obj[i].text){ //如果选了主流程的人
			continue;
		}
		A=frmMain.F8.value.split(',');
		have=0; 
		for(j=0;j<A.length;j++){ //循环字符串 比较有没有这个人
			if(A[j]==obj[i].text){
				have=1; //有这个人
				break
			}
		}
		if(have==0){//如果没有这个人 则添加
			if(obj.value=='all'){ //如果选择的是全部人
				if(obj[i].value!='all' && obj[i].value!=''){
					txt+=obj[i].text+","
				}
			}
			else if(obj[i].selected){ //如果选择的是单个人
				txt+=obj[i].text+","
			}
		}
	}
	frmMain.F8.value+=txt
}
function onMemo(){
	var UL = $("#ulmemo"); 
	if(UL.css("display")=="none"){ 
	UL.css("display","block"); 
	} 
	else{ 
	UL.css("display","none"); 
	} 
}
function del_memo(pk,obj){
	
	if(pk!=""){
		sUrl="admin?fid="+ $("input[name=fid]").val() +"&part=delmemo&pk="+pk;
		R=sendXMLHTTP(sUrl);
		if(R=="1"){
			var li =$(obj).parent('li');
			li.remove();
		}else{
			layer.alert("删除失败");
		}
	}else{
		layer.alert("请输入办理意见");
	}
}
function addMemo(){
	var gw_memo = $("TEXTAREA[name=gw_memo]").val();
	if(gw_memo!=""){
		sUrl="admin?fid="+ $("input[name=fid]").val() +"&part=addmemo&gw_memo="+gw_memo;
		R=sendXMLHTTP(sUrl);
		if(R=="1"){
			layer.alert("添加成功");
			xsMemo();
		}else{
			layer.alert("添加失败");
		}
	}else{
		layer.alert("请输入办理意见");
	}
}
function xsMemo(){
	sUrl="admin?fid="+ $("input[name=fid]").val() +"&part=xsmemo";
	R=sendXMLHTTP(sUrl);
	div = $("#ulmemo"); 
	div.html(R)
	
}
function addgwmemo(obj){
	var gw_memo = $("TEXTAREA[name=gw_memo]").val();
	
	var me=$(obj).html();
	if(gw_memo==""){
		$("TEXTAREA[name=gw_memo]").val(me);
	}else{
		$("TEXTAREA[name=gw_memo]").val(gw_memo+","+me);
	}
}