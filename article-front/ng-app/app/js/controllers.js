'use strict';

/* Controllers */

var articleControllers = angular.module('articleControllers', []);

articleControllers.controller('ArticleListCtrl', ['$scope', 'Suggest', 'Article',
  function($scope, Suggest, Article) {
    $scope.loading = false;
    $scope.suggests = [];
    $scope.currentpage = 0;

    $scope.triggerSuggest = function() {
      $scope.suggests = Suggest.query({title: $scope.searchquery});
    }
    $scope.setSearchQuery = function(suggest) {
      $scope.searchquery = suggest.text;
    }
    $scope.scrollExpand = function() {
      if (!$scope.articles || $scope.loading) return;
      $scope.loading = true;
      $scope.currentpage += 1;
      var more_articles = Article.query({search: $scope.searchquery, page: $scope.currentpage}, function() {
        for (var i = 0; i < more_articles.length; i++) {
          $scope.articles.push(more_articles[i]);
        }
        //$scope.articles.concat(more_articles);
        $scope.loading = false;
      });
    }
    $scope.triggerQuery = function() {
      // clear suggestion list
      $scope.suggests = [];
      $scope.currentpage = 0;
      $scope.articles = Article.query({search: $scope.searchquery, page: $scope.currentpage});
    }

  }]);

articleControllers.controller('ArticleDetailCtrl', ['$scope', '$routeParams', 'ArticleDetail',
  function($scope, $routeParams, ArticleDetail) {
    $scope.article = ArticleDetail.get({article_id: $routeParams.QueryId});
  }]);
