(function(){
    'use strict';

    angular.module('andersblog.posts.controllers')
           .controller('PostsController', PostsController)
           .controller('PostDetailController', PostDetailController);

    PostsController.$inject = ['$scope', '$http', 'Posts'];
    PostDetailController.$inject = ['$scope', '$http', '$routeParams', 'Posts'];
    

    function PostsController($scope, $http, Posts){
        $scope.getPosts = function(){
            $scope.posts = Posts.query();
        };

        $scope.removePost = function(postId){
            Posts.remove({id: postId});
            $scope.getPosts();
        };
        $scope.posts = Posts.query();
    }

    function PostDetailController($scope, $http, $routeParams, Posts){
        $scope.post = Posts.get({id: $routeParams.post_id});
    }

})();