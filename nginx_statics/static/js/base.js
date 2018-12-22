$(function () {

    $("#left-menu").sidr({
        name: "leftnav",
        side: "left",
    });

    function getSession(){
        var username = $.cookie("username");
        if(username){
            $("#username").text(username);
            $("#username").removeClass("hide");
        }else {
            $("#username").text(username);
            $("#username").addClass("hide");
        }
    }

    getSession();

    $.ajax({
        url: "/apis/tagandcat/",
        type: "get",
        success: function (data, status) {
            for (var i = 0; i < data.length; i++) {
                var $catnum = data[i].catnum;
                var $tagnum = data[i].tagnum;
                $("#catnum").text($catnum);
                $("#tagnum").text($tagnum);
                // $trtd.text(data[i].title);
                // $("tbody").append($tr);
            }
        }
    });


    $(window).resize(function () {
        // console.log($(window).width());  //可视域宽度
        // console.log($(document.body).outerWidth(true)); //body宽度
        if ($(document.body).outerWidth(true) >= 750){
            $("#datatarget").css("background-image", "none");
        }
        if ($(document.body).outerWidth(true) < 750){
            $("#datatarget").css("background-image", "url(../imgs/kis.png)");
        }

        if ($(window).width() !== $(document.body).outerWidth(true)) {
            // console.log($(window).width());  //可视域宽度
            // console.log($(document.body).outerWidth(true)); //body宽度
            $(".tag").trigger("click");  //自动触发点击事件
        }
    });


    $(".ham").on("click", function () {
        $("#datatarget").css("background-image", "url(../imgs/kis.png)");
        $("#datatarget").css("background-size", "contain");
        $("#datatarget").css("background-repeat", "no-repeat");
    })

});