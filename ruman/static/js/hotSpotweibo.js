
// 微博热点 页面 js

//第一屏 ====
    var earlyWarningdata=[
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'所长别开枪是我','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'机智达人','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'沈小司司','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'所长别开枪是我','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'机智达人','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'沈小司司','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'所长别开枪是我','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'机智达人','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'沈小司司','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'所长别开枪是我','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'机智达人','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'沈小司司','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'所长别开枪是我','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'机智达人','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'沈小司司','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
        {'a':'2017-05-01 00:00','b':'万科建立新安小镇','c':'所长别开枪是我','d':'股吧','e':'65','f':'53',
            'g':'50000','h':'房地产,达赖,维权','i':'是'},
        {'a':'2017-06-01 00:00','b':'万科发现锂矿产','c':'机智达人','d':'微博','e':'53','f':'44',
            'g':'40000','h':'矿产,煤老板,瓦斯爆炸','i':'否'},
        {'a':'2017-07-01 00:00','b':'格力入股天津一汽','c':'沈小司司','d':'知乎','e':'44','f':'30',
            'g':'30000','h':'汽车能源,比亚迪,天然气,汽油','i':'是'},
    ]
    var earlyWarning_url='/hotSpotweibo/get_hotSpotweibo_list/';
    public_ajax.call_request('get',earlyWarning_url,earlyWarning);
    function earlyWarning(data) {
        console.log(data)
        $('#recordingTable').bootstrapTable('load', data);
        $('#recordingTable').bootstrapTable({
            data:data,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize: 10,//单页记录数
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
                    title: "主题",//标题
                    field: "text",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        var str = '';
                        if(row.text.length > 14){
                            str = row.text.slice(0,14)+'...';
                        }else {
                            str = row.text;
                        }
                        if (row.text==''||row.text=='null'||row.text=='unknown'||!row.text){
                            return '未知';
                        }else {
                            return '<span style="cursor:pointer;color:white;" title="'+row.text+'">'+str+'</span>';
                        };
                    }
                },
                {
                    title: "发布时间",//标题
                    field: "timestamp",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        var str = '';

                        if (row.timestamp==''||row.timestamp=='null'||row.timestamp=='unknown'||!row.timestamp){
                            return '未知';
                        }else {
                            str = getLocalTime(row.timestamp);
                            return str;
                        };
                    }
                },
                {
                    title: "发布者",//标题
                    field: "uid",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "评论数",//标题
                    field: "comment",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直

                },
                {
                    title: "转发数",//标题
                    field: "retweeted",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                // {
                //     title: "用户人数",//标题
                //     field: "g",//键名
                //     sortable: true,//是否可排序
                //     order: "desc",//默认排序方式
                //     align: "center",//水平
                //     valign: "middle",//垂直
                // },
                {
                    title: "关键词",//标题
                    field: "query_kwds",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "热点详情",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.uid+'\',\''+row.en_name+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
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
        $('#recordingTable center.load').hide();
    };
    // earlyWarning(earlyWarningdata);
    // 跳转详情页
    function jumpFrame_1(uid, en_name) {
        var html='/index/hotweiboDetail/?uid='+uid+'&en_name='+en_name;
        window.open(html);

    }

// 造谣、传谣者 暂去掉
/*


    var tjs=[{a:'21343532',b:'213',c:'43'},{a:'21343532',b:'213',c:'43'},{a:'21343532',b:'213',c:'43'},{a:'21343532',b:'213',c:'43'},
        {a:'875321412',b:'342',c:'743'},{a:'875321412',b:'342',c:'743'},{a:'875321412',b:'342',c:'743'},
        {a:'564214312',b:'564',c:'123'},{a:'564214312',b:'564',c:'123'},{a:'564214312',b:'564',c:'123'}]
    function spreadRank(data) {
        $('#spreadRank').bootstrapTable('load', data);
        $('#spreadRank').bootstrapTable({
            data:data,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize: 10,//单页记录数
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
                    title: "排名",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return index+1;
                    }
                },
                {
                    title: "发布者ID",//标题
                    field: "a",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                    //     if (row.a==''||row.a=='null'||row.a=='unknown'||!row.a){
                    //         return '未知';
                    //     }else {
                    //         return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.a+'\')" title="进入画像">'+row.a+'</span>';
                    //     };
                    // }
                },
                {
                    title: "疑似谣言发布数",//标题
                    field: "b",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "疑似谣言评论数",//标题
                    field: "c",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直

                },
            ],
        });
    };
    spreadRank(tjs);
*/

// 气泡图 暂去掉
/*
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
    function dot2() {
        txt2='造谣/传谣分布';
        var myChart = echarts.init(document.getElementById('propagation'),'chalk');
        color = new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
            offset: 0,
            color: 'rgb(251, 118, 123)'
        }, {
            offset: 1,
            color: 'rgb(204, 46, 72)'
        }])
        dotOption('广度','深度');
        myChart.setOption(option2);
    }
    dot2();
 */
