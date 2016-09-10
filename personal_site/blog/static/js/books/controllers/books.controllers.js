(function(){
    'use strict';
    angular.module('andersblog.books.directives')
           .controller('SingleBookController', ['$scope', 'ngDialog', function($scope, ngDialog){

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