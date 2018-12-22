$(function () {
    var tag_list = new Array();
   $.ajax({
       url:"/apis/tags/",
       type: "get",
       success:function (data, status) {
           $("#count-span").text(data.length);
           for(var i=0;i<data.length;i++){
               var $id = data[i].pk;
               var $tag_name = data[i].tag_name;
               var tag = {};
               tag.text = "#" + $tag_name;
               tag.weight = 1;
               tag.link = "/tag4art/" + $id;
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