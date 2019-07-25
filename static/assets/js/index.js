$(function(){
	if ($(".back-bar").length > 0)
	{
		$(window).scroll(function(){
			if($(window).scrollTop() > 0){
				$(".back-bar").addClass("lock");
				$(".top-blank").show();
			}else{
				$(".back-bar").removeClass("lock");
				$(".top-blank").hide();
			}
		});
	}	

	$(".not-open").click(function(){
		ialert("该功能未开放");
		return false;
	});
});

function ialert(msg){
	layer.open({
		content: msg
		,skin: 'msg'
		,time: 2 //2秒后自动关闭
	  });
}
function showloading(){
	layer.open({type: 2 , shadeClose:false});
}
function hideloading(){
	layer.closeAll();
}