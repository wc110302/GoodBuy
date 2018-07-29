$(function () {
    $.get("/admin_page/main_access/",function (data) {
        if(data.code == '200') {
            var access_amount = $('#Amount_of_access_table strong');
            var access_name = $('#Amount_of_access_table a');
            for(var i =0; i < access_amount.length; i++){
                access_amount.eq(i).html(data.access_amount[i]);
                access_name.eq(i).html(data.access_name[i])
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('Amount_of_access_form'));

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: '各网站访问量统计图'
                },
                tooltip: {},
                legend: {
                    data: ['访问量']
                },
                xAxis: {
                    data: data.access_name,
                },
                yAxis: {},
                series: [{
                    name: '访问量',
                    type: 'bar',
                    data: data.access_amount,
                }]
            };
        }

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    },'json');

    $.get("/admin_page/main_access2/",function (data) {
        if(data.code == '200') {
            $('#date_input').val(data.today).attr('max', data.today)
             // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('Amount_of_access2_form'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: '各网站访问量统计图'
                },
                tooltip: {},
                legend: {
                    data: ['访问量']
                },
                xAxis: {
                    type: 'category',
                    data: data.access_name,
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    name: '访问量',
                    type: 'line',
                    data: data.access_amount,
                }]
            };
        }

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    },'json');

    $.get("/admin_page/main_hotword/",function (data) {
        if(data.code == '200') {
            var hotwords = data.hotwords;
            var word = $('#Hot_Word_table a');
            var word_amount = $('#Hot_Word_table strong');
            for(var i =0; i < word.length; i++){
                word_amount.eq(i).html(hotwords[i].value);
                word.eq(i).html(hotwords[i].name);
            }
            var myChart2 = echarts.init(document.getElementById('Hot_Word_from'));
            // 基于准备好的dom，初始化echarts实例
            var option2 =({
                series : [
                    {
                        name: '热门对比',
                        type: 'pie',
                        radius: '55%',
                        data:hotwords
                    }
                ]
            })
            myChart2.setOption(option2);
        }
    },'json')

    $.get("/admin_page/main_focus/",function (data) {
        focus = data.focus
        if(data.code == '200') {
            var focus_goods_html = '<tr><th colspan="4" class="group-title">商品收藏排行</th></tr>'
            for(var i =0; i < focus.length; i++){
                focus_goods_html += '<tr><td><strong>'+(i+1)+'</strong></td><td><a href="#">'+focus[i].goods__name+'</a></td><td><strong>'+focus[i].sum+'</strong></td></tr>'
            }
            $('#focus_goods_table').html(focus_goods_html)
        }
    },'json')

});

function time_access_change() {
    var choice_time = $('#date_input').val()
    $.get('/admin_page/main_access2', {'choice_time':choice_time}, function (data) {
        if(data.code == '200') {
             // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('Amount_of_access2_form'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: '各网站访问量统计图'
                },
                tooltip: {},
                legend: {
                    data: ['访问量']
                },
                xAxis: {
                    type: 'category',
                    data: data.access_name,
                },
                yAxis: {},
                series: [{
                    name: '访问量',
                    type: 'line',
                    data: data.access_amount,
                }]
            };
        }

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    })
}


function date_access_change() {
    var choice_date = $('#data_select').val()
    $.get('/admin_page/main_access2/', {'choice_date':choice_date}, function (data) {
        if(data.code == '200') {
             // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('Amount_of_access2_form'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: '各网站访问量统计图'
                },
                tooltip: {},
                legend: {
                    data: ['访问量']
                },
                xAxis: {
                    type: 'category',
                    data: data.access_name,
                },
                yAxis: {},
                series: [{
                    name: '访问量',
                    type: 'line',
                    data: data.access_amount,
                }]
            };
        }

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    })
}