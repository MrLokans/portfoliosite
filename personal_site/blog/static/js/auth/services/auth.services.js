(function(){
    'use strict';
    angular.module('application.auth.services').
        service('Auth', function($http, $location, $q, $window){
            var Auth = {
                getToken: function(){
                    return $window.localStorage.getItem('token');
                },
                setToken: function(token){
                    $window.localStorage.setItem('token', token);
                },
                deleteToken: function(){
                    $window.localStorage.removeItem('token');
                },
                login: function(username, password){
                    var deffered = $q.defer();

                    $http.post('/api/token-auth/', {
                        username: username,
                        password: password
                    }).success(function(response, status, headers, config){
                        if (response.token){
                            Auth.setToken(response.token);
                        }
                        deffered.resolve(response, status, headers, config);
                    }).error(function(response, status, headers, confif){
                        deffered.reject(response, status, headers, confif);
                    });
                    return deffered.promise;
                },
                logout: function(){
                    Auth.deleteToken();
                    $window.location = '/';
                }
            };
            return Auth;
        });
})();