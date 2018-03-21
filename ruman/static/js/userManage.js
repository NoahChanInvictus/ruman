var userGroupTable_url='';
// public_ajax.call_request('get',userGroupTable_url,userGroup);
var objData=[
    {'a':'user1','b':'普通用户','c':'213131@126.com','d':'2017-11-1 11:34'},
    {'a':'suer2','b':'游客','c':'asida@136.com','d':'2016-12-2 10:33'},
    {'a':'sad23','b':'管理员','c':'admin@163.com','d':'2016-09-22 22:18'},
    {'a':'user1','b':'普通用户','c':'213131@126.com','d':'2017-11-1 11:34'},
    {'a':'suer2','b':'游客','c':'asida@136.com','d':'2016-12-2 10:33'},
    {'a':'sad23','b':'管理员','c':'admin@163.com','d':'2016-09-22 22:18'},
    {'a':'user1','b':'普通用户','c':'213131@126.com','d':'2017-11-1 11:34'},
    {'a':'suer2','b':'游客','c':'asida@136.com','d':'2016-12-2 10:33'},
    {'a':'sad23','b':'管理员','c':'admin@163.com','d':'2016-09-22 22:18'},
    {'a':'user1','b':'普通用户','c':'213131@126.com','d':'2017-11-1 11:34'},
    {'a':'suer2','b':'游客','c':'asida@136.com','d':'2016-12-2 10:33'},
    {'a':'sad23','b':'管理员','c':'admin@163.com','d':'2016-09-22 22:18'},
    {'a':'user1','b':'普通用户','c':'213131@126.com','d':'2017-11-1 11:34'},
    {'a':'suer2','b':'游客','c':'asida@136.com','d':'2016-12-2 10:33'},
    {'a':'sad23','b':'管理员','c':'admin@163.com','d':'2016-09-22 22:18'},
    {'a':'user1','b':'普通用户','c':'213131@126.com','d':'2017-11-1 11:34'},
    {'a':'suer2','b':'游客','c':'asida@136.com','d':'2016-12-2 10:33'},
    {'a':'sad23','b':'管理员','c':'admin@163.com','d':'2016-09-22 22:18'},
    {'a':'user1','b':'普通用户','c':'213131@126.com','d':'2017-11-1 11:34'},
    {'a':'suer2','b':'游客','c':'asida@136.com','d':'2016-12-2 10:33'},
    {'a':'sad23','b':'管理员','c':'admin@163.com','d':'2016-09-22 22:18'},
    {'a':'user1','b':'普通用户','c':'213131@126.com','d':'2017-11-1 11:34'},
    {'a':'suer2','b':'游客','c':'asida@136.com','d':'2016-12-2 10:33'},
    {'a':'sad23','b':'管理员','c':'admin@163.com','d':'2016-09-22 22:18'}
];
function userGroup(data) {
    $('#userGroup').bootstrapTable('load', data);
    $('#userGroup').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 8,//单页记录数
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
                title: "用户名称",//标题
                field: "a",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     if (row.user_name==''||row.user_name=='null'||row.user_name=='unknown'||!row.user_name){
                //         return '未知';
                //     }else {
                //         return row.user_name;
                //     };
                // }
            },
            {
                title: "用户角色",//标题
                field: "b",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "邮箱",//标题
                field: "c",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "上次登录时间",//标题
                field: "d",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "操作",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<span style="cursor:pointer;color:white;" onclick="editThis(\''+row.a+'\')" title="编辑"><i class="icon icon-edit"></i></span>'+
                        '<span style="cursor:pointer;color:white;display: inline-block;margin: 0 10px;" onclick="delThis(\''+row.a+'\')" title="删除"><i class="icon icon-trash"></i></span>';
                }
            },
        ],
    });
};
userGroup(objData)