(function(){

'use strict';

/* Controllers */

angular.module('compositionAppControllers', ['ngStorage'])
.controller('rootCtrl', ['$rootScope', '$scope', '$location', '$localStorage', 'authService',
    function($rootScope, $scope, $location, $localStorage, authService) {
        // helper functions
        function changePath(url) {
            $location.path(url);
            console.log('change to url: '+url);
        }

        // load user meta
        function loadUserMeta(userId, onUserMetaLoaded) {
            if (!userId) {
                console.log('cannot get userId');
                return;
            }
            authService.me(userId,
                function(userMeta) {
                    // cache user meta to local
                    $localStorage.userMeta = userMeta;
                    $scope.gUserMeta = userMeta;
                    if (onUserMetaLoaded) {
                        onUserMetaLoaded(userMeta);
                    }
                },
                function() {
                    console.log("get user meta failed");
                });
        }

        $scope.resetUser = function() {
            // clear scope varible state
            delete $scope.gUserMeta;
            delete $scope.gCurrentUser;
            // clean localStorage
            delete $localStorage.token;
            delete $localStorage.userMeta;
        }

        // get data from localStorage
        $scope.refreshUser = function(onUserMetaLoaded) {
            $scope.gCurrentUser = $rootScope.getUserFromLocal();
            if ($scope.gCurrentUser) {
                loadUserMeta($scope.gCurrentUser.user_id, onUserMetaLoaded);
            } else {
                changePath('/signin');
            }
        }

        $scope.userLogout = function() {
            $rootScope.userLogout();
        };

        // common functions
        $rootScope.getUserFromLocal = function() {
            var token = $localStorage.token;
            var user = null;
            if (token) {
                user = jwt_decode(token);
                console.log(user);
            }
            return user;
        }

        $rootScope.userLogin = function(formData) {
            console.log("user login");
            authService.signin(formData, function(res) {
                if (res.token) {
                    // cache token to local
                    $localStorage.token = res.token;
                    // set scope varible state
                    $scope.refreshUser(null);
                    changePath("/home");
                } else {
                    alert('Network error, Failed to signin.');
                    changePath("/signin");
                }
            }, function() {
                alert('Username or password error, Failed to signin.');
                changePath("/signin");
            });
        };

        $rootScope.userLogout = function() {
            console.log("user logout");
            authService.logout(function() {
                $scope.resetUser();
                $scope.refreshUser(null);
            });
        };

        $rootScope.refreshUser = function(onUserMetaLoaded) {
            $scope.refreshUser(onUserMetaLoaded);
        }

        $rootScope.resetUser = function() {
            $scope.resetUser();
        }

        // controller 
        console.log('start init');
        $scope.refreshUser(null);
        
    }
])

.controller('homeCtrl', ['$rootScope', '$scope',
    function($rootScope, $scope) {
        // controller init
        console.log("home page");
        // $rootScope.refreshUser(null);
        $scope.introduction = "该系统分为两种角色：录入员和审核员";
    }
])

.controller('signinCtrl', ['$rootScope', '$scope',
    function($rootScope, $scope) {
        $scope.signin = function() {
            var formData = {
                username: $scope.username,
                password: $scope.password
            };
            $rootScope.userLogin(formData);
        };

        $scope.logout = function() {
            $rootScope.userLogout();
        };

        // controller init
        console.log("sign page");
        $rootScope.resetUser();
        // $rootScope.refreshUser(null);
    }
])

.controller('compositionsListCtrl', ['$rootScope', '$scope', 'compositionService',
    function($rootScope, $scope, compositionService) {
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
        $rootScope.refreshUser(null);

        $scope.loading = false;
        $scope.currentpage = 1;
        $scope.compositions = [];
    }
])

.controller('userCtrl', ['$rootScope', '$scope', '$location', 'authService',
    function($rootScope, $scope, $location, authService) {
        // controller init
        $rootScope.refreshUser(null);

        var currentUser = $rootScope.getUserFromLocal()
        if (currentUser) {
            authService.me(currentUser.user_id,
                function(userData) {
                    $scope.myDetails = userData;
                },
                function() {
                    console.error("get user detail failed");
                    $rootScope.userLogout();
                });
        } else {
            console.error("user login error");
            $rootScope.userLogout();
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
        $rootScope.refreshUser(null);
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

.controller('compositionsDetailCtrl', ['$rootScope', '$scope', '$location', '$routeParams', 'compositionService',
    function($rootScope, $scope, $location, $routeParams, compositionService) {
        // controller init
        $rootScope.refreshUser(null);
        compositionService.get_detail({
                compositionId: $routeParams.compositionId
            },
            function(compositionDetail) {
                $scope.compositionDetail = compositionDetail;
            });
    }
]);

})();
