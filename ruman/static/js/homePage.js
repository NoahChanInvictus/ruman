
$('#nav').css('height',$('#nav').outerHeight());//防止 nav高度抖动

var gridTop = '20%';//echarts图适配
if(screen.width<1920){
    $('#container .picChart-2, #container .picChart-3, #container .picChart-4, #container .picChart-5, #container .picChart-6, #container .picChart-7').css('height','1.4rem');
    $('#container .left_mid, #container .right_mid').css('top','2.7rem');
    gridTop = '25%';
}else {
    // 1920 * 1080 分辨率
    $('#container .picChart-2, #container .picChart-3, #container .picChart-4, #container .picChart-5, #container .picChart-6, #container .picChart-7').css('height','1.5rem');
    $('#container .left_mid, #container .right_mid').css('top','2.8rem');
    gridTop = '20%';
}

require.config({
    paths: {
        echarts: '/static/js/echarts-2/build/dist',
    }
});
var industry=['农、林、牧、渔业','采掘业','制造业','电力、煤气及水的生产和供应业',
    '建筑业','交通运输、仓储业','信息技术业','批发和零售贸易','金融、保险业',
    '房地产业','社会服务业','传播与文化产业','综合类'];

// 左上 谣言态势
    //一个月时间
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
    var day30Data=[];
    for (var b=0;b< 30;b++){
        day30Data.push(Math.round(Math.random()*(20-5)+5));
    }

    var option = {
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
            right: '10%',
            bottom: '8%',
            // top:'20%',
            top: gridTop,
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            name:'时间',
            nameRotate:'-90',
            nameTextStyle:{
                color:'#fff'
            },
            boundaryGap: false,
            axisLine: {
                lineStyle: {
                    color: '#57617B'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#fff',
                }
            },
            data: day30.reverse(),
        }],
        yAxis: [{
            type: 'value',
            name:'数目',
            nameTextStyle:{
                color:'#fff'
            },
            axisTick: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    color: '#57c4d3'
                }
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 14,
                    color:'white',
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
                data: day30Data,
            }
        ]
    };
    function line() {
        var myChart = echarts.init(document.getElementById('picChart-2'));
        myChart.setOption(option);
    }
    line();

