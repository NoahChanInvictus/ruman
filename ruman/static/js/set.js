
// 操纵详情   历史记录
    var t1_data=[{a:'正在操纵',b:'2017-01-01至今',c:'伪市值管理',d:'1.8'},
        {a:'已完成操纵',b:'2016-01-01~2017-10-01',c:'伪市值管理',d:'1.6'},
        {a:'已完成操纵',b:'2015-01-01~2016-10-01',c:'高送转',d:'1.3'}]
    var history_url = '/maniPulate/manipulateReport/history/?id=' + id;
    public_ajax.call_request('get',history_url,table1);
    function table1(data) {
        $('#Manipulating_details_content').bootstrapTable('load', data);
        $('#Manipulating_details_content').bootstrapTable({
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
                    title: "操纵状态",//标题
                    field: "manipulate_state",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.manipulate_state==''||row.manipulate_state=='null'||row.manipulate_state=='unknown'||!row.manipulate_state){
                            return '未知';
                        }else {
                            return row.manipulate_state;
                        };
                    }
                },
                {
                    title: "操纵时间",//标题
                    field: "start_date",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.start_date==''||row.start_date=='null'||row.start_date=='unknown'||!row.start_date || row.end_date==''||row.end_date=='null'||row.end_date=='unknown'||!row.end_date){
                            return '未知';
                        }else {
                            return row.start_date + '~' + row.end_date;
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
                        if (row.manipulate_type==''||row.manipulate_type=='null'||row.manipulate_type=='unknown'||!row.manipulate_type){
                            return '未知';
                        }else {
                            return row.manipulate_type;
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
                        if (row.increase_ratio==''||row.increase_ratio=='null'||row.increase_ratio=='unknown'||!row.increase_ratio){
                            return '未知';
                        }else {
                            return row.increase_ratio;
                        };
                    }
                },
                {
                    title: "操纵详情",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<span style="cursor:pointer;" onclick="jumpFrame_1(\''+row.stock+'\',\''+row.id+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                    }
                },
            ],
        });
    }
    // table1(t1_data);
    // 跳转详情页
        function jumpFrame_1(stock,id) {
            var html = '';
            stock=escape(stock);
            html='/index/setDetail?stock='+stock+'&id='+id;

            window.open(html);
        }

