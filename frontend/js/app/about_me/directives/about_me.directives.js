(function(){
    'use strict';
    angular.module('andersblog.about_me.directives')
       .directive('skillList', function(){
            return {
                restrict: 'E',
                controller: 'SkillsController',
                templateUrl: 'skill-list.html'
            };
       })
       .directive('skillSingle', function(){
            return {
                restrict: 'E',
                scope: {
                    skill: '=',
                },
                templateUrl: 'skill-single.html'
            };
       });
})();