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
                        var collapseNotesBlock = element.find('.collapse-notes');
                        collapseNotesBlock.on('click', function(e){
                            e.preventDefault();
                            var notesList = element.find('.book-data__notes-list');
                            notesList.toggle("hide");
                        });
                    },
                    templateUrl: 'book-single.html',
                    controller: 'SingleBookController',
                    controllerAs: 'vm'
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