// 左中 热点信息源分布
    function pie_1() {
        var myChart = echarts.init(document.getElementById('picChart-3'),'chalk');
        var option = {
            backgroundColor:'transparent',
            title : {
                text: '',
                subtext: '',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            grid: {
                left: '4%',
                right: '0%',
                bottom: '0%',
                top:'0%',
                containLabel: true
            },
            legend: {
                type: 'scroll',
                orient: 'vertical',
                left:0,
                top:0,
                pagemode: true,
                textStyle: {
                    fontWeight: 'bolder',
                    fontSize: 12,
                    color:'#fff'
                },
                pageIconColor: '#fff',
                pageIconInactiveColor: '#fff',
                pageTextStyle:{color:'#fff'},
                padding: 6,
                data: ['微博','论坛','知乎','App','新闻']
            },
            series : [
                {
                    name: '',
                    type: 'pie',
                    radius : '55%',
                    center: ['65%', '50%'],
                    data: [
                        {value:768, name:'微博'},
                        {value:453, name:'论坛'},
                        {value:1548, name:'知乎'},
                        {value:Math.round(Math.random()*1000), name:'App'},
                        {value:Math.round(Math.random()*1000), name:'新闻'},
                    ],
                    label:{
                        normal:{
                            show:true,
                            // position:'inner',
                            formatter: "{d}%",
                            // textStyle: {
                            //     fontSize : '12',
                            //     color:'#006a86'
                            // }
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
        myChart.setOption(option);
    }
    pie_1();

// 右上 气泡图 热点事件
    function bar_2() {
        var myChart = echarts.init(document.getElementById('picChart-5'),'chalk');
        var data = [
            [[28604,77,17096869,'Australia',1990],[31163,77.4,27662440,'Canada',1990],[1516,68,1154605773,'China',1990],[13670,74.7,10582082,'Cuba',1990],[28599,75,4986705,'Finland',1990],[29476,77.1,56943299,'France',1990],[31476,75.4,78958237,'Germany',1990],[28666,78.1,254830,'Iceland',1990],[1777,57.7,870601776,'India',1990],[29550,79.1,122249285,'Japan',1990],[2076,67.9,20194354,'North Korea',1990],[12087,72,42972254,'South Korea',1990],[24021,75.4,3397534,'New Zealand',1990],[43296,76.8,4240375,'Norway',1990],[10088,70.8,38195258,'Poland',1990],[19349,69.6,147568552,'Russia',1990],[10670,67.3,53994605,'Turkey',1990],[26424,75.7,57110117,'United Kingdom',1990],[37062,75.4,252847810,'United States',1990]],
            [[44056,81.8,23968973,'Australia',2015],[43294,81.7,35939927,'Canada',2015],[13334,76.9,1376048943,'China',2015],[21291,78.5,11389562,'Cuba',2015],[38923,80.8,5503457,'Finland',2015],[37599,81.9,64395345,'France',2015],[44053,81.1,80688545,'Germany',2015],[42182,82.8,329425,'Iceland',2015],[5903,66.8,1311050527,'India',2015],[36162,83.5,126573481,'Japan',2015],[1390,71.4,25155317,'North Korea',2015],[34644,80.7,50293439,'South Korea',2015],[34186,80.6,4528526,'New Zealand',2015],[64304,81.6,5210967,'Norway',2015],[24787,77.3,38611794,'Poland',2015],[23038,73.13,143456918,'Russia',2015],[19360,76.5,78665830,'Turkey',2015],[38225,81.4,64715810,'United Kingdom',2015],[53354,79.1,321773631,'United States',2015]]
        ];
        var option = {
            backgroundColor:'transparent',
            grid: {
                left: '4%',
                right: '15%',
                bottom: '4%',
                // top:'20%',
                top: gridTop,
                containLabel: true
            },
            xAxis: {
                name:'评论数',
                nameRotate:'-90',
                nameGap:25,//坐标轴名称与轴线之间的距离。
                splitLine: {
                    lineStyle: {
                        type: 'dashed'
                    }
                }
            },
            yAxis: {
                name:'转发数',
                splitLine: {
                    lineStyle: {
                        type: 'dashed'
                    }
                },
                scale: true
            },
            series: [
                {
                name: '',
                data: data[0],
                type: 'scatter',
                symbolSize: function (data) {
                    return Math.sqrt(data[2]) / 5e2/2;
                },
                label: {
                    emphasis: {
                        show: true,
                        formatter: function (param) {
                            return param.data[3];
                        },
                        position: 'top'
                    }
                },
                itemStyle: {
                    normal: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(120, 36, 50, 0.5)',
                        shadowOffsetY: 5,
                        color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
                            offset: 0,
                            color: 'rgb(251, 118, 123)'
                        }, {
                            offset: 1,
                            color: 'rgb(204, 46, 72)'
                        }])
                    }
                }
            },
                ]
        };
        myChart.setOption(option);
    }
    bar_2();

// 左下 热点词图
    function keywords() {
        require(
            [
                'echarts',
                'echarts/chart/wordCloud'
            ],
            //关键词
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var myChart = ec.init(document.getElementById('picChart-4'),'chalk');
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

// 右中 操纵态势
    function bar_4() {
        var myChart = echarts.init(document.getElementById('picChart-6'),'chalk');
        var option = {
            backgroundColor:'transparent',
            title: {
                text: '',
                subtext: ''
            },
            tooltip : {
                trigger: 'axis'
            },
            grid: {
                left: '0%',
                right: '10%',
                bottom: '0%',
                // top:'20%',
                top: gridTop,
                containLabel: true
            },
            legend: {
                data:['行业','预警']
            },
            calculable : true,
            itemStyle:{
                normal:{
                    // color:'rgba(198, 229, 121, 0.91)'
                    color:'#f6a38e'
                }
            },
            xAxis : [
                {
                    name:'行业',
                    type : 'category',
                    nameRotate: '-90',
                    nameLocation:'end',
                    data : ['化工','军工','房地产','医疗','媒体','批发','消费品']
                }
            ],
            yAxis : [
                {
                    name:'数量',
                    type : 'value'
                }
            ],
            series : [
                {
                    name:'',
                    type:'bar',
                    data:[21, 44, 77, 32, 111, 82, 56 ],
                },
                {
                    name:'',
                    type:'line',
                    lineStyle:{
                        normal:{color:'#87f7cf'}
                    },
                    data:[21, 44, 77, 32, 111, 82, 56 ],
                }
            ]
        };
        myChart.setOption(option);
    }
    bar_4();
// 右下 操纵板块分布
    function pie_2() {
        var myChart = echarts.init(document.getElementById('picChart-7'),'chalk');
        var option = {
            backgroundColor:'transparent',
            title : {
                text: '',
                subtext: '',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                type: 'scroll',
                orient: 'vertical',
                left:0,
                top:0,
                pagemode: true,
                textStyle: {
                    fontWeight: 'bolder',
                    fontSize: 12,
                    color:'#fff'
                },
                pageIconColor: '#fff',
                pageIconInactiveColor: '#fff',
                pageTextStyle:{color:'#fff'},
                padding: 6,
                data: ['主板','创业板','中小板']
            },
            series : [
                {
                    name: '',
                    type: 'pie',
                    radius : '55%',
                    center: ['65%', '50%'],
                    data: [
                        {value:768, name:'主板'},
                        {value:453, name:'创业板'},
                        {value:1548, name:'中小板'},
                    ],
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
        myChart.setOption(option);
    }
    pie_2();
//-----------------滚动----
//获得当前
var $uList = $("#scroll");
var timer = null;
//触摸清空定时器
$uList.hover(function() {
        clearInterval(timer);
    },
    function() { //离开启动定时器
        timer = setInterval(function() {
            scrollList($uList);
        }, 1000);
    }).trigger("mouseleave"); //自动触发触摸事件
//滚动动画
function scrollList(obj) {
    //获得当前<li>的高度
    var scrollHeight = $("#scroll p:first").height();
    //滚动出一个<li>的高度
    $uList.stop().animate({
            marginTop: -scrollHeight
        },
        600,
        function() {
            //动画结束后，将当前marginTop置为初始值0状态，再将第一个<li>拼接到末尾。
            $uList.css({
                marginTop: 0
            }).find("p:first").remove().appendTo($uList);
        });
}
//滚动终止--