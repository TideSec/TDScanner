var CHECK_URL = "/check_upload";//
var UNBREED_UPLOAD_URL = "/upload_unbreed"
var BREED_UPLOAD_URL = "/upload_breed/"

//静态avml
var download_stat_avml = "http://10.128.77.153:8081/download/";
//分析报告
var download_report = "http://10.128.127.249:5000/report/single/";
//动态avml
var download_dyna_avml ="http://10.128.126.162:20080/download?md5=";
//文件数组
var PENDING_FILES  = [];

//倒计时
var second = 5;
//用来记录跳转链接
var href = "";
//记录投放路径，以确定跳转链接
var method = "";

//用于还原dropbox内的样式
var str_dropbox = '<div class="drop-img">'+
            '<span class="fa fa-upload">'+
            '</span>'+
          '</div>'+
          '<div class="drop-text">'+
            '<span>请选择需要投放的样本文件，可以按住ctrl键，或者shift键</span><br>'+
            '<span>选择多个样本进行批量上传。</span>'+
        '</div>';
//文件格式识别正则表达式(用于验证)
var reg_type= new RegExp("^(exe|dll|drv|vxd|sys|ocx|vbx|bin|elf|rpm|xpi|zip|jar|"+
    "rar|tgz|gz|bz2|arj|7z|cab|doc|docx|xls|xlsx|dot|ppt|pptx|xla|ppa|pps|pot|msi|sdw|wps|txt|pdf|rtf)$")

function handleFiles(files) {
    // 增加文件到PENDING_FILES
    for (var i = 0, ie = files.length; i < ie; i++) {
        PENDING_FILES.push(files[i]);
    }
}

// 主函数入口
$(document).ready(function() {
    
    $("#select-file").on("click", function(e){
        e.preventDefault();
        $("#file-picker").trigger("click");
    });

    // file input点击时操作
    $("#file-picker").on("change", function(e){
        var filename_str='';//用来保存dropbox中的内容
        $(".drop-img").remove();//删除已有图标
        $(".drop-text").remove();
        if($("#dropbox").text()=="您还没有选择需要上传的样本文件，请选择文件！")
            $("#dropbox").text("");
        var filelength = $("#dropbox").find("li").length;//当前已经选择的样本个数
        var filename = $("#dropbox").find("li").text();//获得当前已选择的样本名称
        var files = [];//用来保存最终上传的文件
        var length = filelength + this.files.length;
        //判断样本总数是否超过50个
        if(length >50)
            alert("单批样本上传个数不得超过50个,当前已选择"+filelength+"个样本。");
        else if(this.files!=null){
            filename_str = $("#dropbox").html();//获取现有dropbox下的html
            for(var i = 0;i<this.files.length;i++){
                var str_1 = this.files[i].name;//当前所选对比样本的名称
                var ext = str_1.substring(str_1.lastIndexOf(".")+1,str_1.length).toLowerCase();//获取文件后缀
                
                if(str_1.lastIndexOf(".")<0){
                    if(this.files[i].size>10*1024*1024){
                        alert("所选样本中有文件过大，文件名为"+this.files[i].name+"。请重新选择或者删除该样本。");
                        if($("#dropbox").html().trim()=="")
                            $("#dropbox").html(str_dropbox);
                        return;
                    }
                    else if(filename.indexOf(str_1)==-1){//如果当前所对比样本在当前已选择样本中不存在
                        files.push(this.files[i]);
                        filename_str+="<li>"+this.files[i].name+
                        "<button type='button' class='close-btn' onclick='deletefilename(this)'> ×</button></li><br>";
                    }
                    else{
                        if($("#dropbox").html().trim()=="")
                            $("#dropbox").html(str_dropbox);
                        alert("所选文件中有已选择文件，请重新选择！");
                        $("#file-picker").val("");
                        return;
                    }
                }
                else if(ext.length!=8){
                    if(this.files[i].size>10*1024*1024){
                        alert("所选样本中有文件过大，文件名为"+this.files[i].name+"。请重新选择或者删除该样本。");
                        if($("#dropbox").html().trim()=="")
                            $("#dropbox").html(str_dropbox);
                        return;
                    }
                    else if(!reg_type.test(ext)){
                        alert("所选样本文件格式有误。支持的文件类型为可执行文件（如：*.exe）、办公文档格式文件（如：*.doc）、富文本格式组（如：*.pdf）和压缩文件格式组（如：*.rar）。")
                        if($("#dropbox").html().trim()=="")
                            $("#dropbox").html(str_dropbox);
                        return;
                    }
                    else if(filename.indexOf(str_1)==-1){//如果当前所对比样本在当前已选择样本中不存在
                        files.push(this.files[i]);
                        filename_str+="<li>"+this.files[i].name+
                        "<button type='button' class='close-btn' onclick='deletefilename(this)'> ×</button></li><br>";
                    }
                    else{
                        alert("所选文件中有已选择文件，请重新选择！");
                        if($("#dropbox").html().trim()=="")
                            $("#dropbox").html(str_dropbox);
                        $("#file-picker").val("");
                        return;
                    }
                }
                else{
                    if(this.files[i].size>10*1024*1024){
                        alert("所选样本中有文件过大，文件名为"+this.files[i].name+"。请重新选择或者删除该样本。");
                        if($("#dropbox").html().trim()=="")
                            $("#dropbox").html(str_dropbox);
                        return;
                    }
                    else if(filename.indexOf(str_1)==-1){//如果当前所对比样本在当前已选择样本中不存在
                        files.push(this.files[i]);
                        filename_str+="<li>"+this.files[i].name+
                        "<button type='button' class='close-btn' onclick='deletefilename(this)'> ×</button></li><br>";
                    }
                    else{
                        alert("所选文件中有已选择文件，请重新选择！");
                        if($("#dropbox").html().trim()=="")
                            $("#dropbox").html(str_dropbox);
                        $("#file-picker").val("");
                        return;
                    }
                }
            }  
        }

        handleFiles(files);//将文件添加到总的文件数组中
        this.files=[];//清空文件缓冲数组
        $("#dropbox").html(filename_str);
        $("#file-picker").val("");
    });

    // 上传
    $("#checkBtn").on("click", function(e) {
        e.preventDefault();
        doCheck();

    });
    // 投放
    $("#uploadBtn").on("click", function(e){
        e.preventDefault();  
        doUpload();
    });

});

