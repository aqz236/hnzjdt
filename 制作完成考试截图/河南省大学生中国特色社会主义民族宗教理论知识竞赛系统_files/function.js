//金额大小写转换
//如我输入100.999后应该显示101.00，对应大写也是壹百零壹元整。
// alert(money(211199.999));

function money(mon){            
	var smon = Math.round(mon*100);            
	var splot = smon % 100;            
	var zheng = parseInt(smon / 100);            
	var ch_key = new Array('零','壹','贰','叁','肆','伍','陆','柒','捌','玫');            
	var dan_key = new Array('拾','佰','仟','万','拾万','百万','仟万','亿');            
	var str_num = zheng+'';            
	var len  = str_num.length;            
	var slen = len-1;            
	var rs = ''            
	for(var i = 0;i<len;i++){                
		var ch = parseInt(str_num.charAt(i));                
		rs += ch_key[ch];                
		slen --;                
		if(ch > 0 && slen >= 0) 
		rs += dan_key[slen];                            
	}            
	if(splot == 0){                
		rs += '元整';            
	}else{                
		var str = splot + '';               
	 	var ch = parseInt(str.charAt(0));                
	 	rs += '点' + ch_key[ch];                
	 	ch = parseInt(str.charAt(1));                
	 	rs += ch_key[ch]  + '元';            
	}            
 	return rs;        
 }  
 function getCurrentDateTimeStr(){
	var myDate = new Date();
	var year=myDate.getFullYear();    //获取完整的年份(4位,1970-????)
	var month=myDate.getMonth();       //获取当前月份(0-11,0代表1月)
	var date=myDate.getDate();        //获取当前日(1-31)
	var hours=myDate.getHours();       //获取当前小时数(0-23)
	var minutes=myDate.getMinutes();     //获取当前分钟数(0-59)
	var seconds=myDate.getSeconds();     //获取当前秒数(0-59)
	var currentDateTime=year+"-"+month+"-"+date+" "+hours+":"+minutes+":"+seconds;
	currentDateTime=DateFormat(currentDateTime,"yyyy-MM-dd hh:mm:ss")
	return currentDateTime;
 }      
/**       
 * 对Date的扩展，将 Date 转化为指定格式的String       
 * 月(M)、日(d)、12小时(h)、24小时(H)、分(m)、秒(s)、周(E)、季度(q) 可以用 1-2 个占位符       
 * 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)       
 * eg:       
 * DateFormat("2006-07-02","yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423       
 * DateFormat("2009-03-10 20:09:04","yyyy-MM-dd E HH:mm:ss") ==> 2009-03-10 二 20:09:04       
 * DateFormat("2009-03-10 08:09:04","yyyy-MM-dd EE hh:mm:ss") ==> 2009-03-10 周二 08:09:04       
 * DateFormat("2009-03-10 08:09:04","yyyy-MM-dd EEE hh:mm:ss") ==> 2009-03-10 星期二 08:09:04       
 * DateFormat("2006-07-02 08:09:04","yyyy-M-d h:m:s.S") ==> 2006-7-2 8:9:4.18        
var date = new Date();        
window.alert(DateFormat("009-03-10","yyyy-MM-dd hh:mm:ss"));        
 */          
function DateFormat(dateTimeStr,fmt) { 
    var date= new Date(Date.parse(dateTimeStr.replace(/-/g,   "/"))); //转换成Date();        
    var o = {           
    "M+" : date.getMonth()+1, //月份           
    "d+" : date.getDate(), //日           
    "h+" : date.getHours()%12 == 0 ? 12 : date.getHours()%12, //小时           
    "H+" : date.getHours(), //小时           
    "m+" : date.getMinutes(), //分           
    "s+" : date.getSeconds(), //秒           
    "q+" : Math.floor((date.getMonth()+3)/3), //季度           
    "S" : date.getMilliseconds() //毫秒           
    };           
    var week = {           
    "0" : "/u65e5",           
    "1" : "/u4e00",           
    "2" : "/u4e8c",           
    "3" : "/u4e09",           
    "4" : "/u56db",           
    "5" : "/u4e94",           
    "6" : "/u516d"          
    };           
    if(/(y+)/.test(fmt)){           
        fmt=fmt.replace(RegExp.$1, (date.getFullYear()+"").substr(4 - RegExp.$1.length));           
    }           
    if(/(E+)/.test(fmt)){           
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[date.getDay()+""]);           
    }           
    for(var k in o){           
        if(new RegExp("("+ k +")").test(fmt)){           
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));           
        }           
    }           
    return fmt;           
}      

