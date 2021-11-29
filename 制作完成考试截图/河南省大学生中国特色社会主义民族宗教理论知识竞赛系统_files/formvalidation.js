/**
 * author：ZhangJK
 *
 *使用事例：
 * 	var is_mobile = Mibile_Validation.checkMobile("139343673", 0, "请输入正确的手机号码");
	if(!is_mobile){
		return; 
	}

 */
var mobile_validation=new Mibile_Validation();
function Mibile_Validation(){
	
	/**
	 * 非空校验
	 */
	Mibile_Validation.notEmpty=function(val,str){
		var tempValue=Mibile_Validation.trim(val);
		if(tempValue==""){
			Mibile_Validation.createErrorBox(str);
			return false;
		}
		return true;
	};
	
	/**
	 * 验证数字
	 * @param minLen:最小长度,不校验传0;maxLen:最大长度,不校验传0
	 */
	Mibile_Validation.isDigit=function(val,minLen,maxLen,str) { 
		//验证数字
		var patrn=/^\d|([1-9][0-9]{1,})$/; 
		if (!patrn.test(val)) {
			Mibile_Validation.createErrorBox(str);
			return false;
		}
		//长度验证
		var is_length = Mibile_Validation.lengthLimit(val, minLen, maxLen);
		if(!is_length){
			Mibile_Validation.createErrorBox(str);
			return false;
		}
		return true; 
	};
	
	/**
	 * 校验登录名：只能输入6-20个以字母开头、可带数字、“_”、“.”的字串 ,canImpty:1可以为空
	 */
	Mibile_Validation.checkUserName=function(val,canImpty,str) { 
		if(canImpty==1){
			if(val==""){
				return true;
			}
		}
		var patrn=/^[a-zA-Z]{1}([a-zA-Z0-9]|[._]){5,19}$/; 
		if (!patrn.test(val)) {
			Mibile_Validation.createErrorBox(str);
			return false ;
		}
		return true ;
	};
	
	/**
	 * 校验密码：只能输入6-20个字母、数字、下划线 
	 */
	Mibile_Validation.checkPwd=function(val) { 
		var patrn=/^(\w){6,20}$/; 
		if (!patrn.test(val)){
			Mibile_Validation.createErrorBox("密码格式不合法！只能输入字母、数字、下划线！");
			return false; 
		}
		return true ;
	};
	
	/**
	 * 校验密码：两次密码是否一致
	 */
	Mibile_Validation.checkRepeatPwd=function(val1,val2) { 
		if (val1!=val2){
			Mibile_Validation.createErrorBox("密码不一致！请重新输入");
			//val1="";
			//val2="";
			return false; 
		}
		return true ;
	};
	
	/**
	 * 校验普通电话、传真号码：可以“+”开头，除数字外，可含有“-” 
	 * @param canImpty:1,可空;0,必填
	 */
	Mibile_Validation.checkTel=function(val,canImpty) { 
		if(canImpty==1){
			if(val==""){
				return true;
			}
		}
		var patrn=/^[+]{0,1}(\d){1,3}[ ]?([-]?((\d)|[ ]){1,12})+$/; 
		if (!patrn.test(val)){
			Mibile_Validation.createErrorBox("电话/传真号码格式不正确！");
			return false ;
		}
		return true ;
	};
	
	/**
	 * 验证手机号
	 * @param canImpty:1,可空;0,必填
	 */
	Mibile_Validation.checkMobile=function(mobile,canImpty,str){	
		if(canImpty==1){
			if(mobile==""){
				return true;
			}
		}
		var re = /(^(\d{3,4}-)?\d{7,8})$|(1[3456789][0-9]{9})$/;    
		if(!(re.test(mobile))){ 
			Mibile_Validation.createErrorBox(str);
			return false;
		}
		return true;
	};
	
	/**
	 * 验证身份证号
	 * @param canImpty:1,可空;0,必填
	 */
	Mibile_Validation.checkIDCard=function(idCard,canImpty,str){	
		if(canImpty==1){
			if(idCard==""){
				return true;
			}
		}
		var re = /^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])((\d{4})|\d{3}[A-Z])$/;    
		if(!(re.test(idCard))){ 
			Mibile_Validation.createErrorBox(str);
			return false;
		}
		return true;
	};
	/**
	 * 只能是数字
	 */
	Mibile_Validation.isNumber=function(val,str){
		var reg = /^[1-9]*[1-9][0-9]*$/; 
		if(!reg.test(val)) {
			Mibile_Validation.createErrorBox(str);
			return false; 
		}
		return true;
	};
	
	/**
	 * 只能是汉字
	 */
	Mibile_Validation.isChinese=function(val,str){
		var reg = /^[\u4e00-\u9fa5]+$/gi; 
		if(!reg.test(val)) {
			Mibile_Validation.createErrorBox(str);
			return false; 
		}
		return true;
	};
	
	/**
	 * 长度限制
	 * @param obj:对象,minLen:最小长度,maxLen:最大长度
	 */
	Mibile_Validation.lengthLimit=function(val,minLen,maxLen,str){
		if(minLen>0&&maxLen>0){
			if(val.length<minLen||val.length>maxLen){
				Mibile_Validation.createErrorBox(str);
				return false;
			}
		}else if(maxLen>0){
			if(val.length>maxLen){
				Mibile_Validation.createErrorBox(str);
				return false;
			}
		}else if(minLen>0){
			if(val.length<minLen){
				Mibile_Validation.createErrorBox(str);
				return false;
			}
		}
		return true;
	};
	
	/**
	 * 验证邮箱格式
	 * @param canImpty:1,可空;0,必填
	 */
	Mibile_Validation.isEmail=function(val,canImpty,str) {
		if(canImpty==1){
			if(val==""){
				return true;
			}
		}
		if (val.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/) != -1){
			return true;
		}else{
			Mibile_Validation.createErrorBox(str);
			return false;
		}
	};
	/**
	 * 验证车牌号
	 * @param canImpty:1,可空;0,必填
	 */
	Mibile_Validation.isCarNum=function(val,canImpty,str) {
		if(canImpty==1){
			if(val==""){
				return true;
			}
		}
		if (val.search(/^[\u4e00-\u9fa5]{1}[A-Z]{1}[A-Z_0-9]{5}$/) != -1){
			return true;
		}else{
			Mibile_Validation.createErrorBox(str);
			return false;
		}
	};
	
	/**
	 * 去掉首尾空格
	 */
	Mibile_Validation.trim=function(str) {   
		if(str==""||str==null){
			return str;
		}else{
			return str.replace(/(^\s*)|(\s*$)/g, "");   
		}
	   
	}; 
	
	/**
	 * 重置表单
	 * @para formseq:表单序号
	 */
	Mibile_Validation.resetForm=function(formSeq){
		var obj = null;   
		for (var i = 0; i <= document.forms[0].elements.length - 1; i++) 
		{     
			obj = frm1.elements[i];        
			if (obj.tagName == "INPUT" && obj.type == "text") 
			{            
				obj.setAttribute("value", "");        
			}        
			if (obj.tagName == "INPUT" && obj.type == "checkbox") 
			{            
				obj.setAttribute("checked", false);        
			}        
			if (obj.tagName == "SELECT") 
			{            
				obj.options[0].selected = true;       
			}    
		}
		return false;
	};
	
	/**
	 * 创建错误提示框
	 */
	Mibile_Validation.createErrorBox=function(str) {   
		//alert(str);
		layer.alert(str);
		
	};
}
