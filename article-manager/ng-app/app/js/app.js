(function(){

'use strict';

/* App Module */

angular.module('compositionApp', [
    'ngStorage',
    'ngRoute',
    'ngAnimate',
    'infinite-scroll',
    'angular-loading-bar',
    'textAngular',
    'ngFileUpload',
    'ngTagsInput',

    'compositionAppControllers',
    'compositionAppServices'
])
.config(['$routeProvider', '$httpProvider', '$resourceProvider',
        function($routeProvider, $httpProvider, $resourceProvider) {
            $routeProvider.
            when('/', {
                    templateUrl: 'partials/home.html',
                    controller: 'HomeCtrl'
                })
                .
            when('/signin', {
                    templateUrl: 'partials/signin.html',
                    controller: 'HomeCtrl'
                })
                .
            when('/me', {
                    templateUrl: 'partials/me.html',
                    controller: 'HomeCtrl'
                })
                .
            when('/compositions', {
                    templateUrl: 'partials/compositions.html',
                    controller: 'HomeCtrl'
                })
                .
            when('/compositions/:compositionId', {
                    templateUrl: 'partials/composition-detail.html',
                    controller: 'HomeCtrl'
                })
                .
            when('/add-composition', {
                    templateUrl: 'partials/composition-edit.html',
                    controller: 'HomeCtrl'
                })
                .
            when('/edit-composition/:compositionId', {
                    templateUrl: 'partials/composition-edit.html',
                    controller: 'HomeCtrl'
                })
                .
            otherwise({
                redirectTo: '/signin'
            });

            $httpProvider.interceptors.push(['$q', '$rootScope', '$location', '$localStorage',
                function($q, $rootScope, $location, $localStorage) {
                    return {
                        'request': function(config) {
                            config.headers = config.headers || {};
                            if ($localStorage.token) {
                                config.headers.Authorization = 'JWT ' + $localStorage.token;
                            }
                            return config;
                        },
                        'responseError': function(response) {
                            if (response.status === 401 || response.status === 403) {
                                delete $rootScope.token;
                                delete $localStorage.token;
                                delete $rootScope.currentUser;
                                $location.path('/signin');
                            }
                            return $q.reject(response);
                        }
                    };
                }
            ]);

            $resourceProvider.defaults.stripTrailingSlashes = false;
        }
    ])
    .run(function($rootScope, $location) {
        $rootScope.$on("$routeChangeStart", function(event, next, current) {
            if ($rootScope.gCurrentUser === null) {
                // no logged user, redirect to /login
                if (next.templateUrl === "partials/signin.html") {
                    // pass
                } else {
                    $location.path("/signin");
                }
            }
        });
    });

})();
