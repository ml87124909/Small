/******************************************************
# Author : Jophy.Lee
# Date : 2017.02.09
*******************************************************/
jQuery(function(){
	jQuery(".modal-select").each(function(){
		var txt = jQuery(this).find("select option:selected").text();
		var parent = jQuery(this);
		parent.find("span").html(txt);
		parent.find("select").change(function(){
			var v = jQuery(this).find("option:selected").text();
			parent.find("span").html(v);
		});
	});
});