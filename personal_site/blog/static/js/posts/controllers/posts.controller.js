(function(){
    'use strict';

    angular.module('andersblog.posts.controllers')
           .controller('PostListController', PostListController)
           .controller('AboutController', AboutController)
           .controller('ProjectController', ProjectController);

    PostListController.$inject = ['$scope', '$http', 'Subscription'];
    AboutController.$inject = ['$scope'];
    ProjectController.$inject = ['$scope'];

    function PostListController($scope, $http, Subscription){
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

    function ProjectController($scope){
        $scope.projects = [
            {
                'title': 'Personal Site',
                'description': 'This site itself. Personal blog, portfolio site, playground for experiments.',
                'url': '/',
                'links': [{'type': 'github', 'url': 'https://github.com/MrLokans/portfoliosite'}],
            },
            {
                'title': 'ISP coverage Map',
                'description': ' Map of Belarus high-speed internet access. Each point represents house with some ISP availability. Blue represents ByFly \'s XPON, red - MTS ethernet, purple - Unet.by.',
                'url': '/projects/providers',
                'links': [{'type': '', 'url': ''}],
            },
            {
                'title': 'MoonReader tools',
                'description': 'Python library to parse <a href="http://www.moondownload.com/">MoonReader</a> syncronization formats.',
                'url': 'https://github.com/MrLokans/MoonReader_tools',
                'links': [
                    {'type': 'github', 'url': 'https://github.com/mrlokans/moonreader_tools'},
                    {'type': 'PyPI', 'url': 'https://pypi.python.org/pypi/moonreader_tools'}
                ],
            },
            {
                'title': 'TelegramBot',
                'description': 'Telegram bot that displays currency exchange rates for several belarusian banks and also shows some pretty plots.',
                'url': 'https://github.com/MrLokans/bank_telegram_bot',
                'links': [{'type': 'Github', 'url': 'https://github.com/MrLokans/bank_telegram_bot'}],
            },
            {
                'title': 'IT Books spider',
                'description': 'Scrapy spider that parsers diffrent sites like onliner.by and grabs latest book data, in search of cheap IT books.',
                'url': 'https://github.com/MrLokans/IT_books_spider',
                'links': [{'type': 'Github', 'url': 'https://github.com/MrLokans/IT_books_spider'}],
            },
            {
                'title': 'Koshelek.org exporter',
                'description': 'Exports CSV data about incomes and spendings from <a href="https://koshelek.org/">koshelek.org</a> website',
                'url': 'https://github.com/MrLokans/KoshelekOrgExporter',
                'links': [{'type': 'Github', 'url': 'https://github.com/MrLokans/KoshelekOrgExporter'}],
            },
            {
                'title': 'VK API',
                'description': 'Simple library that wraps requests to <a href="https://new.vk.com/dev/methods">vkontakte API</a>.',
                'url': 'https://github.com/MrLokans/vk_api',
                'links': [{'type': 'Github', 'url': 'https://github.com/MrLokans/vk_api'}],
            },
        ];
    }
})();