(function(){
    'use strict';

    angular
        .module('andersblog.common')
        .service('paginationService', paginationService);

    function paginationService(){
        return {
            buildPaginationFromResponse: buildPaginationFromResponse
        };
        function buildPaginationFromResponse(responseData){
            return {
                totalItems: 0,
                currentPage: 0,
                itemsPerPage: 25
            };
        }
    }

})();