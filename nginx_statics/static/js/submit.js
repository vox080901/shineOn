$(function () {
    var flag = false;
    var flag_email = false;
    var flag_name = false;
    var flag_password = false;
    var flag_confirm = false;
    var flag_authcode = false;
    var reg_mail = /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/;
    var reg_password = /([a-zA-Z\d.\-+*/!@#$%^&()]){6,20}/;
    var reg_authcode = /\d{4}/;
    var $username = $("#user_name");
    var $password = $("#password");
    var $confirm_password = $("#confirm_password");
    var $email = $("#email");
    var $authcode = $("#auth_code");
    var $alert = $(".alert-danger");
    var $buttonsubmit = $("#buttonsubmit");
    var $sendmail = $("#sendmail");
    var $send = $(".send");

    function sleep(numberMillis) {
        var now = new Date();
        var exitTime = now.getTime() + numberMillis;
        while (true) {
        now = new Date();
        if (now.getTime() > exitTime)
        return;
    }
}


    function removeHide() {
        if (flag_confirm === true && flag_email === true && flag_password === true && flag_name === true && flag_authcode === true) {
            $alert.addClass("hide");
            flag = true;
            $buttonsubmit.removeClass("disabled");
        }else {flag = false}
    }


    $email.on("blur", function () {
        if (!reg_mail.test($email.val())) {
            flag_email = false;
            $alert.text("请输入正确的邮箱");
            $alert.removeClass("hide");
            $buttonsubmit.addClass("disabled");
            removeHide()
        } else {
            flag_email = true;
            removeHide();
        }
    });

    $password.on("blur", function () {
        if($password.val().length > 0){
        if (!reg_password.test($password.val())) {
            flag_password = false;
            $alert.text("密码长度为6~20位,不能包含特殊字符");
            $alert.removeClass("hide");
            $buttonsubmit.addClass("disabled");
            removeHide()
        } else {
            flag_password = true;
            removeHide();
        }
        }else{
            $alert.text("密码不能为空");
            $alert.removeClass("hide");
            $buttonsubmit.addClass("disabled");
            flag_password = false;
            removeHide();
        }
    });

    $confirm_password.on("blur", function () {
        if($confirm_password.val().length > 0){
        if ($password.val() !== $confirm_password.val()) {
            flag_confirm = false;
            $alert.text("两次输入的密码不一致");
            $alert.removeClass("hide");
            $buttonsubmit.addClass("disabled");
            removeHide();
        } else {
            flag_confirm = true;
            removeHide();
        }
        }else {
            $alert.text("确认密码不能为空");
            $alert.removeClass("hide");
            $buttonsubmit.addClass("disabled");
            flag_confirm = false;
            removeHide();
        }
    });

    $username.on("blur", function () {
        if($username.val().length === 0){
            flag_name = false;
            $alert.text("昵称不能为空");
            $alert.removeClass("hide");
            $buttonsubmit.addClass("disabled");
            removeHide();
        }else {
            flag_name = true;
            removeHide();
        }
    });

    $authcode.on("blur", function () {
        if($authcode.val().length !== 0){
            if(!reg_authcode.test($authcode.val())){
                flag_authcode = false;
                $alert.text("验证码为四位数字");
                $alert.removeClass("hide");
                $buttonsubmit.addClass("disabled");
                removeHide();
            }else {
                flag_authcode = true;
                removeHide();
            }
        }else {
            $alert.text("验证码不能为空");
            $alert.removeClass("hide");
            $buttonsubmit.addClass("disabled");
            flag_authcode = false;
            removeHide();
        }
    });


    $sendmail.on("click", function () {
        if(flag_email){
            $send.text("验证发已发送至" + $email.val() + ",五分钟内有效");
            $(".send").removeClass("hide");
            $.ajax({
                url:"/apis/sendmail/",
                type: "get",
                data:{"email": $email.val()},
                success: function (data, status) {
                }
            })
            }else {
            $send.text("oops...邮箱有误");
            $send.removeClass("hide");
        }
    });

    $buttonsubmit.on("click", function () {
        if (flag === true) {
            $.ajax({
                url: "/apis/submit/",
                type: 'post',
                // contentType: "application/json",
                data: {
                    "username": $username.val(),
                    "email": $email.val(),
                    "password": $password.val(),
                    "confirm_password": $confirm_password.val(),
                    "authcode": $authcode.val()
                },
                success: function (data, status) {
					console.log(data);
                    var arr = Object.keys(data);
                    if(arr.length === 0){
                        $send.text("注册成功!");
                        sleep(2);
                        window.location.href = "/login/";
                    }else {
                        if(data.mail){
                            $send.text("点击信封发送验证码");
                            $send.removeClass("hide");
                        }else {
                            $send.addClass("hide");
                        }
                        if(data.user_name_code){
                            $("#namecodeerror").text("用户名只能包含英文,数字,下划线");
                            $("#namecodeerror").removeClass("hide")
                        }else {
                            $("#namecodeerror").addClass("hide")
                        }
                        if(data.authcode){
                            $("#authcodeerror").text("验证码错误");
                            $("#authcodeerror").removeClass("hide")
                        }else {
                            $("#authcodeerror").addClass("hide")

                        }
                        if(data.user_name){
                            $("#nameerror").text("用户名已被注册");
                            $("#nameerror").removeClass("hide")
                        }else {
                             $("#nameerror").addClass("hide")
                        }
                        if(data.account){
                            $("#emailerror").text("该账号已被注册");
                            $("#emailerror").removeClass("hide")
                        }else {
                            $("#emailerror").addClass("hide")
                        }
                    }
                },error:function (data) {
                    console.log(data.responseText)
                }
            })
        }
    })

});
