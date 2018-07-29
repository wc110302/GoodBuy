function ed_information() {
    $('#old_information').hide()
    $('#new_information').show()
}
function reed_infomation() {
    $('#old_information').show()
    $('#new_information').hide()
}
$(function () {
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
})
