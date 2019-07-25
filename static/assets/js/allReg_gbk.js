/*******************************************************************
*
* Copyright (c) 2014 tso forever, Michael Pang ,All Rights Reserved.
*         Author : ボルケーノ
*      File name : D:/Zope-Instance/Extensions/knife/admin/ui/H006.py
*    Start  Date : 2014-11-27 15:40:30
*    Last modify : unknown
*    description : 这是一个js 正则表达式校验大全，
*      encodeing : GBK
*********************************************************************/

/**
 * 函数名：isMobile 
 * 函数作用：校验中国手机号码 (形如 13045678975)
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isMobile(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var result = false;
	
	if (str == '' ){
	}else if( typeof(str) == 'string' ){ 
		var reg = /^[1-9]\d{10}$/; //第一个数字不能是0，后面跟着10个任意数字
		if(reg.test(str)){
			result = true;
		}
	}
	
	return result;
}

/**
 * 函数名：isFixedTel 
 * 函数作用：校验中国固话 //(形如 0662-1234567,010-12345678 或者 (0662)1234567 或者不写区号 1234567 )
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isFixedTel(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' ){ 
		var reg = /^((\(\d{3,4}\))|(\d{3,4}-))?\d{7,8}$/; 
		if(reg.test(str)){
			result = true;
		}
	}
	
	return result;
}

/**
 * 函数名：isPostCode 
 * 函数作用：验证中国邮政编码 //(形如 529500 )
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isPostCode(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' ){ 
		var reg = /^[1-9]\d{5}$/; 
		if(reg.test(str)){
			result = true;
		}
	}
	
	return result;
}

/**
 * 函数名：isEmail 
 * 函数作用：验证电子邮件地址 //(形如 zhangsan@163.com; mick234.cn@234.com.net.cn  )
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isEmail(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' ){ 
		var reg = /^\w+([-\+\.]\w+)*@\w+([-.]\w+)*\.\w+([-\.]\w+)*$/; 
		if(reg.test(str)){
			result = true;
		}
	}
	
	return result;
}

/**
 * 函数名：isIDCode 
 * 函数作用：验证中国身份证号 //(形如 包括15位或者18号 )
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isIDCode(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' ){ 
		var reg = /^[1-9]\d{14}(\d{2}[0-9A-Za-z])?$/;  //身份证老式的，可能为15位，新的位18位，然后18位身证号，可能最后一位是写字母的
		if(reg.test(str)){
			result = true;
		}
	}
	
	return result;
}

/**
 * 函数名：isInt
 * 函数作用：验证整数字符串 //(形如 不限长度的整数字符串 12345646786768754 ， isInt('4563')
 *                          也可用于判断固定长度的整数 isInt('132456','fixed',6)
 *                          或者在长度在某个范围内的整数 isInt('123','auto','3')  )
 * 参数：str ，必填，字符类串型，是校验的对象，如果不填，那就直接是false
 *     type, 选填，字符串类型，是校验类型，fixed 为固定长度，auto 为不限长度，默认不限长度
 *     len , 选填，字符串类型，是校验的长度。
 *                当 type 为 fixed 时，校验的是 长度为len的字符串，
 *                当 type 为 auto时，校验的是 长度小于等于len的字符串
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isInt(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	var type = arguments[1] ? arguments[1] : 'no';  // 这是要校验类型，type 默认是 no
	var len = arguments[2] ? arguments[2] : 0;  // 这是要校验长度, len要大于0才生效 
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' && typeof(type)=='string' && typeof(len)=='number' ){  //校验下参数类型有效性
		
		var reg = /^(0|([1-9]\d*))$/; //默认是不限长度的  (整数不能以0开头。所以0要单独一个，或者非零开头的多数位整数)
		if( type=='fixed' && len > 0){ // fixed 处理的是 固定 len 长度的校验
			if(len==1){
				reg = /^[0-9]$/;
			}else{
				eval('reg=/^[1-9]\\d{'+(len-1)+'}$/');
			}
		}else if( type=='auto' && len > 0 ){ //auto 处理的是 len 范围内的长度
			if(len==1){
				reg = /^[0-9]$/;
			}else{
				eval('reg = /^((\\d)|([1-9]\\d{1,'+(len-1)+'}))$/;'); /* 因为长度为1的已经处理，所以这里做2以上的 */
			}
		}
		
		if(reg.test(str)){
			result = true;
		}
		
		/*因为长度参数为0，代表str应该为空，但是这里是不允许为空的，所以直接false，不管str是什么*/
		/*为了区别于默认的 type=='no' && len==0 的情况，所以要加个type判断  */
		if( len == 0 && (type=='auto' || type=='fixed') ){ 
			result =false;
		}
		
	}
	
	return result;
}

