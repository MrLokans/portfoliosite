(function(){
    'use strict';

    angular.module('andersblog.posts.directives')
           .directive('postList', ['Posts', function(Posts){
                return {
                    restrict: 'E',
                    controller: ['$scope', 'Posts', function($scope, Posts){
                        $scope.posts = Posts.query();
                    }],
                    templateUrl: 'post-list.html'
                };
           }]);
})();