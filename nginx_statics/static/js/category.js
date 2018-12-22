// <a href="#" class="button button-glow button-border button-rounded button-royal button-small">button</a>

$(function () {
    var tag_list = new Array();
   $.ajax({
       url:"/apis/categories/",
       type: "get",
       success:function (data, status) {
           $("#count-span").text(data.length);
           for(var i=0;i<data.length;i++){
               var $id = data[i].id;
               var $title = data[i].title;
               var tag = {};
               tag.text = $title;
               tag.weight = 1;
               tag.link = "/cat4art/" + $id;
               tag_list.push(tag);
           }
           // var json_tag = JSON.stringify(tag_list);
           $("#cloud").jQCloud(tag_list, {
               height: data.length * 100,
               removeOverflowing: false,
               delayedMode: true,
           });
       }
   }) 
});




