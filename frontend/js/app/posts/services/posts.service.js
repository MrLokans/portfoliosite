(function(){
    'use strict';

    angular.module('andersblog.posts.services')
           .factory('Posts', Posts);

    Posts.$inject = ['$http', '$resource', 'ENDPOINT'];

    function Posts($http, $resource, ENDPOINT){
        return $resource(ENDPOINT.API_URL + '/api/blog/:id', {id: '@_id'});
    }
})();