$(function () {
   var cid = location.href.split("/")[4];
    $.ajax({
        url:"/apis/categories/articles/cat4art/" + cid + "/",
        type:"get",
        success:function (data, status) {
            var results = data.results;
            var catname = results[0].category;
            var count = data.count;
           if(data.previous === null){
                $(".pre").addClass("disabled");
           }
           if(data.next === null){
                $(".nex").addClass("disabled");
           }
            $("#catname").text(catname);
           $("#count-num").text(count);
            for(var i=0; i<results.length; i++){
                var $article_title = results[i].title;
                var $article_createdate = results[i].create_date;
                var $aid = results[i].pk;
                var $aspan = $("<a class='article-a button button-block button-rounded button-large'>" + "<span class='date'>" + $article_createdate + "</span>" + $article_title + "</a>");
                $aspan.attr("href", "/articles/" + $aid);
                var $li = $("<li class='article-li'>" + "</li>").append($aspan);
                $("#ul").append($li);
            }
        }
    })
});