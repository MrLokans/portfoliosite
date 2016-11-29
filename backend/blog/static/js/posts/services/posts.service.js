(function(){
    'use strict';

    angular.module('andersblog.posts.services')
           .factory('Posts', Posts);

    Posts.$inject = ['$http', '$resource'];

    function Posts($http, $resource){
        return $resource('/api/blog/:id', {id: '@_id'});
    }
})();