var breed_url_done = "http://10.128.126.2:20080/download?md5=";//下载avml、pcap、dump(已完成)
var breed_url_dealing = "http://10.128.126.2:8000/";//下载和处理正在进行的样本路径
var download_report_done = "http://10.128.127.249:5000/report/breed/";//下载已经处理完的样本分析报告
var download_report_dealing = "http://10.128.127.249:5000/report/breed_run/";//下载正在分析的样本分析报告

var str_href = location.href;
var num = location.href.split('/')[5];
var order = location.href.split('/')[6];
var page = location.href.split('/')[4];
var pageCount = Number($("#page_num").text());
//设置条目数默认值
if(num==""||num==undefined){
	num=15;
	$("#select_num").val(num);
}

else
	$("#select_num").val(num);

if(order==""||order==undefined)
	order="start_down";

//修改表头样式
if(order=="hash_up"){
	$("#icon_hash").find("img").remove();
	$("#icon_hash").attr("class","fa fa-caret-up");	
}
if(order=="hash_down"){
	$("#icon_hash").find("img").remove();
	$("#icon_hash").attr("class","fa fa-caret-down");	
}
if(order=="status_down"){
	$("#icon_status").find("img").remove();
	$("#icon_status").attr("class","fa fa-caret-down");	
}
if(order=="status_up"){
	$("#icon_status").find("img").remove();
	$("#icon_status").attr("class","fa fa-caret-up");	
}
if(order=="start_down"){
	if(str_href!="http://10.255.49.38:4000/breed_track"){
		$("#icon_start").find("img").remove();
		$("#icon_start").attr("class","fa fa-caret-down");		
	}
	else
		$("#icon_start").attr("class","");
}
if(order=="start_up"){
	$("#icon_start").find("img").remove();
	$("#icon_start").attr("class","fa fa-caret-up");	
}
if(order=="cast_down"){
	$("#icon_create").find("img").remove();
	$("#icon_create").attr("class","fa fa-caret-down");	
}
if(order=="cast_up"){
	$("#icon_create").find("img").remove();
	$("#icon_create").attr("class","fa fa-caret-up");	
}
if(order=="breed_down"){
	$("#icon_breed_time").find("img").remove();
	$("#icon_breed_time").attr("class","fa fa-caret-down");	
}
if(order=="breed_up"){
	$("#icon_breed_time").find("img").remove();
	$("#icon_breed_time").attr("class","fa fa-caret-up");	
}
if(order=="name_down"){
	$("#icon_name").find("img").remove();
	$("#icon_name").attr("class","fa fa-caret-down");	
}
if(order=="name_up"){
	$("#icon_name").find("img").remove();
	$("#icon_name").attr("class","fa fa-caret-up");	
}
if(order=="size_down"){
	$("#icon_size").find("img").remove();
	$("#icon_size").attr("class","fa fa-caret-down");	
}
if(order=="size_up"){
	$("#icon_size").find("img").remove();
	$("#icon_size").attr("class","fa fa-caret-up");	
}
if(order=="type_down"){
	$("#icon_type").find("img").remove();
	$("#icon_type").attr("class","fa fa-caret-down");	
}
if(order=="type_up"){
	$("#icon_type").find("img").remove();
	$("#icon_type").attr("class","fa fa-caret-up");	
}
if(order=="person_down"){
	$("#icon_user").find("img").remove();
	$("#icon_user").attr("class","fa fa-caret-down");	
}
if(order=="person_up"){
	$("#icon_user").find("img").remove();
	$("#icon_user").attr("class","fa fa-caret-up");	
}



//选择显示条目数量
$("#select_num").on("change",function(){
	var select_num = $('#select_num option:selected').val();
	var str_len = str_href.length;
	var str_1 = str_href.substring(0,str_href.indexOf(page));
	var str_2 = str_href.substring(str_href.indexOf(num)+2,str_len);
	if(str_href=="http://10.128.127.249:10001/breed_track")
		window.location = str_href+"/1/"+select_num+"/start_down";
	else
		window.location = "http://10.128.127.249:10001/breed_track"+"/1/"+select_num+str_2
})

