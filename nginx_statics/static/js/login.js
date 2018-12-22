$(function () {
    var flag = false;
    var flag_email = false;
    var flag_password = false;
    var reg_mail = /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/;
    var reg_password = /([a-zA-Z\d.\-+*/!@#$%^&()]){6,20}/;
    var $password = $("#password");
    var $email = $("#email");
    var $alert = $(".alert-danger");
    var $buttonsubmit = $("#buttonsubmit");

    function removeHide() {
        if (flag_email === true && flag_password === true) {
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

    $buttonsubmit.on("click", function () {
        if (flag === true) {
            $.ajax({
                url: "/apis/login/",
                type: 'post',
                // contentType: "application/json",
                data: {
                    "email": $email.val(),
                    "password": $password.val(),
                },
                success: function (data, status) {
                    console.log(data);
                    $("#passworderror").addClass("hide");
                    $(".alert-success").text("欢迎你, " + data.username + "!");
                    $(".alert-success").removeClass("hide");
                    window.location.href = "/articles/" ;
                },
                error: function (data) {
                    console.log(data);
                    $("#passworderror").text("帐号密码错误");
                    $("#passworderror").removeClass("hide");
                }
            })
        }
    })

});