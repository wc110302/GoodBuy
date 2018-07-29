
function lookUser(name) {
    var myName = name
    post_data = {
        'myName': myName
    }
    $.ajax({
        url: "/admin_user_manage/lookUser/",
        headers:{"X-CSRFToken":$.cookie('csrftoken')},
        type: "POST",
        data: post_data,
        success: function (data) {

            if (data.code == 200) {
                alert(data.password)
            } else {
                alert(data.code);
            }
        }
    });
}

function deleteUser(name) {
    var myName = name
    post_data = {
        'myName': myName
    }
    if(confirm("确定删除该管理员?")) {
        //点击确定后操作


        $.ajax({
            url: "/admin_user_manage/deleteUser/",
            headers:{"X-CSRFToken":$.cookie('csrftoken')},
            type: "POST",
            data: post_data,
            success: function (data) {

                if (data.code == 200) {
                    alert(data.msg)
                    location.reload()
                } else {
                    alert(data.code);
                }
            }
        });
    }
}


function editUser(name) {
    var psd = window.prompt('请填入修改后的密码,按确认提交', 'password');
    //点击确定后操作
    post_data = {
        'myName': name,
        'psd': psd,
    }
    if (psd.length < 6) {
        alert('密码长度过短(建议6位及以上)')
    } else {
        if (psd != null) {
            $.ajax({
                url: "/admin_user_manage/EditUserPsd/",
                type: "POST",
                headers: {"X-CSRFToken": $.cookie('csrftoken')},
                data: post_data,
                success: function (data) {
                    if (data.code == 200) {
                        alert(data.msg)
                        location.reload()
                    } else {
                        alert(data.code);
                    }
                }
            });
        } else {
            alert('密码不能为空!')
        }
    }
}
