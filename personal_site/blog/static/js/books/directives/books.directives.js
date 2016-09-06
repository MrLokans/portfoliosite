(function(){
    'use strict';
    angular.module('andersblog.books.directives')
           .directive('booksList', ['Books', function(Books){
                return {
                    restrict: 'E',
                    controller: ['$scope', 'Books', function($scope, Books){
                        $scope.books = Books.query();
                    }],
                    templateUrl: 'books-list.html'
                };
           }]);
})();