require.config({
    paths: {
        echarts: '../static/js/echarts-2/build/dist',
    }
});
var industry=['农、林、牧、渔业','采掘业','制造业','电力、煤气及水的生产和供应业',
    '建筑业','交通运输、仓储业','信息技术业','批发和零售贸易','金融、保险业',
    '房地产业','社会服务业','传播与文化产业','综合类'];
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
        right: '7%',
        bottom: '8%',
        top:'4%',
        containLabel: true
    },
    xAxis: [{
        type: 'category',
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
            data: ['金融监管机构','金融机构','特定企业','财经门户','财经媒体','自媒体']
        },
        series : [
            {
                name: '',
                type: 'pie',
                radius : '55%',
                center: ['65%', '50%'],
                data: [
                    {value:768, name:'金融监管机构'},
                    {value:453, name:'金融机构'},
                    {value:1548, name:'特定企业'},
                    {value:908, name:'财经门户'},
                    {value:555, name:'财经媒体'},
                    {value:1233, name:'自媒体'},
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

function bar_2() {
    var myChart = echarts.init(document.getElementById('picChart-4'),'chalk');
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
            top:'20%',
            containLabel: true
        },
        calculable : true,
        itemStyle:{
            normal:{
                // color:'rgba(198, 229, 121, 0.91)'
                color:'#C6E579'
            }
        },
        xAxis : [
            {
                name:'行业',
                type : 'category',
                nameRotate: '-90',
                nameLocation:'end',
                data : industry,
                // axisLabel:{
                //     interval:0,
                //     rotate:90,//倾斜度 -90 至 90 默认为0
                //     margin:2,
                //     textStyle:{
                //         fontSize:8
                //     }
                // },
            }
        ],
        yAxis : [
            {
                name:'影响数量',
                type : 'value'
            }
        ],
        series : [
            {
                name:'行业数量',
                type:'bar',
                data:[2, 4, 7, 8, 11, 8, 5, 6,8,22,9,15,18],
            }
        ]
    };
    myChart.setOption(option);
}
bar_2();

function keywords() {
    require(
        [
            'echarts',
            'echarts/chart/wordCloud'
        ],
        //关键词
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('picChart-5'),'chalk');
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
            top:'20%',
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
                data:[34, 54, 66, 33, 123, 65, 44 ],
            }
        ]
    };
    myChart.setOption(option);
}
bar_4();

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