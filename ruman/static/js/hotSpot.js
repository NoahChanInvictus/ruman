// 适配分辨率
    var pageData=6;
    if (screen.width <= 1536){
        pageData=6;
    }else {
        pageData=10;
    }


// 热点监测 表格
    var hotSpotData = [
        {
        increase_ratio: 0.032568,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-30",
        id: 903,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "长园集团(600525)"
        },
        {
        increase_ratio: 0.031488,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-30",
        id: 905,
        industry_name: "农、林、牧、渔业",
        manipulate_state: "正在操纵",
        stock: "天山生物(300313)"
        },
        {
        increase_ratio: 0.015496,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-30",
        id: 902,
        industry_name: "租赁和商务服务业",
        manipulate_state: "正在操纵",
        stock: "中青旅(600138)"
        },
        {
        increase_ratio: 0.004798,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-30",
        id: 906,
        industry_name: "文化、体育和娱乐业",
        manipulate_state: "正在操纵",
        stock: "宋城演艺(300144)"
        },
        {
        increase_ratio: 0.00069,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-30",
        id: 901,
        industry_name: "租赁和商务服务业",
        manipulate_state: "正在操纵",
        stock: "易见股份(600093)"
        },
        {
        increase_ratio: 0,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-30",
        id: 904,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "沙钢股份(002075)"
        },
        {
        increase_ratio: 0.017131,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-29",
        id: 896,
        industry_name: "文化、体育和娱乐业",
        manipulate_state: "正在操纵",
        stock: "唐德影视(300426)"
        },
        {
        increase_ratio: 0.010799,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-29",
        id: 894,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "*ST嘉陵(600877)"
        },
        {
        increase_ratio: 0.009818,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-29",
        id: 893,
        industry_name: "金融业",
        manipulate_state: "正在操纵",
        stock: "中国太保(601601)"
        },
        {
        increase_ratio: 0,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-29",
        id: 895,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "亚光科技(300123)"
        },
        {
        increase_ratio: 0,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-29",
        id: 897,
        industry_name: "文化、体育和娱乐业",
        manipulate_state: "正在操纵",
        stock: "长城影视(002071)"
        },
        {
        increase_ratio: -0.023898,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-29",
        id: 898,
        industry_name: "文化、体育和娱乐业",
        manipulate_state: "正在操纵",
        stock: "上海电影(601595)"
        },
        {
        increase_ratio: -0.027913,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-29",
        id: 899,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "东港股份(002117)"
        },
        {
        increase_ratio: -0.08657,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-29",
        id: 900,
        industry_name: "农、林、牧、渔业",
        manipulate_state: "正在操纵",
        stock: "仙坛股份(002746)"
        },
        {
        increase_ratio: 0.004127,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-28",
        id: 892,
        industry_name: "农、林、牧、渔业",
        manipulate_state: "正在操纵",
        stock: "罗牛山(000735)"
        },
        {
        increase_ratio: -0.000314,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-28",
        id: 891,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "歌力思(603808)"
        },
        {
        increase_ratio: -0.000958,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-28",
        id: 887,
        industry_name: "文化、体育和娱乐业",
        manipulate_state: "正在操纵",
        stock: "天舟文化(300148)"
        },
        {
        increase_ratio: -0.002675,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-28",
        id: 890,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "步森股份(002569)"
        },
        {
        increase_ratio: -0.007394,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-28",
        id: 886,
        industry_name: "金融业",
        manipulate_state: "正在操纵",
        stock: "吴江银行(603323)"
        },
        {
        increase_ratio: -0.018125,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-28",
        id: 889,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "爱迪尔(002740)"
        },
        {
        increase_ratio: -0.029035,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-28",
        id: 888,
        industry_name: "农、林、牧、渔业",
        manipulate_state: "正在操纵",
        stock: "开创国际(600097)"
        },
        {
        increase_ratio: 0.028486,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-27",
        id: 885,
        industry_name: "电力、热力、燃气及水生产和供应业",
        manipulate_state: "正在操纵",
        stock: "中天能源(600856)"
        },
        {
        increase_ratio: 0.002053,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-27",
        id: 882,
        industry_name: "金融业",
        manipulate_state: "正在操纵",
        stock: "北京银行(601169)"
        },
        {
        increase_ratio: -0.017921,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-27",
        id: 883,
        industry_name: "金融业",
        manipulate_state: "正在操纵",
        stock: "无锡银行(600908)"
        },
        {
        increase_ratio: -0.036132,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-27",
        id: 884,
        industry_name: "交通运输、仓储和邮政业",
        manipulate_state: "正在操纵",
        stock: "中储股份(600787)"
        },
        {
        increase_ratio: 0.026531,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-26",
        id: 879,
        industry_name: "科学研究和技术服务业",
        manipulate_state: "正在操纵",
        stock: "天海防务(300008)"
        },
        {
        increase_ratio: 0.017336,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-26",
        id: 881,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "沃施股份(300483)"
        },
        {
        increase_ratio: -0.00277,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-26",
        id: 880,
        industry_name: "租赁和商务服务业",
        manipulate_state: "正在操纵",
        stock: "轻纺城(600790)"
        },
        {
        increase_ratio: -0.099951,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-23",
        id: 878,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "上海凤凰(600679)"
        },
        {
        increase_ratio: 0.610394,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-22",
        id: 873,
        industry_name: "科学研究和技术服务业",
        manipulate_state: "正在操纵",
        stock: "贝瑞基因(000710)"
        },
        {
        increase_ratio: 0.006329,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-22",
        id: 876,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "易尚展示(002751)"
        },
        {
        increase_ratio: -0.004926,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-22",
        id: 874,
        industry_name: "科学研究和技术服务业",
        manipulate_state: "正在操纵",
        stock: "苏交科(300284)"
        },
        {
        increase_ratio: -0.009587,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-22",
        id: 877,
        industry_name: "交通运输、仓储和邮政业",
        manipulate_state: "正在操纵",
        stock: "恒通股份(603223)"
        },
        {
        increase_ratio: -0.034153,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-22",
        id: 875,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "恒天海龙(000677)"
        },
        {
        increase_ratio: 0.026949,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-21",
        id: 869,
        industry_name: "科学研究和技术服务业",
        manipulate_state: "正在操纵",
        stock: "合诚股份(603909)"
        },
        {
        increase_ratio: -0.015864,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-21",
        id: 868,
        industry_name: "科学研究和技术服务业",
        manipulate_state: "正在操纵",
        stock: "能科股份(603859)"
        },
        {
        increase_ratio: -0.019039,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-21",
        id: 871,
        industry_name: "农、林、牧、渔业",
        manipulate_state: "正在操纵",
        stock: "獐子岛(002069)"
        },
        {
        increase_ratio: -0.03791,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-21",
        id: 870,
        industry_name: "制造业",
        manipulate_state: "正在操纵",
        stock: "康欣新材(600076)"
        },
        {
        increase_ratio: 0,
        manipulate_type: "伪市值管理",
        end_date: "至今",
        start_date: "2016-12-20",
        id: 867,
        industry_name: "采矿业",
        manipulate_state: "正在操纵",
        stock: "盛屯矿业(600711)"
        },

    ]
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
                    title: "相关股票",//标题
                    field: "stock",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        var stock = '';

                        if (row.stock==''||row.stock=='null'||row.stock=='unknown'||!row.stock){
                            return '未知';
                        }else if(row.stock.length >=5){
                            stock = row.stock.slice(0,5)+'...';
                            return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.stock+'\',\''+row.id+'\')" title="'+row.stock+'">'+stock+'</span>';
                        }else {
                            stock = row.stock;
                            return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.stock+'\',\''+row.id+'\')" title="'+row.stock+'">'+stock+'</span>';
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
                    title: "热点类型",//标题
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
                        var industryName = '';

                        if (row.industry_name==''||row.industry_name=='null' || row.industry_name==null ||row.industry_name=='unknown'||!row.industry_name){
                            return '未知';
                        }else if(row.industry_name.length >=5){
                            industryName = row.industry_name.slice(0,5)+'...';
                            return '<span style="cursor:pointer;color:white;" title="'+row.industry_name+'">'+industryName+'</span>';
                        }else {
                            industryName = row.industry_name;
                            return '<span style="cursor:pointer;color:white;" title="'+row.industry_name+'">'+industryName+'</span>';
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
                    title: "热点状态",//标题
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
                return "没有相关的匹配结果";  //没 效果
            },
            formatLoadingMessage: function(){
                return "请稍等，正在加载中。。。";
            },
        });
        $('#hotspotTable p.loading').hide();
        $('.hotspotTable .fixed-table-toolbar .search input').attr('placeholder','请输入查询内容');
    };
    hotSpot(hotSpotData);

// 跳转详情页
    function jumpFrame_1(stock,id) {
        var html = '';
        stock=escape(stock);
        html='/index/hotDetail?stock='+stock+'&id='+id;
        // window.location.href=html;
        window.open(html);
    }



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
tables(obj);

function line_1() {
    var myChart = echarts.init(document.getElementById('analysis'),'chalk');
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
            top:'4%',
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            boundaryGap: false,
            axisLine: {
                lineStyle: {
                    color: '#fff',
                    width:'2'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#fff',
                    fontWeight:'700'
                }
            },
            data: ['周一','周二','周三','周四','周五','周六','周日'],
        }],
        yAxis: [{
            name:'热度',
            type: 'value',
            axisTick: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    color: '#fff',
                    width:'2'
                }
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 14,
                    fontWeight:'700',
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
                data: [11, 11, 15, 13, 12, 13, 10],
            }
        ]
    };
    myChart.setOption(option);
}
line_1();


// 鱼骨图
//
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
    spread_pie_3(fish);


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
                var myChart = ec.init(document.getElementById('word-cloud'),'chalk');
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

// 纵向时间轴







