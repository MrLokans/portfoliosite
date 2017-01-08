(function(){
    'use strict';

    angular.module('andersblog.favorites.controllers')
           .controller('FavoriteDetailController', FavoriteDetailController)
           .controller('FavoritesListController', FavoritesListController);

    FavoriteDetailController.$inject = ['$scope', '$log', '$http', 'ngDialog', 'Favorites'];
    FavoritesListController.$inject = ['$scope', '$log', '$http', '$routeParams', 'Favorites'];

    function FavoriteDetailController($scope, $log, $http, ngDialog, Favorites){
        var self = this;
    }


    function FavoritesListController($scope, $log, $http, $routeParams, Favorites){
        var self = this;
        this.$onInit = function(){
            $log.debug('Loading list of favorites on controller init.');

            Favorites.getAllFavorites()
                .then(successFn, errorFn);

            function successFn(response){
                $log.debug("Favorites list loaded.");
                self.favorites = response.data;
            }
            function errorFn(error){
                $log.error("Error getting favorites list: " + error.message);
            }
        };
    }

})();