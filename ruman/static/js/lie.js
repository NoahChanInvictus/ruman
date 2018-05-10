
// 演化分析
    function get7DaysBefore(date,m){
        var date = date || new Date(),
            timestamp, newDate;
        if(!(date instanceof Date)){
            date = new Date(date);
        }
        timestamp = date.getTime();
        newDate = new Date(timestamp - m * 24 * 3600 * 1000);
        return [newDate.getFullYear(), newDate.getMonth() + 1, newDate.getDate()].join('-');
    };
    var day30=[];
    for (var a=0;a < 30;a++){
        day30.push(get7DaysBefore(new Date(),a));
    }
    var day30Data1=[];
    for (var b=0;b<30;b++){
        day30Data1.push(Math.round(Math.random()*(20-5)+5));
    }
    var day30Data2=[];
    for (var c=0;c<30;c++){
        day30Data2.push(Math.round(Math.random()*(20-3)));
    }
    var option,tit;
    function _option(ytit,dd) {
        option = {
            backgroundColor:'transparent',
            title: {
                text: tit,
                x:'center',
                textStyle:{
                    // color:'#fff'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        // color: '#30c7ff'
                    }
                }
            },
            grid: {
                left: '3%',
                right: '3%',
                bottom: '0%',
                top:'6%',
                // width:'80%',
                containLabel: true
            },
            xAxis: [{
                name:'时间',
                type: 'category',
                boundaryGap: false,
                axisLine: {
                    lineStyle: {
                        // color: '#fff'
                    }
                },
                axisLabel: {
                    textStyle: {
                        // color: '#fff',
                    }
                },
                data: day30.reverse(),
            }],
            yAxis: {
                name:ytit,
                type: 'value',
                axisLine: {
                    lineStyle: {
                        // color: '#fff'
                    }
                },
                nameTextStyle:{
                    // color:'#fff'
                },
                splitLine:{
                    show:false
                }
            },
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
                    // areaStyle: {
                    //     normal: {
                    //         // color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    //         //     offset: 0,
                    //         //     color: 'rgba(137, 189, 27, 0.8)'
                    //         // }, {
                    //         //     offset: 1,
                    //         //     color: 'rgba(137, 189, 27, 0.2)'
                    //         // }], false),
                    //         // shadowColor: 'rgba(0, 0, 0, 0.1)',
                    //         // shadowBlur: 10
                    //     }
                    // },
                    // itemStyle: {
                    //     normal: {
                    //         color: 'rgb(137,189,27)',
                    //         borderColor: 'rgba(137,189,2,0.27)',
                    //         borderWidth: 12
                    //     }
                    // },
                    data: dd,
                }
            ]
        };
    };
    function line_1() {
        tit='热度演化曲线图';
        var myChart = echarts.init(document.getElementById('evolution-chat-1'));
        myChart.showLoading();

        _option('热度',day30Data1);

        myChart.hideLoading();
        myChart.setOption(option);
    }

    line_1();

    function line_2() {
        tit='情绪演化曲线图';
        var myChart = echarts.init(document.getElementById('evolution-chat-2'));
        myChart.showLoading();

        _option('情绪',day30Data2);

        myChart.hideLoading();
        myChart.setOption(option);
    }
    line_2();
    // $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    //     // 获取已激活的标签页的名称
    //     var activeTab = $(e.target).text();
    //     // 获取前一个激活的标签页的名称
    //     var previousTab = $(e.relatedTarget).text();
    //     // $(".active-tab span").html(activeTab);
    //     // $(".previous-tab span").html(previousTab);
    //     console.log(activeTab);
    //     if(activeTab){
    //         console.log(activeTab);
    //     }
    //     console.log(activeTab);
    // });


