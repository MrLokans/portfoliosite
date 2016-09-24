(function(){
    'use strict';
    angular.module('andersblog.filters')
           .filter('skillLevelizer', function(){
                return function(item){
                    var levels = {
                        1: 'novice',
                        2: 'intermediate',
                        3: 'advanced'
                    };
                    if (item.toString() in levels){
                        return levels[item.toString()];
                    } else {
                        return 'unknown';
                    }
                };
           });
})();