//+---------------------------------------------------
//| 求两个时间的天数差 日期格式为 YYYY-MM-dd  
//|alert(daysBetween('2013-12-07','2013-12-08'));
//+---------------------------------------------------
function daysBetween(DateOne,DateTwo){
	var OneMonth = DateOne.substring(5,DateOne.lastIndexOf ('-'));
	var OneDay = DateOne.substring(DateOne.length,DateOne.lastIndexOf ('-')+1);
	var OneYear = DateOne.substring(0,DateOne.indexOf ('-'));
	var TwoMonth = DateTwo.substring(5,DateTwo.lastIndexOf ('-'));
	var TwoDay = DateTwo.substring(DateTwo.length,DateTwo.lastIndexOf ('-')+1);
	var TwoYear = DateTwo.substring(0,DateTwo.indexOf ('-'));
	var cha=((Date.parse(TwoMonth+'/'+TwoDay+'/'+TwoYear)-Date.parse(OneMonth+'/'+OneDay+'/'+OneYear))/86400000);
	//Math.abs(cha);
	return cha;
} 
//------------------------------------------------------------------------------------------------------------------------
function inputPrice(activexid){
	var activexObj=$("#"+activexid);
	activexObj.addClass("mask-pnum"); // 追加样式 
	activexObj.bind('input propertychange', function() {
	  var price=activexObj.val();
		if(isNaN(price)){
		    activexObj.val("");
		}else{
		     var priceArray=price.split(".");
			 if(priceArray.length==2){
				 if(priceArray[1].length>2){
				 	activexObj.val(priceArray[0]+"."+priceArray[1].substring(0,2))
			      }
			 }
		}     
	});	
}
function inputInt(activexid){
	    var activexObj=$("#"+activexid);
		activexObj.addClass("mask-pint"); // 追加样式 
		activexObj.bind('input propertychange', function() {
		  var value=activexObj.val();
			if(isNaN(value)){
			    activexObj.val("");
			}     
		});	
}
//------------------------------------------------------------------------------------------------------------------------
function getYuanByFen(fen){
    if (isNaN(parseInt(fen))){return 0.00}
	var yuan=parseInt(fen)/100;
	yuan=yuan.toFixed(2);
	return yuan;
}
function getFenByYuan(yuan){
     if (isNaN(yuan)){return 0}
    var fen = Math.round(yuan*100); 
	return fen;
}
//去掉空格
function ClearTrim(str){
    var result="";
    if(str==null)result="";
    if(str=="null")result="";
    if(str!=null)result=str.replace(/^\s*|\s*$/g,"");
	return result;
}
function getInt(str,defaultNum){
   if (isNaN(parseInt(str))){
   	 return defaultNum
   }
    return str;
}
function isWeiXin(){
    var ua = window.navigator.userAgent.toLowerCase();
    if(ua.match(/MicroMessenger/i) == 'micromessenger'){
        return true;
    }else{
        return false;
    }
}
/**
 * [mobileType 判断平台]
 * @param test: 0:iPhone    1:Android
 */