/**
 * 函数名：isDecimal
 * 函数作用：验证小数字符串 //(形如 不限长度的整数字符串 1234564.6786768754 ， isInt('456.2543')
 *                          也可用于判断固定长度的小数 isDecimal('123.132456','fixed',6)
 *                          或者在长度在某个范围内的小数isDecimal('45.123','auto','3')  
 *                          区别于整数，这里的小数必须包含 小数点 和 整数，小数位可以为空： '123.' ，'0.'，'123.45'  这些都是可以的。 
 * 参数：str ，必填，字符类串型，是校验的对象，如果不填，那就直接是false
 *     type, 选填，字符串类型，是校验类型，fixed 为固定长度，auto 为不限长度，默认不限长度
 *     len , 选填，字符串类型，是校验的长度。
 *                当 type 为 fixed 时，校验的是 小数长度为len的字符串，
 *                当 type 为 auto时，校验的是 小数长度小于等于len的字符串
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isDecimal(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	var type = arguments[1] ? arguments[1] : 'no';  // 这是要校验类型，type 默认是 no
	var len = arguments[2] ? arguments[2] : 0;  // 这是要校验长度, len要大于0才生效 
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' && typeof(type)=='string' && typeof(len)=='number' ){  //校验下参数类型有效性
		
		var reg = /^(0|([1-9]\d*))\.\d*$/ //默认是不限小数长度的，因为数据库可以接受 123. 的形式，所以 整数加上点也是可以成立的 
		if( type=='fixed' && len > 0){ // fixed 处理的是 固定 len 长度的校验
			if(len==1){
				reg = /^((0)|([1-9]\d*))\.\d$/; /*一位小数只能是这样了*/
			}else{
				eval('reg=/^((0)|([1-9]\\d*))\\.\\d{'+len+'}$/'); //固定小数位是 len 的长度
			}
		}else if( type=='auto' && len > 0 ){ //auto 处理的是 len 范围内的长度
			if(len==1){
				reg = /^((0)|([1-9]\d*))\.\d?$/; /* 一位小数，或者小数位为空只有小数点*/
			}else{
				eval('reg = /^((0)|([1-9]\\d*))\\.\\d{0,'+len+'}?$/;'); /* 浮动1至n位小数 */
			}
		}
		
		if(reg.test(str)){
			result = true;
		}else{
			result = isInt(str); /*让整数也能通过小数的判断*/
		}
	}
	
	return result;
}

