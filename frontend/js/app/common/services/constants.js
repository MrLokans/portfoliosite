(function(){
    'use strict';
    angular
        .module('andersblog.common')
        .service('urlConstants', urlConstants);

    function urlConstants(){
        return {
            BOOKS_LIST_URL: '/api/books/:id?format=json',
        };
    }
})();