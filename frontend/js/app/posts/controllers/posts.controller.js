(function(){
    'use strict';

    angular.module('andersblog.posts.controllers')
           .controller('PostsController', PostsController)
           .controller('PostDetailController', PostDetailController);

    PostsController.$inject = ['$scope', '$log', '$http', '$sce', 'ngDialog', 'Posts', 'marked', 'lodash'];
    PostDetailController.$inject = ['$scope', '$http', '$sce', '$routeParams', 'Posts', 'marked'];
    

    function PostsController($scope, $log, $http, $sce, ngDialog, Posts, marked, lodash){

        $scope.pagination = {
            totalItems: 0,
            currentPage: 0,
            itemsPerPage: 25
        };

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
            Posts.query(function(posts){
                $scope.posts = posts;
                lodash.each(posts, function(value){
                    value.markdown = $sce.trustAsHtml(marked(value.content));
                });
            });
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
        $scope.getPosts();
    }

    function PostDetailController($scope, $http, $sce, $routeParams, Posts, marked){
        Posts.get({id: $routeParams.post_id}, function(post){
            $scope.post = post;
            $scope.post.markdown = $sce.trustAsHtml(marked($scope.post.content));
        });
    }

})();