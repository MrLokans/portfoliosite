(function(){
    'use strict';

    angular.module('andersblog.about_me.services')
           .service('Skills', Skills)
           .service('Projects', Projects);

    Skills.$inject = ['$http', 'ENDPOINT'];
    Projects.$inject = ['$http', 'ENDPOINT'];

    function Skills($http, ENDPOINT){
        var Skills = {
            getSkills: function(){
                return $http.get(ENDPOINT.API_URL + '/api/technologies/');
            }
        };
        return Skills;
    }

    function Projects($http, ENDPOINT){
        var Projects = {
            getProjects: function(){
                return $http.get(ENDPOINT.API_URL + '/api/projects/');
            }
        };
        return Projects;
    }

})();