function mobileType(){
    var u = navigator.userAgent, app = navigator.appVersion;
    if(/AppleWebKit.*Mobile/i.test(navigator.userAgent) || (/MIDP|SymbianOS|NOKIA|SAMSUNG|LG|NEC|TCL|Alcatel|BIRD|DBTEL|Dopod|PHILIPS|HAIER|LENOVO|MOT-|Nokia|SonyEricsson|SIE-|Amoi|ZTE/.test(navigator.userAgent))){
     if(window.location.href.indexOf("?mobile")<0){
      try{
       if(/iPhone|mac|iPod|iPad/i.test(navigator.userAgent)){
        return '0';
       }else{
        return '1';
       }
      }catch(e){}
     }
    }else if( u.indexOf('iPad') > -1){
        return '0';
    }else{
        return '1';
    }
};
function getUseraccountType(useraccount){
		 var type="useraccount";
	 	 var mobile_partten = /^1[3-9]\d{9}$/;
		 if(mobile_partten.test(useraccount)){
		    type="mobile";
		    return type;
		 }
		var email_partten = /^(?:[a-z0-9]+[_\-+.]?)*[a-z0-9]+@(?:([a-z0-9]+-?)*[a-z0-9]+\.)+([a-z]{2,})+$/i;
	    if(email_partten.test(useraccount)){
	        type="mail";
	         return type;
	    }
	   return type;
}
function getColPicPath(colpicvalue){
    var pic=colpicvalue;
    if(pic==null)pic="";
    if(pic=="null")pic="";
	 if(pic==""){
		pic=rootPath+"/uploadpage/swfupload/images/noimg.png";
	}else{				    	
		if(pic.indexOf("http")==-1){
			pic=fileServerUrl+"/"+pic;
		}else{
			pic=pic;
		}
	}  
	return pic;    
}
//js加密
function encode64(input){
			var keyStr = "ABCDEFGHIJKLMNOP" +"QRSTUVWXYZabcdef" +"ghijklmnopqrstuv" +"wxyz0123456789+/" + "=";
		   var output = "";
			 var chr1, chr2, chr3 = "";
			 var enc1, enc2, enc3, enc4 = "";
			 var i = 0;
			 do
			 {
				 chr1 = input.charCodeAt(i++);
				 chr2 = input.charCodeAt(i++);
				 chr3 = input.charCodeAt(i++);
				 enc1 = chr1 >> 2;
				 enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
				 enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
				 enc4 = chr3 & 63;
				 if (isNaN(chr2)){
					 enc3 = enc4 = 64;
				 }else if (isNaN(chr3)){
					 enc4 = 64;
				 }
				 output = output +
				 keyStr.charAt(enc1) +
				 keyStr.charAt(enc2) +
				 keyStr.charAt(enc3) +
				 keyStr.charAt(enc4);
				 chr1 = chr2 = chr3 = "";
				 enc1 = enc2 = enc3 = enc4 = "";
			 } while (i < input.length);
			 return output;
		}	


//得到复选框的值
function getCheckBoxValue(activeXName){
    var result="";
	var obj=document.getElementsByName(activeXName);
	for(i=0;i<obj.length;i++){	
				if(obj[i].checked==true){
				    if(result!="")result+=",";
					result+=obj[i].value;					
				}				
			}
   return result;
}
//得到单选框的值
function getRadioValue(activeXName){
    var result="";
	var obj=document.getElementsByName(activeXName);
	for(i=0;i<obj.length;i++){	
				if(obj[i].checked==true){
					result=obj[i].value;					
				}				
			}
   return result;
}
//--复选框只选择一条记录objName为复选框的name-----------------------------------------------------------------
function singleRow(objName){
    var a =jQuery("input[name='"+objName+"']");
	a.click(function(){	
		jQuery.each(a, function(k, v) {
			jQuery(this).attr("checked", false);
		});
		jQuery(this).attr("checked", true);
		})
}
//--复选框选择所有-----------------------------------------------------------------
function checkBoxAll(objName,allName){
  var objArray=document.getElementsByName(objName);
  var checkAllObj=document.getElementsByName(allName);
  for (var i=0;i<objArray.length;i++){
    var e = objArray[i];
    if ((e.name != allName)&&(e.type.indexOf("checkbox")!=-1))
       e.checked = checkAllObj[0].checked;
    }
}
//--复选框得到值-----------------------------------------------------------------
function checkBoxObj(objName){
  var objArray=document.getElementsByName(objName);
  var row=0;
  var value="";
   for (var i=0;i<objArray.length;i++){
	   if(objArray[i].checked){
		   row++;
		   if(value!="")value+=",";
		   value+=objArray[i].value;
	   }
   }
   var Item=new Object(); 
   Item.row=row;
   Item.value=value;
   return Item;
}

