/**
 * Created by Dasate on 2017/9/14.
 * QQ361899429
 */
/*抢*/
var simpleAlert1 = function (opts) {
    //设置默认参数
    var opt = {
        "closeAll": false,
        "content": "",
        "buttons": {}
    }
    //合并参数
    var option = $.extend(opt, opts);
    //事件
    var dialog = {}
    var $simpleAlert = $('<div class="simpleAlert1">');
    var $shelter = $('<div class="simpleAlertShelter1">');
    var $simpleAlertBody = $('<div class="simpleAlertBody1" style="background-image: url(asset/images/3.png);">');
    var $simpleAlertBodyClose = $('<img class="simpleAlertBodyClose1" src="" />');
    var $simpleAlertBodyContent = $('<p class="simpleAlertBodyContent1">' + option.content + '</p>');
    dialog.init = function () {
        $simpleAlertBody.append($simpleAlertBodyClose).append($simpleAlertBodyContent);
        var num = 0;
        var only = false;
        var onlyArr = [];
        for (var i = 0; i < 2; i++) {
            for (var key in option.buttons) {
                switch (i) {
                    case 0:
                        onlyArr.push(key);
                        break;
                    case 1:
                        if (onlyArr.length <= 1) {
                            only = true;
                        } else {
                            only = false;
                        }
                        num++;
                        var $btn = $('<button class="simpleAlertBtn11 simpleAlertBtn11' + num + '">' + key + '</button>')
                        $btn.bind("click", option.buttons[key]);
                        if (only) {
                            $btn.addClass("onlyOne1")
                        }
                        $simpleAlertBody.append($btn);
                        break;
                }

            }
        }
        $simpleAlert.append($shelter).append($simpleAlertBody);
        $("body").append($simpleAlert);
        $simpleAlertBody.show().animate({"marginTop":"-128px","opacity":"1"},300);
    }
    //右上角关闭按键事件
    $simpleAlertBodyClose.bind("click", function () {
        option.closeAll=false;
        dialog.close();
		$('.pingspan').css("background-image" , "url(asset/images/ping.png)");
    })
    dialog.close = function () {
        if(option.closeAll){
            $(".simpleAlert1").remove()
        }else {
            $simpleAlertBody.animate({"marginTop": "-188px", "opacity": "0"}, 200, function () {
                $(".simpleAlert1").last().remove()
            });
        }
    }
    dialog.init();
    return dialog;
}



/*我的排名*/
var simpleAlert = function (opts) {
    //设置默认参数
    var opt = {
        "closeAll": false,
        "content": "",
        "buttons": {}
    }
    //合并参数
    var option = $.extend(opt, opts);
    //事件
    var dialog = {}
    var $simpleAlert = $('<div class="simpleAlert">');
    var $shelter = $('<div class="simpleAlertShelter">');
    var $simpleAlertBody = $('<div class="simpleAlertBody" style="background-image: url(asset/images/6.png);">');
    var $simpleAlertBodyClose = $('<img class="simpleAlertBodyClose" src=""/>');
	var $simpleAlertBodyButton = $('<button class="simpleAlertBtna" ></button>');
	var $simpleAlertBodyButtona= $('<button class="simpleAlertBtnb" ></button>');
    var $simpleAlertBodyContent = $('<p class="simpleAlertBodyContent">' + option.content + '</p>');
    dialog.init = function () {
        $simpleAlertBody.append($simpleAlertBodyClose).append($simpleAlertBodyButton).append($simpleAlertBodyButtona).append($simpleAlertBodyContent);
        var num = 0;
        var only = false;
        var onlyArr = [];
        for (var i = 0; i < 2; i++) {
            for (var key in option.buttons) {
                switch (i) {
                    case 0:
                        onlyArr.push(key);
                        break;
                    case 1:
                        if (onlyArr.length <= 1) {
                            only = true;
                        } else {
                            only = false;
                        }
                        num++;
                        var $btn = $('<button class="simpleAlertBtn simpleAlertBtn' + num + '">' + key + '</button>')
                        $btn.bind("click", option.buttons[key]);
                        if (only) {
                            $btn.addClass("onlyOne")
                        }
                        $simpleAlertBody.append($btn);
                        break;
                }

            }
        }
        $simpleAlert.append($shelter).append($simpleAlertBody);
        $("body").append($simpleAlert);
        $simpleAlertBody.show().animate({"marginTop":"-128px","opacity":"1"},300);
    }

	//点击活动规则事件
	$simpleAlertBodyButton.bind("click", function () {
        $(".woupis").css("display" , "none");
		$(".guiis").css("display" , "block");
		$('.pingspan').css("background-image" , "url(asset/images/ping.png)");
    })
    
	//点击我的排名事件
	$simpleAlertBodyButtona.bind("click", function () {
        $(".woupis").css("display" , "block");
		$(".guiis").css("display" , "none");
		$('.pingspan').css("background-image" , "url(asset/images/qiang.png)");
    })


    //右上角关闭按键事件
    $simpleAlertBodyClose.bind("click", function () {
        option.closeAll=false;
        dialog.close();
		$('.pingspan').css("background-image" , "url(asset/images/ping.png)");
    })
    dialog.close = function () {
        if(option.closeAll){
            $(".simpleAlert").remove()
        }else {
            $simpleAlertBody.animate({"marginTop": "-188px", "opacity": "0"}, 200, function () {
                $(".simpleAlert").last().remove()
            });
        }
    }
    dialog.init();
    return dialog;
}



