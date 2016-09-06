(function(){
    'use strict';

    angular.module('andersblog', ['andersblog.posts',
                                  'andersblog.books',
                                  'andersblog.config',
                                  'andersblog.routes',
                                    ]);
    angular.module('andersblog.config', []);
    angular.module('andersblog.routes', ['ngRoute']);

    angular.module('andersblog').run(run);

    run.$inject = ['$http'];

    function run($http){
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }
})();