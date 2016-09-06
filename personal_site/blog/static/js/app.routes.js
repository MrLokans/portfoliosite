(function(){
    'use strict';

    angular.module('andersblog.routes')
           .config(config);
    config.$inject = ['$routeProvider', '$locationProvider'];



    function config($routeProvider, $locationProvider){
        // $locationProvider.html5Mode(true);
        $routeProvider
            // .when('/', {
            //     template: 'test'
            // })
            .when('/projects', {
                templateUrl: 'projects.html',
                controller: "ProjectController"
            })

            .when('/blog', {
                templateUrl: 'blog.html',
            })

            .when('/books', {
                templateUrl: 'books.html'
            })

            .when('/about_me', {
                templateUrl: 'about_me.html',
                controller: "AboutController",
                controllerAs: "vm"
        }).otherwise('/');
    }
})();