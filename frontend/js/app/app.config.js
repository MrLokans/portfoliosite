(function(){
    'use strict';
    angular.module('andersblog.config')
        .config(function($httpProvider, $locationProvider){
            $httpProvider.interceptors.push('AuthInterceptor');
        });
    
})();