/**
 * 函数名：isMoney 
 * 函数作用：验证中国的金额字符串 //(形如 包括纯数字的和 带逗号的表示，金额的小数位最多允许有两位，即到 分位 )
 *          这里都是允许整数带点的形式表示小数的。形如 123. 这是合法的表示方式
 *          默认是只判断纯数字形式的金额的。如果要兼容逗号表示法，那么就要将type 设置为 'dot'
 * 参数：str ，必填，字符类型，是校验的对象
 *     type，选填，字符串类型，是校验的类型，
 *                默认情况下为空，这样就只校验是否是数字（整数或者小数），
 *                如果填写 'dot' 表示可以兼容带逗号的表示法
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isMoney(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	var type = arguments[1] ? arguments[1] : '';  // 这是要校验类型，type 默认是''
	
	var result = false;
	//这个是可以判断是否 逗号表示法的金额字符串的正则。（型如：1,456,123,000.02 ）
	//规则是 ： 整数部分是 0 或者 非0的整数以逗号隔开，小数部分可以没有，或者 只有一个点。如果有小数只能，有两位小数。
	//        因为，正常交易，现在都是到 分位 的了。
	var dot_reg = /^(((0)|([1-9](\d{1,2})?(,\d{3})*))(\.\d{0,2})?)$/; 
	//这个是判断 纯数字形式金额的正则
	var reg = /^((0)|([1-9]\d*))((\.)|(\.\d{1,2}))?$/
	
	if (str == ''){
	}else if( typeof(str) == 'string' && typeof(type) == 'string'){ 
		if(type=='dot'){ //如果是要兼容逗号表示法的话
			if(reg.test(str)){ //先判断是不是纯数字的形式，如果不是再判断是否带逗号的表示法，如果都不是就不管了
				result = true;
			}else{
				if(dot_reg.test(str)){
					result = true;
				}
			}
		}else{
			if(reg.test(str)){
				result = true;
			}
		}
		
	}
	
	return result;
}

/**
 * 函数名 ：   isSignedMoney
 * 函数作用：  在 isMoney 的基础上增加对符号判断，允许有负号
 * 参数：str ，必填，字符类型，是校验的对象
 *     type，选填，字符串类型，是校验的类型，
 *                默认情况下为空，这样就只校验是否是数字（整数或者小数），
 *                如果填写 'dot' 表示可以兼容带逗号的表示法
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isSignedMoney(){
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	var type = arguments[1] ? arguments[1] : '';  // 这是要校验类型，type 默认是''
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' && typeof(type)=='string' ){
		
		var l = str.length; //长度
		var head = str.substr(0,1); //首字符
		var part = str.substring(1,l); // 除了首字符外，剩下的部分
		
		if( head == '-' ){ //如果是有符号的, 用剩下的部分去判断
			result = isMoney(part,type); 
		}else{ //如果是没符号的
			result = isMoney(str,type);
		}
	}
	
	return result;
	
}

/**
 * 函数名 ：   isSignedInt 
 * 函数作用：验证整数字符串 (在 isInt 的基础上增加符号判断，方便判断带负号的整数)
 *                       (形如 不限长度的整数字符串 12345646786768754 ， isInt('4563')
 *                          也可用于判断固定长度的整数 isInt('132456','fixed',6)
 *                          或者在长度在某个范围内的整数 isInt('123','auto','3')  )
 * 参数：str ，必填，字符类串型，是校验的对象，如果不填，那就直接是false
 *     type, 选填，字符串类型，是校验类型，fixed 为固定长度，auto 为不限长度，默认不限长度
 *     len , 选填，字符串类型，是校验的长度。
 *                当 type 为 fixed 时，校验的是 长度为len的字符串，
 *                当 type 为 auto时，校验的是 长度小于等于len的字符串
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isSignedInt(){
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	var type = arguments[1] ? arguments[1] : 'no';  // 这是要校验类型，type 默认是auto
	var len = arguments[2] ? arguments[2] : 0;  // 这是要校验长度, len要大于0才生效
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' && typeof(type)=='string' && typeof(len)=='number' ){  //校验下参数类型有效性
		
		var l = str.length; //长度
		var head = str.substr(0,1); //首字符
		var part = str.substring(1,l); // 除了首字符外，剩下的部分
		
		if( head == '-' ){ //如果是有符号的, 用剩下的部分去判断
			result = isInt(part,type,len); 
		}else{ //如果是没符号的
			result = isInt(str,type,len); 
		}
	}
	
	return result;
	
}


/**
 * 函数名 ：   isSignedDecimal 
 * 函数作用：验证小数字符串 在isDecimal的基础上增加负号判断 
 *                          (形如 不限长度的整数字符串 1234564.6786768754 ， isInt('456.2543')
 *                          也可用于判断固定长度的整数 isDecimal('123.132456','fixed',6)
 *                          或者在长度在某个范围内的整数isDecimal('45.123','auto','3')  
 *                          区别于整数，这里的小数必须包含 小数点 和 整数，小数位可以为空： '123.' ，'0.'，'123.45'  这些都是可以的。 
 * 参数：str ，必填，字符类串型，是校验的对象，如果不填，那就直接是false
 *     type, 选填，字符串类型，是校验类型，fixed 为固定长度，auto 为不限长度，默认不限长度
 *     len , 选填，字符串类型，是校验的长度。
 *                当 type 为 fixed 时，校验的是 小数长度为len的字符串，
 *                当 type 为 auto时，校验的是 小数长度小于等于len的字符串
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是
 */
function isSignedDecimal(){
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	var type = arguments[1] ? arguments[1] : 'no';  // 这是要校验类型，type 默认是auto
	var len = arguments[2] ? arguments[2] : 0;  // 这是要校验长度, len要大于0才生效
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' && typeof(type)=='string' && typeof(len)=='number' ){  //校验下参数类型有效性
		
		var l = str.length; //长度
		var head = str.substr(0,1); //首字符
		var part = str.substring(1,l); // 除了首字符外，剩下的部分
		
		if( head == '-' ){ //如果是有符号的, 用剩下的部分去判断
			result = isDecimal(part,type,len); 
		}else{ //如果是没符号的
			result = isDecimal(str,type,len); 
		}
	}
	
	return result;
	
}