//--某一列的值-----------------------------------------------------------------
function tdObj(objName){
  var objArray=document.getElementsByName(objName);
  var row=0;
  var value="";
   for (var i=0;i<objArray.length;i++){
	   if(objArray[i].checked){
		   row++;
		   if(value!="")value+=",";
		   value+=objArray[i].value;
	   }
   }
   var Item=new Object(); 
   Item.row=row;
   Item.value=value;
   return Item;
}
/**
obj={
url:url,//请求地址 
data:data,//请求参数
async:async,//如果是true,则为异步，如果是false则为同步，默认为同步
}
*/
function getRequestJson(obj){
var jd=null;
jQuery.ajax({url:obj.url,
			type:'post',
			async: false,      //ajax同步
			dataType:"html",
			data:obj.data,//URL参数
			success:function(responseText){
				jd=eval("("+responseText+")");//转化为json串
		       },
		    error:function(){
	           alert("错误");
	        }
	        })
	    
return jd;
}
/**
obj={
okobj:okobj
url:url,//请求地址 
data:data,//请求参数
async:async,//如果是true,则为异步，如果是false则为同步，默认为同步
"renderer":function(jsonObj){					//结果函数
			if(jsonObj.success=="1")window.location.reload();
			if(jsonObj.success!="1")alert(jsonObj.msg);
			             } 
}
*/
function getRequestAsyJson(obj){
if(obj.okobj!=null)obj.okobj.disabled=true;
var async=false;
if(obj.async!=null)async=obj.async;
jQuery.ajax({url:obj.url,
			type:'post',
			async: async,      //ajax异步
			dataType:"html",
			data:obj.data,//URL参数
			success:function(responseText){
			    if(obj.okobj!=null)obj.okobj.disabled=false;
				var jsonObj=eval("("+responseText+")");//转化为json串
				obj.renderer(jsonObj);
		       },
		    error:function(){
		     obj.okobj.disabled=false;
	           alert("错误");
	        }
	        })
}
//----------------------------------------------------------------------------------------------------------------------------------
function getSSM(){
	var ssm="";
	var url=rootPath+"/com/common/appAction.php?action=ssm"
	jQuery.ajax({url:url,
				type:'post',
				async: false,      
				dataType:"html",
				data:null,//URL参数
				success:function(responseText){
					ssm=responseText;
					ssm=encode64(ssm);
			       },
			    error:function(){
			     
		        }
		        })
	return ssm
}
//----------------------------------------------------------------------------------------------------------------------------------
function getXXM(){
	var xxm="";
	var url=rootPath+"/com/common/appAction.php?action=xxm"
	jQuery.ajax({url:url,
				type:'post',
				async: false,      
				dataType:"html",
				data:obj.data,//URL参数
				success:function(responseText){
				 xxm=responseText;
			       },
			    error:function(){
			     
		        }
		        })
	return xxm
}

