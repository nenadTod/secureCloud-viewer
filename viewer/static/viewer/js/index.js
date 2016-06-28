$(document).ready(function() {
    $("#cloud_select").val($("#cloud_select_helper").text());

    $(".image-item").mouseenter(function(){
        $(this).find(".over-image").slideDown();
    });

    $(".image-item").mouseleave(function(){
        $(this).find(".over-image").slideUp();
    });
})