/**
 * 函数名：isQQCode 
 * 函数作用：验证中国QQ号码
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function isQQCode(){
	
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' ){ 
		var reg = /^[1-9]\d{4,}$/ /*一开始的QQ是五位数的，然后一直发展到现在*/
		if(reg.test(str)){
			result = true;
		}
	}
	
	return result;
}


/**
 * 函数名： hasCHNwords
 * 函数作用：  用于判断字符串中是否包含中文字符(需要特别注意的是，这里只能判断是否含有中文文字，对于中文标点是判断不出来的)
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function hasCHNwords(){
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' ){ 
		var reg = /[\u4e00-\u9fa5]/  // 只要字符串中能匹配出一个就认为是有中文字符的。
		if(reg.test(str)){
			result = true;
		}
	}
	
	return result;
}


/**
 * 函数名： hasDByte
 * 函数作用：  用于判断字符串中是否包含双字节字符，能有效判断全角字符，或者中文，以及特殊字符。只要是双字节的都能判断出来
 *           这个函数在判断 字符的真实长度以及 判断是否含有全角字符 以及 中文判断都可以使用
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：Boolean 类型 true 或者 false
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function hasDByte(){
	/*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var result = false;
	
	if (str == ''){
	}else if( typeof(str) == 'string' ){ 
		var reg = /[^\x00-\xff]/  // 只要字符串中能匹配出一个就认为是有双字节字符的。
		if(reg.test(str)){
			result = true;
		}
	}
	
	return result;
}

/**
 * 函数名： lenB
 * 函数作用：  用于计算字符串的真实长度以字节为单位。（
 *             js的length属性返回的是虚拟长度，中文也会被认为是长度为 1，所以这里要自己做个函数求）
 * 参数：str ，必填，字符类型，是校验的对象
 * 返回值：number 类型 ，返回的是字符串的字节长度
 * 说明：函数只处理字符类型或者字符串的校验，如果传入参数非字符类型或者字符串类型，那么直接返回false结果
 *      如果不写参数直接调用，默认str参数是 空字符，那么返回的结果 显然是 false 
 */
function lenB(){
    
    /*这是js的多态写法。方便多参数处理，要是以后要加参数也方便*/  
	var str = arguments[0] ? arguments[0] : '';  // 这是要校验的内容
	
	var reg = /[^\x00-\xff]/g;
	var result = 0;
	
	if (str == ''){
	}else if( typeof(str) == 'string' ){ 
	    result = str.length;
    	var k = str.match(reg);
    	if( k != null){ //如果有双字节字符
    	    result += k.length
    	}
    }
	return result;
}

