(function(){
    'use strict';

    angular.module('andersblog.books',
        [
         'andersblog.books.controllers',
         'andersblog.books.services',
         'andersblog.books.directives',
         ]);
    angular.module('andersblog.books.controllers', ['ngDialog']);
    angular.module('andersblog.books.services', ['ngResource']);
    angular.module('andersblog.books.directives', []);
})();