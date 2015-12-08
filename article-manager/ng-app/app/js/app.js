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
.config(['$routeProvider', '$locationProvider', '$httpProvider', '$resourceProvider',
        function($routeProvider, $locationProvider, $httpProvider, $resourceProvider) {
            $routeProvider.
            when('/home', {
                    templateUrl: 'partials/home.html',
                    controller: 'homeCtrl'
                })
                .
            when('/signin', {
                    templateUrl: 'partials/signin.html',
                    controller: 'signinCtrl'
                })
                .
            when('/me', {
                    templateUrl: 'partials/me.html',
                    controller: 'userCtrl'
                })
                .
            when('/compositions', {
                    templateUrl: 'partials/compositions.html',
                    controller: 'compositionsListCtrl'
                })
                .
            when('/compositions/:compositionId', {
                    templateUrl: 'partials/composition-detail.html',
                    controller: 'compositionsDetailCtrl'
                })
                .
            when('/add-composition', {
                    templateUrl: 'partials/composition-edit.html',
                    controller: 'compositionsEditCtrl'
                })
                .
            when('/edit-composition/:compositionId', {
                    templateUrl: 'partials/composition-edit.html',
                    controller: 'compositionsEditCtrl'
                })
                .
            otherwise({
                redirectTo: '/signin'
            });

            $locationProvider.html5Mode(true);

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
                                $rootScope.userLogout();
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
