(function(){
    'use strict';

    angular.module('andersblog.posts.controllers')
           .controller('PostListController', PostListController);

    PostListController.$inject = ['$scope', '$http', 'Subscription'];
    

    function PostListController($scope, $http, Subscription){
    }

})();