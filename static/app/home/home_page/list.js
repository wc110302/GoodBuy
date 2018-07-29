/*
@功能：列表页js
@作者：diamondwang
@时间：2013年11月13日
*/

$(function(){
	var sort_list = $('.sort dd')
	sort_list.removeClass('cur')
	var path = location.search
    var sort = path.split('sort=')
	var sort_index = sort[1][0]
	sort_list.eq(sort_index).addClass('cur')
	$(".child h3").click(function(){
		$(this).toggleClass("on").parent().find("ul").toggle();
	});
});
function page_text(key,sort,brand){
	alert(1)
	var page = $('.page_num').val();
	$.get('/search', {'key':key, 'sort':sort,'brand':brand, 'page':page},function () {
		alert(2)
    })
}