//删除文件
function deletefilename(para){
    var i = $(para).parent().prevAll("li").length;
    PENDING_FILES.splice(i,1);//将其从总文件数组中删除
    $(para).parent().next("br").remove();
    $(para).parent().remove();
    if($("#dropbox").html().trim()=="")
        $("#dropbox").html(str_dropbox);
}

$("#radio_dynamic_analysis").on("click",function(){
    if($(this).attr("checked")=="checked"){
        $(this).removeAttr("checked");
    }
    else{
        $("#radio_sample_breeding").removeAttr("checked");
        $("#input_breeding_time").attr("disabled","disabled");
        $(this).attr("checked","checked");

    }
})
$("#radio_sample_breeding").on("click",function(){
    if($(this).attr("checked")=="checked"){
        $(this).removeAttr("checked");
        $("#input_breeding_time").attr("disabled","disabled");
    }
    else{
        $("#radio_dynamic_analysis").removeAttr("checked");
        $(this).attr("checked","checked");
        $("#input_breeding_time").removeAttr("disabled");
    }
})

// 预处理操作
function doCheck() {
    //上传时不许操作 
    // 创建表单，相当于前台的form标签
    fd = collectFormData();
    // 文件传入表单
    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
            fd.append("file", PENDING_FILES[i]); 
    }

    // 检查时，没有上传文件时，点击后提醒
    if (PENDING_FILES.length==0) {
        $("#dropbox").text("您还没有选择需要上传的样本文件，请选择文件！");
        return;
    }

    else{
        $("#loading_button").trigger("click");
        //后台请求
        fd.append("__ajax", "true");

        var xhr = $.ajax({
            url: CHECK_URL,
            method: "POST",
            contentType: false,
            processData: false,
            cache: false,
            data: fd,
            success: function(data) {
                $("#myModal_loading button").trigger("click");

                items = JSON.parse(data); 
                var sum_upload = items.length; //the sum of upload file
                var fail_upload = 0; //the count of file  failed upload
                for(var i = 0;i < sum_upload; i++ ){
                    if(items[i]["flag"] = "f"){
                        fail_upload++;

                    }
                }
                $("#upload_form").css("display","none");
                $(".modal-backdrop").removeClass();
                $(".modal-open").removeClass();
                $("h1").text("样本处理结果");
                $("h1").removeAttr("style");
                var html_text = '<span style="width: 1150px;  margin: auto; line-height: 40px;">预处理完成，上传了' + sum_upload + '个样本。'
                    html_text += '您可以点击“批量投放”将样本进行批量投放操作，并可以设置其投放环节。</span>';
                $("#btn_upload").hide();
                $(".describe").html(html_text);
                $(".separator").css("display","block");

                for(var i = 0; i < items.length; i++){
                    var insertItem = '';
                    insertItem ='<tr>'+
                                     '<td class="td-hash tooltip-test" data-toggle="tooltip" title="'+items[i]["file_feature"]["name"]+'">'+ items[i]["file_feature"]["name"] +'</td>'+
                                     '<td class="td-hash tooltip-test" data-toggle="tooltip" title="'+items[i]["file_feature"]["type"]+'">'+ items[i]["file_feature"]["type"] +'</td>'+
                                     '<td>'+ items[i]["file_feature"]["size"] +'</td>';
                    if(parseInt(items[i]["total"])>0){
                        insertItem += '<td> <a style="color:#337ab7" data-toggle="collapse" href="#'+ items[i]["file_feature"]["md5"] +'" ia-expanded="false" aria-controls="'+ items[i]["total"]["md5"] +'">已分析</a></td>';
                    }else{
                        insertItem += '<td>未分析</td>';
                    }                
                    insertItem +=   '<td>'+ items[i]["total"] +'</td>'+
                                    '<td class="td-hash tooltip-test" data-toggle="tooltip" title="'+items[i]["file_feature"]["md5"]+'">'+ items[i]["file_feature"]["md5"] +'</td>'+
                                    '<td class="td-hash tooltip-test" data-toggle="tooltip" title="'+items[i]["file_feature"]["sha1"]+'">'+ items[i]["file_feature"]["sha1"] +'</td>'+
                                '</tr>';
                    
                    if(parseInt(items[i]["total"]) > 0){
                        insertItem += '<tr id="'+ items[i]["file_feature"]["md5"] +'" class="collapse"  style="width:1289px;margin:-1px auto;border-right:1px solid #ddd">'+
                                            '<td colspan="7" style="padding:0px">';
                        for(var j = 0; j < items[i]["total"]; j++){
                            var item = items[i]["details"][j];
                            if(item["sign"]=="unbreed"){
                                insertItem +=  '<div style="background-color:#d9edf7;height:125px" >'+
                                                '<div style="height:40px;margin-top:10px;width:1288px">'+
                                                    '<span style="width:390px;margin-top:10px;margin-left:40px;float:left;text-align:left" >最新上传时间：'+ item["cast_time"] +'</span>'+
                                                '</div>'+
                                                '<div style="height:30px">'+
                                                    '<span style="width:390px;margin-left:40px;float:left;text-align:left">分析类型：常规分析</span>'+
                                                    '<span style="width:485px;float:left;text-align:left" >HASH：'+items[i]["file_feature"]["md5"] +'.'+ items[i]["file_feature"]["crc"]+'</span>'+
                                                    '<span style="width:300px;float:left;text-align:left">判定结果：'+item["is_virus"]+'</span>'+ 
                                                '</div>'+
                                                '<div style="height:30px">'+
                                                    '<span style="width:390px;margin-left:40px;margin-left:40px;float:left;text-align:left">分析环节：'+ item["analysis_steps"] +'</span>'+
                                                    '<span style="width:485px;float:left;text-align:left">静态分析状态：'+ item["static_status"]+'</span>'
                                                    if(item["analysis_steps"]=="预处理-多引擎扫描-静态分析"){
                                                        insertItem += '<span style="width:300px;float:left;text-align:left">动态分析状态：未经过'
                                                    }
                                                    else{
                                                        insertItem += '<span style="width:300px;float:left;text-align:left">动态分析状态：'+ item["dynamic_status"] +'</span>'
                                                    }
                                                insertItem += '</div>'+
                                                '<div style="height:30px">';
                                                if(item["behaviors"]=='')
                                                    insertItem += '<span style="width:390px;margin-left:40px;float:left;text-align:left">样本行为：无</span>';
                                                else
                                                    insertItem += '<span style="width:390px;margin-left:40px;float:left;text-align:left">样本行为：'+ item["behaviors"] +'</span>';
                                                    insertItem += '<span style="width:850px;text-align:left;float:left">下载：';
                                                        // 给静态avml加链接
                                                        if(item["static_status"] == "已完成"){
                                                            insertItem += '<a href="'+ download_stat_avml + items[i]["file_feature"]["md5"] +'.' + items[i]["file_feature"]["crc"]+".static.avml"+'" style="margin-left: 10px;color: #31b0d5">静态avml</a>';
                                                        }else{
                                                            insertItem += '<a href="#" style="margin-left: 10px; color: darkgray" disabled="disabled "onclick="">静态avml</a>';                                                   
                                                        }
                                                        
                                                        // 给动态avml文件加链接
                                                        if(item["dynamic_status"] == "已完成"){
                                                            insertItem += '<a href="'+download_dyna_avml + items[i]["file_feature"]["md5"] + "&crc32="+items[i]["file_feature"]["crc"]+"&category=dynamic_avml"+'"style="margin-left: 80px;color: #31b0d5">动态avml</a>';
                                                        } else if(item["dynamic_status"] == "未完成"||item["analysis_steps"]=="预处理-多引擎扫描-静态分析"){
                                                            insertItem += '<a href="#" style="margin-left: 80px;color:darkgray">动态avml</a>';
                                                        }  

                                                        // 给报告加链接
                                                        if(item["static_status"] == "已完成")                                                      
                                                            insertItem += '<a href="'+download_report + items[i]["file_feature"]["md5"] +'.' + items[i]["file_feature"]["crc"]  +'" style="margin-left: 80px;color: #31b0d5">分析报告</a>';
                                                        else
                                                            insertItem += '<a href="#" style="margin-left: 80px;color: darkgray">分析报告</a>';

                                        insertItem +='</span>'+
                                                '</div>'+
                                            '</div>';
                            }
                            if(item["sign"]=="breed"){
                                insertItem +=  '<div style="background-color:#d9edf7;height:125px" >'+
                                                '<div style="height:40px;margin-top:10px;width:1288px">'+
                                                    '<span style="width:390px;margin-left:40px;margin-top:10px;float:left;text-align:left" >最新上传时间：'+ item["cast_time"] +'</span>'+
                                                '</div>'+
                                                '<div style="height:30px">'+
                                                    '<span style="width:390px;margin-left:40px;float:left;text-align:left">分析类型：养殖分析</span>'+
                                                    '<span style="width:485px;float:left;text-align:left" >HASH：'+items[i]["file_feature"]["md5"] +'.'+ items[i]["file_feature"]["crc"]+'</span>'+
                                                '</div>'+
                                                '<div style="height:30px">'+
                                                    '<span style="width:390px;margin-left:40px;margin-left:40px;float:left;text-align:left">分析环节：'+ item["analysis_steps"] +'</span>'+
                                                    '<span style="width:485px;float:left;text-align:left">静态分析状态：'+ item["static_status"]+'</span>'+
                                                    '<span style="width:300px;float:left;text-align:left">养殖分析状态：'+ item["breed_status"] +'</span>'+
                                                '</div>'+
                                                '<div style="height:30px">'+
                                                    '<span style="width:1240px;margin-left:40px;text-align:left;float:left">下载：';
                                                        
                                                        if(item["breed_status"] == "正在分析")
                                                            insertItem += '<a href="'+"/realTimeAvml/" + items[i]["file_feature"]["md5"] +'.' + items[i]["file_feature"]["crc"]+item["task_id"]+'" style="margin-left: 10px;color: #31b0d5">avml</a>';
                                                        else if(item["breed_status"] == "分析完成")
                                                            insertItem += '<a href="'+ download_dyna_avml +items[i]["file_feature"]["md5"] + "&crc32="+items[i]["file_feature"]["crc"]+"&category=dynamic_avml"+'" style="margin-left: 10px;color: #31b0d5">avml</a>';
                                                        else
                                                            insertItem += '<a href="#" style="margin-left: 10px; color: darkgray" disabled="disabled "onclick="">avml</a>';                                                   
                                                          

                                                        // 给报告加链接 
                                                        if(item["breed_status"] == "分析完成"){                                                        
                                                            insertItem += '<a href="http://10.128.127.249:5000/report/breed/'+items[i]["file_feature"]["md5"] +'.' + items[i]["file_feature"]["crc"]+ '/' + item["task_id"] +'/' + items[i]["file_feature"]["md5"] +'.' + items[i]["file_feature"]["crc"]  +'" style="margin-left: 80px;color: #31b0d5">分析报告</a>';
                                                        }
                                                        else if(item["breed_status"] == "正在分析"){
                                                            insertItem += '<a href="http://10.128.127.249:5000/report/breed_run/'+items[i]["file_feature"]["md5"] +'.' + items[i]["file_feature"]["crc"] +'" style="margin-left: 80px;color: #31b0d5">分析报告</a>';
                                                        }else{
                                                            insertItem += '<a href="#" style="margin-left: 80px;color: darkgray">分析报告</a>';                                                    
                                                        }
                                                        insertItem +='</span>'+
                                                                '</div>'+
                                                            '</div>';
                            }                            
                        }

                        insertItem +=        '</td>'+
                                      '</tr>';
                        insertItem += '<footer style="margin-bottom:100px"></footer>'
                    }
                   
                    $("#result_table > tbody").append(insertItem);
                }                          
            }
        });
    }
}

