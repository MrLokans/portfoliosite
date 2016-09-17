(function(){
    'use strict';
    angular.module('andersblog.auth.services').
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
                    }).error(function(response, status, headers, config){
                        deffered.reject(response, status, headers, config);
                    });
                    return deffered.promise;
                },
                logout: function(){
                    Auth.deleteToken();
                    $window.location = '/';
                },
                register: function(user){
                    var deffered = $q.defer();

                    $http.post('/api/register/', {
                        user: user
                    }).success(function(response, status, headers, config){
                        Auth.login(user.username, user.password).
                            then(function(response, status, headers, config){
                                $window.location = '/';
                            });
                        deffered.resolve(response, status, headers, config);
                    }).error(function() {
                        deffered.reject(response, status, headers, config);
                    });
                    return deffered.promise;
                }
            };
            return Auth;
        });
})();