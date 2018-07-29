/*
@功能：头部js
@作者：diamondwang
@时间：2013年11月13日
*/
/* 注意，要在页面中先引入jquery*/
$(function(){
	// 热门比价
	$.get("/admin_page/main_hotword/",function (data) {
        if(data.code == '200') {
            hot_search = $('.hot_search');
            var hot_search_html = '<strong>热门搜索:</strong>';
			for(var i =0; i < data.hotwords.length; i++) {
				hot_search_html += '<a href="/search?key='+data.hotwords[i].name+'">&nbsp;&nbsp;'+data.hotwords[i].name+'&nbsp;&nbsp;</a>'
            }
            hot_search.html(hot_search_html);
        }
    },'json')

	//头部用户
	$(".user").mouseover(function(){
		$(this).find("dd").show();
		$(this).find("dt").addClass("on");
	}).mouseout(function(){
		$(this).find("dd").hide();
		$(this).find("dt").removeClass("on");
	});

	//购物车
	$(".cart").mouseover(function(){
		$(this).find("dd").show();
		$(this).find("dt").addClass("on");
	}).mouseout(function(){
		$(this).find("dd").hide();
		$(this).find("dt").removeClass("on");
	});

	//导航菜单效果
	$(".cat").hover(function(){
		$(this).find(".cat_detail").show();
		$(this).find("h3").addClass("on");
	},function(){
		$(this).find(".cat_detail").hide();
		$(this).find("h3").removeClass("on");
	});

	//非首页，导航菜单显隐效果
	$(".cat1").hover(function(){
		$(".cat1 .cat_hd").addClass("on").removeClass("off");
		$(".cat1 .cat_bd").show();
	},function(){
		$(".cat1 .cat_hd").addClass("off").removeClass("on");
		$(".cat1 .cat_bd").hide();
	});


});
