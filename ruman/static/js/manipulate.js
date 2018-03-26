
// 预警数
    var warningNumber_url='/maniPulate/manipulateWarning';
    public_ajax.call_request('get',warningNumber_url,warningNumber);
    function warningNumber(data){
        if(data){
            $('#container .firstScreen .com-1').text(data.weeknum);
            $('#container .firstScreen .com-2').text(data.monthnum);
            $('#container .firstScreen .com-3').text(data.seasonnum);
        }
    }

//第一屏   疑似操纵预警
    var loadingHtml = '<center class="loading">正在加载中...</center>';
    $('#recordingTable').append(loadingHtml);

    var earlyWarning_url='/maniPulate/manipulateWarningText';
    public_ajax.call_request('get',earlyWarning_url,earlyWarning);
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
            // showLoading:true,
            columns: [
                {
                    title: "相关股票",//标题
                    field: "stock",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.stock==''||row.stock=='null'||row.stock=='unknown'||!row.stock){
                            return '未知';
                        }else {
                            return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.stock+'\',\''+row.id+'\')" title="进入预警报告">'+row.stock+'</span>';
                        };
                    }
                },
                {
                    title: "开始时间",//标题
                    field: "start_date",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.start_date==''||row.start_date=='null' || row.start_date==null ||row.start_date=='unknown'||!row.start_date){
                            return '未知';
                        }else {
                            return row.start_date;
                        };
                    }

                },
                {
                    title: "结束时间",//标题
                    field: "end_date",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.end_date==''||row.end_date=='null' || row.end_date==null ||row.end_date=='unknown'||!row.end_date){
                            return '未知';
                        }else {
                            return row.end_date;
                        };
                    }
                },
                {
                    title: "操纵类型",//标题
                    field: "manipulate_type",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.manipulate_type==''||row.manipulate_type=='null' || row.manipulate_type==null ||row.manipulate_type=='unknown'||!row.manipulate_type){
                            return '未知';
                        }else {
                            return row.manipulate_type;
                        };
                    }
                },
                {
                    title: "所属行业",//标题
                    field: "industry_name",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.industry_name==''||row.industry_name=='null' || row.industry_name==null ||row.industry_name=='unknown'||!row.industry_name){
                            return '未知';
                        }else {
                            return row.industry_name;
                        };
                    }

                },
                {
                    title: "超涨比率",//标题
                    field: "increase_ratio",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        var increaseRatio;
                        if(row.increase_ratio === 0){
                            return '0%';
                        }else if (row.increase_ratio==''||row.increase_ratio=='null'||row.increase_ratio=='unknown'||!row.increase_ratio){
                            return '未知';
                        }else {
                            increaseRatio = (row.increase_ratio *100).toFixed(2).toString() + '%';
                            return increaseRatio;
                        };
                    }
                },
                {
                    title: "操纵状态",//标题
                    field: "manipulate_state",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.manipulate_state==''||row.manipulate_state=='null' || row.manipulate_state==null ||row.manipulate_state=='unknown'||!row.manipulate_state){
                            return '未知';
                        }else {
                            return row.manipulate_state;
                        };
                    }
                },
                {
                    title: "监测详情",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.stock+'\',\''+row.id+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
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
                return "没有相关的匹配结果";
            },
            formatLoadingMessage: function(){
                return "请稍等，正在加载中。。。";
            }
        });
        $('#recordingTable center.loading').hide();
    };

    // 跳转详情页
    function jumpFrame_1(stock,id) {
        var html = '';
        stock=escape(stock);
        html='/index/setDetail?stock='+stock+'&id='+id;
        // window.location.href=html;
        window.open(html);
    }

//第二屏   预警态势
    var myChart = echarts.init(document.getElementById('trendLine'));
    myChart.showLoading({
        text: '加载中...',
        color: '#c23531',
        textColor: '#000',
        // maskColor: 'rgba(255, 255, 255, 0.8)',
        // maskColor: 'transparent',
        maskColor: 'rgba(0,0,0,.4)',
        zlevel: 0
    });
    var warningNum_url='/maniPulate/manipulateWarningNum?date=7';
    public_ajax.call_request('get',warningNum_url,warningNum);
    function warningNum(data){
        var tit='疑似操纵预警次数';
        var date = data.date;
        var times = data.times;
        var option = {
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
                data: date,
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
                    data: times,
                }
            ]
        };
        myChart.hideLoading();
        myChart.setOption(option);
    }
    // 更改下拉框时
    $('#second_select_1').change(function(){
        var select_warningNum_val = $(this).val();
        myChart.showLoading({
            text: '加载中...',
            color: '#c23531',
            textColor: '#000',
            // maskColor: 'rgba(255, 255, 255, 0.8)',
            maskColor: 'transparent',
            zlevel: 0
        });
        warningNum_url = '/maniPulate/manipulateWarningNum?date='+ select_warningNum_val;
        public_ajax.call_request('get',warningNum_url,warningNum);
    })

