$(document).ready(function () {
    $("#form1").submit(function (e) {
        e.preventDefault();
        var serializedData = $(this).serialize();
         $.ajax({
             type: 'POST',
             dataType: 'json',
             url: $("#form1").attr("action"),
             data: serializedData,
             success: function (d) {
                 if(d['status']==true){
                     alert("ok");
                     location.reload()
                 }else{
                     var errors = d['errors'];
                     alert(errors);
                 }
             },
             error: function (d){
                 alert("не заполнено");
             }
         });
    });

    $('.js-cnt').hide();
    $('.js-cnt-show').click(function (){
        $('.js-cnt').toggle();
        $('.js-ctn-qps').css("transform","rotate(180deg)")
        $('.js-cnt-show .row').css("border","none")
    });

    $("#form2").submit(function (e) {
        e.preventDefault();
        var serializedData = $(this).serialize();
         $.ajax({
             type: 'POST',
             dataType: 'json',
             url: $("#form2").attr("action"),
             data: serializedData,
             success: function (d) {
                 if(d['status']==true){
                     alert("ok");
                     location.reload()
                 }else{
                     $(this).addClass('errr');
                     var errors = d['errors'];
                     alert(errors);
                 }

             },
             error: function (d){
                 alert("не заполнено");
             }
         });
    });
    $("#search1").submit(function (e) {
        let day1 = $('#day1').val()
        let month1 = $('#month1').val()
        let year1 = $('#year1').val()
        let day2 = $('#day2').val()
        let month2 = $('#month2').val()
        let year2 = $('#year2').val()

        if (year1 == 0){
            alert("Year 1 not found")
        }
        else if (year2 == 0){
            alert("Year 2 not found")
        }
    });


})