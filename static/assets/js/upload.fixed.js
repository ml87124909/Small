/******************************************************
# Author : Jophy.Lee
# Date : 2017.01.26
*******************************************************/
function initCanvas(img , Orientation){
	var degree=0,drawWidth,drawHeight,width,height;
	drawWidth=img.naturalWidth;
	drawHeight=img.naturalHeight;
	//以下改变一下图片大小
	var maxSide = Math.max(drawWidth, drawHeight);
	if (maxSide > 1024) {
		var minSide = Math.min(drawWidth, drawHeight);
		minSide = minSide / maxSide * 1024;
		maxSide = 1024;
		if (drawWidth > drawHeight) {
		  drawWidth = maxSide;
		  drawHeight = minSide;
		} else {
		  drawWidth = minSide;
		  drawHeight = maxSide;
		}
	}
	//alert(expectWidth+','+expectHeight);  
	var canvas = document.createElement("canvas"); 
	canvas.width=width=drawWidth;
	canvas.height=height=drawHeight;
	var ctx = canvas.getContext("2d");
	//判断图片方向，重置canvas大小，确定旋转角度，iphone默认的是home键在右方的横屏拍摄方式
	switch(Orientation){
	//iphone横屏拍摄，此时home键在左侧
		case 3:
		  degree=180;
		  drawWidth=-width;
		  drawHeight=-height;
		  break;
		//iphone竖屏拍摄，此时home键在下方(正常拿手机的方向)
		case 6:
		  canvas.width=height;
		  canvas.height=width; 
		  degree=90;
		  drawWidth=width;
		  drawHeight=-height;
		  break;
		//iphone竖屏拍摄，此时home键在上方
		case 8:
		  canvas.width=height;
		  canvas.height=width; 
		  degree=270;
		  drawWidth=-width;
		  drawHeight=height;
		  break;
	}
	// canvas.width = expectWidth;  
	//canvas.height = expectHeight;  
	ctx.rotate(degree*Math.PI/180);
	//ctx.drawImage(this, 0, 0, expectWidth, expectHeight); 
	ctx.drawImage(img,0,0,drawWidth,drawHeight);
	return canvas;
}
function singleUpload(fileObj,cls,callback){
	var file = fileObj.files[0]; 
    //图片方向角 added by lzk  
    var Orientation = null;  
    if (file) {  
        //console.log("正在上传,请稍后...");  
        var rFilter = /^(image\/jpeg|image\/png)$/i; // 检查图片格式  
        if (!rFilter.test(file.type)) {  
            //showMyTips("请选择jpeg、png格式的图片", false);  
            return;  
        }  
        // var URL = URL || webkitURL;  
        //获取照片方向角属性，用户旋转控制  
        EXIF.getData(file, function() {  
           // alert(EXIF.pretty(this));  
            EXIF.getAllTags(this);   
            //alert(EXIF.getTag(this, 'Orientation'));   
            Orientation = EXIF.getTag(this, 'Orientation');  
            //return;  
        });  
          
        var oReader = new FileReader();  
        oReader.onload = function(e) {  
            //var blob = URL.createObjectURL(file);  
            //_compress(blob, file, basePath);  
            var image = new Image();  
            image.src = e.target.result;  
            image.onload = function() {  
                var canvas = initCanvas(this , Orientation); 
				
				var base64 = canvas.toDataURL("image/jpeg", 0.8);  
				$(cls+" .upload-value").val(base64.substr(22));
                if(typeof callback == 'function'){
					callback(base64);
				}
            };  
        };  
        oReader.readAsDataURL(file); 
	}
}

function multiUpload(fileObj,callback){
	var files = fileObj.files;
	for (var i = 0;i <  files.length;i++ )
	{
		var file = files[i];
		var rFilter = /^(image\/jpeg|image\/png)$/i; // 检查图片格式  
        if (!rFilter.test(file.type)) {   
            return;  
        }  
		EXIF.getData(file, function() {  
            EXIF.getAllTags(this);     
            Orientation = EXIF.getTag(this, 'Orientation');  
        });  
		var oReader = new FileReader();  
        oReader.onload = function(e) {   
            var image = new Image();  
            image.src = e.target.result;  
            image.onload = function() {  
                var canvas = initCanvas(this , Orientation); 
				
				var base64 = canvas.toDataURL("image/jpeg", 0.8);  
                if(typeof callback == 'function'){
					callback(base64);
				}
            };  
        };  
        oReader.readAsDataURL(file); 
	}
}
