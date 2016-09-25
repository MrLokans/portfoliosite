(function(){
    'use strict';
    angular.module('andersblog.about_me.controllers')
           .controller('SkillsController', SkillsController)
           .controller('ProjectsController', ProjectsController);

            SkillsController.$inject = ['$http', '$scope', '$log', 'Skills'];
            ProjectsController.$inject = ['$http', '$scope', '$log', 'Projects'];

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

            function ProjectsController($http, $scope, $log, Projects){

                Projects.getProjects().then(getProjectsSuccessFn, getProjectsErrFn);

                function getProjectsSuccessFn(data, status, headers, config){
                    $scope.projects = data.data;
                    $log.debug($scope.projects);
                }
                function getProjectsErrFn(data, status, headers, config){
                    $scope.projects = null;
                    $log.error('Error obtaining projects');
                }
            }
})();