(function(){

'use strict';

/* Services */

var compositionAppServices = angular.module('compositionAppServices', ['ngResource']);

compositionAppServices.factory('authService', ['$http',
    function($http) {
        var baseUrl = "/api-token-auth";
        return {
            signin: function(data, success, error) {
                $http.post(baseUrl + '/signin/', data)
                    .success(success)
                    .error(error);
            },
            me: function(userid, success, error) {
                $http.get(baseUrl + '/me/' + userid + '/')
                    .success(success)
                    .error(error);
            },
            logout: function(success) {
                success();
            }
        };
    }
]);

compositionAppServices.factory('compositionService', ['$resource',
    function($resource) {
        return $resource('/composition/', {
            'format': 'json'
        }, {
            get_add_meta: {
                url: '/composition/',
                method: 'OPTIONS'
            },
            get_edit_meta: {
                url: '/composition/:compositionId/',
                method: 'OPTIONS'
            },
            get_detail: {
                url: '/composition/:compositionId/',
                method: 'GET'
            },
            put_detail: {
                url: '/composition/:compositionId/',
                method: 'PUT'
            },
            put_image: {
                url: '/composition/image/:compositionId/',
                method: 'PUT',
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        });
    }
]);

})();
