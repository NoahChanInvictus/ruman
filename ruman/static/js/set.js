
// 基本信息
    var gongshang_url = '/maniPulate/manipulateReport/gongshang/?id=' + id;
    public_ajax.call_request('get',gongshang_url,gongshang);
    function gongshang(data){
        if(data){
            var name = '未知';
            var place = '未知';
            var start_date = '未知';
            var industry = '未知';

            var money = '未知';
            var person = '未知';
            var kind = '未知';
            var plate = '未知';

            if(data.name && data.name!= '' && data.name!=null){name = data.name};
            if(data.place && data.place!= '' && data.place!=null){place = data.place};
            if(data.start_date && data.start_date!= '' && data.start_date!=null){start_date = data.start_date};
            if(data.industry && data.industry!= '' && data.industry!=null){industry = data.industry};

            if(data.money && data.money!= '' && data.money!=null){money = data.money};
            if(data.person && data.person!= '' && data.person!=null){person = data.person};
            if(data.kind && data.kind!= '' && data.kind!=null){kind = data.kind};
            if(data.plate && data.plate!= '' && data.plate!=null){plate = data.plate};

            $('#card .type-1').text(name).attr('title',name);
            $('#card .type-2').text(place).attr('title',place);
            $('#card .type-3').text(start_date).attr('title',start_date);
            $('#card .type-4').text(industry).attr('title',industry);
            $('#card .type-5').text(money).attr('title',money);
            $('#card .type-6').text(person).attr('title',person);
            $('#card .type-7').text(kind).attr('title',kind);
            $('#card .type-8').text(plate).attr('title',plate);
        }
    }

// 操纵详情   历史记录
    // var loadingHtml = '<center class="loading">正在加载中...</center>';
    // $('#Manipulating_details_content').append(loadingHtml);

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
                        var manipulate_state = '';
                        if (row.manipulate_state==''||row.manipulate_state=='null'||row.manipulate_state=='unknown'||!row.manipulate_state){
                            manipulate_state =  '未知';
                        }else {
                            manipulate_state =  row.manipulate_state;
                        };
                        if(row.ifthis == 1){
                            return '<span class="this-stock">'+manipulate_state+'</span>';
                        }else {
                            return manipulate_state;
                        }
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
                        var date = '';
                        if (row.start_date==''||row.start_date=='null'||row.start_date=='unknown'||!row.start_date || row.end_date==''||row.end_date=='null'||row.end_date=='unknown'||!row.end_date){
                            date =  '未知';
                        }else {
                            date =  row.start_date + '~' + row.end_date;
                        };
                        if(row.ifthis == 1){
                            return '<span class="this-stock">'+date+'</span>';
                        }else {
                            return date;
                        }
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
                        var manipulate_type = '';
                        if (row.manipulate_type==''||row.manipulate_type=='null'||row.manipulate_type=='unknown'||!row.manipulate_type){
                            manipulate_type =  '未知';
                        }else {
                            manipulate_type =  row.manipulate_type;
                        };
                        if(row.ifthis == 1){
                            return '<span class="this-stock">'+manipulate_type+'</span>';
                        }else {
                            return manipulate_type;
                        }
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
                        var increase_ratio = '';
                        if (row.increase_ratio==''||row.increase_ratio=='null'||row.increase_ratio=='unknown'||!row.increase_ratio){
                            increase_ratio =  '未知';
                        }else {
                            increase_ratio =  row.increase_ratio;
                        };
                        if(row.ifthis == 1){
                            return '<span class="this-stock">'+increase_ratio+'</span>';
                        }else {
                            return increase_ratio;
                        }
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
                        if(row.ifthis == 1){
                            return '<span class="this-stock" style="cursor:pointer;" onclick="jumpFrame_1(\''+row.name+'\',\''+row.id+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                        }else {
                            return '<span style="cursor:pointer;" onclick="jumpFrame_1(\''+row.name+'\',\''+row.id+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                        }
                    }
                },
            ],
        });

        $('#Manipulating_details_content center.loading').hide();
    }
    // 跳转详情页
        function jumpFrame_1(name,id) {
            var html = '';
            html='/index/setDetail?stock='+name+'&id='+id;

            window.open(html);
        }

