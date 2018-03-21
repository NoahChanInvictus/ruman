var industry=['农、林、\n牧、渔业','采掘业','制造业','电力、煤气及\n水的生产和供应业',
    '建筑业','交通运输、仓储业','信息技术业','批发和零售贸易','金融、保险业',
    '房地产业','社会服务业','传播与文化产业','综合类'];
//第一屏
    var earlyWarningdata=[
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'所长别开枪是我','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'机智达人','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'沈小司司','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源','i':'是'},
    ]
    var earlyWarning_url='';
    // public_ajax.call_request('get',earlyWarning_url,earlyWarning);
    function earlyWarning(data) {
        $('#recordingTable').bootstrapTable('load', data);
        $('#recordingTable').bootstrapTable({
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
                    title: "发布时间",//标题
                    field: "a",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.a==''||row.a=='null'||row.a=='unknown'||!row.a){
                            return '未知';
                        }else {
                            return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.a+'\')" title="进入画像">'+row.a+'</span>';
                        };
                    }
                },
                {
                    title: "疑似谣言",//标题
                    field: "b",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直

                },
                {
                    title: "发布者",//标题
                    field: "c",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "发布渠道",//标题
                    field: "d",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "评论数",//标题
                    field: "e",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直

                },
                {
                    title: "转发数",//标题
                    field: "f",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "波及人数",//标题
                    field: "g",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "波及行业",//标题
                    field: "h",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "是否辟谣",//标题
                    field: "i",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "监测详情",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1()" title="查看详情"><i class="icon icon-file-alt"></i></span>';
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
        });
    };
    earlyWarning(earlyWarningdata);
    // 跳转详情页
    function jumpFrame_1() {
        var html='/index/lieDetail';
        window.open(html);
    }


