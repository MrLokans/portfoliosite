(function(){
    'use strict';

    angular.module('andersblog.books.services')
           .factory('Books', Books);

    Books.$inject = ['$http', '$resource', 'ENDPOINT'];

    function Books($http, $resource){
        return $resource(ENDPOINT.API_URL + '/api/books/:id?format=json', 
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