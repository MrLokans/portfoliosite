$(document).ready(function() {
    $(".book-data__title").on("click", function(){
        $(this).parent().find(".book-data__notes-list").toggle("hide");
    });
});