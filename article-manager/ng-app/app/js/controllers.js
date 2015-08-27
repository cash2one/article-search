(function(){

'use strict';

/* Controllers */

angular.module('compositionAppControllers', ['ngStorage'])
.controller('HomeCtrl', ['$rootScope', '$scope', '$location', '$localStorage', 'authService', 'compositionService',
    function($rootScope, $scope, $location, $localStorage, authService, compositionService) {
        // helper functions
        function changeUser(user) {
            angular.extend($rootScope.gCurrentUser, user);
        }

        function getUserFromLocal() {
            var token = $localStorage.token;
            var user = {};
            if (typeof token !== 'undefined') {
                user = jwt_decode(token);
                // console.log(user);
            }
            return user;
        }

        function changePath(url) {
            $location.path(url);
            // console.log('change to url:'+url);
        }

        // load user meta
        function loadUserMeta(user_id) {
            authService.me(user_id,
                function(userMeta) {
                    $rootScope.gUserMeta = userMeta;
                    // cache user meta to local
                    $localStorage.userMeta = userMeta;
                    changePath("/");
                },
                function() {
                    $rootScope.gUserMeta = null;
                    alert("get user meta failed");
                    changePath("/");
                });
        }

        $scope.signin = function() {
            var formData = {
                username: $scope.username,
                password: $scope.password
            };
            authService.signin(formData, function(res) {
                if (res.token) {
                    // set scope varible state
                    $rootScope.gToken = res.token;
                    // cache token to local
                    $localStorage.token = res.token;
                    var currentUser = getUserFromLocal();
                    changeUser(currentUser);
                    // load user info
                    loadUserMeta(currentUser.user_id);
                } else {
                    alert('Network error, Failed to signin');
                }
            }, function() {
                alert('Username or password error, Failed to signin');
            });
        };

        $scope.logout = function() {
            authService.logout(function() {
                // clear scope varible state
                delete $rootScope.gToken;
                delete $rootScope.gUserMeta;
                delete $localStorage.token;
                changeUser({});
                changePath("/");
            });
        };

        // controller init
        $rootScope.gToken = $localStorage.token;
        $rootScope.gCurrentUser = getUserFromLocal();
        $rootScope.gUserMeta = $localStorage.userMeta;
        $scope.signinError = null;
    }
])

.controller('compositionsListCtrl', ['$scope', 'compositionService',
    function($scope, compositionService) {
        $scope.scrollExpand = function() {
            if (!$scope.compositions || $scope.loading) return;
            $scope.loading = true;
            var more_compositions = compositionService.get({
                    page: $scope.currentpage
                },
                function() {
                    for (var i = 0; i < more_compositions.results.length; i++) {
                        $scope.compositions.push(more_compositions.results[i]);
                    }
                    //$scope.compositions.concat(more_compositions.results);
                    $scope.loading = false;
                });
            $scope.currentpage += 1;
        };

        // controller init
        $scope.loading = false;
        $scope.currentpage = 1;
        $scope.compositions = [];
    }
])

.controller('userCtrl', ['$rootScope', '$scope', '$location', 'authService',
    function($rootScope, $scope, $location, authService) {
        // controller init
        if ($rootScope.gCurrentUser) {
            authService.me($rootScope.gCurrentUser.user_id,
                function(userData) {
                    $scope.myDetails = userData;
                },
                function() {
                    alert("get user detail failed");
                    $scope.logout();
                });
        } else {
            alert("user login error");
            $scope.logout();
        }
    }
])

.controller('compositionsEditCtrl', ['$rootScope', '$scope', '$location', '$routeParams', 'Upload', 'compositionService',
    function($rootScope, $scope, $location, $routeParams, Upload, compositionService) {
        $scope.insertCompositionSuccess = function(msg) {
            alert(msg);
            $location.path("/");
        };

        $scope.UpdateCompositionImage = function(id, msg) {
            if ($scope.uploadImage) {
                Upload.upload({
                        method: 'PUT',
                        fields: {
                            'format': 'api'
                        },
                        url: '/backend/composition/image/' + id + '/',
                        file: $scope.uploadImage,
                        fileFormDataName: 'image'
                    })
                    .progress(function(evt) {
                        var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                        console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
                    })
                    .success(function(data, status, headers, config) {
                        //console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
                        $scope.insertCompositionSuccess(msg);
                    })
                    .error(function(data, status, headers, config) {
                        console.log('error status: ' + status);
                    });
            }
        };

        $scope.AddOrUpdateComposition = function() {
                if ($scope.compositionEdit && $scope.compositionEdit.id) {
                    // update existed composition
                    compositionService.put_detail({
                            compositionId: $routeParams.compositionId
                        },
                        $scope.compositionEdit,
                        function() {
                            if ($scope.uploadImage) {
                                // upload image
                                $scope.UpdateCompositionImage($routeParams.compositionId, "审核成功！");
                            } else {
                                // change to detail page
                                //$location.path('/compositions/'+$routeParams.compositionId+'/');
                                $scope.insertCompositionSuccess("审核成功！");
                            }
                        }
                    );
                } else {
                    // add new composition
                    var comData = compositionService.save({}, $scope.compositionEdit,
                        function() {
                            if ($scope.uploadImage) {
                                // upload image
                                $scope.UpdateCompositionImage(comData.id, "录入成功！");
                            } else {
                                // change to detail page
                                $scope.insertCompositionSuccess("录入成功！");
                            }
                        }
                    );
                }
            }; // end of AddOrUpdateComposition

        $scope.cancelEdit = function() {
            $location.path("/");
        };

        // load meta info
        function loadCompositionMeta(type, id) {
            if ($scope.gradeOptions && $scope.atypeOptions) {
                // meta info loaded already
                return;
            }
            var hFail = function() {
                alert('Get composition meta failed');
                $scope.cancelEdit();
            };
            if (type == 'add') {
                compositionService.get_add_meta({},
                    function(meta) {
			$scope.compostionMeta = meta.actions.POST;
                        $scope.gradeOptions = meta.actions.POST.grade.choices;
                        $scope.atypeOptions = meta.actions.POST.atype.choices;
                    }, hFail);
            } else if (type == 'edit') {
                compositionService.get_edit_meta({
                        compositionId: id
                    },
                    function(meta) {
			$scope.compostionMeta = meta.actions.PUT;
                        $scope.gradeOptions = meta.actions.PUT.grade.choices;
                        $scope.atypeOptions = meta.actions.PUT.atype.choices;
                    }, hFail);
            } else {
                alert("operation type error");
                $scope.cancelEdit();
            }
        }

        // controller init
	$scope.taToolbarConfig = [
		['h1', 'h2', 'h3', 'h4', 'p', 'pre', 'quote'],
		['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
		['justifyLeft', 'justifyCenter', 'justifyRight', 'indent', 'outdent'],
		['html', 'wordcount', 'charcount']
	];
        $scope.compositionEdit = null;
	$scope.compostionMeta = null;
        if ($routeParams.compositionId) {
            // edit existed composition
            loadCompositionMeta('edit', $routeParams.compositionId);
            var compositionEdit = compositionService.get_detail({
                    compositionId: $routeParams.compositionId
                },
                function() {
                    // set composition detail after load
                    $scope.compositionEdit = compositionEdit;
                },
                function() {
                    alert("get composition failed");
                    $location.path("/compositions");
                }
            );
        } else {
            // add new composition
            // use empty compositionEdit object
            loadCompositionMeta('add');
            $scope.compositionEdit = null;
        }
    }
])

.controller('compositionsDetailCtrl', ['$scope', '$location', '$routeParams', 'compositionService',
    function($scope, $location, $routeParams, compositionService) {
        // controller init
        compositionService.get_detail({
                compositionId: $routeParams.compositionId
            },
            function(compositionDetail) {
                $scope.compositionDetail = compositionDetail;
            });
    }
]);

})();