// 价格与收益率
    var myChart_1 = echarts.init(document.getElementById('Price_1'));
    myChart_1.showLoading();
    var myChart_2 = echarts.init(document.getElementById('Price_2'));
    myChart_2.showLoading();

    var price_url = '/maniPulate/manipulateReport/price/?id=' + id;//id=1 测试
    public_ajax.call_request('get',price_url,Price);
    function Price(data){
        var date_data = data.date || [];

        var price_data = data.price || [];
        var industry_price_data = data.industry_price || [];
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
                    showSymbol: true,
                    hoverAnimation: true,
                },
                {
                    // name:'大盘',
                    name:'同行业平均值',
                    type:'line',
                    yAxisIndex: 1,
                    // data:[2728, 3452,3214, 2244, 3155, 3343, 3032, 2947],
                    data: industry_price_data,
                    showSymbol: true,
                    hoverAnimation: true,
                }
            ]
        };
        myChart_1.hideLoading();
        myChart_1.setOption(option_1);

        var ratio_data = data.ratio || [];
        var industry_ratio_data = data.industry_ratio || [];
        var D_value_data = data.D_value || [];
        for(var i=0;i<ratio_data.length;i++){
            ratio_data[i] = ratio_data[i].toFixed(4);
        }
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
                    showSymbol: true,
                    hoverAnimation: true,
                },
                {
                    // name:'万科',
                    name: stock,
                    type:'line',
                    // data:[1, 2, 2, 5, 3, 2, 0,4],
                    data: ratio_data,
                    showSymbol: true,
                    hoverAnimation: true,
                },
                {
                    name:'差值',
                    type:'line',
                    // data:[5, 11, 7, 5, 8, 9,13,10],
                    data: D_value_data,
                    showSymbol: true,
                    hoverAnimation: true,
                }
            ]
        };
        myChart_2.hideLoading();
        myChart_2.setOption(option_2);
    }

// 公告信息
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

        $('#Bulletin_content center.loading').hide();
    }
    // 查看原文
    function originalText(url){

        window.open(url);
    }

// 交易分析
    // 十大股东
        var top10holders_url = '';
        //  渲染 下拉框
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

            $('#Transaction-1 center.loading').hide();
        }

    // 大宗交易
        var Largetrans_url = '/maniPulate/manipulateReport/Largetrans?id=' + id;
        public_ajax.call_request('get',Largetrans_url,table4);
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
                        field: "date",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            if (row.date==''||row.date=='null'||row.date=='unknown'||!row.date){
                                return '未知';
                            }else {
                                return row.date;
                            };
                        }
                    },
                    {
                        title: "成交价(元)",//标题
                        field: "price",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            if (row.price==''||row.price=='null'||row.price=='unknown'||!row.price){
                                return '未知';
                            }else {
                                return row.price;
                            };
                        }
                    },
                    {
                        title: "成交量(万股)",//标题
                        field: "number",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            if (row.number==''||row.number=='null'||row.number=='unknown'||!row.number){
                                return '-';
                            }else {
                                return row.number;
                            };
                        }
                    },
                    {
                        title: "成交额(万元)",//标题
                        field: "amount",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            if (row.amount==''||row.amount=='null'||row.amount=='unknown'||!row.amount){
                                return '-';
                            }else {
                                return row.amount;
                            };
                        }
                    },
                    {
                        title: "折价率(%)",//标题
                        field: "ratio",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            if (row.ratio==''||row.ratio=='null'||row.ratio=='unknown'||!row.ratio){
                                return '-';
                            }else {
                                return row.ratio;
                            };
                        }
                    },
                    {
                        title: "买方营业部",//标题
                        field: "buyer",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            if (row.buyer==''||row.buyer=='null'||row.buyer=='unknown'||!row.buyer){
                                return '-';
                            }else {
                                return row.buyer;
                            };
                        }
                    },
                    {
                        title: "卖方营业部",//标题
                        field: "seller",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            if (row.seller==''||row.seller=='null'||row.seller=='unknown'||!row.seller){
                                return '-';
                            }else {
                                return row.seller;
                            };
                        }
                    },
                ],
            });

            $('#Transaction-2 center.loading').hide();
        }

// 股权分析
    var myChart_3 = echarts.init(document.getElementById('Stock_1'),'chalk');
    myChart_3.showLoading();
    var myChart_4 = echarts.init(document.getElementById('Stock_2'),'chalk');
    myChart_4.showLoading();

    var holderspct_url = '/maniPulate/manipulateReport/holderspct?id=' + id;
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
