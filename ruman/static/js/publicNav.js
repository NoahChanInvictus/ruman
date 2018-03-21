$('#nav .nav_middle .main_li .li_a').on('mouseover',function () {
    $(this).siblings('.line').css({left:'0%'});
}).on('mouseout',function () {
    $(this).siblings('.line').css({left:'-100%'});
});
function createRandomItemStyle() {
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 128+127),
                Math.round(Math.random() * 128+127),
                Math.round(Math.random() * 128+127)
            ].join(',') + ')',

        }
    };
}