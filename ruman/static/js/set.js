// 操纵详情 页 js

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
                    title: "涨幅",//标题
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
                            return '<span class="this-stock" style="cursor:pointer;" onclick="jumpFrame_1(\''+row.name+'\',\''+row.id+'\',\''+row.manipulate_type_num+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                        }else {
                            return '<span style="cursor:pointer;" onclick="jumpFrame_1(\''+row.name+'\',\''+row.id+'\',\''+row.manipulate_type_num+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                        }
                    }
                },
            ],
        });

        $('#Manipulating_details_content center.loading').hide();
    }

    // 跳转详情页
    function jumpFrame_1(stock, id, manipulate_type_num) {
        var html = '';
        stock=escape(stock);
        html='/index/setDetail?stock='+stock+'&id='+id +'&manipulate_type_num='+manipulate_type_num;
        // window.location.href=html;
        window.open(html);
    }

//舆情分析
    if(manipulate_type_num == 4){ //显示 虚假消息 舆情分析
        $('#False_message').show();
        $('#Public_opinion').show();
        // 虚假消息

            var rumantext_url = '/maniPulate/manipulateReport/rumantext/?id=' + id;
            public_ajax.call_request('get',rumantext_url,rumantext);
            function rumantext(data){
                $('#False_message p.False_content').empty().text(data.text);
            }

        // 舆情分析
            var rumancomment_url = '/maniPulate/manipulateReport/rumancomment/?id=' + id;
            public_ajax.call_request('get',rumancomment_url,table5);
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
                            field: "publish_time",//键名
                            sortable: true,//是否可排序
                            order: "desc",//默认排序方式
                            align: "center",//水平
                            valign: "middle",//垂直
                        },
                        {
                            title: "发布者",//标题
                            field: "author",//键名
                            sortable: true,//是否可排序
                            order: "desc",//默认排序方式
                            align: "center",//水平
                            valign: "middle",//垂直
                            formatter: function (value, row, index) {
                                if (row.author==''||row.author=='null'||row.author=='unknown'||!row.author){
                                    return '-';
                                }else {
                                    return row.author;
                                };
                            }
                        },
                        {
                            title: "渠道",//标题
                            field: "source",//键名
                            sortable: true,//是否可排序
                            order: "desc",//默认排序方式
                            align: "center",//水平
                            valign: "middle",//垂直
                            formatter: function (value, row, index) {
                                if (row.source==''||row.source=='null'||row.source=='unknown'||!row.source){
                                    return '-';
                                }else {
                                    return row.source;
                                    // return '微博';
                                };
                            }
                        },
                        {
                            title: "内容",//标题
                            field: "text",//键名
                            sortable: true,//是否可排序
                            order: "desc",//默认排序方式
                            align: "center",//水平
                            valign: "middle",//垂直
                            formatter: function (value, row, index) {
                                if (row.text==''||row.text=='null'||row.text=='unknown'||!row.text){
                                    return '-';
                                }else {
                                    if(row.text.length>50){
                                        return '<span title="'+row.text+'">'+row.text.substring(0,150)+'...</span>';
                                    }else {
                                        return row.text;
                                    }
                                };
                            }
                        },
                    ],
                });
            }
            // table5(t5_data)
    }else {         //隐藏  虚假消息 舆情分析
        $('#False_message').hide();
        $('#Public_opinion').hide();

    }

