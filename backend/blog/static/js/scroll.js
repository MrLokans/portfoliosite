(function(){
    'use strict';
    
    var MIN_SROLL_DISTANCE = 100;
    var SCROLL_SELECTOR = '.scroll-to-top';
    var SCROLL_UP_TO = 0;
    var SCROLL_DURATION = 400;

    $(document).ready(function(){
        $(window).scroll(function(){
            if ($(this).scrollTop() >MIN_SROLL_DISTANCE ){
                $(SCROLL_SELECTOR).fadeIn();
            } else {
                $(SCROLL_SELECTOR).fadeOut();
            }
        });

        $(SCROLL_SELECTOR).click(function() {
            $('html, body').animate({scrollTop: SCROLL_UP_TO}, SCROLL_DURATION);
            return false;
        });
    });


})();

