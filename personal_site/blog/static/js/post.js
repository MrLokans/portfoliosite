$(document).ready(function($) {
    posts = $('.post-content').each(function() {
        content = $(this);
        content.html(renderContent(content.text()));

    });
});

function renderContent(content){
    console.log(content);
    var markedContent = marked(content || '');
    return markedContent;
}