// 语义分析
    // 观点聚类
        var ViewpointData = [
            {num:1,a:'正面',Percentage:'30%',title_1:'独狼行动',title_2:'资本有方',title_3:'张百忍',con_1:'计划经济正式回归',con_2:'水泥先行！冀东先行',con_3:'不错，跟上形势'},
            {num:2,a:'负面',Percentage:'60%',title_1:'悟空说他很傻',title_2:'谁吾与从001',title_3:'ICE__XU',con_1:'搞来搞去还是只有搞地产',con_2:'抵制万科，不买它的任何产品',con_3:'野鸡新闻'},
            {num:3,a:'正面',Percentage:'30%',title_1:'独狼行动',title_2:'资本有方',title_3:'张百忍',con_1:'计划经济正式回归',con_2:'水泥先行！冀东先行',con_3:'不错，跟上形势'},
            {num:4,a:'负面',Percentage:'60%',title_1:'独狼行动',title_2:'资本有方',title_3:'张百忍',con_1:'计划经济正式回归',con_2:'水泥先行！冀东先行',con_3:'不错，跟上形势'}
        ];
        function Viewpoint(data){
            $('#Viewpoint-clustering').bootstrapTable('load', data);
            $('#Viewpoint-clustering').bootstrapTable({
                data:data,
                search: false,//是否搜索
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
                            return '<div class="inforContent">'+
                                '<div class="main">'+
                                '<p class="option">'+
                                '<span>观点<b>'+row.num+'</b></span>'+
                                '<span style="margin:0 10px;"><b>'+row.a+'</b></span>'+
                                '<span><b>'+row.Percentage+'</b></span>'+
                                '<span class="moreInfo">查看更多</span>'+
                                '</p>'+
                                '<div class="context">'+
                                '<p style="margin:10px 0;"><span style="font-weight: 700;color:#1f4e79;"><img src="/static/images/textIcon.png" class="textFlag" style="top: 8px;margin-right:5px;">'+row.title_1+':</span><span>'+row.con_1+'</span></p>'+
                                '<p style="margin:10px 0;"><span style="font-weight: 700;color:#1f4e79;"><img src="/static/images/textIcon.png" class="textFlag" style="top: 8px;margin-right:5px;">'+row.title_2+':</span><span>'+row.con_2+'</span></p>'+
                                '<p style="margin:10px 0;"><span style="font-weight: 700;color:#1f4e79;"><img src="/static/images/textIcon.png" class="textFlag" style="top: 8px;margin-right:5px;">'+row.title_3+':</span><span>'+row.con_3+'</span></p>'+
                                '</div>'+
                                '</div>';
                        }
                    }
                ],
            });
        }
        // Viewpoint(ViewpointData);

    // 字符云
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

        // var createRandomItemStyle1 = function (params) {　　　　//此方法与下方配置中的第一个textStle下的color等同
        //     var colors = ['#fda67e', '#81cacc', '#cca8ba', "#88cc81", "#82a0c5", '#fddb7e', '#735ba1', '#bda29a', '#6e7074', '#546570', '#c4ccd3'];
        //     return colors[parseInt(Math.random() * 10)];
        // }

        require.config({
            paths: {
                echarts: '/static/js/echarts-2/build/dist',
            }
        });
        function keywords() {
            require(
                [
                    'echarts',
                    'echarts/chart/wordCloud'
                ],
                //关键词
                function (ec) {
                    // 基于准备好的dom，初始化echarts图表
                    var myChart = ec.init(document.getElementById('word-1'),'chalk');
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
                                // enable: true,
                                // minSize: 18
                            },
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
                        }]
                    };
                    myChart.setOption(option);
                }
            );
        }
        keywords();

    // 主题时间轴


