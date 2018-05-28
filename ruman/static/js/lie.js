// 基本信息 ====
    var infor_url = '/rumor/get_rumor_infor?en_name='+en_name;
    // console.log(infor_url);
    public_ajax.call_request('get',infor_url,infor);
    function infor(data){
        $('#card .type-1').text(data.query_kwds).attr('title',data.query_kwds);
        $('#card .type-2').text(data.publish_time).attr('title',data.publish_time);
        $('#card .type-3').text(data.author).attr('title',data.author);
        $('#card .type-4').text(data.comment).attr('title',data.comment);
        $('#card .type-5').text(data.retweeted).attr('title',data.retweeted);
        $('#card .hotContent #hotContent').text(data.text);
    }

// 发布者画像 ====
    var pageData = 10;
    var radiusNum = 102;
    if(screen.width<1920){
        pageData = 5;
        radiusNum = 66;
        $('.evaluate-sp').css('margin-bottom','0');
    }else {
        $('.evaluate-sp').css('margin-bottom','.1rem');
    }

    var weibo_num;
    // 基本信息
        // var card_url = '/attribute/new_user_profile/?uid=3069348215';//测试的
        var card_url = '/attribute/new_user_profile/?uid='+uid;
        public_ajax.call_request('get',card_url,card);

        function card(data){
            if(data.photo_url != '' && data.photo_url != null && data.photo_url != 'unknown' && data.photo_url != '未知'){
                $('#userImage .user-img img').attr('src',data.photo_url);//发布者画像头像
            }else {
                $('#userImage .user-img img').attr('src','/static/images/unknown.png');//发布者画像头像
            }

            $('#userImage .evaluate .description').empty().html('<b>描述</b> '+data.description).attr('title',data.description);//描述
            $('#userImage .evaluate .friendsnum').empty().html('<b>好友数</b> '+data.friendsnum).attr('title',data.friendsnum);//好友数
            $('#userImage .evaluate .fansnum').empty().html('<b>粉丝数</b> '+data.fansnum).attr('title',data.fansnum);//粉丝数
            $('#userImage .evaluate .statusnum').empty().html('<b>发布信息数</b> '+data.statusnum).attr('title',data.statusnum);//发布信息数

            weibo_num = data.statusnum;

            $('#userImage .background-information span.nick_name').attr('title',data.nick_name).find('b').text(data.nick_name);//昵称
            $('#userImage .background-information span.user_id').attr('title',data.id).find('b').text(data.id);//id

            var create_tm=getLocalTime(data.create_at);
            $('#userImage .background-information span.create_tm').attr('title',create_tm).find('b').text(create_tm);//注册时间

            var now_timestamp=new Date().getTime();//当前时间戳
            var timestamp = (now_timestamp/1000) - data.create_at;

            var year = Math.floor(timestamp/86400/365);
            var day = Math.floor(timestamp/86400%365);
            // console.log(year);
            // console.log(day);

            $('#userImage .background-information span.Registration_length').attr('title',year+'年'+day+'天').find('b').text(year+'年'+day+'天');//注册时长

            $('#userImage .background-information span.location').attr('title',data.user_location).find('b').text(data.user_location);//注册地

            var iSverified_type = '未知';
            if(data.verified_type == -1){
                iSverified_type = '否';
            }else {
                iSverified_type = '是';
            }
            $('#userImage .background-information span.iSverified_type').attr('title',iSverified_type).find('b').text(iSverified_type);//是否认证
            $('#userImage .background-information span.verified_type').attr('title',data.verified_type_ch).find('b').text(data.verified_type_ch);//认证类型
            var sex = '未知';
            if(data.sex == 1){
                sex = '男';
            }else if(data.sex == 2){
                sex = '女';
            }
            $('#userImage .background-information span.sex').attr('title',sex).find('b').text(sex);//性别

            var blogUrl = 'http://weibo.com/u/'+data.uid;
            if(data.blog_url != ''){
                blogUrl = data.blog_url;
            }
            $('#userImage .background-information span.blog_url').attr('title',blogUrl).find('a').text(blogUrl).attr('href',blogUrl);//微博地址
        }

    // 整体评价
        // var evaluate_url = '/attribute/new_user_evaluate/?uid=3069348215';//测试的
        var evaluate_url = '/attribute/new_user_evaluate/?uid='+uid;
        public_ajax.call_request('get',evaluate_url,evaluate);
        function evaluate(data){
            var activenessStr = '';
            if(data.activeness[0] == '' && data.activeness[1] == '' && data.activeness[2] == '' && data.activeness[3] == ''){
                activenessStr = '<b>活跃度</b> '+ 0 ;
            }else {
                activenessStr = '<b>活跃度</b> '+data.activeness[0].toFixed(2) + ' (No.'+data.activeness[1]+'/'+data.activeness[4]+') '+'最高值'+data.activeness[2].toFixed(2)+'/最低值'+data.activeness[3].toFixed(2);
            }
            // var activenessStr = '<b>活跃度</b> '+data.activeness[0].toFixed(2) + ' (No.'+data.activeness[1]+'/'+data.activeness[4]+') '+'最高值'+data.activeness[2].toFixed(2)+'/最低值'+data.activeness[3].toFixed(2);
            $('.activeness').empty().html(activenessStr);
            // data.activeness[0].toFixed(2) 平均数
            // data.activeness[1] 排名
            // data.activeness[2].toFixed(2) 最高值
            // data.activeness[3].toFixed(2) 最低值
            // data.activeness[4] 总数

            var influenceStr = '';
            if(data.influence[0] == '' && data.influence[1] == '' && data.influence[2] == '' && data.influence[3] == ''){
                influenceStr = '<b>影响力</b> '+ 0 ;
            }else {
                influenceStr = '<b>影响力</b> '+data.influence[0].toFixed(2) + ' (No.'+data.influence[1]+'/'+data.influence[4]+') '+'最高值'+data.influence[2].toFixed(2)+'/最低值'+data.influence[3].toFixed(2);
            }
            // var influenceStr = '<b>影响力</b> '+data.influence[0].toFixed(2) + ' (No.'+data.influence[1]+'/'+data.influence[4]+') '+'最高值'+data.influence[2].toFixed(2)+'/最低值'+data.influence[3].toFixed(2);
            $('.influence').empty().html(influenceStr);
            // data.influence[0].toFixed(2) 平均数
            // data.influence[1] 排名
            // data.influence[2].toFixed(2) 最高值
            // data.influence[3].toFixed(2) 最低值
            // data.influence[4] 总数

            var importanceStr = '';
            if(data.importance[0] == '' && data.importance[1] == '' && data.importance[2] == '' && data.importance[3] == ''){
                importanceStr = '<b>重要度</b> '+ 0 ;
            }else {
                importanceStr = '<b>重要度</b> '+data.importance[0].toFixed(2) + ' (No.'+data.importance[1]+'/'+data.importance[4]+') '+'最高值'+data.importance[2].toFixed(2)+'/最低值'+data.importance[3].toFixed(2);
            }
            // var importanceStr = '<b>重要度</b> '+data.importance[0].toFixed(2) + ' (No.'+data.importance[1]+'/'+data.importance[4]+') '+'最高值'+data.importance[2].toFixed(2)+'/最低值'+data.importance[3].toFixed(2);
            $('.importance').empty().html(importanceStr);
            // data.importance[0].toFixed(2) 平均数
            // data.importance[1] 排名
            // data.importance[2].toFixed(2) 最高值
            // data.importance[3].toFixed(2) 最低值
            // data.importance[4] 总数
        }

    // 相关微博
        // var weibo_url = '/attribute/new_user_weibo/?uid=3069348215&sort_type=timestamp';//测试的
        var weibo_url = '/attribute/new_user_weibo/?uid='+uid+'&sort_type=timestamp';
        public_ajax.call_request('get',weibo_url,userWeibo);
        function userWeibo(data){
            $('#userWeibo').bootstrapTable('load', data);
            $('#userWeibo').bootstrapTable({
                data:data,
                search: false,//是否搜索
                pagination: true,//是否分页
                pageSize: 5,//单页记录数
                // pageList: [15,20,25],//分页步进值
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
                            // row --- [
                            // "4046163315603407",
                            // "3069348215",
                            // "哈哈哈哈哈哈哈哈哈神经病//@HaoRabbit：射手就是莫名其妙就笑了起来的那种人[微笑]",    【内容】
                            // "219.236.29.48",  【发布IP】
                            // null,  【发布地址】
                            // 1480163971,
                            // "2016-11-26 20:39:31",  【时间】
                            // 0,   【转发数】
                            // 0,   【评论数】
                            // 0,   【点赞数】
                            // "http://weibo.com/3069348215/EjmUXnvHx"
                            // ],
                            var address = '未知';//发布地址
                            if(row[4] != null && row[4] != ''){
                                address = row[4];
                            }
                            return '<div class="center_rel">'+
                                        '<div>'+
                                            '<img src="/static/images/unknown.png" alt="" class="center_icon">'+
                                            '<a href="###" class="center_1" style="color:#ff9645;font-weight:700;">'+row[1]+'</a>'+
                                            '<span class="time" style="font-weight:900;color:#337ab7;font-weight:400;margin-left:10px;">'+
                                                '&nbsp;&nbsp;IP:'+row[3]+
                                                '&nbsp;&nbsp;地址:'+address+
                                            '</span>'+

                                            '<span style="margin-left:10px;">'+row[2]+'</span>'+
                                            '&nbsp;&nbsp;<a href="'+row[10]+'" target="_blank">原文</a>'+
                                        '</div>'+
                                        '<div class="clearfix" style="margin-top:8px;">'+
                                            '<span class="time pull-left" style="font-weight:900;color:#337ab7;font-weight:400;">'+
                                                '<i class="icon icon-time">&nbsp;'+row[6]+'</i>'+
                                            '</span>'+
                                            '<span class="pull-right"">'+
                                                '<span class="retweet_count">转发数('+row[7]+')</span>&nbsp;&nbsp;|&nbsp;&nbsp;'+
                                                '<span class="retweet_count">评论数('+row[8]+')</span>&nbsp;&nbsp;|&nbsp;&nbsp;'+
                                                '<span class="retweet_count">点赞数('+row[9]+')</span>'+
                                            '</span>'+
                                        '</div>'+
                                    '</div>';
                        }
                    },
                ],
            });
            $('#userWeibo p.load').hide();
        }

    // 影响力技能 雷达图
        // 设置 影响力雷达图 下面的div的padding-top
        $('.effect>div').css('padding-top',$('.effect h4').outerHeight());
        // 影响力雷达图
            var myChart_originalSkill = echarts.init(document.getElementById('originalSkill'));
            var myChart_spreadSkill = echarts.init(document.getElementById('spreadSkill'));
            myChart_originalSkill.showLoading();
            myChart_spreadSkill.showLoading();

            // function radar(boxId,tit,subtit,indicatorData,data,seriesName){
            function radar(myChart,tit,subtit,indicatorData,data,seriesName){
                // var myChart = echarts.init(document.getElementById(boxId));
                var option = {
                    title: {
                        text: tit,
                        subtext:subtit
                    },
                    tooltip: {},
                    legend: {
                        // data: ['预算分配（Allocated Budget）', '实际开销（Actual Spending）']
                    },
                    radar: {
                        // shape: 'circle',
                        name: {
                            textStyle: {
                                color: '#fff',
                                backgroundColor: '#999',
                                borderRadius: 3,
                                padding: [3, 5]
                            }
                        },
                        // indicator: [
                        //     { name: '质疑度', max: 60},
                        //     { name: '发布者可疑度', max: 60},
                        //     { name: '扩散速度', max: 60},
                        //     { name: '波及人次', max: 60},
                        //     { name: '评论数', max: 60},
                        //     { name: '转发数', max: 60}
                        // ]
                        indicator:indicatorData,
                        center : ['50%', '55%'],
                        // radius: 102
                        radius: radiusNum
                    },
                    series: [{
                        name: '',
                        type: 'radar',
                        // areaStyle: {normal: {}},
                        data : [
                            {
                                // value : [60,15,10,50,30,40],
                                value : data,
                                // name : '预算分配（Allocated Budget）'
                                name : seriesName
                            },
                            //  {
                            //     value : [5000, 14000, 28000, 31000, 42000, 21000],
                            //     name : '实际开销（Actual Spending）'
                            // }
                        ]
                    }]
                };
                myChart.hideLoading();
                myChart.setOption(option)
            }
            var originalSkill_indicatorData = [
                { name: '原创数', max: 100},
                { name: '原创被转发数', max: 100},
                { name: '原创被评论数', max: 100},
                { name: '原创微博转发速度', max: 100},
                { name: '原创微博评论速度', max: 100},
            ];
            // var originalSkill_Data = [];
            // for (var i=0;i<6;i++){
            //     originalSkill_Data.push(Math.floor(Math.random()*100+1))
            // }
            var spreadSkill_indicatorData = [
                { name: '转发数', max: 100},
                { name: '评论数', max: 100},
                { name: '转发微博被转发数', max: 100},
                { name: '转发微博被评论数', max: 100},
                { name: '转发微博转发速度', max: 100},
            ];
            // var spreadSkill_Data = [];
            // for (var i=0;i<6;i++){
            //     spreadSkill_Data.push(Math.floor(Math.random()*100+1))
            // }
            // radar('originalSkill','原创技能','网红必备技能一',originalSkill_indicatorData,originalSkill_Data);
            // radar('spreadSkill','传播技能','网红必备技能二',spreadSkill_indicatorData,spreadSkill_Data);

        // var influenceApplication_url = '/influence_application/specified_user_active/?date=2016-05-21&uid=3069348215';//测试的
        var influenceApplication_url = '/influence_application/specified_user_active/?date=2016-05-21&uid='+uid;

        setTimeout(function(){
            public_ajax.call_request('get',influenceApplication_url,influenceApplication);
        },1000)
        function influenceApplication(data){
            // console.log(weibo_num);
            var data = data[0];

            // ==================
            // console.log("====原创技能====")
            // ==================

            // console.log(weibo_num/399139, data.origin_weibo_retweeted_total_number/1009130, data.origin_weibo_comment_total_number/241403, data.origin_weibo_comment_brust_average/36345.5, data.origin_weibo_retweeted_brust_average/79278);
            var radius_1=Math.max(weibo_num/399139, data.origin_weibo_retweeted_total_number/1009130, data.origin_weibo_comment_total_number/241403, data.origin_weibo_comment_brust_average/36345.5, data.origin_weibo_retweeted_brust_average/79278);
            // console.log(radius_1);

            var k=100/radius_1;
            // console.log(k*weibo_num/399139, k*data.origin_weibo_retweeted_total_number/1009130, k*data.origin_weibo_comment_total_number/241403, k*data.origin_weibo_comment_brust_average/36345.5, k*data.origin_weibo_retweeted_brust_average/79278);

            // 原创技能
            var originalSkill_Data = [];
            originalSkill_Data.push(k*weibo_num/399139+10, k*data.origin_weibo_retweeted_total_number/1009130+20, k*data.origin_weibo_comment_total_number/241403, k*data.origin_weibo_retweeted_brust_average/79278, k*data.origin_weibo_comment_brust_average/36345.5);
            for(var i=0;i<originalSkill_Data.length;i++){
                originalSkill_Data[i] = originalSkill_Data[i].toFixed(2);
            }
            // console.log(originalSkill_Data);
            // radar('originalSkill','原创技能','网红必备技能一',originalSkill_indicatorData,originalSkill_Data,'原创技能相对排位');
            radar(myChart_originalSkill,'原创技能','网红必备技能一',originalSkill_indicatorData,originalSkill_Data,'原创技能相对排位');

            // ==================
            // console.log("====传播技能====")
            // ==================

            // console.log(data.retweeted_weibo_number/85378, data.comment_weibo_number/1, data.retweeted_weibo_retweeted_total_number/169076, data.retweeted_weibo_comment_total_number/7074, data.retweeted_weibo_retweeted_brust_average/6434.5);
            var radius_2=Math.max(data.retweeted_weibo_number/85378, data.comment_weibo_number/1, data.retweeted_weibo_retweeted_total_number/169076, data.retweeted_weibo_comment_total_number/7074, data.retweeted_weibo_retweeted_brust_average/6434.5);
            var k2=100/radius_2;
            // 传播技能
            var spreadSkill_Data = [];
            spreadSkill_Data.push(k2*data.retweeted_weibo_number/85378+20, k2*data.comment_weibo_number/1+10, k2*data.retweeted_weibo_retweeted_total_number/169076, k2*data.retweeted_weibo_comment_total_number/7074, k2*data.retweeted_weibo_retweeted_brust_average/6434.5);
            for(var j=0;j<spreadSkill_Data.length;j++){
                spreadSkill_Data[j] = spreadSkill_Data[j].toFixed(2);
            }
            // console.log(spreadSkill_Data);
            // radar('spreadSkill','传播技能','网红必备技能二',spreadSkill_indicatorData,spreadSkill_Data,'传播技能相对排位');
            radar(myChart_spreadSkill,'传播技能','网红必备技能二',spreadSkill_indicatorData,spreadSkill_Data,'传播技能相对排位');
        }

    // 社交特征
        // 谁关注我
            // var social_url = '/info_person_social/follower/?uid=3069348215';//测试的
            var social_url = '/info_person_social/follower/?uid='+uid;
            public_ajax.call_request('get',social_url,social);
            function social(data){
                $('#attention-1Table').bootstrapTable('load', data);
                $('#attention-1Table').bootstrapTable({
                    data:data,
                    search: false,//是否搜索
                    pagination: true,//是否分页
                    // pageSize: 10,//单页记录数
                    pageSize: pageData,//单页记录数
                    // pageList: [15,20,25],//分页步进值
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
                                // row --- {
                                //     count: 108,    交互次数 鼠标悬停显示
                                //     uname: "未知",  未知则显示 uid前几位
                                //     weibo_count: "",
                                //     uid: "5565680411",
                                //     fansnum: "",
                                //     friendsnum: "",
                                //     influence: "",
                                //     photo_url: ""    未知 则显示默认头像
                                // },
                                var imgSrc = '/static/images/unknown.png';// 默认头像地址
                                if(row.photo_url != null && row.photo_url != '' && row.photo_url != 'unknown' && row.photo_url != '未知'){
                                    imgSrc = row.photo_url;
                                }
                                var uname = row.uname;
                                if(row.uname == '未知' || row.uname == null || row.uname == '' || row.uname == 'unknown'){
                                    uname = row.uid;
                                }
                                return '<div class="attentioncontent-1" title="交互次数：'+row.count+'">'+
                                            '<img src="'+imgSrc+'" alt="">'+
                                            '<br>'+
                                            '<span>'+uname+'</span>'+
                                        '</div>';
                            }
                        },
                    ],
                });
                $('#attention-1Table p.load').hide();
            }

        // 我关注谁
            // var attention_url = '/info_person_social/attention/?uid=3069348215';//测试的
            var attention_url = '/info_person_social/attention/?uid='+uid;
            public_ajax.call_request('get',attention_url,attention);
            function attention(data){
                $('#attention-2Table').bootstrapTable('load', data);
                $('#attention-2Table').bootstrapTable({
                    data:data,
                    search: false,//是否搜索
                    pagination: true,//是否分页
                    pageSize: 10,//单页记录数
                    // pageList: [15,20,25],//分页步进值
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
                                // row --- {
                                //     count: 108,    交互次数 鼠标悬停显示
                                //     uname: "未知",  未知则显示 uid前几位
                                //     weibo_count: "",
                                //     uid: "5565680411",
                                //     fansnum: "",
                                //     friendsnum: "",
                                //     influence: "",
                                //     photo_url: ""    未知 则显示默认头像
                                // },
                                var imgSrc = '/static/images/unknown.png';// 默认头像地址
                                if(row.photo_url != null && row.photo_url != '' && row.photo_url != 'unknown' && row.photo_url != '未知'){
                                    imgSrc = row.photo_url;
                                }
                                var uname = row.uname;
                                if(row.uname == '未知' || row.uname == null || row.uname == '' || row.uname == 'unknown'){
                                    uname = row.uid;
                                }
                                return '<div class="attentioncontent-1" title="交互次数：'+row.count+'">'+
                                            '<img src="'+imgSrc+'" alt="">'+
                                            '<br>'+
                                            '<span>'+uname+'</span>'+
                                        '</div>';
                            }
                        },
                    ],
                });
                $('#attention-2Table p.load').hide();
            }

