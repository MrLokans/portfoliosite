(function(){
    'use strict';
    angular.module('andersblog.config')
        .config(['markedProvider', function (markedProvider) {
          markedProvider.setOptions({
            gfm: true,
            tables: true,
            highlight: function (code, lang) {
              if (lang) {
                return hljs.highlight(lang, code, true).value;
              } else {
                return hljs.highlightAuto(code).value;
              }
            }
          });
        }])
        .config(['$httpProvider', '$locationProvider', function($httpProvider, $locationProvider){
            $httpProvider.interceptors.push('AuthInterceptor');
        }])
        .config(['$resourceProvider', function($resourceProvider) {
          // Don't strip trailing slashes from calculated URLs
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }]);
    
})();