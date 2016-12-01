(function(){
    'use strict';

    angular.module('andersblog.posts.controllers')
           .controller('PostListController', PostListController)
           .controller('PostDetailController', PostDetailController);

    PostListController.$inject = ['$scope', '$http', 'Subscription'];
    PostListController.$inject = ['$scope', '$http', '$routeParams', 'Posts'];
    

    function PostListController($scope, $http, Subscription){
    }

    function PostDetailController($scope, $http, $routeParams, Posts){
        $scope.post = Posts.get({id: $routeParams.post_id});
    }

})();