// 语义分析 ====
    // 观点聚类 （暂弃用）
        var ViewpointData = [
            {num:1,a:'正面',Percentage:'30%',title_1:'独狼行动',title_2:'资本有方',title_3:'张百忍',con_1:'计划经济正式回归',con_2:'水泥先行！冀东先行',con_3:'不错，跟上形势'},
            {num:2,a:'负面',Percentage:'60%',title_1:'悟空说他很傻',title_2:'谁吾与从001',title_3:'ICE__XU',con_1:'搞来搞去还是只有搞地产',con_2:'抵制万科，不买它的任何产品',con_3:'野鸡新闻'},
            {num:3,a:'正面',Percentage:'30%',title_1:'独狼行动',title_2:'资本有方',title_3:'张百忍',con_1:'计划经济正式回归',con_2:'水泥先行！冀东先行',con_3:'不错，跟上形势'},
            {num:4,a:'负面',Percentage:'60%',title_1:'独狼行动',title_2:'资本有方',title_3:'张百忍',con_1:'计划经济正式回归',con_2:'水泥先行！冀东先行',con_3:'不错，跟上形势'}
        ];
        function Viewpoint(data){
            $('#Viewpoint-clustering').bootstrapTable('load', data);
            $('#Viewpoint-clustering').bootstrapTable({
                data:data,
                search: false,//是否搜索
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
                            return '<div class="inforContent">'+
                                '<div class="main">'+
                                '<p class="option">'+
                                '<span>观点<b>'+row.num+'</b></span>'+
                                '<span style="margin:0 10px;"><b>'+row.a+'</b></span>'+
                                '<span><b>'+row.Percentage+'</b></span>'+
                                '<span class="moreInfo">查看更多</span>'+
                                '</p>'+
                                '<div class="context">'+
                                '<p style="margin:10px 0;"><span style="font-weight: 700;color:#1f4e79;"><img src="/static/images/textIcon.png" class="textFlag" style="top: 8px;margin-right:5px;">'+row.title_1+':</span><span>'+row.con_1+'</span></p>'+
                                '<p style="margin:10px 0;"><span style="font-weight: 700;color:#1f4e79;"><img src="/static/images/textIcon.png" class="textFlag" style="top: 8px;margin-right:5px;">'+row.title_2+':</span><span>'+row.con_2+'</span></p>'+
                                '<p style="margin:10px 0;"><span style="font-weight: 700;color:#1f4e79;"><img src="/static/images/textIcon.png" class="textFlag" style="top: 8px;margin-right:5px;">'+row.title_3+':</span><span>'+row.con_3+'</span></p>'+
                                '</div>'+
                                '</div>';
                        }
                    }
                ],
            });
        }
        // Viewpoint(ViewpointData);

    // 字符云 ====

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
                    var wordCloud_myChart = ec.init(document.getElementById('word-1'),'chalk');
                    wordCloud_myChart.showLoading({
                        text: '加载中...',
                    });

                    // var wordCloudurl = '/topic_language_analyze/during_keywords/?topic=te-lang-pu-ji-xin-ge-1492166854&start_ts=1478736000&end_ts=1480176000';//测试的
                    var wordCloudurl = '/topic_language_analyze/during_keywords/?topic='+en_name+'&start_ts=1478736000&end_ts=1480176000';
                    public_ajax.call_request('get',wordCloudurl,wordCloud_L);
                    function wordCloud_L(data){
                        var seriesData = [];
                        for(var i=0;i<data.length;i++){
                            seriesData.push({
                                itemStyle: createRandomItemStyle(),
                                name: data[i][0],
                                value: (data[i][1]*10000).toFixed(2)
                            })
                        }

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
                                // 假数据
                                    // data: [
                                    //     {
                                    //         name: "我要金蛋",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "屹农金服",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "理财去",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "联投银帮",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "弘信宝",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "网惠金融",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "晶行财富",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "孺牛金服",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "摩根浦捷贷",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "知屋理财",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "沪臣地方金融",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "升隆财富",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "冰融贷",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "靠谱鸟",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "速溶360",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "存米网",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    //     {
                                    //         name: "太保金服",
                                    //         value: 999,
                                    //         itemStyle: createRandomItemStyle()
                                    //     },
                                    // ]
                                data: seriesData
                            }]
                        };

                        wordCloud_myChart.hideLoading();
                        wordCloud_myChart.setOption(option);
                    }
                }
            );
        }
        keywords();

    // 主题时间轴 ====
            // var topic_source_val = $('#semanticsSource_select').val();
            // var topicaxis_url = '/hotSpot/hotspotReport/topicaxis/?source='+topic_source_val+'&id='+id;//
            // var topicaxis_url = '/topic_language_analyze/symbol_weibos/?topic=te-lang-pu-ji-xin-ge-1492166854&start_ts=1478736000&end_ts=1480204800';//测试的
            var topicaxis_url = '/topic_language_analyze/symbol_weibos/?topic='+en_name+'&start_ts=1478736000&end_ts=1480204800';

            public_ajax.call_request('get',topicaxis_url,topicaxis);
            function topicaxis(data){

                // console.log(data[0]);
                // for (var key in data){
                //     console.log(key);
                //     console.log(data[key]);
                // }
                var classLR = 'pos-left';

                var str = '';
                if(data.length == 0 || data == 0){
                    $('.VivaTimeline').empty().html('<center>暂无记录</center>');;
                }else {
                    for (var key in data){

                        if(classLR == 'pos-left'){
                            classLR = 'pos-right';
                        }else if(classLR == 'pos-right'){
                            classLR = 'pos-left';
                        }
                        str += '<dd class="'+classLR+' clearfix">'+
                                    '<div class="circ"></div>'+
                                    '<div class="time">'+data[key][0].datetime+'</div>'+
                                    '<div class="events">'+
                                        '<div class="events-header">'+key+'</div>'+
                                        '<div class="events-body">'+
                                            '<div class="row">'+
                                                '<div class="events-desc">'+data[key][0].content+

                                                '</div>'+
                                            '</div>'+
                                            /*


                                                <div class="row">
                                                    <div class="col-md-6 pull-left">
                                                        <img class="events-object img-responsive img-rounded" src="/static/images/VivaTimeline/dog01.jpeg" />
                                                    </div>
                                                    <div class="events-desc">
                                                        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-6 pull-left">
                                                        <img class="events-object img-responsive img-rounded" src="/static/images/VivaTimeline/dog02.jpeg" />
                                                    </div>
                                                    <div class="events-desc">
                                                        Morbi at nisi vitae mauris pretium egestas. Morbi placerat risus ligula, nec placerat urna porta vel. Nullam sollicitudin orci quis odio eleifend, ut facilisis orci lobortis. Vivamus sed lobortis odio. Nam volutpat, leo a ullamcorper luctus, sapien libero auctor est, sed semper massa turpis sed quam. Mauris posuere, libero in ultricies dignissim, lacus purus egestas urna, nec semper lorem tellus non eros. Nam at bibendum libero. Curabitur a ante et orci cursus tincidunt. Vivamus dictum, libero et rhoncus congue, nulla erat mollis dui, vitae cursus dui justo quis velit. In a tellus arcu. Nam at lobortis nisl. Donec consequat placerat eros, quis elementum mauris sodales a. Maecenas id feugiat velit. Phasellus dictum eleifend varius. Cras nec orci turpis. Aenean ut turpis nibh.
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-6 pull-left">
                                                        <img class="events-object img-responsive img-rounded" src="/static/images/VivaTimeline/dog03.jpeg" />
                                                    </div>
                                                    <div class="events-desc">
                                                        Cras condimentum, metus ut vehicula euismod, odio massa pulvinar neque, id gravida neque est et sem. Proin consequat id nibh quis molestie. Quisque vehicula purus id purus elementum facilisis. Phasellus sodales nibh quis neque rhoncus aliquet. Nunc eget ipsum efficitur, pretium arcu et, gravida purus. Phasellus tempor lacus ac enim pulvinar elementum. Integer aliquet justo lacinia nunc tempus vulputate.
                                                    </div>
                                                </div>
                                             */
                                        '</div>'+
                                        '<div class="events-footer">'+
                                        '</div>'+
                                    '</div>'+
                                '</dd>';
                    }
                }
                $('.VivaTimeline dl').empty().html(str);

                $('.VivaTimeline').vivaTimeline({
                    // carousel: true,//自动轮播
                    carousel: false,//自动轮播 关闭
                    // carouselTime: 2000//轮播间隔
                });
            }
            // 更改下拉框
            // $('#semanticsSource_select').change(function(){
            //     topic_source_val = $(this).val();
            //     topicaxis_url = '/hotSpot/hotspotReport/topicaxis/?source='+topic_source_val+'&id='+id;
            //     public_ajax.call_request('get',topicaxis_url,topicaxis);
            // });

    // 观点微博 ====
        // var  weiboOpinion_url = '/topic_language_analyze/weibo_content/?topic=pu-jin-hui-1491486370&start_ts=1478736000&end_ts=1480176000&opinion=';

        // // 先获取 观点 opinion
        // var opinion_url = '/topic_language_analyze/subopinion/?topic=pu-jin-hui-1491486370';
        // public_ajax.call_request('get',opinion_url,opinion);
        // function opinion(data){
        //     var str = '';
        //     for(var i=0;i<data.length;i++){
        //         str += '<span class="opinionChild">'+data[i][0]+'</span>';
        //     }
        //     $('.opinion').empty().append(str);

        //     // 请求第一个观点的微博
        //     weiboOpinion_url = '/topic_language_analyze/weibo_content/?topic=pu-jin-hui-1491486370&start_ts=1478736000&end_ts=1480176000&opinion='+data[0][0];
        //     public_ajax.call_request('get',weiboOpinion_url,weiboOpinion);
        // }

        // $('.opinion').on('click','span',function(){//给动态生成的元素绑定事件
        //     $('#word-3content p.load').show();
        //     // console.log($(this).text());
        //     weiboOpinion_url = '/topic_language_analyze/weibo_content/?topic=pu-jin-hui-1491486370&start_ts=1478736000&end_ts=1480176000&opinion='+$(this).text();
        //     public_ajax.call_request('get',weiboOpinion_url,weiboOpinion);
        // });


        var demoData = [
            [
            "4046163315603407",
            "3069348215",
            "哈哈哈哈哈哈哈哈哈神经病//@HaoRabbit：射手就是莫名其妙就笑了起来的那种人[微笑]",
            "219.236.29.48",
            null,
            1480163971,
            "2016-11-26 20:39:31",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EjmUXnvHx"
            ],
            [
            "4046118143352613",
            "3069348215",
            "处女座是浩瀚宇宙里边绝无仅有，可攻可受，可萌可恨，雌雄同体，收放自如的一个存在。不问你怕不怕，就问你服不服。[摊手]",
            "106.121.75.165",
            null,
            1480153201,
            "2016-11-26 17:40:01",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EjlK6e4ap"
            ],
            [
            "4046049264193760",
            "3069348215",
            "比起爱，水瓶，天秤，双子更希望和懂TA们的人在一起。爱有的时候会累，至少理解彼此的相处起来不累。当然在理解的基础上相爱更好。[doge]",
            "106.121.3.246",
            null,
            1480136779,
            "2016-11-26 13:06:19",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EjjX0hAZi"
            ],
            [
            "4046020067146416",
            "3069348215",
            "哈哈哈哈哈哈哈哈哈//@竟敢比我萌：金牛座 别说看见sb 躲远了 看见自己喜欢的人 都能躲远了[喵喵][喵喵]🙊🙊",
            "219.236.29.48",
            null,
            1480129818,
            "2016-11-26 11:10:18",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EjjbUtZ6M"
            ],
            [
            "4045842355041936",
            "3069348215",
            "马评论！",
            "219.236.29.48",
            null,
            1480087448,
            "2016-11-25 23:24:08",
            0,
            0,
            0,
            "http://weibo.com/3069348215/Ejezhl9Dy"
            ],
            [
            "4045463919207522",
            "3069348215",
            "中送粉！ //@当时我就震惊了:转发这条视频，我会抽5位粉丝每人100元现金，感恩有你[心]",
            "219.236.29.48",
            null,
            1479997222,
            "2016-11-24 22:20:22",
            211,
            6,
            0,
            "http://weibo.com/3069348215/Ej4ITCDiq"
            ],
            [
            "4045453350053922",
            "3069348215",
            "外卖小哥，即将成为各高校里仅次于快递小哥的撩妹高手了嘛[doge][doge]啊不，撩汗也可能哒哒哒哒⸜(ّᶿധّᶿ)⸝",
            "223.73.60.127",
            null,
            1479994701,
            "2016-11-24 21:38:21",
            1705,
            2,
            0,
            "http://weibo.com/3069348215/Ej4rRe1I"
            ],
            [
            "4045443874655056",
            "3069348215",
            "我发起了一个投票 【你觉得十二星座谁最渣？】http://t.cn/Rf9gLsV",
            "219.236.29.48",
            null,
            1479992443,
            "2016-11-24 21:00:43",
            18,
            15742,
            0,
            "http://weibo.com/3069348215/Ej4czjwZy"
            ],
            [
            "4045418033370624",
            "3069348215",
            "回复@送你一杯雪沾酒:我1米8[摊手]",
            "106.121.7.19",
            null,
            1479986282,
            "2016-11-24 19:18:02",
            0,
            0,
            0,
            "http://weibo.com/3069348215/Ej3wTe8QU"
            ],
            [
            "4045382591708757",
            "3069348215",
            "感恩拥有的一切 和你们[爱你]",
            "1.202.40.234",
            null,
            1479977832,
            "2016-11-24 16:57:12",
            177,
            325,
            0,
            "http://weibo.com/3069348215/Ej2BJ7awB"
            ],
            [
            "4045364199728417",
            "3069348215",
            "就酱紫[摊手] //@_种花家的兔子_yue:转发微博 http://t.cn/Rf9Rxf2",
            "1.202.40.234",
            null,
            1479973447,
            "2016-11-24 15:44:07",
            180,
            13,
            0,
            "http://weibo.com/3069348215/Ej283EONX"
            ],
            [
            "4045316204874320",
            "3069348215",
            "猛点头.gif//@柠檬味小姐姐：处女座：逼逼是在乎你 不在乎你鸟都不鸟你",
            "1.202.40.234",
            null,
            1479962004,
            "2016-11-24 12:33:24",
            997,
            63,
            0,
            "http://weibo.com/3069348215/Ej0SEks24"
            ],
            [
            "4045286005511705",
            "3069348215",
            "处女座把最美好的时光都献给了两件事 逼逼别人和逼逼自己。[摊手]",
            "1.202.40.234",
            null,
            1479954804,
            "2016-11-24 10:33:24",
            72,
            4,
            0,
            "http://weibo.com/3069348215/Ej05Wn7Qt"
            ],
            [
            "4045120749530971",
            "3069348215",
            "啊啊啊啊啊啊啊啊啊！",
            "219.236.29.48",
            null,
            1479915404,
            "2016-11-23 23:36:44",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiVNoDZrl"
            ],
            [
            "4045117012454289",
            "3069348215",
            "[心]",
            "219.236.29.48",
            null,
            1479914513,
            "2016-11-23 23:21:53",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiVHnaitj"
            ],
            [
            "4045113036743554",
            "3069348215",
            "恭喜@杜安Duane 获得【范冰冰亲笔签名处女座搪胶公仔】。微博官方唯一抽奖工具@微博抽奖平台 对本次抽奖进行监督，结果公正有效。公证链接：http://t.cn/RfK1mYU",
            "10.75.13.70",
            null,
            1479913565,
            "2016-11-23 23:06:05",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiVAXsij0"
            ],
            [
            "4045077821197943",
            "3069348215",
            "我替你问问//@爱笑的夹心：内容我先不看，我就想问问，双子跟水瓶到底配不配？[摊手]",
            "1.202.40.234",
            null,
            1479905169,
            "2016-11-23 20:46:09",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiUGa51DF"
            ],
            [
            "4045065380525261",
            "3069348215",
            "是我 //@小野妹子学吐槽:是我//@日式冷吐槽:是我//@草沐灰：必须5:40，让别人多等一分钟我就不好受",
            "106.121.7.19",
            null,
            1479902203,
            "2016-11-23 19:56:43",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiUm62cDX"
            ],
            [
            "4045058690366876",
            "3069348215",
            "十二星座如何走出情伤？你需要一个摆渡人！[doge]",
            "10.73.14.39",
            null,
            1479900608,
            "2016-11-23 19:30:08",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiUbj1xrm"
            ],
            [
            "4045034019879386",
            "3069348215",
            "想哭但是哭不出来 //@我爱大黄瓜s:其实不是的 伤的都记心里了 只是脸还是笑的 也许笑的太真了 所以大家都觉得我们无所谓了",
            "1.202.40.234",
            null,
            1479894726,
            "2016-11-23 17:52:06",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiTxvFs4W"
            ],
            [
            "4044946673435078",
            "3069348215",
            "[伤心]//@七月与十四_：她看起来很酷 可好孤独",
            "1.202.40.234",
            null,
            1479873900,
            "2016-11-23 12:05:00",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiRgDepCu"
            ],
            [
            "4044747540619748",
            "3069348215",
            "还有一个星座不敢黑[摊手]",
            "219.236.29.48",
            null,
            1479826424,
            "2016-11-22 22:53:44",
            72,
            4,
            0,
            "http://weibo.com/3069348215/EiM5s2BdW"
            ],
            [
            "4044738942786080",
            "3069348215",
            "哈哈哈哈哈哈",
            "219.236.29.48",
            null,
            1479824374,
            "2016-11-22 22:19:34",
            645,
            19,
            0,
            "http://weibo.com/3069348215/EiLRAbGMM"
            ],
            [
            "4044692737986098",
            "3069348215",
            "能提出来这个法案我也真是呵呵了//@小不二不二小：太反人类了 谁同意怼死谁 妈卖批的 http://t.cn/RfS9Miu",
            "1.202.40.234",
            null,
            1479813358,
            "2016-11-22 19:15:58",
            414,
            10,
            0,
            "http://weibo.com/3069348215/EiKF3xvy2"
            ],
            [
            "4044678401629948",
            "3069348215",
            "狮子为了维护形象，面子，心里再放不下也要假装无所谓。只是一到晚上啊，哎……距离狮子玻璃心还有三小时。[困]",
            "219.236.29.48",
            null,
            1479809940,
            "2016-11-22 18:19:00",
            97,
            3163,
            0,
            "http://weibo.com/3069348215/EiKhW6Q1u"
            ],
            [
            "4044632189179030",
            "3069348215",
            "天冷了，给你们做了个帽子，喜欢嘛……[拜拜]",
            "106.38.128.150",
            null,
            1479798922,
            "2016-11-22 15:15:22",
            157,
            1150,
            0,
            "http://weibo.com/3069348215/EiJ5oCvSS"
            ],
            [
            "4044583288166787",
            "3069348215",
            "水瓶，天蝎，处女，金牛的情感洁癖简直了，你对别人做过的再好再浪漫都别用我身上，我嫌弃。就这么说吧，你给我发过的表情包，在发给别人，那你以后就别给我发了。懂？[二哈]",
            "1.202.40.234",
            null,
            1479787263,
            "2016-11-22 12:01:03",
            9309,
            2,
            0,
            "http://weibo.com/3069348215/EiHOwygyn"
            ],
            [
            "4044543861430183",
            "3069348215",
            "没错 //@温柔是给中意人:我记得你 我好好活",
            "106.38.128.150",
            null,
            1479777863,
            "2016-11-22 09:24:23",
            533,
            14,
            0,
            "http://weibo.com/3069348215/EiGMW603t"
            ],
            [
            "4044409173265396",
            "3069348215",
            "忘不了的就记得 别逼着自己去忘了 毕竟记得也不代表什么 因为以后会更好的 不管是你还是生活 晚安",
            "219.236.29.48",
            null,
            1479745751,
            "2016-11-22 00:29:11",
            23,
            1,
            0,
            "http://weibo.com/3069348215/EiDhHdHtG"
            ],
            [
            "4044390571407173",
            "3069348215",
            "恭喜@Free-Vicky 获得【狮子座公仔】。微博官方唯一抽奖工具@微博抽奖平台 对本次抽奖进行监督，结果公正有效。公证链接：http://t.cn/RfaSI4a",
            "10.69.2.149",
            null,
            1479741316,
            "2016-11-21 23:15:16",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiCNH5U4l"
            ],
            [
            "4044382724503112",
            "3069348215",
            "[摊手] //@小野妹子学吐槽:[摊手]//@祖國的小還纸：谁能想到，这个16岁的花季少女，四年前仅仅12岁",
            "219.236.29.48",
            null,
            1479739445,
            "2016-11-21 22:44:05",
            181,
            0,
            0,
            "http://weibo.com/3069348215/EiCB2iTsQ"
            ],
            [
            "4044365335081450",
            "3069348215",
            "#你好明星# 本期嘉宾——范冰冰。对别人要求高对自己要求低的处女座究竟还有哪些“优点”，看看视频就知道！[二哈]（11月23日从转发里抽一名粉丝送@范冰冰 亲笔签名处女座搪胶公仔）http://t.cn/RfaA3or",
            "219.236.29.48",
            null,
            1479735299,
            "2016-11-21 21:34:59",
            873,
            0,
            0,
            "http://weibo.com/3069348215/EiC8ZljUS"
            ],
            [
            "4044328374593235",
            "3069348215",
            "[摊手][摊手] //@Yagom:如果你感受过我特别神经病的一面，那说明我还挺在意你[摊手]",
            "1.202.40.234",
            null,
            1479726487,
            "2016-11-21 19:08:07",
            1021,
            0,
            0,
            "http://weibo.com/3069348215/EiBbnjgUr"
            ],
            [
            "4044312503004391",
            "3069348215",
            "能把所有玩笑都当真话听。越小的事情越较真，有时候明明就没啥，但是能根据你这语气不对的一个字，给你想出来个连环故事。不过这些都是真喜欢你的表现。不然你没这待遇！没错，我说的就是TA们，一动真心就变得不像自己的……",
            "1.202.40.234",
            null,
            1479722703,
            "2016-11-21 18:05:03",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiALMcBzV"
            ],
            [
            "4044252029600847",
            "3069348215",
            "金牛——颜值高，会生活，有品位。带的出去见朋友，带的回来领上床。文能装逼武能逗逼完了还专一。👏",
            "1.202.40.234",
            null,
            1479708285,
            "2016-11-21 14:04:45",
            2,
            0,
            0,
            "http://weibo.com/3069348215/EizceEhCn"
            ],
            [
            "4044218462976568",
            "3069348215",
            "[失望]//@颜柔：挺心疼白羊的 活泼开朗是表面 很少有人发现背后的心酸都是自己一人扛 留给开心给大家[悲伤]",
            "1.202.40.234",
            null,
            1479700282,
            "2016-11-21 11:51:22",
            891,
            67,
            0,
            "http://weibo.com/3069348215/Eiyk6cula"
            ],
            [
            "4044069757837282",
            "3069348215",
            "晚安，巨蟹。[心]",
            "219.236.29.48",
            null,
            1479664828,
            "2016-11-21 02:00:28",
            0,
            0,
            0,
            "http://weibo.com/3069348215/EiusfwSPM"
            ],
            [
            "4044039944640692",
            "3069348215",
            "我的小鱼干呢？！？",
            "219.236.29.48",
            null,
            1479657720,
            "2016-11-21 00:02:00",
            0,
            39,
            0,
            "http://weibo.com/3069348215/EitGajtfS"
            ]
            ]
        function weiboOpinion(data){
            $('#word-3content').bootstrapTable('load', data);
            $('#word-3content').bootstrapTable({
                data:data,
                search: false,//是否搜索
                pagination: true,//是否分页
                pageSize: 5,//单页记录数
                // pageList: [15,20,25],//分页步进值
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
                            // row --- [
                            // "4046163315603407",
                            // "3069348215",
                            // "哈哈哈哈哈哈哈哈哈神经病//@HaoRabbit：射手就是莫名其妙就笑了起来的那种人[微笑]",    【内容】
                            // "219.236.29.48",  【发布IP】
                            // null,  【发布地址】
                            // 1480163971,
                            // "2016-11-26 20:39:31",  【时间】
                            // 0,   【转发数】
                            // 0,   【评论数】
                            // 0,   【点赞数】
                            // "http://weibo.com/3069348215/EjmUXnvHx"
                            // ],
                            var address = '未知';//发布地址
                            if(row[4] != null && row[4] != ''){
                                address = row[4];
                            }
                            return '<div class="center_rel">'+
                                        '<div>'+
                                            '<img src="/static/images/unknown.png" alt="" class="center_icon">'+
                                            '<a href="###" class="center_1" style="color:#ff9645;font-weight:700;">'+row[1]+'</a>'+
                                            '<span class="time" style="font-weight:900;color:#337ab7;font-weight:400;margin-left:10px;">'+
                                                '&nbsp;&nbsp;IP:'+row[3]+
                                                '&nbsp;&nbsp;地址:'+address+
                                            '</span>'+

                                            '<span style="margin-left:10px;">'+row[2]+'</span>'+
                                            '&nbsp;&nbsp;<a href="'+row[10]+'" target="_blank">原文</a>'+
                                        '</div>'+
                                        '<div class="clearfix" style="margin-top:8px;">'+
                                            '<span class="time pull-left" style="font-weight:900;color:#337ab7;font-weight:400;">'+
                                                '<i class="icon icon-time">&nbsp;'+row[6]+'</i>'+
                                            '</span>'+
                                            '<span class="pull-right"">'+
                                                '<span class="retweet_count">转发数('+row[7]+')</span>&nbsp;&nbsp;|&nbsp;&nbsp;'+
                                                '<span class="retweet_count">评论数('+row[8]+')</span>&nbsp;&nbsp;|&nbsp;&nbsp;'+
                                                '<span class="retweet_count">点赞数('+row[9]+')</span>'+
                                            '</span>'+
                                        '</div>'+
                                    '</div>';
                        }
                    },
                ],
            });
            $('#word-3content p.load').hide();
        }
        // weiboOpinion(demoData);
        // var now_weiboOpinion_url = '/topic_language_analyze/subopinion_all/?topic=pu-jin-hui-1491486370';//测试的
        var now_weiboOpinion_url = '/topic_language_analyze/subopinion_all/?topic='+en_name;
        public_ajax.call_request('get',now_weiboOpinion_url,now_weiboOpinion);
        var allweiboData;
        function now_weiboOpinion(data){
            if(data.length == 0){
                $('#word-3content p.load').text('暂无记录');
            }else {
                allweiboData = data;
                var str = '';
                for(var i=0;i<data.length;i++){
                    str += '<span class="opinionChild">'+data[i].keys+'</span>';
                }
                $('.opinion').empty().append(str);
                $('.opinion span').eq(0).addClass("active");

                // 显示第一个观点的微博
                var weiboData = data[0].weibos;
                $('#word-3content').bootstrapTable('load', weiboData);
                $('#word-3content').bootstrapTable({
                    data:weiboData,
                    search: false,//是否搜索
                    pagination: true,//是否分页
                    pageSize: 5,//单页记录数
                    // pageList: [15,20,25],//分页步进值
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
                                // [
                                //     "4045475264512032",
                                //     {
                                //         comment: 0,
                                //         uid: "1726613594",
                                //         text: "台媒：特朗普接受纽约时报专访 墙上现蒋介石照片-新闻频道-手机搜狐@手机QQ浏览器 http://t.cn/RfCKrmB",
                                //         retweeted: 0,
                                //         mid: "4045475264512032",
                                //         uname: "unknown",
                                //         timestamp: 1479999927,
                                //         photo_url: "unknown"
                                //     }
                                // ],
                                var imgsrc = '/static/images/unknown.png';//头像地址
                                if(row[1].photo_url != 'unknown' && row[1].photo_url != ''){
                                    imgsrc = row[1].photo_url;
                                }
                                var uname = '';
                                if(row[1].uname != '' && row[1].uname != 'unknown'){
                                    uname = row[1].uname;
                                }else {
                                    uname = '';
                                }
                                return '<div class="center_rel">'+
                                            '<div>'+
                                                '<img src="'+imgsrc+'" alt="" class="center_icon">'+
                                                '<a href="###" class="center_1" style="color:#ff9645;font-weight:700;">'+row[1].uid+'</a>'+
                                                '<a href="###" class="center_1" style="color:#337ab7;font-weight:700;margin-left:15px;">'+uname+'</a>'+
                                                '<span class="time" style="font-weight:900;color:#337ab7;font-weight:400;margin-left:10px;">'+
                                                    // '&nbsp;&nbsp;IP:'+row[3]+
                                                    // '&nbsp;&nbsp;地址:'+address+
                                                '</span>'+

                                                '<span style="margin-left:10px;">'+row[1].text+'</span>'+
                                                // '&nbsp;&nbsp;<a href="'+row[10]+'" target="_blank">原文</a>'+
                                            '</div>'+
                                            '<div class="clearfix" style="margin-top:8px;">'+
                                                '<span class="time pull-left" style="font-weight:900;color:#337ab7;font-weight:400;">'+
                                                    '<i class="icon icon-time">&nbsp;'+getLocalTime(row[1].timestamp)+'</i>'+
                                                '</span>'+
                                                '<span class="pull-right"">'+
                                                    '<span class="retweet_count">转发数('+row[1].retweeted+')</span>&nbsp;&nbsp;|&nbsp;&nbsp;'+
                                                    '<span class="retweet_count">评论数('+row[1].comment+')</span>'+
                                                    // '<span class="retweet_count">点赞数('+row[9]+')</span>'+
                                                '</span>'+
                                            '</div>'+
                                        '</div>';
                            }
                        },
                    ],
                });
                $('#word-3content p.load').hide();
            }

        }
        $('.opinion').on('click','span',function(){//给动态生成的元素绑定事件
            $(this).addClass('active').siblings('span').removeClass('active');
            $('#word-3content p.load').show();
            var index = $('.opinion span').index(this);

            tab_weiboOpinion(allweiboData[index].weibos)
        });
        function tab_weiboOpinion(data){
            $('#word-3content').bootstrapTable('load', data);
            $('#word-3content').bootstrapTable({
                data:data,
                search: false,//是否搜索
                pagination: true,//是否分页
                pageSize: 5,//单页记录数
                // pageList: [15,20,25],//分页步进值
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
                            // [
                            //     "4045475264512032",
                            //     {
                            //         comment: 0,
                            //         uid: "1726613594",
                            //         text: "台媒：特朗普接受纽约时报专访 墙上现蒋介石照片-新闻频道-手机搜狐@手机QQ浏览器 http://t.cn/RfCKrmB",
                            //         retweeted: 0,
                            //         mid: "4045475264512032",
                            //         uname: "unknown",
                            //         timestamp: 1479999927,
                            //         photo_url: "unknown"
                            //     }
                            // ],
                            var imgsrc = '/static/images/unknown.png';//头像地址
                            if(row[1].photo_url != 'unknown' && row[1].photo_url != ''){
                                imgsrc = row[1].photo_url;
                            }
                            var uname = '';
                            if(row[1].uname != '' && row[1].uname != 'unknown'){
                                uname = row[1].uname;
                            }else {
                                uname = '';
                            }
                            return '<div class="center_rel">'+
                                        '<div>'+
                                            '<img src="'+imgsrc+'" alt="" class="center_icon">'+
                                            '<a href="###" class="center_1" style="color:#ff9645;font-weight:700;">'+row[1].uid+'</a>'+
                                            '<a href="###" class="center_1" style="color:#337ab7;font-weight:700;margin-left:15px;">'+uname+'</a>'+
                                            '<span class="time" style="font-weight:900;color:#337ab7;font-weight:400;margin-left:10px;">'+
                                                // '&nbsp;&nbsp;IP:'+row[3]+
                                                // '&nbsp;&nbsp;地址:'+address+
                                            '</span>'+

                                            '<span style="margin-left:10px;">'+row[1].text+'</span>'+
                                            // '&nbsp;&nbsp;<a href="'+row[10]+'" target="_blank">原文</a>'+
                                        '</div>'+
                                        '<div class="clearfix" style="margin-top:8px;">'+
                                            '<span class="time pull-left" style="font-weight:900;color:#337ab7;font-weight:400;">'+
                                                '<i class="icon icon-time">&nbsp;'+getLocalTime(row[1].timestamp)+'</i>'+
                                            '</span>'+
                                            '<span class="pull-right"">'+
                                                '<span class="retweet_count">转发数('+row[1].retweeted+')</span>&nbsp;&nbsp;|&nbsp;&nbsp;'+
                                                '<span class="retweet_count">评论数('+row[1].comment+')</span>'+
                                                // '<span class="retweet_count">点赞数('+row[9]+')</span>'+
                                            '</span>'+
                                        '</div>'+
                                    '</div>';
                        }
                    },
                ],
            });
            $('#word-3content p.load').hide();
        }