// 传播分析
    function spread_pie_1(){
        var myChart = echarts.init(document.getElementById('spread-pie-1'));
        var option = {
            title : {
                text: '参与传播的媒体粉丝数分布',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'right',
                data: ['5万以下','5万-10万','10万-20万','20万-50万','50万-100万','100万以上']
            },
            series : [
                {
                    name: '媒体粉丝数分布',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '50%'],
                    data:[
                        {value:335, name:'5万以下'},
                        {value:310, name:'5万-10万'},
                        {value:234, name:'10万-20万'},
                        {value:135, name:'20万-50万'},
                        {value:1350, name:'50万-100万'},
                        {value:1548, name:'100万以上'},
                    ],
                    label: {
                        normal:{
                            show: true,
                            // position:'inner',
                            formatter: "{d}%",
                            textStyle: {
                                fontWeight:'bolder',
                                // fontSize : '12',
                                // color:'#fff'
                            }
                        }
                    },
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option)
    }
    // spread_pie_1();
    function spread_pie_2(){
        var myChart = echarts.init(document.getElementById('spread-pie-2'));
        var option = {
            title : {
                text: '参与传播的个人粉丝数分布',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'right',
                data: ['5万以下','5万-10万','10万-20万','20万-50万','50万-100万','100万以上']
            },
            series : [
                {
                    name: '个人粉丝数分布',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '50%'],
                    data:[
                        {value:335, name:'5万以下'},
                        {value:310, name:'5万-10万'},
                        {value:234, name:'10万-20万'},
                        {value:135, name:'20万-50万'},
                        {value:1350, name:'50万-100万'},
                        {value:1548, name:'100万以上'}
                    ],
                    label: {
                        normal:{
                            show: true,
                            // position:'inner',
                            formatter: "{d}%",
                            textStyle: {
                                fontWeight:'bolder',
                                // fontSize : '12',
                                // color:'#fff'
                            }
                        }
                    },
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option)
    }
    // spread_pie_2();




    // 鱼骨图
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
            // $('#container .fishBone .fish_box').width(fish_length*180);
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
        spread_pie_3(fish);

// 影响分析
// 波及人数
function influncePerson(){
    var myChart = echarts.init(document.getElementById('influnce_person'));
    var option = {
        title: {
            text:'',
            left:'center'
        },
        tooltip: {
            trigger: 'axis',
            // formatter: "Temperature : <br/>{b}km : {c}°C"
            formatter: "疑似谣言波及人数 : <br/>{c}"
        },
        grid: {
            top: '8%',
            left: '0%',
            right: '8%',
            bottom: '0%',
            containLabel: true
        },
        xAxis: {
            name:'传播时间',
            type: 'category',
            axisLabel:{
                interval:0,
                rotate:90,//倾斜度 -90 至 90 默认为0
                margin:2,
                textStyle:{
                    fontSize:8
                }
            },
            data: ['0.00', '1.00', '2.00', '3.00', '4.00', '5.00', '6.00', '7.00', '8.00','9.00', '10.00','11.00' ,'12.00', '13.00', '14.00', '15.00', '16.00', '17.00', '18.00','19.00','20.00','21.00', '22.00', '23.00', '24.00','0.00']
        },
        yAxis: {
            name:'波及人数',
            type: 'value',
            // axisLine: {onZero: false},
            axisLabel: {
                // formatter: '{value} km'
            },
            boundaryGap: false,
            // data: ['0', '10', '20', '30', '40', '50', '60', '70', '80']
        },
        series: [
            {
                name: '疑似谣言波及人数',
                type: 'line',
                smooth: true,
                lineStyle: {
                    normal: {
                        width: 3,
                        shadowColor: 'rgba(0,0,0,0.4)',
                        shadowBlur: 10,
                        shadowOffsetY: 10
                    }
                },
                data:[100,200,400,444,555,666,777,888,999,1000,1230,1500,1622,1674,1689,1755,1800,1900,2007,2500,2600,3000,3100,3232,]
            }
        ]
    };
    myChart.setOption(option)
}
influncePerson();
// 市场关联
function influnceMarket(){
    var myChart = echarts.init(document.getElementById('influnce_market'));
    var upColor = '#ec0000';
    var upBorderColor = '#8A0000';
    var downColor = '#00da3c';
    var downBorderColor = '#008F28';

    // 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
    var data0 = splitData([
        ['2013/1/24', 2320.26,2320.26,2287.3,2362.94],
        ['2013/1/25', 2300,2291.3,2288.26,2308.38],
        ['2013/1/28', 2295.35,2346.5,2295.35,2346.92],
        ['2013/1/29', 2347.22,2358.98,2337.35,2363.8],
        ['2013/1/30', 2360.75,2382.48,2347.89,2383.76],
        ['2013/1/31', 2383.43,2385.42,2371.23,2391.82],
        ['2013/2/1', 2377.41,2419.02,2369.57,2421.15],
        ['2013/2/4', 2425.92,2428.15,2417.58,2440.38],
        ['2013/2/5', 2411,2433.13,2403.3,2437.42],
        ['2013/2/6', 2432.68,2434.48,2427.7,2441.73],
        ['2013/2/7', 2430.69,2418.53,2394.22,2433.89],
        ['2013/2/8', 2416.62,2432.4,2414.4,2443.03],
        ['2013/2/18', 2441.91,2421.56,2415.43,2444.8],
        ['2013/2/19', 2420.26,2382.91,2373.53,2427.07],
        ['2013/2/20', 2383.49,2397.18,2370.61,2397.94],
        ['2013/2/21', 2378.82,2325.95,2309.17,2378.82],
        ['2013/2/22', 2322.94,2314.16,2308.76,2330.88],
        ['2013/2/25', 2320.62,2325.82,2315.01,2338.78],
        ['2013/2/26', 2313.74,2293.34,2289.89,2340.71],
        ['2013/2/27', 2297.77,2313.22,2292.03,2324.63],
        ['2013/2/28', 2322.32,2365.59,2308.92,2366.16],
        ['2013/3/1', 2364.54,2359.51,2330.86,2369.65],
        ['2013/3/4', 2332.08,2273.4,2259.25,2333.54],
        ['2013/3/5', 2274.81,2326.31,2270.1,2328.14],
        ['2013/3/6', 2333.61,2347.18,2321.6,2351.44],
        ['2013/3/7', 2340.44,2324.29,2304.27,2352.02],
        ['2013/3/8', 2326.42,2318.61,2314.59,2333.67],
        ['2013/3/11', 2314.68,2310.59,2296.58,2320.96],
        ['2013/3/12', 2309.16,2286.6,2264.83,2333.29],
        ['2013/3/13', 2282.17,2263.97,2253.25,2286.33],
        ['2013/3/14', 2255.77,2270.28,2253.31,2276.22],
        ['2013/3/15', 2269.31,2278.4,2250,2312.08],
        ['2013/3/18', 2267.29,2240.02,2239.21,2276.05],
        ['2013/3/19', 2244.26,2257.43,2232.02,2261.31],
        ['2013/3/20', 2257.74,2317.37,2257.42,2317.86],
        ['2013/3/21', 2318.21,2324.24,2311.6,2330.81],
        ['2013/3/22', 2321.4,2328.28,2314.97,2332],
        ['2013/3/25', 2334.74,2326.72,2319.91,2344.89],
        ['2013/3/26', 2318.58,2297.67,2281.12,2319.99],
        ['2013/3/27', 2299.38,2301.26,2289,2323.48],
        ['2013/3/28', 2273.55,2236.3,2232.91,2273.55],
        ['2013/3/29', 2238.49,2236.62,2228.81,2246.87],
        ['2013/4/1', 2229.46,2234.4,2227.31,2243.95],
        ['2013/4/2', 2234.9,2227.74,2220.44,2253.42],
        ['2013/4/3', 2232.69,2225.29,2217.25,2241.34],
        ['2013/4/8', 2196.24,2211.59,2180.67,2212.59],
        ['2013/4/9', 2215.47,2225.77,2215.47,2234.73],
        ['2013/4/10', 2224.93,2226.13,2212.56,2233.04],
        ['2013/4/11', 2236.98,2219.55,2217.26,2242.48],
        ['2013/4/12', 2218.09,2206.78,2204.44,2226.26],
        ['2013/4/15', 2199.91,2181.94,2177.39,2204.99],
        ['2013/4/16', 2169.63,2194.85,2165.78,2196.43],
        ['2013/4/17', 2195.03,2193.8,2178.47,2197.51],
        ['2013/4/18', 2181.82,2197.6,2175.44,2206.03],
        ['2013/4/19', 2201.12,2244.64,2200.58,2250.11],
        ['2013/4/22', 2236.4,2242.17,2232.26,2245.12],
        ['2013/4/23', 2242.62,2184.54,2182.81,2242.62],
        ['2013/4/24', 2187.35,2218.32,2184.11,2226.12],
        ['2013/4/25', 2213.19,2199.31,2191.85,2224.63],
        ['2013/4/26', 2203.89,2177.91,2173.86,2210.58],
        ['2013/5/2', 2170.78,2174.12,2161.14,2179.65],
        ['2013/5/3', 2179.05,2205.5,2179.05,2222.81],
        ['2013/5/6', 2212.5,2231.17,2212.5,2236.07],
        ['2013/5/7', 2227.86,2235.57,2219.44,2240.26],
        ['2013/5/8', 2242.39,2246.3,2235.42,2255.21],
        ['2013/5/9', 2246.96,2232.97,2221.38,2247.86],
        ['2013/5/10', 2228.82,2246.83,2225.81,2247.67],
        ['2013/5/13', 2247.68,2241.92,2231.36,2250.85],
        ['2013/5/14', 2238.9,2217.01,2205.87,2239.93],
        ['2013/5/15', 2217.09,2224.8,2213.58,2225.19],
        ['2013/5/16', 2221.34,2251.81,2210.77,2252.87],
        ['2013/5/17', 2249.81,2282.87,2248.41,2288.09],
        ['2013/5/20', 2286.33,2299.99,2281.9,2309.39],
        ['2013/5/21', 2297.11,2305.11,2290.12,2305.3],
        ['2013/5/22', 2303.75,2302.4,2292.43,2314.18],
        ['2013/5/23', 2293.81,2275.67,2274.1,2304.95],
        ['2013/5/24', 2281.45,2288.53,2270.25,2292.59],
        ['2013/5/27', 2286.66,2293.08,2283.94,2301.7],
        ['2013/5/28', 2293.4,2321.32,2281.47,2322.1],
        ['2013/5/29', 2323.54,2324.02,2321.17,2334.33],
        ['2013/5/30', 2316.25,2317.75,2310.49,2325.72],
        ['2013/5/31', 2320.74,2300.59,2299.37,2325.53],
        ['2013/6/3', 2300.21,2299.25,2294.11,2313.43],
        ['2013/6/4', 2297.1,2272.42,2264.76,2297.1],
        ['2013/6/5', 2270.71,2270.93,2260.87,2276.86],
        ['2013/6/6', 2264.43,2242.11,2240.07,2266.69],
        ['2013/6/7', 2242.26,2210.9,2205.07,2250.63],
        ['2013/6/13', 2190.1,2148.35,2126.22,2190.1]
    ]);

    function splitData(rawData) {
        var categoryData = [];
        var values = []
        for (var i = 0; i < rawData.length; i++) {
            categoryData.push(rawData[i].splice(0, 1)[0]);
            values.push(rawData[i])
        }
        return {
            categoryData: categoryData,
            values: values
        };
    }

    function calculateMA(dayCount) {
        var result = [];
        for (var i = 0, len = data0.values.length; i < len; i++) {
            if (i < dayCount) {
                result.push('-');
                continue;
            }
            var sum = 0;
            for (var j = 0; j < dayCount; j++) {
                sum += data0.values[i - j][1];
            }
            result.push(sum / dayCount);
        }
        return result;
    }

    option = {
        title: {
            text: '',
            left: 0
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        grid: {
            top: '8%',
            left: '0%',
            right: '8%',
            bottom: '0%',
            containLabel: true
        },
        xAxis: {
            name:'时间',
            type: 'category',
            data: data0.categoryData,
            scale: true,
            boundaryGap : false,
            axisLine: {onZero: false,},
            splitLine: {show: false},
            splitNumber: 20,
            min: 'dataMin',
            max: 'dataMax',
            axisLabel:{
                interval:0,
                rotate:90,//倾斜度 -90 至 90 默认为0
                margin:2,
                textStyle:{
                    fontSize:8
                }
            },
        },
        yAxis: {
            name:'数值',
            scale: true,
            splitArea: {
                show: true
            }
        },
        dataZoom: [
            {
                type: 'inside',
                start: 50,
                end: 100
            },
            {
                show: true,
                type: 'slider',
                y: '90%',
                start: 50,
                end: 100
            }
        ],
        series: [
            {
                name: '日K',
                type: 'candlestick',
                data: data0.values,
                itemStyle: {
                    normal: {
                        color: upColor,
                        color0: downColor,
                        borderColor: upBorderColor,
                        borderColor0: downBorderColor
                    }
                },
                markPoint: {
                    label: {
                        normal: {
                            formatter: function (param) {
                                return param != null ? Math.round(param.value) : '';
                            }
                        }
                    },
                    data: [
                        {
                            name: 'XX标点',
                            coord: ['2013/5/31', 2300],
                            value: 2300,
                            itemStyle: {
                                normal: {color: 'rgb(41,60,85)'}
                            }
                        },
                        {
                            name: 'highest value',
                            type: 'max',
                            valueDim: 'highest'
                        },
                        {
                            name: 'lowest value',
                            type: 'min',
                            valueDim: 'lowest'
                        },
                        {
                            name: 'average value on close',
                            type: 'average',
                            valueDim: 'close'
                        }
                    ],
                    tooltip: {
                        formatter: function (param) {
                            return param.name + '<br>' + (param.data.coord || '');
                        }
                    }
                },
                markLine: {
                    symbol: ['none', 'none'],
                    data: [
                        [
                            {
                                name: 'from lowest to highest',
                                type: 'min',
                                valueDim: 'lowest',
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    normal: {show: false},
                                    emphasis: {show: false}
                                }
                            },
                            {
                                type: 'max',
                                valueDim: 'highest',
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    normal: {show: false},
                                    emphasis: {show: false}
                                }
                            }
                        ],
                        {
                            name: 'min line on close',
                            type: 'min',
                            valueDim: 'close'
                        },
                        {
                            name: 'max line on close',
                            type: 'max',
                            valueDim: 'close'
                        }
                    ]
                }
            },
            {
                name: 'MA5',
                type: 'line',
                data: calculateMA(5),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: calculateMA(10),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: calculateMA(20),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA30',
                type: 'line',
                data: calculateMA(30),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },

        ]
    };
    myChart.setOption(option)
}
influnceMarket();

// 判别原因
//
function Features(){
    var myChart = echarts.init(document.getElementById('Features'));
    var option = {
        title: {
            text: ''
        },
        tooltip: {},
        legend: {
            // data: ['预算分配（Allocated Budget）', '实际开销（Actual Spending）']
        },
        radar: {
            // shape: 'circle',
            name: {
                textStyle: {
                    color: '#fff',
                    backgroundColor: '#999',
                    borderRadius: 3,
                    padding: [3, 5]
                }
            },
            indicator: [
                { name: '质疑度', max: 60},
                { name: '发布者可疑度', max: 60},
                { name: '扩散速度', max: 60},
                { name: '波及人次', max: 60},
                { name: '评论数', max: 60},
                { name: '转发数', max: 60}
            ]
        },
        series: [{
            name: '',
            type: 'radar',
            // areaStyle: {normal: {}},
            data : [
                {
                    value : [60,15,10,50,30,40],
                    // name : '预算分配（Allocated Budget）'
                },
                //  {
                //     value : [5000, 14000, 28000, 31000, 42000, 21000],
                //     name : '实际开销（Actual Spending）'
                // }
            ]
        }]
    };
    myChart.setOption(option)
}
Features();