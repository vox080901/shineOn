$(function () {
    var url = location.href.split("/");
   $.ajax({
       url:"/apis/" + url[3] + "/" + url[4],
       type:"get",
       success:function (data, status) {
           // console.log(data.results[0].years);
           $("#count-span").text(data.count);
           $(".progress-bar").text(data.count + "%");
           $(".progress-bar-success").css("width", data.count + "%");
           if(data.previous === null){
                $(".pre").addClass("disabled");
           }
           if(data.next === null){
                $(".nex").addClass("disabled");
           }
           $("#pre").attr("href", data.previous);
           $("#nex").attr("href", data.next);
           for(var i=0;i<data.results.length;i++){
               var year_title = $(".year-title").children().last().text();
               var $year = data.results[i].year;

               if($year != year_title){
                   var $div = $("<div class='year-title animated bounceInLeft'>" + $year + "</div>");
                   var $ul = $("<ul class='article-ul animated bounceInUp'>" + "</ul>");
                   $div.attr("id", "div" + $year);
                   $ul.attr("id", "ul" + $year);
                   $div.text($year);
                   $("#ul").append($div);
                   $("#ul").append($ul);
               }
               var $article = data.results[i].article;
               for(var j=0;j<$article.length;j++){
                   // console.log($article[j]);
                    var $article_title = $article[j].title;
                    var $article_createdate = $article[j].create_date;
                    var $aspan = $("<a class='article-a button button-block button-rounded button-large' style='text-align: left'>" + "<span class='date'>" + $article_createdate + "</span>" + $article_title + "</a>");
                    $aspan.attr("href", "/articles/" + $article[j].pk);
                    var $li = $("<li class='article-li'>" + "</li>").append($aspan);
                    $("#ul" +$year).append($li);
               }
           }
       }
   });
});