//----------------------------------------------------------------------------------------------------------------------------------
/*
下拉iframe数据选择
selectData({
    activeId:"warename"
    ,width:600
    ,height:400
	,url:"http://www.baidu.com"
	,btntitle:"选择"					
});
*/
function selectData(gridObj){
	var activex_obj=$("#"+gridObj.activeId);
	var btnId="btn_"+gridObj.activeId;//选择按钮Id
	var menuContentId="menuContent_"+gridObj.activeId;//菜单
	var iframeid="iframe_"+gridObj.activeId;
	
	$("#"+btnId).empty();
	activex_obj.after("<a id=\""+btnId+"\"  style=\"cursor:pointer;padding:3px;background:#ff7f00;color:#fff; text-align:center;line-height:25px;\">"+gridObj.btntitle+"</a>");
	$("#"+btnId).bind("click", function(){
	        new function showMenu() {
				var cityOffset = activex_obj.offset();
				$("#"+menuContentId).css({left:cityOffset.left + "px", top:cityOffset.top + activex_obj.outerHeight() + "px"}).slideDown("fast");
				$("body").bind("mousedown", function(event){
						if (!(event.target.id == btnId ||event.target.id == menuContentId || $(event.target).parents("#"+menuContentId).length>0))SelectDataHideMenu(gridObj);
				});
			}
	
	});
	var menuContent="";
	menuContent+="<div id=\""+menuContentId+"\"  style=\"display:none;position: absolute;min-width:"+gridObj.width+"px;height:"+gridObj.height+"px;background: #f0f6e4;\">";
	menuContent+="</div>";
	$("#"+btnId).after(menuContent);
	$("#"+menuContentId).html("<iframe id=\""+iframeid+"\" src=\""+gridObj.url+"\" width=\""+gridObj.width+"\" height=\""+gridObj.height+"\" frameborder=\"0\" style=\"border: 1px solid #617775;\"></iframe>");	
}
function SelectDataHideMenu(gridObj) {
            var menuContentId="menuContent_"+gridObj.activeId;
			$("#"+menuContentId).fadeOut("fast");
			$("body").unbind("mousedown", function(event){
				if (!(event.target.id == menuContentId || $(event.target).parents("#"+menuContentId).length>0))SelectDataHideMenu(gridObj);
			});
		}
function SelectDataHideDiv(activeId) {	
            var menuContentId="menuContent_"+activeId;
			$("#"+menuContentId).fadeOut("fast");
			$("body").unbind("mousedown", function(event){
				if (!(event.target.id == menuContentId || $(event.target).parents("#"+menuContentId).length>0))SelectDataHideMenu(gridObj);
			});
}	
//----------------------------------------------------------------------------------------------------------------------------------
//=============多个图片预览start
function InitUplodPic(activeID,fileNum){
  var goodpic_div_id=activeID+"_div";
  var iframe_div_id=activeID+"_upload_iframe";
  var piccontent="";
      piccontent+="<div class='goodpic' id='"+goodpic_div_id+"'>";
      piccontent+="<ul>";
      for(var i=0;i<fileNum;i++){
         var picLiId=activeID+"_"+i;
         piccontent+="<li id='"+picLiId+"' ><img src=\""+rootPath+"/etc/core/img/good.jpg\"/></li>";
      }
       piccontent+="</ul>";
       piccontent+="<iframe";
       piccontent+=" id=\""+iframe_div_id+"\" name=\""+iframe_div_id+"\"";
       piccontent+=" src=\""+rootPath+"/uploadpage/swfupload/big_upload.jsp?uploadparam="+uploadparam+"&containerId="+activeID+"\"";
       piccontent+=" width=\"400\"";
       piccontent+=" height=\"35\"";
       piccontent+=" frameborder=\"no\"";
       piccontent+=" scrolling=\"no\"";
       piccontent+=" border=\"0\"";
       piccontent+=" marginwidth=\"0\"";
       piccontent+=" marginheight=\"0\"";
       piccontent+="></iframe>";
       piccontent+="</div>";
      $("#"+activeID).after(piccontent);
      UplodPicChange(activeID,goodpic_div_id,iframe_div_id,fileNum);
      $("#"+goodpic_div_id+" ul li").click(function(){$(this).addClass("on").siblings().removeClass("on");});
	  $("#"+activeID).bind('input propertychange', function() {UplodPicChange(activeID,goodpic_div_id,iframe_div_id,fileNum);});
	  $("body").bind("mousemove", function () {UplodPicChange(activeID,goodpic_div_id,iframe_div_id,fileNum);});	
}
function UplodPicChange(activeID,goodpic_div_id,iframe_div_id,fileNum){
	      var pathArray=$("#"+activeID).val().split(",");
		  for(var i=0;i<pathArray.length;i++){
		             if(pathArray[i]=="")continue;
		             var picImg=$("#"+activeID+"_"+i+" img");
				  	 picImg.attr("src",fileServerUrl+"/"+pathArray[i]);
				  	 picImg.dblclick(function(){window.open($(this).attr('src'));});
				  	 var picLi=$("#"+activeID+"_"+i);
				  	 picLi.click(function(){
				  	      var current_i=0;
				  	      var currentId=$(this).attr('id');
				  	      $("#"+goodpic_div_id+" ul li").each(function(j){if($(this).attr('id')==currentId)current_i=j;});
					  	  $("#"+iframe_div_id).attr("src",fileServerRoot+"/swfupload/big_upload.jsp?uploadparam="+uploadparam+"&containerId="+activeID+"&i="+current_i+"&random="+Math.random());
				  	 })
		  }	
		  if(fileNum>pathArray.length){
			  for(var i=pathArray.length;i<fileNum;i++){
			            var picLi=$("#"+activeID+"_"+i);
					  	 picLi.click(function(){
					  	      var current_i=0;
					  	      var currentId=$(this).attr('id');
					  	      $("#"+goodpic_div_id+" ul li").each(function(j){if($(this).attr('id')==currentId)current_i=j;});
						  	  $("#"+iframe_div_id).attr("src",fileServerRoot+"/swfupload/big_upload.jsp?uploadparam="+uploadparam+"&containerId="+activeID+"&i="+current_i+"&random="+Math.random());
					  	 })
			  
			  }
		  }
	}	
