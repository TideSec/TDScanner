//分页焦点偏移
var nowPage = parseInt((location.href).split('/')[4]);//获取当前页
var pageCount = Number($("#page_num").text());
var resultCount = $("#result_count").text()
var pagearr = [];
if(!nowPage){
	nowPage = 1;
}

$("#str_page").text("当前显示第"+nowPage+"页/"+pageCount+"页，共"+resultCount+"条数据");

$(".page_the_show").empty()
$(".page_the_hide li").each(function(){
	pagearr.push("<li>"+$(this).html()+"</li>");
})
var pageItem = "";
if(nowPage > 1)
	pageItem='<li><a id = "the_pre" ><span>&laquo;</span></a></li><li><a id = "the_first"><span>首页</span></a></li>';
else
	pageItem='<li><a id = "the_first"><span>首页</span></a></li>';
if(pageCount<=8){
	for(var i=2;i<pageCount+2;i++)
		pageItem+=pagearr[i];
}else if(nowPage-3<=0 && pageCount>7){
	for(var i=2;i<9;i++){
		pageItem+=pagearr[i];
	}
}else if(nowPage-3>0 && nowPage+3<=pageCount){
	for(var i=nowPage-2;i<nowPage+5;i++){
		pageItem+=pagearr[i];
  	}
}else if(nowPage-3>0 && nowPage+3>pageCount){
	for(var i = pageCount-5;i<pageCount+2;i++){
		pageItem+=pagearr[i];
	}
}
if(nowPage == pageCount)
  	pageItem+='<li><a id = "the_last"><span>末页</span></a></li>'
else
  	pageItem+='<li><a id = "the_last"><span>末页</span></a></li> <li><a id = "the_next"><span>&raquo;</span></a></li>';

$(".page_the_show").append(pageItem);

$(".page_the_show li a").each(function(){
	if($(this).text() == nowPage){
		$(this).parent().attr("class","active");
	}
})
//上一页
$("#the_pre").on("click",function(){
	$(".page_the_show .active").prev().find("a span").click();
})
//下一页
$("#the_next").on("click",function(){
	$(".page_the_show .active").next().find("a span").click();
})
//首页
$("#the_first").on("click",function(){
	$(".page_the_hide").find("li:eq(2) span").click();
})
//尾页
$("#the_last").on("click",function(){
	$(".page_the_hide").children().last().prev().prev().find("span").click();
})





