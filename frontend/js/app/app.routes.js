(function(){
    'use strict';

    angular.module('andersblog.routes')
           .config(config);
    config.$inject = ['$routeProvider', '$locationProvider'];



    function config($routeProvider, $locationProvider){
        // $locationProvider.html5Mode(true);
        $routeProvider
            .when('/projects', {
                templateUrl: 'projects.html',
                controller: "ProjectsController"
            })
            .when('/blog', {
                templateUrl: 'blog.html',
            })
            .when('/contacts', {
                templateUrl: 'contacts.html',
            })
            .when('/blog/:post_id', {
                templateUrl: 'post-details.html',
                controller: "PostDetailController",
            })
            .when('/books', {
                templateUrl: 'books.html'
            })
            .when('/books/:book_id', {
                templateUrl: 'book-details.html',
                controller: "BookDetailController",
            })
            .when('/about_me', {
                templateUrl: 'about_me.html',
                controller: "AboutController",
                controllerAs: "vm"
            })
            .when('/favorites', {
                templateUrl: 'favorites.html',
            })
            .when('/', {
                redirectTo: '/about_me'
            }).
            otherwise('/about_me');
    }
})();