(function(){
    'use strict';
    angular.module('andersblog.books.directives')
           .controller('SingleBookController', ['$scope', '$http', 'ngDialog', function($scope, $http, ngDialog){

                $scope.save = function(){
                    var book = $scope.book;
                    var id = book.id;
                    return $http.put('/api/books/' + id + '/', {
                        'title': book.title,
                        'percentage': book.percentage,
                        'notes': book.notes,
                    });
                };

                $scope.openDetails = function(){
                    var options = {
                        template: 'book-detail-edit.html', 
                        className: 'ngdialog-theme-default',
                        scope: $scope,
                    };
                    ngDialog.open(options);
                };

           }]);
})();