// 价格与收益率
    var myChart_1 = echarts.init(document.getElementById('Price_1'));
    myChart_1.showLoading();
    var myChart_2 = echarts.init(document.getElementById('Price_2'));
    myChart_2.showLoading();
    var myPriceChart_3 = echarts.init(document.getElementById('Price_3'));
    myPriceChart_3.showLoading();
    var myPriceChart_4 = echarts.init(document.getElementById('Price_4'));
    myPriceChart_4.showLoading();

    var price_url = '/maniPulate/manipulateReport/price/?id=' + id;//id=1 测试
    public_ajax.call_request('get',price_url,Price);
    function Price(data){
        var date_data = data.date || [];

        // 价格变化
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
                left: '5%',
                right: '9%',
                bottom: '15%',
                top:'17%',
                // containLabel: true
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
                // name:'时间',
                name:'',
                type: 'category',
                boundaryGap: true,
                // nameGap:40,
                // data: ['2017-3-1','2017-3-8','2017-3-15','2017-3-22','2017-3-29','2017-4-5','2017-4-12','2017-2-19'],
                data: date_data,
                axisLabel:{
                    rotate:90
                }
            },
            yAxis: [
                {
                    name:'价格(元)',
                    type: 'value',
                    axisLabel: {
                        // formatter: '{value} °C'
                    },
                    // min:'dataMin',
                    // max:'dataMax'
                    min:function(value) {
                        return Math.floor(value.min - 2);//向下取整
                    },
                    max:function(value) {
                        return Math.ceil(value.max + 2);//向上取整
                    },
                },
                {
                    name:'',
                    type: 'value',
                    // min:'dataMin',
                    // max:'dataMax'
                    min:function(value) {
                        return (value.min - 2).toFixed(2);
                    },
                    max:function(value) {
                        return (value.max + 2).toFixed(2);
                    },
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

        // ===========

        // 收益率变化
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
                data:[stock,'同行业平均值','差值'],
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
            color:['#c23531','#749f83','#2f4554'],
            series: [
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
                    // name:'大盘指数',
                    name: '同行业平均值',
                    type:'line',
                    // data:[11, 11, 15, 13, 12, 13,11, 10],
                    data: industry_ratio_data,
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

// 成交量 成交额 变化=========
    // var trading_url = '/maniPulate/manipulateReport/trading/?id=1920'// 测试的
    var trading_url = '/maniPulate/manipulateReport/trading/?id=' + id;
    public_ajax.call_request('get',trading_url,Trading);
    function Trading(data){
        var date_data = data.date || [];

        // 成交量变化
        var volume_data = data.volume || [];
        // for(var i=0;i<volume_data.length;i++){
        //     volume_data[i] = volume_data[i]/1000000;
        // }
        var option_3 = {
            title: {
                // text: '万科收益率变化',
                text: stock+'成交量变化',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                // data:['大盘指数','万科','差值'],
                // data:[stock,'同行业平均值','差值'],
                data:['成交量'],
                orient:'horizontal',//horizontal
                // zlevel:99
                top:'7%',
                left:'center'
            },
            grid: {
                left: '0%',
                right: '9%',
                bottom: '3%',
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
                name:'成交量(股)',
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                    // rotate:45
                },

            },
            color:['#c23531','#749f83','#2f4554'],
            series: [
                {
                    // name:'万科',
                    name: stock,
                    type:'line',
                    // data:[1, 2, 2, 5, 3, 2, 0,4],
                    data: volume_data,
                    showSymbol: true,
                    hoverAnimation: true,
                },
            ]
        };
        myPriceChart_3.hideLoading();
        myPriceChart_3.setOption(option_3);

        // 成交额变化
        var amt_data = data.amt || [];
        // for(var i=0;i<amt_data.length;i++){
        //     amt_data[i] = amt_data[i]/1000000;
        // }
        var option_4 = {
            title: {
                // text: '万科收益率变化',
                text: stock+'成交额变化',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                // data:['大盘指数','万科','差值'],
                // data:[stock,'同行业平均值','差值'],
                data:['成交额'],
                orient:'horizontal',//horizontal
                // zlevel:99
                top:'7%',
                left:'center'
            },
            grid: {
                left: '0%',
                right: '9%',
                bottom: '3%',
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
                name:'成交额(元)',
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                }
            },
            color:['#c23531','#749f83','#2f4554'],
            series: [
                {
                    // name:'万科',
                    name: stock,
                    type:'line',
                    // data:[1, 2, 2, 5, 3, 2, 0,4],
                    data: amt_data,
                    showSymbol: true,
                    hoverAnimation: true,
                },
            ]
        };
        myPriceChart_4.hideLoading();
        myPriceChart_4.setOption(option_4);
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
                            if(row.title.length>150){
                                return '<span style="cursor:pointer;" title="'+row.title+'">'+row.title.substring(0,150)+'...</span>';
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

// 交易分析 // 十大股东
    var top10holders_url = '';



    //  渲染 下拉框
    var seasonBox_url = '/maniPulate/manipulateReport/seasonBox?id=' + id;

    public_ajax.call_request('get',seasonBox_url,seasonBox);
    function seasonBox(data){
        if(data){
            var str = '';
            var flag = true;
            for(var i=0;i<data.length;i++){
                if(data[i].show == 1 || data[i].show == '1' ){
                    flag = false;//有默认选项 不必设置最后一个选中
                    str += '<option value="'+data[i].seasonid+'" selected="selected">'+ data[i].season + '</option>';
                }else {
                    str += '<option value="'+data[i].seasonid+'">'+ data[i].season + '</option>';
                }

            }

            // $('._time2').empty().append(str).children('option:last-child').attr('selected','selected');
            // $('._time2').empty().append(str);
            if(flag == true){
                $('._time2').empty().append(str).children('option:last-child').attr('selected','selected');
            }else {
                $('._time2').empty().append(str);
            }

            top10holders_url = '/maniPulate/manipulateReport/top10holders?id=' + id +'&seasonid=' + $('._time2').val();
            public_ajax.call_request('get',top10holders_url,table3);
        }
    }

    // 更新下拉框时
    $('._time2').change(function(){
        $('#Transaction-1 center.loading').show();
        top10holders_url = '/maniPulate/manipulateReport/top10holders?id=' + id +'&seasonid=' + $(this).val();
        public_ajax.call_request('get',top10holders_url,table3);
    });

    function table3(data) {
        $('#Transaction-1 center.loading').show();

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
                        if (row.holder_name==''||row.holder_name=='null'||row.holder_name=='unknown'||!row.holder_name||row.holder_name=='none' || row.holder_name=='None'){
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
                        if (row.holder_quantity=='null'||row.holder_quantity=='unknown'){
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
                        if (row.holder_pct==''||row.holder_pct=='null'||row.holder_pct=='unknown'){
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
    // var myChart_3 = echarts.init(document.getElementById('Stock_1'),'chalk');
    var myChart_3 = echarts.init(document.getElementById('Stock_1'));
    myChart_3.showLoading();
    var myChart_4 = echarts.init(document.getElementById('Stock_2'));
    myChart_4.showLoading();

    var holderspct_url = '';//股权分析的

    var seasonBoxpct_url = '/maniPulate/manipulateReport/seasonBoxpct?id=' + id;
    public_ajax.call_request('get',seasonBoxpct_url,seasonBoxpct);
    function seasonBoxpct(data){
        if(data){
            var str = '';
            var flag = true;
            for(var i=0;i<data.length;i++){
                if(data[i].show == 1 || data[i].show == '1' ){
                    flag = false;//有默认选项 不必设置最后一个选中
                    str += '<option value="'+data[i].seasonid+'" selected="selected">'+ data[i].season + '</option>';
                }else {
                    str += '<option value="'+data[i].seasonid+'">'+ data[i].season + '</option>';
                }
            }

            $('.shareholding_time').empty().append(str).children('option:last-child').attr('selected','selected');//持股分析的
            if(flag == true){
                $('.shareholding_time').empty().append(str).children('option:last-child').attr('selected','selected');//默认选中最后一个
            }else {
                $('.shareholding_time').empty().append(str);
            }

            holderspct_url = '/maniPulate/manipulateReport/holderspct?id=' + id +'&seasonid='+$('.shareholding_time').val();
            public_ajax.call_request('get',holderspct_url,Stock);
        }
    }

    // var holderspct_url = '/maniPulate/manipulateReport/holderspct?id=' + id +'&seasonid='+$('.shareholding_time').val();
    // public_ajax.call_request('get',holderspct_url,Stock);
    function Stock(data){
        var holder_pctbyinst_data = data.holder_pctbyinst.toFixed(2);      //机构投资者持股
        var holder_notpctbyinst_data = data.holder_notpctbyinst.toFixed(2);//非 机构投资者持股

        var holder_top10pct_data = data.holder_top10pct.toFixed(2);        //十大股东
        var holder_nottop10pct_data = data.holder_nottop10pct.toFixed(2);  //非 十大股东

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
                y:'20%',
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
                y:'20%',
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

    // 假数据  已 弃用
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

    $('.shareholding_time').change(function(){
        myChart_3.showLoading();
        myChart_4.showLoading();
        holderspct_url = '/maniPulate/manipulateReport/holderspct?id=' + id +'&seasonid='+$(this).val();
        public_ajax.call_request('get',holderspct_url,Stock);
    });

    // 折线图
    var myChart_Stock_3 = echarts.init(document.getElementById('Stock_3'));
    var myChart_Stock_4 = echarts.init(document.getElementById('Stock_4'));
    myChart_Stock_3.showLoading();
    myChart_Stock_4.showLoading();
    var holderspctline_url = '/maniPulate/manipulateReport/holderspctline?id=' + id;
    public_ajax.call_request('get',holderspctline_url,holderspctline);
    function holderspctline(data){
        var option_Stock_3 = {
            title: {
                text: stock+'机构投资者持股比例变化',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: '机构投资者持股比例变化',
                orient:'horizontal',
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
                data: data.season,
                axisLabel:{
                    rotate:90
                }
            },
            yAxis: {
                name:'',
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                },
                min:function(value) {
                    return Math.floor(value.min - 5);//向下取整
                },
                // max:function(value) {
                //     return Math.ceil(value.max + 5);//向上取整
                // },
            },
            // color:['#c23531','#749f83','#2f4554'],
            series: [
                {
                    name: '投资者',
                    type:'line',
                    data: data.inst,
                    showSymbol: true,
                    hoverAnimation: true,
                },
            ]
        };
        myChart_Stock_3.hideLoading();
        myChart_Stock_3.setOption(option_Stock_3);

        var option_Stock_4 = {
            title: {
                text: stock+'十大股东持股比例变化',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: '十大股东持股比例变化',
                orient:'horizontal',
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
                data: data.season,
                axisLabel:{
                    rotate:90
                }
            },
            yAxis: {
                name:'',
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                },
                min:function(value) {
                    return Math.floor(value.min - 5);//向下取整
                },
                // max:function(value) {
                //     return Math.ceil(value.max + 5);//向上取整
                // },
            },
            // color:['#c23531','#749f83','#2f4554'],
            series: [
                {
                    // name:'万科',
                    name: '股东',
                    type:'line',
                    data: data.top10,
                    showSymbol: true,
                    hoverAnimation: true,
                },
            ]
        };
        myChart_Stock_4.hideLoading();
        myChart_Stock_4.setOption(option_Stock_4);
    }

// 财报数据
    var profit_url = '/maniPulate/manipulateReport/profit?id=' + id;
    public_ajax.call_request('get',profit_url,profit_table);
    function profit_table(data) {
        $('#profit-content').bootstrapTable('load', data);
        $('#profit-content').bootstrapTable({
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
                    title: "季度",//标题
                    field: "date",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.date=='null'||row.date=='unknown'){
                            return '未知';
                        }else {
                            return row.date;
                        };
                    }
                },
                {
                    title: "净资产收益率(%)",//标题
                    field: "roe",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.roe=='null'||row.roe=='unknown'){
                            return '未知';
                        }else {
                            return row.roe;
                        };
                    }
                },
                {
                    title: "净利率(%)",//标题
                    field: "net_profit_ratio",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.net_profit_ratio=='null'||row.net_profit_ratio=='unknown'){
                            return '-';
                        }else {
                            return row.net_profit_ratio;
                        };
                    }
                },
                {
                    title: "毛利率(%)",//标题
                    field: "gross_profit_rate",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.gross_profit_rate=='null'||row.gross_profit_rate=='unknown'){
                            return '-';
                        }else {
                            return row.gross_profit_rate;
                        };
                    }
                },
                {
                    title: "净利润(万元)",//标题
                    field: "net_profits",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.net_profits=='null'||row.net_profits=='unknown'){
                            return '-';
                        }else {
                            return row.net_profits;
                        };
                    }
                },
                {
                    title: "每股收益",//标题
                    field: "eps",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.eps=='null'||row.eps=='unknown'){
                            return '-';
                        }else {
                            return row.eps;
                        };
                    }
                },
                {
                    title: "营业收入(百万元)",//标题
                    field: "business_income",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.business_income=='null'||row.business_income=='unknown'){
                            return '-';
                        }else {
                            return row.business_income;
                        };
                    }
                },
                {
                    title: "每股主营业务收入(元)",//标题
                    field: "bips",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.bips=='null'||row.bips=='unknown'){
                            return '-';
                        }else {
                            return row.bips;
                        };
                    }
                },
            ],
        });

        $('#profit-content center.loading').hide();
    }

