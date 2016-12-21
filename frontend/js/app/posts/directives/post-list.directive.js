(function(){
    'use strict';

    angular.module('andersblog.posts.directives')
       .directive('postList', ['Posts', function(Posts){
            return {
                restrict: 'E',
                controller: 'PostsController',
                templateUrl: 'post-list.html'
            };
       }]);
})();