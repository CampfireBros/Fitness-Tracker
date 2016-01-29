'use strict';

// Declare templates level module which depends on views, and components
angular.module('myApp', ['ngRoute', 'ui.bootstrap', 'ngCookies'])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider
          .when('/', {
                templateUrl: 'static/partials/home.html',
                controller: HomeCtrl
          })
          .when('/signin', {
                templateUrl: 'static/partials/signin.html',
                controller: SignInCtrl
          })
          .when('/signup', {
                templateUrl: 'static/partials/signup.html',
                controller: SignUpCtrl
          })
            .when('/bodybuilding', {
                templateUrl: 'static/partials/bodybuilding.html',
                controller: BodyBuildingCtrl
          })
            .when('/powerlifting', {
                templateUrl: 'static/partials/powerlifting.html',
                controller: PowerliftingCtrl
          })
            .when('/crossfit', {
                templateUrl: 'static/partials/crossfit.html',
                controller: CrossfitCtrl
          })
            .when('/signup', {
                templateUrl: 'static/partials/signup.html',
                controller: SignUpCtrl
          })
            .when('/account', {
                templateUrl: 'static/partials/account.html',
                controller: AccountCtrl
          })
            .when('/tracker', {
                templateUrl: 'static/partials/tracker.html',
                controller: TrackerCtrl
          })
            .when('/bodyfat', {
                templateUrl: 'static/partials/bodyfat.html',
                controller: BodyFatCtrl
          })
          .otherwise({redirectTo: '/'});
    }])
    .run(["$rootScope", "$cookies", "$location", "$http", function ($rootScope, $cookies, $location, $http) {
        $rootScope.$on('$routeChangeSuccess', function(){
            ga('send', 'pageview', $location.path());
        });

        $rootScope.loggedIn = false;
        $rootScope.trackerStyle = '';
        $rootScope.styles = ['Body Building', 'Crossfit', 'Powerlifting'];
        $rootScope.login = angular.fromJson($cookies.getObject('login'));
        if(typeof $rootScope.login !== 'undefined') {
            $rootScope.token = $rootScope.login.token;
            $rootScope.name = $rootScope.login.name;
            $rootScope.style = $rootScope.login.style;

            $rootScope.loggedIn = true;
        }

        $rootScope.logout = function() {
            $rootScope.loggedIn = false;
            $cookies.remove('login');
            $location.path('/');
        };

        $rootScope.muscleExercises = {};

        $http({
            method: 'GET',
            url: '/exercises/getMuscles'
        }).then(function successCallback(response) {
            $rootScope.muscles = response['data']['data'];
            $rootScope.exercisesForEachMuscle();
        }, function errorCallback(response) {
        });

        $rootScope.exercisesForEachMuscle = function() {
            if (typeof $rootScope.muscles !== 'undefined') {
                $rootScope.muscles.forEach(function (ele, index, arr) {
                    $http({
                        method: 'GET',
                        url: '/exercises/exercisesForMuscle/' + ele
                    }).then(function successCallback(response) {
                        $rootScope.muscleExercises[ele] = response['data']['data'];
                    }, function errorCallback(response) {
                    });
                });
            }
        }
    }]);