// 历史信用
    var credit_url = '/maniPulate/manipulateReport/credit/?id='+id;
    public_ajax.call_request('get',credit_url,creditHistory);
    // 假数据
        var creditHistoryData = [
            {date:'2018-5-26',type:'证监会判罚',content:'你了发货了看法了按时发啦发啦按身份靠你了我看看你发'},
            {date:'2018-5-26',type:'证监会判罚',content:'你了发货了看法了按时发啦发啦按身份靠你了我看看你发'},
            {date:'2018-5-26',type:'证监会判罚',content:'你了发货了看法了按时发啦发啦按身份靠你了我看看你发'},
            {date:'2018-5-26',type:'证监会判罚',content:'你了发货了看法了按时发啦发啦按身份靠你了我看看你发'},
            {date:'2018-5-26',type:'证监会判罚',content:'你了发货了看法了按时发啦发啦按身份靠你了我看看你发'},
            {date:'2018-5-26',type:'证监会判罚',content:'你了发货了看法了按时发啦发啦按身份靠你了我看看你发'},
            {date:'2018-5-26',type:'证监会判罚',content:'你了发货了看法了按时发啦发啦按身份靠你了我看看你发'},
            {date:'2018-5-26',type:'证监会判罚',content:'你了发货了看法了按时发啦发啦按身份靠你了我看看你发'},
        ];
    function creditHistory(data) {
        $('#creditHistory_content').bootstrapTable('load', data);
        $('#creditHistory_content').bootstrapTable({
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
                    title: "类型",//标题
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
                    title: "摘要",//标题
                    field: "abstract",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.abstract==''||row.abstract=='null'||row.abstract=='unknown'||!row.abstract){
                            return '暂无标题';
                        }else {
                            if(row.abstract.length>150){
                                return '<span style="cursor:pointer;" title="'+row.abstract+'">'+row.abstract.substring(0,150)+'...</span>';
                            }else {
                                return row.abstract;
                            }
                        };
                    }
                },
            ],
        });

        $('#creditHistory_content center.loading').hide();
    }
    // creditHistory(creditHistoryData)