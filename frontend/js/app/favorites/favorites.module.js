(function(){
    'use strict';

    angular.module('andersblog.favorites',
        [
         'andersblog.favorites.controllers',
         'andersblog.favorites.services',
         'andersblog.favorites.components',
         ]);
    angular.module('andersblog.favorites.controllers', []);
    angular.module('andersblog.favorites.services', ['ngResource']);
    angular.module('andersblog.favorites.components', []);
})();