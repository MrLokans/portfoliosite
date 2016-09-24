(function(){
    'use strict';
    angular.module('andersblog.about_me.controllers')
           .controller('SkillsController', SkillsController);

            SkillsController.$inject = ['$http', '$scope', '$log', 'Skills'];

            function SkillsController($http, $scope, $log, Skills){

                Skills.getSkills().then(getSkillsSuccessFn, getSkillsErrFn);

                function getSkillsSuccessFn(data, status, headers, config){
                    $scope.skills = data.data;
                    $log.debug($scope.skills);
                }
                function getSkillsErrFn(data, status, headers, config){
                    $log.error('Error obtaining skills');
                }
            }
})();