'use strict';

/* Controllers */


function HomeCtrl($scope) {

}

function SignInCtrl($scope) {

}

function SignUpCtrl($scope) {
    $scope.addUser = function() {
        console.log($scope.email);
        console.log($scope.password);
    }
}