// 确认投放操作
function doUpload() {
    // 二次检查，当没有要上传的文件存在时，可做以下处理
    if(!fd["file"]){
        //alert("没有文件上传，请回到样本投放重新选择文件")
    }

    method = $("#upload_method input").filter(":checked").next().text();
    var upload_method_url;

    var table_1= $("#result_table");
    if(window.person_info.person_id=="")
        fd.append("person_id","无")
    else
        fd.append("person_id",window.person_info.person_id);
    fd.append('username',window.person_info.name);
    // fd.append("person_id",1);
    // fd.append("username","username");

    // 选择哪种方式上传你定    
    if(method == "动态分析"){
        fd.append("MISSION", "MISSION");     
        upload_method_url = UNBREED_UPLOAD_URL;        
    }else if(method == "长期养殖"){
        var breed_cast_time_setting = $("#input_breeding_time").val();
        var BREED_UPLOAD_URL = "/upload_breed/";
        if(breed_cast_time_setting){
            upload_method_url =BREED_UPLOAD_URL + breed_cast_time_setting;
        }else{
            upload_method_url =BREED_UPLOAD_URL + '20';
        }        
    }else{
        upload_method_url = UNBREED_UPLOAD_URL;
    }   
    //样本投放
    var xhr = $.ajax({        
        url: upload_method_url,
        method: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: fd,
        success: function(data) {
            var data = JSON.parse(data);
            var result_success = "";
            var result_fail = "";
            if(!data["success"])
                result_success="<li style='list-style:none'>无</li>";
            else{
                for(var i=0;i<data["success"].length;i++)
                    result_success += "<li style='list-style:none'>"+data["success"][i]+"</li>";
            }
            if(!data["upload_fail"])
                result_fail = "<li style='list-style:none'>无</li>";
            else{
                for(var i=0;i<data["upload_fail"].length;i++)
                    result_fail += "<li style='list-style:none'>"+data["upload_fail"][i]+"</li>";
            }
            $("#result_success").html(result_success);
            $("#result_fail").html(result_fail);
            $("#upload_result_button").trigger("click");

            if(method=="")
                method="静态分析";
            if(method=="长期养殖")
                href="http://10.128.127.249:10001/breed_track";
            else
                href="http://10.128.127.249:10001/history_record";
            //倒计时跳转

            setInterval(function(){
                $("#str_href").html("您选择的投放路径为"+'"'+method+'"，'+second+"秒后将自动跳转到相应模块"+"<a href='"+href+"'>点击跳转</a>");
                if(second==0){
                    window.location.href = href;
                }else
                    second--;
            },1000);
        },
        error: function(data){
            // alert("请打开172段VPN！")
        }
    });
}

// 设置表单
function collectFormData() {
    // 收集前台表单信息
    var fd = new FormData();

    $("#upload_form :input").each(function() {
        var $this = $(this);
        var name  = $this.attr("name");
        var type  = $this.attr("type") || "";
        var value = $this.val();
        //没有文件名则直接返回
        if (name === undefined) {
            return;
        }

        // 如果是文件表单，则跳过
        if (type === "file") {
            return;
        }       

    });

    return fd;
}
