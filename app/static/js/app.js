'use strict';

// Declare templates level module which depends on views, and components
angular.module('myApp', ['ngRoute', 'ui.bootstrap'])
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
          .otherwise({redirectTo: '/'});
    }])
    .run(["$rootScope", function ($rootScope) {
            $rootScope.loggedIn = false;
    }]);
