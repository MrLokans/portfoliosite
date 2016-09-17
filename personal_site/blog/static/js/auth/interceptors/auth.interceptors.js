(function(){
    'use strict';
    angular.module('andersblog.auth.interceptors')
        .service('AuthInterceptor', ['$injector', '$location', function($injector, $location){
            var AuthInterceptor = {
                request: function(config){
                    var Auth = $injector.get('Auth');
                    var token = Auth.getToken();

                    if (token) {
                        config.headers['Authorization'] = 'JWT ' + token;
                    }
                    return config;
                },
                responseError: function(response){
                    if (response.status === 403){
                        $location.path('#/login');
                    }
                    return response;
                }
            };

            return AuthInterceptor;
    }]);

    // angular.module('andersblog.auth.controllers', []);
    // angular.module('andersblog.auth.interceptors', []);
    angular.module('andersblog.auth.services', []);

})();

