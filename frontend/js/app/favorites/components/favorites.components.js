(function(){
    'use strict';


    angular.module('andersblog.favorites.components')
           .component('favoritesList', {
                controller: 'FavoritesListController',
                templateUrl: 'favorites-list.html',
           })

           // TODO: investigate ng-repeat binding
           .component('favoriteLink', {
                // WARN: it is not currently working
                bindings: {
                    favLink: '=',
                },
                controller: 'FavoriteDetailController',
                templateUrl: 'favorite-link.html',
           });
})();