/***************************************************************************************************************************

非法字符验证 
匹配非法字符如:< > & / ' | 
正则表达式 [^<>&/|'\]+

日期验证 
匹配形式如:20030718,030718 
范围:1900--2099 
正则表达式((((19){1}|(20){1})d{2})|d{2})[01]{1}d{1}[0-3]{1}d{1}


匹配中文字符的正则表达式： [\u4e00-\u9fa5]
评注：匹配中文还真是个头疼的事，有了这个表达式就好办了

匹配双字节字符(包括汉字在内)：[^\x00-\xff]
评注：可以用来计算字符串的长度（一个双字节字符长度计2，ASCII字符计1）

匹配空白行的正则表达式：\n\s*\r
评注：可以用来删除空白行

匹配HTML标记的正则表达式：< (\S*?)[^>]*>.*?|< .*? />
评注：网上流传的版本太糟糕，上面这个也仅仅能匹配部分，对于复杂的嵌套标记依旧无能为力

匹配首尾空白字符的正则表达式：^\s*|\s*$
评注：可以用来删除行首行尾的空白字符(包括空格、制表符、换页符等等)，非常有用的表达式

匹配Email地址的正则表达式：\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*
评注：表单验证时很实用

匹配网址URL的正则表达式：[a-zA-z]+://[^\s]*
评注：网上流传的版本功能很有限，上面这个基本可以满足需求

匹配帐号是否合法(字母开头，允许5-16字节，允许字母数字下划线)：^[a-zA-Z][a-zA-Z0-9_]{4,15}$
评注：表单验证时很实用

匹配国内电话号码：\d{3}-\d{8}|\d{4}-\d{7}
评注：匹配形式如 0511-4405222 或 021-87888822


匹配中国邮政编码：[1-9]\d{5}(?!\d)
评注：中国邮政编码为6位数字

匹配身份证：\d{15}|\d{18}
评注：中国的身份证为15位或18位

匹配ip地址：\d+\.\d+\.\d+\.\d+
评注：提取ip地址时有用

提取信息中的ip地址: 
(\d+)\.(\d+)\.(\d+)\.(\d+)   

提取信息中的中国手机号码:
(86)*0*13\d{9}   

提取信息中的中国固定电话号码:
(\(\d{3,4}\)|\d{3,4}-|\s)?\d{8}   

提取信息中的中国电话号码（包括移动和固定电话）:
(\(\d{3,4}\)|\d{3,4}-|\s)?\d{7,14}   

提取信息中的中国邮政编码:
[1-9]{1}(\d+){5}   

提取信息中的中国身份证号码:
\d{18}|\d{15}   

提取信息中的整数：
\d+   

提取信息中的浮点数（即小数）：
(-?\d*)\.?\d+   

提取信息中的任何数字 ：
(-?\d*)(\.\d+)?

提取信息中的中文字符串：
[\u4e00-\u9fa5]*   

提取信息中的双字节字符串 (汉字)：
[^\x00-\xff]*

提取信息中的英文字符串：
\w*
提取信息中的网络链接:
(h|H)(r|R)(e|E)(f|F) *= *('|")?(\w|\\|\/|\.)+('|"| *|>)?  

提取信息中的邮件地址:
\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*

提取信息中的图片链接:
(s|S)(r|R)(c|C) *= *('|")?(\w|\\|\/|\.)+('|"| *|>)?

匹配特定数字：
^[1-9]\d*$　 　 //匹配正整数
^-[1-9]\d*$ 　 //匹配负整数
^-?[1-9]\d*$　　 //匹配整数
^[1-9]\d*|0$　 //匹配非负整数（正整数 + 0）
^-[1-9]\d*|0$　　 //匹配非正整数（负整数 + 0）
^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$　　 //匹配正浮点数
^-([1-9]\d*\.\d*|0\.\d*[1-9]\d*)$　 //匹配负浮点数
^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$　 //匹配浮点数
^[1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0$　　 //匹配非负浮点数（正浮点数 + 0）
^(-([1-9]\d*\.\d*|0\.\d*[1-9]\d*))|0?\.0+|0$　　//匹配非正浮点数（负浮点数 + 0）
评注：处理大量数据时有用，具体应用时注意修正
匹配特定字符串：
^[A-Za-z]+$　　//匹配由26个英文字母组成的字符串
^[A-Z]+$　　//匹配由26个英文字母的大写组成的字符串
^[a-z]+$　　//匹配由26个英文字母的小写组成的字符串
^[A-Za-z0-9]+$　　//匹配由数字和26个英文字母组成的字符串
^\w+$　　//匹配由数字、26个英文字母或者下划线组成的字符串
**************************************************************************************************/

/*这个函数是做测试用的*/
function doTest(){
	var table = $("#testResult"); /* table 对象 */
	var testList = $('test');  /*test标签对象数组*/
	var i = 0;
	
	//首先，让我们先画出表格的头部
	var head_cont = ['序号','测试用例','返回结果','结论']
	var tr_head = $(mk_tr());
	for(i=0;i<head_cont.length;i++){
		if(i==0){
			tr_head.append( mk_td( head_cont[i],'text-align:center','' ) ); /*序号要居中对齐*/
		}else{
			tr_head.append( mk_td( head_cont[i],'','text-left' ) ); /*其他左对齐*/
		}
	}
	table.append(tr_head);
	
	//然后开始绘制表格的主体
	//每次循环绘制一行
	for(i=0;i<testList.length;i++){ //有多少个test标签，就循环多少行
		var tr = $(mk_tr());
		var result = false;
		var words = '';
		tr.append( mk_td( ''+(i+1), 'text-align:center', 'text-center' ) );
		try{
			eval( 'result = '+$(testList[i]).attr("param") );
		}catch(e){
			result = '执行发生异常'
		}
		tr.append( mk_td( $(testList[i]).attr("param") ) );
		tr.append( mk_td( ''+result, '', 'text-left' ) ); /*这里输出的是函数的执行结果*/
		
		if( result.toString() == $(testList[i]).attr("expected") ){
			words = '执行结果正确，测试通过';
		}else{
			words = '<label class="text-error">执行结果错误，不能通过测试</label>';
		}
		tr.append( mk_td( words, '', 'text-left' ) );  /*然后根据执行结果，判断执行的正确与否*/
		table.append(tr); 
	}
}