// 价格与收益率
    var myChart_1 = echarts.init(document.getElementById('Price_1'));
    myChart_1.showLoading();
    var myChart_2 = echarts.init(document.getElementById('Price_2'));
    myChart_2.showLoading();

    var price_url = '/maniPulate/manipulateReport/price/?id=1';
    public_ajax.call_request('get',price_url,Price);
    function Price(data){
        var date_data = data.date || [];

        var price_data = data.price || [];
        var industry_price_data = data.industryprice || []; //一会儿改
        for(var i=0;i<industry_price_data.length;i++){
            industry_price_data[i] = industry_price_data[i].toFixed(2);
        }
        var option_1 = {
            title: {
                // text: '万科价格变化',
                text: stock+'价格变化',
                x: 'center',
            },
            tooltip: {
                trigger: 'axis'
            },
            grid: {
                left: '0%',
                right: '9%',
                bottom: '0%',
                top:'17%',
                containLabel: true
            },
            legend: {
                // data:['收盘价（元）','大盘'],
                data:['收盘价（元）','同行业平均值'],
                orient:'horizontal',//horizontal
                // zlevel:99
                top:'7%',
                left:'center'
            },
            xAxis:  {
                name:'时间',
                type: 'category',
                boundaryGap: false,
                // data: ['2017-3-1','2017-3-8','2017-3-15','2017-3-22','2017-3-29','2017-4-5','2017-4-12','2017-2-19'],
                data: date_data,
                axisLabel:{
                    rotate:90
                }
            },
            yAxis: [
                {
                    name:'价格',
                    type: 'value',
                    axisLabel: {
                        // formatter: '{value} °C'
                    }
                },
                {
                    name:'',
                    type: 'value',
                },
            ],
            series: [
                {
                    name:'收盘价（元）',
                    type:'line',
                    // data:[28, 22,34, 44, 55, 43, 32, 47],
                    data: price_data,
                    showSymbol: false,
                    hoverAnimation: false,
                },
                {
                    // name:'大盘',
                    name:'同行业平均值',
                    type:'line',
                    yAxisIndex: 1,
                    // data:[2728, 3452,3214, 2244, 3155, 3343, 3032, 2947],
                    data: industry_price_data,
                    showSymbol: false,
                    hoverAnimation: false,
                }
            ]
        };
        myChart_1.hideLoading();
        myChart_1.setOption(option_1);

        var radtio_data = data.ratio || [];
        var industry_ratio_data = data.industry_ratio || [];
        var D_value_data = data.D_value || [];
        for(var i=0;i<industry_ratio_data.length;i++){
            industry_ratio_data[i] = industry_ratio_data[i].toFixed(4);
        }
        for(var i=0;i<D_value_data.length;i++){
            D_value_data[i] = D_value_data[i].toFixed(4);
        }
        var option_2 = {
            title: {
                // text: '万科收益率变化',
                text: stock+'收益率变化',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                // data:['大盘指数','万科','差值'],
                data:['同行业平均值',stock,'差值'],
                orient:'horizontal',//horizontal
                // zlevel:99
                top:'7%',
                left:'center'
            },
            grid: {
                left: '0%',
                right: '9%',
                bottom: '0%',
                top:'17%',
                containLabel: true
            },
            xAxis:  {
                name:'时间',
                type: 'category',
                boundaryGap: false,
                // data: ['2017-3-1','2017-3-8','2017-3-15','2017-3-22','2017-3-29','2017-4-5','2017-4-12','2017-2-19'],
                data: date_data,
                axisLabel:{
                    rotate:90
                }
            },
            yAxis: {
                name:'收益率%',
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                }
            },
            series: [
                {
                    // name:'大盘指数',
                    name: '同行业平均值',
                    type:'line',
                    // data:[11, 11, 15, 13, 12, 13,11, 10],
                    data: industry_ratio_data,
                    showSymbol: false,
                    hoverAnimation: false,
                },
                {
                    // name:'万科',
                    name: stock,
                    type:'line',
                    // data:[1, 2, 2, 5, 3, 2, 0,4],
                    data: radtio_data,
                    showSymbol: false,
                    hoverAnimation: false,
                },
                {
                    name:'差值',
                    type:'line',
                    // data:[5, 11, 7, 5, 8, 9,13,10],
                    data: D_value_data,
                    showSymbol: false,
                    hoverAnimation: false,
                }
            ]
        };
        myChart_2.hideLoading();
        myChart_2.setOption(option_2);
    }
    function Price_1(){
        var myChart = echarts.init(document.getElementById('Price_1'));
        var option = {
            title: {
                text: '万科价格变化',
                x: 'center',
            },
            tooltip: {
                trigger: 'axis'
            },
            grid: {
                left: '0%',
                right: '9%',
                bottom: '0%',
                top:'17%',
                containLabel: true
            },
            legend: {
                data:['收盘价（元）','大盘'],
                orient:'horizontal',//horizontal
                // zlevel:99
                top:'7%',
                left:'center'
            },
            xAxis:  {
                name:'时间',
                type: 'category',
                boundaryGap: false,
                data: ['2017-3-1','2017-3-8','2017-3-15','2017-3-22','2017-3-29','2017-4-5','2017-4-12','2017-2-19'],
                axisLabel:{
                    rotate:90
                }
            },
            yAxis: [
                {
                    name:'价格',
                    type: 'value',
                    axisLabel: {
                        // formatter: '{value} °C'
                    }
                },
                {
                    name:'',
                    type: 'value',
                },
            ],
            series: [
                {
                    name:'收盘价（元）',
                    type:'line',
                    data:[28, 22,34, 44, 55, 43, 32, 47],
                    showSymbol: false,
                    hoverAnimation: false,
                },
                {
                    name:'大盘',
                    type:'line',
                    yAxisIndex: 1,
                    data:[2728, 3452,3214, 2244, 3155, 3343, 3032, 2947],
                    showSymbol: false,
                    hoverAnimation: false,
                }
            ]
        };
        myChart.setOption(option)
    }
    // Price_1();
    function Price_2(){
        var myChart = echarts.init(document.getElementById('Price_2'));
        var option = {
            title: {
                text: '万科收益率变化',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['大盘指数','万科','差值'],
                orient:'horizontal',//horizontal
                // zlevel:99
                top:'7%',
                left:'center'
            },
            grid: {
                left: '0%',
                right: '9%',
                bottom: '0%',
                top:'17%',
                containLabel: true
            },
            xAxis:  {
                name:'时间',
                type: 'category',
                boundaryGap: false,
                data: ['2017-3-1','2017-3-8','2017-3-15','2017-3-22','2017-3-29','2017-4-5','2017-4-12','2017-2-19'],
                axisLabel:{
                    rotate:90
                }
            },
            yAxis: {
                name:'收益率%',
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                }
            },
            series: [
                {
                    name:'大盘指数',
                    type:'line',
                    data:[11, 11, 15, 13, 12, 13,11, 10],
                    showSymbol: false,
                    hoverAnimation: false,
                },
                {
                    name:'万科',
                    type:'line',
                    data:[1, 2, 2, 5, 3, 2, 0,4],
                    showSymbol: false,
                    hoverAnimation: false,
                },
                {
                    name:'差值',
                    type:'line',
                    data:[5, 11, 7, 5, 8, 9,13,10],
                    showSymbol: false,
                    hoverAnimation: false,
                }
            ]
        };
        myChart.setOption(option)
    }
    // Price_2();

