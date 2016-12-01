(function(){
    'use strict';

    angular.module('andersblog.posts',
        [
         'andersblog.posts.controllers',
         'andersblog.posts.services',
         'andersblog.posts.directives',
         ]);
    angular.module('andersblog.posts.controllers', []);
    angular.module('andersblog.posts.services', ['ngResource']);
    angular.module('andersblog.posts.directives', []);
})();