//第三屏   操纵影响
    var myChart_2 = echarts.init(document.getElementById('influnce'),'chalk');
    myChart_2.showLoading({
        text: '加载中...',
        color: '#c23531',
        textColor: '#000',
        maskColor: 'transparent',
        zlevel: 0
    });
    var influnce_url='/maniPulate/manipulateInfluence?date=7';
    public_ajax.call_request('get',influnce_url,influnce);
    function influnce(data){
        var ratio = data.ratio;
        var num = data.num;
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
                data: ratio,
                axisLabel:{
                    interval:0,
                    rotate:90,//倾斜度 -90 至 90 默认为0
                    margin:2,
                    textStyle:{
                        fontSize: 14
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
                            },
                            position: 'top',
                        }
                    },
                    data: num,
                },

            ]
        };
        myChart_2.hideLoading();
        myChart_2.setOption(option);
    }
    // 更改下拉框时
    $('#third_select_1').change(function(){
        var select_influnce_val = $(this).val();
        myChart_2.showLoading({
            text: '加载中...',
            color: '#c23531',
            textColor: '#000',
            maskColor: 'transparent',
            zlevel: 0
        });
        influnce_url = '/maniPulate/manipulateInfluence?date='+ select_influnce_val;
        public_ajax.call_request('get',influnce_url,influnce);
    })

//第四屏   行业分布
    var myChart_3 = echarts.init(document.getElementById('bar-1'),'chalk');
    myChart_3.showLoading({
        text: '加载中...',
        color: '#c23531',
        textColor: '#000',
        maskColor: 'transparent',
        zlevel: 0
    });
    var Industry_url='/maniPulate/manipulateIndustry?date=7';
    public_ajax.call_request('get',Industry_url,Industry);
    function Industry(data){
        var industry = data.industry;
        var num = data.num;
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
                        fontSize:14
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
                                color:'#f5f5f5',
                            },
                            position: 'top',


                        }
                    },
                    data: num,
                },

            ]
        };
        myChart_3.hideLoading();
        myChart_3.setOption(option);

        // 前五名
        var num_Max = data.num_Max;
        var industry_Max = data.industry_Max;
        var table_html = '';
        for(vari=0;i<num_Max.length;i++){
            table_html += '<tr><td>'+industry_Max[i]+'</td><td>'+num_Max[i]+'</td></tr>';
        }
        $('.barRank tbody').empty().append(table_html);
    }
    // 更改下拉框时
    $('#four_select').change(function(){
        var select_influnce_val = $(this).val();
        myChart_3.showLoading({
            text: '加载中...',
            color: '#c23531',
            textColor: '#000',
            maskColor: 'transparent',
            zlevel: 0
        });
        Industry_url = '/maniPulate/manipulateIndustry?date='+ select_influnce_val;
        public_ajax.call_request('get',Industry_url,Industry);
    })

//第五屏   操纵类型
    var myChart_4 = echarts.init(document.getElementById('pie-1'),'chalk');
    myChart_4.showLoading({
        text: '加载中...',
        color: '#c23531',
        textColor: '#000',
        maskColor: 'transparent',
        zlevel: 0
    });
    var manipulateType_url='/maniPulate/manipulateType?date=7';
    public_ajax.call_request('get',manipulateType_url,manipulateType);
    function manipulateType(data){
        var type = data.type;
        var num = data.num;
        var num_1 = data.num;
        var seriesData = [];
        for(var i=0;i<num.length;i++){
            seriesData.push({name:type[i],value:num[i]})
        }
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
                data: type
            },
            series : [
                {
                    name: '发布者',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '50%'],
                    data: seriesData,
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
        myChart_4.hideLoading();
        myChart_4.setOption(option);
    }
    // 更改下拉框时
    $('#five_select').change(function(){
        var select_type_val = $(this).val();
        myChart_4.showLoading({
            text: '加载中...',
            color: '#c23531',
            textColor: '#000',
            maskColor: 'transparent',
            zlevel: 0
        });
        manipulateType_url = '/maniPulate/manipulateType?date='+ select_type_val;
        public_ajax.call_request('get',manipulateType_url,manipulateType);
    })

//第六屏   市值分布
    var myChart_5 = echarts.init(document.getElementById('pie-3'),'chalk');
    myChart_5.showLoading({
        text: '加载中...',
        color: '#c23531',
        textColor: '#000',
        maskColor: 'transparent',
        zlevel: 0
    });
    var Panel_url='/maniPulate/manipulatePanel?date=7';
    public_ajax.call_request('get',Panel_url,Panel);
    function Panel(data){
        var PANEL = data.PANEL;
        var num = data.num;
        var seriesData = [];
        for(var i=0;i<num.length;i++){
            seriesData.push({name:PANEL[i],value:num[i]})
        }
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
                data: PANEL
            },
            series : [
                {
                    name: '发布者',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '50%'],
                    data: seriesData,
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
        myChart_5.hideLoading();
        myChart_5.setOption(option);
    }
    // 更改下拉框时
    $('#six_select').change(function(){
        var select_PANEL_val = $(this).val();
        myChart_5.showLoading({
            text: '加载中...',
            color: '#c23531',
            textColor: '#000',
            maskColor: 'transparent',
            zlevel: 0
        });
        Panel_url = '/maniPulate/manipulatePanel?date='+ select_PANEL_val;
        public_ajax.call_request('get',Panel_url,Panel);
    })
