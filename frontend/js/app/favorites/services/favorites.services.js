(function(){
    'use strict';

    angular.module('andersblog.favorites.services')
           .factory('Favorites', Favorites);

    Favorites.$inject = ['$http', '$resource', 'ENDPOINT'];

    var FAVORITES_ENDPOINT = '/api/favorites/';

    function Favorites($http, $resource, ENDPOINT){
        return {
            getAllFavorites: getAllFavorites,
            getOneFavorite: getOneFavorite,
            createFavorite: createFavorite,
            deleteFavorite: deleteFavorite,
        };

        function getAllFavorites(){
            return $http.get(ENDPOINT.API_URL + FAVORITES_ENDPOINT);
        }

        function getOneFavorite(favoriteID){
            return $http.get(ENDPOINT.API_URL + FAVORITES_ENDPOINT + favoriteID + '/');
        }

        function createFavorite(favoriteData){
            return $http.post(ENDPOINT.API_URL + FAVORITES_ENDPOINT, favoriteData);
        }

        function deleteFavorite(favoriteID){
            return $http.delete(ENDPOINT.API_URL + FAVORITES_ENDPOINT + favoriteID + '/');
        }
    }
})();