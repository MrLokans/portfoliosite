(function(){
    'use strict';
    angular.module('andersblog.config')
        .config(['$httpProvider', '$locationProvider', function($httpProvider, $locationProvider){
            $httpProvider.interceptors.push('AuthInterceptor');
        }])
        .config(['$resourceProvider', function($resourceProvider) {
          // Don't strip trailing slashes from calculated URLs
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }]);
    
})();