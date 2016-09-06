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
           }])

           .directive('bookSingle', function(){
                return {
                    restrict: 'E',
                    scope: {
                        book: '=',
                    },
                    templateUrl: 'book-single.html'
                };
           })

           .directive('bookNote', function(){
                return {
                    restrict: 'E',
                    scope: {
                        note: '=',
                    },
                    templateUrl: 'books-note.html'
                };
           });
})();