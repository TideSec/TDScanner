//点击查看报告时，会显示细节
URL_LOOKUP = "/get_unbreed_detail/";
SEARCH_INFO = "/search_info/";

// 历史查询中的路径
var download_stat_avml = "http://10.128.77.153:8081/download/";
var download_dynamic_avml = "http://10.128.126.162:20080/download?md5=";
var download_report_url = 'http://10.128.127.249:5000/report/single/';

$(".bs-callout a").on("click",function(){ 
    var self = $(this);   
	var str_md5 = self.attr("href");
    var child_nodes = self.parent().siblings(".insert-place").children(".bg-info").length;
    
	$.ajax({
		url:URL_LOOKUP + str_md5,
		post:"POST",
		success:function(data){
            data = JSON.parse(data);
            var detail_info = '';
            for(var i = 0; i < data.length; i++){
                detail_info +=  '<div class = "bg-info">'+
                                    '<p style="width:30%; float:left">最新上传时间：'+ data[i]["cast_time"] +'</p>'+
                                    '<p style="width:30%; float:left">判定结果：';
                                    if(data[i]["is_virus"]=="恶意")
                                        detail_info += '<span class="label label-default" style="background-color: rgb(255, 58, 1);">'+data[i]["is_virus"]+'</span></p>';
                                    else if(data[i]["is_virus"]=="非恶意")
                                        detail_info += '<span class="label label-default label-success">'+data[i]["is_virus"]+'</span></p>';
                                    else
                                        detail_info += '<span class="label label-default bg-gray">'+data[i]["is_virus"]+'</span></p>';
                                    detail_info += '<p style="width:40%; float:left">分析环节：'+ data[i]["analysis_steps"] +'</p>'+
                                    '<p style="width:30%; float:left">静态分析状态：'+ data[i]["static_status"] +'</p>';
                                    if(data[i]["analysis_steps"]=="预处理-多引擎扫描-静态分析")
                                        detail_info += '<p style="width:30%; float:left">动态分析状态：未经过</p>';
                                    else
                                        detail_info += '<p style="width:30%; float:left">动态分析状态：'+ data[i]["dynamic_status"] +'</p>';
                                    if(data[i]["behaviors"]=='')
                                        detail_info += '<p style="width:40%; float:left">样本行为：无</p>';
                                    else
                                        detail_info += '<p style="width:40%; float:left">样本行为：'+ data[i]["behaviors"] +'</p>';
                                    detail_info +='<p style="width:60%; float:left">下载：';
                                    if(data[i]["static_status"]=="已完成")
                                        detail_info += '<a href="'+ download_stat_avml + data[i]['md5']+"."+ data[i]['crc32'] + '.static.avml' +'"style="color:#31b0d5">静态avml</a>';
                                    else
                                        detail_info +='<a href="#" style="color:darkgray">静态avml</a>';
                                    if(data[i]["dynamic_status"]=="未完成"||data[i]["analysis_steps"]=="预处理-多引擎扫描-静态分析")
                                        detail_info += '<a href="#" style="margin-left: 30px;color:darkgray">动态avml</a>';
                                    else
                                        detail_info += '<a href="'+download_dynamic_avml+ data[i]['md5'] + "&crc32="+ data[i]['crc32'] +"&category=dynamic_avml" +'" style="margin-left: 30px;color:#31b0d5">动态avml</a>';
                                    if(data[i]["static_status"]=="已完成")
                                        detail_info += '<a href="'+ download_report_url + data[i]['md5']+"."+ data[i]['crc32'] +'" style="margin-left: 30px;color:#31b0d5">分析报告</a>';
                                    else
                                        detail_info += '<a href="#" style="margin-left: 30px;color:darkgray">分析报告</a>';
                                    detail_info += '</p>'+
                                '</div>';
            };

            if(child_nodes==0){
                self.parent().siblings(".insert-place").append(detail_info);
                self.find("i").attr("class","fa fa-caret-up");
            }
            else{
                self.parent().siblings(".insert-place").children("div").remove();
                self.find("i").attr("class","fa fa-caret-down");
            }
		}
	});
});


$("#searchBtn").on("click",function(){
    var str_input = $("#search_info").val();
    if(str_input)
        window.location.href = "/history_record/1/8/"+str_input;
    else
        window.location.href = "/history_record/1/8";   
})
