(function(){
    'use strict';
    angular.module('andersblog.about_me.services')
           .service('Skills', function($http){
                var Skills = {
                    getSkills: function(){
                        return $http.get('/api/technologies/');
                    }
                };
                return Skills;
           });

})();