//第二屏
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
    day30Data2.push(2*c);
}
var option,tit;
function _option(ytit,dd) {
    option = {
        backgroundColor:'transparent',
        title: {
            text: tit,
            x:'center',
            textStyle:{
                color:'#fff'
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                lineStyle: {
                    color: '#30c7ff'
                }
            }
        },
        grid: {
            left: '0%',
            right: '9%',
            bottom: '0%',
            top:'6%',
            containLabel: true
        },
        xAxis: [{
            name:'时间',
            type: 'category',
            boundaryGap: false,
            axisLine: {
                lineStyle: {
                    color: '#fff'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#fff',
                }
            },
            data: day30.reverse(),
        }],
        yAxis: {
            name:ytit,
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: '#fff'
                }
            },
            nameTextStyle:{
                color:'#fff'
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
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(137, 189, 27, 0.8)'
                        }, {
                            offset: 1,
                            color: 'rgba(137, 189, 27, 0.2)'
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
                data: dd,
            }
        ]
    };
};
function line_1() {
    tit='疑似谣言预警次数';
    var myChart = echarts.init(document.getElementById('trendLine'));
    _option('次数',day30Data1);
    myChart.setOption(option);
}
line_1();
function line_2() {
    tit='疑似谣言累计人数';
    var myChart = echarts.init(document.getElementById('place'));
    _option('累计人数',day30Data2);
    myChart.setOption(option);
}
line_2();
//第3屏
function bar_1() {
    var myChart = echarts.init(document.getElementById('bar-1'),'chalk');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: '疑似谣言行业分布',
            x: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '0%',
            right: '9%',
            bottom: '0%',
            top:'6%',
            containLabel: true
        },
        yAxis: {
            name:'数量',
            type: 'value',
            boundaryGap: [0, 0.01]
        },
        xAxis: {
            name:'行业',
            type: 'category',
            // axisLabel:{
            //     interval:0,
            //     rotate:90,
            // },
            data: industry,
            axisLabel:{
                interval:0,
                rotate:90,//倾斜度 -90 至 90 默认为0
                margin:2,
                textStyle:{
                    fontSize:8
                }
            },
        },
        series: [
            {
                name: '行业数量',
                type: 'bar',
                itemStyle:{
                    normal:{color:'#2eade3'},
                },
                label: {
                    normal:{
                        show: true,
                        textStyle: {
                            fontWeight:'bolder',
                            fontSize : '12',
                            color:'#f5f5f5'
                        }
                    }
                },
                data: [132, 345, 342, 534, 199, 444, 222,234,444, 222,234,123,235],
            },

        ]
    };
    myChart.setOption(option);
}
bar_1();
//第4屏
function pie_1() {
    var myChart = echarts.init(document.getElementById('pie-1'),'chalk');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '疑似谣言发布者类别分布',
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['金融监管机构','金融机构','特定企业','财经门户','财经媒体','自媒体']
        },
        series : [
            {
                name: '发布者',
                type: 'pie',
                radius : '55%',
                center: ['50%', '50%'],
                data:[
                    {value:335, name:'金融监管机构'},
                    {value:310, name:'金融机构'},
                    {value:234, name:'特定企业'},
                    {value:135, name:'财经门户'},
                    {value:848, name:'财经媒体'},
                    {value:456, name:'自媒体'},
                ],
                label: {
                    normal:{
                        show: true,
                        // position:'inner',
                        formatter: "{b} {d}%",
                        textStyle: {
                            fontWeight:'bolder',
                            // fontSize : '12',
                            // color:'#164d8e'
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
    myChart.setOption(option);
}
pie_1();
//第6屏
require.config({
    paths: {
        echarts: '../static/js/echarts-2/build/dist',
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
                    // borderColor:'#ff1c15',
                    // borderRadius: 4,
                    // borderWidth: 2,
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
                        {
                            name: "枪击案",
                            value: 999,
                            itemStyle: createRandomItemStyle()
                        },
                        {
                            name: "庆祝",
                            value: 999,
                            itemStyle: createRandomItemStyle()
                        },
                        {
                            name: "视频",
                            value: 999,
                            itemStyle: createRandomItemStyle(),
                        },
                    ]
                }]
            };
            myChart.setOption(option);
        }
    );
}
keywords();
//第6屏
var data = [
    [[28604,77,17096869,'Australia',1990], [31163,77.4,27662440,'Canada',1990],[1516,68,1154605773,'China',1990],
        [13670,74.7,10582082,'Cuba',1990],[28599,75,4986705,'Finland',1990],[29476,77.1,56943299,'France',1990],[31476,75.4,78958237,'Germany',1990],[28666,78.1,254830,'Iceland',1990],[1777,57.7,870601776,'India',1990],[29550,79.1,122249285,'Japan',1990],[2076,67.9,20194354,'North Korea',1990],[12087,72,42972254,'South Korea',1990],[24021,75.4,3397534,'New Zealand',1990],[43296,76.8,4240375,'Norway',1990],[10088,70.8,38195258,'Poland',1990],[19349,69.6,147568552,'Russia',1990],[10670,67.3,53994605,'Turkey',1990],[26424,75.7,57110117,'United Kingdom',1990],[37062,75.4,252847810,'United States',1990]],
    [[44056,81.8,23968973,'Australia',2015],[43294,81.7,35939927,'Canada',2015],[13334,76.9,1376048943,'China',2015],[21291,78.5,11389562,'Cuba',2015],[38923,80.8,5503457,'Finland',2015],[37599,81.9,64395345,'France',2015],[44053,81.1,80688545,'Germany',2015],[42182,82.8,329425,'Iceland',2015],[5903,66.8,1311050527,'India',2015],[36162,83.5,126573481,'Japan',2015],[1390,71.4,25155317,'North Korea',2015],[34644,80.7,50293439,'South Korea',2015],[34186,80.6,4528526,'New Zealand',2015],[64304,81.6,5210967,'Norway',2015],[24787,77.3,38611794,'Poland',2015],[23038,73.13,143456918,'Russia',2015],[19360,76.5,78665830,'Turkey',2015],[38225,81.4,64715810,'United Kingdom',2015],[53354,79.1,321773631,'United States',2015]]
];
var option2,txt2,color;
function dotOption(x,y) {
    option2 = {
        backgroundColor:'transparent',
        title: {
            text: txt2,
            x:'center'
        },
        grid: {
            left: '0%',
            right: '11%',
            bottom: '0%',
            top:'7%',
            containLabel: true
        },
        xAxis: {
            name:x,
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            }
        },
        yAxis: {
            name:y,
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },
            scale: true
        },
        series: [{
            name: '',
            data: data[0],
            type: 'scatter',
            symbolSize: function (data) {
                return Math.sqrt(data[2]) / 5e2;
            },
            label: {
                normal:{
                    show:true,
                    position:'inside',
                    color:'#fff',
                    formatter:  function (param) {
                        return param.data[3];
                    },
                },
                // emphasis: {
                //     show: true,
                //     formatter: function (param) {
                //         return param.data[3];
                //     },
                //     position: 'top'
                // }
            },
            itemStyle: {
                normal: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(120, 36, 50, 0.5)',
                    shadowOffsetY: 5,
                    color: color
                }
            }
        }]
    };
}
function dot1() {
    txt2='疑似谣言影响力分布';
    color=new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
        offset: 0,
        color: 'rgb(251, 118, 123)'
    }, {
        offset: 1,
        color: 'rgb(204, 46, 72)'
    }]);
    var myChart = echarts.init(document.getElementById('influe'),'chalk');
    dotOption('转发量','评论量');
    myChart.setOption(option2);
}
dot1();
function dot2() {
    txt2='疑似谣言传播力分布';
    var myChart = echarts.init(document.getElementById('propagation'),'chalk');
    color = new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
        offset: 0,
        color: 'rgb(129, 227, 238)'
    }, {
        offset: 1,
        color: 'rgb(25, 183, 207)'
    }]);
    dotOption('广度','深度');
    myChart.setOption(option2);
}
dot2();
