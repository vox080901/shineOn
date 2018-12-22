$(function () {

    var $title = $(".title");
    var $authorname = $(".author_name");
    var $category = $(".category");
    var $createtime = $(".create_time");
    var $updatetiem = $(".update_time");
    var $tags = $(".atags");
    var $readcount = $(".readcount");
    var $summary = $("#summary");
    var $article = $(".artcle");
    var $up = $(".upnumber");
    var $down = $(".downnumber");
    var article_pk = document.URL.split("/")[4];
    var count_up = 0;
    var count_down = 0;

    // console.log(article_pk); # wenti

    function change_count(countup, countdown) {
        count_up = countup;
        count_down = countdown;
    }

    function change(i) {
        article_pk = i;
    }

    if (article_pk === "" || article_pk === "#") {
        change("1")
    }


    $.ajax({
        url: "/apis/articles/" + article_pk + "/",
        type: "get",
        success: function (data, status) {
            // $(".caption").text(data.content);
            for (var i = 0; i < data.tags.length; i++) {
                // console.log(data.tags[i]);
                // console.log(data.tags.length);
                var $span = $("<a class='btn btn-default'>" + "<span>" + "#" + data.tags[i].tag_name + "</span>" + "</a>");
                $span.attr("href", "/tag4art/" + data.tags[i].tag_id);
                $tags.append($span);
            }

            var $cata = $("<a>" + "<span>" + data.category + "</span>" + "</a>");
            $cata.attr("href", "/cat4art/" + data.category_id);
            $title.text(data.title);
            var $authora = $("<a href='#'>" + "<span>" + data.author_name + "</span>" + "</a>");
            $authorname.append($authora);
            $createtime.text(data.create_time.split("T")[0]);
            $updatetiem.text(data.update_time.split("T")[0]);
            // console.log(data.create_time.split("T"));
            $category.append($cata);
            $readcount.text(data.count_read); //---> 待扩展(已扩展)
            $summary.text(data.summary);
            $article.html(data.content); //之后扩展为html, 数据库中以存带html标签的文章, 直接渲染好
            $up.text(data.count_up);
            $down.text(data.count_down);
            change_count(data.count_up, data.count_down)
        }
    });


    var imgstatus = 0;

    function changeimgstatus() {
        imgstatus = 1
    }

    $(".upimg").on("click", function () {
        if (imgstatus === 0) {
            $.ajax({
                type: "patch",
                url: "/apis/updown/" + article_pk + "/",
                data: {'data': 1},
                success: function (data, status) {
                    if (data.code == 1) {
                        $(".label-success").removeClass("hide");
                    }
                    if (data.code == 0) {
                        $(".label-warning").removeClass("hide");
                    }
                },
                error: function (data) {
                    $(".label-info").removeClass("hide");
                }
            });
            $(".upimg").attr("src", "../imgs/uped.png");
            $up.text(count_up + 1);
            changeimgstatus();
        }
    });
    $(".downimg").on("click", function () {
        if (imgstatus === 0) {
            $.ajax({
                type: "patch",
                url: "/apis/updown/" + article_pk + "/",
                // url: "/apis/submit/",
                // contentType: "application/json",
                success: function (data, status) {
                    if (data.code == 1) {
                        $(".label-success").removeClass("hide");
                    }
                    if (data.code == 0) {
                        $(".label-warning").removeClass("hide");
                    }
                },
                error: function (data) {
                    $(".label-info").removeClass("hide");
                }
            });
            $(".downimg").attr("src", "../imgs/downed.png");
            $down.text(count_down + 1);
            changeimgstatus();
        }
    });

    $(".upimg").on("mouseover", function () {
        $(".upimg").addClass("animated tada infinite");
    });
    $(".upimg").on("mouseleave", function () {
        $(".upimg").removeClass("animated tada infinite");
    });

    $(".downimg").on("mouseover", function () {
        $(".downimg").addClass("animated bounce infinite");
    });
    $(".downimg").on("mouseleave", function () {
        $(".downimg").removeClass("animated bounce infinite");
    });

});