
 
 /**
 **清除查询条件
 */
function clean(){
	$("#docTitle").val("")
	$("#docCode").val("")
	$("#startDate").val("")
	$("#endDate").val("")
	$("#docType").val("")
	$("#provinceCode").val("")
	$("#provinceNames").val("");
	$(".special_select").text("");
	
  }
/**
 * getList
 */
  function query(){
	 var frm  =  document.getElementById("listForm"); 
     frm.action = "/MSS-PORTAL/announcementjoin/list.do?provinceJT=JT";
     frm.submit();
  }
/**
 * 信息查看
 */
   function view(id,categroyFlag,encryCode){//根据资源类别打开不同的窗口
	  var url="/MSS-PORTAL/account/viewad.do?category="+categroyFlag+"&id="+id+"&encryCode="+encryCode;
	  var strFeature = 'left=0,top=0,width='+ (screen.availWidth - 10) +',height='+ (screen.availHeight-50) +',scrollbars,resizable=yes,toolbar=no';	  
	  var handle = window.open(url,"newWin",strFeature);
  }
