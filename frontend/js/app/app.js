(function(){
    'use strict';

    angular.module('andersblog', ['andersblog.constants',
                                  'andersblog.auth',
                                  'andersblog.posts',
                                  'andersblog.books',
                                  'andersblog.about_me',
                                  'andersblog.favorites',
                                  'andersblog.config',
                                  'andersblog.filters',
                                  'andersblog.routes',
                                  'angulartics',
                                  'angulartics.google.analytics']);
    angular.module('andersblog.constants', []);
    angular.module('andersblog.config', []);
    angular.module('andersblog.routes', ['ngRoute']);
    angular.module('andersblog.filters', []);

    angular.module('andersblog').run(run);

    run.$inject = ['$http'];

    function run($http){
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }
})();