// 公告信息
    var t2_data=[{'a':'股权质押','b':'2017.10.01 13:23','c':'万科A:2017年十月份销售及近期新增项目情况简报'},
    {'a':'股权质押','b':'2017.09.01 13:23','c':'万科A:关于按照《香港上市规则》公布2017年10月份证券变动月'},
    {'a':'对外投资','b':'2017.08.01 13:23','c':'万科A:关于股东股份质押的公告'},
    {'a':'并购重组','b':'2017.07.01 13:23','c':'万科A:关于投资设立物流地产投资基金的公告'},
    {'a':'高送转','b':'2017.06.01 13:23','c':'万科A:2017年面向合格投资者公开发行公司债券(第二期)上市公告书'},]

    var announcement_url = '/maniPulate/manipulateReport/announcement/?id='+id;
    public_ajax.call_request('get',announcement_url,table2);
    function table2(data) {
        $('#Bulletin_content').bootstrapTable('load', data);
        $('#Bulletin_content').bootstrapTable({
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
                    title: "公告类型",//标题
                    field: "type",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.type==''||row.type=='null'||row.type=='unknown'||!row.type){
                            return '未知';
                        }else {
                            return row.type;
                        };
                    }
                },
                {
                    title: "公告时间",//标题
                    field: "publish_time",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.publish_time==''||row.publish_time=='null'||row.publish_time=='unknown'||!row.publish_time){
                            return '未知';
                        }else {
                            return row.publish_time;
                        };
                    }
                },
                {
                    title: "公告标题",//标题
                    field: "title",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.title==''||row.title=='null'||row.title=='unknown'||!row.title){
                            return '暂无标题';
                        }else {
                            if(row.title.length>50){
                                return '<span title="'+row.title+'">'+row.title.substring(0,150)+'...</span>';
                            }else {
                                return row.title;
                            }
                        };
                    }
                },
                {
                    title: "查看原文",//标题
                    field: "url",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.url==''||row.url=='null'||row.url=='unknown'||!row.url){
                            return '未知';
                        }else {
                            return '<span style="cursor:pointer;" onclick="originalText(\''+row.url+'\')" title="查看原文"><i class="icon icon-file-alt"></i></span>';
                        }

                    }
                },
            ],
        });
    }
    // table2(t2_data);
    // 查看原文
    function originalText(url){

        window.open(url);
    }

