(function(){
    'use strict';
    angular.module('andersblog.books.directives')
           .controller('SingleBookController', SingleBookController)
           .controller('BookDetailController', BookDetailController);

           SingleBookController.$inject = ['$scope', '$http', 'Books', 'ENDPOINT'];
           BookDetailController.$inject = ['$scope', '$http', '$routeParams', 'ngDialog', 'Books'];


            function SingleBookController($scope, $http, Books){
                $scope.save = function(){
                    var book = $scope.book;
                    var id = book.id;
                    return $http.put(ENDPOINT.API_URL + '/api/books/' + id + '/', {
                        'title': book.title,
                        'percentage': book.percentage,
                        'notes': book.notes,
                    });
                };
            }

            function BookDetailController($scope, $http, $routeParams, ngDialog, Books){
                $scope.book = Books.get({id: $routeParams.book_id});

                $scope.openDetails = function(){
                    var options = {
                        template: 'book-detail-edit.html', 
                        className: 'ngdialog-theme-default',
                        scope: $scope,
                    };
                    ngDialog.open(options);
                };
            }
})();