//下载按钮
$("td .fa-download").on("click",function(){
	var str= $(this).parent().find("option:selected").text();//获取下拉菜单中的下载项值
	var breeding_status = $(this).parent().parent().find("td:first").next().text();//获取样本的当前养殖状态
	var td_hash = $(this).parent().parent().children().first().text().trim();//获取样本hash值
	var md5 = td_hash.split(".")[0];//样本的组成结构为md5.crc32以“.”为分隔符，取“.”之前的值即为hash值
	var crc32 = td_hash.split(".")[1];//同上，取“.”之后的值即为crc32值
	var task_id = $(this).parent().next().text();//获取样本的task_id
	var task_name = $(this).parent().next().text();//获取样本的task_name
	
	if(str =="样本"){
		window.location.href = "/download/"+td_hash;//样本的下载路径是唯一的
	}

	if(str=="avml"){
		if(breeding_status=="分析中"){
			window.location.href = "/realTimeAvml/"+td_hash+"/"+task_id;//如果样本处于分析中状态，则下载实时的avml
		}else{
			window.location.href = breed_url_done+md5+"&crc32="+crc32+"&category=dynamic_avml";//如果样本是已完成或者是结束状态下载最终的avml
		}
	}

	if(str=="pcap"){
		if(breeding_status=="分析中"){
			window.location.href = breed_url_dealing+"download_pcap?task_id="+task_id+"&task_name="+task_name;//如果样本处于分析中状态，则下载实时的pcap包
		}else{
			window.location.href = breed_url_done+md5+"&crc32="+crc32+"&category=pcap";//如果样本是已完成或者是结束状态下载最终的pcap包
		}
	}

	if(str=="dump"){
		window.location.href = breed_url_done+md5+"&crc32="+crc32+"&category=dump";
	}

	if(str=="历史记录")
	{
		$.ajax({
			url:"/get_history_record/"+md5+"/"+crc32,
			type:"GET",	
			dataType:"json",
			success:function(data){
				var item = JSON.parse(data);
				var resultitem = "";
				for(var i=0;i<item.length;i++){
					resultitem += "<li style='margin-top:10px;'><span>"+item[i][0]+"</span>";
					if(item[i][0]<10)
						resultitem += "<span style='margin-left:37px'>"+item[i][2].substring(0,19)+"</span>";
					else
						resultitem += "<span style='margin-left:30px'>"+item[i][2].substring(0,19)+"</span>";
					resultitem += "<span style='margin-left:130px'>"+'<a href="'+item[i][1]+'">下载</a></span></li>';
				}
				$("#result_history").html(resultitem);
				$("#upload_history_button").trigger("click");
			}
		})
		// window.location.href = breed_url_harbin+"20080/download_history?md5="+md5+"&crc32="+crc32+"&category=dynamic_avml";
	}
})

//检索按钮
$("#breed_search_btn").on("click",function(){
	var str_select_status = $("#select_status").find("option:selected").text();
	if(str_select_status=="全部")
		str_select_status = "";
	if(str_select_status=="已完成")
		str_select_status="SUCCESS";
	if(str_select_status=="分析超时")
		str_select_status="TIMEOUT";
	if(str_select_status=="分析失败")
		str_select_status="FAILURE";
	if(str_select_status=="待分析")
		str_select_status=="PENDING";
	if(str_select_status=="取消分析")
		str_select_status="CANCELED";
	if(str_select_status=="分析中")
		str_select_status="STARTED";
	var str_input = $("#breed_search_text").val();
	if(str_select_status && str_input){
		window.location.href = "/breed_track/1/"+num+"/"+order+""+str_select_status+"/"+str_input;
	}else if(str_select_status && (!str_input)){
		window.location.href = "/breed_track/1/"+num+"/"+order+"/status/"+str_select_status
	}else if((!str_select_status) && str_input){
		window.location.href = "/breed_track/1/"+num+"/"+order+"/condition/" + str_input;
	}else{
		window.location.href = "/breed_track/1/"+num+"/"+order
	}	
})