// 演化分析 ====
    // 假数据
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
            day30Data2.push(Math.round(Math.random()*(20-3)));
        }
    var option,tit;
    // function _option(ytit,dd, dateData) {
    function _option(tit, ytit, dd_1, dd_2, dd_3, dateData) {
        option = {
            backgroundColor:'transparent',
            title: {
                text: tit,
                x:'center',
                textStyle:{
                    // color:'#fff'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        // color: '#30c7ff'
                    }
                }
            },
            legend:{
                data:['原创','转发','评论'],
                y:30
            },
            grid: {
                left: '3%',
                right: '3%',
                bottom: '0%',
                top:'20%',
                // width:'80%',
                containLabel: true
            },
            xAxis: [{
                name:'时间',
                type: 'category',
                boundaryGap: false,
                axisLine: {
                    lineStyle: {
                        // color: '#fff'
                    }
                },
                axisLabel: {
                    textStyle: {
                        // color: '#fff',
                    }
                },
                // data: day30.reverse(),
                data: dateData
            }],
            yAxis: {
                name:ytit,
                type: 'value',
                axisLine: {
                    lineStyle: {
                        // color: '#fff'
                    }
                },
                nameTextStyle:{
                    // color:'#fff'
                },
                splitLine:{
                    show:false
                }
            },
            dataZoom: [
                {
                    type: 'slider',
                    show: false,
                    xAxisIndex: [0],
                    start: 1,
                    end: 100
                },
                // {
                //     type: 'slider',
                //     show: true,
                //     yAxisIndex: [0],
                //     left: '93%',
                //     start: 29,
                //     end: 36
                // },
                {
                    type: 'inside',
                    show: false,
                    xAxisIndex: [0],
                    start: 1,
                    end: 35
                },
                // {
                //     type: 'inside',
                //     yAxisIndex: [0],
                //     start: 29,
                //     end: 36
                // }
            ],
            series: [
                {
                    name: '原创',
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
                    // areaStyle: {
                    //     normal: {
                    //         // color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    //         //     offset: 0,
                    //         //     color: 'rgba(137, 189, 27, 0.8)'
                    //         // }, {
                    //         //     offset: 1,
                    //         //     color: 'rgba(137, 189, 27, 0.2)'
                    //         // }], false),
                    //         // shadowColor: 'rgba(0, 0, 0, 0.1)',
                    //         // shadowBlur: 10
                    //     }
                    // },
                    // itemStyle: {
                    //     normal: {
                    //         color: 'rgb(137,189,27)',
                    //         borderColor: 'rgba(137,189,2,0.27)',
                    //         borderWidth: 12
                    //     }
                    // },
                    data: dd_1,
                    // data: [9, 13, 5, 17, 13, 23, 14, 8, 18, 19, 19, 16, 18, 16, 14, 47, 19, 20, 13, 7, 18, 15, 7, 15, 12, 14, 20, 15, 13, 8],
                },
                {
                    name: '转发',
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
                    data:dd_2
                    // data: [9, 13, 5, 17, 13, 13, 14, 8, 18, 9, 19, 16, 8, 16, 14, 17, 19, 10, 13, 7, 18, 15, 7, 15, 12, 14, 20, 15, 13, 8],
                },
                {
                    name: '评论',
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
                    data:dd_3
                    // data: [14, 14, 8, 14, 18, 8, 12, 8, 18, 15, 9, 12, 8, 13, 12, 8, 13, 14, 5, 12, 7, 5, 11, 17, 7, 5, 10, 12, 5, 19],
                },
            ]
        };
    };

    function line_1() {
        var tit='热度演化曲线图';
        var myChart = echarts.init(document.getElementById('evolution-chat-1'));
        myChart.showLoading();

        // var line_1_url = '/topic_time_analyze/mtype_count/?topic=te-lang-pu-ji-xin-ge-1492166854&start_ts=1478736000&end_ts=1480176000&pointInterval=3600';//测试的
        var line_1_url = '/topic_time_analyze/mtype_count/?topic='+en_name+'&start_ts=1478736000&end_ts=1480176000&pointInterval=3600';
        public_ajax.call_request('get',line_1_url,line_1success);
        function line_1success(data){
            var dateData = [];
            var seriesData_1 = [];
            var seriesData_2 = [];
            var seriesData_3 = [];

            for(var key in data){
                dateData.push(getLocalTime(key));
                if(data[key][1] == undefined){
                    seriesData_1.push(0);
                }else {
                    seriesData_1.push(data[key][1]);
                }
                if(data[key][2] == undefined){
                    seriesData_2.push(0);
                }else {
                    seriesData_2.push(data[key][2]);
                }
                if(data[key][3] == undefined){
                    seriesData_3.push(0);
                }else {
                    seriesData_3.push(data[key][3]);
                }
            }
            // console.log(seriesData_1);
            // console.log(seriesData_2);
            // console.log(seriesData_3);

            // _option('热度',day30Data1, dateData);
            _option(tit, '热度',seriesData_1, seriesData_2, seriesData_3, dateData);
            // console.log(day30Data1);
            // console.log(day30Data1.reverse());

            myChart.hideLoading();
            myChart.setOption(option);
        }

    }
    line_1();

    // 情绪====
    // function _option2(tit, ytit,dd_0, dd_1, dd_2, dd_3, dd_4, dd_5, dd_6, dateData) {
    function _option2(tit, ytit,dd_0, dd_1, dd_2, dateData) {
        option = {
            backgroundColor:'transparent',
            title: {
                text: tit,
                x:'center',
                textStyle:{
                    // color:'#fff'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        // color: '#30c7ff'
                    }
                }
            },
            legend:{
                // data:['中立情绪','积极情绪','生气情绪','焦虑情绪','悲伤情绪','厌恶情绪','消极其他'],
                data:['中立情绪','积极情绪','消极情绪'],
                y:30
            },
            grid: {
                left: '3%',
                right: '3%',
                bottom: '0%',
                top:'20%',
                // width:'80%',
                containLabel: true
            },
            xAxis: [{
                name:'时间',
                type: 'category',
                boundaryGap: false,
                axisLine: {
                    lineStyle: {
                        // color: '#fff'
                    }
                },
                axisLabel: {
                    textStyle: {
                        // color: '#fff',
                    }
                },
                data: dateData
            }],
            yAxis: {
                name:ytit,
                type: 'value',
                axisLine: {
                    lineStyle: {
                        // color: '#fff'
                    }
                },
                nameTextStyle:{
                    // color:'#fff'
                },
                splitLine:{
                    show:false
                }
            },
            dataZoom: [
                {
                    type: 'slider',
                    show: false,
                    xAxisIndex: [0],
                    start: 1,
                    end: 100
                },
                // {
                //     type: 'slider',
                //     show: true,
                //     yAxisIndex: [0],
                //     left: '93%',
                //     start: 29,
                //     end: 36
                // },
                {
                    type: 'inside',
                    show: false,
                    xAxisIndex: [0],
                    start: 1,
                    end: 35
                },
                // {
                //     type: 'inside',
                //     yAxisIndex: [0],
                //     start: 29,
                //     end: 36
                // }
            ],
            series: [
                {
                    name: '中立情绪',
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
                    data:dd_0
                },
                {
                    name: '积极情绪',
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
                    data: dd_1,
                },
                {
                    name: '消极情绪',
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
                    data: dd_2,
                },
                // {
                //     name: '生气情绪',
                //     type: 'line',
                //     smooth: true,
                //     symbol: 'circle',
                //     symbolSize: 5,
                //     showSymbol: false,
                //     lineStyle: {
                //         normal: {
                //             width: 1,
                //         }
                //     },
                //     data:dd_2
                // },
                // {
                //     name: '焦虑情绪',
                //     type: 'line',
                //     smooth: true,
                //     symbol: 'circle',
                //     symbolSize: 5,
                //     showSymbol: false,
                //     lineStyle: {
                //         normal: {
                //             width: 1,
                //         }
                //     },
                //     data:dd_3
                // },
                // {
                //     name: '悲伤情绪',
                //     type: 'line',
                //     smooth: true,
                //     symbol: 'circle',
                //     symbolSize: 5,
                //     showSymbol: false,
                //     lineStyle: {
                //         normal: {
                //             width: 1,
                //         }
                //     },
                //     data:dd_4
                // },
                // {
                //     name: '厌恶情绪',
                //     type: 'line',
                //     smooth: true,
                //     symbol: 'circle',
                //     symbolSize: 5,
                //     showSymbol: false,
                //     lineStyle: {
                //         normal: {
                //             width: 1,
                //         }
                //     },
                //     data:dd_5
                // },
                // {
                //     name: '消极其他',
                //     type: 'line',
                //     smooth: true,
                //     symbol: 'circle',
                //     symbolSize: 5,
                //     showSymbol: false,
                //     lineStyle: {
                //         normal: {
                //             width: 1,
                //         }
                //     },
                //     data:dd_6
                // },
            ]
        };
    };
    function line_2() {
        var tit='情绪演化曲线图';
        var myChart = echarts.init(document.getElementById('evolution-chat-2'));
        myChart.showLoading();

        // var line_2_url = '/topic_sen_analyze/sen_time_count/?topic=te-lang-pu-ji-xin-ge-1492166854&start_ts=1478736000&end_ts=1480176000&pointInterval=3600';//测试的
        var line_2_url = '/topic_sen_analyze/sen_time_count/?topic='+en_name+'&start_ts=1478736000&end_ts=1480176000&pointInterval=3600';
        public_ajax.call_request('get',line_2_url,line_2success);
        function line_2success(data){

            var dateData = [];
            var seriesData_0 = [];//中立情绪
            var seriesData_1 = [];//积极情绪

            // var seriesData_2 = [];//消极情绪
            var seriesData_2 = [];//生气情绪
            var seriesData_3 = [];//焦虑情绪
            var seriesData_4 = [];//悲伤情绪
            var seriesData_5 = [];//厌恶情绪
            var seriesData_6 = [];//消极其他

            var negative_data = [];//消极情绪
            if(JSON.stringify(data) == "{}"){
                // console.log("空对象");
                dateData = [
                    '2016/11/16', '2016/11/17', '2016/11/18', '2016/11/19', '2016/11/20', '2016/11/21', '2016/11/22', '2016/11/23', '2016/11/24', '2016/11/25', '2016/11/26',
                ];
                seriesData_0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                seriesData_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                negative_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }else {
                for(var key in data){
                    dateData.push(getLocalTime(key));
                    if(data[key][0] == undefined){
                        seriesData_0.push(0);
                    }else {
                        seriesData_0.push(data[key][0]);
                    }
                    if(data[key][1] == undefined){
                        seriesData_1.push(0);
                    }else {
                        seriesData_1.push(data[key][1]);
                    }


                    if(data[key][2] == undefined){
                        seriesData_2.push(0);
                    }else {
                        seriesData_2.push(data[key][2]);
                    }
                    if(data[key][3] == undefined){
                        seriesData_3.push(0);
                        // seriesData_2.push(0);
                    }else {
                        seriesData_3.push(data[key][3]);
                        // seriesData_2.push(data[key][3]);
                    }
                    if(data[key][4] == undefined){
                        seriesData_4.push(0);
                        // seriesData_2.push(0);
                    }else {
                        seriesData_4.push(data[key][4]);
                        // seriesData_2.push(data[key][4]);
                    }
                    if(data[key][5] == undefined){
                        seriesData_5.push(0);
                        // seriesData_2.push(0);
                    }else {
                        seriesData_5.push(data[key][5]);
                        // seriesData_2.push(data[key][5]);
                    }
                    if(data[key][6] == undefined){
                        seriesData_6.push(0);
                        // seriesData_2.push(0);
                    }else {
                        seriesData_6.push(data[key][6]);
                        // seriesData_2.push(data[key][6]);
                    }
                }
                // console.log(seriesData_0);
                // console.log(seriesData_1);
                // console.log(seriesData_2);
                // console.log(seriesData_3);
                // console.log(seriesData_4);
                // console.log(seriesData_5);
                // console.log(seriesData_6);

                negative_data = [];//消极情绪
                for(var i=0;i<seriesData_2.length;i++){
                    negative_data.push(parseInt(seriesData_2[i]) + parseInt(seriesData_3[i]) + parseInt(seriesData_4[i]) + parseInt(seriesData_5[i]) + parseInt(seriesData_6[i]))
                }
                // console.log(negative_data);
            }



            // _option2(tit, '情绪',seriesData_0, seriesData_1, seriesData_2, seriesData_3, seriesData_4, seriesData_5, seriesData_6, dateData);
            _option2(tit, '情绪',seriesData_0, seriesData_1, negative_data, dateData);

            myChart.hideLoading();
            myChart.setOption(option);
        }
    }
    line_2();
    // $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    //     // 获取已激活的标签页的名称
    //     var activeTab = $(e.target).text();
    //     // 获取前一个激活的标签页的名称
    //     var previousTab = $(e.relatedTarget).text();
    //     // $(".active-tab span").html(activeTab);
    //     // $(".previous-tab span").html(previousTab);
    //     console.log(activeTab);
    //     if(activeTab){
    //         console.log(activeTab);
    //     }
    //     console.log(activeTab);
    // });