//=============单 个图片预览start
/*
上传 文本 的 class="singlepic";
例如 <input type="hidden" name="pic" id="pic" class="singlepic" tip=""  uploadparam="<?php echo Fun::encode("GOODS_PRODUCT_0");?>"  value="<?php echo($obj["PIC"]);?>">
必须 属性:
 class="uploadsinglepic"
 uploadtype="pic"   //pic为图片 video为 视频 file为文件 
 tip=""  
 uploadparam="<?php echo Fun::encode("GOODS_PRODUCT_0");?>"  
 value="<?php echo($obj["PIC"]);?>"
*/
function singlePicUpload(){
	function singlePicUploadInit(activexid){
		var virvalue = $("#"+activexid).val();
		var uploadtype     = $("#"+activexid).attr("uploadtype");
		var imgsrc   = $("#"+activexid+"_img").attr("src");
		if(uploadtype==null || uploadtype=="") uploadtype="pic";
		if(virvalue!=imgsrc){
			 var filepath="";
			 var imgurl="";
			 if(virvalue==""){
				imgurl=rootPath+"/uploadpage/swfupload/images/noimg.png";
				 if(uploadtype=="pic")imgurl=rootPath+"/uploadpage/swfupload/images/noimg.png";
				 if(uploadtype=="video")imgurl=rootPath+"/uploadpage/swfupload/images/novideo.jpg";
				 if(uploadtype=="file")imgurl=rootPath+"/uploadpage/swfupload/images/nofile.jpg";
			 }else{
				var isHttp=virvalue.indexOf("http");
				if(isHttp!=0)filepath=fileServerUrl+"/"+virvalue; 
				if(isHttp==0)filepath=virvalue;
				 if(uploadtype=="pic")imgurl=filepath;;
				 if(uploadtype=="video")imgurl=rootPath+"/uploadpage/swfupload/images/video.jpg";
				 if(uploadtype=="file")imgurl=rootPath+"/uploadpage/swfupload/images/file.jpg";
			 }
			 $("#"+activexid+"_img").attr({ src:imgurl }); 
			 $("#"+activexid+"_img").wrap("<a href='" +filepath + "'  target='_blank'/>");
		 } 
	}
	$(".uploadsinglepic").css({"background":"url("+rootPath+"/uploadpage/swfupload/images/selectpic.png) no-repeat right","cursor":"pointer"});
	$(".uploadsinglepic").bind("dblclick", function(){
		var activexid   = $(this).attr("id");
		var uploadparam = $(this).attr("uploadparam");
		/*
		var params=null;
		var picsurl=rootPath+"/uploadpage/picsAction.php?activexid="+activexid;
		$.post(picsurl,params,function(responseText){
			layer.tab({
				  area: ['800px', '560px'],
				  shade: 0.1,
				  tab: [{
				    title: '选择图片', 
				    content: responseText
				  }, {
				    title: '上传图片', 
				    content: '内容2'
				  }]
				});
			
			
			
			
		})
	/** */
		layer.open({
			  type: 2,
			  title: '上传文件',
			  shadeClose: true,
			  shade: 0.1,
			  area: ['450px', '300px'],
			  btn: ['确定', '取消'], //只是为了演示
		        yes: function(){
		        	layer.closeAll();
		      },
		      btn2: function(){
		          layer.closeAll();
		      },
			  content: rootPath+"/uploadpage/upload/upload.php?uploadparam="+uploadparam+"&containerId="+activexid //iframe的url
			 // content: rootPath+"/uploadpage/pics.php?activexid="+activexid //iframe的url
			}); 
		 
		
	})
	
	$("body").on("mousemove",function(){ 
		$(".uploadsinglepic").each(function(index){ 
			var activexid   = $(this).attr("id");
			singlePicUploadInit(activexid);
		})
	})
	$(".uploadsinglepic").on("propertychange",function(){   
		var activexid   = $(this).attr("id");
		singlePicUpload(activexid);
	}).each(function(index){ 
		var activexid   = $(this).attr("id");
		var uploadparam = $(this).attr("uploadparam");
		var tip         = $(this).attr("tip");
		if(tip=="")tip="&nbsp;图片内容必须清晰可见。"
		var uploadpage_url=rootPath+"/uploadpage/swfupload/big_upload.php?uploadparam="+uploadparam+"&containerId="+activexid;
		uploadpage_url=rootPath+"/uploadpage/layuiupload/big_upload.php?uploadparam="+uploadparam+"&containerId="+activexid;
		var content="<ul style='height:77px;'>";
		    content+="	<li style=\"float:left;\">";
		    content+="		<img  id=\""+activexid+"_img\" src=\""+rootPath+"/uploadpage/swfupload/images/noimg.png\" style=\"cursor:pointer;margin:0px;border: 2px solid #d7d7d7;width:73px;height:73px;\"/>";
		    content+="	    <div style=\"clear: both;\"></div>";
		    content+="	</li>";
		    content+="	<li style=\"float:left;\">";
		    content+="		<iframe  src=\""+uploadpage_url+"\"  width=\"500\" height=\"35\" frameborder=\"no\" scrolling=\"no\" border=\"0\" marginwidth=\"0\" marginheight=\"0\"></iframe>";
		    content+="		<div style=\"line-height:35px;\" id=\""+activexid+"_msg\">"+tip+"</div>";
		    content+="	    <div style=\"clear: both;\"></div>";
		    content+="	</li>";
		    content+="	<div style=\"clear: both;\"></div>";
		    content+="</ul>";
		    $("#"+activexid+"_con").empty().append(content);
		    //$("#"+activexid).after(content);
		    singlePicUploadInit(activexid);
	});
}
//=============多个图片预览end
//=============单个图片预览end
//=============多个图片预览

