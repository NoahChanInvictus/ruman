// 热点监测详情 页面js 【新闻热点/溯源分析-详情  版本】 【页面改为了tab样式】

// 基本信息
    var card_url = '/hotSpot/hotspotReport/basicMessage/?id='+id;
    public_ajax.call_request('get',card_url,card);

    function card(data){
        $('#card .type-1').text(data.title).attr('title',data.title);
        $('#card .type-4').text(data.web).attr('title',data.web);
        $('#card .type-2').text(data.in_time).attr('title',data.in_time);
        $('#card .type-3').text(data.key_word).attr('title',data.key_word);
        $('#card .type-5').text(data.url).attr('title',data.url).attr('href',data.url);

        $('#card .hotContent #hotContent').text(data.content)
    }

// ---------暂 弃用
    var obj=[{a:'经济',b:'2018-02-03',c:'231',d:'微博',e:'用CSS能非常容易的改变这些图标的颜色、大小、阴影以及任何CSS能控制的属性。'},
        {a:'人才',b:'2017-12-11',c:'231',d:'百度',e:'一个字体文件包含了所有图标。Font Awesome 助你完整表达web页面上每个动作的含义。'},
        {a:'历史',b:'2018-07-03',c:'231',d:'知乎',e:'Font Awesome 中包含的都是矢量图标，在高分辨率的显示器上也能完美呈现。'},
        {a:'诈骗',b:'2016-11-08',c:'231',d:'facebook',e:'Font Awesome是完全从头设计的整套图标，完全和Bootstrap 2.2.2版本兼容.'},
        {a:'非法',b:'2018-02-03',c:'231',d:'twitter',e:'虽然增加了 16% 的图标，3.0 版本的体积却变得更小了。 Font Awesome 还可以定制，将你不需要的图标去掉。'},
        {a:'大学生',b:'2014-02-23',c:'231',d:'人人网',e:'Font Awesome supports IE7. If you need it, you have my condolences.'},
        {a:'维权',b:'2017-05-03',c:'231',d:',stockflow',e:'用CSS能非常容易的改变这些图标的颜色、大小、阴影以及任何CSS能控制的属性。'},
    ]
    function tables(data) {
        $('#tableContent').bootstrapTable('load', data);
        $('#tableContent').bootstrapTable({
            data:data,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize: 5,//单页记录数
            pageList: [15,20,25],//分页步进值
            sidePagination: "client",//服务端分页
            searchAlign: "left",
            searchOnEnterKey: false,//回车搜索
            showRefresh: false,//刷新按钮
            showColumns: false,//列选择按钮
            buttonsAlign: "right",//按钮对齐方式
            locale: "zh-CN",//中文支持
            detailView: false,
            showToggle:false,
            sortName:'bci',
            sortOrder:"desc",
            columns: [
                {
                    title: "",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        var str=
                            '<div class="inforContent" style="text-align: left;">'+
                            '    <div class="main">'+
                            '    <img src="/static/images/textIcon.png" class="textFlag" style="top:8px;">'+
                            '    <p class="option">'+
                            '       <span>热点新词：<b style="color: #ff6d70">'+row.a+'</b></span>'+
                            '       <span>发布时间：<b style="color: #ff6d70">'+row.b+'</b></span>'+
                            '       <span>评论数：<b style="color: #ff6d70">'+row.c+'</b></span>'+
                            '       <span>渠道：<b style="color: #ff6d70">'+row.d+'</b></span>'+
                            '       <button class="originalbtn btn-primary btn-xs">查看原文</button>'+
                            '    </p>'+
                            '    <p class="context">'+ row.e+'</p>'+
                            '</div>'+
                            '</div>';
                        return str;
                    }
                },
            ],
        });
    };
    // tables(obj);

