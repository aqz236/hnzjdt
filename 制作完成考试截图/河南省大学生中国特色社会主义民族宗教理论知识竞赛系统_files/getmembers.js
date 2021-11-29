function getMemberInfoJson(usercodelist){
var ds=null;
var params={usercodelist:usercodelist}
var url=rootPath+"/com/common/csmMemberAction.php?action=getMemberInfoJson";
    jQuery.ajax({url:url,
			type:'post',
			async: false,      //ajax同步
			dataType:"html",
			data:params,//URL参数
			success:function(responseText){
				ds=eval("("+responseText+")");         
			},
			error:function(){}
			});
return ds;
}
function getMember(MemberInfoJson,usercode){
 var memberObj=null;
	if(MemberInfoJson!=null){
		for(var i=0; i<MemberInfoJson.length; i++){
		    if(MemberInfoJson[i].USERCODE==usercode){
		    	memberObj=MemberInfoJson[i];
		    	break;
		    }
		  }
	}
	return memberObj
}
function getMemberUseraccount(MemberInfoJson,usercode){
 var useraccount="";
	if(MemberInfoJson!=null){
		for(var i=0; i<MemberInfoJson.length; i++){
		    if(MemberInfoJson[i].USERCODE==usercode){
		    	useraccount=MemberInfoJson[i].useraccount;
		    	break;
		    }
		  }
	}
	return useraccount
}

function getMemberNickname(MemberInfoJson,usercode){
 var nickname="";
	if(MemberInfoJson!=null){
		for(var i=0; i<MemberInfoJson.length; i++){
		    if(MemberInfoJson[i].USERCODE==usercode){
		    	nickname=MemberInfoJson[i].nickname;
		    	break;
		    }
		  }
	}
	return nickname;
}



