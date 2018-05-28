// 适配分辨率
    var pageData=6;
    if (screen.width <= 1536){
        pageData=6;
    }else {
        pageData=10;
    }


// 热点监测 表格
    var hotSpotData = [
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'论坛','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'App','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'知乎','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'论坛','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'App','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'知乎','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'论坛','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'App','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'知乎','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'论坛','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'App','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'知乎','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'论坛','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'App','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'知乎','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'论坛','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'机智达人','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'沈小司司','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
    ]

    var hotSpot_url = 'hotspotNewsText';
    public_ajax.call_request('get',hotSpot_url,hotSpot);
    function hotSpot(data) {
        $('#hotspotTable p.loading').show();
        $('#hotspotTable').bootstrapTable('load', data);
        $('#hotspotTable').bootstrapTable({
            data:data,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize: pageData,//单页记录数
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
            // showLoading:true,
            columns: [
                {
                    title: "新闻标题",//标题
                    field: "title",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        var title = '';

                        if (row.title==''||row.title=='null'||row.title=='unknown'||!row.title){
                            return '未知';
                        }else if(row.title.length >=20){
                            title = row.title.slice(0,20)+'...';
                            return '<span style="cursor:pointer;color:white;" title="'+row.title+'">'+title+'</span>';
                        }else {
                            title = row.title;
                            return '<span style="cursor:pointer;color:white;" title="'+row.title+'">'+title+'</span>';
                        };
                    }
                },
                {
                    title: "发布网站",//标题
                    field: "web",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.web==''||row.web=='null' || row.web==null ||row.web=='unknown'||!row.web){
                            return '未知';
                        }else {
                            return row.web;
                        };
                    }

                },
                {
                    title: "发布时间",//标题
                    field: "in_time",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.in_time==''||row.in_time=='null' || row.in_time==null ||row.in_time=='unknown'||!row.in_time){
                            return '未知';
                        }else {
                            return row.in_time;
                        };
                    }

                },
                // {
                //     title: "发布渠道",//标题
                //     field: "c",//键名
                //     sortable: true,//是否可排序
                //     order: "desc",//默认排序方式
                //     align: "center",//水平
                //     valign: "middle",//垂直
                //     formatter: function (value, row, index) {
                //         if (row.c==''||row.c=='null' || row.c==null ||row.c=='unknown'||!row.c){
                //             return '未知';
                //         }else {
                //             return row.c;
                //         };
                //     }
                // },
                {
                    title: "关键词",//标题
                    field: "key_word",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.key_word==''||row.key_word=='null' || row.key_word==null ||row.key_word=='unknown'||!row.key_word){
                            return '未知';
                        }else {
                            return row.key_word;
                        };
                    }
                },
                {
                    title: "新闻链接",//标题
                    field: "url",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        var str = '<a style="cursor:pointer;color:white;" title="'+row.url+'" href="'+row.url+'" target="_blank"> <i class="icon icon-link"></i></a>';
                        if (row.url==''||row.url=='null' || row.url==null ||row.url=='unknown'||!row.url){
                            return '未知';
                        }else {

                            return str;
                        };
                    }
                },
                {
                    title: "溯源详情",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.id+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                    }
                },
                {
                    title: "处理",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<input type="checkbox" id="checkbox_d'+index+'" class="chk"/><label for="checkbox_d'+index+'"></label>';
                    }
                },
            ],
            formatNoMatches: function(){
                return "没有相关的匹配结果";  //没 效果
            },
            formatLoadingMessage: function(){
                return "请稍等，正在加载中。。。";
            },
        });
        $('#hotspotTable p.loading').hide();
        $('.hotspotTable .fixed-table-toolbar .search input').attr('placeholder','请输入查询内容');
    };
    // hotSpot(hotSpotData);

// 跳转详情页
    function jumpFrame_1(id) {
        var html = '';
        html='/index/hotDetail?id='+id;
        // window.location.href=html;
        window.open(html);
    }



