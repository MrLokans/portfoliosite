(function(){
    'use strict';
    angular.module('andersblog.about_me.controllers')
           .controller('SkillsController', SkillsController)
           .controller('ProjectsController', ProjectsController)
           .controller('AboutController', AboutController);

            AboutController.$inject = ['$scope'];
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

            function AboutController($scope){
                // TODO: possible memory leak, find a better way to organise it
                $scope.workInfo = [
                    {
                      id: 1,
                      content: 'Gymnasium #42',
                      start: '2013-05-16',
                      end: '2014-06-16'
                    },

                    {
                      id: 2, 
                      content: 'VPI Photonics', 
                      start: '2014-07-16', 
                      end: '2016-07-16'
                    },
                    {
                      id: 3,
                      content: 'itransition',
                      start: '2016-07-18',
                      end: new Date()
                    }
                ];
                var container = document.getElementById('work-timeline');
                var items = new vis.DataSet($scope.workInfo);
                var options = {};
                var timeline = new vis.Timeline(container, items, options);
            }
})();