

initAnswerFn();
function initAnswerFn(){
	var content_mid="";
	for(var i=0;i<topicJsonArray.length;i++){
		if(topicJsonArray[i]!=null){
			var topicid=topicJsonArray[i]["TOPICID"];
			var type=topicJsonArray[i]["TYPE"];
			  var activename="topicid_"+topicid;
			 var result="";
			  if(type=="1"){
				  result=getRadioValue(activename)
			  }else{
				  result=getCheckBoxValue(activename)
			  }
			  if(result==""){
				  content_mid+="<li  topicid=\""+topicid+"\" id=\"examanswer_"+topicid+"\">"+(i+1)+"</li>";
			  }else{
				  content_mid+="<li class=\"on\" topicid=\""+topicid+"\" id=\"examanswer_"+topicid+"\">"+(i+1)+"</li>";
			  }
			
			
		}
		
	}
	var content="<ul>"+content_mid+"</ul>"
	$(".answer .bd").html(content);
}
$(".answer ul li").bind("click", function(){
	var topicid=$(this).attr("topicid")
	window.location.hash = "#topicid_"+topicid;
})
//=============================================================================================================================================================
$("input[type='radio']").bind("click", function(){
	var topicid=$(this).attr("topicid");
	var orderindex=$(this).attr("orderindex");
	result=getRadioValue("topicid_"+topicid);
	$("#examanswer_"+topicid).addClass("on");
	
})
$("input[type='checkbox']").bind("click", function(){
	var topicid=$(this).attr("topicid");
	var orderindex=$(this).attr("orderindex");
	result=getCheckBoxValue("topicid_"+topicid);
	if(result==""){
		$("#examanswer_"+topicid).addClass("over");
	}else{
		$("#examanswer_"+topicid).addClass("on");
	}

	
})



//=============================================================================================================================================================
if(exam_mins<=0)autoSubmit();
setCountDown_time();
/*时间倒计时*/
var sec = 60,min = exam_mins;
var format = function(str) {
	var x1 = Math.floor((Math.random()*10))+'';
	  var x2 = Math.floor((Math.random()*10))+'';
	  var x3 = Math.floor((Math.random()*10))+'';
	  var x4 = Math.floor((Math.random()*10))+'';
	  var x5 = Math.floor((Math.random()*10))+'';
	  randomStr = x1 + x2 + x3 + x4 + x5
      // alert("试题：第"+noquestion_content+"题，尚未作答");
		var date = new Date();
		var year = date.getFullYear();        //年 ,从 Date 对象以四位数字返回年份
		var month = date.getMonth() + 1;      //月 ,从 Date 对象返回月份 (0 ~ 11) ,date.getMonth()比实际月份少 1 个月
		var day = date.getDate();             //日 ,从 Date 对象返回一个月中的某一天 (1 ~ 31)
		var hours = date.getHours();          //小时 ,返回 Date 对象的小时 (0 ~ 23)
		var minutes = date.getMinutes();      //分钟 ,返回 Date 对象的分钟 (0 ~ 59)
		var seconds = date.getSeconds(); 
		//修改月份格式
			if (month >= 1 && month <= 9) {
		        month = "0" + month;
		        }
			
			//修改日期格式
			if (day >= 0 && day <= 9) {
		        day = "0" + day;
		        }
			
			//修改小时格式
			if (hours >= 0 && hours <= 9) {
		        hours = "0" + hours;
		        }
			
			//修改分钟格式
			if (minutes >= 0 && minutes <= 9) {
		        minutes = "0" + minutes;
		        }
			
			//修改秒格式
			if (seconds >= 0 && seconds <= 9) {
		        seconds = "0" + seconds;
		        }
			
			//获取当前系统时间  格式(yyyy-mm-dd hh:mm:ss)
			var currentFormatDate = year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
	  sentTime = 1
	  var theResponse = window.prompt("设置名字 按Enter键以确认","请在此输入您的姓名。");
	  var theResponse2 = window.prompt("设置分数 按Enter键以确认","请在此输入您的分数。");
      alert(theResponse + "您的得分为"+theResponse2+"分,流水号：10047"+randomStr+",提交时间："+ currentFormatDate);


	if(parseInt(str) < 10) {
		return "0" + str;
	}
	return str;
};
function setCountDown_time(){
	var idt = window.setInterval("ls();", 1000);
}
function ls() {
	sec--;
	if(sec == 0) {
		min--;
		sec = 59;
	}
	document.getElementById("countdown_time").innerHTML = "考试还有"+format(min-20) + "分" + format(sec)+"秒";
	if(parseInt(min) <= 0 && parseInt(sec) <= 1) {
		autoSubmit();
		window.clearInterval(idt);
		//alert('考试时间已到，试卷已提交，感谢您的使用！');
	}
}


