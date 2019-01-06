$(function() {
	$.ajax({
		type : "POST",
		url :window.sso+'/permission/valadate_session/',
		data : {
			sys_url : window.location.href.split('#')[0].toString()
		},
		dataType : "jsonp",
		jsonpCallback : "callback",
		success : function(ajax) {
			if(ajax.flag=="succ"){
				generate_menu();
				window.person_info = ajax['person_info'];
            	window.sys_list = ajax['sys_list'];
				$.getScript(sso_url+"/search/static/javascripts/nav_search.js");
			}
			else
				window.location.href = window.welcome;
		}
	});	
});

function generate_menu(){
        $.ajax({
	        type: "POST",
	        dataType : "jsonp",
	        url: window.sso+'/permission/scc/get_menu/',
	        dataType : "jsonp",
	        jsonpCallback:"callback",
	        success: function(ajax) {
                for (i = 0; i < ajax.length; i++){
                    $('#role_menu').append(
                        '<li>'+
                            '<a href="#" class="dropdown-toggle">'+
                                '<i class="icon-desktop"></i>'+
                                '<span>'+ajax[i].g_name+'</span>'+
                                '<b class="arrow icon-angle-down"></b>'+
                            '</a>'+
                            '<ul class="submenu" id="submenu'+i+'" style="display: none;"></ul>'+
                        '</li>'
                    );
				    for (j = 0; j < ajax[i].funs.length; j++){
                        $('#submenu'+i).append(
                            '<li><a href="'+ajax[i].funs[j].f_url+'"><i class="icon-double-angle-right"></i> '+ ajax[i].funs[j].f_name +'</a></li>'
                        )
				    }
                }
                //动态修改“修改密码”的模态框样式
                $("#search_btn").removeAttr("class");
        		$("#search_btn").attr("class","fa fa-search");
        		$("#reset_pw").removeAttr("class");
        		$("#reset_pw").attr("class","modal fade");
        		$("#reset_pw").find("h3").remove();
        		$("#reset_pw .modal-header").append("<h4 style='color:white;font-family:Microsoft Yahei'>修改密码</h4>");
        		var str = '<label id="lab" style="margin-right: 28px;margin-top: 15px;width: 50%;">旧密码：'+
        						'<input type="password" id="pw_old" style="margin-top: 2px;margin-left:14px">'+
        				  '</label>'+
						  '<label id="lab" style="margin-right: 28px;margin-top: 15px;clear: both">新密码：'+
						  		'<input type="password" id="pw_new" style="margin-top: 2px;margin-left:14px">'+ 
						  '</label>'+			         
						  '<label id="lab" style="margin-right: 15px;margin-top: 15px;clear: both">确认密码：'+
						  		'<input type="password" id="pw_again" style="margin-top: 2px;">'+
						  '</label>'+					          
						  '<label id="pw_warn" style="clear: both; padding-top:  10px; "></label>';      
        		$("#reset_pw .modal-body div").children().remove();
        		$("#reset_pw .modal-body div").append(str);
        		$("#pw_submit").removeAttr("class");
        		$("#pw_cancel").removeAttr("class");
        		$("#pw_submit").attr("class","btn btn-default");
        		$("#pw_cancel").attr("class","btn btn-default");
	        }
	    });
	}
