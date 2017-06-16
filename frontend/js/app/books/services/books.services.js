(function(){
    'use strict';

    angular.module('andersblog.books.services')
           .factory('Books', Books);

    Books.$inject = ['$http', '$resource', 'ENDPOINT', 'urlConstants'];

    function Books($http, $resource, ENDPOINT, urlConstants){
        return $resource(ENDPOINT.API_URL + urlConstants.BOOKS_LIST_URL, 
            {id: '@_id'},
            {
                'query': {
                    method: 'GET', 
                    isArray: true,
                    transformResponse: function(data, headers){
                        var booksData = JSON.parse(data);
                        return booksData.results;
                    }
                }
            });
    }
})();