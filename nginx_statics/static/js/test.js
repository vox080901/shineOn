$(function () {
   $.ajax({
        url: "apis/shineon/",
        type: "get",
        success: function (data, status) {
                for(var i=0; i<data.length; i++){
                    console.log(data[i].test01_varchar);
            }


       }
   })
});