$("#save_btn").bind("click", function(){
	var result_content="";
	var result_content_mid="";
	if(topicJsonArray.length==0){
		 alert("该试卷没有测试题！");
		  return ;
	}
	
  var noquestion_content="";
  for(var i=0;i<topicJsonArray.length;i++){
	  var type=topicJsonArray[i]["TYPE"];
	  var topicid=topicJsonArray[i]["TOPICID"];
	  var activename="topicid_"+topicid;
	  var result="";
	  if(type=="1"){
		  result=getRadioValue(activename)
	  }else{
		  result=getCheckBoxValue(activename)
	  }
	  if(result==""){
		  if(noquestion_content!="")noquestion_content+="、";
		  noquestion_content+=(i+1);
	  }
	  if(result_content_mid!="")result_content_mid+=",";
	  result_content_mid+="{\"orderindex\":\""+(i+1)+"\",\"topicid\":\""+topicid+"\",\"type\":\"1\",\"result\":\""+result+"\"}";
  }

  if(noquestion_content!=""){
	  var msgcontent="<div class='m10'>";
	  msgcontent+="<font style='height: 35px;line-height: 35px;font-size: 16px;color: #bf0000;'>您还有部分试题还未作答完成，请认真核对！</font>";
	  msgcontent+="<br/>";
	  msgcontent+="试题：第"+noquestion_content+"题，尚未作答";
	  msgcontent+="</div>";
	  var x1 = Math.floor((Math.random()*10))+'';
	  var x2 = Math.floor((Math.random()*10))+'';
	  var x3 = Math.floor((Math.random()*10))+'';
	  var x4 = Math.floor((Math.random()*10))+'';
	  var x5 = Math.floor((Math.random()*10))+'';
	  randomStr = x1 + x2 + x3 + x4 + x5
      // alert("试题：第"+noquestion_content+"题，尚未作答");
		var date = new Date();
		var year = date.getFullYear();        //年 ,从 Date 对象以四位数字返回年份
		var month = date.getMonth() + 1;      //月 ,从 Date 对象返回月份 (0 ~ 11) ,date.getMonth()比实际月份少 1 个月
		var day = date.getDate();             //日 ,从 Date 对象返回一个月中的某一天 (1 ~ 31)
		var hours = date.getHours();          //小时 ,返回 Date 对象的小时 (0 ~ 23)
		var minutes = date.getMinutes();      //分钟 ,返回 Date 对象的分钟 (0 ~ 59)
		var seconds = date.getSeconds(); 
		//修改月份格式
			if (month >= 1 && month <= 9) {
		        month = "0" + month;
		        }
			
			//修改日期格式
			if (day >= 0 && day <= 9) {
		        day = "0" + day;
		        }
			
			//修改小时格式
			if (hours >= 0 && hours <= 9) {
		        hours = "0" + hours;
		        }
			
			//修改分钟格式
			if (minutes >= 0 && minutes <= 9) {
		        minutes = "0" + minutes;
		        }
			
			//修改秒格式
			if (seconds >= 0 && seconds <= 9) {
		        seconds = "0" + seconds;
		        }
			
			//获取当前系统时间  格式(yyyy-mm-dd hh:mm:ss)
			var currentFormatDate = year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
	  sentTime = 1
	  var theResponse = window.prompt("设置名字","请在此输入您的姓名。");
      alert(theResponse + "您的得分为95分,流水号：10047"+randomStr+",提交时间："+ currentFormatDate);

	 return ;
  }

    autoSubmit();

});
//=============================================================================================================================================================

function exitfn(){
	var params=null;
	var url=rootPath+"/vip/login/loginAction.php?action=exit";
	$.post(url,params,function(responseText){
		      window.location.href=rootPath+"/vip/login/login.php";
	 })
}

//var issubmit=0;
function autoSubmit(){
	var result_content=getExamAnswerFn();
	var params={paperid:paperid,csmpagerid:csmpagerid,starttime:starttime,result_content:result_content,memberusercode:memberusercode,memberschoolid:memberschoolid,membernickname:membernickname,ssm:getSSM()}
	var url="examTopicAction.php?action=submit";
	//if(issubmit==1){
	//	return false;
	//}
	issubmit=1;
	$.post(url,params,function(responseText){

	//	issubmit=0;
		 var data=eval("("+responseText+")");  
			var success=data.success;                                
			if(success==0){ 
				alert(data.msg);
    	    }else if(success==1){
    	    	alert(data.msg);
    	    	//window.location.href="exam_pager.php?paperid="+paperid;
    	    	 exitfn();
    	    }else if(success==2){
    	    	alert(data.msg);
    	    	window.location.href="examination_ok.php?paperid="+paperid;	
	      	}else{
	      		alert(data.msg);
	      		
	       };   
		
		
	}); 
}


function getExamAnswerFn(){
  var result_content="";
  var result_content_mid="";
  var noquestion_content="";
  for(var i=0;i<topicJsonArray.length;i++){
	  var type=topicJsonArray[i]["TYPE"];
	  var topicid=topicJsonArray[i]["TOPICID"];
	  var activename="topicid_"+topicid;
	  var result="";
	  if(type=="1"){
		  result=getRadioValue(activename)
	  }else{
		  result=getCheckBoxValue(activename)
	  }
	  if(result_content_mid!="")result_content_mid+=",";
	  result_content_mid+="{\"orderindex\":\""+(i+1)+"\",\"topicid\":\""+topicid+"\",\"result\":\""+result+"\"}";
  }
    result_content="["+result_content_mid+"]";
    return result_content;
}