//=============多个图片预览end
//=============单个图片预览end
//=============多个图片预览
//上传图个图片或文件
function moreFileUpload(){
	$(".uploadmorefile").each(function(index){ 
		var activexid   = $(this).attr("id");
		var width       = $(this).attr("width");
		var height      = $(this).attr("height");
		var uploadtype  = $(this).attr("uploadtype");
		var uploadparam = $(this).attr("uploadparam");
		var tip         = $(this).attr("tip");
	    if(width==null)width="";
	    if(height==null)height="";
	    if(uploadtype==null)uploadtype="pic";
		if(width=="")width=500;
		if(height=="")height=72;
		var content="<iframe  src=\""+rootPath+"/uploadpage/layuiupload/more_upload.php?uploadparam="+uploadparam+"&containerId="+activexid+"&uploadtype="+uploadtype+"\"  width=\""+width+"\" height=\""+height+"\" frameborder=\"no\" scrolling=\"no\" border=\"0\" marginwidth=\"0\" marginheight=\"0\"></iframe>";
		$("#"+activexid+"_con").empty().append(content);
	});
}
//=============多个图片预览end
//=============单个图片预览end
//=============多个图片预览
function InitKindEditor(actives){
  document.write("<link href=\""+rootPath+"/uploadpage/kindeditor/themes/default/default.css\" rel=\"stylesheet\" type=\"text/css\"></link>");
  document.write("<script charset=\"utf-8\"  src=\""+rootPath+"/uploadpage/kindeditor/kindeditor-all-min.js\"></script>");
  document.write("<script charset=\"utf-8\"  src=\""+rootPath+"/uploadpage/kindeditor/lang/zh-CN.js\"></script>");
   $(document).ready(function(){ 
	   var xxm=getXXM();
		  var uploadJson = rootPath+'/uploadpage/kindeditor/php/upload_json.php?xxm='+xxm;
		  var activeArray=actives.split(",");
		  KindEditor.ready(function(K) {
			for(var i=0;i<activeArray.length;i++){
			K.create('textarea[name="'+activeArray+'"]', {
						cssPath : rootPath+'/uploadpage/kindeditor/plugins/code/prettify.css',
						uploadJson : uploadJson,
						fileManagerJson : rootPath+'/uploadpage/kindeditor/php/file_manager_json.php?xxm='+xxm,
						allowFileManager :false,
						allowUpload : false, 
						fillDescAfterUploadImage :false,//上传图片后跳转到图片编辑页面
						//pagebreakHtml : '$$$$$$', //自定义分页符
						afterCreate : function() {var self = this;self.sync();},
						afterChange : function() {var self = this;self.sync();},
						afterBlur : function() {var self = this;self.sync();}
					});
			}
		 })
 })
}
function systip(tipid,msg){
	 var tipObj=$("#"+tipid);
    tipObj.css("display","");
    tipObj.html("<font class=\"cred\">"+msg+"</font>")
	tipObj.fadeOut(2000,function(){tipObj.html("");});
}
/////----------------------------------------------------------------------------------------------------------------------------
function fnChangeName(value,jsArray){
                 var result="";
			       for(var i=0;i<jsArray.length;i++){
				       if((""+value)==(jsArray[i][0]+"")){
					       result=jsArray[i][1];
					       break;
				       }
			       }
			       return result;
         }