// 已放入 详情页

    // var obj=[{a:'经济',b:'2018-02-03',c:'231',d:'微博',e:'用CSS能非常容易的改变这些图标的颜色、大小、阴影以及任何CSS能控制的属性。'},
    //     {a:'人才',b:'2017-12-11',c:'231',d:'百度',e:'一个字体文件包含了所有图标。Font Awesome 助你完整表达web页面上每个动作的含义。'},
    //     {a:'历史',b:'2018-07-03',c:'231',d:'知乎',e:'Font Awesome 中包含的都是矢量图标，在高分辨率的显示器上也能完美呈现。'},
    //     {a:'诈骗',b:'2016-11-08',c:'231',d:'facebook',e:'Font Awesome是完全从头设计的整套图标，完全和Bootstrap 2.2.2版本兼容.'},
    //     {a:'非法',b:'2018-02-03',c:'231',d:'twitter',e:'虽然增加了 16% 的图标，3.0 版本的体积却变得更小了。 Font Awesome 还可以定制，将你不需要的图标去掉。'},
    //     {a:'大学生',b:'2014-02-23',c:'231',d:'人人网',e:'Font Awesome supports IE7. If you need it, you have my condolences.'},
    //     {a:'维权',b:'2017-05-03',c:'231',d:',stockflow',e:'用CSS能非常容易的改变这些图标的颜色、大小、阴影以及任何CSS能控制的属性。'},
    // ]
    // function tables(data) {
    //     $('#tableContent').bootstrapTable('load', data);
    //     $('#tableContent').bootstrapTable({
    //         data:data,
    //         search: true,//是否搜索
    //         pagination: true,//是否分页
    //         pageSize: 5,//单页记录数
    //         pageList: [15,20,25],//分页步进值
    //         sidePagination: "client",//服务端分页
    //         searchAlign: "left",
    //         searchOnEnterKey: false,//回车搜索
    //         showRefresh: false,//刷新按钮
    //         showColumns: false,//列选择按钮
    //         buttonsAlign: "right",//按钮对齐方式
    //         locale: "zh-CN",//中文支持
    //         detailView: false,
    //         showToggle:false,
    //         sortName:'bci',
    //         sortOrder:"desc",
    //         columns: [
    //             {
    //                 title: "",//标题
    //                 field: "",//键名
    //                 sortable: true,//是否可排序
    //                 order: "desc",//默认排序方式
    //                 align: "center",//水平
    //                 valign: "middle",//垂直
    //                 formatter: function (value, row, index) {
    //                     var str=
    //                         '<div class="inforContent" style="text-align: left;">'+
    //                         '    <div class="main">'+
    //                         '    <img src="/static/images/textIcon.png" class="textFlag" style="top:8px;">'+
    //                         '    <p class="option">'+
    //                         '       <span>热点新词：<b style="color: #ff6d70">'+row.a+'</b></span>'+
    //                         '       <span>发布时间：<b style="color: #ff6d70">'+row.b+'</b></span>'+
    //                         '       <span>评论数：<b style="color: #ff6d70">'+row.c+'</b></span>'+
    //                         '       <span>渠道：<b style="color: #ff6d70">'+row.d+'</b></span>'+
    //                         '       <button class="originalbtn btn-primary btn-xs">查看原文</button>'+
    //                         '    </p>'+
    //                         '    <p class="context">'+ row.e+'</p>'+
    //                         '</div>'+
    //                         '</div>';
    //                     return str;
    //                 }
    //             },
    //         ],
    //     });
    // };
    // tables(obj);

    // function line_1() {
    //     var myChart = echarts.init(document.getElementById('analysis'),'chalk');
    //     var option = {
    //         backgroundColor:'transparent',
    //         tooltip: {
    //             trigger: 'axis',
    //             axisPointer: {
    //                 lineStyle: {
    //                     color: '#57617B'
    //                 }
    //             }
    //         },
    //         grid: {
    //             left: '4%',
    //             right: '7%',
    //             bottom: '8%',
    //             top:'4%',
    //             containLabel: true
    //         },
    //         xAxis: [{
    //             type: 'category',
    //             boundaryGap: false,
    //             axisLine: {
    //                 lineStyle: {
    //                     color: '#fff',
    //                     width:'2'
    //                 }
    //             },
    //             axisLabel: {
    //                 textStyle: {
    //                     color: '#fff',
    //                     fontWeight:'700'
    //                 }
    //             },
    //             data: ['周一','周二','周三','周四','周五','周六','周日'],
    //         }],
    //         yAxis: [{
    //             name:'热度',
    //             type: 'value',
    //             axisTick: {
    //                 show: false
    //             },
    //             axisLine: {
    //                 lineStyle: {
    //                     color: '#fff',
    //                     width:'2'
    //                 }
    //             },
    //             axisLabel: {
    //                 margin: 10,
    //                 textStyle: {
    //                     fontSize: 14,
    //                     fontWeight:'700',
    //                     color:'white',
    //                 }
    //             },
    //             splitLine: {
    //                 lineStyle: {
    //                     color: '#57617B'
    //                 }
    //             }
    //         }],
    //         series: [
    //             {
    //                 name: '',
    //                 type: 'line',
    //                 smooth: true,
    //                 symbol: 'circle',
    //                 symbolSize: 5,
    //                 showSymbol: false,
    //                 lineStyle: {
    //                     normal: {
    //                         width: 1,
    //                     }
    //                 },
    //                 areaStyle: {
    //                     normal: {
    //                         color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
    //                             offset: 0,
    //                             color: 'rgba(137, 189, 27, 0.8)'
    //                         }, {
    //                             offset: 1,
    //                             color: 'rgba(137, 189, 27, 0)'
    //                         }], false),
    //                         shadowColor: 'rgba(0, 0, 0, 0.1)',
    //                         shadowBlur: 10
    //                     }
    //                 },
    //                 itemStyle: {
    //                     normal: {
    //                         color: 'rgb(137,189,27)',
    //                         borderColor: 'rgba(137,189,2,0.27)',
    //                         borderWidth: 12
    //                     }
    //                 },
    //                 data: [11, 11, 15, 13, 12, 13, 10],
    //             }
    //         ]
    //     };
    //     myChart.setOption(option);
    // }
    // line_1();


    // // 鱼骨图
    // //
    //     var fish=[['','人民网','2017-11-11 11:11'],
    //         ['','中国经济','2018-01-11 10:11'],
    //         ['','京东金融','2018-01-11 10:11'],
    //         ['','263财富网','2017-08-03 09:11'],
    //         ['','网易财经','2017-08-03 09:11'],
    //         ['','新浪财经','2016-12-11 13:33'],
    //         ['','中证网','2018-11-11 11:11'],
    //         ['','搜狐新闻','2018-11-11 11:11'],
    //     ]
    //     function spread_pie_3(data){
    //         var finshdata = '';
    //         $.each(data,function (index,item) {
    //             if (index%2 == 0){
    //                 finshdata+=
    //                     '<div class="fish_item">'+
    //                     '   <ul class="top">'+
    //                     // '       <li class="weibo" title="'+item[0]+'" style="border-left: 1px solid rgb(248, 151, 130);">事件ID：'+item[0]+'</li>'+
    //                     '       <li class="weibo" title="'+item[1]+'" style="height: 86px;white-space: normal;border-left: 1px solid rgb(248, 151, 130);">公司：'+item[1]+'</li>'+
    //                     '       <li class="weibo" title="'+item[2]+'" style="border-left: 1px solid rgb(248, 151, 130);">时间：'+item[2]+'</li>'+
    //                     '       <li class="line-last line-point" style="background-position: 0 0;"></li>'+
    //                     '   </ul>'+
    //                     '</div>';
    //             }else {
    //                 finshdata+=
    //                     '<div class="fish_item" style="top: 1.22rem;">'+
    //                     '   <ul class="bottom">'+
    //                     // '       <li class="weibo" title="'+item[0]+'" style="border-left: 1px solid rgb(26, 132, 206);">事件ID：'+item[0]+'</li>'+
    //                     '       <li class="weibo" title="'+item[1]+'" style="height:0.86rem;white-space: normal;border-left: 1px solid rgb(26, 132, 206);">公司：'+item[1]+'</li>'+
    //                     '       <li class="weibo" title="'+item[2]+'" style="border-left: 1px solid rgb(26, 132, 206);">时间：'+item[2]+'</li>'+
    //                     '       <li class="line-last line-point" style="background-position: 0 -20px;"></li>'+
    //                     '   </ul>'+
    //                     '</div>';
    //             }
    //         })
    //         $(".fishBone .fish_box").append(finshdata);
    //         var _p=0;
    //         var fish_length=data.length;
    //         $('#container .fishBone .fish_box').width(fish_length*320);
    //         var fish_width=fish_length*180;
    //         $('#container .fishBone .prev').on('click',function () {
    //             _p+=180;
    //             if (fish_length<=5){
    //                 alert('没有其他卡片内容了。');
    //             }else {
    //                 var fishbone=$(".fishBone .fish_box");
    //                 var step1=_p;
    //                 if (step1 > 0 ){
    //                     alert('没有其他内容了。');
    //                     _p=0;
    //                 }else {
    //                     $(fishbone).css({
    //                         "-webkit-transform":"translateX("+step1+"px)",
    //                         "-moz-transform":"translateX("+step1+"px)",
    //                         "-ms-transform":"translateX("+step1+"px)",
    //                         "-o-transform":"translateX("+step1+"px)",
    //                         "transform":"translateX("+step1+"px)",
    //                     });
    //                 }
    //             }
    //         });
    //         $('#container .fishBone .next').on('click',function () {
    //             _p-=180;
    //             if (fish_length<=5){
    //                 alert('没有其他卡片内容了。');
    //             }else {
    //                 var step2=_p;
    //                 var fishbone=$(".fishBone .fish_box");
    //                 if (step2 <= (-fish_width+900)){
    //                     alert('没有其他内容了');
    //                     _p=-180;
    //                 }else {
    //                     $(fishbone).css({
    //                         "-webkit-transform":"translateX("+step2+"px)",
    //                         "-moz-transform":"translateX("+step2+"px)",
    //                         "-ms-transform":"translateX("+step2+"px)",
    //                         "-o-transform":"translateX("+step2+"px)",
    //                         "transform":"translateX("+step2+"px)",
    //                     });
    //                 };
    //             }
    //         });
    //     }
    //     spread_pie_3(fish);


    // // 字符云
    //     // function createRandomItemStyle() {
    //     //     return {
    //     //         normal: {
    //     //             color: 'rgb(' + [
    //     //                 Math.round(Math.random() * 160),
    //     //                 Math.round(Math.random() * 160),
    //     //                 Math.round(Math.random() * 160)
    //     //             ].join(',') + ')'
    //     //         }
    //     //     };
    //     // }

    //     require.config({
    //         paths: {
    //             echarts: '/static/js/echarts-2/build/dist',
    //         }
    //     });
    //     function keywords() {
    //         require(
    //             [
    //                 'echarts',
    //                 'echarts/chart/wordCloud'
    //             ],
    //             //关键词
    //             function (ec) {
    //                 // 基于准备好的dom，初始化echarts图表
    //                 var myChart = ec.init(document.getElementById('word-cloud'),'chalk');
    //                 var option = {
    //                     title: {
    //                         text: '',
    //                     },
    //                     tooltip: {
    //                         show: true,
    //                     },
    //                     series: [{
    //                         type: 'wordCloud',
    //                         size: ['100%', '90%','100%','90%','100%','20%','10%','20%'],
    //                         textRotation : [0, 45, 90, -45],
    //                         textPadding: 0,
    //                         autoSize: {
    //                             // enable: true,
    //                             // minSize: 18
    //                         },
    //                         data: [
    //                             {
    //                                 name: "我要金蛋",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "屹农金服",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "理财去",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "联投银帮",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "弘信宝",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "网惠金融",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "晶行财富",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "孺牛金服",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "摩根浦捷贷",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "知屋理财",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "沪臣地方金融",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "升隆财富",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "冰融贷",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "靠谱鸟",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "速溶360",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "存米网",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                             {
    //                                 name: "太保金服",
    //                                 value: 999,
    //                                 itemStyle: createRandomItemStyle()
    //                             },
    //                         ]
    //                     }]
    //                 };
    //                 myChart.setOption(option);
    //             }
    //         );
    //     }
    //     keywords();

    // // 纵向时间轴







