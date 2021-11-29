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
/*
gridload({id:'content',single:true});
id为table id在一个页面上不能重复
single为是否单选，true为单选false为多选
*/
function gridload(gridobj){
	var tableid=gridobj.id;
	var single=gridobj.single;
	if(tableid==undefined)return false;
	if(single==undefined)single=false;	
	var bgColor="#F2FDDF";
	$("tr").mouseover(function(){
	  $(this).addClass("mouse_over");
	})
	$("tr").mouseout(function(){
	  $(this).removeClass("mouse_over");
	})
	
	var checklist = $("#"+gridobj.id+" input[type='checkbox']");
	var thcheckbox = $("tr th input[type='checkbox']");
	thcheckbox.click(function(){//有全选按钮的情况下
		var ischecked = $(this).attr("checked");
		if(ischecked=="checked"){
			checklist.each(function(i){
					$(this).parent().parent().attr("backgroundColor",bgColor);
					$(this).parent().parent().css("backgroundColor",bgColor);
					$(this).attr("checked",true);
			});
		}else{
			checklist.each(function(i){
					$(this).parent().parent().attr("backgroundColor","");
					$(this).parent().parent().css("backgroundColor","");
					$(this).attr("checked",false);
			});
		}
	});
	var table_tr_obj=$("#"+gridobj.id+"  tr");
	if(checklist.length==0){//无复选框情况下
			table_tr_obj.click(function(){
				table_tr_obj.each(function(i){	
					var bg = $(this).attr("backgroundColor");	
					if(bg==bgColor)$(this).css("backgroundColor","");
				});
				var backgroundColor = $(this).attr("backgroundColor");
				if(backgroundColor==undefined||backgroundColor==bgColor){
					$(this).attr("backgroundColor",bgColor);
					$(this).css("backgroundColor",bgColor);
				}else{
					$(this).css("backgroundColor","");
				}
		});
	}else{//有复选框情况下
		table_tr_obj.click(function(){		
				var obj = $(this).find("input[type='checkbox']");
				var c = $("#"+gridobj.id+"  :checked");
				if(single){// true 代表单选
					c.attr("checked",false);
					$(c).parent().parent().css("backgroundColor","");
				}
				
				if(obj.attr("checked")=="checked"){
					obj.attr("checked",false);
					$(this).css("backgroundColor","");
				}else{
					obj.attr("checked",true);
					$(this).css("backgroundColor",bgColor);
				}
			});
		$("#"+gridobj.id+" input[type='checkbox']").click(function(){		
				var obj = $(this);
				var row = $(this).parent().parent();
				if(obj.attr("checked")=="checked"){
					obj.attr("checked",false);
					row.css("backgroundColor","");
				}else{
					obj.attr("checked",true);
					row.css("backgroundColor",bgColor);
				}			 
			});
	}
}	
//分页
function gridpage(grid){
	 var url=grid.url;//请求url
	 var single=grid.single;//是否单选 
	 if(single==null)single=false;
	 var param=grid.param;//传递参数
	 var list_div=grid.bodyid;//数据ID
	 var nav_div=grid.pagenavid;//分页导航ID
	 var showType=grid.showType;//分页类型
	 if(showType==null)showType=3;
	 var length=grid.length;//每页记录数
	 if(length==null)length=10;
	 var currentPage=1;
	 var params = {};
	
	if(param==null ||param==undefined){
		param = {};
	}else{
	 if(param!=""){
		var str = param.split("&");
		for(var i=0;i<str.length;i++){
			if(str[i]==undefined){continue;}
			var p = str[i].split("=");
			var str1 = "params."+p[0]+"='"+p[1]+"'";
			eval(str1);
		}
		}
	}
	 params.start=0;
	 params.length=length;
	 params.ts=(new Date()).getTime();
        $("#"+list_div).empty().append("<div style='width:100%;z-index:20;text-align:center;margin-top:15px;'>数据正在加载中</div>");
        $.post(url,params,function(responseText){
		     var json=eval("("+responseText+")"); 
			var total=json.totalProperty; //总记录数
            $("#"+list_div).empty().append(grid.store(json));
             if(grid.afterload!=null)grid.afterload();
            gridload({id:list_div,single:single}); 
			if(total==0){
				$("#"+nav_div).empty();
			}else{
				$("#"+nav_div).mypagination(total,{perPage:length,showType:showType,callback:function(posPage){
					$("#"+list_div).empty().append("<div style='width:100%;z-index:20;text-align:center;margin-top:15px;'>数据正在加载中</div>");
					      params.start=(posPage-1)*length;
						  $.post(url,params,function(responseText){
						   var json=eval("("+responseText+")");
						  $("#"+list_div).empty().append(grid.store(json));
						  gridload({id:list_div,single:single});
						
						});	
					}
				});
			}
		});	
}
$.fn.mypagination = function(totalProperty,opts){
	opts = $.extend({
		perPage:0, 
		callback:function(){
		}
	},opts||{});
		
	return this.each(function(){
		function numPages(){
			return Math.ceil(totalProperty/opts.perPage);
		}
		
		function selectPage(page){
			return function(){
				currPage = page;
				if (page<0) currPage = 0;
				if (page>=numPages()) currPage = numPages()-1;
				eval("render"+opts.showType+"();");
				opts.callback(currPage+1);
				document.documentElement.scrollTop = document.body.scrollTop =0;
			}
		}
		function render1_bak(){
		    
			var html= '' ;
			html+='';
			if(currPage > 0){
				html+='<a href="javascript:void(0);" class="page-first">[首页]</a>';
				html+='<a href="javascript:void(0);" class="page-prev">[上页]</a>';
			}else{
				html+='<span class="page-first">[首页]</span></td>';
				html+='<span class="page-prev">[上页]</span></td>';
			}
			if (currPage < numPages()-1){
				html+='<a href="javascript:void(0);" class="page-next">[下页]</a>';
				html+='<a href="javascript:void(0);" class="page-last">[尾页]</a>';
			}else{
				html+='<span class="page-next">[下页]</span></td>';
				html+='<span class="page-next">[尾页]</span></td>';
			}
			html+='第<input type="text" style="text-align: center;width:20px;" class="page-num">页/共'+numPages()+'页';
			html+='<span style="padding-left:10px;">共'+totalProperty+'条记录</span>';
			html+='';
			
			panel.empty();
			panel.append(html);
			$(".page-first",panel).bind('click',selectPage(0));
			$(".page-prev",panel).bind('click',selectPage(currPage-1));	
			$(".page-next",panel).bind('click',selectPage(currPage+1));	
			$(".page-last",panel).bind('click',selectPage(numPages()-1));
			$('input.page-num',panel).val(currPage+1).keydown(function(event){
                       if(event.keyCode==13){
						selectPage($(this).val()-1)();
					}
				});
		}
		function render1(){
		    
			var html= '' ;
			html+='<ul class="pager">';
			if(currPage > 0){
				html+='<li> <a href="javascript:void(0);" class="page-first">第一页</a></li>';
				html+='<li> <a href="javascript:void(0);" class="page-prev">上一页</a></li>';
			}else{
				html+='<li> <a class="page-first">第一页</a></li>';
				html+='<li> <a class="page-prev">上一页</a></li>';
			}
			if (currPage < numPages()-1){
				html+='<li> <a href="javascript:void(0);" class="page-next">下一页</a></li>';
				html+='<li> <a href="javascript:void(0);" class="page-last">最后页</a></li>';
			}else{
				html+='<li> <a class="page-next">下一页</a></li>';
				html+='<li> <a class="page-next">最后页</a></li>';
			}
			html+=' 第<input type="text" style="text-align: center;width:30px;height:20px;padding:0px;" class="page-num">页/共'+numPages()+'页';
			html+=' <span style="padding-left:10px;">共'+totalProperty+'条记录</span>';
			html+='</ul>';
			
			panel.empty();
			panel.append(html);
			$(".page-first",panel).bind('click',selectPage(0));
			$(".page-prev",panel).bind('click',selectPage(currPage-1));	
			$(".page-next",panel).bind('click',selectPage(currPage+1));	
			$(".page-last",panel).bind('click',selectPage(numPages()-1));
			$('input.page-num',panel).val(currPage+1).keydown(function(event){
                       if(event.keyCode==13){
						selectPage($(this).val()-1)();
					}
				});
		}
		function render2(){
			var html=''; 
			    html+='<div class="paginition">' ;
			if(currPage > 0){
				html+=' <a class="page-first" href="javascript:void(0);" style="margin:2px;padding:5px;border: 1px solid #ff6600;">第一页</a> ';
				html+=' <a class="page-prev" href="javascript:void(0);" style="margin:2px;padding:5px;border: 1px solid #ff6600;">上一页</a>';
			}else{
				html+='<span class="page-first" style="margin:2px;padding:5px;border: 1px solid #ff6600;">第一页</span> ';
				html+='<span class="page-prev" style="margin:2px;padding:5px;border: 1px solid #ff6600;">上一页</span>';
			}
			if (currPage < numPages()-1){
				html+=' <a class="page-next" href="javascript:void(0);" style="margin:2px;padding:5px;border: 1px solid #ff6600;">下一页</a> ';
				html+='<a class="page-last" href="javascript:void(0);" style="margin:2px;padding:5px;border: 1px solid #ff6600;">最后页</a>';
			}else{
				html=html+'<span class="page-next" style="margin:2px;padding:5px;border: 1px solid #ff6600;">下一页</span>';
				html+='<span class="page-last" style="margin:2px;padding:5px;border: 1px solid #ff6600;">最后页</span>';
			}
			html+='共<span class="cf00">'+numPages()+'</span>页 第<span class="cf00">'+(currPage+1)+'</span>页 ';
			html+='</div>';
			panel.empty();
			panel.append(html);
			if(numPages()!=1){
				if(currPage!=0 && currPage==(numPages()-1)){
					$(".page-first",panel).bind('click',selectPage(0));	
					$(".page-prev",panel).bind('click',selectPage(currPage-1));	
				}else if(currPage==0 && currPage!=(numPages()-1)){
					$(".page-next",panel).bind('click',selectPage(currPage+1));	
					$(".page-last",panel).bind('click',selectPage(numPages()-1));
				}else{
					$(".page-first",panel).bind('click',selectPage(0));	
					$(".page-prev",panel).bind('click',selectPage(currPage-1));
					$(".page-next",panel).bind('click',selectPage(currPage+1));	
					$(".page-last",panel).bind('click',selectPage(numPages()-1));
				}
			}
		}
		function render3(){
			var html= '<ul class=pageb>' ;
			html+='';
			var totalPage=numPages();
			 var startPoint = 1;
             var endPoint = 9;
			 if (currPage > 4) {
            startPoint = currPage - 4;
            endPoint = currPage + 4;
        }
        if (endPoint > totalPage) {
            startPoint = totalPage - 8;
            endPoint = totalPage;
        }
        if (startPoint < 1) {
            startPoint = 1;
        }
		for (var i = startPoint; i <= endPoint; i++) {
			if(currPage==(i-1))html += '<li class="page-number-'+i+' page_point_current">'+i+'</li> ';
			if(currPage!=(i-1))html += '<li class="page-number-'+i+' page_point">'+i+'</li> ';
		
		}	
			
			
		    html+='<li style="padding-top:5px;">第</li>';
		    html+='<li><input class="page-num"/></li>';
		    html+='<li><input class="page-num-button" type="button" value="确定"/></li>';
			html+='<li style="padding-top:5px;">页/共'+numPages()+'页</li>';
			html+='<li style="padding-left:10px;padding-top:5px;">共'+totalProperty+'条记录</li>';
			html+='</ul>';
			panel.empty();
			panel.append(html);
			$('input.page-num',panel).val(currPage+1).keydown(function(event){
                       if(event.keyCode==13){
						selectPage($(this).val()-1)();
					}
				});
			for(var i=1;i<=totalPage;i++){
			    $(".page-number-"+i,panel).bind('click',selectPage(i-1));
			}
	     $(".page-num-button",panel).bind('click',function(){
	       selectPage($(".page-num").val()-1)();
	     
	     });	 
		}
		
		var currPage = 0;
		var panel = $(this);
		eval("render"+opts.showType+"();");
 
	});
}