(function(){
    'use strict';

    angular.module('andersblog', ['andersblog.posts']);
    angular.module('andersblog').run(run);

    run.$inject = ['$http'];

    function run($http){
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }
})();