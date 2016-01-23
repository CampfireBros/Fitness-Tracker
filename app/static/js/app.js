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
          .otherwise({redirectTo: '/'});

}]);