//表头排序
$("th").on("click",function(){
	var th_str = $(this).text();
	console.log(th_str);
	var str_len = str_href.length;
	var order_len = order.length;
	var str_1 = str_href.substring(0,str_href.indexOf(order));
	var str_2 = str_href.substring(str_href.indexOf(order)+parseInt(order_len),str_len);
	if(th_str=="HASH"){
		if(str_href=="http://10.128.127.249:10001/breed_track")
			window.location.href = "/breed_track/1/15/hash_down";
		if(order=="hash_down")
			window.location.href= str_1+"hash_up"+str_2;
		if(order=="hash_up")
			window.location.href= str_1+"hash_down"+str_2;
		if(order!="hash_down"&&order!="hash_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"hash_down"+str_2;
	}
	if(th_str=="养殖状态"){
		if(str_href=="http://10.128.127.249:10001/breed_track")
			window.location.href = "/breed_track/1/15/status_down";
		if(order=="status_down")
			window.location.href= str_1+"status_up"+str_2;
		if(order=="status_up")
			window.location.href= str_1+"status_down"+str_2;
		if(order!="status_down"&&order!="status_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"status_down"+str_2;
	}
	if(th_str=="开始养殖时间"){
		if(str_href=="http://10.128.127.249:10001/breed_track"&&order=="start_down")
			window.location.href = "/breed_track/1/15/start_down";
		if(order=="start_down"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"start_up"+str_2;
		if(order=="start_up")
			window.location.href= str_1+"start_down"+str_2;
		if(order!="start_down"&&order!="start_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"start_down"+str_2;
	}
	if(th_str=="投放时间"){
		if(str_href=="http://10.128.127.249:10001/breed_track")
			window.location.href = "/breed_track/1/15/cast_down";
		if(order=="cast_down")
			window.location.href= str_1+"cast_up"+str_2;
		if(order=="cast_up")
			window.location.href= str_1+"cast_down"+str_2;
		if(order!="cast_down"&&order!="cast_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"cast_down"+str_2;
	}
	if(th_str=="养殖时间"){
		if(str_href=="http://10.128.127.249:10001/breed_track")
			window.location.href = "/breed_track/1/15/breed_down";
		if(order=="breed_down")
			window.location.href= str_1+"breed_up"+str_2;
		if(order=="breed_up")
			window.location.href= str_1+"breed_down"+str_2;
		if(order!="breed_down"&&order!="breed_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"breed_down"+str_2;
	}
	if(th_str=="原始文件名"){
		if(str_href=="http://10.128.127.249:10001/breed_track")
			window.location.href = "/breed_track/1/15/name_down";
		if(order=="name_down")
			window.location.href= str_1+"name_up"+str_2;
		if(order=="name_up")
			window.location.href= str_1+"name_down"+str_2;
		if(order!="name_down"&&order!="name_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"name_down"+str_2;
	}
	if(th_str=="文件大小"){
		if(str_href=="http://10.128.127.249:10001/breed_track")
			window.location.href = "/breed_track/1/15/size_down";
		if(order=="size_down")
			window.location.href= str_1+"size_up"+str_2;
		if(order=="size_up")
			window.location.href= str_1+"size_down"+str_2;
		if(order!="size_down"&&order!="size_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"size_down"+str_2;
	}
	if(th_str=="文件类型"){
		if(str_href=="http://10.128.127.249:10001/breed_track")
			window.location.href = "/breed_track/1/15/type_down";
		if(order=="type_down")
			window.location.href= str_1+"type_up"+str_2;
		if(order=="type_up")
			window.location.href= str_1+"type_down"+str_2;
		if(order!="type_down"&&order!="type_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"type_down"+str_2;
	}
	if(th_str=="投放人员"){
		if(str_href=="http://10.128.127.249:10001/breed_track")
			window.location.href = "/breed_track/1/15/person_down";
		if(order=="person_down")
			window.location.href= str_1+"person_up"+str_2;
		if(order=="person_up")
			window.location.href= str_1+"person_down"+str_2;
		if(order!="person_down"&&order!="person_up"&&str_href!="http://10.128.127.249:10001/breed_track")
			window.location.href= str_1+"person_down"+str_2;
	}
})