// 交易分析
    var t3_data=[{'a':'深圳市地铁集团有限公司','b':'增持','c':'3,242,810,791','d':'413,005,395','e':'9.3800','f':'3.7500'},
        {'a':'香港中央结算(代理人)有限公司','b':'','c':'1,314,910,949','d':'2,200','e':'1.9100','f':'0.0000'},
        {'a':'深圳市钜盛华股份有限公司','b':'','c':'926,070,472','d':'','e':'.3900','f':'0.0000'},
        {'a':'国信证券-工商银行-国信金鹏分级1号集合资产管理计划','b':'','c':'456,993,190','d':'','e':'.1400','f':'0.0000'},
        {'a':'前海人寿保险股份有限公司-海利年年','b':'','c':'349,776,441','d':'','e':'.1700','f':'0.0000'},
        {'a':'招商财富-招商银行-德赢1号专项资产管理计划','b':'','c':'329,352,920','d':'','e':'.9800','f':'0.0000'},
        {'a':'安邦财产保险股份有限公司-传统产品','b':'-','c':'258,167,403','d':'0','e':'2.3400','f':'0.0000'},
        {'a':'安邦人寿保险股份有限公司-保守型投资组合','b':'-','c':'243,677,851','d':'0','e':'2.2100','f':'0.0000'},
        {'a':'西部利得基金-建设银行-西部利得金裕1号资产管理计划','b':'-','c':'225,494,379','d':'0','e':'2.0400','f':'0.0000'},
        {'a':'1前海人寿保险股份有限公司-聚富产品','b':'新进','c':'218,081,383','d':'-','e':'1.9800','f':'9800'},]

    var top10holders_url = '';
    // 十大股东 渲染 下拉框
    var seasonBox_url = '/maniPulate/manipulateReport/seasonBox?id=' + id;
    public_ajax.call_request('get',seasonBox_url,seasonBox);
    function seasonBox(data){
        if(data){
            var str = '';
            for(var i=0;i<data.length;i++){
                str += '<option value="'+data[i].seasonid+'">'+ data[i].season + '</option>';
            }
            $('._time2').empty().append(str).children('option:last-child').attr('selected','selected');

            top10holders_url = '/maniPulate/manipulateReport/top10holders?id=' + id +'&seasonid=' + $('._time2').val();
            public_ajax.call_request('get',top10holders_url,table3);
        }
    }

    // 更新下拉框时
    $('._time2').change(function(){
        top10holders_url = '/maniPulate/manipulateReport/top10holders?id=' + id +'&seasonid=' + $(this).val();
        public_ajax.call_request('get',top10holders_url,table3);
    });

    function table3(data) {
        $('#Transaction-1').showLoading();
        $('#Transaction-1').bootstrapTable('load', data);
        $('#Transaction-1').bootstrapTable({
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
                    title: "排名",//标题
                    field: "ranking",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        // return index+1;
                        if (row.ranking==''||row.ranking=='null'||row.ranking=='unknown'||!row.ranking){
                            return '未知';
                        }else {
                            return row.ranking;
                        };
                    }
                },
                {
                    title: "股东名称",//标题
                    field: "holder_name",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.holder_name==''||row.holder_name=='null'||row.holder_name=='unknown'||!row.holder_name||row.holder_name=='none'){
                            return '-';
                        }else {
                            return row.holder_name;
                        };
                    }
                },
                {
                    title: "方向",//标题
                    field: "holder_hold_direction",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.holder_hold_direction==''||row.holder_hold_direction=='null'||row.holder_hold_direction=='unknown'||!row.holder_hold_direction){
                            return '-';
                        }else {
                            return row.holder_hold_direction;
                        };
                    }
                },
                {
                    title: "持股数量(股)",//标题
                    field: "holder_quantity",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.holder_quantity==''||row.holder_quantity=='null'||row.holder_quantity=='unknown'||!row.holder_quantity){
                            return '-';
                        }else {
                            return row.holder_quantity;
                        };
                    }
                },
                {
                    title: "持股数量变动(股)",//标题
                    field: "holder_quantity_change",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.holder_quantity_change==''||row.holder_quantity_change=='null'||row.holder_quantity_change=='unknown'||!row.holder_quantity_change){
                            return '-';
                        }else {
                            return row.holder_quantity_change;
                        };
                    }
                },
                {
                    title: "占总股本比例(%)",//标题
                    field: "holder_pct",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.holder_pct==''||row.holder_pct=='null'||row.holder_pct=='unknown'||!row.holder_pct){
                            return '-';
                        }else {
                            return row.holder_pct;
                        };
                    }
                },
                {
                    title: "持股比例变动(%)",//标题
                    field: "holder_pct_change",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.holder_pct_change==''||row.holder_pct_change=='null'||row.holder_pct_change=='unknown'||!row.holder_pct_change){
                            return '-';
                        }else {
                            return row.holder_pct_change;
                        };
                    }
                },
            ],
        });
    }
    // table3(t3_data);

    // 万宗交易
    var t4_data=[{'a':'2017/11/1','b':'9.15','c':'7.36','d':'214.54','e':'0.12','f':'海通证券威海高山街','g':'机构专用'},
        {'a':'2017/11/1','b':'9.15','c':'7.5','d':'218.63','e':'0.12','f':'中信证券上海环球金融中心','g':'机构专用'},
        {'a':'2017/9/21','b':'8.4','c':'11.8','d':'335.12','e':'0.22','f':'中信证券上海中信广场','g':'机构专用'},
        {'a':'2017/9/21','b':'8.4','c':'7.5','d':'213','e':'0.14','f':'中信证券大连星海广场','g':'机构专用'},
        {'a':'2017/7/18','b':'2.15','c':'2302.82','d':'51007.37','e':'20.28','f':'中国国际金融广州天河路','g':'中国国际金融广州天河路'},
        {'a':'2017/7/18','b':'2.15','c':'323.86','d':'7173.5','e':'3.45','f':'中国国际金融广州天河路','g':'中国国际金融广州天河路'},
        {'a':'2017/7/12','b':'2.28','c':'782.28','d':'17429.21','e':'6.32','f':'国国际金融广州天河路','g':'国泰君安证券顺德大良'},
        {'a':'2017/6/26','b':'26.48','c':'11.47','d':'303.73','e':'0.07','f':'信建投证券北京太阳宫中路','g':'机构专用'},
        {'a':'2017/3/29','b':'21.27','c':'322','d':'6848.94','e':'12.32','f':'信证券上海淮海中路','g':'中信证券上海淮海中路'},
        {'a':'2016/11/29','b':'27.5','c':'2518.15','d':'69249.13','e':'25.26','f':'泰君安证券广州黄埔大道','g':'中信证券北京复外大街'},
    ]
    function table4(data) {
        $('#Transaction-2').bootstrapTable('load', data);
        $('#Transaction-2').bootstrapTable({
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
                    title: "交易日期",//标题
                    field: "a",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                },
                {
                    title: "成交价(元)",//标题
                    field: "b",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.b==''||row.b=='null'||row.b=='unknown'||!row.b){
                            return '未知';
                        }else {
                            return row.b;
                        };
                    }
                },
                {
                    title: "成交量(万股)",//标题
                    field: "c",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.c==''||row.c=='null'||row.c=='unknown'||!row.c){
                            return '-';
                        }else {
                            return row.c;
                        };
                    }
                },
                {
                    title: "成交额(万元)",//标题
                    field: "d",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.d==''||row.d=='null'||row.d=='unknown'||!row.d){
                            return '-';
                        }else {
                            return row.d;
                        };
                    }
                },
                {
                    title: "成交额占比(%)",//标题
                    field: "e",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.e==''||row.e=='null'||row.e=='unknown'||!row.e){
                            return '-';
                        }else {
                            return row.e;
                        };
                    }
                },
                {
                    title: "买方营业部",//标题
                    field: "f",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.f==''||row.f=='null'||row.f=='unknown'||!row.f){
                            return '-';
                        }else {
                            return row.f;
                        };
                    }
                },
                {
                    title: "卖方营业部",//标题
                    field: "g",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.g==''||row.g=='null'||row.g=='unknown'||!row.g){
                            return '-';
                        }else {
                            return row.g;
                        };
                    }
                },
            ],
        });
    }
    table4(t4_data)

