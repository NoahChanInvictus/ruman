//第一屏
    var earlyWarningdata=[
        {'a':'万科（000000）','b':'2017-01-01','c':'2017-10-01','d':'伪市值管理','e':'房地产','f':'50%',
            'g':'已完成操纵'},
        {'a':'安硕信息（000000）','b':'2017-01-01','c':'至今','d':'高送转','e':'信息','f':'50%',
            'g':'正在操纵'},
        {'a':'新洋丰（000000）','b':'2017-01-01','c':'2017-10-01','d':'定向增发','e':'农业','f':'50%',
            'g':'已完成操纵'},
        {'a':'匹凸匹（000000）','b':'2017-01-01','c':'至今','d':'散布信息牟利','e':'金融','f':'50%',
            'g':'正在操纵'},
        {'a':'恒康医疗（000000）','b':'2017-01-01','c':'2017-10-01','d':'其他','e':'医疗','f':'50%',
            'g':'已完成操纵'},
        {'a':'宏达新材（000000）','b':'2017-01-01','c':'至今','d':'伪市值管理','e':'材料','f':'50%',
            'g':'正在操纵'},
    ]
    var earlyWarning_url='';
    // public_ajax.call_request('get',earlyWarning_url,earlyWarning);
    function earlyWarning(data) {
        $('#recordingTable').bootstrapTable('load', data);
        $('#recordingTable').bootstrapTable({
            data:data,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize: 7,//单页记录数
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
                    title: "相关股票",//标题
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
                    title: "开始时间",//标题
                    field: "b",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直

                },
                {
                    title: "结束时间",//标题
                    field: "c",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "操纵类型",//标题
                    field: "d",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "所属行业",//标题
                    field: "e",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直

                },
                {
                    title: "超涨比率",//标题
                    field: "f",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "操纵状态",//标题
                    field: "g",//键名
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
        var html='/index/setDetail';
        // window.location.href=html;
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
var day30Data=[];
for (var b=0;b< 30;b++){
    day30Data.push(Math.round(Math.random()*(20-5)+5));
}
var option,tit;
function _option() {
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
            name:'次数',
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
                data: day30Data,
            }
        ]
    };
};
function line_1() {
    tit='疑似操纵预警次数';
    var myChart = echarts.init(document.getElementById('trendLine'));
    _option();
    myChart.setOption(option);
}
line_1();
//第三屏
var industry=['农、林、牧、渔业','采矿业','制造业','电力、热力、燃气\n及水生产和供应业','建筑业','批发和零售业','交通运输、\n仓储和邮政业',
    '住宿和餐饮业','信息传输、软件\n和信息技术服务业','金融业','房地产业','租赁和\n商务服务业','科学研究\n和技术服务业',
    '水利、环境和\n公共设施管理业','居民服务、修理和\n其他服务业','教育','卫生和\n社会工作','文化、体育和\n娱乐业','综合',];
function bar_1() {
    var myChart = echarts.init(document.getElementById('influnce'),'chalk');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: '疑似操纵影响',
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
            top:'7%',
            containLabel: true
        },
        yAxis: {
            name:'数量',
            type: 'value',
            boundaryGap: [0, 0.01],
        },
        xAxis: {
            name:'股价涨幅',
            type: 'category',
            data: ['0%~10%','10%~20%','20%~30%','30%~40%','40%~50%','50%~60%','60%~70%','70%~80%','80%~90%','100%~110%','110%~120%',
                '120%~130%','130%~140%','140%~150%','150%~160%','160%~170%','170%~180%','180%~190%','190%~200%'],
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
                data: [132, 345, 342, 534, 222,199, 444, 222,234,444,345, 222,234, 222,234,444,345, 222,234],
            },

        ]
    };
    myChart.setOption(option);
}
bar_1();
//第四屏
function bar_2() {
    var myChart = echarts.init(document.getElementById('bar-1'),'chalk');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: '疑似操纵行业分布',
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
            top:'7%',
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
                    normal:{color:'#ee9080'},
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
                data: [132, 345, 342, 534, 333,199, 444, 222,234,199, 444, 222,234, 222,234,444,345, 222,234],
            },

        ]
    };
    myChart.setOption(option);
}
bar_2();
//第五屏
function pie_1() {
    var myChart = echarts.init(document.getElementById('pie-1'),'chalk');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '疑似操纵类型分布',
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['高送转','定向增发','伪市值管理','散布信息牟利','其他']
        },
        series : [
            {
                name: '发布者',
                type: 'pie',
                radius : '55%',
                center: ['50%', '50%'],
                data:[
                    {value:335, name:'高送转'},
                    {value:310, name:'定向增发'},
                    {value:234, name:'散布信息牟利'},
                    {value:135, name:'伪市值管理'},
                    {value:1548, name:'其他'},
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
//第六屏
function pie_2() {
    var myChart = echarts.init(document.getElementById('pie-3'),'chalk');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '疑似操纵公司市值分布',
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['主板','创业板','中小板']
        },
        series : [
            {
                name: '发布者',
                type: 'pie',
                radius : '55%',
                center: ['50%', '50%'],
                data:[
                    {value:335, name:'主板'},
                    {value:310, name:'创业板'},
                    {value:234, name:'中小板'},
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
pie_2();