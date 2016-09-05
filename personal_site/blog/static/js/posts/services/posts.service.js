(function(){
    'use strict';

    angular.module('andersblog.posts.controllers')
           .controller('PostListController', PostListController);

    PostListController.$inject = ['$scope', '$http', 'Subscription'];

    function PostListController($scope, $http, Subscription){
    }
})();

(function(){
    'use strict';

    angular.module('andersblog.posts.services')
           .factory('Posts', Posts);

    Posts.$inject = ['$http'];

    function Posts($http){
        var Posts = {
            getPostList: getPostList
        };
        return Posts;

        function getPostList(){
            return $http.get('/api/blog/', {}).then(successFunc, errorFunc);
        }
        function successFunc(data, status, headers, config){
            console.log(data);
        }
        function errorFunc(data, status, headers, config){
            console.log(data);
        }
    }
})();