//文本框，按钮样式=============
function form_style(){
	var aray =document.getElementsByTagName("td");
	for(var i = 0; i<aray.length; i++) {if(aray[i].innerHTML=="")aray[i].innerHTML="&nbsp;";}
	//按钮样式以及文本样式
	var list_input=document.getElementsByTagName("input");//获取input表单并付给数组
	for(var i=0;i<list_input.length &&list_input[i];i++){
	    if(list_input[i].className!="")continue;
	    if(list_input[i].type.indexOf("button") !=  -1)list_input[i].className="layui-btn layui-btn-sm layui-btn-normal";
		if(list_input[i].type.indexOf("text") !=  -1)list_input[i].className="hmui-input";
		if(list_input[i].type.indexOf("password") !=  -1)list_input[i].className="hmui-input";	
		if(list_input[i].type.indexOf("submit") !=  -1)list_input[i].className="layui-btn layui-btn-sm layui-btn-normal";
		if(list_input[i].type.indexOf("reset") !=  -1)list_input[i].className="layui-btn layui-btn-sm layui-btn-normal";
		if(list_input[i].type.indexOf("file") !=  -1)list_input[i].className="hmui-textarea";
	    //--
	    if(list_input[i].disabled ==true&&list_input[i].type.indexOf("checkbox") ==  -1)list_input[i].className="input_text_reaonly";
	} 
//大文本框样式
	var list_textarea=document.getElementsByTagName("textarea");//获取textarea表单并付给数组
   	for(var i=0;i<list_textarea.length &&list_textarea[i];i++){list_textarea[i].className="hmui-input";}
 //下拉框 
 	var list_select=document.getElementsByTagName("select");//获取select表单并付给数组
   	for(var i=0;i<list_select.length &&list_select[i];i++){
   	    list_select[i].className="hmui-input";
   	    if(list_select[i].disabled ==true)list_select[i].className="hmui-input input_text_reaonly";
    }
}
