'use strict';

/* Services */

var articleServices = angular.module('articleServices', ['ngResource']);

articleServices.factory('Suggest', ['$resource',
  function($resource){
    return $resource('/title_suggestion', {title:'@searchquery'}, {});
  }]);

articleServices.factory('Article', ['$resource',
  function($resource){
    return $resource('/query_match', {search:'@searchquery', page:'@currentpage'}, {});
  }]);

articleServices.factory('ArticleDetail', ['$resource',
  function($resource){
    return $resource('/query_detail', {article_id:'@article_id'}, {});
  }]);
