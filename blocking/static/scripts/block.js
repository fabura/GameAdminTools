/**
 * Created with IntelliJ IDEA.
 * User: bulat.fattahov
 * Date: 05.11.12
 * Time: 13:17
 */

seriesModule = angular.module('BlockApp', []);

function BlockCtrl($scope, $resource) {
    var Messages = $resource("/block/messages/:param");

    $scope.oldMessages = [];
    $scope.message = {title:'', text: '', id: ''};

    $scope.toBlockText = '';
    $scope.toBlock = [];

    $scope.getOldMessages = function () {
        Messages.get({param:'old'}, function (responce) {
            if (responce.data && ( responce.data instanceof  Array)) {
                var proto = {
                    select:function () {
                        $scope.message = this;
                        $scope.message.id = ''
                    }
                };
                for (message in responce.data) {
                    message.__proto__ = proto;
                    $scope.oldMessages = message;
                }
            }
        })
    }

    $scope.createToBlockList = function (){

    }


}



