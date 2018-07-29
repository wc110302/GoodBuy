

$(document).ready(function () {
    var path = location.href;
    var pk = path.split('/')[4];
    $.get('/items/' + pk + '/', function (data) {
        $('.summary h3 strong').text(data.data.name);
        new Vue({
            el: "#sum_vue",
            data: {
                id: data.data.id,
                price: data.data.c_price,
                img_url: data.data.image,
                c_amount: data.data.comments_amount,
                s_number: data.data.sales_number,
            },
            delimiters: ['${', '}']
        });
        new Vue({
            el: ".xxx",
            data: {
                description: data.data.description,
                name: data.data.name,
                source_url: data.data.source,
            },
            delimiters: ['${', '}']
        });
    });

    $('#search').submit(function (e) {
       e.preventDefault();
       var txt = $('.txt').text();
       $.post('//', {'goods_id': pk, 'text': txt}, function (data) {

       });
    });

    $.get('/is_focus/' + pk + '/', function (data) {
            if (data.data.is_focus == true){
                $('#focussubmit').attr('value', '已收藏')
            }else if (data.data.is_focus == false){
                $('#focussubmit').attr('value', '加入收藏')
            }
        });

    $.get('/history/' + pk + '/', function (data) {

        var dates = data.data.date.split(',');
        var prices = data.data.price.split(',');
        // 基于准备好的dom，初始化echarts实例

        var myChart = echarts.init(document.getElementById('mainCharts'));
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '历史价格'
            },
            xAxis: {
                type: 'category',
                data: dates.slice(0,30)
            },
            yAxis: {
                type: 'value',
                min: 6700
            },
            series: [{
                type: 'line',
                smooth: true,
                data:prices.slice(0,30)
            }]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    });

    $('#focus').submit(function (e) {
        e.preventDefault();
        $.post('/focus/', {'item_id': pk}, function (data) {
            if (data.data.is_focus == true){
                $('#focussubmit').attr('value', '已收藏')
            }else if (data.data.is_focus == false){
                $('#focussubmit').attr('value', '加入收藏')
            }
        });
    });

    $.get('/comments/' + pk + '/', function (data) {
        var int_ave_score = Math.round(data.score_data.ave_score);
        if(int_ave_score < 1){
            int_ave_score = 1;
        }
        $('.goodsinfo ul li').eq(2).children().eq(1).attr('class', 'star'+int_ave_score);
        $('.goodsinfo ul li').eq(2).children().eq(2).text(data.score_data.ave_score.toFixed(1)+'分');
        new Vue({
            el: "#comment-vue",
            data: {
                ave_sore: data.score_data.ave_score,
                good_comments: data.score_data.good_comments,
                mid_comments: data.score_data.mid_comments,
                bad_comments: data.score_data.bad_comments,
                good_comments_percent: data.score_data.good_comments_percent,
                mid_comments_percent: data.score_data.mid_comments_percent,
                bad_comments_percent: data.score_data.bad_comments_percent,
                comments_data: data.data,
                page: 1, //当前页面
                pageTotal: 10, //总页数
                showPage: 10, //最多显示10个num-item
                showPageArr: [], //显示的num-item数组
                goodsList: {}, //商品数据
                showLeftEllipsis: false,
                showRightEllipsis: false
            },

            mounted: function() {
					var oThis = this;
					this.pageTotal = parseInt(data.data.length / 7) + 1;
					tpage = this.pageTotal;
					if(this.pageTotal <= this.showPage) {
						this.showPage = this.pageTotal;
					}
					this.showPageFn();

					$(document).on('click', '.num-item', function() {
						oThis.page = parseInt($(this).html());
						oThis.showPageFn();
					});
				},
				methods: {
					getData: function() {
						this.goodsList = data.data.slice(this.page * 7 - 7, this.page * 7);
						xxx = data.data.slice(this.page * 7 - 7, this.page * 7)
					},

					showPageFn: function() {
						// debugger;
						var min = 0,
							max = this.showPage;
						this.showLeftEllipsis = this.showRightEllipsis = false;
						this.showPageArr = [];
						if(this.page <= this.showPage / 2) {
							min = 0;
							max = this.showPage;
						} else if(this.pageTotal - this.page <= Math.ceil(this.showPage / 2)) {
							min = this.pageTotal - this.showPage;
							max = this.pageTotal;
						} else {
							min = Math.round(this.page - this.showPage / 2);
							max = Math.round(this.page + this.showPage / 2);
						}
						for(var i = min + 1; i < max + 1; i++) {
							this.showPageArr.push(i);
						}
						if(this.showPageArr[0] > 1) {
							this.showLeftEllipsis = true;
						}
						if(this.showPageArr[this.showPageArr.length - 1] < this.pageTotal) {
							this.showRightEllipsis = true;
						}
						this.getData();
					},

					goPre: function() {
						if(this.page == 1) {
							return;
						}
						this.page--;
						this.showPageFn();
					},

					goNext: function() {
						if(this.page == this.pageTotal) {
							return;
						}
						this.page++;
						this.showPageFn();
					},

					inputJump: function() {
						var value = $('.index-target').val();
						if(parseInt(value) < 1 || parseInt(value) > this.pageTotal || value.trim() == '') {
							this.page = 1;
						} else {
							this.page = parseInt(value);
						}
						$('.index-target').val('');
						this.showPageFn();
					}
				},
            delimiters: ['${', '}'],
        });

    });



    $('#comments').submit(function (e) {
        score = $('input[name=grade]:checked').val();
        content = $('#comments_text').val();
        e.preventDefault();
        $.post('/comments/' + pk + '/', {'goods_id': pk, 'content': content, 'score': score}, function (data) {
            $('input[name=grade]').attr('checked', 'off');
            $('#comments_text').val('');
        });
    });
});



$(function(){
	//商品缩略图左右移动效果
	//点击后退
	$("#backward").click(function(){
		var left = parseInt($(".smallpic_wrap ul").css("left")); //获取ul水平方向偏移量
		var offset = left + 62;
		if (offset <= 0){
			$(".smallpic_wrap ul").stop(true,false).animate({left:offset},"slow",'',function(){
				//动画完成之后，判断是否到了左边缘
				if ( parseInt($(".smallpic_wrap ul").css("left")) >= 0 ){
					$("#backward").removeClass("on").addClass("off");
				}
			});
			//开启右边的按钮
			$("#forward").removeClass("off").addClass("on");
		}

		$(this).blur(); //去除ie 虚边框
	});

	//点击前进
	$("#forward").click(function(){
		var left = parseInt($(".smallpic_wrap ul").css("left")); //获取ul水平方向偏移量
		var len = $(".smallpic_wrap li").size() * 62; //获取图片的整体宽度(图片数 * 图片宽度)558
		var offset = left - 62;
		if (offset >= -(len - 62*5)){
			$(".smallpic_wrap ul").stop(true,false).animate({left:offset},"slow",'',function(){
				//判断是否到了右边缘
				if ( parseInt($(".smallpic_wrap ul").css("left")) <= -(len - 62*5) ){
					$("#forward").removeClass("on").addClass("off");
				}
			});
			//开启左边的按钮
			$("#backward").addClass("on").removeClass("off");

		}

		$(this).blur(); //去除ie 虚边框
	});

	//商品详情效果
	$(".detail_hd li").click(function(){
		$(".detail_div").hide().eq($(this).index()).show();
		$(this).addClass("on").siblings().removeClass("on");
	});
});