// 演化分析
    // 热度图
    var myChart_analysis = echarts.init(document.getElementById('analysis'));
    myChart_analysis.showLoading();

    var time_val = $('#time_select').val();
    var source_val = $('#five_select').val();
    var evolution_url = '/hotSpot/hotspotReport/evolution?frequency='+time_val+'&source='+source_val+'&id='+id;
    public_ajax.call_request('get',evolution_url,line_1);


    function line_1(data) {
        // var myChart = echarts.init(document.getElementById('analysis'),'chalk');
        // var myChart = echarts.init(document.getElementById('analysis'));
        var option = {
            backgroundColor:'transparent',
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        color: '#57617B'
                    }
                }
            },
            grid: {
                left: '4%',
                right: '7%',
                bottom: '8%',
                top:'14%',
                containLabel: true
            },
            xAxis: [{
                type: 'category',
                boundaryGap: false,
                axisLine: {
                    lineStyle: {
                        // color: '#fff',
                        color: '#333',
                        width:'2'
                    }
                },
                axisLabel: {
                    textStyle: {
                        // color: '#fff',
                        color:'#333',
                        fontWeight:'700'
                    }
                },
                // data: ['周一','周二','周三','周四','周五','周六','周日'],
                data: data.time,
            }],
            yAxis: [{
                name:'热度',
                type: 'value',
                axisTick: {
                    show: false
                },
                axisLine: {
                    lineStyle: {
                        // color: '#fff',
                        width:'2'
                    }
                },
                axisLabel: {
                    margin: 10,
                    textStyle: {
                        fontSize: 14,
                        fontWeight:'700',
                        // color:'white',
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: '#57617B'
                    }
                }
            }],
            series: [
                {
                    name: '',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 5,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1,
                        }
                    },
                    areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(137, 189, 27, 0.8)'
                            }, {
                                offset: 1,
                                color: 'rgba(137, 189, 27, 0)'
                            }], false),
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 10
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: 'rgb(137,189,27)',
                            borderColor: 'rgba(137,189,2,0.27)',
                            borderWidth: 12
                        }
                    },
                    // data: [11, 11, 15, 13, 12, 13, 10],
                    data: data.count,
                }
            ]
        };
        myChart_analysis.hideLoading();
        myChart_analysis.setOption(option);
    }
    // line_1();
    // 更新下拉框
        $('#time_select').change(function(){
            myChart_analysis.showLoading();
            time_val = $(this).val();
            source_val = $('#five_select').val();
            evolution_url = '/hotSpot/hotspotReport/evolution?frequency='+time_val+'&source='+source_val+'&id='+id;
            public_ajax.call_request('get',evolution_url,line_1);
        })

        $('#five_select').change(function(){
            myChart_analysis.showLoading();
            source_val = $(this).val();
            time_val = $('#time_select').val();
            evolution_url = '/hotSpot/hotspotReport/evolution?frequency='+time_val+'&source='+source_val+'&id='+id;
            public_ajax.call_request('get',evolution_url,line_1);
        })

