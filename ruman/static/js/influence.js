

function Influence(){
  this.ajax_method = 'GET';
}

function getDate_in(tm){
  var tt = new Date(parseInt(tm)*1000).format("MM-dd");
  return tt;
}

Influence.prototype = {  
  call_ajax_request:function(url, method, callback){
      $.ajax({
          url:url,
          type:"GET",
          dataType:'json',
          async:true,
          success:callback,
      });
  },

  influ_skill_new:function(data){
    data=data[0];
    var init_ca=[]
    console.log(weibo_num/399139, data.origin_weibo_retweeted_total_number/1009130, data.origin_weibo_comment_total_number/241403, data.origin_weibo_comment_brust_average/36345.5, data.origin_weibo_retweeted_brust_average/79278);
    var radius_1=Math.max(weibo_num/399139, data.origin_weibo_retweeted_total_number/1009130, data.origin_weibo_comment_total_number/241403, data.origin_weibo_comment_brust_average/36345.5, data.origin_weibo_retweeted_brust_average/79278);
    console.log(radius_1);
    
    var k=100/radius_1;
    console.log(k*weibo_num/399139, k*data.origin_weibo_retweeted_total_number/1009130, k*data.origin_weibo_comment_total_number/241403, k*data.origin_weibo_comment_brust_average/36345.5, k*data.origin_weibo_retweeted_brust_average/79278);
    init_ca[0]=k*weibo_num/399139+10;
    init_ca[1]=k*data.origin_weibo_retweeted_total_number/1009130+20;
    init_ca[2]=k*data.origin_weibo_comment_total_number/241403;
    init_ca[4]=k*data.origin_weibo_retweeted_brust_average/79278;
    init_ca[3]=k*data.origin_weibo_comment_brust_average/36345.5;

    var myChart = echarts.init(document.getElementById('originalSkill')); 
    var option = {
    title : {
        text: '原创技能',
        subtext: '网红必备技能一'
    },
    tooltip : {
        trigger: 'axis'
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    polar : [
        {
            indicator : [
                {text : '原创数', max  : 100},
                {text : '原创被转发数', max  : 100},
                {text : '原创被评论数', max  : 100},
                {text : '原创微博评论速度', max  :100},
                {text : '原创微博转发速度', max  : 100},
            ],
            radius : 102
        }
    ],
    series : [
        {
            name: '原创技能',
            type: 'radar',
            itemStyle: {
                normal: {
                    areaStyle: {
                        type: 'default'
                    }
                }
            },
            data : [
                {
                    value : [init_ca[0].toFixed(2),init_ca[1].toFixed(2),init_ca[2].toFixed(2),init_ca[3].toFixed(2),init_ca[4].toFixed(2)],
                    name:'原创技能相对排位'
                }
            ]
        }
      ]
    };
  myChart.setOption(option);
},
  influ_skill_new2:function(data){
    data=data[0];
    var init_ca=[]
    console.log(data.retweeted_weibo_number/85378, data.comment_weibo_number/1, data.retweeted_weibo_retweeted_total_number/169076, data.retweeted_weibo_comment_total_number/7074, data.retweeted_weibo_retweeted_brust_average/6434.5);
    var radius_2=Math.max(data.retweeted_weibo_number/85378, data.comment_weibo_number/1, data.retweeted_weibo_retweeted_total_number/169076, data.retweeted_weibo_comment_total_number/7074, data.retweeted_weibo_retweeted_brust_average/6434.5);
    
    var k=100/radius_2

    init_ca[0]=k*data.retweeted_weibo_number/85378+20;
    init_ca[1]=k*data.comment_weibo_number/1+10;
    init_ca[2]=k*data.retweeted_weibo_retweeted_total_number/169076;
    init_ca[4]=k*data.retweeted_weibo_comment_total_number/7074;
    init_ca[3]=k*data.retweeted_weibo_retweeted_brust_average/6434.5;


    var myChart = echarts.init(document.getElementById('spreadSkill')); 
    var option = {
    title : {
        text: '传播技能',
        subtext: '网红必备技能二'
    },
    tooltip : {
        trigger: 'axis'
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    polar : [
        {
            indicator : [
                {text : '转发数', max  : 100},
                {text : '评论数', max  : 100},
                {text : '转发微博被转发数', max  : 100},
                {text : '转发微博被评论数', max  : 100},
                {text : '转发微博转发速度', max  : 100},
            ],
            radius : 102
        }
    ],
    series : [
        {
            name: '传播技能',
            type: 'radar',
            itemStyle: {
                normal: {
                    areaStyle: {
                        type: 'default'
                    }
                }
            },
            data : [
                {
                    value : [init_ca[0].toFixed(2),init_ca[1].toFixed(2),init_ca[2].toFixed(2),init_ca[3].toFixed(2),init_ca[4].toFixed(2),init_ca[4].toFixed(2)],
                    name:'传播技能相对排位'
                }
            ]
        }
      ]
    };
  myChart.setOption(option);
},

  get_weibo_num:function(data){
      weibo_num=data['statusnum'];
  }

}

//获取当前时间，格式YYYY-MM-DD
function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    currentdate = year + seperator1 + month + seperator1 + strDate;
    return currentdate;
}




var influSkill_url = '/influence_application/specified_user_active/?date=2016-05-21&uid=3069348215';
Influence.call_ajax_request(influSkill_url, Influence.ajax_method, Influence.influ_skill_new);
Influence.call_ajax_request(influSkill_url, Influence.ajax_method, Influence.influ_skill_new2);



