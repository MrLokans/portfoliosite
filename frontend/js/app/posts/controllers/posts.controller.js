(function(){
    'use strict';

    angular.module('andersblog.posts.controllers')
           .controller('PostsController', PostsController)
           .controller('PostDetailController', PostDetailController);

    PostsController.$inject = ['$scope', '$log', '$http', 'ngDialog', 'Posts'];
    PostDetailController.$inject = ['$scope', '$http', '$routeParams', 'Posts'];
    

    function PostsController($scope, $log, $http, ngDialog, Posts){
        $scope.currentPost = {
            author: 'MrLokans',
            body: ""
        };

        $scope.openPostModal = function(){
            ngDialog.open(
                {
                    template: 'post-create.form',
                    scope: $scope
                });
        };

        $scope.getPosts = function(){
            $scope.posts = Posts.query();
        };

        $scope.removePost = function(postId){
            Posts.remove({id: postId});
            $scope.getPosts();
        };

        $scope.createPost = function(){
            $log.debug('Creating post;');
            var newPost = new Posts({content: $scope.currentPost.body,
                                     title: 'test title'});
            newPost.$save();
            $scope.getPosts();
        };
        $scope.posts = Posts.query();
    }

    function PostDetailController($scope, $http, $routeParams, Posts){
        $scope.post = Posts.get({id: $routeParams.post_id});
    }

})();