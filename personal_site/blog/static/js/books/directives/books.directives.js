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
                    link: function postLink(scope, element, attrs){
                        var bookTitle = element.find('.book-data__title')
                        bookTitle.on('click', function(){
                            element.find(".book-data__notes-list").toggle("hide");
                        });
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