// 鱼骨图
    //暂弃用
        var fish=[['','人民网','2017-11-11 11:11'],
            ['','中国经济','2018-01-11 10:11'],
            ['','京东金融','2018-01-11 10:11'],
            ['','263财富网','2017-08-03 09:11'],
            ['','网易财经','2017-08-03 09:11'],
            ['','新浪财经','2016-12-11 13:33'],
            ['','中证网','2018-11-11 11:11'],
            ['','搜狐新闻','2018-11-11 11:11'],
        ]
        function spread_pie_3(data){
            var finshdata = '';
            $.each(data,function (index,item) {
                if (index%2 == 0){
                    finshdata+=
                        '<div class="fish_item">'+
                        '   <ul class="top">'+
                        // '       <li class="weibo" title="'+item[0]+'" style="border-left: 1px solid rgb(248, 151, 130);">事件ID：'+item[0]+'</li>'+
                        '       <li class="weibo" title="'+item[1]+'" style="height: 86px;white-space: normal;border-left: 1px solid rgb(248, 151, 130);">公司：'+item[1]+'</li>'+
                        '       <li class="weibo" title="'+item[2]+'" style="border-left: 1px solid rgb(248, 151, 130);">时间：'+item[2]+'</li>'+
                        '       <li class="line-last line-point" style="background-position: 0 0;"></li>'+
                        '   </ul>'+
                        '</div>';
                }else {
                    finshdata+=
                        '<div class="fish_item" style="top: 1.22rem;">'+
                        '   <ul class="bottom">'+
                        // '       <li class="weibo" title="'+item[0]+'" style="border-left: 1px solid rgb(26, 132, 206);">事件ID：'+item[0]+'</li>'+
                        '       <li class="weibo" title="'+item[1]+'" style="height:0.86rem;white-space: normal;border-left: 1px solid rgb(26, 132, 206);">公司：'+item[1]+'</li>'+
                        '       <li class="weibo" title="'+item[2]+'" style="border-left: 1px solid rgb(26, 132, 206);">时间：'+item[2]+'</li>'+
                        '       <li class="line-last line-point" style="background-position: 0 -20px;"></li>'+
                        '   </ul>'+
                        '</div>';
                }
            })
            $(".fishBone .fish_box").append(finshdata);
            var _p=0;
            var fish_length=data.length;
            $('#container .fishBone .fish_box').width(fish_length*320);
            var fish_width=fish_length*180;
            $('#container .fishBone .prev').on('click',function () {
                _p+=180;
                if (fish_length<=5){
                    alert('没有其他卡片内容了。');
                }else {
                    var fishbone=$(".fishBone .fish_box");
                    var step1=_p;
                    if (step1 > 0 ){
                        alert('没有其他内容了。');
                        _p=0;
                    }else {
                        $(fishbone).css({
                            "-webkit-transform":"translateX("+step1+"px)",
                            "-moz-transform":"translateX("+step1+"px)",
                            "-ms-transform":"translateX("+step1+"px)",
                            "-o-transform":"translateX("+step1+"px)",
                            "transform":"translateX("+step1+"px)",
                        });
                    }
                }
            });
            $('#container .fishBone .next').on('click',function () {
                _p-=180;
                if (fish_length<=5){
                    alert('没有其他卡片内容了。');
                }else {
                    var step2=_p;
                    var fishbone=$(".fishBone .fish_box");
                    if (step2 <= (-fish_width+900)){
                        alert('没有其他内容了');
                        _p=-180;
                    }else {
                        $(fishbone).css({
                            "-webkit-transform":"translateX("+step2+"px)",
                            "-moz-transform":"translateX("+step2+"px)",
                            "-ms-transform":"translateX("+step2+"px)",
                            "-o-transform":"translateX("+step2+"px)",
                            "transform":"translateX("+step2+"px)",
                        });
                    };
                }
            });
        }
        // spread_pie_3(fish);

    // LL新版
    var data = [
        {'审理时间':'2016-12-20 至 2016-12-20',
        '承办庭室':'吕磊'
        ,'承办法官':'吕磊',
        '承办法院':'吕磊法院',
        '案件状态':'吕磊',
        '案号':'(XXXX)XXXXXX第吕磊号'},
        {'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},{'审理时间': '2016-12-20 至 2016-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'}];
    //创建案件历史
    // $(".fishBone").fishBone(data);

    var fishSource_val = $('#fishSource_select').val();
    var propagate_url = '/hotSpot/hotspotReport/propagate/?source='+fishSource_val+'&id='+id;
    // var propagate_url = '/hotSpot/hotspotReport/propagate/?source=bbs&id=1';
    public_ajax.call_request('get',propagate_url,propagate);
    function propagate(data){
        $(".fishBone").empty().append('<center>加载中...</center>');
        if(data.length == 0){
            $(".fishBone").empty().append('<center>暂无记录</center>');
        }else {
            var fishdata = [];
            for(var i=0;i<data.length;i++){
                // if(data[i].title.length>14){
                //     data[i].title = data[i].title.substr(0,14)+'...'
                // }

                // 修改插件文件 fishBone.js  有 LL 标识

                // fishdata.push({'发布时间':data[i].publish_time,'标题':data[i].title,'承办法官':'吕磊','承办法院':'吕磊','案件状态':'吕磊','承办庭室':'吕磊'});//多个li时 可以把fishBone.js中 改回来
                fishdata.push({'发布时间':data[i].publish_time,'标题':data[i].title,'关键词':data[i].keyword,'作者':data[i].author,'主题':data[i].topic,'链接':data[i].url});//多个li时 可以把fishBone.js中 改回来
                // fishdata.push({'发布时间':data[i].publish_time,'标题 ':data[i].title});
                // fishdata.push({'发布时间':data[i].publish_time,'标题':data[i].title,}); // fishBone.js中 ==标题 时是特殊样式
            }
            fishdata.push({'发布时间':' ','标题':' ','关键词':' ','作者':' ','主题':' ','链接':' '});
            // console.log(fishdata);
            $(".fishBone").empty();
            $(".fishBone").fishBone(fishdata);

            $('.fishBone li.item:last').hide();
        }

        $('#spread-pie-3 center.loading').hide();
    }
    // 更新下拉框
        $('#fishSource_select').change(function(){
            $('#spread-pie-3').empty().append('<center class="loading">正在加载中...</center>');
            // console.log($(this).val());
            propagate_url = '/hotSpot/hotspotReport/propagate/?source='+$(this).val()+'&id='+id;
            public_ajax.call_request('get',propagate_url,propagate);
        })

// 字符云 ====
    // function createRandomItemStyle() {
    //     return {
    //         normal: {
    //             color: 'rgb(' + [
    //                 Math.round(Math.random() * 160),
    //                 Math.round(Math.random() * 160),
    //                 Math.round(Math.random() * 160)
    //             ].join(',') + ')'
    //         }
    //     };
    // }


    require.config({
        paths: {
            echarts: '/static/js/echarts-2/build/dist',
        }
    });
    function keywords() {
        // for(var i=0;i<data.length;i++){
        //     data[i].itemStyle = createRandomItemStyle();
        // }
        require(
            [
                'echarts',
                'echarts/chart/wordCloud'
            ],
            //关键词
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var wordCloud_myChart = ec.init(document.getElementById('word-cloud'),'chalk');
                wordCloud_myChart.showLoading({
                    text: '加载中...',
                    color: '#c23531',
                    // textColor: '#000',
                    textColor: '#c23531',
                    maskColor: 'rgba(0,0,0,.1)',
                    // zlevel: 0
                });

                var source_word_val = $('#wordCloud_select').val();
                var wordCloudurl = '/hotSpot/hotspotReport/wordcloud?source='+source_word_val+'&id='+id;
                public_ajax.call_request('get',wordCloudurl,wordCloud_L);
                function wordCloud_L(data){
                    for(var i=0;i<data.length;i++){
                        data[i].itemStyle = createRandomItemStyle();
                    }
                    var option = {
                        title: {
                            text: '',
                        },
                        tooltip: {
                            show: true,
                        },
                        series: [{
                            type: 'wordCloud',
                            size: ['100%', '90%','100%','90%','100%','20%','10%','20%'],
                            textRotation : [0, 45, 90, -45],
                            textPadding: 0,
                            autoSize: {
                                enable: true,
                                minSize: 18
                            },
                            // 假数据
                                /*
                                data: [
                                    {
                                        name: "我要金蛋",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "屹农金服",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "理财去",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "联投银帮",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "弘信宝",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "网惠金融",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "晶行财富",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "孺牛金服",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "摩根浦捷贷",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "知屋理财",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "沪臣地方金融",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "升隆财富",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "冰融贷",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "靠谱鸟",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "速溶360",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "存米网",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                    {
                                        name: "太保金服",
                                        value: 999,
                                        itemStyle: createRandomItemStyle()
                                    },
                                ]
                                 */
                            data:data
                        }]
                    };

                    wordCloud_myChart.hideLoading();
                    wordCloud_myChart.setOption(option);
                }

                // myChart.setOption(option);
                // 更新下拉框
                $('#wordCloud_select').change(function(){
                    wordCloud_myChart.showLoading();
                    source_word_val = $(this).val();
                    // console.log(source_word_val);
                    wordCloudurl = '/hotSpot/hotspotReport/wordcloud?source='+source_word_val+'&id='+id;
                    public_ajax.call_request('get',wordCloudurl,wordCloud_L);
                })
            }
        );
    }
    keywords();



// 纵向 主题时间轴 在html文件
    var topic_source_val = $('#semanticsSource_select').val();
    var topicaxis_url = '/hotSpot/hotspotReport/topicaxis/?source='+topic_source_val+'&id='+id;//
    // var topicaxis_url = '/hotSpot/hotspotReport/topicaxis/?source=bbs&id=1';//测试的
    public_ajax.call_request('get',topicaxis_url,topicaxis);
    function topicaxis(data){
        // console.log(data);
        var classLR = '';

        var str = '';

        if(data.length == 0){
            $('.VivaTimeline').empty().html('<center>暂无记录</center>');;
        }else {
            for(var n=0;n<data.length;n++){
                str += '<dt>'+data[n].month+'</dt>';

                for(var i=0;i<data[n].monthtext.length;i++){
                    if(i%2 == 0){
                        classLR = 'pos-left';
                    }else {
                        classLR = 'pos-right';
                    }
                    var eventStr = '';
                    if(data[n].monthtext[i].text.length != 0){
                        var eventHeading_str = '';
                        for(var j=0;j<data[n].monthtext[i].text.length;j++){
                            eventStr += '<div class="row">'+
                                            '<div class="events-desc">'+data[n].monthtext[i].text[j].content+

                                            '</div>'+
                                        '</div>';
                            // eventHeading_str = data[n].monthtext[i].text[j].title;
                            eventHeading_str += '<div class="events-header">'+data[n].monthtext[i].text[j].title+'</div>';
                        }
                    }
                    str += '<dd class="'+classLR+' clearfix">'+
                                '<div class="circ"></div>'+
                                '<div class="time">'+data[n].monthtext[i].date+'</div>'+
                                '<div class="events">'+
                                    // '<div class="events-header">'+eventHeading_str+'</div>'+
                                    '<div class="events-head">'+eventHeading_str+'</div>'+
                                    // eventHeading_str+
                                    '<div class="events-body">'+eventStr+
                                        /*


                                            <div class="row">
                                                <div class="col-md-6 pull-left">
                                                    <img class="events-object img-responsive img-rounded" src="/static/images/VivaTimeline/dog01.jpeg" />
                                                </div>
                                                <div class="events-desc">
                                                    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-6 pull-left">
                                                    <img class="events-object img-responsive img-rounded" src="/static/images/VivaTimeline/dog02.jpeg" />
                                                </div>
                                                <div class="events-desc">
                                                    Morbi at nisi vitae mauris pretium egestas. Morbi placerat risus ligula, nec placerat urna porta vel. Nullam sollicitudin orci quis odio eleifend, ut facilisis orci lobortis. Vivamus sed lobortis odio. Nam volutpat, leo a ullamcorper luctus, sapien libero auctor est, sed semper massa turpis sed quam. Mauris posuere, libero in ultricies dignissim, lacus purus egestas urna, nec semper lorem tellus non eros. Nam at bibendum libero. Curabitur a ante et orci cursus tincidunt. Vivamus dictum, libero et rhoncus congue, nulla erat mollis dui, vitae cursus dui justo quis velit. In a tellus arcu. Nam at lobortis nisl. Donec consequat placerat eros, quis elementum mauris sodales a. Maecenas id feugiat velit. Phasellus dictum eleifend varius. Cras nec orci turpis. Aenean ut turpis nibh.
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-6 pull-left">
                                                    <img class="events-object img-responsive img-rounded" src="/static/images/VivaTimeline/dog03.jpeg" />
                                                </div>
                                                <div class="events-desc">
                                                    Cras condimentum, metus ut vehicula euismod, odio massa pulvinar neque, id gravida neque est et sem. Proin consequat id nibh quis molestie. Quisque vehicula purus id purus elementum facilisis. Phasellus sodales nibh quis neque rhoncus aliquet. Nunc eget ipsum efficitur, pretium arcu et, gravida purus. Phasellus tempor lacus ac enim pulvinar elementum. Integer aliquet justo lacinia nunc tempus vulputate.
                                                </div>
                                            </div>
                                         */
                                    '</div>'+
                                    '<div class="events-footer">'+
                                    '</div>'+
                                '</div>'+
                            '</dd>';
                }
            }
            $('.VivaTimeline center.loading').hide();
            $('.VivaTimeline dl').empty().html(str);

            $('.VivaTimeline').vivaTimeline({
                // carousel: true,//自动轮播
                carousel: false,//自动轮播 关闭时
                // carouselTime: 2000//轮播间隔
            });
        }


    }

    $('#semanticsSource_select').change(function(){
        $('.VivaTimeline dl').empty().append('<center class="loading">正在加载中...</center>');
        topic_source_val = $(this).val();
        topicaxis_url = '/hotSpot/hotspotReport/topicaxis/?source='+topic_source_val+'&id='+id;
        public_ajax.call_request('get',topicaxis_url,topicaxis);
    });
