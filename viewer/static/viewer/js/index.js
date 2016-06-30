$(document).ready(function() {

    $("#cloud_select").val($("#cloud_select_helper").text());
    $("#gallery_select").val($("#gallery_select_helper").text());

    $(".image-item").mouseenter(function(){
        $(this).find(".over-image").slideDown();
    });

    $(".image-item").mouseleave(function(){
        $(this).find(".over-image").slideUp();
    });

    $(".single-pager").click(function() {

        if ($(this).hasClass("active") || $(this).hasClass("disabled"))
            return;

        var value = $(this).attr("value");
        if (value == null)
            return;

        var final_value = 1;
        if (value < 0) {
            if (value == -11)
                final_value = parseInt(global_active) + 1;
            else if (value == -9)
                final_value = parseInt(global_active) - 1;
            else if (value == -5)
                final_value = 1;
            else if (value == -15)
                final_value = global_total;
        } else {
            final_value = value;
        }

        $("#paging-form-page").val(final_value);

        var form = $("#paging-form");
        form.submit();
    })
})

function set_paging(active, total) {
    global_active = active;
    global_total = total;

    var paging = $(".pagination");

    if (active == 1) {
        $(paging).find("#first-page").addClass("disabled");
        $(paging).find("#prev-page").addClass("disabled");
    } else if (active == total) {
        $(paging).find("#last-page").addClass("disabled");
        $(paging).find("#next-page").addClass("disabled");
    }

    $(paging).find("li[value="+active+"]").addClass("active");
}