// 传播分析 ====
    // 饼图 (暂弃用)
        function spread_pie_1(){
            var myChart = echarts.init(document.getElementById('spread-pie-1'));
            var option = {
                title : {
                    text: '参与传播的媒体粉丝数分布',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    left: 'right',
                    data: ['5万以下','5万-10万','10万-20万','20万-50万','50万-100万','100万以上']
                },
                series : [
                    {
                        name: '媒体粉丝数分布',
                        type: 'pie',
                        radius : '55%',
                        center: ['50%', '50%'],
                        data:[
                            {value:335, name:'5万以下'},
                            {value:310, name:'5万-10万'},
                            {value:234, name:'10万-20万'},
                            {value:135, name:'20万-50万'},
                            {value:1350, name:'50万-100万'},
                            {value:1548, name:'100万以上'},
                        ],
                        label: {
                            normal:{
                                show: true,
                                // position:'inner',
                                formatter: "{d}%",
                                textStyle: {
                                    fontWeight:'bolder',
                                    // fontSize : '12',
                                    // color:'#fff'
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
            myChart.setOption(option)
        }
        // spread_pie_1();
        function spread_pie_2(){
            var myChart = echarts.init(document.getElementById('spread-pie-2'));
            var option = {
                title : {
                    text: '参与传播的个人粉丝数分布',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    left: 'right',
                    data: ['5万以下','5万-10万','10万-20万','20万-50万','50万-100万','100万以上']
                },
                series : [
                    {
                        name: '个人粉丝数分布',
                        type: 'pie',
                        radius : '55%',
                        center: ['50%', '50%'],
                        data:[
                            {value:335, name:'5万以下'},
                            {value:310, name:'5万-10万'},
                            {value:234, name:'10万-20万'},
                            {value:135, name:'20万-50万'},
                            {value:1350, name:'50万-100万'},
                            {value:1548, name:'100万以上'}
                        ],
                        label: {
                            normal:{
                                show: true,
                                // position:'inner',
                                formatter: "{d}%",
                                textStyle: {
                                    fontWeight:'bolder',
                                    // fontSize : '12',
                                    // color:'#fff'
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
            myChart.setOption(option)
        }
        // spread_pie_2();

    /*
        @function     JsonSort ==== 对json排序 ====
        @param        json     用来排序的json
        @param        key      排序的键值
    */
    function JsonSort(json,key){
        //console.log(json);
        for(var j=1,jl=json.length;j < jl;j++){
            var temp = json[j],
                val  = temp[key],
                i    = j-1;
            while(i >=0 && json[i][key]>val){
                json[i+1] = json[i];
                i = i-1;
            }
            json[i+1] = temp;

        }
        //console.log(json);
        return json;

    }
    // var json = JsonSort(willSort,'age');
    // console.log(json);
    // 十大造谣者 传谣者

        // var spread_1_url = '/topic_network_analyze/get_trend_maker/?topic=te-lang-pu-ji-xin-ge-1492166854';//测试的
        // var spread_1_url = '/topic_network_analyze/get_trend_maker/?topic='+en_name;
        // public_ajax.call_request('get',spread_1_url,spread_1);
        function spread_1(data){
            // [
            //     {
            //         uid: 3176105483, --- ID
            //         timestamp: 1479087720,
            //         mid: "4041649191833379",
            //         rank: 1,  --- 排名
            //         fans: 50863,--- 粉丝数
            //         photo: "no",
            //         name: "未知"
            //     },
            // ]
            var data = JsonSort(data,'rank');//按排名 排序
            var str = '';
            // for(var i=0;i<10;i++){
            if(data.length > 10){
                for(var i=0;i<10;i++){
                    str += '<tr><td>'+data[i].rank+'</td>';
                    str += '<td>'+data[i].uid+'</td>';
                    str += '<td>'+data[i].fans+'</td></tr>';
                }
            }else if(data.length == 0){
                str += '<tr><td>暂无记录</td></tr>';
            }else {
                for(var i=0;i<data.length;i++){
                    str += '<tr><td>'+data[i].rank+'</td>';
                    str += '<td>'+data[i].uid+'</td>';
                    str += '<td>'+data[i].fans+'</td></tr>';
                }
            }
            $('#spread-1 table tbody').empty().append(str);
        }
        // 传谣者
        // var spread_2_url = '/topic_network_analyze/get_trend_pusher/?topic=te-lang-pu-ji-xin-ge-1492166854';//测试的
        // var spread_2_url = '/topic_network_analyze/get_trend_pusher/?topic='+en_name;
        // public_ajax.call_request('get',spread_2_url,spread_2);
        function spread_2(data){
            var data = JsonSort(data,'rank');//按排名 排序
            var str = '';
            // for(var i=0;i<10;i++){
            if(data.length > 10){
                for(var i=0;i<10;i++){
                    str += '<tr><td>'+data[i].rank+'</td>';
                    str += '<td>'+data[i].uid+'</td>';
                    str += '<td>'+data[i].fans+'</td></tr>';
                }
            }else if(data.length == 0){
                str += '<tr><td>暂无记录</td></tr>';
            }else {
                for(var i=0;i<data.length;i++){
                    str += '<tr><td>'+data[i].rank+'</td>';
                    str += '<td>'+data[i].uid+'</td>';
                    str += '<td>'+data[i].fans+'</td></tr>';
                }
            }
            $('#spread-2 table tbody').empty().append(str);
        }

        // 改为一个接口
            // var spread_url = '/rumor/get_trend/?en_name=le-shi-shou-kuan-4045705104264682';//测试的
            var spread_url = '/rumor/get_trend/?en_name='+en_name;
            public_ajax.call_request('get',spread_url,spreadNewurl);
            function spreadNewurl(data){
                var makerData = data.maker;
                makerData = JsonSort(makerData,'rank');//按排名 排序
                var makerStr = '';
                // for(var i=0;i<10;i++){
                if(makerData.length > 10){
                    for(var i=0;i<10;i++){
                        makerStr += '<tr><td>'+makerData[i][1]+'</td>';
                        makerStr += '<td>'+makerData[i][0]+'</td>';
                        makerStr += '<td>'+makerData[i][2]+'</td></tr>';
                    }
                }else if(makerData.length == 0){
                    makerStr += '<tr><td>暂无记录</td></tr>';
                }else {
                    for(var i=0;i<makerData.length;i++){
                        makerStr += '<tr><td>'+makerData[i][1]+'</td>';
                        makerStr += '<td>'+makerData[i][0]+'</td>';
                        makerStr += '<td>'+makerData[i][2]+'</td></tr>';
                    }
                }
                $('#spread-1 table tbody').empty().append(makerStr);

                // 传播者
                var pusherData = data.pusher;
                pusherData = JsonSort(pusherData,'rank');//按排名 排序
                var pusherStr = '';
                // for(var i=0;i<10;i++){
                if(pusherData.length > 10){
                    for(var i=0;i<10;i++){
                        pusherStr += '<tr><td>'+pusherData[i][1]+'</td>';
                        pusherStr += '<td>'+pusherData[i][0]+'</td>';
                        pusherStr += '<td>'+pusherData[i][2]+'</td></tr>';
                    }
                }else if(pusherData.length == 0){
                    pusherStr += '<tr><td>暂无记录</td></tr>';
                }else {
                    for(var i=0;i<pusherData.length;i++){
                        pusherStr += '<tr><td>'+pusherData[i][1]+'</td>';
                        pusherStr += '<td>'+pusherData[i][0]+'</td>';
                        pusherStr += '<td>'+pusherData[i][2]+'</td></tr>';
                    }
                }
                $('#spread-2 table tbody').empty().append(pusherStr);
            }

    // 鱼骨图
        // 旧版
        /*


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
                // $('#container .fishBone .fish_box').width(fish_length*180);
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
         */

        var propagate_url = '/rumor/get_source/?en_name='+en_name;
        // var propagate_url = '/rumor/rumorPropagate?en_name=te-lang-pu-ji-xin-ge-1492166854';//测试的 【只有 它 有数据】
        public_ajax.call_request('get',propagate_url,propagate);
        function propagate(data){
            $(".fishBone").empty().append('<center>加载中...</center>');
            if(data.length == 0){
                $(".fishBone").empty().append('<center>暂无记录</center>');
            }else {
                var fishdata = [];
                for(var i=0;i<data.length;i++){
                    // if(data[i].title.length>14){
                    //     data[i].title = data[i].title.substr(0,14)+'...'
                    // }

                    // 修改插件文件 fishBone.js  有 LL 标识

                    // fishdata.push({'发布时间':data[i].publish_time,'标题':data[i].title,'承办法官':'吕磊','承办法院':'吕磊','案件状态':'吕磊','承办庭室':'吕磊'});//多个li时 可以把fishBone.js中 改回来
                    fishdata.push({'发布时间':getLocalTime(data[i].publish_time),'标题':data[i].text,'关键词':data[i].keyword,'发布者ID':data[i].uid,'粉丝数':data[i].user_fansnum,'地点':data[i].geo});//多个li时 可以把fishBone.js中 改回来
                    // fishdata.push({'发布时间':data[i].publish_time,'标题 ':data[i].title});
                    // fishdata.push({'发布时间':data[i].publish_time,'标题':data[i].title,}); // fishBone.js中 ==标题 时是特殊样式
                }
                fishdata.push({'发布时间':' ','标题':' ','关键词':' ','发布者ID':' ','粉丝数':' ','地点':' '});
                // 标题即为内容标题 有特殊样式  详见fishBone.js
                // console.log(fishdata);
                $(".fishBone").empty();
                $(".fishBone").fishBone(fishdata);

                $('.fishBone li.item:last').hide();
            }

            $('#spread-pie-3 center.loading').hide();
        }

// 影响分析 （暂弃用）
    // 波及人数
    function influncePerson(){
        var myChart = echarts.init(document.getElementById('influnce_person'));
        var option = {
            title: {
                text:'',
                left:'center'
            },
            tooltip: {
                trigger: 'axis',
                // formatter: "Temperature : <br/>{b}km : {c}°C"
                formatter: "疑似谣言波及人数 : <br/>{c}"
            },
            grid: {
                top: '8%',
                left: '0%',
                right: '8%',
                bottom: '0%',
                containLabel: true
            },
            xAxis: {
                name:'传播时间',
                type: 'category',
                axisLabel:{
                    interval:0,
                    rotate:90,//倾斜度 -90 至 90 默认为0
                    margin:2,
                    textStyle:{
                        fontSize:8
                    }
                },
                data: ['0.00', '1.00', '2.00', '3.00', '4.00', '5.00', '6.00', '7.00', '8.00','9.00', '10.00','11.00' ,'12.00', '13.00', '14.00', '15.00', '16.00', '17.00', '18.00','19.00','20.00','21.00', '22.00', '23.00', '24.00','0.00']
            },
            yAxis: {
                name:'波及人数',
                type: 'value',
                // axisLine: {onZero: false},
                axisLabel: {
                    // formatter: '{value} km'
                },
                boundaryGap: false,
                // data: ['0', '10', '20', '30', '40', '50', '60', '70', '80']
            },
            series: [
                {
                    name: '疑似谣言波及人数',
                    type: 'line',
                    smooth: true,
                    lineStyle: {
                        normal: {
                            width: 3,
                            shadowColor: 'rgba(0,0,0,0.4)',
                            shadowBlur: 10,
                            shadowOffsetY: 10
                        }
                    },
                    data:[100,200,400,444,555,666,777,888,999,1000,1230,1500,1622,1674,1689,1755,1800,1900,2007,2500,2600,3000,3100,3232,]
                }
            ]
        };
        myChart.setOption(option)
    }
    // influncePerson();
    // 市场关联
    function influnceMarket(){
        var myChart = echarts.init(document.getElementById('influnce_market'));
        var upColor = '#ec0000';
        var upBorderColor = '#8A0000';
        var downColor = '#00da3c';
        var downBorderColor = '#008F28';

        // 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
        var data0 = splitData([
            ['2013/1/24', 2320.26,2320.26,2287.3,2362.94],
            ['2013/1/25', 2300,2291.3,2288.26,2308.38],
            ['2013/1/28', 2295.35,2346.5,2295.35,2346.92],
            ['2013/1/29', 2347.22,2358.98,2337.35,2363.8],
            ['2013/1/30', 2360.75,2382.48,2347.89,2383.76],
            ['2013/1/31', 2383.43,2385.42,2371.23,2391.82],
            ['2013/2/1', 2377.41,2419.02,2369.57,2421.15],
            ['2013/2/4', 2425.92,2428.15,2417.58,2440.38],
            ['2013/2/5', 2411,2433.13,2403.3,2437.42],
            ['2013/2/6', 2432.68,2434.48,2427.7,2441.73],
            ['2013/2/7', 2430.69,2418.53,2394.22,2433.89],
            ['2013/2/8', 2416.62,2432.4,2414.4,2443.03],
            ['2013/2/18', 2441.91,2421.56,2415.43,2444.8],
            ['2013/2/19', 2420.26,2382.91,2373.53,2427.07],
            ['2013/2/20', 2383.49,2397.18,2370.61,2397.94],
            ['2013/2/21', 2378.82,2325.95,2309.17,2378.82],
            ['2013/2/22', 2322.94,2314.16,2308.76,2330.88],
            ['2013/2/25', 2320.62,2325.82,2315.01,2338.78],
            ['2013/2/26', 2313.74,2293.34,2289.89,2340.71],
            ['2013/2/27', 2297.77,2313.22,2292.03,2324.63],
            ['2013/2/28', 2322.32,2365.59,2308.92,2366.16],
            ['2013/3/1', 2364.54,2359.51,2330.86,2369.65],
            ['2013/3/4', 2332.08,2273.4,2259.25,2333.54],
            ['2013/3/5', 2274.81,2326.31,2270.1,2328.14],
            ['2013/3/6', 2333.61,2347.18,2321.6,2351.44],
            ['2013/3/7', 2340.44,2324.29,2304.27,2352.02],
            ['2013/3/8', 2326.42,2318.61,2314.59,2333.67],
            ['2013/3/11', 2314.68,2310.59,2296.58,2320.96],
            ['2013/3/12', 2309.16,2286.6,2264.83,2333.29],
            ['2013/3/13', 2282.17,2263.97,2253.25,2286.33],
            ['2013/3/14', 2255.77,2270.28,2253.31,2276.22],
            ['2013/3/15', 2269.31,2278.4,2250,2312.08],
            ['2013/3/18', 2267.29,2240.02,2239.21,2276.05],
            ['2013/3/19', 2244.26,2257.43,2232.02,2261.31],
            ['2013/3/20', 2257.74,2317.37,2257.42,2317.86],
            ['2013/3/21', 2318.21,2324.24,2311.6,2330.81],
            ['2013/3/22', 2321.4,2328.28,2314.97,2332],
            ['2013/3/25', 2334.74,2326.72,2319.91,2344.89],
            ['2013/3/26', 2318.58,2297.67,2281.12,2319.99],
            ['2013/3/27', 2299.38,2301.26,2289,2323.48],
            ['2013/3/28', 2273.55,2236.3,2232.91,2273.55],
            ['2013/3/29', 2238.49,2236.62,2228.81,2246.87],
            ['2013/4/1', 2229.46,2234.4,2227.31,2243.95],
            ['2013/4/2', 2234.9,2227.74,2220.44,2253.42],
            ['2013/4/3', 2232.69,2225.29,2217.25,2241.34],
            ['2013/4/8', 2196.24,2211.59,2180.67,2212.59],
            ['2013/4/9', 2215.47,2225.77,2215.47,2234.73],
            ['2013/4/10', 2224.93,2226.13,2212.56,2233.04],
            ['2013/4/11', 2236.98,2219.55,2217.26,2242.48],
            ['2013/4/12', 2218.09,2206.78,2204.44,2226.26],
            ['2013/4/15', 2199.91,2181.94,2177.39,2204.99],
            ['2013/4/16', 2169.63,2194.85,2165.78,2196.43],
            ['2013/4/17', 2195.03,2193.8,2178.47,2197.51],
            ['2013/4/18', 2181.82,2197.6,2175.44,2206.03],
            ['2013/4/19', 2201.12,2244.64,2200.58,2250.11],
            ['2013/4/22', 2236.4,2242.17,2232.26,2245.12],
            ['2013/4/23', 2242.62,2184.54,2182.81,2242.62],
            ['2013/4/24', 2187.35,2218.32,2184.11,2226.12],
            ['2013/4/25', 2213.19,2199.31,2191.85,2224.63],
            ['2013/4/26', 2203.89,2177.91,2173.86,2210.58],
            ['2013/5/2', 2170.78,2174.12,2161.14,2179.65],
            ['2013/5/3', 2179.05,2205.5,2179.05,2222.81],
            ['2013/5/6', 2212.5,2231.17,2212.5,2236.07],
            ['2013/5/7', 2227.86,2235.57,2219.44,2240.26],
            ['2013/5/8', 2242.39,2246.3,2235.42,2255.21],
            ['2013/5/9', 2246.96,2232.97,2221.38,2247.86],
            ['2013/5/10', 2228.82,2246.83,2225.81,2247.67],
            ['2013/5/13', 2247.68,2241.92,2231.36,2250.85],
            ['2013/5/14', 2238.9,2217.01,2205.87,2239.93],
            ['2013/5/15', 2217.09,2224.8,2213.58,2225.19],
            ['2013/5/16', 2221.34,2251.81,2210.77,2252.87],
            ['2013/5/17', 2249.81,2282.87,2248.41,2288.09],
            ['2013/5/20', 2286.33,2299.99,2281.9,2309.39],
            ['2013/5/21', 2297.11,2305.11,2290.12,2305.3],
            ['2013/5/22', 2303.75,2302.4,2292.43,2314.18],
            ['2013/5/23', 2293.81,2275.67,2274.1,2304.95],
            ['2013/5/24', 2281.45,2288.53,2270.25,2292.59],
            ['2013/5/27', 2286.66,2293.08,2283.94,2301.7],
            ['2013/5/28', 2293.4,2321.32,2281.47,2322.1],
            ['2013/5/29', 2323.54,2324.02,2321.17,2334.33],
            ['2013/5/30', 2316.25,2317.75,2310.49,2325.72],
            ['2013/5/31', 2320.74,2300.59,2299.37,2325.53],
            ['2013/6/3', 2300.21,2299.25,2294.11,2313.43],
            ['2013/6/4', 2297.1,2272.42,2264.76,2297.1],
            ['2013/6/5', 2270.71,2270.93,2260.87,2276.86],
            ['2013/6/6', 2264.43,2242.11,2240.07,2266.69],
            ['2013/6/7', 2242.26,2210.9,2205.07,2250.63],
            ['2013/6/13', 2190.1,2148.35,2126.22,2190.1]
        ]);

        function splitData(rawData) {
            var categoryData = [];
            var values = []
            for (var i = 0; i < rawData.length; i++) {
                categoryData.push(rawData[i].splice(0, 1)[0]);
                values.push(rawData[i])
            }
            return {
                categoryData: categoryData,
                values: values
            };
        }

        function calculateMA(dayCount) {
            var result = [];
            for (var i = 0, len = data0.values.length; i < len; i++) {
                if (i < dayCount) {
                    result.push('-');
                    continue;
                }
                var sum = 0;
                for (var j = 0; j < dayCount; j++) {
                    sum += data0.values[i - j][1];
                }
                result.push(sum / dayCount);
            }
            return result;
        }

        option = {
            title: {
                text: '',
                left: 0
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            legend: {
                data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
            },
            grid: {
                top: '8%',
                left: '0%',
                right: '8%',
                bottom: '0%',
                containLabel: true
            },
            xAxis: {
                name:'时间',
                type: 'category',
                data: data0.categoryData,
                scale: true,
                boundaryGap : false,
                axisLine: {onZero: false,},
                splitLine: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax',
                axisLabel:{
                    interval:0,
                    rotate:90,//倾斜度 -90 至 90 默认为0
                    margin:2,
                    textStyle:{
                        fontSize:8
                    }
                },
            },
            yAxis: {
                name:'数值',
                scale: true,
                splitArea: {
                    show: true
                }
            },
            dataZoom: [
                {
                    type: 'inside',
                    start: 50,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    y: '90%',
                    start: 50,
                    end: 100
                }
            ],
            series: [
                {
                    name: '日K',
                    type: 'candlestick',
                    data: data0.values,
                    itemStyle: {
                        normal: {
                            color: upColor,
                            color0: downColor,
                            borderColor: upBorderColor,
                            borderColor0: downBorderColor
                        }
                    },
                    markPoint: {
                        label: {
                            normal: {
                                formatter: function (param) {
                                    return param != null ? Math.round(param.value) : '';
                                }
                            }
                        },
                        data: [
                            {
                                name: 'XX标点',
                                coord: ['2013/5/31', 2300],
                                value: 2300,
                                itemStyle: {
                                    normal: {color: 'rgb(41,60,85)'}
                                }
                            },
                            {
                                name: 'highest value',
                                type: 'max',
                                valueDim: 'highest'
                            },
                            {
                                name: 'lowest value',
                                type: 'min',
                                valueDim: 'lowest'
                            },
                            {
                                name: 'average value on close',
                                type: 'average',
                                valueDim: 'close'
                            }
                        ],
                        tooltip: {
                            formatter: function (param) {
                                return param.name + '<br>' + (param.data.coord || '');
                            }
                        }
                    },
                    markLine: {
                        symbol: ['none', 'none'],
                        data: [
                            [
                                {
                                    name: 'from lowest to highest',
                                    type: 'min',
                                    valueDim: 'lowest',
                                    symbol: 'circle',
                                    symbolSize: 10,
                                    label: {
                                        normal: {show: false},
                                        emphasis: {show: false}
                                    }
                                },
                                {
                                    type: 'max',
                                    valueDim: 'highest',
                                    symbol: 'circle',
                                    symbolSize: 10,
                                    label: {
                                        normal: {show: false},
                                        emphasis: {show: false}
                                    }
                                }
                            ],
                            {
                                name: 'min line on close',
                                type: 'min',
                                valueDim: 'close'
                            },
                            {
                                name: 'max line on close',
                                type: 'max',
                                valueDim: 'close'
                            }
                        ]
                    }
                },
                {
                    name: 'MA5',
                    type: 'line',
                    data: calculateMA(5),
                    smooth: true,
                    lineStyle: {
                        normal: {opacity: 0.5}
                    }
                },
                {
                    name: 'MA10',
                    type: 'line',
                    data: calculateMA(10),
                    smooth: true,
                    lineStyle: {
                        normal: {opacity: 0.5}
                    }
                },
                {
                    name: 'MA20',
                    type: 'line',
                    data: calculateMA(20),
                    smooth: true,
                    lineStyle: {
                        normal: {opacity: 0.5}
                    }
                },
                {
                    name: 'MA30',
                    type: 'line',
                    data: calculateMA(30),
                    smooth: true,
                    lineStyle: {
                        normal: {opacity: 0.5}
                    }
                },

            ]
        };
        myChart.setOption(option)
    }
    // influnceMarket();

// 判别原因（暂弃用）
    //
    function Features(){
        var myChart = echarts.init(document.getElementById('Features'));
        var option = {
            title: {
                text: ''
            },
            tooltip: {},
            legend: {
                // data: ['预算分配（Allocated Budget）', '实际开销（Actual Spending）']
            },
            radar: {
                // shape: 'circle',
                name: {
                    textStyle: {
                        color: '#fff',
                        backgroundColor: '#999',
                        borderRadius: 3,
                        padding: [3, 5]
                    }
                },
                indicator: [
                    { name: '质疑度', max: 60},
                    { name: '发布者可疑度', max: 60},
                    { name: '扩散速度', max: 60},
                    { name: '波及人次', max: 60},
                    { name: '评论数', max: 60},
                    { name: '转发数', max: 60}
                ]
            },
            series: [{
                name: '',
                type: 'radar',
                // areaStyle: {normal: {}},
                data : [
                    {
                        value : [60,15,10,50,30,40],
                        // name : '预算分配（Allocated Budget）'
                    },
                    //  {
                    //     value : [5000, 14000, 28000, 31000, 42000, 21000],
                    //     name : '实际开销（Actual Spending）'
                    // }
                ]
            }]
        };
        myChart.setOption(option)
    }
    // Features();