// 股权分析
    var myChart_3 = echarts.init(document.getElementById('Stock_1'),'chalk');
    myChart_3.showLoading();
    var myChart_4 = echarts.init(document.getElementById('Stock_2'),'chalk');
    myChart_4.showLoading();

    var holderspct_url = '/maniPulate/manipulateReport/holderspct?id=16';
    public_ajax.call_request('get',holderspct_url,Stock);
    function Stock(data){
        var holder_pctbyinst_data = data.holder_pctbyinst;      //机构投资者持股
        var holder_notpctbyinst_data = data.holder_notpctbyinst;//非 机构投资者持股

        var holder_top10pct_data = data.holder_top10pct;        //十大股东
        var holder_nottop10pct_data = data.holder_nottop10pct;  //非 十大股东

        var option_3 = {
            backgroundColor:'transparent',
            title : {
                // text: '万科机构投资者持股比例',
                text: stock + '机构投资者持股比例',
                x:'center',
                textStyle:{
                    color:'#333'
                }
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['机构投资者','非机构投资者'],
                textStyle:{
                    color:'#333'
                }
            },
            series : [
                {
                    name: '投资者',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '50%'],
                    data:[
                        // {value:335, name:'机构投资者'},
                        // {value:166, name:'非机构投资者'},
                        {value: holder_pctbyinst_data, name:'机构投资者'},
                        {value: holder_notpctbyinst_data, name:'非机构投资者'},
                    ],
                    label: {
                        normal:{
                            show: true,
                            // position:'inner',
                            formatter: "{b} {d}%",
                            textStyle: {
                                // fontWeight:'bolder',
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
        myChart_3.hideLoading();
        myChart_3.setOption(option_3);

        var option_4 = {
            backgroundColor:'transparent',
            title : {
                // text: '万科十大股东持股比例',
                text: stock + '十大股东持股比例',
                x:'center',
                textStyle:{
                    color:'#333'
                }
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['十大股东','非十大股东'],
                textStyle:{
                    color:'#333'
                }
            },
            series : [
                {
                    name: '股东',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '50%'],
                    data:[
                        // {value:111, name:'十大股东'},
                        // {value:789, name:'非十大股东'},
                        {value:holder_top10pct_data, name:'十大股东'},
                        {value:holder_nottop10pct_data, name:'非十大股东'},
                    ],
                    label: {
                        normal:{
                            show: true,
                            // position:'inner',
                            formatter: "{b} {d}%",
                            // textStyle: {
                            //     fontWeight:'bolder',
                            //     fontSize : '12',
                            //     color:'#164d8e'
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
        myChart_4.hideLoading();
        myChart_4.setOption(option_4);
    }
    function Stock_1(){
        var myChart = echarts.init(document.getElementById('Stock_1'),'chalk');
        var option = {
            backgroundColor:'transparent',
            title : {
                text: '万科机构投资者持股比例',
                x:'center',
                textStyle:{
                    color:'#333'
                }
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['机构投资者','非机构投资者'],
                textStyle:{
                    color:'#333'
                }
            },
            series : [
                {
                    name: '投资者',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '50%'],
                    data:[
                        {value:335, name:'机构投资者'},
                        {value:166, name:'非机构投资者'},
                    ],
                    label: {
                        normal:{
                            show: true,
                            // position:'inner',
                            formatter: "{b} {d}%",
                            textStyle: {
                                // fontWeight:'bolder',
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
    // Stock_1()

    function Stock_2(){
        var myChart = echarts.init(document.getElementById('Stock_2'),'chalk');
        var option = {
            backgroundColor:'transparent',
            title : {
                text: '万科十大股东持股比例',
                x:'center',
                textStyle:{
                    color:'#333'
                }
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['十大股东','非十大股东'],
                textStyle:{
                    color:'#333'
                }
            },
            series : [
                {
                    name: '股东',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '50%'],
                    data:[
                        {value:111, name:'十大股东'},
                        {value:789, name:'非十大股东'},
                    ],
                    label: {
                        normal:{
                            show: true,
                            // position:'inner',
                            formatter: "{b} {d}%",
                            // textStyle: {
                            //     fontWeight:'bolder',
                            //     fontSize : '12',
                            //     color:'#164d8e'
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
        myChart.setOption(option)
    }
    // Stock_2()

//舆情分析
var t5_data=[{'a':'2017.10.01 13:23','b':'微博','c':'所长别开枪是我','d':'国家发布雄安新区新资讯，新政策的颁布'},
    {'a':'2017.09.01 13:23','b':'股吧','c':'机智达人','d':'新能源汽车不断被尝试，多家公司涉足新'},
    {'a':'2017.08.01 13:23','b':'知乎','c':'沈小司司','d':'快递行业在政策促进下稳步前进，快递业'},
    {'a':'2017.07.01 13:23','b':'贴吧','c':'所长别开枪是我','d':'传统煤炭产业再度进入大众视线，能源产'},
    {'a':'2017.06.01 13:23','b':'微博','c':'机智达人','d':'北京市发布医疗改革新办法，医改给人们'},
];
function table5(data) {
    $('#opinion').bootstrapTable('load', data);
    $('#opinion').bootstrapTable({
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
                title: "时间",//标题
                field: "a",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "渠道",//标题
                field: "b",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.b==''||row.b=='null'||row.b=='unknown'||!row.b){
                        return '未知';
                    }else {
                        return row.b;
                    };
                }
            },
            {
                title: "发布者",//标题
                field: "c",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.c==''||row.c=='null'||row.c=='unknown'||!row.c){
                        return '-';
                    }else {
                        return row.c;
                    };
                }
            },
            {
                title: "内容",//标题
                field: "d",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.d==''||row.d=='null'||row.d=='unknown'||!row.d){
                        return '-';
                    }else {
                        if(row.d.length>50){
                            return '<span title="'+row.d+'">'+row.d.substring(0,150)+'...</span>';
                        }else {
                            return row.d;
                        }
                    };
                }
            },
            {
                title: "查看详情",//标题
                field: "e",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<span style="cursor:pointer;" onclick="" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                }
            },
        ],
    });
}
table5(t5_data)
