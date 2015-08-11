'use strict';

/* App Module */

var articleApp = angular.module('articleApp', [
  'ngRoute',
  'ngSanitize',

  'infinite-scroll',
  'articleControllers',
  'articleServices'
]);

articleApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/articles', {
        templateUrl: 'partials/article-list.html',
        controller: 'ArticleListCtrl'
      }).
      when('/articles/:QueryId', {
        templateUrl: 'partials/article-detail.html',
        controller: 'ArticleDetailCtrl'
      }).
      otherwise({
        redirectTo: '/articles'
      });
  }]);
